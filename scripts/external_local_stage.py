"""Supervised fixed worker for synthetic local stages, never a production CLI.

Only literal loopback HTTP and manifest-bound paired validation are accepted.
The parent never owns the runner flock while the child runs. Failed or interrupted
work is retained, with no automatic reconciliation or overwrite of external jobs.
"""
import argparse
import hashlib
import ipaddress
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from urllib.parse import urlsplit

from pilot_dry_runner import DryRunner
from process_supervisor_v2 import atomic_json,supervise
from bounded_http_transport import transfer_http


def validate_stage(stage):
    if not isinstance(stage,dict) or not re.fullmatch('[A-Za-z0-9_-]+',stage.get('name','')):raise ValueError('Named local stage required')
    if stage.get('kind')=='http':
        if set(stage)!={'kind','name','url','expected','chunk_size'}:raise ValueError('Fixed HTTP stage schema')
        p=urlsplit(stage['url'])
        if p.scheme!='http' or p.username or p.password or p.fragment:raise ValueError('Literal loopback HTTP only')
        try:loopback=ipaddress.ip_address(p.hostname).is_loopback
        except ValueError:loopback=False
        if not loopback:raise ValueError('Non-loopback URL refused')
        if type(stage['chunk_size']) is not int or not 1<=stage['chunk_size']<=65536:raise ValueError('Invalid chunk size')
    elif stage.get('kind') in ('paired_fastq','archive'):
        if set(stage)!={'kind','name'}:raise ValueError('Fixed paired stage schema')
    else:raise ValueError('Unsupported local stage')


def worker(job):
    validate_stage(job['stage']);stage=job['stage']
    r=DryRunner(job['root'],job['manifest'],job['limits'])
    try:
        fault=job.get('synthetic_fault')
        if fault in ('stall_validator','stall_archive'):
            subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)'])
            guard=r.guard
            def blocked_guard():
                guard()
                paired=(r.root/'paired-fastq'/stage['name']/'prefix-R1.fastq.gz.partial').exists()
                archived=any(p.is_file() for p in (r.root/'archives'/stage['name']/'partial').rglob('*'))
                if (fault=='stall_validator' and paired) or (fault=='stall_archive' and archived):time.sleep(30)
            r.guard=blocked_guard
        elif fault=='crash_worker':os._exit(74)
        elif fault is not None:raise ValueError('Unknown synthetic fault')
        if stage['kind']=='http':
            p=urlsplit(stage['url']);origin=f'{p.scheme}://{p.netloc}'
            transfer_http(r,stage['name'],stage['url'],stage['expected'],[origin],chunk_size=stage['chunk_size'],reserve_reads=True)
        elif stage['kind']=='archive':r.archive(stage['name'])
        else:r.paired_fastq(stage['name'])
    finally:r.close()


def run_local_stage(root,manifest,limits,stage,*,timeout,rss_bytes=128*1024**2,address_space_bytes=128*1024**2,synthetic_fault=None):
    validate_stage(stage)
    if type(timeout) not in (int,float) or not math.isfinite(timeout) or timeout<=0:raise ValueError('Positive finite timeout required')
    if any(type(v) is not int or v<=0 for v in (rss_bytes,address_space_bytes)):raise ValueError('Explicit positive memory limits required')
    if synthetic_fault not in (None,'stall_validator','stall_archive','crash_worker'):raise ValueError('Unknown synthetic fault')
    if synthetic_fault=='stall_validator' and stage['kind']!='paired_fastq':raise ValueError('Validator fault requires paired stage')
    if synthetic_fault=='stall_archive' and stage['kind']!='archive':raise ValueError('Archive fault requires archive stage')
    root=Path(root).resolve()
    r=DryRunner(root,manifest,limits)
    try:deadline=r.state['deadline_epoch']
    finally:r.close()
    folder=root/'external-receipts';folder.mkdir(exist_ok=True)
    job_path=folder/(stage['name']+'.job.json')
    job={'root':str(root),'manifest':manifest,'limits':limits,'stage':stage,'synthetic_fault':synthetic_fault,'scope':'local-synthetic-only','raw_execution_ready':False,
         'supervision':{'requested_timeout_seconds':timeout,'rss_bytes':rss_bytes,'address_space_bytes':address_space_bytes,'deadline_epoch':deadline}}
    with job_path.open('x') as f:
        json.dump(job,f,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
    fd=os.open(folder,os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
    effective=min(timeout,deadline-time.time())
    if effective<=0:raise RuntimeError('Global deadline before spawn')
    def disk_guard():
        used=0
        for p in root.rglob('*'):
            try:
                if p.is_file():used+=p.stat().st_size
            except FileNotFoundError:pass  # Atomic child renames; next sample observes final path.
        if used>limits['disk_bytes']:raise RuntimeError('External disk cap')
        if shutil.disk_usage(root).free<limits['reserve_bytes']:raise RuntimeError('External disk reserve')
    rec=supervise(stage['name'],[sys.executable,str(Path(__file__).resolve()),'--local-job',str(job_path)],folder,timeout=effective,rss_limit=rss_bytes,address_space=address_space_bytes,checkpoint=disk_guard)
    outcome={'status':'verified' if rec['exit_code']==0 and not rec['violation'] and not rec['live_group_members_after_cleanup'] else 'failed',
             'job_sha256':hashlib.sha256(job_path.read_bytes()).hexdigest(),'external_receipt':stage['name']+'.json',
             'effective_timeout_seconds':effective,'raw_execution_ready':False}
    # Parent records evidence only; never turns a killed inner phase into verified.
    atomic_json(folder/(stage['name']+'.outcome.json'),outcome)
    return rec


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--local-job',type=Path,required=True);args=p.parse_args()
    worker(json.loads(args.local_job.read_text()))
