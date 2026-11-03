"""Read-only reuse of sealed control prefixes; exploratory local UNC13A audit.

Revised guard and phase allocation after the first reduction timeout.
No HTTP, TDP, target change or coverage-gate promotion. Exact-plan acceptance,
exclusive root, CLOCK_BOOTTIME, supervised native producer, bounded inventory.
"""
import argparse
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

import offline_control_pilot as base
import unc13a_locus_audit as previous
import unc13a_locus_pipeline as pipeline
import unc13a_reference_contract as reference
from paired_fastq_integrity import file_digest
from process_supervisor_v2 import atomic_json, supervise, proc_info
from workflow_seal import read, sha, check_outer

GiB=1024**3
PREFIX_PAIRS=1_000_000
SCOPE='exploratory local UNC13A inventory; same sealed 1M CTRL pairs; no HTTP, TDP or gate promotion'
PHASES={'verify':180,'stage':120,'producer':900,'reduce':720,'finalize':60}
PINNED={'workflow-job.json':'33caa216410ef61b199b68941d755ac6f85c4fb81ae19bd5550e650b5244d5ed',
'operator-acceptance.json':'e9691982877beec59d86f022d567ab364d294414770cc92c64d040b584874ea3',
'ledger.json':'2b5fb713ea427133fd141616f8a02f92e57021214e8cfe5202e633f593d57605',
'workflow-inner.json':'a2bddfd745794346192a4fa9e803c21c23513eea5d37739c829ce0ffef69301d',
'workflow-receipts/run.json':'38350516bd7ac978b2cd9a39a1c917a84896e33bc0d47b5273a1832f23bc83f0'}
ROOT=Path(__file__).resolve().parents[1]
REFERENCE_FILES=[reference.ROOT/'sources/sequence.json',reference.ROOT/'sources/annotation.json',reference.ROOT/'retrievals.json',reference.ROOT/'contract.json']


def small(path):
    path=Path(path)
    if path.is_symlink() or path.stat().st_size>1024**2:raise ValueError('Regular bounded metadata required')
    return read(path)


def geometry():
    sources=reference.ROOT/'sources'
    for item in small(reference.ROOT/'retrievals.json'):
        if not item['saved'] or sha(sources/item['name'])!=item['sha256']:raise ValueError('Reference source changed')
    models,accepted=reference.evaluate(small(sources/'sequence.json'),small(sources/'annotation.json'))
    contract=small(reference.ROOT/'contract.json')
    if accepted!=contract['events']:raise ValueError('Coordinate contract changed')
    return {'models':models,'accepted':accepted,'source_limit':'cached UCSC sequence/annotation; not an independent provider','region':list(pipeline.REGION)}


def identity():
    result=base.identity()
    result['audit_files']={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),Path(previous.__file__),Path(pipeline.__file__),Path(reference.__file__)]+REFERENCE_FILES}
    return result


def failed_binding(control):
    root=previous.output_root(control)
    if (root/'audit-seal.json').exists() or (root/'audit-inner.json').exists():raise ValueError('Expected incomplete failed audit, not adopted results')
    job=small(root/'audit-plan.json');state=small(root/'audit-state.json');rec=small(root/'supervision/run.json')
    acceptance=small(root/'operator-acceptance.json')
    expected=previous.make_job(control);expected['clock_policy']=job['clock_policy']
    if job!=expected or acceptance.get('prepared_sha256')!=sha(root/'audit-plan.json') or acceptance.get('accepted_local_audit_window') is not True:raise ValueError('Failed audit fixed descriptor/acceptance changed')
    if (rec.get('status')!='finished' or rec.get('exit_code')!=-9 or rec.get('live_group_members_after_cleanup')!=[] or
        rec.get('supervisor_error')!='RuntimeError: Audit phase elapsed cap' or rec.get('violation') is not None):raise ValueError('Expected cleaned-up phase timeout required')
    if state.get('clock_policy')!=job['clock_policy'] or state.get('phase')!='reduce' or state.get('new_transfer_bytes')!=0 or state.get('cumulative_body_bytes')!=base.CHARGED:raise ValueError('Failed reduction accounting/clock changed')
    completed=state['completed_phases']
    if [p['phase'] for p in completed]!=['verify','stage','producer']:raise ValueError('Failed audit prior phases incomplete')
    last=state['started_tick']
    for phase in completed:
        if not last<=phase['started_tick']<=phase['finished_tick']<phase['deadline_tick'] or phase['deadline_tick']!=min(phase['started_tick']+previous.PHASES[phase['phase']],state['started_tick']+2100):raise ValueError('Failed audit completed phase timing changed')
        last=phase['finished_tick']
    if state['phase_started_tick']!=last or state['phase_deadline_tick']!=min(last+300,state['started_tick']+2100):raise ValueError('Expected original 300-second reduction cap')
    names=('audit-plan.json','audit-state.json','operator-acceptance.json','supervision/run.json','supervision/run.log','producer.log')
    for name in names:
        p=root/name
        if p.is_symlink() or p.stat().st_size>1024**2:raise ValueError('Bounded regular failed-attempt metadata required')
    return {'root':str(root),'metadata_sha256':{n:sha(root/n) for n in names},
            'disposition':'preserved, no compact-run or plaintext adoption','prior_elapsed_seconds':rec['elapsed_seconds'],
            'prior_phase_seconds':previous.PHASES,'last_phase':'reduce'}


def source_binding(root):
    control=previous.source_binding(root)
    return {**control,'failed_audit':failed_binding(control)}


def output_root(binding):return Path(binding['failed_audit']['root']+'-guard-02')


def make_job(binding):
    _,limits=base.make_manifest(binding['read_binding']);limits=copy.deepcopy(limits);limits['wall_seconds']=2100
    return {'schema':'unc13a-local-locus-audit-guard-v2','execution_enabled':False,'root':str(output_root(binding)),
            'source':binding,'limits':limits,'phase_seconds':PHASES,'clock_policy':base.clock.clock_policy(),
            'identity':identity(),'geometry':geometry(),'scope':SCOPE,'new_transfer_bytes':0,'cumulative_body_bytes':base.CHARGED}


def validate(job):
    if source_binding(job['source']['root'])!=job['source'] or make_job(job['source'])!=job:raise ValueError('Audit sources/code/clock/scope changed')
    return Path(job['root'])


def disk_guard(job):
    roots=job['source']['read_binding']['lineage_roots']+[job['source']['root'],job['source']['failed_audit']['root']];root=Path(job['root'])
    if len(set(roots+[str(root)]))!=14:raise ValueError('Fourteen distinct trees required')
    history=base.history_bytes({'lineage_roots':roots})
    if history>18*GiB:raise RuntimeError('Historical artifact partition cap')
    usage={'plain':0,'compact':0,'receipts':0}
    for p in base.execution.iter_files(root):
        try:
            if p.is_symlink():raise ValueError('Audit symlink')
            if not p.is_file():continue
            relative=p.relative_to(root);bucket='plain' if relative.parts[0]=='alignment-inputs' else 'compact' if relative.parts[0]=='compact' else 'receipts'
            usage[bucket]+=p.stat().st_size
        except FileNotFoundError:pass  # a compact run may be reclaimed between samples
    if usage['plain']>2*GiB or usage['compact']>6*GiB or usage['receipts']>GiB//4 or history+sum(usage.values())>job['limits']['disk_bytes']:raise RuntimeError('Audit disk partition cap')
    if base.real.shutil.disk_usage(root if root.exists() else root.parent).free<job['limits']['reserve_bytes']:raise RuntimeError('Audit disk reserve')


def prepare(root):
    job=make_job(source_binding(Path(root).expanduser().resolve()))
    if Path(job['root']).exists():raise ValueError('Never reuse attempted audit root')
    base.real.check_host(job['root'],job['limits']);disk_guard(job)
    return job


class Guard:
    """Worker checks its own in-memory phase; parent independently reads the file.

    Deadlines are checked on every checkpoint. Boot, disk and producer-log size
    are sampled every .25s. No per-row metadata read in the worker hot loop.
    """
    def __init__(self,job,start=None,local_state=False):
        self.job=job;self.start=base.clock.tick() if start is None else start
        self.last=self.start;self.sample=-1e20;self.local_state=local_state;self.current=None
    def reject(self,reason,now,state=None):
        detail={'reason':reason,'tick':now,'run_elapsed_seconds':now-self.start}
        if state is not None:detail.update(phase=state.get('phase'),phase_elapsed_seconds=now-state.get('phase_started_tick',now),deadline_tick=state.get('phase_deadline_tick'))
        raise RuntimeError('Audit guard: '+json.dumps(detail,sort_keys=True))
    def __call__(self):
        now=base.clock.tick()
        if now<self.last:self.reject('elapsed clock moved backwards',now)
        if now-self.start>=2100:self.reject('total deadline',now)
        self.last=now
        p=Path(self.job['root'])/'audit-state.json'
        state=self.current if self.local_state else small(p) if p.exists() else None
        now=base.clock.tick()
        if state is not None:
            if state['clock_policy']!=self.job['clock_policy']:self.reject('phase clock identity',now,state)
            if state['phase'] not in PHASES:self.reject('unknown phase',now,state)
            if not self.start<=state['started_tick']<=state['phase_started_tick']<=now:self.reject('phase time ordering',now,state)
            if state['phase_deadline_tick']!=min(state['phase_started_tick']+PHASES[state['phase']],state['started_tick']+2100):self.reject('phase deadline policy',now,state)
            if now>=state['phase_deadline_tick']:self.reject('phase deadline',now,state)
            if state['cumulative_body_bytes']!=base.CHARGED or state['new_transfer_bytes']!=0:self.reject('body counter changed',now,state)
        if now-self.sample>=.25:
            if base.clock.clock_policy()!=self.job['clock_policy']:self.reject('boot identity changed',now,state)
            disk_guard(self.job);self.sample=now
            log=Path(self.job['root'])/'producer.log'
            if log.exists() and log.stat().st_size>1024**2:self.reject('producer log cap',now,state)
    def phase(self,name):
        self();now=base.clock.tick();p=Path(self.job['root'])/'audit-state.json'
        prior=self.current if self.local_state else small(p) if p.exists() else None
        names=list(PHASES)
        if (prior is None and name!='verify') or (prior is not None and names.index(name)!=names.index(prior['phase'])+1):raise ValueError('Fixed audit phase order')
        completed=[] if prior is None else prior['completed_phases']+[{'phase':prior['phase'],'started_tick':prior['phase_started_tick'],'finished_tick':now,'deadline_tick':prior['phase_deadline_tick']}]
        state={'completed_phases':completed,'clock_policy':self.job['clock_policy'],'started_tick':self.start,'phase':name,'phase_started_tick':now,'phase_deadline_tick':min(now+PHASES[name],self.start+2100),'new_transfer_bytes':0,'cumulative_body_bytes':base.CHARGED}
        atomic_json(p,state);self.current=state;self()


def verify_prefixes(job,guard):
    for p in job['source']['prefixes']:
        if Path(p['path']).is_symlink() or file_digest(p['path'],guard)!={k:p[k] for k in ('bytes','sha256')}:raise ValueError('Sealed prefix changed')


def argv(job):
    b=job['source'];a=b['read_binding']['index']['aligner'];args=base.real.alignment_argv(Path(job['root']),b['spec'],a)
    args[args.index('-x')+1]=b['read_binding']['index']['index_prefix'];return args


def stage(job,guard):
    folder=Path(job['root'])/'alignment-inputs/CTRL_compute';folder.mkdir(parents=True)
    total=0;files=[]
    for i,item in enumerate(job['source']['prefixes'],1):
        p=folder/f'R{i}.fastq';h=hashlib.sha256();size=0
        with gzip.open(item['path'],'rb') as inp,p.open('xb') as out:
            while True:
                guard();chunk=inp.read(65536)
                if not chunk:break
                total+=len(chunk);size+=len(chunk)
                if total>min(2*GiB,job['source']['spec']['max_plaintext_bytes']):raise ValueError('Plaintext cap')
                out.write(chunk);h.update(chunk)
            out.flush();os.fsync(out.fileno())
        files.append({'path':str(p),'bytes':size,'sha256':h.hexdigest()})
    return files


def worker(job):
    root=validate(job);guard=Guard(job,local_state=True);guard.phase('verify');b=job['source'];verify_prefixes(job,guard)
    base.cached.verify_index_data(b['read_binding']['index'],guard);base.real.validate_aligner(b['read_binding']['index']['aligner']);guard()
    guard.phase('stage');plain=stage(job,guard);guard.phase('producer');process=None
    try:
        with (root/'producer.log').open('xb') as log:
            process=subprocess.Popen(argv(job),stdout=subprocess.PIPE,stderr=log)
            def finish():
                guard();code=process.wait(timeout=max(.01,small(root/'audit-state.json')['phase_deadline_tick']-base.clock.tick()))
                if code==0:guard.phase('reduce')
                return code
            with process.stdout as stream:result=pipeline.run(stream,root/'compact',b['spec']['library'],b['spec']['targets'],b['spec']['limits'],finish,checkpoint=guard)
    finally:
        if process is not None:
            if process.poll() is None:process.kill()
            process.wait()
    guard.phase('finalize')
    original=small(Path(b['root'])/'compact/CTRL_compute/result.json')
    if result['routes']!=original['routes'] or result['records']!=original['records']:raise ValueError('Same-prefix target/QC replay differs from sealed pilot')
    for item in plain:
        if file_digest(item['path'],guard)!={k:item[k] for k in ('bytes','sha256')}:raise ValueError('Plain input changed')
        Path(item['path']).unlink()
    (root/'alignment-inputs/CTRL_compute').rmdir()
    verify_prefixes(job,guard)
    if source_binding(b['root'])!=b:raise ValueError('Source metadata changed during audit')
    guard();atomic_json(root/'audit-inner.json',{'status':'complete_exploratory','result_sha256':sha(root/'compact/result.json'),'producer_log_sha256':sha(root/'producer.log'),'job_sha256':sha(root/'audit-plan.json'),'argv':argv(job),'target_and_qc_replay_identical':True,'finished_tick':base.clock.tick(),'new_transfer_bytes':0,'cumulative_body_bytes':base.CHARGED})


def seal(job,record):
    check_outer(record);root=validate(job);inner=small(root/'audit-inner.json');s=small(root/'audit-state.json');result=small(root/'compact/result.json')
    a=small(root/'operator-acceptance.json')
    if small(root/'supervision/run.json')!=record or small(root/'audit-plan.json')!=job or a.get('prepared_sha256')!=sha(root/'audit-plan.json') or a.get('accepted_local_audit_window') is not True:raise ValueError('Audit outer acceptance changed')
    if inner.get('status')!='complete_exploratory' or inner['job_sha256']!=sha(root/'audit-plan.json') or inner['argv']!=argv(job) or inner['result_sha256']!=sha(root/'compact/result.json') or inner['producer_log_sha256']!=sha(root/'producer.log') or not inner['target_and_qc_replay_identical']:raise ValueError('Audit inner result changed')
    if any(x.get('new_transfer_bytes')!=0 or x.get('cumulative_body_bytes')!=base.CHARGED for x in (s,inner)):raise ValueError('Audit final body counter changed')
    if s['phase_deadline_tick']!=min(s['phase_started_tick']+PHASES['finalize'],s['started_tick']+2100):raise ValueError('Audit final phase policy changed')
    if s['phase']!='finalize' or not s['started_tick']<=inner['finished_tick']<min(s['phase_deadline_tick'],s['started_tick']+2100) or s['clock_policy']!=job['clock_policy']:raise ValueError('Audit final elapsed receipt')
    if [p['phase'] for p in s['completed_phases']]!=list(PHASES)[:-1] or any(not s['started_tick']<=p['started_tick']<=p['finished_tick']<p['deadline_tick'] or p['deadline_tick']!=min(p['started_tick']+PHASES[p['phase']],s['started_tick']+2100) for p in s['completed_phases']):raise ValueError('Audit phase history incomplete')
    original=small(Path(job['source']['root'])/'compact/CTRL_compute/result.json')
    if result['status']!='verified' or result['producer_exit_code']!=0 or result['routes']!=original['routes'] or result['records']!=original['records'] or (root/'alignment-inputs/CTRL_compute').exists():raise ValueError('Audit incomplete/replay changed')
    regional=result['regional_audit']
    if regional['window']!=list(pipeline.REGION) or regional['routes']['text15']!=regional['routes']['hts15'] or regional['routes']['text8']!=regional['routes']['hts8']:raise ValueError('Regional audit inconsistent')
    summary={'status':'sealed_exploratory_locus_audit','root':str(root),'original_control_gate':'coverage_insufficient','gate_promoted':False,'prior_failed_attempt':job['source']['failed_audit'],'geometry':job['geometry'],'regional_audit':regional,'same_prefix_target_and_qc_replay_identical':True,'new_transfer_bytes':0,'cumulative_body_bytes':base.CHARGED,'raw_execution_ready':False,
        'sha256':{n:sha(root/n) for n in ('audit-plan.json','operator-acceptance.json','audit-state.json','audit-inner.json','compact/result.json','producer.log','supervision/run.json')}}
    atomic_json(root/'audit-seal.json',summary);return summary


def execute(path,accepted,accept=False):
    if not accept or not re.fullmatch('[a-f0-9]{64}',accepted or '') or sha(path)!=accepted:raise ValueError('Exact SHA and new local audit window acceptance required')
    job=small(path);root=validate(job);base.real.check_host(root,job['limits']);disk_guard(job);root.mkdir(exist_ok=False)
    with (root/'audit-plan.json').open('xb') as f:f.write(Path(path).read_bytes());f.flush();os.fsync(f.fileno())
    atomic_json(root/'operator-acceptance.json',{'prepared_sha256':accepted,'accepted_local_audit_window':True})
    guard=Guard(job);caps=job['limits']['process_caps']
    record=supervise('run',[sys.executable,str(Path(__file__).resolve()),'--worker',str(root/'audit-plan.json')],root/'supervision',timeout=2100,rss_limit=caps['rss_bytes'],address_space=caps['address_space_bytes'],checkpoint=guard)
    return seal(job,record)


def console_summary(sealed):
    routes=sealed['regional_audit']['routes']
    return {'status':sealed['status'],'root':sealed['root'],'full_inventory_file':str(Path(sealed['root'])/'audit-seal.json'),
            'original_control_gate':sealed['original_control_gate'],'gate_promoted':False,
            'coordinate_contract':sealed['geometry']['accepted'],'window':sealed['regional_audit']['window'],
            'same_prefix_target_and_qc_replay_identical':sealed['same_prefix_target_and_qc_replay_identical'],
            'new_transfer_bytes':sealed['new_transfer_bytes'],'cumulative_body_bytes':sealed['cumulative_body_bytes'],
            'routes':{r:{'qc':routes[r]['qc'],'distinct_junctions':len(routes[r]['junctions']),
                'top20_by_support':sorted(routes[r]['junctions'],key=lambda row:(-row['fragments'],row['event']))[:20],
                'all_target_neighbors_within_2bp':[row for row in routes[r]['junctions'] if row['near_original_targets']]} for r in ('text15','text8')},
            'console_inventory_is_summary':True,'raw_execution_ready':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--prepare',type=Path);g.add_argument('--execute',type=Path);g.add_argument('--worker',type=Path,help=argparse.SUPPRESS)
    p.add_argument('--control',type=Path);p.add_argument('--accept-plan-sha256');p.add_argument('--accept-local-audit-window',action='store_true');a=p.parse_args()
    if a.prepare:
        if not a.control:p.error('--control required')
        j=prepare(a.control)
        with a.prepare.open('x') as f:json.dump(j,f,indent=2);f.write('\n')
        print(json.dumps({'prepared_file':str(a.prepare),'sha256':sha(a.prepare),'execution_enabled':False,'root':j['root'],'total_seconds':2100,'reduction_seconds':720,'guard_policy':'in-memory-worker-independent-parent-v2','prefix_pairs':PREFIX_PAIRS,'new_transfer_bytes':0,'cumulative_body_bytes':base.CHARGED,'clock':'CLOCK_BOOTTIME','gate_promoted':False,'scope':SCOPE},indent=2))
    elif a.execute:print(json.dumps(console_summary(execute(a.execute,a.accept_plan_sha256,a.accept_local_audit_window)),indent=2))
    else:
        job=small(a.worker);root=validate(job)
        if a.worker.resolve()!=root/'audit-plan.json':raise ValueError('Fixed audit worker path')
        acceptance=small(root/'operator-acceptance.json')
        if acceptance.get('prepared_sha256')!=sha(a.worker) or acceptance.get('accepted_local_audit_window') is not True:raise ValueError('Missing audit acceptance')
        receipt=root/'supervision/run.json';outer=small(receipt);until=time.monotonic()+2
        while outer.get('status')=='started' and 'procfs_group' not in outer and time.monotonic()<until:time.sleep(.01);outer=small(receipt)
        if outer.get('status')!='started' or outer.get('procfs_group')!=proc_info(int(os.readlink('/proc/self')))['group']:raise ValueError('Active audit supervisor required')
        sys.addaudithook(base.deny_network);worker(job)


if __name__=='__main__':main()
