#!/usr/bin/env python3
"""Bounded two-connection range fallback; accept only full ENA MD5 match."""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib
import json
import os
import signal
import subprocess
from pathlib import Path
import sys
import time
import urllib.request
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.fetch_gse122069_pilot import disk_guard
from scripts.gse122069_run_config import DEFAULT_RUN, load_rows, configure, validate_receipt


def validate_range(status,headers,start,end,total,etag):
    if status!=206 or headers.get('Content-Range')!=f'bytes {start}-{end}/{total}':
        raise ValueError('Incorrect range response')
    if headers.get('ETag')!=etag or int(headers.get('Content-Length','-1'))!=end-start+1:
        raise ValueError('Range object identity/size mismatch')


def download_plan(manifest,run_accession=DEFAULT_RUN):
    config=configure(manifest['rows'],run_accession)
    row=next(r for r in manifest['rows'] if r['run']==config['run'])
    return {'run':row['run'],'gsm':row['gsm'],'url':row['url'],'expected_bytes':row['fastq_bytes'],
            'expected_md5':row['md5'],'expected_reads':row['reads'],'verified':False,
            'mode':'plan_only_no_network_or_fastq_opened','etag_verification_pending':True,
            'own_sha256_pending_download':True,'download_deadline_seconds':1800,'connections':2}


def bounded_download(command,report,plan,deadline=1800):
    """Bound the whole transport process, including worker threads/network IO.

    A timeout never yields a verified receipt. Unverified partial bytes remain
    for a separately reviewed recovery; no automatic restart or budget growth.
    """
    report=Path(report)
    if report.exists():raise ValueError('Refuse to overwrite an existing download receipt')
    report.parent.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();proc=subprocess.Popen(command,start_new_session=True)
    error=None
    try:
        try:
            code=proc.wait(timeout=max(0,deadline-(time.monotonic()-start)))
        except subprocess.TimeoutExpired:
            try:os.killpg(proc.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            proc.wait()
            error='TimeoutError: bounded download exceeded explicit deadline'
            code=proc.returncode
        result=dict(plan,verified=False,mode='bounded_download_failed')
        if report.exists():
            try:
                child=json.loads(report.read_text())
                if not isinstance(child,dict):raise ValueError('Child receipt is not an object')
                result=child
            except (ValueError,OSError) as exc:
                result['error']='ValueError: invalid child download receipt: '+str(exc)
                if report.exists():result['invalid_child_receipt_sha256']=hashlib.sha256(report.read_bytes()).hexdigest()
        if code or error or result.get('verified') is not True:
            result['verified']=False
            result['error']=error or result.get('error') or 'RuntimeError: download child did not produce a verified receipt'
        else:
            try:validate_receipt({'run':plan['run'],'gsm':plan['gsm'],'expected_fastq_bytes':plan['expected_bytes'],'expected_md5':plan['expected_md5']},result)
            except ValueError as exc:result.update(verified=False,error='ValueError: '+str(exc))
        result.update(transport_process_exit_code=code,transport_wall_deadline_seconds=deadline,
                      transport_parent_elapsed_seconds=time.monotonic()-start)
        tmp=report.with_suffix(report.suffix+'.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');os.replace(tmp,report)
        if not result['verified']:raise RuntimeError(result['error'])
        return result
    finally:
        if proc.poll() is None:
            try:os.killpg(proc.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            proc.wait()


def fetch(manifest,destination,report,etag,run_accession=DEFAULT_RUN):
    config=configure(manifest['rows'],run_accession)
    if not etag or etag.startswith('W/'):raise ValueError('Observed strong ETag required before download')
    row=next(r for r in manifest['rows'] if r['run']==config['run']);total=row['fastq_bytes']
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
    p=argparse.ArgumentParser(__doc__);p.add_argument('--manifest',required=True);p.add_argument('--destination',required=True);p.add_argument('--report',required=True);p.add_argument('--etag');p.add_argument('--run-accession',default=DEFAULT_RUN);p.add_argument('--plan-only',action='store_true');p.add_argument('--transport-child',action='store_true',help=argparse.SUPPRESS);a=p.parse_args()
    manifest={'rows':load_rows(a.manifest)}
    if a.plan_only:
        report=Path(a.report);report.parent.mkdir(parents=True,exist_ok=True)
        report.write_text(json.dumps(download_plan(manifest,a.run_accession),indent=2)+'\n')
    else:
        if not a.etag:p.error('download requires a newly verified object ETag')
        if a.transport_child:
            fetch(manifest,Path(a.destination),Path(a.report),a.etag,a.run_accession)
        else:
            command=[sys.executable,str(Path(__file__).resolve()),'--manifest',a.manifest,'--destination',a.destination,'--report',a.report,'--etag',a.etag,'--run-accession',a.run_accession,'--transport-child']
            bounded_download(command,Path(a.report),download_plan(manifest,a.run_accession))
