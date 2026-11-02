"""Offline extraction/inspection of a sealed recovered index; never downloads.

One exclusive derived output root. No adoption of failed jobs or original clock
renewal. New local step <=900s; original body accounting remains unchanged.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import resource
import shutil
import subprocess
import sys
import time
import re

import archive_ledger_phase as archive
import real_pilot_workflow as real
import recover_index_range as recovery
from process_supervisor_v2 import atomic_json,supervise,proc_info
from workflow_seal import read,sha as meta_sha,check_outer
from paired_fastq_integrity import file_digest
from pilot_execution_policy import iter_files

GiB=1024**3
PHASES={'preflight':{'seconds':120,'rss':512*1024**2,'space':GiB},
        'extract':{'seconds':600,'rss':GiB,'space':2*GiB},
        'inspect':{'seconds':120,'rss':6*GiB,'space':8*GiB}}
LIMITS={'wall_seconds':900,'rss_bytes':6*GiB,'address_space_bytes':8*GiB,
        'disk_bytes':25*GiB,'reserve_bytes':8*GiB,'threads':2}
CODE=tuple(sorted(set(real.CODE+recovery.CODE+('prepare_verified_index.py',))))


def identity():return {'python_sha256':file_digest(sys.executable)['sha256'],
    'code_sha256':{n:file_digest(Path(__file__).with_name(n))['sha256'] for n in CODE}}


def recovery_binding(root):
    root=Path(root).resolve();seal=read(root/'recovery-seal.json')
    if seal.get('status')!='sealed_verified_index_archive' or set(seal.get('sha256',{}))!=set(recovery.SEALED):raise ValueError('Complete recovered archive seal required')
    for name in recovery.SEALED:
        path=root/name
        if path.is_symlink() or meta_sha(path)!=seal['sha256'][name]:raise ValueError('Recovered sealed metadata changed')
    plan=read(root/'recovery-plan.json');result=read(root/'recovery-result.json');state=read(root/'recovery-state.json');accept=read(root/'operator-acceptance.json')
    check_outer(read(root/'supervision/run.json'))
    expected=plan['original_audit']['charged_body_bytes']+recovery.SOURCE['bytes']-plan['range_start']
    if plan.get('root')!=str(root) or plan.get('source')!=recovery.SOURCE or accept.get('prepared_sha256')!=meta_sha(root/'recovery-plan.json') or accept.get('accepted_additional_time_window') is not True:raise ValueError('Recovery source/acceptance mismatch')
    if state.get('status')!='verified' or result.get('status')!='verified_archive_pending_outer_seal' or result.get('state_sha256')!=meta_sha(root/'recovery-state.json'):raise ValueError('Recovery inner state incomplete')
    if seal.get('archive_sha256')!=recovery.SOURCE['sha256'] or result.get('sha256')!=recovery.SOURCE['sha256'] or seal.get('archive_bytes')!=recovery.SOURCE['bytes'] or result.get('bytes')!=recovery.SOURCE['bytes']:raise ValueError('Wrong recovered archive')
    if not expected<=12_000_000_000 or any(v!=expected for v in (seal.get('cumulative_body_bytes'),result.get('cumulative_body_bytes'),state.get('transfer_bytes_consumed'))):raise ValueError('Recovery cumulative accounting mismatch')
    path=root/'hg38_genome.tar.gz'
    if path.is_symlink() or not path.is_file() or path.stat().st_size!=recovery.SOURCE['bytes']:raise ValueError('Recovered regular archive missing/size changed')
    return {'root':str(root),'original_root':plan['original_root'],'seal_sha256':meta_sha(root/'recovery-seal.json'),
            'archive':str(path),'expected':{'bytes':recovery.SOURCE['bytes'],'sha256':recovery.SOURCE['sha256']},
            'cumulative_body_bytes':expected,'remaining_body_budget_bytes':12_000_000_000-expected}


def make_job(root,aligner_path):
    binding=recovery_binding(root);binary=Path(aligner_path).expanduser().resolve()
    aligner={'path':str(binary),'sha256':file_digest(binary)['sha256'],'version':'2.2.3',
        'source_commit':real.source_commit_at(binary.parent),'inspect_path':str(binary.with_name('hisat2-inspect-s')),
        'inspect_sha256':file_digest(binary.with_name('hisat2-inspect-s'))['sha256']}
    real.validate_aligner(aligner)
    original,_=real.sources();ref=original['reference'];members=ref['members']
    spec={'members':members,'max_members':16,'max_expanded_bytes':sum(m['bytes'] for m in members),
        'max_tar_bytes':sum(m['bytes']+((-m['bytes'])%512)+512 for m in members)+1024**2}
    output=Path(binding['root']).with_name(Path(binding['root']).name+'-extracted-01')
    return {'schema':'offline-verified-index-v1','root':str(output),'recovery':binding,'aligner':aligner,
            'archive_spec':spec,'limits':dict(LIMITS),'phases':PHASES,'identity':identity(),'new_transfer_bytes':0}


def validate_job(job):
    if not isinstance(job,dict) or set(job)!={'schema','root','recovery','aligner','archive_spec','limits','phases','identity','new_transfer_bytes'} or job['schema']!='offline-verified-index-v1' or job['new_transfer_bytes']!=0:raise ValueError('Fixed offline index descriptor required')
    if job['limits']!=LIMITS or job['phases']!=PHASES or job['identity']!=identity():raise ValueError('Offline resources/code changed')
    binding=recovery_binding(job['recovery']['root'])
    expected=make_spec()
    root=Path(binding['root']).with_name(Path(binding['root']).name+'-extracted-01')
    if job['recovery']!=binding or job['archive_spec']!=expected or job['root']!=str(root):raise ValueError('Offline source/inventory/output changed')
    real.validate_aligner(job['aligner']);return root


def make_spec():
    old,_=real.sources();members=old['reference']['members']
    return {'members':members,'max_members':16,'max_expanded_bytes':sum(m['bytes'] for m in members),
        'max_tar_bytes':sum(m['bytes']+((-m['bytes'])%512)+512 for m in members)+1024**2}


def disk_guard(job):
    size=0
    for root in (job['root'],job['recovery']['root'],job['recovery']['original_root']):
        for p in iter_files(root):
            try:
                if p.is_symlink():raise ValueError('Symlink in offline index lineage')
                if p.is_file():size+=p.stat().st_size
            except FileNotFoundError:pass
    if size>job['limits']['disk_bytes']:raise RuntimeError('Offline lineage disk cap')
    if shutil.disk_usage(Path(job['root']).parent).free<job['limits']['reserve_bytes']:raise RuntimeError('Offline disk reserve')


class Budget:
    def __init__(self,job):
        self.job=job;self.root=Path(job['root']);self.last_disk_check=float('-inf')
        if (self.root/'index-state.json').exists():raise ValueError('Never reopen attempted offline index step')
        self.state={'status':'started','deadline_epoch':time.time()+job['limits']['wall_seconds'],
            'last_epoch':time.time(),'phases':{},'new_transfer_bytes':0,'cumulative_body_bytes':job['recovery']['cumulative_body_bytes']};self.save()
    def save(self):atomic_json(self.root/'index-state.json',self.state)
    def guard(self):
        now=time.time()
        if now<self.state['last_epoch'] or now>=self.state['deadline_epoch']:raise RuntimeError('Offline global clock')
        self.state['last_epoch']=now
        for p in self.state['phases'].values():
            if p['status']=='started' and now>=p['deadline_epoch']:raise RuntimeError('Offline phase time cap')
        # The independent parent samples disk as well. Avoid a complete tree
        # walk for every64KiB hash/decompression read in this child.
        tick=time.monotonic()
        if tick-self.last_disk_check>=.1:
            disk_guard(self.job);self.last_disk_check=tick
    def begin(self,name):
        self.guard()
        if name in self.state['phases'] or any(p['status']=='started' for p in self.state['phases'].values()):raise ValueError('No offline phase reuse')
        caps=self.job['phases'][name];_,hard=resource.getrlimit(resource.RLIMIT_AS);resource.setrlimit(resource.RLIMIT_AS,(caps['space'],hard))
        now=time.time();self.state['phases'][name]={'status':'started','started_epoch':now,'deadline_epoch':min(self.state['deadline_epoch'],now+caps['seconds'])};self.save()
    def finish(self,name):self.guard();self.state['phases'][name].update(status='verified',finished_epoch=time.time());self.save()


def extract_checked(source,out,spec,expected,guard):
    out=Path(out);out.mkdir(exist_ok=False)
    details=archive.extract(source,out,spec,guard)
    if file_digest(source,guard)!=expected:raise ValueError('Archive changed during extraction')
    for item in details['files']:os.replace(out/'partial'/item['name'],out/'files'/item['name'])
    for directory in sorted([p for p in (out/'partial').rglob('*') if p.is_dir()],key=lambda p:len(p.parts),reverse=True):directory.rmdir()
    (out/'partial').rmdir()
    for directory in sorted([p for p in (out/'files').rglob('*') if p.is_dir()],key=lambda p:len(p.parts),reverse=True)+[out/'files',out]:archive.fsync_directory(directory)
    atomic_json(out/'extraction.json',details);return details


def verify_members(out,spec,guard):
    out=Path(out);expected={m['name'] for m in spec['members']}
    actual={str(p.relative_to(out/'files')) for p in (out/'files').rglob('*') if p.is_file() or p.is_symlink()}
    if actual!=expected or (out/'partial').exists():raise ValueError('Extracted inventory changed or incomplete')
    for m in spec['members']:
        p=out/'files'/m['name']
        if p.is_symlink() or file_digest(p,guard)!={'bytes':m['bytes'],'sha256':m['sha256']}:raise ValueError('Extracted member changed')


def inspect_summary(aligner,prefix,guard):
    real.validate_aligner(aligner);argv=[aligner['inspect_path'],'-s',str(prefix)]
    proc=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    try:
        data=proc.stdout.read(65537)
        if len(data)>65536:raise ValueError('Index summary cap')
        if proc.wait(timeout=30)!=0:raise ValueError('Index summary command failed')
        text=data.decode('utf-8','strict');guard()
        if len(re.findall(r'^Sequence-\d+\tchr19\t58617616$',text,re.M))!=1:raise ValueError('Expected hg38 chr19 missing/wrong length')
        real.validate_aligner(aligner);return {'argv':argv,'output':text,'scope':'summary/reference name and length, not full sequence equality or alignment benchmark'}
    finally:
        proc.stdout.close()
        if proc.poll() is None:proc.kill()
        proc.wait()


def worker(job):
    validate_job(job);budget=Budget(job);source=job['recovery']['archive'];root=budget.root
    try:
        budget.begin('preflight');probe=real.version_probe(job['aligner'])
        if file_digest(source,budget.guard)!=job['recovery']['expected']:raise ValueError('Recovered archive content changed')
        atomic_json(root/'preflight.json',probe);budget.finish('preflight');budget.begin('extract')
        extract_checked(source,root/'index',job['archive_spec'],job['recovery']['expected'],budget.guard)
        budget.finish('extract');budget.begin('inspect')
        summary=inspect_summary(job['aligner'],root/'index/files/hg38/genome',budget.guard)
        verify_members(root/'index',job['archive_spec'],budget.guard)
        if recovery_binding(job['recovery']['root'])!=job['recovery']:raise ValueError('Recovery provenance changed during offline step')
        atomic_json(root/'index-summary.json',summary);budget.finish('inspect');budget.state['status']='verified';budget.save()
        atomic_json(root/'index-result.json',{'status':'verified_index_pending_outer_seal','index_prefix':str(root/'index/files/hg38/genome'),
            'members':job['archive_spec']['members'],'source_archive_sha256':job['recovery']['expected']['sha256'],
            'state_sha256':meta_sha(root/'index-state.json'),'new_transfer_bytes':0,
            'cumulative_body_bytes':job['recovery']['cumulative_body_bytes'],'remaining_body_budget_bytes':job['recovery']['remaining_body_budget_bytes'],
            'raw_execution_ready':False,'scope':'extracted and summary-inspected index only; no reads/alignment'} )
    except BaseException as exc:
        for p in budget.state['phases'].values():
            if p['status']=='started':p.update(status='failed',error_type=type(exc).__name__)
        budget.state.update(status='failed',error_type=type(exc).__name__);budget.save();raise


def monitor(job,start):
    root=Path(job['root'])
    def clocks():
        if time.monotonic()-start>=job['limits']['wall_seconds']:raise RuntimeError('External offline time cap')
        if (root/'index-state.json').exists():
            state=read(root/'index-state.json');now=time.time()
            if now<state['last_epoch'] or now>=state['deadline_epoch']:raise RuntimeError('External offline clock')
            for name,p in state['phases'].items():
                if p['status']=='started' and now>=min(p['deadline_epoch'],p['started_epoch']+job['phases'][name]['seconds']):raise RuntimeError('External offline phase cap')
        disk_guard(job)
    def memory(rss,members,identity):
        if (root/'index-state.json').exists():
            state=read(root/'index-state.json')
            for name,p in state['phases'].items():
                if p['status']=='started' and rss>job['phases'][name]['rss']:raise RuntimeError('External offline phase RSS cap')
    return clocks,memory


def accept_outer(job,record):
    check_outer(record);root=Path(job['root']);result=read(root/'index-result.json');state=read(root/'index-state.json')
    if read(root/'supervision/run.json')!=record or read(root/'index-job.json')!=job:raise ValueError('Offline external metadata changed')
    if state.get('status')!='verified' or set(state['phases'])!=set(job['phases']) or any(p['status']!='verified' for p in state['phases'].values()):raise ValueError('Offline phases incomplete')
    if result.get('status')!='verified_index_pending_outer_seal' or result.get('state_sha256')!=meta_sha(root/'index-state.json') or result.get('members')!=job['archive_spec']['members'] or result.get('source_archive_sha256')!=job['recovery']['expected']['sha256']:raise ValueError('Offline index result incomplete')
    if result.get('new_transfer_bytes')!=0 or result.get('cumulative_body_bytes')!=job['recovery']['cumulative_body_bytes']:raise ValueError('Offline accounting changed')
    expected_prefix=str(root/'index/files/hg38/genome')
    if result.get('index_prefix')!=expected_prefix or result.get('remaining_body_budget_bytes')!=job['recovery']['remaining_body_budget_bytes'] or state.get('new_transfer_bytes')!=0 or state.get('cumulative_body_bytes')!=job['recovery']['cumulative_body_bytes']:raise ValueError('Offline prefix/accounting mismatch')
    if recovery_binding(job['recovery']['root'])!=job['recovery']:raise ValueError('Offline recovery binding changed')
    for item in job['archive_spec']['members']:
        path=root/'index/files'/item['name']
        if path.is_symlink() or not path.is_file() or path.stat().st_size!=item['bytes']:raise ValueError('Offline output missing or changed')
    if (root/'index-seal.json').exists():raise FileExistsError('Offline result already sealed')
    files=('index-job.json','index-state.json','preflight.json','index/extraction.json','index-summary.json','index-result.json','supervision/run.json')
    seal={'status':'sealed_verified_extracted_index','sha256':{n:meta_sha(root/n) for n in files},
        'index_prefix':result['index_prefix'],'member_count':len(result['members']),'new_transfer_bytes':0,
        'cumulative_body_bytes':result['cumulative_body_bytes'],'remaining_body_budget_bytes':result['remaining_body_budget_bytes'],'raw_execution_ready':False}
    atomic_json(root/'index-seal.json',seal);return seal


def execute(root,aligner):
    job=make_job(root,aligner);out=validate_job(job)
    if shutil.disk_usage(out.parent).free<LIMITS['reserve_bytes']+job['archive_spec']['max_expanded_bytes']:raise ValueError('Insufficient offline free disk plus reserve')
    out.mkdir(exist_ok=False);atomic_json(out/'index-job.json',job);start=time.monotonic();clocks,memory=monitor(job,start)
    rec=supervise('run',[sys.executable,str(Path(__file__).resolve()),'--worker',str(out/'index-job.json')],out/'supervision',timeout=LIMITS['wall_seconds'],rss_limit=LIMITS['rss_bytes'],address_space=LIMITS['address_space_bytes'],checkpoint=clocks,group_checkpoint=memory)
    return accept_outer(job,rec)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--recovery',type=Path);p.add_argument('--aligner',type=Path);p.add_argument('--worker',type=Path,help=argparse.SUPPRESS);a=p.parse_args()
    if a.worker:
        job=read(a.worker);root=validate_job(job)
        if a.worker.resolve()!=root/'index-job.json':raise ValueError('Fixed offline worker descriptor required')
        outer=read(root/'supervision/run.json');until=time.monotonic()+2
        while outer.get('status')=='started' and 'procfs_group' not in outer and time.monotonic()<until:
            time.sleep(.01);outer=read(root/'supervision/run.json')
        if outer.get('status')!='started' or outer.get('procfs_group')!=proc_info(int(os.readlink('/proc/self')))['group']:raise ValueError('Offline worker requires active supervisor')
        worker(job)
    else:
        if not a.recovery or not a.aligner:p.error('--recovery and --aligner required')
        print(json.dumps(execute(a.recovery,a.aligner),indent=2))
