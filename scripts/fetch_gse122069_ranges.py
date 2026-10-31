#!/usr/bin/env python3
"""Bounded two-connection range fallback; accept only full ENA MD5 match."""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import urllib.request
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.fetch_gse122069_pilot import disk_guard


def validate_range(status,headers,start,end,total,etag):
    if status!=206 or headers.get('Content-Range')!=f'bytes {start}-{end}/{total}':
        raise ValueError('Incorrect range response')
    if headers.get('ETag')!=etag or int(headers.get('Content-Length','-1'))!=end-start+1:
        raise ValueError('Range object identity/size mismatch')


def fetch(manifest,destination,report,etag):
    row=next(r for r in manifest['rows'] if r['run']=='SRR8144907');total=row['fastq_bytes']
    destination.parent.mkdir(parents=True,exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
    part=destination.with_suffix(destination.suffix+'.range.part')
    if part.exists() or destination.exists():raise ValueError('Explicit verified reuse required; no overwrite')
    disk_guard(destination.parent,total)
    chunk=16*1024**2;start_time=time.monotonic();entries=[];errors=[]
    result={'run':row['run'],'gsm':row['gsm'],'url':row['url'],'expected_md5':row['md5'],
            'expected_bytes':total,'verified':False,'mode':'two connections; exact HTTP ranges; full final checksum required'}
    def get_range(start,end):
        url=row['url']+f'?pilot_range={start}'
        for attempt in range(2):
            try:
                if time.monotonic()-start_time>1800:raise TimeoutError('Range download exceeds30min')
                req=urllib.request.Request(url,headers={'Range':f'bytes={start}-{end}','If-Range':etag})
                with urllib.request.urlopen(req,timeout=60) as r:
                    validate_range(r.status,r.headers,start,end,total,etag)
                    b=r.read(end-start+2)
                if len(b)!=end-start+1:raise ValueError('Truncated/oversized range payload')
                return start,end,b
            except Exception as exc:
                errors.append({'start':start,'end':end,'attempt':attempt+1,'error':type(exc).__name__+': '+str(exc)})
                if attempt==1:raise
    try:
        ranges=[(n,min(n+chunk,total)-1) for n in range(0,total,chunk)]
        with part.open('xb') as f,ThreadPoolExecutor(max_workers=2) as pool:
            futures=[pool.submit(get_range,a,b) for a,b in ranges]
            for future in as_completed(futures):
                a,b,data=future.result();disk_guard(destination.parent,len(data));f.seek(a);f.write(data)
                entries.append({'start':a,'end':b,'sha256':hashlib.sha256(data).hexdigest()})
                if len(entries)%4==0:print(f'ranges complete {len(entries)}/{len(ranges)}',flush=True)
        if len(entries)!=len(ranges) or part.stat().st_size!=total:raise ValueError('Incomplete range set')
        h,m=hashlib.sha256(),hashlib.md5()
        with part.open('rb') as f:
            for b in iter(lambda:f.read(8*1024**2),b''):h.update(b);m.update(b)
        result.update(bytes=part.stat().st_size,md5=m.hexdigest(),sha256=h.hexdigest())
        if m.hexdigest()!=row['md5']:raise ValueError('Full ENA MD5 mismatch')
        os.replace(part,destination);result['verified']=True
    except Exception as exc:result['error']=type(exc).__name__+': '+str(exc);raise
    finally:
        result.update(ranges=sorted(entries,key=lambda e:e['start']),range_errors=errors,elapsed_seconds=time.monotonic()-start_time)
        report.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__);p.add_argument('--manifest',required=True);p.add_argument('--destination',required=True);p.add_argument('--report',required=True);p.add_argument('--etag',required=True);a=p.parse_args()
    fetch(json.loads(Path(a.manifest).read_text()),Path(a.destination),Path(a.report),a.etag)
