"""Explicit new pilot from sealed index and recovered CTRL_R1, never a retry.

--prepare emits a disabled plan. Three remaining HTTP files only. Historical
workers stay unchanged; byte charges and old clocks are retained. New 27GiB disk
cap keeps all partials plus a verified local copy; requires exact plan acceptance.
"""
import argparse
import copy
import fcntl
import json
import os
from pathlib import Path
import re
import resource
import sys
import time

import cached_index_pilot as cached
import recover_ctrl_read as recovery
import real_pilot_workflow as real
import pilot_execution_policy as policy
from pilot_dry_runner import DryRunner,digest
from process_supervisor_v2 import atomic_json,supervise,proc_info
from workflow_seal import read,sha,check_outer

GiB=1024**3
PLAN_SHA='e462886c47e9e95a94b8e96b4e52813069ace57c7d5bbf7b72dde0d12c3d43fe'
READ_SHA='298a8b4769fcd5434f883706c873d56795c5a20d855917d80a391b2e5c38beff'
CHARGED=5318543809
CODE=tuple(sorted(set(recovery.CODE+('recovered_read_pilot.py',))))
FILES=('workflow-job.json','operator-acceptance.json','ledger.json','workflow-inner.json','workflow-receipts/run.json')
SCOPE='NEW7200s pilot/1800s transfers including local copy; disk27GiB/artifacts18GiB; sealed index and CTRL_R1 reused; prior charges/clocks unchanged; no biological inference'


def identity():
    return {'python_sha256':recovery.base.file_hash(sys.executable)['sha256'],'code_sha256':{n:recovery.base.file_hash(Path(__file__).with_name(n))['sha256'] for n in CODE},'decoder':real.decoder_identity()}


def read_binding(root):
    root=Path(root).resolve();seal=read(root/'recovery-seal.json')
    if seal.get('status')!='sealed_verified_ctrl_r1' or set(seal.get('sha256',{}))!=set(recovery.SEALED):raise ValueError('Sealed recovered CTRL_R1 required')
    for n in recovery.SEALED:
        if (root/n).is_symlink() or sha(root/n)!=seal['sha256'][n]:raise ValueError('Recovered read metadata changed')
    plan=read(root/'recovery-plan.json');accept=read(root/'operator-acceptance.json');result=read(root/'recovery-result.json');state=read(root/'recovery-state.json');tail=read(root/'range-attempt.json');check_outer(read(root/'supervision/run.json'))
    if sha(root/'recovery-plan.json')!=PLAN_SHA or recovery.validate_plan(plan)!=root or accept.get('prepared_sha256')!=PLAN_SHA or accept.get('accepted_additional_time_window') is not True:raise ValueError('Exact accepted recovery plan required')
    obs=plan['original_audit'];original=Path(plan['original_root'])
    if any((original/n).is_symlink() or sha(original/n)!=v for n,v in obs['metadata_sha256'].items()):raise ValueError('Failed run metadata changed')
    index=obs['cached_index']
    if cached.index_binding(index['index_root'])!=index:raise ValueError('Cached index lineage changed')
    if state.get('status')!='verified' or state.get('limits')!=plan['limits'] or state.get('original_deadline_epoch')!=obs['prior_global_deadline_epoch'] or state.get('prior_transfer_elapsed_seconds')!=obs['prior_transfer_elapsed_seconds'] or set(state.get('phases',{}))!={'copy','range','verify'} or any(p.get('status')!='verified' for p in state['phases'].values()):raise ValueError('Recovery phases/clocks incomplete')
    if result.get('status')!='verified_ctrl_r1_pending_outer_seal' or result.get('state_sha256')!=sha(root/'recovery-state.json') or result.get('source_verified') is not True or result.get('file')!='CTRL_R1.fastq.gz' or result.get('bytes')!=recovery.SOURCE['bytes'] or result.get('md5')!=recovery.SOURCE['md5'] or result.get('sha256')!=READ_SHA:raise ValueError('Recovered full read identity changed')
    if seal.get('file_sha256')!=READ_SHA or seal.get('file_md5')!=result['md5'] or seal.get('file_bytes')!=result['bytes'] or seal.get('file')!=result['file']:raise ValueError('Recovered output seal differs')
    if any(r.get('cumulative_body_bytes')!=CHARGED for r in (seal,result)) or state.get('transfer_bytes_consumed')!=CHARGED or seal.get('remaining_body_budget_bytes')!=12_000_000_000-CHARGED or result.get('additional_body_bytes')!=606225236 or tail.get('body_bytes')!=606225236 or tail.get('charged_body_bytes')!=CHARGED or tail.get('range_start')!=354631727 or tail.get('range_end')!=960856962 or tail.get('status')!='tail_received_not_source_verified':raise ValueError('Recovered cumulative body accounting differs')
    elapsed=state['phases']['range']['finished_epoch']-state['phases']['range']['started_epoch']
    if not 0<=elapsed<=1800 or result.get('additional_transfer_elapsed_seconds')!=elapsed or result.get('prior_transfer_elapsed_seconds')!=obs['prior_transfer_elapsed_seconds']:raise ValueError('Recovered transfer clock differs')
    return {'root':str(root),'seal_sha256':sha(root/'recovery-seal.json'),'original_root':str(original),'index':index,'file':'CTRL_R1.fastq.gz','bytes':result['bytes'],'md5':result['md5'],'sha256':READ_SHA,'cumulative_body_bytes':CHARGED,'prior_transfer_elapsed_seconds':obs['prior_transfer_elapsed_seconds']+elapsed,'prior_deadline_epoch':obs['prior_global_deadline_epoch']}


def output_root(binding):return Path(binding['root']).with_name(Path(binding['root']).name+'-pilot-01')


def make_manifest(binding):
    if read_binding(binding['root'])!=binding:raise ValueError('Read cache binding changed')
    m,l=cached.make_manifest(binding['index']['aligner'],binding['index']);m=copy.deepcopy(m);l=copy.deepcopy(l)
    l['disk_bytes']=27*GiB;m['execution_policy']['allocations']['artifacts']=18*GiB
    m['recovered_read']=binding
    step=next(s for s in m['sealed_workflow']['steps'] if s['name']=='CTRL_R1');step.clear();step.update(name='CTRL_R1',kind='local_read')
    m['execution_policy']['phases']['CTRL_R1']['wall_seconds']=180
    policy.validate(m['execution_policy'],l,allow_real=True)
    return m,l


def prepare(root):
    b=read_binding(Path(root).expanduser().resolve());out=output_root(b)
    if out.exists():raise ValueError('New pilot root exists; no retry')
    m,l=make_manifest(b)
    return {'schema':'recovered-read-pilot-v1','execution_enabled':False,'root':str(out),'manifest':m,'limits':l,'identity':identity(),'host_observed':real.check_host(out,l),'scope':SCOPE,'unverified':['actual human alignment resources and target coverage']}


def validate_job(job):
    if not isinstance(job,dict) or set(job)!={'schema','execution_enabled','root','manifest','limits','identity','host_observed','scope','unverified'} or job['schema']!='recovered-read-pilot-v1' or job['execution_enabled'] is not False:raise ValueError('Disabled recovered-read pilot required')
    b=job['manifest']['recovered_read'];m,l=make_manifest(b)
    if job['manifest']!=m or job['limits']!=l or job['identity']!=identity() or job['scope']!=SCOPE or Path(job['root'])!=output_root(b):raise ValueError('Fixed samples/code/resources/lineage changed')
    return Path(job['root'])


def combined_disk_guard(root,state,m,l):
    b=m['recovered_read'];usage=policy.disk_usage(root,state);extra=cached.lineage_usage(b['index'])
    for base in (b['original_root'],b['root']):
        for path in policy.iter_files(base):
            try:
                if path.is_symlink():raise ValueError('Read lineage symlink')
                if path.is_file():extra+=path.stat().st_size
            except FileNotFoundError:pass
    usage['artifacts']+=extra
    if sum(usage.values())>l['disk_bytes'] or any(usage[k]>m['execution_policy']['allocations'][k] for k in usage):raise RuntimeError('Whole lineage disk/partition cap')
    import shutil
    if shutil.disk_usage(root).free<l['reserve_bytes']:raise RuntimeError('Free disk reserve')


class Runner(DryRunner):
    """New exclusive ledger, retaining old phase methods without modifying them."""
    def __init__(self,job):
        self.root=validate_job(job);self.root.mkdir(exist_ok=True);self.clock=time.time;self.manifest=copy.deepcopy(job['manifest']);l=job['limits'];self.policy=policy.validate(self.manifest['execution_policy'],l,allow_real=True)
        self.lock=(self.root/'runner.lock').open('a')
        try:
            fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB);self.path=self.root/'ledger.json'
            if self.path.exists():raise ValueError('Never reopen failed/completed pilot')
            now=self.clock();b=self.manifest['recovered_read'];self.state={'fingerprint':digest({'manifest':self.manifest,'limits':l}),'limits':l,'deadline_epoch':now+l['wall_seconds'],'transfer_bytes_consumed':b['cumulative_body_bytes'],'prior_transfer_elapsed_seconds':b['prior_transfer_elapsed_seconds'],'prior_deadline_epoch':b['prior_deadline_epoch'],'phases':{},'mode':'real-pilot','raw_pilot_ready':False,'last_epoch':now,'transfer_elapsed_seconds':0};self.save();self.guard()
        except BaseException:self.lock.close();raise
    def guard(self):
        now=self.clock()
        if now<getattr(self,'observed_epoch',self.state['last_epoch']) or now>=self.state['deadline_epoch']:raise RuntimeError('Pilot clock/deadline')
        self.observed_epoch=now;policy.guard_clocks(self.state,self.policy,now)
        if not self.manifest['recovered_read']['cumulative_body_bytes']<=self.state['transfer_bytes_consumed']<=self.state['limits']['transfer_bytes']:raise RuntimeError('Cumulative body cap/floor')
        tick=time.monotonic()
        if tick-getattr(self,'last_disk',float('-inf'))>=.1:combined_disk_guard(self.root,self.state,self.manifest,self.state['limits']);self.last_disk=tick


def adopt_read(runner):
    b=runner.manifest['recovered_read'];signature=digest(b)
    if not runner.begin('CTRL_R1','transfer',signature):raise ValueError('Never adopt prior phase')
    phase=runner.state['phases']['CTRL_R1'];target=runner.root/'CTRL_R1.partial';source=Path(b['root'])/b['file']
    try:
        if read_binding(b['root'])!=b:raise ValueError('Read metadata changed')
        expected={'bytes':b['bytes'],'sha256':b['sha256']}
        if recovery.whole_hash(source,runner.guard)!={**expected,'md5':b['md5']}:raise ValueError('Recovered read checksum changed')
        recovery.base.copy_prefix(source,target,expected,runner.guard)
        if read_binding(b['root'])!=b or recovery.whole_hash(source,runner.guard)!={**expected,'md5':b['md5']}:raise ValueError('Read changed during local copy')
        runner.guard();os.replace(target,runner.root/'CTRL_R1');fd=os.open(runner.root,os.O_DIRECTORY)
        try:os.fsync(fd)
        finally:os.close(fd)
        phase.update(status='verified',**expected,md5=b['md5'],local_recovered_source=b,new_body_bytes=0);runner.save()
    except BaseException as exc:phase.update(status='failed',error_type=type(exc).__name__);runner.save();raise


def transfer_read(runner,step):
    """Fixed remaining mate, single HTTP200 attempt with30s socket timeout."""
    import hashlib
    import urllib.request
    from bounded_http_transport import NoRedirect,read_reserved_blocks
    name=step['name'];expected=step['expected'];signature=digest({'step':step,'socket_seconds':30})
    if not runner.begin(name,'transfer',signature):raise ValueError('No transfer retry')
    phase=runner.state['phases'][name];partial=runner.root/(name+'.attempt-0.partial');receipt=runner.root/(name+'.attempt-0.json');rec={'status':'started','attempt':0,'body_bytes':0,'budget_scope':'HTTP entity-body read, not wire bytes'};atomic_json(receipt,rec)
    try:
        if expected['bytes']>runner.state['limits']['transfer_bytes']-runner.state['transfer_bytes_consumed']:raise ValueError('Remaining mate exceeds body cap')
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect());request=urllib.request.Request(step['url'],headers={'Accept-Encoding':'identity'})
        with opener.open(request,timeout=min(30,runner.remaining(name,'transfer'))) as response:
            if response.status!=200 or response.headers.get_all('Content-Length')!=[str(expected['bytes'])] or response.headers.get('Content-Encoding','identity')!='identity' or response.headers.get('Transfer-Encoding') or response.headers.get('Content-Range'):raise ValueError('Exact unencoded full mate response required')
            with partial.open('xb') as out:
                md5,sha256=read_reserved_blocks(runner,phase,response,out,receipt,rec,expected,65536,4194304);out.flush();os.fsync(out.fileno())
        if rec['body_bytes']!=expected['bytes'] or md5.hexdigest()!=expected['md5'] or partial.stat().st_size!=expected['bytes']:raise ValueError('Whole mate MD5/size mismatch')
        runner.guard();os.replace(partial,runner.root/name);fd=os.open(runner.root,os.O_DIRECTORY)
        try:os.fsync(fd)
        finally:os.close(fd)
        rec.update(status='verified',md5=md5.hexdigest(),sha256=sha256.hexdigest());atomic_json(receipt,rec)
        phase.update(status='verified',bytes=expected['bytes'],md5=rec['md5'],sha256=rec['sha256'],attempts_used=1);runner.save()
    except BaseException as exc:
        rec.update(status='failed',error_type=type(exc).__name__);atomic_json(receipt,rec);phase.update(status='failed',error_type=type(exc).__name__);runner.save();raise


def worker(job):
    runner=Runner(job)
    try:
        completed=[];outcome='complete'
        for step in runner.manifest['sealed_workflow']['steps']:
            name=step['name'];kind=step['kind'];caps=runner.phase_policy(name,{'http':'transfer','local_read':'transfer','stream_compute':'compact'}.get(kind,kind));_,hard=resource.getrlimit(resource.RLIMIT_AS);resource.setrlimit(resource.RLIMIT_AS,(caps['address_space_bytes'],hard))
            if kind=='process':cached.run_preflight(runner,name)
            elif kind=='local_read':adopt_read(runner)
            elif kind=='http':transfer_read(runner,step)
            elif kind=='paired_fastq':runner.paired_fastq(name)
            else:real.run_stream(runner,name)
            completed.append(name)
            if runner.state['phases'][name].get('coverage',{}).get('adequate') is False:outcome='coverage_insufficient';break
        atomic_json(runner.root/'workflow-inner.json',{'status':outcome,'completed_steps':completed,'ledger_sha256':sha(runner.root/'ledger.json'),'technical_real_execution':True,'raw_execution_ready':False})
    finally:runner.close()


def monitor(job,start):
    root=Path(job['root']);m=job['manifest'];l=job['limits'];clocks,memory=real.local_monitor(root,m,l,start);last=[float('-inf')]
    def guard():
        clocks();path=root/'ledger.json'
        if path.exists():
            state=read(path)
            if state.get('prior_transfer_elapsed_seconds')!=m['recovered_read']['prior_transfer_elapsed_seconds'] or state.get('prior_deadline_epoch')!=m['recovered_read']['prior_deadline_epoch'] or not CHARGED<=state['transfer_bytes_consumed']<=l['transfer_bytes']:raise RuntimeError('External lineage accounting changed')
            tick=time.monotonic()
            if tick-last[0]>=.1:combined_disk_guard(root,state,m,l);last[0]=tick
    return guard,memory


def accept_outer(job,rec):
    check_outer(rec);root=Path(job['root']);state=read(root/'ledger.json');inner=read(root/'workflow-inner.json');steps=[s['name'] for s in job['manifest']['sealed_workflow']['steps']];done=inner.get('completed_steps',[])
    if read(root/'workflow-job.json')!=job or read(root/'workflow-receipts/run.json')!=rec or inner.get('ledger_sha256')!=sha(root/'ledger.json') or inner.get('status') not in ('complete','coverage_insufficient') or not done or done!=steps[:len(done)] or set(state['phases'])!=set(done) or any(p.get('status')!='verified' for p in state['phases'].values()):raise ValueError('Incomplete pilot result')
    if inner['status']=='complete' and done!=steps:raise ValueError('Missing pilot steps')
    if inner['status']=='coverage_insufficient' and state['phases'][done[-1]].get('coverage',{}).get('adequate') is not False:raise ValueError('Insufficient coverage evidence missing')
    b=job['manifest']['recovered_read'];a=read(root/'operator-acceptance.json')
    if a.get('plan_sha256')!=sha(root/'workflow-job.json') or a.get('accepted_new_window_and_disk') is not True or state.get('limits')!=job['limits'] or state.get('fingerprint')!=digest({'manifest':job['manifest'],'limits':job['limits']}) or state.get('prior_transfer_elapsed_seconds')!=b['prior_transfer_elapsed_seconds'] or state.get('prior_deadline_epoch')!=b['prior_deadline_epoch'] or not CHARGED<=state['transfer_bytes_consumed']<=job['limits']['transfer_bytes']:raise ValueError('Pilot final accounting/acceptance differs')
    local=state['phases'].get('CTRL_R1',{})
    if local.get('local_recovered_source')!=b or local.get('bytes')!=b['bytes'] or local.get('sha256')!=b['sha256'] or local.get('md5')!=b['md5'] or local.get('new_body_bytes')!=0:raise ValueError('Missing verified local read')
    seal={'status':'sealed_recovered_read_pilot','technical_status':inner['status'],'sha256':{n:sha(root/n) for n in FILES},'cumulative_body_bytes':state['transfer_bytes_consumed'],'remaining_body_budget_bytes':job['limits']['transfer_bytes']-state['transfer_bytes_consumed'],'raw_execution_ready':False};atomic_json(root/'workflow-seal.json',seal);return seal


def execute(path,accepted,accept_window=False):
    if not accept_window:raise ValueError('Explicit NEW window and27GiB disk acceptance required')
    if not re.fullmatch('[0-9a-f]{64}',accepted or '') or sha(path)!=accepted:raise ValueError('Exact plan SHA required')
    job=read(path);root=validate_job(job);real.check_host(root,job['limits']);root.mkdir(exist_ok=False)
    with (root/'workflow-job.json').open('xb') as f:f.write(Path(path).read_bytes());f.flush();os.fsync(f.fileno())
    atomic_json(root/'operator-acceptance.json',{'plan_sha256':accepted,'accepted_new_window_and_disk':True,'accepted_epoch':time.time()});clocks,memory=monitor(job,time.monotonic());l=job['limits'];caps=l['process_caps']
    rec=supervise('run',[sys.executable,str(Path(__file__).resolve()),'--worker',str(root/'workflow-job.json')],root/'workflow-receipts',timeout=l['wall_seconds'],rss_limit=caps['rss_bytes'],address_space=caps['address_space_bytes'],checkpoint=clocks,group_checkpoint=memory);return accept_outer(job,rec)


def worker_file(path):
    job=read(path);root=validate_job(job)
    if Path(path).resolve()!=root/'workflow-job.json':raise ValueError('Fixed worker path')
    a=read(root/'operator-acceptance.json')
    if a.get('plan_sha256')!=sha(path) or a.get('accepted_new_window_and_disk') is not True:raise ValueError('Missing worker acceptance')
    receipt=root/'workflow-receipts/run.json';outer=read(receipt);until=time.monotonic()+2
    while outer.get('status')=='started' and 'procfs_group' not in outer and time.monotonic()<until:time.sleep(.01);outer=read(receipt)
    if outer.get('status')!='started' or outer.get('procfs_group')!=proc_info(int(os.readlink('/proc/self')))['group']:raise ValueError('Active parent supervisor required')
    worker(job)


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--prepare',type=Path);g.add_argument('--execute',type=Path);g.add_argument('--worker',type=Path,help=argparse.SUPPRESS);p.add_argument('--recovery',type=Path);p.add_argument('--accept-plan-sha256');p.add_argument('--accept-new-window-and-disk',action='store_true');a=p.parse_args()
    if a.prepare:
        if not a.recovery:p.error('--recovery required')
        job=prepare(a.recovery)
        with a.prepare.open('x') as f:json.dump(job,f,indent=2);f.write('\n')
        b=job['manifest']['recovered_read'];needed=sum(s['expected']['bytes'] for s in job['manifest']['sealed_workflow']['steps'] if s['kind']=='http')
        print(json.dumps({'prepared_file':str(a.prepare),'sha256':sha(a.prepare),'execution_enabled':False,'root':job['root'],'planned_new_body_bytes':needed,'prior_charged_body_bytes':b['cumulative_body_bytes'],'minimum_cumulative_if_both_libraries_downloaded':b['cumulative_body_bytes']+needed,'new_index_or_CTRL_R1_body_bytes':0,'new_wall_seconds':7200,'new_transfer_seconds_including_local_copy':1800,'proposed_disk_gib':27,'scope':SCOPE,'raw_execution_ready':False},indent=2))
    elif a.execute:print(json.dumps(execute(a.execute,a.accept_plan_sha256,a.accept_new_window_and_disk),indent=2))
    else:worker_file(a.worker)


if __name__=='__main__':main()
