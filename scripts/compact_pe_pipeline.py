"""Bounded SAM stream -> derived JSON runs -> PE target counts, no retained SAM.

Only local computation. Metadata agreement and CIGAR agreement are checked on each
record; pair reduction remains shared. Temp space is charged before each write.
The caller must separately supervise producer and consumer in the same group.
"""
import argparse
from collections import Counter
import hashlib
import heapq
import itertools
import json
import os
from pathlib import Path

import pe_fragment_contract as pe
from process_supervisor_v2 import atomic_json

DEFAULT_LIMITS={'max_input_bytes':8*1024**2,'max_line_bytes':65536,'max_header_bytes':1024**2,'max_records':100000,
                'max_row_bytes':65536,'chunk_bytes':1024**2,'merge_fan_in':8,'max_runs':1024,
                'max_temp_bytes':32*1024**2,'max_result_bytes':1024**2,'max_targets':1000}
ROUTES=('text15','hts15','text8','hts8')


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()


class Disk:
    def __init__(self,limit,guard):self.limit=limit;self.used=0;self.peak=0;self.guard=guard
    def write(self,handle,data):
        self.guard()
        if self.used+len(data)>self.limit:raise ValueError('Temporary disk cap')
        self.used+=len(data);self.peak=max(self.peak,self.used);handle.write(data)
    def remove(self,path):self.used-=path.stat().st_size;path.unlink()


def key(row):
    parts=row.split(b'\t',2)
    if len(parts)!=3:raise ValueError('Corrupt compact row')
    return parts[0],parts[1]


def validate(library,targets,limits):
    if not isinstance(library,str) or not library or len(library)>128 or any(ord(c)<33 or ord(c)>126 for c in library):raise ValueError('Explicit bounded ASCII library required')
    if set(limits)!=set(DEFAULT_LIMITS) or any(type(v) is not int or v<=0 for v in limits.values()):raise ValueError('Explicit positive pipeline limits required')
    if limits['merge_fan_in']<2 or limits['max_row_bytes']>limits['chunk_bytes']:raise ValueError('Invalid merge/chunk policy')
    if limits['max_result_bytes']<4096:raise ValueError('Result cap must accommodate failure receipt')
    if not isinstance(targets,list) or not targets or len(targets)>limits['max_targets']:raise ValueError('Bounded target inventory required')
    out=[]
    for t in targets:
        if not isinstance(t,(tuple,list)) or len(t)!=4:raise ValueError('Target interval schema')
        chrom,start,end,strand=t
        if not isinstance(chrom,str) or not chrom or len(chrom)>255 or any(ord(c)<33 or ord(c)>126 for c in chrom) or type(start) is not int or type(end) is not int or start<0 or end<=start or strand not in ('+','-'):raise ValueError('Target coordinates')
        out.append(tuple(t))
    if len(set(out))!=len(out):raise ValueError('Duplicate targets')
    return out


def decode(line,header):
    import pysam
    text15=next(pe.text_records_from_lines([line],15));text8=next(pe.text_records_from_lines([line],8))
    segment=pysam.AlignedSegment.fromstring(line.rstrip('\n'),header)
    hts15=next(pe.hts_decoded([segment],15));hts8=next(pe.hts_decoded([segment],8))
    records=[text15,hts15,text8,hts8];meta={k:v for k,v in text15.items() if k!='events'}
    if any({k:v for k,v in r.items() if k!='events'}!=meta for r in records):raise ValueError('Decoder metadata disagreement')
    if text15['events']!=hts15['events'] or text8['events']!=hts8['events']:raise ValueError('Decoder CIGAR disagreement')
    if not isinstance(meta['qname'],str) or not meta['qname'] or any(ord(c)<33 or ord(c)>126 for c in meta['qname']):raise ValueError('QNAME key schema')
    if not isinstance(meta['rg'],str) or any(ord(c)<32 or ord(c)>126 for c in meta['rg']):raise ValueError('RG key schema')
    # No SEQ, QUAL, CIGAR, optional tag payloads or SAM headers are persisted.
    return meta['rg'].encode()+b'\t'+meta['qname'].encode()+b'\t'+encoded({'meta':meta,'events':[r['events'] for r in records]})+b'\n'


def bounded_rows(handle,cap,guard):
    while True:
        guard();row=handle.readline(cap+1)
        if not row:return
        if len(row)>cap or not row.endswith(b'\n'):raise ValueError('Compact row cap/framing')
        yield row


def run(stream,out,library,targets,limits,finish_source,checkpoint=None):
    import pysam
    targets=validate(library,targets,limits)
    if not callable(finish_source):raise ValueError('Producer completion callback required')
    guard=checkpoint or (lambda:None);out=Path(out)
    result={'status':'started','policy':'compact-pe-v1','library':library,'targets':[list(t) for t in targets],'limits':limits,
            'raw_execution_ready':False,'retained_sam':False,'independence':'CIGAR decoding; agreed metadata and shared pair reduction'}
    if len((json.dumps(result,indent=2)+'\n').encode())>limits['max_result_bytes']:raise ValueError('Initial receipt cap')
    out.mkdir(parents=True,exist_ok=False);atomic_json(out/'result.json',result)
    work=out/'work';work.mkdir();disk=Disk(limits['max_temp_bytes'],guard);digest=hashlib.sha256()
    stats={'input_bytes':0,'records':0,'header_bytes':0,'initial_runs':0,'merge_passes':0}
    paths=[];chunk=[];chunk_size=0;headers=[];header=None;serial=0
    def new_path():
        nonlocal serial
        serial+=1;return work/f'run-{serial}.jsonl'
    def flush():
        nonlocal chunk,chunk_size
        if not chunk:return
        if len(paths)>=limits['max_runs']:raise ValueError('Initial run cap')
        path=new_path()
        with path.open('xb') as h:
            for row in sorted(chunk,key=key):disk.write(h,row)
            h.flush();os.fsync(h.fileno())
        paths.append(path);stats['initial_runs']+=1;chunk=[];chunk_size=0
    try:
        while True:
            guard();line=stream.readline(min(limits['max_line_bytes']+1,limits['max_input_bytes']-stats['input_bytes']+1))
            if not line:break
            if not isinstance(line,bytes):raise ValueError('Binary SAM stream required')
            stats['input_bytes']+=len(line)
            if stats['input_bytes']>limits['max_input_bytes']:raise ValueError('Input byte cap')
            if len(line)>limits['max_line_bytes'] or not line.endswith(b'\n'):raise ValueError('SAM line cap/framing')
            digest.update(line);text=line.decode('ascii')
            if text.startswith('@'):
                if header is not None:raise ValueError('Header after SAM records')
                stats['header_bytes']+=len(line)
                if stats['header_bytes']>limits['max_header_bytes']:raise ValueError('Header cap')
                headers.append(text);continue
            if header is None:
                header=pysam.AlignmentHeader.from_text(''.join(headers))
                references=dict(zip(header.references,header.lengths))
                if any(t[0] not in references or t[2]>references[t[0]] for t in targets):raise ValueError('Target/header reference mismatch')
                headers=[]
            stats['records']+=1
            if stats['records']>limits['max_records']:raise ValueError('Record cap')
            row=decode(text,header)
            if len(row)>limits['max_row_bytes']:raise ValueError('Compact row cap')
            if chunk_size+len(row)>limits['chunk_bytes']:flush()
            chunk.append(row);chunk_size+=len(row)
        if header is None:raise ValueError('No SAM alignment records')
        code=finish_source();result['producer_exit_code']=code
        if type(code) is not int or code!=0:raise ValueError('Producer did not complete successfully')
        flush();result['source_sha256']=digest.hexdigest()
        # Multi-pass stable external merge, at most fan-in input files open.
        while len(paths)>1:
            merged=[];stats['merge_passes']+=1
            for offset in range(0,len(paths),limits['merge_fan_in']):
                group=paths[offset:offset+limits['merge_fan_in']]
                if len(group)==1:merged.extend(group);continue
                dest=new_path();handles=[]
                try:
                    handles=[p.open('rb') for p in group]
                    with dest.open('xb') as h:
                        for row in heapq.merge(*(bounded_rows(f,limits['max_row_bytes'],guard) for f in handles),key=key):disk.write(h,row)
                        h.flush();os.fsync(h.fileno())
                finally:
                    for f in handles:f.close()
                for p in group:disk.remove(p)
                merged.append(dest)
            paths=merged
        counters={route:Counter() for route in ROUTES};qcs={route:Counter() for route in ROUTES};last=None
        with paths[0].open('rb') as handle:
            for group_key,rows in itertools.groupby(bounded_rows(handle,limits['max_row_bytes'],guard),key=key):
                if last is not None and group_key<=last:raise ValueError('Compact merge order')
                last=group_key;batch=list(itertools.islice(rows,17))
                if len(batch)>16:raise ValueError('Fragment group exceeds 16 records')
                decoded=[json.loads(row.split(b'\t',2)[2]) for row in batch]
                for i,route in enumerate(ROUTES):
                    records=[{**r['meta'],'events':[tuple(e) for e in r['events'][i]]} for r in decoded]
                    counts,qc=pe.count_fragments(iter(records),library);qcs[route].update(qc)
                    for t in targets:counters[route][t]+=counts.get((library,)+t,0)
        if counters['text15']!=counters['hts15'] or qcs['text15']!=qcs['hts15'] or counters['text8']!=counters['hts8'] or qcs['text8']!=qcs['hts8']:raise ValueError('Reduced decoder disagreement')
        result.update(status='verified',input_eof=True,pysam_version=pysam.__version__,htslib_samtools_version=pysam.__samtools_version__,
                      routes={r:{'counts':[{'event':list(t),'fragments':counters[r][t]} for t in targets],'qc':dict(sorted(qcs[r].items()))} for r in ROUTES})
        # Prepare and validate bounded result before removing temporary evidence.
        result.update(stats,peak_temp_bytes=disk.peak)
        if len((json.dumps(result,indent=2)+'\n').encode())>limits['max_result_bytes']:raise ValueError('Result byte cap')
        guard()
        for path in paths:disk.remove(path)
        work.rmdir();atomic_json(out/'result.json',result)
        return result
    except BaseException as exc:
        result={'status':'failed','policy':'compact-pe-v1','raw_execution_ready':False,'error_type':type(exc).__name__,'error':str(exc)[:256],
                **stats,'peak_temp_bytes':disk.peak,'producer_exit_code':result.get('producer_exit_code')}
        # Failed/started receipts never certify run files left for reconciliation.
        atomic_json(out/'result.json',result);raise


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--sam-fixture',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--policy',type=Path,required=True);a=p.parse_args()
    policy=json.loads(a.policy.read_text())
    with a.sam_fixture.open('rb') as source:run(source,a.out,policy['library'],policy['targets'],policy['limits'],lambda:0)
