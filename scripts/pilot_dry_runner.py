"""Persistent pilot orchestration with injected synthetic transport only.

No HTTP client, real FASTQ download or aligner command is exposed by the CLI.
Incomplete/failed phases stop resumption; no automatic reset of budgets.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import time
from process_supervisor_v2 import atomic_json,supervise
from paired_fastq_integrity import file_digest
from paired_fastq_phase import run_phase,verify_phase
from artifact_checksums import validate_expected,check
from archive_ledger_phase import run_archive,verify_archive
import pilot_execution_policy as execution

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

class DryRunner:
    def __init__(self,root,manifest,limits,clock=time.time):
        self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True);self.clock=clock
        self.manifest=json.loads(json.dumps(manifest))
        self.policy=execution.validate(self.manifest.get('execution_policy'),limits)
        self.lock=(self.root/'runner.lock').open('a')
        try:
            fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            self.path=self.root/'ledger.json';fingerprint=digest({'manifest':manifest,'limits':limits})
            if self.path.exists():
                self.state=json.loads(self.path.read_text())
                if self.state['fingerprint']!=fingerprint:raise ValueError('Manifest or limits changed')
                if self.manifest.get('sealed_workflow'):
                    from workflow_seal import assert_seal
                    assert_seal(self.root,self.manifest,limits)
                if any(p.get('status')!='verified' for p in self.state['phases'].values()):raise ValueError('Incomplete/failed phase requires explicit reconciliation')
                for name,phase in self.state['phases'].items():
                    if phase['status']!='verified':raise ValueError('Incomplete/failed phase requires explicit reconciliation: '+name)
                    if phase['kind']=='transfer':
                        if file_digest(self.root/name,self.guard)!={'bytes':phase['bytes'],'sha256':phase['sha256']}:raise ValueError('Verified artifact changed')
                    elif phase['kind']=='paired_fastq':
                        verify_phase(self,name,phase)
                    elif phase['kind']=='archive':
                        verify_archive(self,name,phase)
                    elif phase['kind']=='compact':
                        if phase.get('binding',{}).get('policy')=='sealed-stream-v1':
                            from sealed_local_workflow import verify_stream
                            verify_stream(self,name,phase)
                        else:
                            from compact_ledger_phase import verify_compact
                            verify_compact(self,name,phase)
                    elif phase['kind']=='process':
                        receipt=self.root/'process-receipts'/phase['receipt']
                        if hashlib.sha256(receipt.read_bytes()).hexdigest()!=phase['receipt_sha256']:raise ValueError('Process receipt changed')
                    else:raise ValueError('Unknown phase kind')
            else:
                self.state={'fingerprint':fingerprint,'limits':limits,'deadline_epoch':clock()+limits['wall_seconds'],'transfer_bytes_consumed':0,'phases':{},'mode':'synthetic-only','raw_pilot_ready':False}
                if self.policy:self.state.update(last_epoch=clock(),transfer_elapsed_seconds=0)
                self.save()
            self.guard()
        except BaseException:
            self.lock.close();raise
    def close(self):self.lock.close()
    def save(self):
        error=None
        if self.policy:
            now=max(self.clock(),self.state.get('last_epoch',self.clock()),getattr(self,'observed_epoch',float('-inf')))
            newly_verified=[]
            for p in self.state['phases'].values():
                if p['status']!='started' and 'started_epoch' in p and 'finished_epoch' not in p:
                    p['finished_epoch']=now
                    if p['status']=='verified':newly_verified.append(p)
            self.state['last_epoch']=now;self.state['transfer_elapsed_seconds']=execution.elapsed_transfers(self.state,now)
            if newly_verified:
                try:
                    if now>=self.state['deadline_epoch']:raise RuntimeError('Global deadline before commit')
                    execution.guard_clocks(self.state,self.policy,now)
                except RuntimeError as exc:
                    error=exc
                    for p in newly_verified:p.update(status='failed',error_type='CommitClockViolation')
        atomic_json(self.path,self.state)
        if error is not None:raise error
    def guard(self):
        l=self.state['limits']
        now=self.clock()
        if self.policy:
            if now<getattr(self,'observed_epoch',self.state.get('last_epoch',now)):raise RuntimeError('Clock moved backwards within runner')
            self.observed_epoch=now
        if now>=self.state['deadline_epoch']:raise RuntimeError('Global deadline')
        if self.policy:execution.guard_clocks(self.state,self.policy,now)
        if self.state['transfer_bytes_consumed']>l['transfer_bytes']:raise RuntimeError('Global transfer budget')
        if self.policy:
            usage=execution.disk_usage(self.root,self.state)
            if sum(usage.values())>l['disk_bytes']:raise RuntimeError('Global disk budget')
            if any(usage[k]>self.policy['allocations'][k] for k in usage):raise RuntimeError('Disk partition budget')
        elif sum(p.stat().st_size for p in execution.iter_files(self.root) if p.is_file())>l['disk_bytes']:raise RuntimeError('Global disk budget')
        if shutil.disk_usage(self.root).free<l['reserve_bytes']:raise RuntimeError('Free disk reserve')
    def begin(self,name,kind,signature):
        if not re.fullmatch('[A-Za-z0-9_-]+',name):raise ValueError('Invalid phase name')
        self.guard()
        if name in self.state['phases']:
            phase=self.state['phases'][name]
            if phase['status']=='verified' and phase['kind']==kind and phase['signature']==signature:return False
            raise RuntimeError('Phase already attempted')
        phase={'kind':kind,'status':'started','signature':signature}
        if self.policy:
            caps=self.phase_policy(name,kind)
            if any(p['status']=='started' for p in self.state['phases'].values()):raise RuntimeError('Policy phases must be sequential')
            if any(p['kind']=='compact' and p['status']=='verified' and not p['coverage']['adequate'] for p in self.state['phases'].values()):raise RuntimeError('Coverage insufficient; no automatic next phase')
            now=self.clock();phase.update(started_epoch=now,deadline_epoch=now+self.remaining(name,kind))
            if kind=='compact':phase.update(substage='producer',subdeadline_epoch=min(phase['deadline_epoch'],now+caps['producer_seconds']))
        self.state['phases'][name]=phase;self.save();return True
    def phase_policy(self,name,kind):
        if not self.policy:return None
        cap=self.policy['phases'].get(name)
        if cap is None or cap['kind']!=kind:raise ValueError('Phase not declared with matching kind')
        return cap
    def remaining(self,name,kind):
        self.guard();now=self.clock();remaining=self.state['deadline_epoch']-now
        if self.policy:
            caps=self.phase_policy(name,kind);remaining=min(remaining,caps['wall_seconds'])
            phase=self.state['phases'].get(name)
            if phase and phase['status']=='started':remaining=min(remaining,phase['deadline_epoch']-now,phase.get('subdeadline_epoch',phase['deadline_epoch'])-now)
            if kind=='transfer':remaining=min(remaining,self.policy['transfer_seconds']-execution.elapsed_transfers(self.state,now))
        if remaining<=0:raise RuntimeError('No remaining phase time')
        return remaining
    def compact_reduction(self,name):
        self.guard();p=self.state['phases'][name]
        if self.policy:
            if p['kind']!='compact' or p['status']!='started' or p.get('substage')!='producer':raise ValueError('Invalid compact stage transition')
            p.update(substage='reduce',subdeadline_epoch=min(p['deadline_epoch'],self.clock()+self.phase_policy(name,'compact')['reduce_seconds']));self.save()
        return 0
    def transfer(self,name,chunks,expected):
        validate_expected(expected)
        if not self.begin(name,'transfer',digest(expected)):return self.state['phases'][name]
        phase=self.state['phases'][name];partial=self.root/(name+'.partial')
        try:
            if expected['bytes']>self.state['limits']['disk_bytes']:raise RuntimeError('Artifact exceeds disk budget')
            size=0;md5=hashlib.md5();sha=hashlib.sha256()
            with partial.open('xb') as out:
                for chunk in chunks:
                    self.guard()
                    self.state['transfer_bytes_consumed']+=len(chunk);self.save();self.guard()
                    if size+len(chunk)>expected['bytes']:raise ValueError('Unexpected transfer size')
                    out.write(chunk);out.flush();size+=len(chunk);md5.update(chunk);sha.update(chunk);self.guard()
                os.fsync(out.fileno())
            check(expected,size=size,md5=md5.hexdigest(),sha256=sha.hexdigest())
            os.replace(partial,self.root/name)
            fd=os.open(self.root,os.O_DIRECTORY)
            try:os.fsync(fd)
            finally:os.close(fd)
            self.guard();phase.update(status='verified',bytes=size,sha256=sha.hexdigest(),md5=md5.hexdigest());self.save()
        except BaseException as exc:
            phase.update(status='failed',error=f'{type(exc).__name__}: {exc}');self.save();raise
        return phase
    def process_limits(self,requested=None):
        if requested is None:
            return {'wall_seconds':5,'rss_bytes':128*1024**2,'address_space_bytes':128*1024**2}
        keys={'wall_seconds','rss_bytes','address_space_bytes'}
        if not isinstance(requested,dict) or set(requested)!=keys or any(type(v) is not int or v<=0 for v in requested.values()):
            raise ValueError('Explicit positive integer process limits required')
        caps=self.state['limits'].get('process_caps')
        if not isinstance(caps,dict) or set(caps)!=keys or any(type(v) is not int or v<=0 for v in caps.values()):
            raise ValueError('Manifest-bound process caps required')
        if any(requested[k]>caps[k] for k in keys):raise ValueError('Process limits exceed pinned caps')
        return dict(requested)
    def paired_fastq(self,name):
        return run_phase(self,name)
    def archive(self,name):
        return run_archive(self,name)
    def compact(self,name):
        from compact_ledger_phase import run_compact
        return run_compact(self,name)
    def plan_process(self,argv,process_limits=None,*,production=True):
        self.guard()
        if production and process_limits is None:raise ValueError('Production requires explicit process limits')
        policy=self.process_limits(process_limits)
        return {'argv':argv,'process_limits':policy,'production_configuration':production,
                'effective_wall_seconds':min(policy['wall_seconds'],self.state['deadline_epoch']-self.clock()),
                'execution_enabled':False,'raw_execution_ready':False}
    def process(self,name,argv,*,process_limits=None,production=False):
        if production:raise ValueError('Production execution disabled in DryRunner; plan only')
        if self.policy:
            caps=self.phase_policy(name,'process')
            if process_limits!={k:caps[k] for k in ('wall_seconds','rss_bytes','address_space_bytes')}:raise ValueError('Policy process limits must be explicit and match')
        policy=self.process_limits(process_limits)
        signature=digest(argv) if process_limits is None and not production else digest({'argv':argv,'process_limits':policy,'production':production})
        if not self.begin(name,'process',signature):return self.state['phases'][name]
        phase=self.state['phases'][name]
        try:
            remaining=self.remaining(name,'process')
            phase['process_limits']=policy;phase['production_configuration']=production;self.save()
            r=supervise(name,argv,self.root/'process-receipts',timeout=min(remaining,policy['wall_seconds']),rss_limit=policy['rss_bytes'],address_space=policy['address_space_bytes'],checkpoint=self.guard)
            if r['exit_code'] or r['violation'] or r['live_group_members_after_cleanup']:raise RuntimeError('Supervised process failed')
            receipt=self.root/'process-receipts'/(name+'.json')
            self.guard();phase.update(status='verified',receipt=name+'.json',receipt_sha256=hashlib.sha256(receipt.read_bytes()).hexdigest());self.save()
        except BaseException as exc:
            phase.update(status='failed',error=f'{type(exc).__name__}: {exc}');self.save();raise
        return phase

def simulation(root):
    data=b'synthetic-transport-only\n';manifest={'fixture':'two_mates','sha256':hashlib.sha256(data).hexdigest()}
    limits={'wall_seconds':30,'transfer_bytes':1024,'disk_bytes':2*1024**2,'reserve_bytes':0}
    expected={'bytes':len(data),'md5':hashlib.md5(data).hexdigest(),'sha256':manifest['sha256']}
    runner=DryRunner(root,manifest,limits)
    try:
        for name in ['mate1','mate2']:runner.transfer(name,[data[:10],data[10:]],expected)
        runner.process('synthetic_process',[sys.executable,'-c','print("synthetic success")'])
        return runner.state
    finally:runner.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--simulate',type=Path,required=True);args=p.parse_args()
    print(json.dumps(simulation(args.simulate),indent=2))
