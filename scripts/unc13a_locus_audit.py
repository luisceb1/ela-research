"""Read-only reuse of sealed control prefixes; exploratory local UNC13A audit.

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
import unc13a_locus_pipeline as pipeline
import unc13a_reference_contract as reference
from paired_fastq_integrity import file_digest
from process_supervisor_v2 import atomic_json, supervise, proc_info
from workflow_seal import read, sha, check_outer

GiB=1024**3
PREFIX_PAIRS=1_000_000
SCOPE='exploratory local UNC13A inventory; same sealed 1M CTRL pairs; no HTTP, TDP or gate promotion'
PHASES={'verify':300,'stage':300,'producer':900,'reduce':300,'finalize':180}
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
    result['audit_files']={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),Path(pipeline.__file__),Path(reference.__file__)]+REFERENCE_FILES}
    return result


def source_binding(root):
    root=Path(root)
    if not root.is_absolute() or root!=root.resolve():raise ValueError('Canonical control root required')
    for name,expected in PINNED.items():
        small(root/name)
        if sha(root/name)!=expected:raise ValueError('Original sealed control metadata changed')
    seal=small(root/'workflow-seal.json');old=small(root/'workflow-job.json');ledger=small(root/'ledger.json')
    check_outer(small(root/'workflow-receipts/run.json'))
    if seal['status']!='sealed_offline_control_pilot' or seal['sha256']!=PINNED or seal['technical_status']!='coverage_insufficient':raise ValueError('Original control seal required')
    if old['identity']!=base.identity() or old['scope']!=base.SCOPE or old['execution_enabled'] is not False:raise ValueError('Original control identity changed')
    b=base.read_binding(old['manifest']['offline_control']['root'])
    if b!=old['manifest']['offline_control'] or base.output_root(b)!=root:raise ValueError('Control lineage mismatch')
    pairdir=root/'paired-fastq/CTRL_prefix';receipt=small(pairdir/'receipt.json');pair=small(pairdir/'result.json')
    if sha(pairdir/'receipt.json')!=ledger['phases']['CTRL_prefix']['receipt_sha256'] or receipt['result_sha256']!=sha(pairdir/'result.json') or receipt['binding']!=ledger['phases']['CTRL_prefix']['binding']:raise ValueError('Pair metadata changed')
    if pair['status']!='verified' or not pair['source_gzip_eof_crc_validated'] or pair['prefix_pairs_written']!=PREFIX_PAIRS:raise ValueError('Complete fixed prefix required')
    targets=old['manifest']['real_compute']['CTRL_compute']['targets']
    expected=[[r['chrom'] if 'chrom' in r else 'chr19',r['start0'],r['end0'],'-'] for r in geometry()['accepted']]
    if targets!=expected:raise ValueError('Original target/reference coordinate mismatch')
    compute=root/'compact/CTRL_compute';rec=small(compute/'receipt.json');result=small(compute/'result.json')
    if sha(compute/'receipt.json')!=ledger['phases']['CTRL_compute']['receipt_sha256'] or rec['result_sha256']!=sha(compute/'result.json') or result['status']!='verified' or result['producer_exit_code']!=0:raise ValueError('Original compute result changed')
    prefixes=[]
    for i,expected in enumerate(pair['prefixes'],1):
        p=pairdir/f'prefix-R{i}.fastq.gz'
        if p.is_symlink() or p.stat().st_size!=expected['bytes']:raise ValueError('Regular prefix missing/size changed')
        prefixes.append({'path':str(p),**expected})
    if len(prefixes)!=2:raise ValueError('Two prefixes required')
    return {'root':str(root),'metadata_sha256':{**PINNED,'workflow-seal.json':sha(root/'workflow-seal.json'),'paired-fastq/CTRL_prefix/receipt.json':sha(pairdir/'receipt.json'),'paired-fastq/CTRL_prefix/result.json':sha(pairdir/'result.json'),'compact/CTRL_compute/receipt.json':sha(compute/'receipt.json'),'compact/CTRL_compute/result.json':sha(compute/'result.json')},
            'read_binding':b,'prefixes':prefixes,'spec':old['manifest']['real_compute']['CTRL_compute'],'original_result_sha256':sha(compute/'result.json')}


def output_root(binding):return Path(binding['root']+'-locus-audit-01')


def make_job(binding):
    _,limits=base.make_manifest(binding['read_binding']);limits=copy.deepcopy(limits);limits['wall_seconds']=2100
    return {'schema':'unc13a-local-locus-audit-v1','execution_enabled':False,'root':str(output_root(binding)),
            'source':binding,'limits':limits,'phase_seconds':PHASES,'clock_policy':base.clock.clock_policy(),
            'identity':identity(),'geometry':geometry(),'scope':SCOPE,'new_transfer_bytes':0,'cumulative_body_bytes':base.CHARGED}


def validate(job):
    if source_binding(job['source']['root'])!=job['source'] or make_job(job['source'])!=job:raise ValueError('Audit sources/code/clock/scope changed')
    return Path(job['root'])


def disk_guard(job):
    roots=job['source']['read_binding']['lineage_roots']+[job['source']['root']];root=Path(job['root'])
    if len(set(roots+[str(root)]))!=13:raise ValueError('Thirteen distinct trees required')
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
    def __init__(self,job,start=None):self.job=job;self.start=base.clock.tick() if start is None else start;self.last=self.start;self.sample=-1e20
    def __call__(self):
        now=base.clock.tick()
        if now<self.last or now-self.start>=2100 or base.clock.clock_policy()!=self.job['clock_policy']:raise RuntimeError('Audit elapsed/boot cap')
        self.last=now;p=Path(self.job['root'])/'audit-state.json'
        if p.exists():
            s=small(p);now=base.clock.tick()
            if s['clock_policy']!=self.job['clock_policy'] or s['phase'] not in PHASES or not self.start<=s['started_tick']<=s['phase_started_tick']<=now or now>=s['phase_deadline_tick']:raise RuntimeError('Audit phase elapsed cap')
            if s['phase_deadline_tick']!=min(s['phase_started_tick']+PHASES[s['phase']],s['started_tick']+2100):raise RuntimeError('Audit phase policy changed')
            if s['cumulative_body_bytes']!=base.CHARGED or s['new_transfer_bytes']!=0:raise RuntimeError('Audit body counter changed')
        if now-self.sample>=.25:disk_guard(self.job);self.sample=now
        log=Path(self.job['root'])/'producer.log'
        if log.exists() and log.stat().st_size>1024**2:raise RuntimeError('Producer log cap')
    def phase(self,name):
        self();now=base.clock.tick();p=Path(self.job['root'])/'audit-state.json'
        previous=small(p) if p.exists() else None
        names=list(PHASES)
        if (previous is None and name!='verify') or (previous is not None and names.index(name)!=names.index(previous['phase'])+1):raise ValueError('Fixed audit phase order')
        completed=[] if previous is None else previous['completed_phases']+[{'phase':previous['phase'],'started_tick':previous['phase_started_tick'],'finished_tick':now,'deadline_tick':previous['phase_deadline_tick']}]
        s={'completed_phases':completed,'clock_policy':self.job['clock_policy'],'started_tick':self.start,'phase':name,'phase_started_tick':now,'phase_deadline_tick':min(now+PHASES[name],self.start+2100),'new_transfer_bytes':0,'cumulative_body_bytes':base.CHARGED}
        atomic_json(p,s);self()


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
    root=validate(job);guard=Guard(job);guard.phase('verify');b=job['source'];verify_prefixes(job,guard)
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
    summary={'status':'sealed_exploratory_locus_audit','root':str(root),'original_control_gate':'coverage_insufficient','gate_promoted':False,'geometry':job['geometry'],'regional_audit':regional,'same_prefix_target_and_qc_replay_identical':True,'new_transfer_bytes':0,'cumulative_body_bytes':base.CHARGED,'raw_execution_ready':False,
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
        print(json.dumps({'prepared_file':str(a.prepare),'sha256':sha(a.prepare),'execution_enabled':False,'root':j['root'],'total_seconds':2100,'prefix_pairs':PREFIX_PAIRS,'new_transfer_bytes':0,'cumulative_body_bytes':base.CHARGED,'clock':'CLOCK_BOOTTIME','gate_promoted':False,'scope':SCOPE},indent=2))
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
