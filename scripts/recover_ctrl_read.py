"""Recover only the interrupted CTRL_R1 gzip; --prepare never starts HTTP.

Original run is immutable. Explicit exact-plan and NEW time acceptance required.
No retries, other mates, decompression, alignment or automatic pilot restart.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import time
import urllib.request

import cached_index_pilot as cached
import real_pilot_workflow as real
import recover_index_range as base
from bounded_http_transport import NoRedirect,read_reserved_blocks
from process_supervisor_v2 import atomic_json,supervise,proc_info
from workflow_seal import read,sha as meta_sha,check_outer
from pilot_execution_policy import iter_files

GiB=1024**3
JOB_SHA='15f85f9dc42b991732204589f9cf10f7404830ffc725a2581512eddf92da9d18'
FINGERPRINT='44e3396df12f3e8ecda149d77c629bacd54c1852610b8f5a851ba59e48ed6087'
SOURCE={'url':'https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR334/016/SRR33425816/SRR33425816_1.fastq.gz','bytes':960856963,'md5':'ed58daa011d6508a3e8d1f05bc39fc29'}
LIMITS={**base.LIMITS,'socket_seconds':30}
CODE=tuple(sorted(set(base.CODE+cached.CODE+('recover_ctrl_read.py',))))
META=('workflow-job.json','operator-acceptance.json','ledger.json','cached-preflight.json','CTRL_R1.attempt-0.json','workflow-receipts/run.json')
SEALED=base.SEALED
SCOPE='recover CTRL_R1 only; no other mates, FASTQ decompression, alignment or pilot restart'
TIME_REVIEW='NEW2400s recovery window including1800s HTTP; old deadlines and spent clocks unchanged'


def identity():
    return {'python_sha256':base.file_hash(sys.executable)['sha256'],'code_sha256':{n:base.file_hash(Path(__file__).with_name(n))['sha256'] for n in CODE}}


def recovery_root(original):return Path(original).with_name(Path(original).name+'-CTRL_R1-recovery-01')


def inspect(original,guard=lambda:None):
    original=Path(original).resolve()
    if any((original/n).is_symlink() for n in META):raise ValueError('Original metadata symlink')
    hashes={n:meta_sha(original/n) for n in META}
    if hashes['workflow-job.json']!=JOB_SHA:raise ValueError('Exact failed WSL job required')
    job=read(original/'workflow-job.json');real.validate_job(job)
    if job['root']!=str(original):raise ValueError('Failed job root differs')
    acceptance=read(original/'operator-acceptance.json')
    if acceptance.get('prepared_file_sha256')!=JOB_SHA or acceptance.get('accepted_cached_run_window') is not True:raise ValueError('Original accepted cached plan required')
    state=read(original/'ledger.json');outer=read(original/'workflow-receipts/run.json');attempt=read(original/'CTRL_R1.attempt-0.json')
    if outer.get('status')!='finished' or outer.get('exit_code')!=1 or outer.get('violation') is not None or outer.get('supervisor_error') is not None or outer.get('live_group_members_after_cleanup')!=[]:raise ValueError('Cleanly stopped failed worker required')
    phases=state.get('phases',{});pre=phases.get('preflight',{});phase=phases.get('CTRL_R1',{})
    if state.get('fingerprint')!=FINGERPRINT or state.get('mode')!='real-pilot' or set(phases)!={'preflight','CTRL_R1'} or pre.get('status')!='verified' or phase.get('status')!='failed' or phase.get('error')!='TimeoutError: The read operation timed out':raise ValueError('Exact interrupted CTRL_R1 phase required')
    if pre.get('receipt')!='cached-preflight.json' or pre.get('receipt_sha256')!=hashes['cached-preflight.json']:raise ValueError('Preflight receipt changed')
    binding=job['manifest']['cached_index']
    if cached.index_binding(binding['index_root'])!=binding:raise ValueError('Index lineage changed')
    if state.get('transfer_bytes_consumed')!=4712318573 or state.get('transfer_elapsed_seconds')!=523.6879758834839 or state.get('cumulative_transfer_elapsed_seconds')!=4272.2037699222565 or state.get('prior_transfer_elapsed_seconds')!=3748.5157940387726 or state.get('deadline_epoch')!=1793698176.656901:raise ValueError('Observed prior charge/clock changed')
    if attempt.get('status')!='failed' or attempt.get('attempt')!=0 or attempt.get('body_bytes')!=354631727 or attempt.get('expected_checksums')!={'md5':SOURCE['md5']} or attempt.get('accounting')!='durable-block-reservation-v1' or attempt.get('reservation_block_bytes')!=4194304 or attempt.get('reserve_reads') is not True or attempt.get('error')!=phase['error']:raise ValueError('Failed transfer receipt changed')
    if phase.get('reservation_start_body_bytes')!=352321536 or phase.get('unsettled_body_reservation_bytes')!=4194304:raise ValueError('Conservative reservation changed')
    partial=original/'CTRL_R1.attempt-0.partial'
    if partial.is_symlink() or partial.stat().st_size!=attempt['body_bytes']:raise ValueError('Partial size differs from receipt')
    actual=base.file_hash(partial,guard)
    if hashes!={n:meta_sha(original/n) for n in META}:raise ValueError('Original changed during audit')
    return {'root':str(original),'metadata_sha256':hashes,'partial_bytes':actual['bytes'],'partial_sha256':actual['sha256'],
            'charged_body_bytes':state['transfer_bytes_consumed'],'prior_transfer_elapsed_seconds':state['cumulative_transfer_elapsed_seconds'],
            'prior_global_deadline_epoch':state['deadline_epoch'],'cached_index':binding}


def prepare(original):
    original=Path(original).expanduser().resolve();root=recovery_root(original)
    if root.exists():raise ValueError('Recovery root exists; no automatic retry')
    obs=inspect(original)
    if shutil.disk_usage(original).free<LIMITS['disk_bytes']+LIMITS['reserve_bytes']:raise ValueError('33 GiB free required')
    return {'schema':'ctrl-r1-only-range-recovery-v1','execution_enabled':False,'original_root':str(original),'root':str(root),'original_audit':obs,
            'source':dict(SOURCE),'limits':dict(LIMITS),'identity':identity(),'range_start':obs['partial_bytes'],'range_end':SOURCE['bytes']-1,'scope':SCOPE,'time_review':TIME_REVIEW}


def validate_plan(plan):
    keys={'schema','execution_enabled','original_root','root','original_audit','source','limits','identity','range_start','range_end','scope','time_review'}
    if not isinstance(plan,dict) or set(plan)!=keys or plan['schema']!='ctrl-r1-only-range-recovery-v1' or plan['execution_enabled'] is not False:raise ValueError('Disabled fixed CTRL_R1 recovery required')
    original=Path(plan['original_root']);root=Path(plan['root']);obs=plan['original_audit']
    if not original.is_absolute() or original!=original.resolve() or root!=recovery_root(original) or root!=root.resolve() or obs['root']!=str(original):raise ValueError('Canonical exclusive recovery lineage required')
    if plan['source']!=SOURCE or plan['limits']!=LIMITS or plan['identity']!=identity() or plan['scope']!=SCOPE or plan['time_review']!=TIME_REVIEW:raise ValueError('Pinned recovery source/resources/code changed')
    if type(plan['range_start']) is not int or plan['range_start']!=354631727 or obs['partial_bytes']!=plan['range_start'] or plan['range_end']!=SOURCE['bytes']-1 or not re.fullmatch('[0-9a-f]{64}',str(obs['partial_sha256'])):raise ValueError('Exact failed partial required')
    if obs['charged_body_bytes']!=4712318573 or obs['prior_transfer_elapsed_seconds']!=4272.2037699222565 or obs['prior_global_deadline_epoch']!=1793698176.656901:raise ValueError('Prior charges/time cannot be refunded')
    if obs['charged_body_bytes']+SOURCE['bytes']-plan['range_start']>LIMITS['transfer_bytes']:raise ValueError('Remaining body cap')
    return root


def disk_guard(plan):
    binding=plan['original_audit']['cached_index'];roots=[binding[k] for k in ('original_root','recovery_root','index_root')]+[plan['original_root'],plan['root']]
    if len(set(roots))!=5:raise ValueError('Distinct lineage roots required')
    total=0
    for root in roots:
        for path in iter_files(root):
            try:
                if path.is_symlink():raise ValueError('Lineage symlink')
                if path.is_file():total+=path.stat().st_size
            except FileNotFoundError:pass
    if total>plan['limits']['disk_bytes'] or shutil.disk_usage(plan['original_root']).free<plan['limits']['reserve_bytes']:raise RuntimeError('Lineage disk cap/reserve')


class Budget(base.Budget):
    def guard(self):
        now=self.clock()
        if now<self.state['last_epoch'] or now>=self.state['deadline_epoch']:raise RuntimeError('Recovery clock/deadline')
        self.state['last_epoch']=now
        if any(p['status']=='started' and now>=p['deadline_epoch'] for p in self.state['phases'].values()):raise RuntimeError('Recovery phase time cap')
        if not self.plan['original_audit']['charged_body_bytes']<=self.state['transfer_bytes_consumed']<=self.plan['limits']['transfer_bytes']:raise RuntimeError('Cumulative body cap')
        tick=time.monotonic()
        if tick-getattr(self,'last_disk_check',float('-inf'))>=.1:disk_guard(self.plan);self.last_disk_check=tick


def range_append(budget,target,source,start):
    remaining=source['bytes']-start;phase=budget.state['phases']['range']
    if remaining<=0 or remaining>budget.state['limits']['transfer_bytes']-budget.state['transfer_bytes_consumed']:raise ValueError('Remaining range exceeds body budget')
    if Path(target).is_symlink() or Path(target).stat().st_size!=start:raise ValueError('Exact copied prefix required')
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect());request=urllib.request.Request(source['url'],headers={'Accept-Encoding':'identity','Range':f"bytes={start}-{source['bytes']-1}"})
    rec={'status':'started','body_bytes':0,'range_start':start,'range_end':source['bytes']-1,'prior_charged_bytes':budget.state['transfer_bytes_consumed'],'attempts':1,'budget_scope':'HTTP entity-body read, not wire bytes'};receipt=budget.root/'range-attempt.json';atomic_json(receipt,rec)
    try:
        with opener.open(request,timeout=min(budget.plan['limits']['socket_seconds'],budget.remaining())) as response:
            headers=response.headers
            def single(name,value):
                if headers.get_all(name)!=[value]:raise ValueError('Recovery response '+name+' mismatch')
            if response.status!=206:raise ValueError('HTTP206 required; no full response append')
            single('Content-Length',str(remaining));single('Content-Range',f"bytes {start}-{source['bytes']-1}/{source['bytes']}")
            if headers.get('Content-Encoding','identity')!='identity' or headers.get('Transfer-Encoding') or headers.get('Content-Type','').lower().startswith('multipart/'):raise ValueError('Encoded/chunked/multipart response refused')
            with Path(target).open('ab') as out:
                read_reserved_blocks(budget,phase,response,out,receipt,rec,{'bytes':remaining},65536,4194304);out.flush();os.fsync(out.fileno())
        budget.guard()
        if rec['body_bytes']!=remaining or Path(target).stat().st_size!=source['bytes']:raise ValueError('Tail/file size mismatch')
        rec.update(status='tail_received_not_source_verified',charged_body_bytes=budget.state['transfer_bytes_consumed']);atomic_json(receipt,rec)
    except BaseException as exc:
        rec.update(status='failed',error_type=type(exc).__name__);atomic_json(receipt,rec);raise


def whole_hash(path,guard):
    md5=hashlib.md5();sha=hashlib.sha256();size=0
    with Path(path).open('rb') as f:
        while True:
            guard();data=f.read(1024**2)
            if not data:break
            size+=len(data);md5.update(data);sha.update(data)
    return {'bytes':size,'md5':md5.hexdigest(),'sha256':sha.hexdigest()}


def recover(budget):
    p=budget.plan;root=budget.root;target=root/'recovered-CTRL_R1.partial'
    try:
        budget.begin('copy')
        if inspect(p['original_root'],budget.guard)!=p['original_audit']:raise ValueError('Original changed')
        base.copy_prefix(Path(p['original_root'])/'CTRL_R1.attempt-0.partial',target,{'bytes':p['range_start'],'sha256':p['original_audit']['partial_sha256']},budget.guard)
        budget.finish('copy');budget.begin('range');range_append(budget,target,p['source'],p['range_start']);budget.finish('range');budget.begin('verify')
        actual=whole_hash(target,budget.guard)
        if actual['bytes']!=p['source']['bytes'] or actual['md5']!=p['source']['md5']:raise ValueError('Whole recovered FASTQ MD5/size mismatch')
        if inspect(p['original_root'],budget.guard)!=p['original_audit']:raise ValueError('Original changed during recovery')
        budget.guard();os.replace(target,root/'CTRL_R1.fastq.gz');directory=os.open(root,os.O_DIRECTORY)
        try:os.fsync(directory)
        finally:os.close(directory)
        budget.finish('verify');budget.state['status']='verified';budget.save()
        atomic_json(root/'recovery-result.json',{'status':'verified_ctrl_r1_pending_outer_seal','file':'CTRL_R1.fastq.gz',**actual,'state_sha256':meta_sha(root/'recovery-state.json'),'cumulative_body_bytes':budget.state['transfer_bytes_consumed'],'additional_body_bytes':budget.state['transfer_bytes_consumed']-p['original_audit']['charged_body_bytes'],'prior_transfer_elapsed_seconds':p['original_audit']['prior_transfer_elapsed_seconds'],'additional_transfer_elapsed_seconds':budget.state['phases']['range']['finished_epoch']-budget.state['phases']['range']['started_epoch'],'source_verified':True,'raw_execution_ready':False})
    except BaseException as exc:
        for phase in budget.state['phases'].values():
            if phase['status']=='started':phase.update(status='failed',error_type=type(exc).__name__,finished_epoch=budget.clock())
        budget.state.update(status='failed',error_type=type(exc).__name__);budget.save();raise


def monitor(plan,start):
    last=[float('-inf')]
    def guard():
        if time.monotonic()-start>=plan['limits']['wall_seconds']:raise RuntimeError('External total time cap')
        path=Path(plan['root'])/'recovery-state.json'
        if path.exists():
            state=read(path);now=time.time()
            if state['limits']!=plan['limits'] or state['original_deadline_epoch']!=plan['original_audit']['prior_global_deadline_epoch'] or state['prior_transfer_elapsed_seconds']!=plan['original_audit']['prior_transfer_elapsed_seconds']:raise RuntimeError('External prior limits/clocks changed')
            if now<state['last_epoch'] or now>=state['deadline_epoch'] or not plan['original_audit']['charged_body_bytes']<=state['transfer_bytes_consumed']<=plan['limits']['transfer_bytes']:raise RuntimeError('External clock/body cap')
            for name,phase in state['phases'].items():
                cap=plan['limits'][{'copy':'copy_seconds','range':'transfer_seconds','verify':'verify_seconds'}[name]]
                if phase['status']=='started' and now>=min(phase['deadline_epoch'],phase['started_epoch']+cap):raise RuntimeError('External phase time cap')
        tick=time.monotonic()
        if tick-last[0]>=.1:disk_guard(plan);last[0]=tick
    return guard


def accept_outer(root,plan,record):
    check_outer(record);root=Path(root);state=read(root/'recovery-state.json');result=read(root/'recovery-result.json');tail=read(root/'range-attempt.json');expected=plan['original_audit']['charged_body_bytes']+plan['source']['bytes']-plan['range_start']
    if read(root/'supervision/run.json')!=record or read(root/'recovery-plan.json')!=plan:raise ValueError('Outer receipt/plan changed')
    acceptance=read(root/'operator-acceptance.json')
    if acceptance.get('prepared_sha256')!=meta_sha(root/'recovery-plan.json') or acceptance.get('accepted_additional_time_window') is not True:raise ValueError('Missing acceptance')
    if state.get('limits')!=plan['limits'] or state.get('original_deadline_epoch')!=plan['original_audit']['prior_global_deadline_epoch'] or state.get('prior_transfer_elapsed_seconds')!=plan['original_audit']['prior_transfer_elapsed_seconds'] or state.get('status')!='verified' or set(state.get('phases',{}))!={'copy','range','verify'} or any(p.get('status')!='verified' for p in state['phases'].values()):raise ValueError('Incomplete recovery state')
    if result.get('status')!='verified_ctrl_r1_pending_outer_seal' or result.get('state_sha256')!=meta_sha(root/'recovery-state.json') or result.get('bytes')!=SOURCE['bytes'] or result.get('md5')!=SOURCE['md5'] or not re.fullmatch('[0-9a-f]{64}',str(result.get('sha256',''))) or result.get('file')!='CTRL_R1.fastq.gz':raise ValueError('Recovered result incomplete')
    if state['transfer_bytes_consumed']!=expected or result.get('cumulative_body_bytes')!=expected or result.get('additional_body_bytes')!=SOURCE['bytes']-plan['range_start'] or tail.get('status')!='tail_received_not_source_verified' or tail.get('body_bytes')!=SOURCE['bytes']-plan['range_start'] or tail.get('charged_body_bytes')!=expected or tail.get('range_start')!=plan['range_start'] or tail.get('range_end')!=plan['range_end']:raise ValueError('Body accounting mismatch')
    out=root/'CTRL_R1.fastq.gz'
    if out.is_symlink() or not out.is_file() or out.stat().st_size!=SOURCE['bytes']:raise ValueError('Recovered output missing')
    seal={'status':'sealed_verified_ctrl_r1','sha256':{n:meta_sha(root/n) for n in SEALED},'file':'CTRL_R1.fastq.gz','file_sha256':result['sha256'],'file_md5':result['md5'],'file_bytes':result['bytes'],'cumulative_body_bytes':expected,'remaining_body_budget_bytes':LIMITS['transfer_bytes']-expected,'raw_execution_ready':False};atomic_json(root/'recovery-seal.json',seal);return seal


def execute(path,accepted,accept_time=False):
    if not accept_time:raise ValueError('Explicit NEW recovery time acceptance required')
    if not re.fullmatch('[0-9a-f]{64}',accepted or '') or meta_sha(path)!=accepted:raise ValueError('Exact prepared SHA acceptance required')
    plan=read(path);root=validate_plan(plan)
    if root.exists():raise ValueError('Attempted recovery cannot be reused')
    disk_guard(plan)
    if shutil.disk_usage(plan['original_root']).free<LIMITS['disk_bytes']+LIMITS['reserve_bytes']:raise ValueError('33 GiB free required')
    root.mkdir(exist_ok=False)
    with (root/'recovery-plan.json').open('xb') as f:f.write(Path(path).read_bytes());f.flush();os.fsync(f.fileno())
    atomic_json(root/'operator-acceptance.json',{'prepared_sha256':accepted,'accepted_additional_time_window':True,'accepted_epoch':time.time()})
    rec=supervise('run',[sys.executable,str(Path(__file__).resolve()),'--worker',str(root/'recovery-plan.json')],root/'supervision',timeout=LIMITS['wall_seconds'],rss_limit=LIMITS['rss_bytes'],address_space=LIMITS['address_space_bytes'],checkpoint=monitor(plan,time.monotonic()))
    return accept_outer(root,plan,rec)


def worker_file(path):
    plan=read(path);root=validate_plan(plan)
    if Path(path).resolve()!=root/'recovery-plan.json':raise ValueError('Fixed worker path')
    a=read(root/'operator-acceptance.json')
    if a.get('prepared_sha256')!=meta_sha(path) or a.get('accepted_additional_time_window') is not True:raise ValueError('Missing worker acceptance')
    receipt=root/'supervision/run.json';outer=read(receipt);until=time.monotonic()+2
    while outer.get('status')=='started' and 'procfs_group' not in outer and time.monotonic()<until:time.sleep(.01);outer=read(receipt)
    if outer.get('status')!='started' or outer.get('procfs_group')!=proc_info(int(os.readlink('/proc/self')))['group']:raise ValueError('Active parent supervisor required')
    recover(Budget(plan))


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--prepare',type=Path);g.add_argument('--execute',type=Path);g.add_argument('--worker',type=Path,help=argparse.SUPPRESS);p.add_argument('--original',type=Path);p.add_argument('--accept-plan-sha256');p.add_argument('--accept-additional-time-window',action='store_true');a=p.parse_args()
    if a.prepare:
        if not a.original:p.error('--original required')
        plan=prepare(a.original)
        with a.prepare.open('x') as f:json.dump(plan,f,indent=2);f.write('\n')
        print(json.dumps({'prepared_file':str(a.prepare),'sha256':meta_sha(a.prepare),'execution_enabled':False,'root':plan['root'],'scope':SCOPE,'remaining_read_body_bytes':SOURCE['bytes']-plan['range_start'],'prior_charged_body_bytes':plan['original_audit']['charged_body_bytes'],'expected_cumulative_body_bytes_after_recovery':plan['original_audit']['charged_body_bytes']+SOURCE['bytes']-plan['range_start'],'additional_transfer_seconds':LIMITS['transfer_seconds'],'new_wall_seconds':LIMITS['wall_seconds'],'raw_execution_ready':False},indent=2))
    elif a.execute:print(json.dumps(execute(a.execute,a.accept_plan_sha256,a.accept_additional_time_window),indent=2))
    else:worker_file(a.worker)


if __name__=='__main__':main()
