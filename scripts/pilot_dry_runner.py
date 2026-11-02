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

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

class DryRunner:
    def __init__(self,root,manifest,limits,clock=time.time):
        self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True);self.clock=clock
        self.lock=(self.root/'runner.lock').open('a')
        try:
            fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            self.path=self.root/'ledger.json';fingerprint=digest({'manifest':manifest,'limits':limits})
            if self.path.exists():
                self.state=json.loads(self.path.read_text())
                if self.state['fingerprint']!=fingerprint:raise ValueError('Manifest or limits changed')
                for name,phase in self.state['phases'].items():
                    if phase['status']!='verified':raise ValueError('Incomplete/failed phase requires explicit reconciliation: '+name)
                    if phase['kind']=='transfer':
                        data=(self.root/name).read_bytes()
                        if len(data)!=phase['bytes'] or hashlib.sha256(data).hexdigest()!=phase['sha256']:raise ValueError('Verified artifact changed')
                    else:
                        receipt=self.root/'process-receipts'/phase['receipt']
                        if hashlib.sha256(receipt.read_bytes()).hexdigest()!=phase['receipt_sha256']:raise ValueError('Process receipt changed')
            else:
                self.state={'fingerprint':fingerprint,'limits':limits,'deadline_epoch':clock()+limits['wall_seconds'],'transfer_bytes_consumed':0,'phases':{},'mode':'synthetic-only','raw_pilot_ready':False}
                self.save()
            self.guard()
        except BaseException:
            self.lock.close();raise
    def close(self):self.lock.close()
    def save(self):atomic_json(self.path,self.state)
    def guard(self):
        l=self.state['limits']
        if self.clock()>=self.state['deadline_epoch']:raise RuntimeError('Global deadline')
        if self.state['transfer_bytes_consumed']>l['transfer_bytes']:raise RuntimeError('Global transfer budget')
        if sum(p.stat().st_size for p in self.root.rglob('*') if p.is_file())>l['disk_bytes']:raise RuntimeError('Global disk budget')
        if shutil.disk_usage(self.root).free<l['reserve_bytes']:raise RuntimeError('Free disk reserve')
    def begin(self,name,kind,signature):
        if not re.fullmatch('[A-Za-z0-9_-]+',name):raise ValueError('Invalid phase name')
        self.guard()
        if name in self.state['phases']:
            phase=self.state['phases'][name]
            if phase['status']=='verified' and phase['kind']==kind and phase['signature']==signature:return False
            raise RuntimeError('Phase already attempted')
        self.state['phases'][name]={'kind':kind,'status':'started','signature':signature};self.save();return True
    def transfer(self,name,chunks,expected):
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
            if size!=expected['bytes'] or md5.hexdigest()!=expected['md5'] or sha.hexdigest()!=expected['sha256']:raise ValueError('Transfer integrity mismatch')
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
    def plan_process(self,argv,process_limits=None,*,production=True):
        self.guard()
        if production and process_limits is None:raise ValueError('Production requires explicit process limits')
        policy=self.process_limits(process_limits)
        return {'argv':argv,'process_limits':policy,'production_configuration':production,
                'effective_wall_seconds':min(policy['wall_seconds'],self.state['deadline_epoch']-self.clock()),
                'execution_enabled':False,'raw_execution_ready':False}
    def process(self,name,argv,*,process_limits=None,production=False):
        if production:raise ValueError('Production execution disabled in DryRunner; plan only')
        policy=self.process_limits(process_limits)
        signature=digest(argv) if process_limits is None and not production else digest({'argv':argv,'process_limits':policy,'production':production})
        if not self.begin(name,'process',signature):return self.state['phases'][name]
        phase=self.state['phases'][name]
        try:
            remaining=self.state['deadline_epoch']-self.clock()
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
