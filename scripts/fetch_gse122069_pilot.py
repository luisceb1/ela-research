#!/usr/bin/env python3
"""Fetch only the fixed public culture control; require ENA MD5 before use."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import time
import urllib.request

BASELINE_FREE = 63485673472
DISK_LIMIT = 15*1024**3
RESERVE = 8*1024**3


def disk_guard(path, additional=0):
    free = shutil.disk_usage(path).free-additional
    if free<RESERVE or BASELINE_FREE-free>DISK_LIMIT:
        raise ValueError('Shared disk budget/reserve exceeded')


def fetch(manifest, destination, report):
    row = next(r for r in manifest['rows'] if r['run']=='SRR8144907')
    destination.parent.mkdir(parents=True,exist_ok=True)
    report.parent.mkdir(parents=True,exist_ok=True)
    partial=destination.with_suffix(destination.suffix+'.part')
    if destination.exists() or partial.exists(): raise ValueError('Explicitly verify existing file before reuse; no overwrite')
    disk_guard(destination.parent,row['fastq_bytes'])
    md5,sha,n=hashlib.md5(),hashlib.sha256(),0
    start,last=time.monotonic(),time.monotonic()
    result={'run':row['run'],'gsm':row['gsm'],'url':row['url'],'expected_md5':row['md5'],
            'expected_bytes':row['fastq_bytes'],'verified':False}
    try:
        with urllib.request.urlopen(row['url'],timeout=30) as r,partial.open('xb') as target:
            if r.status!=200: raise ValueError('HTTP failure')
            result['headers']=dict(r.headers)
            length=r.headers.get('Content-Length')
            if length is not None and int(length)!=row['fastq_bytes']:raise ValueError('HTTP size mismatch')
            while True:
                if time.monotonic()-start>1800:raise TimeoutError('Download exceeds30min')
                chunk=r.read(8*1024**2)
                if not chunk:break
                n+=len(chunk)
                if n>row['fastq_bytes']:raise ValueError('Unexpected download size')
                disk_guard(destination.parent,len(chunk))
                target.write(chunk);md5.update(chunk);sha.update(chunk)
                if time.monotonic()-last>15:
                    print(f'control download {n}/{row["fastq_bytes"]} bytes',flush=True);last=time.monotonic()
        if n!=row['fastq_bytes'] or md5.hexdigest()!=row['md5']:raise ValueError('ENA size/MD5 mismatch')
        os.replace(partial,destination);result['verified']=True
    except Exception as e:
        result['error']=type(e).__name__+': '+str(e);raise
    finally:
        result.update(bytes=n,md5=md5.hexdigest(),sha256=sha.hexdigest(),elapsed_seconds=time.monotonic()-start)
        report.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__);p.add_argument('--manifest',required=True);p.add_argument('--destination',required=True);p.add_argument('--report',required=True);a=p.parse_args()
    fetch(json.loads(Path(a.manifest).read_text()),Path(a.destination),Path(a.report))
