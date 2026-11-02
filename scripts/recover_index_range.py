"""Explicit index-only recovery proposal. --prepare never downloads.

The old run stays immutable. One new bounded S3 Range request is possible only
with exact-plan SHA acceptance AND acknowledgment of the additional time window.
No FASTQ, extraction, alignment, automatic retry, deadline reset or adoption.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import urllib.request

import inspect_interrupted_pilot as audit
from bounded_http_transport import NoRedirect, read_reserved_blocks
from pilot_execution_policy import iter_files
from process_supervisor_v2 import atomic_json, supervise, proc_info
from workflow_seal import read, sha as meta_sha, check_outer

GiB=1024**3
LIMITS={'wall_seconds':2400,'copy_seconds':300,'transfer_seconds':1800,'verify_seconds':300,
        'transfer_bytes':12_000_000_000,'disk_bytes':25*GiB,'reserve_bytes':8*GiB,
        'rss_bytes':512*1024**2,'address_space_bytes':GiB,'threads':2,
        'read_chunk_bytes':65536,'reservation_block_bytes':4*1024**2}
SOURCE={'url':audit.INDEX_URL,'bytes':audit.INDEX_BYTES,'sha256':audit.INDEX_SHA,
        'version_id':'8z.MUbL_W4wij.Nmcia5c4mT7tlz0cU.'}
CODE=('recover_index_range.py','inspect_interrupted_pilot.py','bounded_http_transport.py',
      'pilot_execution_policy.py','pilot_dry_runner.py','paired_fastq_integrity.py',
      'paired_fastq_phase.py','archive_ledger_phase.py','artifact_checksums.py',
      'process_supervisor_v2.py','workflow_seal.py')
SEALED=('recovery-plan.json','operator-acceptance.json','recovery-state.json',
        'range-attempt.json','recovery-result.json','supervision/run.json')


def file_hash(path,guard=lambda:None):
    h=hashlib.sha256();count=0
    with Path(path).open('rb') as f:
        while True:
            guard();data=f.read(1024**2)
            if not data:break
            count+=len(data);h.update(data)
    return {'bytes':count,'sha256':h.hexdigest()}


def identity():
    return {'python_sha256':file_hash(sys.executable)['sha256'],
            'code_sha256':{n:file_hash(Path(__file__).with_name(n))['sha256'] for n in CODE}}


def recovery_root(original):return Path(original).with_name(Path(original).name+'-index-recovery-01')


def prepare(original):
    original=Path(original).expanduser().resolve();observed=audit.inspect(original);root=recovery_root(original)
    if root.exists():raise ValueError('Recovery directory already exists; no automatic new attempt')
    if observed['prior_transfer_elapsed_seconds']<3600:raise ValueError('This proposal is for the exhausted first index transfer only')
    if observed['charged_body_bytes']+SOURCE['bytes']-observed['partial_bytes']>LIMITS['transfer_bytes']:raise ValueError('Remaining range cannot fit original body cap')
    if shutil.disk_usage(original).free<LIMITS['disk_bytes']+LIMITS['reserve_bytes']:raise ValueError('33 GiB free required before recovery')
    return {'schema':'index-only-range-recovery-v1','execution_enabled':False,'original_root':str(original),'root':str(root),
        'original_audit':observed,'source':dict(SOURCE),'limits':dict(LIMITS),'identity':identity(),
        'range_start':observed['partial_bytes'],'range_end':SOURCE['bytes']-1,
        'scope':'recover index archive only; no extraction, FASTQ, alignment or biological result',
        'time_review':'new explicit 2400s recovery window, including up to1800s additional transfer; original deadlines/spent time unchanged'}


def validate_plan(plan):
    keys={'schema','execution_enabled','original_root','root','original_audit','source','limits','identity','range_start','range_end','scope','time_review'}
    if not isinstance(plan,dict) or set(plan)!=keys or plan['schema']!='index-only-range-recovery-v1' or plan['execution_enabled'] is not False:raise ValueError('Disabled recovery proposal required')
    original=Path(plan['original_root']);root=Path(plan['root']);obs=plan['original_audit']
    if not original.is_absolute() or original!=original.resolve() or root!=recovery_root(original) or root!=root.resolve():raise ValueError('Canonical exclusive recovery lineage required')
    if plan['source']!=SOURCE or plan['limits']!=LIMITS or plan['identity']!=identity():raise ValueError('Pinned source/resources/code changed')
    if obs.get('status')!='AUDITED_INTERRUPTED_NOT_RESUMABLE' or obs.get('source_verified') is not False or obs.get('root')!=str(original) or obs.get('expected_index_bytes')!=SOURCE['bytes']:raise ValueError('Audited interrupted index required')
    if type(plan['range_start']) is not int or not 0<plan['range_start']<SOURCE['bytes'] or plan['range_start']!=obs.get('partial_bytes') or plan['range_end']!=SOURCE['bytes']-1:raise ValueError('Exact remaining range required')
    if not re.fullmatch('[0-9a-f]{64}',str(obs.get('partial_sha256',''))):raise ValueError('Partial SHA identity required')
    charged=obs.get('charged_body_bytes')
    if type(charged) is not int or charged<plan['range_start'] or charged+SOURCE['bytes']-plan['range_start']>LIMITS['transfer_bytes']:raise ValueError('Prior charges must fit original body budget')
    if obs.get('prior_transfer_elapsed_seconds',0)<3600:raise ValueError('Original transfer clock evidence required')
    return root


def disk_guard(plan):
    size=0
    for root in (Path(plan['original_root']),Path(plan['root'])):
        for path in iter_files(root):
            try:
                if path.is_symlink():raise ValueError('Symlink in recovery lineage')
                if path.is_file():size+=path.stat().st_size
            except FileNotFoundError:pass
    if size>plan['limits']['disk_bytes']:raise RuntimeError('Original plus recovery disk cap')
    if shutil.disk_usage(Path(plan['original_root'])).free<plan['limits']['reserve_bytes']:raise RuntimeError('Recovery free disk reserve')


class Budget:
    def __init__(self,plan,clock=time.time):
        self.plan=plan;self.root=Path(plan['root']);self.clock=clock;now=clock()
        self.state={'status':'started','limits':plan['limits'],'deadline_epoch':now+plan['limits']['wall_seconds'],
            'last_epoch':now,'transfer_bytes_consumed':plan['original_audit']['charged_body_bytes'],
            'prior_transfer_elapsed_seconds':plan['original_audit']['prior_transfer_elapsed_seconds'],
            'original_deadline_epoch':plan['original_audit']['prior_global_deadline_epoch'],'phases':{}}
        if (self.root/'recovery-state.json').exists():raise ValueError('Never reopen an attempted recovery')
        self.save()
    def save(self):
        self.state['last_epoch']=max(self.clock(),self.state['last_epoch'])
        atomic_json(self.root/'recovery-state.json',self.state)
    def guard(self):
        now=self.clock()
        if now<self.state['last_epoch']:raise RuntimeError('Recovery clock moved backwards')
        self.state['last_epoch']=now
        if now>=self.state['deadline_epoch']:raise RuntimeError('Recovery global time cap')
        for phase in self.state['phases'].values():
            if phase['status']=='started' and now>=phase['deadline_epoch']:raise RuntimeError('Recovery phase time cap')
        charged=self.state['transfer_bytes_consumed']
        if not self.plan['original_audit']['charged_body_bytes']<=charged<=self.plan['limits']['transfer_bytes']:raise RuntimeError('Recovery cumulative body budget')
        disk_guard(self.plan)
    def begin(self,name):
        self.guard()
        if name in self.state['phases'] or any(p['status']=='started' for p in self.state['phases'].values()):raise ValueError('Exclusive sequential recovery phase required')
        now=self.clock();seconds=self.plan['limits'][{'copy':'copy_seconds','range':'transfer_seconds','verify':'verify_seconds'}[name]]
        phase={'status':'started','started_epoch':now,'deadline_epoch':min(now+seconds,self.state['deadline_epoch'])}
        self.state['phases'][name]=phase;self.save();return phase
    def finish(self,name):
        self.guard();self.state['phases'][name].update(status='verified',finished_epoch=self.clock());self.save()
    def remaining(self):
        self.guard();now=self.clock()
        return min([self.state['deadline_epoch']]+[p['deadline_epoch'] for p in self.state['phases'].values() if p['status']=='started'])-now


def copy_prefix(source,target,expected,guard):
    if Path(source).is_symlink():raise ValueError('Partial symlink refused')
    h=hashlib.sha256();size=0
    with Path(source).open('rb') as inp,Path(target).open('xb') as out:
        while True:
            guard();data=inp.read(min(1024**2,expected['bytes']-size+1))
            if not data:break
            size+=len(data)
            if size>expected['bytes']:raise ValueError('Partial grew beyond audited size')
            out.write(data);h.update(data)
        out.flush();os.fsync(out.fileno())
    if {'bytes':size,'sha256':h.hexdigest()}!=expected:raise ValueError('Partial changed since audit')


def range_append(budget,target,source,start):
    """One pinned HTTP206 request. Tests use loopback fixtures only."""
    remaining=source['bytes']-start;phase=budget.state['phases']['range']
    if remaining<=0 or remaining>budget.state['limits']['transfer_bytes']-budget.state['transfer_bytes_consumed']:raise ValueError('Exact remaining body does not fit cumulative cap')
    if Path(target).is_symlink() or Path(target).stat().st_size!=start:raise ValueError('Exact copied prefix required')
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    request=urllib.request.Request(source['url'],headers={'Accept-Encoding':'identity','Range':f"bytes={start}-{source['bytes']-1}"})
    rec={'status':'started','body_bytes':0,'range_start':start,'range_end':source['bytes']-1,
         'prior_charged_bytes':budget.state['transfer_bytes_consumed'],'attempts':1,'scope':'HTTP entity-body read, excludes TLS/TCP/headers/buffering'}
    receipt=budget.root/'range-attempt.json';atomic_json(receipt,rec)
    try:
        with opener.open(request,timeout=min(5,budget.remaining())) as response:
            headers=response.headers
            def single(name,value):
                values=headers.get_all(name) if hasattr(headers,'get_all') else [headers.get(name)]
                if values!=[value]:raise ValueError('Recovery response '+name+' mismatch')
            if response.status!=206:raise ValueError('Recovery requires HTTP206; never append a full HTTP200')
            single('Content-Length',str(remaining));single('Content-Range',f"bytes {start}-{source['bytes']-1}/{source['bytes']}")
            if headers.get('Content-Encoding','identity')!='identity' or headers.get('Transfer-Encoding') or headers.get('Content-Type','').lower().startswith('multipart/'):raise ValueError('Encoded/chunked/multipart recovery refused')
            single('x-amz-version-id',source['version_id'])
            with Path(target).open('ab') as out:
                md5,sha=read_reserved_blocks(budget,phase,response,out,receipt,rec,{'bytes':remaining},budget.plan['limits']['read_chunk_bytes'],budget.plan['limits']['reservation_block_bytes'])
                out.flush();os.fsync(out.fileno())
        budget.guard()
        if rec['body_bytes']!=remaining or Path(target).stat().st_size!=source['bytes']:raise ValueError('Recovery tail/file size mismatch')
        rec.update(status='tail_received_not_source_verified',tail_md5=md5.hexdigest(),tail_sha256=sha.hexdigest(),charged_body_bytes=budget.state['transfer_bytes_consumed'])
        atomic_json(receipt,rec);return rec
    except BaseException as exc:
        rec.update(status='failed',error_type=type(exc).__name__);atomic_json(receipt,rec);raise


def recover(budget):
    plan=budget.plan;root=budget.root;original=Path(plan['original_root']);target=root/'recovered-index.partial'
    try:
        budget.begin('copy')
        if audit.inspect(original)!=plan['original_audit']:raise ValueError('Original audit changed; no recovery')
        copy_prefix(original/'index_archive.attempt-0.partial',target,{'bytes':plan['range_start'],'sha256':plan['original_audit']['partial_sha256']},budget.guard)
        budget.finish('copy');budget.begin('range')
        range_append(budget,target,plan['source'],plan['range_start']);budget.finish('range');budget.begin('verify')
        actual=file_hash(target,budget.guard)
        if actual!={'bytes':plan['source']['bytes'],'sha256':plan['source']['sha256']}:raise ValueError('Recovered whole index SHA256 mismatch; no promotion')
        if audit.inspect(original)!=plan['original_audit']:raise ValueError('Original changed during recovery')
        budget.guard();os.replace(target,root/'hg38_genome.tar.gz')
        directory=os.open(root,os.O_DIRECTORY)
        try:os.fsync(directory)
        finally:os.close(directory)
        budget.finish('verify');budget.state['status']='verified';budget.save()
        result={'status':'verified_archive_pending_outer_seal','archive':'hg38_genome.tar.gz',**actual,
            'cumulative_body_bytes':budget.state['transfer_bytes_consumed'],
            'additional_body_bytes':budget.state['transfer_bytes_consumed']-plan['original_audit']['charged_body_bytes'],
            'prior_transfer_elapsed_seconds':plan['original_audit']['prior_transfer_elapsed_seconds'],
            'additional_transfer_elapsed_seconds':budget.state['phases']['range']['finished_epoch']-budget.state['phases']['range']['started_epoch'],
            'state_sha256':meta_sha(root/'recovery-state.json'),'source_verified':True,'index_extracted':False,'raw_execution_ready':False}
        atomic_json(root/'recovery-result.json',result);return result
    except BaseException as exc:
        for phase in budget.state['phases'].values():
            if phase['status']=='started':phase.update(status='failed',error_type=type(exc).__name__,finished_epoch=budget.clock())
        budget.state.update(status='failed',error_type=type(exc).__name__);budget.save();raise


def monitor(plan,start):
    root=Path(plan['root'])
    def guard():
        if time.monotonic()-start>=plan['limits']['wall_seconds']:raise RuntimeError('External recovery total time cap')
        path=root/'recovery-state.json'
        if path.exists():
            state=read(path);now=time.time()
            if now<state['last_epoch'] or now>=state['deadline_epoch']:raise RuntimeError('External recovery wall clock')
            if not plan['original_audit']['charged_body_bytes']<=state['transfer_bytes_consumed']<=plan['limits']['transfer_bytes']:raise RuntimeError('External cumulative body cap')
            for name,phase in state['phases'].items():
                cap=plan['limits'][{'copy':'copy_seconds','range':'transfer_seconds','verify':'verify_seconds'}[name]]
                if phase['status']=='started' and now>=min(phase['deadline_epoch'],phase['started_epoch']+cap):raise RuntimeError('External recovery phase cap')
        disk_guard(plan)
    return guard


def accept_outer(root,plan,record):
    check_outer(record);root=Path(root);state=read(root/'recovery-state.json');result=read(root/'recovery-result.json');tail=read(root/'range-attempt.json')
    expected=plan['original_audit']['charged_body_bytes']+plan['source']['bytes']-plan['range_start']
    if read(root/'supervision/run.json')!=record or read(root/'recovery-plan.json')!=plan:raise ValueError('Recovery external receipt/descriptor changed')
    acceptance=read(root/'operator-acceptance.json')
    if acceptance.get('prepared_sha256')!=meta_sha(root/'recovery-plan.json') or acceptance.get('accepted_additional_time_window') is not True:raise ValueError('Recovery acceptance changed')
    if state.get('limits')!=plan['limits'] or state.get('original_deadline_epoch')!=plan['original_audit']['prior_global_deadline_epoch'] or state.get('prior_transfer_elapsed_seconds')!=plan['original_audit']['prior_transfer_elapsed_seconds']:raise ValueError('Recovery prior clock/limits changed')
    if state.get('status')!='verified' or set(state.get('phases',{}))!={'copy','range','verify'} or any(p.get('status')!='verified' for p in state['phases'].values()):raise ValueError('Recovery phases incomplete')
    if result.get('status')!='verified_archive_pending_outer_seal' or result.get('state_sha256')!=meta_sha(root/'recovery-state.json') or result.get('sha256')!=plan['source']['sha256'] or result.get('bytes')!=plan['source']['bytes'] or result.get('archive')!='hg38_genome.tar.gz':raise ValueError('Recovery result incomplete')
    if state['transfer_bytes_consumed']!=expected or result.get('cumulative_body_bytes')!=expected or tail.get('status')!='tail_received_not_source_verified' or tail.get('body_bytes')!=plan['source']['bytes']-plan['range_start'] or tail.get('charged_body_bytes')!=expected or tail.get('range_start')!=plan['range_start'] or tail.get('range_end')!=plan['range_end']:raise ValueError('Recovery body accounting mismatch')
    if not (root/'hg38_genome.tar.gz').is_file() or (root/'hg38_genome.tar.gz').is_symlink() or (root/'hg38_genome.tar.gz').stat().st_size!=result['bytes']:raise ValueError('Recovery output missing')
    seal={'status':'sealed_verified_index_archive','sha256':{name:meta_sha(root/name) for name in SEALED},
          'archive_sha256':result['sha256'],'archive_bytes':result['bytes'],'cumulative_body_bytes':expected,
          'remaining_body_budget_bytes':plan['limits']['transfer_bytes']-expected,'index_extracted':False,'raw_execution_ready':False}
    atomic_json(root/'recovery-seal.json',seal);return seal


def execute(prepared_file,accepted_sha256,accept_additional_time=False):
    if not accept_additional_time:raise ValueError('Explicit additional time-window acknowledgment required; old clock is exhausted')
    if not re.fullmatch('[0-9a-f]{64}',accepted_sha256 or '') or meta_sha(prepared_file)!=accepted_sha256:raise ValueError('Exact prepared recovery SHA256 acceptance required')
    plan=read(prepared_file);root=validate_plan(plan)
    if shutil.disk_usage(Path(plan['original_root'])).free<plan['limits']['disk_bytes']+plan['limits']['reserve_bytes']:raise ValueError('33 GiB free required')
    root.mkdir(exist_ok=False)
    with (root/'recovery-plan.json').open('xb') as f:f.write(Path(prepared_file).read_bytes());f.flush();os.fsync(f.fileno())
    atomic_json(root/'operator-acceptance.json',{'prepared_sha256':accepted_sha256,'accepted_additional_time_window':True,'accepted_epoch':time.time(),'prior_deadline_unchanged':plan['original_audit']['prior_global_deadline_epoch']})
    start=time.monotonic();limits=plan['limits']
    rec=supervise('run',[sys.executable,str(Path(__file__).resolve()),'--worker',str(root/'recovery-plan.json')],root/'supervision',timeout=limits['wall_seconds'],rss_limit=limits['rss_bytes'],address_space=limits['address_space_bytes'],checkpoint=monitor(plan,start))
    return accept_outer(root,plan,rec)


def worker_file(path):
    plan=read(path);root=validate_plan(plan)
    if Path(path).resolve()!=root/'recovery-plan.json':raise ValueError('Fixed worker descriptor path required')
    acceptance=read(root/'operator-acceptance.json')
    if acceptance.get('prepared_sha256')!=meta_sha(path) or acceptance.get('accepted_additional_time_window') is not True:raise ValueError('Worker missing exact plan/time acceptance')
    until=time.monotonic()+2;receipt=root/'supervision/run.json';outer=read(receipt)
    while outer.get('status')=='started' and 'procfs_group' not in outer and time.monotonic()<until:
        time.sleep(.01);outer=read(receipt)
    group=proc_info(int(os.readlink('/proc/self')))['group']
    if outer.get('status')!='started' or outer.get('procfs_group')!=group:raise ValueError('Recovery requires active parent supervisor')
    recover(Budget(plan))


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--prepare',type=Path);g.add_argument('--execute',type=Path);g.add_argument('--worker',type=Path,help=argparse.SUPPRESS)
    p.add_argument('--original',type=Path);p.add_argument('--accept-plan-sha256');p.add_argument('--accept-additional-time-window',action='store_true');a=p.parse_args()
    if a.prepare:
        if not a.original:p.error('--prepare requires --original')
        plan=prepare(a.original)
        with a.prepare.open('x') as f:json.dump(plan,f,indent=2);f.write('\n')
        print(json.dumps({'prepared_file':str(a.prepare),'sha256':meta_sha(a.prepare),'execution_enabled':False,
            'root':plan['root'],'scope':plan['scope'],'remaining_index_body_bytes':SOURCE['bytes']-plan['range_start'],
            'prior_charged_body_bytes':plan['original_audit']['charged_body_bytes'],
            'expected_cumulative_body_bytes_after_recovery':plan['original_audit']['charged_body_bytes']+SOURCE['bytes']-plan['range_start'],
            'proposed_additional_transfer_seconds':LIMITS['transfer_seconds'],'proposed_recovery_wall_seconds':LIMITS['wall_seconds'],
            'prior_deadline_unchanged':plan['original_audit']['prior_global_deadline_epoch'],'raw_execution_ready':False},indent=2))
    elif a.execute:print(json.dumps(execute(a.execute,a.accept_plan_sha256,a.accept_additional_time_window),indent=2))
    else:worker_file(a.worker)


if __name__=='__main__':main()
