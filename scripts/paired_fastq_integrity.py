"""Four-line DNA FASTQ paired integrity; full EOF/CRC scan, deterministic gzip prefix.

No Phred encoding inference, global name uniqueness certificate, or biological data
CLI. Output directory is exclusive. Only result.json status=verified certifies both
prefixes; failed attempts retain partials and must never be reused automatically.
"""
import gzip
import hashlib
import os
from pathlib import Path
from process_supervisor_v2 import atomic_json

MAX_LINE=20000

def record(stream,mate):
    head=stream.readline(MAX_LINE+1)
    if not head:return None
    lines=[head]+[stream.readline(MAX_LINE+1) for _ in range(3)]
    if any(not line.endswith(b'\n') or len(line)>MAX_LINE for line in lines):raise ValueError('Truncated or overlong four-line FASTQ')
    header,seq,plus,qual=[line.rstrip(b'\r\n') for line in lines]
    if not header.startswith(b'@') or not plus.startswith(b'+'):raise ValueError('FASTQ framing')
    tokens=header[1:].split()
    if not tokens:raise ValueError('Missing FASTQ identity')
    name=tokens[0];role=None
    if name.endswith((b'/1',b'/2')):role=int(name[-1:]);name=name[:-2]
    elif len(name)>2 and name[-2:-1]==b'/' and name[-1:].isdigit():raise ValueError('Unsupported mate suffix')
    if not name:raise ValueError('Missing normalized identity')
    if len(tokens)>1 and tokens[1][:2] in (b'1:',b'2:'):
        casava=int(tokens[1][:1])
        if role is not None and role!=casava:raise ValueError('Conflicting mate labels')
        role=casava
    if role is not None and role!=mate:raise ValueError('Incorrect mate label')
    if plus[1:]:
        repeated=plus[1:].split()
        if not repeated or repeated[0]!=tokens[0] or (len(repeated)>1 and plus[1:]!=header[1:]):raise ValueError('Repeated plus identity mismatch')
    if not seq or set(seq.upper())-set(b'ACGTN') or len(seq)!=len(qual):raise ValueError('Sequence/quality schema')
    if min(qual)<33 or max(qual)>126:raise ValueError('Quality ASCII outside declared syntax')
    if any(byte<33 or byte>126 for byte in tokens[0]):raise ValueError('Identity ASCII schema')
    return name,b''.join(lines),len(seq)

def file_digest(path,checkpoint=None):
    sha=hashlib.sha256();size=0
    with Path(path).open('rb') as inp:
        for block in iter(lambda:inp.read(65536),b''):
            if checkpoint:checkpoint()
            sha.update(block);size+=len(block)
    return {'bytes':size,'sha256':sha.hexdigest()}

def validate_pair(r1,r2,out,prefix_pairs,checkpoint=None):
    if type(prefix_pairs) is not int or prefix_pairs<=0:raise ValueError('Positive integer prefix required')
    r1,r2=Path(r1),Path(r2)
    if r1.resolve()==r2.resolve():raise ValueError('Mates must be distinct files')
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    result={'status':'started','prefix_pairs_requested':prefix_pairs,'pairs_scanned':0,'prefix_pairs_written':0,
            'source_gzip_eof_crc_validated':False,'global_identity_uniqueness_certified':False,
            'format_policy':'four-line ACGTN DNA; ASCII33-126 syntax only; Phred encoding not inferred',
            'raw_execution_ready':False}
    atomic_json(out/'result.json',result)
    try:
        if checkpoint:checkpoint()
        source_hashes=[file_digest(p,checkpoint) for p in (r1,r2)]
        partials=[out/f'prefix-R{i}.fastq.gz.partial' for i in (1,2)]
        with gzip.open(r1,'rb') as first,gzip.open(r2,'rb') as second,partials[0].open('xb') as one,partials[1].open('xb') as two:
            with gzip.GzipFile(fileobj=one,mode='wb',filename='',mtime=0) as target1,gzip.GzipFile(fileobj=two,mode='wb',filename='',mtime=0) as target2:
                while True:
                    if checkpoint:checkpoint()
                    a,b=record(first,1),record(second,2)
                    if a is None and b is None:break
                    if a is None or b is None:raise ValueError('Different mate record counts')
                    if a[0]!=b[0]:raise ValueError('Mate identity/order mismatch')
                    result['pairs_scanned']+=1
                    if result['pairs_scanned']<=prefix_pairs:
                        target1.write(a[1]);target2.write(b[1]);result['prefix_pairs_written']+=1
            one.flush();two.flush();os.fsync(one.fileno());os.fsync(two.fileno())
        if result['prefix_pairs_written']!=prefix_pairs:raise ValueError('Source shorter than fixed prefix')
        # gzip EOF includes all concatenated members and CRC; no early prefix exit.
        if checkpoint:checkpoint()
        for i,path in enumerate(partials,1):path.rename(out/f'prefix-R{i}.fastq.gz')
        result.update(status='verified',source_gzip_eof_crc_validated=True,source_compressed=source_hashes,
                      prefixes=[file_digest(out/f'prefix-R{i}.fastq.gz',checkpoint) for i in (1,2)],
                      prefix_ordinal_range_1based=[1,prefix_pairs])
    except BaseException as exc:
        result.update(status='failed',error_type=type(exc).__name__,error='FASTQ integrity or execution guard rejected input; no prefix certified')
        raise
    finally:atomic_json(out/'result.json',result)
    return result
