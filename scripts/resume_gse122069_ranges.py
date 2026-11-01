#!/usr/bin/env python3
"""Resume only verified ranges of the same fixed control within original 30min download budget."""
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import urllib.request
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.fetch_gse122069_ranges import validate_range
from scripts.fetch_gse122069_pilot import disk_guard
from scripts.gse122069_full_control import save


def validate_saved(path, entries, total, chunk=16*1024**2):
    expected={(n,min(n+chunk,total)-1) for n in range(0,total,chunk)}
    seen=set()
    with path.open('rb') as f:
        for e in entries:
            key=(e['start'],e['end'])
            if key not in expected or key in seen:
                raise ValueError('Invalid/duplicate saved range')
            seen.add(key);f.seek(e['start']);b=f.read(e['end']-e['start']+1)
            if hashlib.sha256(b).hexdigest()!=e['sha256']:
                raise ValueError('Saved range bytes changed')
    return sorted(expected-seen)


def resume(root=ROOT):
    os.chdir(root)
    out=Path('reports/gse122069-full-control-20261031')
    report=out/'fastq-download.json';old=json.loads(report.read_text())
    prior=out/'fastq-download-attempt1.json'
    if prior.exists():raise ValueError('One explicit resume only; do not overwrite history')
    save(prior,old)
    if old['verified'] or old['error']!='ValueError: Shared disk budget/reserve exceeded':
        raise ValueError('Resume applies only to recorded disk interruption')
    row=next(r for r in json.loads(Path('reports/gse122069-resource-plan/input_manifest.json').read_text())['rows'] if r['run']=='SRR8144907')
    destination=Path('data/cache/gse122069/SRR8144907.fastq.gz')
    part=destination.with_suffix('.gz.range.part')
    # Isolate the partial cache as well; do not copy data or change the bytes.
    cache=destination.parent;isolated=Path('/tmp/ela-full-control-fastq-a30d50c208ec-20261031')
    if not cache.is_symlink():
        if isolated.exists():raise ValueError('Isolation target already exists')
        os.rename(cache,isolated);cache.symlink_to(isolated,target_is_directory=True)
        for p in isolated.iterdir():
            if p.name!=part.name and p.is_file():p.unlink()
    entries=old['ranges'];missing=validate_saved(part,entries,row['fastq_bytes'])
    start=time.monotonic();budget=1800-old['elapsed_seconds'];errors=[]
    result=dict(old,verified=False,range_errors=list(old['range_errors']),resume_reason='disk duplicate caches retired; original input and budget unchanged',resumed_ranges=len(missing),reused_verified_ranges=len(entries))
    def get(pair):
        a,b=pair
        for attempt in range(2):
            try:
                if time.monotonic()-start>budget:raise TimeoutError('Original cumulative download30min budget exceeded')
                req=urllib.request.Request(row['url']+f'?pilot_range={a}',headers={'Range':f'bytes={a}-{b}','If-Range':'"52e97188-57e8ce9e25a00"'})
                with urllib.request.urlopen(req,timeout=min(60,max(1,budget-(time.monotonic()-start)))) as r:
                    validate_range(r.status,r.headers,a,b,row['fastq_bytes'],'"52e97188-57e8ce9e25a00"');data=r.read(b-a+2)
                if len(data)!=b-a+1:raise ValueError('Range payload length mismatch')
                return a,b,data
            except Exception as exc:
                errors.append({'start':a,'end':b,'resume_attempt':attempt+1,'error':type(exc).__name__+': '+str(exc)})
                if attempt:raise
    try:
        it=iter(missing)
        with part.open('r+b') as f,ThreadPoolExecutor(max_workers=2) as pool:
            active={pool.submit(get,pair) for pair in [next(it,None),next(it,None)] if pair is not None}
            while active:
                done,active=wait(active,return_when=FIRST_COMPLETED)
                for future in done:
                    a,b,data=future.result();disk_guard(cache,len(data));f.seek(a);f.write(data);f.flush()
                    entries.append({'start':a,'end':b,'sha256':hashlib.sha256(data).hexdigest()})
                    result.update(ranges=sorted(entries,key=lambda e:e['start']),range_errors=old['range_errors']+errors)
                    save(out/'fastq-resume-checkpoint.json',result)
                    print('verified saved ranges',len(entries),'of83',flush=True)
                    pair=next(it,None)
                    if pair is not None:active.add(pool.submit(get,pair))
        if validate_saved(part,entries,row['fastq_bytes']) or part.stat().st_size!=row['fastq_bytes']:
            raise ValueError('Incomplete assembled ranges')
        h,m=hashlib.sha256(),hashlib.md5()
        with part.open('rb') as f:
            for b in iter(lambda:f.read(8*1024**2),b''):h.update(b);m.update(b)
        if m.hexdigest()!=row['md5'] or h.hexdigest()!='d3f57e023735d35261f9b0c2acb4d8034a859295ab12178375be352c7b7d6593':
            raise ValueError('Complete fixed input hash mismatch')
        os.replace(part,destination)
        result.update(verified=True,bytes=destination.stat().st_size,md5=m.hexdigest(),sha256=h.hexdigest())
        result.pop('error',None)
    except Exception as exc:
        result['error']=type(exc).__name__+': '+str(exc);raise
    finally:
        result.update(ranges=sorted(entries,key=lambda e:e['start']),range_errors=old['range_errors']+errors,
                      first_attempt_seconds=old['elapsed_seconds'],resume_seconds=time.monotonic()-start,
                      elapsed_seconds=old['elapsed_seconds']+time.monotonic()-start)
        save(report,result)

if __name__=='__main__':resume()
