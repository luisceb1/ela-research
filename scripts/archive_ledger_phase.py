"""Manifest-bound bounded tar.gz extraction, with no network or production CLI.

Regular tar headers and parent directories only. PAX/GNU extension records are
rejected at the header, before allocating metadata payload. A directory/receipt
alone never certifies outputs; the verified ledger must also match.
"""
import gzip
import hashlib
import json
import os
from pathlib import Path,PurePosixPath
import re
import tarfile

from artifact_checksums import validate_expected
from paired_fastq_integrity import file_digest
from paired_fastq_phase import digest,sha
from process_supervisor_v2 import atomic_json

POLICY='bounded-tar-gzip-ledger-v1'
CHUNK=65536


def safe_name(name):
    if not isinstance(name,str) or not name or len(name)>512 or '\\' in name or any(ord(c)<33 or ord(c)>126 for c in name):raise ValueError('Unsafe tar path')
    path=PurePosixPath(name)
    if not path.parts or path.is_absolute() or str(path)!=name or any(p in ('.','..') or len(p)>255 for p in path.parts):raise ValueError('Noncanonical tar path')
    return name


def contract(runner,name):
    if not isinstance(name,str) or not re.fullmatch('[A-Za-z0-9_-]+',name):raise ValueError('Invalid archive phase name')
    spec=runner.manifest.get('archives',{}).get(name)
    keys={'transfer','identity','expected','members','max_members','max_expanded_bytes','max_tar_bytes'}
    if not isinstance(spec,dict) or set(spec)!=keys:raise ValueError('Archive manifest contract required')
    transfer=spec['transfer']
    if not isinstance(transfer,str) or not re.fullmatch('[A-Za-z0-9_-]+',transfer) or not isinstance(spec['identity'],str) or not spec['identity']:raise ValueError('Archive identity required')
    validate_expected(spec['expected'])
    if spec['expected'].get('sha256') is None:raise ValueError('Archive requires pinned SHA256')
    for key in ('max_members','max_expanded_bytes','max_tar_bytes'):
        if type(spec[key]) is not int or spec[key]<=0:raise ValueError('Positive archive caps required')
    members=spec['members']
    if not isinstance(members,list) or not members or len(members)>spec['max_members']:raise ValueError('Bounded nonempty inventory required')
    names=set()
    for item in members:
        if not isinstance(item,dict) or set(item)!={'name','bytes','sha256'}:raise ValueError('Member size/SHA256 required')
        name_in_tar=safe_name(item['name']);validate_expected({'bytes':item['bytes'],'sha256':item['sha256']})
        if name_in_tar in names:raise ValueError('Duplicate manifest member')
        names.add(name_in_tar)
    if any(str(parent) in names for n in names for parent in PurePosixPath(n).parents if str(parent)!='.'):raise ValueError('File/directory inventory collision')
    expected_total=sum(m['bytes'] for m in members)
    if expected_total>spec['max_expanded_bytes'] or expected_total+1024>spec['max_tar_bytes']:raise ValueError('Inventory exceeds archive caps')
    phase=runner.state['phases'].get(transfer,{})
    if phase.get('kind')!='transfer' or phase.get('status')!='verified':raise ValueError('Verified archive transfer required')
    if phase.get('bytes')!=spec['expected']['bytes'] or phase.get('sha256')!=spec['expected']['sha256'] or (spec['expected'].get('md5') is not None and phase.get('md5')!=spec['expected']['md5']):raise ValueError('Archive transfer/manifest mismatch')
    if (runner.root/transfer).is_symlink() or file_digest(runner.root/transfer,runner.guard)!={'bytes':phase['bytes'],'sha256':phase['sha256']}:raise ValueError('Archive source changed')
    binding={'policy':POLICY,'spec':spec,'fingerprint':runner.state['fingerprint'],'transfer_receipt_sha256':digest(phase)}
    if 'attempts_used' in phase:
        receipt=runner.root/f"{transfer}.attempt-{phase['attempts_used']-1}.json";rec=json.loads(receipt.read_text())
        if rec.get('status')!='verified' or rec.get('body_bytes')!=phase['bytes'] or any(rec.get(k)!=phase[k] for k in ('md5','sha256')):raise ValueError('Incomplete HTTP receipt')
        binding['http_receipt_sha256']=sha(receipt)
    return binding,digest(binding)


def fsync_directory(path):
    fd=os.open(path,os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)


class TarReader:
    def __init__(self,stream,cap,guard):self.stream=stream;self.cap=cap;self.guard=guard;self.bytes=0
    def read(self,n):
        self.guard();n=min(n,CHUNK,self.cap-self.bytes+1)
        if n<=0:raise ValueError('Tar stream cap exceeded')
        data=self.stream.read(n);self.bytes+=len(data)
        if self.bytes>self.cap:raise ValueError('Tar stream cap exceeded')
        return data
    def exact(self,n):
        chunks=[]
        while n:
            data=self.read(n)
            if not data:raise ValueError('Truncated tar stream')
            chunks.append(data);n-=len(data)
        return b''.join(chunks)


def extract(source,out,spec,guard):
    files=out/'files';files.mkdir()
    partials=out/'partial';partials.mkdir()
    inventory={m['name']:m for m in spec['members']}
    allowed_dirs={str(p) for name in inventory for p in PurePosixPath(name).parents if str(p)!='.'}
    seen=set();seen_files=set();observed=[];total=0;headers=0
    with gzip.open(source,'rb') as gz:
        reader=TarReader(gz,spec['max_tar_bytes'],guard)
        while True:
            block=reader.exact(512)
            if block==b'\0'*512:
                if reader.exact(512)!=b'\0'*512:raise ValueError('Tar requires two zero end records')
                break
            member=tarfile.TarInfo.frombuf(block,'utf-8','strict')
            headers+=1
            if headers>spec['max_members']:raise ValueError('Tar member cap')
            name=safe_name(member.name.rstrip('/') if member.isdir() else member.name)
            if name in seen:raise ValueError('Duplicate tar member')
            seen.add(name)
            if member.isdir():
                if name not in allowed_dirs or member.size!=0:raise ValueError('Unexpected tar directory')
                (files/name).mkdir(parents=True,exist_ok=True);continue
            if member.type not in (tarfile.REGTYPE,tarfile.AREGTYPE):raise ValueError('Tar links/special/extension headers forbidden')
            if name not in inventory:raise ValueError('Unexpected archive member')
            expected=inventory[name]
            if member.size!=expected['bytes'] or member.size<0 or total+member.size>spec['max_expanded_bytes']:raise ValueError('Member size/cap mismatch')
            target=files/name;target.parent.mkdir(parents=True,exist_ok=True);partial=partials/name;partial.parent.mkdir(parents=True,exist_ok=True)
            h=hashlib.sha256();remaining=member.size
            with partial.open('xb') as handle:
                while remaining:
                    data=reader.read(min(CHUNK,remaining))
                    if not data:raise ValueError('Truncated member')
                    handle.write(data);handle.flush();h.update(data);remaining-=len(data);guard()
                os.fsync(handle.fileno())
            if h.hexdigest()!=expected['sha256']:raise ValueError('Member SHA256 mismatch')
            padding=(-member.size)%512
            if padding and reader.exact(padding)!=b'\0'*padding:raise ValueError('Nonzero tar padding')
            seen_files.add(name);total+=member.size;observed.append(dict(expected))
        if seen_files!=set(inventory):raise ValueError('Missing expected member')
        # Drain all remaining gzip members/tail to check CRC; only zero tar padding
        # is accepted. read() permits one sentinel byte to detect cap overflow.
        while True:
            data=reader.read(CHUNK)
            if not data:break
            if data.strip(b'\0'):raise ValueError('Nonzero data after tar end')
    guard()
    return {'files':observed,'file_bytes':total,'tar_headers':headers,'tar_stream_bytes':reader.bytes,'gzip_eof_crc_validated':True}


def verify_archive(runner,name,phase):
    binding,signature=contract(runner,name)
    if signature!=phase['signature'] or binding!=phase['binding']:raise ValueError('Archive binding changed')
    out=runner.root/'archives'/name;path=out/'result.json'
    if sha(path)!=phase['receipt_sha256']:raise ValueError('Archive receipt changed')
    result=json.loads(path.read_text())
    if result.get('status')!='verified' or result.get('binding')!=binding or not result.get('gzip_eof_crc_validated'):raise ValueError('Incomplete archive receipt')
    inventory=binding['spec']['members']
    if sorted(result['files'],key=lambda v:v['name'])!=sorted(inventory,key=lambda v:v['name']):raise ValueError('Archive inventory changed')
    expected_names={m['name'] for m in inventory}
    actual_names={str(p.relative_to(out/'files')) for p in (out/'files').rglob('*') if p.is_file() or p.is_symlink()}
    if actual_names!=expected_names:raise ValueError('Archive outputs changed')
    if any(p.is_file() or p.is_symlink() for p in (out/'partial').rglob('*')):raise ValueError('Unpromoted archive partial')
    for item in inventory:
        target=out/'files'/item['name']
        if target.is_symlink() or file_digest(target,runner.guard)!={'bytes':item['bytes'],'sha256':item['sha256']}:raise ValueError('Extracted file changed')
    runner.guard()


def run_archive(runner,name):
    binding,signature=contract(runner,name)
    if not runner.begin(name,'archive',signature):
        phase=runner.state['phases'][name];verify_archive(runner,name,phase);return phase
    phase=runner.state['phases'][name];phase['binding']=binding;runner.save()
    out=runner.root/'archives'/name
    result={'status':'started','binding':binding,'raw_execution_ready':False}
    created=False
    try:
        out.mkdir(parents=True,exist_ok=False);created=True;atomic_json(out/'result.json',result)
        details=extract(runner.root/binding['spec']['transfer'],out,binding['spec'],runner.guard)
        if contract(runner,name)!=(binding,signature):raise ValueError('Archive source/binding changed during extraction')
        for item in details['files']:
            target=out/'files'/item['name'];os.replace(out/'partial'/item['name'],target)
        for directory in sorted({out/'files'/str(p) for n in [m['name'] for m in details['files']] for p in PurePosixPath(n).parents},key=lambda p:len(p.parts),reverse=True):fsync_directory(directory)
        for directory in sorted([p for p in (out/'partial').rglob('*') if p.is_dir()],key=lambda p:len(p.parts),reverse=True):directory.rmdir()
        (out/'partial').rmdir()
        runner.guard();result.update(details,status='verified');atomic_json(out/'result.json',result)
        fsync_directory(out.parent)
        phase.update(status='verified',receipt_sha256=sha(out/'result.json'));runner.guard();runner.save();return phase
    except BaseException as exc:
        result.update(status='failed',error_type=type(exc).__name__)
        if created:atomic_json(out/'result.json',result)
        phase.update(status='failed',error_type=type(exc).__name__);runner.save();raise
