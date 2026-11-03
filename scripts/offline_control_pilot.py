"""Control-only pilot from sealed local index/R1/R2. No HTTP or TDP steps.

Preparation emits a disabled fixed descriptor. Execution requires its exact SHA
and a new 3000s elapsed-clock window; historical files/budgets stay immutable.
"""
import argparse
import copy
import fcntl
import json
import math
import os
from pathlib import Path
import re
import resource
import sys
import time

import recover_ctrl_r2_clock as clock
import recovered_read_pilot as recovered
import cached_index_pilot as cached
import real_pilot_workflow as real
import paired_fastq_phase as paired
import pilot_execution_policy as execution
from paired_fastq_phase import digest
from process_supervisor_v2 import atomic_json, supervise, proc_info
from workflow_seal import read, sha, check_outer

GiB = 1024**3
CHARGED = 7322807977
PREFIX_PAIRS = 1_000_000
R2_SHA = 'b034affa4479b28154fa9217a943128c4513590f6e622690a7af7afd272ca2f6'
R2_PLAN_SHA = '36c64ad45e944461a4817b05ea86abcbf83b4367b31fefad997f7d835a021855'
CODE = tuple(sorted(set(clock.CODE + ('offline_control_pilot.py',))))
STEPS = [('preflight', 'process'), ('CTRL_R1', 'transfer'), ('CTRL_R2', 'transfer'),
         ('CTRL_prefix', 'paired_fastq'), ('CTRL_compute', 'compact')]
SCOPE = 'offline CTRL-4/SRR33425816 only; 1M paired prefix; no HTTP, TDP, PSI or biological inference'
FILES = ('workflow-job.json', 'operator-acceptance.json', 'ledger.json',
         'workflow-inner.json', 'workflow-receipts/run.json')


def identity():
    return {'python_sha256': clock.transport.base.file_hash(sys.executable)['sha256'],
            'code_sha256': {n: clock.transport.base.file_hash(Path(__file__).with_name(n))['sha256'] for n in CODE},
            'decoder': real.decoder_identity()}


def metadata_chain(value):
    """Recheck frozen metadata snapshots, never old multi-GB partials."""
    if isinstance(value, dict):
        if 'metadata_sha256' in value:
            root = Path(value['root'])
            if not root.is_absolute() or root != root.resolve():
                raise ValueError('Canonical historical metadata root required')
            for name, expected in value['metadata_sha256'].items():
                p = root/name
                if (p.is_symlink() or not p.resolve().is_relative_to(root) or p.stat().st_size > 1024**2 or
                    not re.fullmatch('[0-9a-f]{64}', str(expected)) or sha(p) != expected):
                    raise ValueError('Historical metadata changed/oversized')
        for item in value.values():
            metadata_chain(item)
    elif isinstance(value, list):
        for item in value:
            metadata_chain(item)


def read_binding(root):
    root = Path(root).resolve()
    seal = read(root/'recovery-seal.json')
    if seal.get('status') != 'sealed_verified_ctrl_r2_elapsed' or set(seal.get('sha256', {})) != set(clock.SEALED):
        raise ValueError('Sealed complete CTRL_R2 required')
    for name in clock.SEALED:
        p = root/name
        if p.is_symlink() or p.stat().st_size > 1024**2 or sha(p) != seal['sha256'][name]:
            raise ValueError('R2 sealed metadata changed')
    p, a, s, tail, r, outer = (read(root/n) for n in clock.SEALED)
    check_outer(outer)
    if (sha(root/'recovery-plan.json') != R2_PLAN_SHA or p.get('schema') != 'ctrl-r2-elapsed-clock-v1' or
        p.get('execution_enabled') is not False or p.get('root') != str(root) or
        clock.recovery_root(p['original_root']) != root or p.get('source') != clock.SOURCE or
        p.get('limits') != clock.LIMITS or p.get('identity') != clock.identity() or p.get('scope') != clock.SCOPE or
        p.get('range_start') != clock.PARTIAL_BYTES or p.get('range_end') != clock.SOURCE['bytes']-1 or
        a.get('prepared_sha256') != R2_PLAN_SHA or a.get('accepted_elapsed_clock_window') is not True):
        raise ValueError('Accepted fixed R2 descriptor changed')
    # Historical boot identity is checked internally, not against today's boot.
    policy = p['clock_policy']
    if (set(policy) != {'clock', 'boot_id', 'wall_time'} or policy.get('clock') != 'CLOCK_BOOTTIME' or
        policy.get('wall_time') != 'diagnostic only' or not re.fullmatch('[a-f0-9-]{36}', policy.get('boot_id', '')) or
        seal.get('clock_policy') != policy or s.get('clock_policy') != policy or r.get('clock_policy') != policy):
        raise ValueError('Historical elapsed-clock identity mismatch')
    metadata_chain(p['original_audit'])
    if (s.get('status') != 'verified' or s.get('limits') != p['limits'] or
        s.get('prior_transfer_elapsed_seconds') != p['original_audit']['prior_transfer_elapsed_seconds'] or
        s.get('original_deadline_epoch') != p['original_audit']['prior_global_deadline_epoch'] or
        set(s.get('phases', {})) != {'copy', 'range', 'verify'} or
        not 0 <= s['last_tick']-s['started_tick'] < p['limits']['wall_seconds']):
        raise ValueError('R2 state/elapsed accounting incomplete')
    for name, phase in s['phases'].items():
        cap = p['limits'][{'copy': 'copy_seconds', 'range': 'transfer_seconds', 'verify': 'verify_seconds'}[name]]
        if (phase.get('status') != 'verified' or
            not s['started_tick'] <= phase['started_tick'] <= phase['finished_tick'] < min(phase['deadline_tick'], s['deadline_tick']) or
            phase['finished_tick']-phase['started_tick'] >= cap):
            raise ValueError('Historical R2 phase elapsed cap')
    elapsed = s['phases']['range']['finished_tick']-s['phases']['range']['started_tick']
    if (r.get('status') != 'verified_ctrl_r2_elapsed_pending_outer_seal' or r.get('source_verified') is not True or
        r.get('state_sha256') != sha(root/'recovery-state.json') or r.get('file') != 'CTRL_R2.fastq.gz' or
        r.get('bytes') != clock.SOURCE['bytes'] or r.get('md5') != clock.SOURCE['md5'] or r.get('sha256') != R2_SHA or
        r.get('additional_transfer_elapsed_seconds') != elapsed or
        r.get('prior_transfer_elapsed_seconds') != p['original_audit']['prior_transfer_elapsed_seconds'] or
        r.get('additional_body_bytes') != clock.SOURCE['bytes']-clock.PARTIAL_BYTES or
        any(v.get('cumulative_body_bytes') != CHARGED for v in (seal, r)) or s.get('transfer_bytes_consumed') != CHARGED or
        seal.get('remaining_body_budget_bytes') != 12_000_000_000-CHARGED or
        seal.get('manual_browser_reserved_body_bytes') != clock.MANUAL_BROWSER_RESERVE or
        seal.get('manual_browser_exact_body_known') is not False or
        any(seal.get(k) != v for k, v in {'file':'CTRL_R2.fastq.gz','file_bytes':r['bytes'],'file_md5':r['md5'],'file_sha256':R2_SHA}.items()) or
        tail.get('status') != 'tail_received_not_source_verified' or tail.get('address_family') != 'IPv4' or
        tail.get('body_bytes') != r['additional_body_bytes'] or tail.get('charged_body_bytes') != CHARGED or
        tail.get('range_start') != clock.PARTIAL_BYTES or tail.get('range_end') != clock.SOURCE['bytes']-1):
        raise ValueError('R2 full-file result/source/accounting mismatch')
    b = p['original_audit']['resume_audit']['previous_audit']['ipv4_audit']['pilot_audit']['read_binding']
    if recovered.read_binding(b['root']) != b:
        raise ValueError('R1/index lineage changed')
    files = [{'name':'CTRL_R1','path':str(Path(b['root'])/b['file']),'bytes':b['bytes'],'md5':b['md5'],'sha256':b['sha256']},
             {'name':'CTRL_R2','path':str(root/'CTRL_R2.fastq.gz'),'bytes':r['bytes'],'md5':r['md5'],'sha256':R2_SHA}]
    for item in files:
        path = Path(item['path'])
        if path.is_symlink() or not path.is_file() or path.stat().st_size != item['bytes']:
            raise ValueError('Sealed regular read file missing/size changed')
    return {'root':str(root),'seal_sha256':sha(root/'recovery-seal.json'),'files':files,'index':b['index'],
            'lineage_roots':clock.roots_for(p),'cumulative_body_bytes':CHARGED,
            'prior_transfer_elapsed_seconds':s['prior_transfer_elapsed_seconds']+elapsed,
            'manual_browser_reserved_body_bytes':clock.MANUAL_BROWSER_RESERVE,'manual_browser_exact_body_known':False}


def output_root(binding):
    return Path(binding['root']).with_name(Path(binding['root']).name+'-control-01')


def make_manifest(binding):
    if read_binding(binding['root']) != binding:
        raise ValueError('Control source binding changed')
    m, l = cached.make_manifest(binding['index']['aligner'], binding['index'])
    m, l = copy.deepcopy(m), copy.deepcopy(l)
    l.update(wall_seconds=3000, disk_bytes=27*GiB)
    m['offline_control'] = binding
    m['paired_fastq'] = {'CTRL_prefix':m['paired_fastq']['CTRL_prefix']}
    m['real_compute'] = {'CTRL_compute':m['real_compute']['CTRL_compute']}
    if m['paired_fastq']['CTRL_prefix']['prefix_pairs'] != PREFIX_PAIRS:
        raise ValueError('Fixed prospective prefix required')
    policy = m['execution_policy']
    policy.update(total_seconds=3000, transfer_seconds=600)
    policy['allocations']['artifacts'] = 18*GiB
    policy['phases'] = {n:policy['phases'][n] for n, _ in STEPS}
    for n in ('CTRL_R1','CTRL_R2'):
        policy['phases'][n]['wall_seconds'] = 300
    policy['phases']['preflight']['wall_seconds'] = 180
    m['sealed_workflow'].update(schema='offline-control-v1', origins=[],
        steps=[{'name':n,'kind':{'transfer':'local_read','compact':'stream_compute'}.get(k,k)} for n,k in STEPS])
    execution.validate(policy, l, allow_real=True)
    return m, l


def identity_job(binding):
    m, l = make_manifest(binding)
    return {'schema':'offline-control-pilot-v1','execution_enabled':False,'root':str(output_root(binding)),
            'manifest':m,'limits':l,'identity':identity(),'clock_policy':clock.clock_policy(),'scope':SCOPE}


def prepare(root):
    b = read_binding(Path(root).expanduser().resolve())
    if output_root(b).exists():
        raise ValueError('Control root already exists; no retry')
    job = identity_job(b)
    real.check_host(job['root'], job['limits'])
    disk_guard(job, {'phases':{},'limits':job['limits']})
    projected_disk_check(job)
    return job


def validate_job(job):
    keys = {'schema','execution_enabled','root','manifest','limits','identity','clock_policy','scope'}
    if not isinstance(job,dict) or set(job) != keys or job.get('schema') != 'offline-control-pilot-v1' or job.get('execution_enabled') is not False:
        raise ValueError('Disabled fixed offline control job required')
    b = job['manifest']['offline_control']
    if job != identity_job(b):
        raise ValueError('Fixed samples/code/resources/clock/lineage changed')
    return Path(job['root'])


def history_bytes(binding):
    total = 0
    for base in binding['lineage_roots']:
        for path in execution.iter_files(base):
            try:
                if path.is_symlink():raise ValueError('Historical data symlink')
                if path.is_file():total += path.stat().st_size
            except FileNotFoundError:pass
    return total


def projected_disk_check(job):
    b = job['manifest']['offline_control']
    projected = history_bytes(b)+sum(item['bytes'] for item in b['files'])
    if projected > job['manifest']['execution_policy']['allocations']['artifacts']:
        raise ValueError('Historical artifacts plus both planned local copies exceed artifact partition')


def disk_guard(job, state):
    root = Path(job['root']);m = job['manifest'];l = job['limits']
    usage = execution.disk_usage(root, state)
    binding = m['offline_control'];roots = binding['lineage_roots']
    if len(roots) != 11 or len(set(roots+[str(root)])) != 12:
        raise ValueError('Twelve distinct cumulative trees required')
    history = history_bytes(binding)
    usage['artifacts'] += history
    if sum(usage.values()) > l['disk_bytes'] or any(usage[k] > m['execution_policy']['allocations'][k] for k in usage):
        raise RuntimeError('Control lineage disk/partition cap')
    base = root if root.exists() else root.parent
    if real.shutil.disk_usage(base).free < l['reserve_bytes']:
        raise RuntimeError('Control free disk reserve')


class Runner:
    def __init__(self, job, elapsed_clock=clock.tick, wall_clock=time.time):
        self.job = job;self.root = validate_job(job);self.manifest = job['manifest'];self.policy = self.manifest['execution_policy']
        self.elapsed_clock,self.clock = elapsed_clock,wall_clock
        self.root.mkdir(exist_ok=True)
        self.lock = (self.root/'runner.lock').open('a')
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX|fcntl.LOCK_NB)
            self.path = self.root/'ledger.json'
            if self.path.exists():
                raise ValueError('Never reopen an attempted control')
            now = elapsed_clock()
            self.observed_tick = now
            self.state = {'fingerprint':digest({'manifest':self.manifest,'limits':job['limits']}),
                'limits':job['limits'],'clock_policy':job['clock_policy'],'started_tick':now,'last_tick':now,
                'deadline_tick':now+job['limits']['wall_seconds'],'last_epoch':wall_clock(),
                'transfer_bytes_consumed':CHARGED,'new_transfer_bytes':0,
                'prior_transfer_elapsed_seconds':self.manifest['offline_control']['prior_transfer_elapsed_seconds'],
                'phases':{},'mode':'offline-control-only','raw_execution_ready':False}
            self.save();self.guard()
        except BaseException:
            self.lock.close();raise
    def close(self):self.lock.close()
    def phase_policy(self, name, kind):
        p = self.policy['phases'].get(name)
        if p is None or p['kind'] != kind:
            raise ValueError('Declared phase with matching kind required')
        return p
    def guard(self):
        now = self.elapsed_clock()
        if now < self.observed_tick:
            raise RuntimeError('Control elapsed clock moved backwards')
        self.observed_tick = now
        check_state(self.job,self.state,now)
        if now-getattr(self,'last_disk',float('-inf')) >= .1:
            disk_guard(self.job,self.state);self.last_disk = now
    def save(self):
        now,wall = self.elapsed_clock(),self.clock()
        if not math.isfinite(now) or now < self.observed_tick:
            raise RuntimeError('Invalid control elapsed clock')
        self.observed_tick = now
        for phase in self.state['phases'].values():
            if phase['status'] != 'started' and 'finished_tick' not in phase:
                phase.update(finished_tick=now,finished_epoch=wall)
                if phase['status']=='verified' and now >= min(phase['deadline_tick'],phase.get('subdeadline_tick',phase['deadline_tick'])):
                    phase.update(status='failed',error_type='CommitElapsedViolation')
                    atomic_json(self.path,self.state)
                    raise RuntimeError('Control phase expired before commit')
        delta = (wall-self.state['last_epoch'])-(now-self.state['last_tick'])
        if abs(delta) > .5:
            events = self.state.setdefault('wall_clock_adjustments',[])
            if len(events)<16:events.append({'tick':now,'wall_epoch':wall,'offset_change_seconds':delta})
        self.state.update(last_tick=now,last_epoch=wall)
        atomic_json(self.path,self.state)
    def begin(self, name, kind, signature):
        self.guard();caps = self.phase_policy(name,kind)
        if name in self.state['phases'] or any(p['status']=='started' for p in self.state['phases'].values()):
            raise ValueError('No adopted/overlapping phases')
        expected = [n for n,_ in STEPS]
        if list(self.state['phases']) != expected[:expected.index(name)]:
            raise ValueError('Fixed control phase order required')
        now = self.elapsed_clock()
        phase = {'kind':kind,'status':'started','signature':signature,'started_tick':now,'started_epoch':self.clock(),
                 'deadline_tick':min(now+caps['wall_seconds'],self.state['deadline_tick'])}
        if kind=='compact':phase.update(substage='producer',subdeadline_tick=min(phase['deadline_tick'],now+caps['producer_seconds']))
        self.state['phases'][name] = phase;self.save();return True
    def remaining(self,name,kind):
        self.guard();caps = self.phase_policy(name,kind);now = self.elapsed_clock();phase = self.state['phases'].get(name,{})
        remain = min(self.state['deadline_tick']-now,caps['wall_seconds'])
        if phase.get('status')=='started':remain = min(remain,phase['deadline_tick']-now,phase.get('subdeadline_tick',phase['deadline_tick'])-now)
        if remain<=0:raise RuntimeError('No remaining control phase time')
        return remain
    def compact_reduction(self,name):
        self.guard();p = self.state['phases'][name]
        if p['kind']!='compact' or p['status']!='started' or p.get('substage')!='producer':
            raise ValueError('Invalid compact stage transition')
        now = self.elapsed_clock();p.update(substage='reduce',subdeadline_tick=min(p['deadline_tick'],now+self.phase_policy(name,'compact')['reduce_seconds']))
        self.save();return 0
    def paired_fastq(self,name):return paired.run_phase(self,name)


def check_state(job,state,now):
    if state.get('clock_policy') != job['clock_policy'] or not math.isfinite(now) or now < state['last_tick']:
        raise RuntimeError('Control elapsed clock/boot mismatch')
    if now >= state['deadline_tick']:
        raise RuntimeError('Control total elapsed deadline')
    if state['transfer_bytes_consumed'] != CHARGED or state.get('new_transfer_bytes') != 0:
        raise RuntimeError('Offline control body counter changed')
    if state.get('prior_transfer_elapsed_seconds') != job['manifest']['offline_control']['prior_transfer_elapsed_seconds']:
        raise RuntimeError('Historical clock accounting changed')
    for name,p in state['phases'].items():
        if p['status']=='started' and now >= min(p['deadline_tick'],p.get('subdeadline_tick',p['deadline_tick'])):
            raise RuntimeError('Control phase/subphase elapsed deadline: '+name)


def adopt_read(runner,name):
    item = next(f for f in runner.manifest['offline_control']['files'] if f['name']==name)
    runner.begin(name,'transfer',digest(item));p = runner.state['phases'][name]
    source = Path(item['path']);target = runner.root/(name+'.partial')
    try:
        if source.is_symlink() or clock.transport.whole_hash(source,runner.guard) != {k:item[k] for k in ('bytes','md5','sha256')}:
            raise ValueError('Recovered read changed')
        clock.transport.base.copy_prefix(source,target,{k:item[k] for k in ('bytes','sha256')},runner.guard)
        if clock.transport.whole_hash(source,runner.guard) != {k:item[k] for k in ('bytes','md5','sha256')}:
            raise ValueError('Recovered read changed during copy')
        runner.guard();os.replace(target,runner.root/name)
        fd = os.open(runner.root,os.O_DIRECTORY)
        try:os.fsync(fd)
        finally:os.close(fd)
        p.update(status='verified',**{k:item[k] for k in ('bytes','md5','sha256')},source_kind='sealed_local_read',source=item,new_body_bytes=0)
        runner.save()
    except BaseException as exc:
        p.update(status='failed',error_type=type(exc).__name__);runner.save();raise


def deny_network(event,args):
    if event in ('socket.connect','socket.getaddrinfo'):
        raise RuntimeError('Offline control worker cannot connect to network')


def worker(job):
    r = Runner(job)
    try:
        for name,kind in STEPS:
            caps = r.phase_policy(name,kind);_,hard = resource.getrlimit(resource.RLIMIT_AS)
            resource.setrlimit(resource.RLIMIT_AS,(caps['address_space_bytes'],hard))
            if name=='preflight':cached.run_preflight(r,name)
            elif kind=='transfer':adopt_read(r,name)
            elif kind=='paired_fastq':r.paired_fastq(name)
            else:real.run_stream(r,name)
        r.guard()
        binding = r.manifest['offline_control']
        if read_binding(binding['root']) != binding:
            raise ValueError('Source metadata changed during control')
        coverage = r.state['phases']['CTRL_compute']['coverage']
        atomic_json(r.root/'workflow-inner.json',{'status':'coverage_adequate' if coverage['adequate'] else 'coverage_insufficient',
            'completed_steps':[n for n,_ in STEPS],'coverage':coverage,'ledger_sha256':sha(r.path),'new_transfer_bytes':0,'raw_execution_ready':False})
    finally:r.close()


def monitor(job,start):
    last_disk = [float('-inf')]
    def guard():
        now = clock.tick()
        if now<start or now-start>=job['limits']['wall_seconds']:
            raise RuntimeError('External control total elapsed cap')
        if clock.clock_policy()!=job['clock_policy']:
            raise RuntimeError('External control boot changed')
        path = Path(job['root'])/'ledger.json'
        if path.exists():
            state = read(path)
            if state['limits']!=job['limits']:raise RuntimeError('External control limits changed')
            check_state(job,state,clock.tick())
        else:state = {'phases':{},'limits':job['limits']}
        if now-last_disk[0]>=.1:disk_guard(job,state);last_disk[0] = now
    def memory(rss,members,identity):
        path = Path(job['root'])/'ledger.json'
        if path.exists():
            s = read(path)
            for name,p in s['phases'].items():
                if p['status']=='started' and rss>job['manifest']['execution_policy']['phases'][name]['rss_bytes']:
                    raise RuntimeError('External control phase RSS cap')
    return guard,memory


def accept_outer(job,record):
    check_outer(record);root = Path(job['root'])
    if read(root/'workflow-receipts/run.json')!=record or read(root/'workflow-job.json')!=job:
        raise ValueError('Control external receipt/job changed')
    a = read(root/'operator-acceptance.json')
    if a.get('prepared_sha256')!=sha(root/'workflow-job.json') or a.get('accepted_offline_control_window') is not True:
        raise ValueError('Control acceptance missing')
    s,inner = read(root/'ledger.json'),read(root/'workflow-inner.json')
    expected = [n for n,_ in STEPS]
    if (s.get('fingerprint')!=digest({'manifest':job['manifest'],'limits':job['limits']}) or s.get('limits')!=job['limits'] or
        s.get('clock_policy')!=job['clock_policy'] or s.get('transfer_bytes_consumed')!=CHARGED or s.get('new_transfer_bytes')!=0 or
        s.get('prior_transfer_elapsed_seconds')!=job['manifest']['offline_control']['prior_transfer_elapsed_seconds'] or
        list(s.get('phases',{}))!=expected or inner.get('completed_steps')!=expected or inner.get('ledger_sha256')!=sha(root/'ledger.json') or
        inner.get('new_transfer_bytes')!=0 or not 0<=s['last_tick']-s['started_tick']<job['limits']['wall_seconds']):
        raise ValueError('Control incomplete phases/clocks/accounting')
    for name,kind in STEPS:
        p = s['phases'][name];caps = job['manifest']['execution_policy']['phases'][name]
        if (p.get('kind')!=kind or p.get('status')!='verified' or
            not s['started_tick']<=p['started_tick']<=p['finished_tick']<min(p['deadline_tick'],p.get('subdeadline_tick',p['deadline_tick']),s['deadline_tick']) or
            p['finished_tick']-p['started_tick']>=caps['wall_seconds']):
            raise ValueError('Control phase incomplete/expired')
        if kind=='transfer':
            item = next(f for f in job['manifest']['offline_control']['files'] if f['name']==name)
            if p.get('source')!=item or p.get('new_body_bytes')!=0 or any(p.get(k)!=item[k] for k in ('bytes','md5','sha256')):
                raise ValueError('Missing local read provenance')
    pre = s['phases']['preflight']
    pre_result = read(root/'cached-preflight.json')
    if (pre.get('receipt') != 'cached-preflight.json' or pre.get('receipt_sha256') != sha(root/'cached-preflight.json') or
        pre.get('signature') != digest({'cached_index':job['manifest']['cached_index'],'producer':job['manifest']['sealed_workflow']['producer']}) or
        pre_result.get('status') != 'verified' or pre_result.get('cached_index') != job['manifest']['cached_index'] or
        pre_result.get('probe',{}).get('sha256') != job['manifest']['aligner']['sha256']):
        raise ValueError('Control preflight receipt incomplete')
    pair = read(root/'paired-fastq/CTRL_prefix/result.json')
    pair_receipt = read(root/'paired-fastq/CTRL_prefix/receipt.json')
    if (sha(root/'paired-fastq/CTRL_prefix/receipt.json') != s['phases']['CTRL_prefix'].get('receipt_sha256') or
        pair_receipt.get('status') != 'verified' or pair_receipt.get('result_sha256') != sha(root/'paired-fastq/CTRL_prefix/result.json') or
        pair_receipt.get('binding') != s['phases']['CTRL_prefix'].get('binding')):
        raise ValueError('Control pair receipt incomplete')
    out = root/'compact/CTRL_compute';receipt = read(out/'receipt.json');result = read(out/'result.json')
    spec = job['manifest']['real_compute']['CTRL_compute']
    binding = s['phases']['CTRL_compute'].get('binding',{})
    argv = real.alignment_argv(root,spec,job['manifest']['aligner']);argv[argv.index('-x')+1] = job['manifest']['cached_index']['index_prefix']
    if (receipt.get('binding') != binding or binding.get('spec') != spec or binding.get('fingerprint') != s['fingerprint'] or
        binding.get('paired_sha256') != digest(s['phases']['CTRL_prefix']) or binding.get('preflight_sha256') != digest(pre) or
        binding.get('cached_index') != job['manifest']['cached_index'] or binding.get('aligner') != job['manifest']['aligner'] or
        binding.get('producer') != job['manifest']['sealed_workflow']['producer'] or binding.get('argv') != argv or
        s['phases']['CTRL_compute'].get('signature') != digest({'spec':spec,'fingerprint':s['fingerprint']}) or
        receipt.get('plaintext_removed_on_success') is not True):
        raise ValueError('Control alignment provenance incomplete')
    metric = real.coverage(result,spec)
    if (pair.get('status')!='verified' or pair.get('source_gzip_eof_crc_validated') is not True or pair.get('prefix_pairs_written')!=PREFIX_PAIRS or
        sha(out/'receipt.json')!=s['phases']['CTRL_compute']['receipt_sha256'] or receipt.get('status')!='verified' or
        receipt.get('result_sha256')!=sha(out/'result.json') or result.get('status')!='verified' or result.get('producer_exit_code')!=0 or
        s['phases']['CTRL_compute'].get('coverage')!=metric or receipt.get('coverage')!=metric or inner.get('coverage')!=metric or
        inner.get('status')!=('coverage_adequate' if metric['adequate'] else 'coverage_insufficient') or
        (root/'alignment-inputs/CTRL_compute').exists()):
        raise ValueError('Control paired/producer/coverage result incomplete')
    seal = {'status':'sealed_offline_control_pilot','technical_status':inner['status'],'root':str(root),
        'sha256':{n:sha(root/n) for n in FILES},'coverage':metric,'pairs_scanned':pair['pairs_scanned'],
        'prefix_pairs':PREFIX_PAIRS,'counts_primary':result['routes']['text15']['counts'],'new_transfer_bytes':0,
        'cumulative_body_bytes':CHARGED,'remaining_body_budget_bytes':job['limits']['transfer_bytes']-CHARGED,
        'manual_browser_reserved_body_bytes':job['manifest']['offline_control']['manual_browser_reserved_body_bytes'],
        'manual_browser_exact_body_known':False,'raw_execution_ready':False}
    atomic_json(root/'workflow-seal.json',seal);return seal


def execute(path,accepted,accept_window=False):
    if not accept_window:raise ValueError('Explicit new offline control 50-minute window acceptance required')
    if not re.fullmatch('[0-9a-f]{64}',accepted or '') or sha(path)!=accepted:raise ValueError('Exact prepared SHA acceptance required')
    job = read(path);root = validate_job(job)
    real.check_host(root,job['limits']);disk_guard(job,{'phases':{},'limits':job['limits']});projected_disk_check(job)
    root.mkdir(exist_ok=False)
    with (root/'workflow-job.json').open('xb') as f:f.write(Path(path).read_bytes());f.flush();os.fsync(f.fileno())
    atomic_json(root/'operator-acceptance.json',{'prepared_sha256':accepted,'accepted_offline_control_window':True,'accepted_epoch':time.time()})
    guard,memory = monitor(job,clock.tick());caps = job['limits']['process_caps']
    record = supervise('run',[sys.executable,str(Path(__file__).resolve()),'--worker',str(root/'workflow-job.json')],
        root/'workflow-receipts',timeout=job['limits']['wall_seconds'],rss_limit=caps['rss_bytes'],address_space=caps['address_space_bytes'],
        checkpoint=guard,group_checkpoint=memory)
    return accept_outer(job,record)


def worker_file(path):
    job = read(path);root = validate_job(job)
    if Path(path).resolve()!=root/'workflow-job.json':raise ValueError('Fixed control worker path')
    a = read(root/'operator-acceptance.json')
    if a.get('prepared_sha256')!=sha(path) or a.get('accepted_offline_control_window') is not True:raise ValueError('Missing control worker acceptance')
    receipt = root/'workflow-receipts/run.json';outer = read(receipt);until = time.monotonic()+2
    while outer.get('status')=='started' and 'procfs_group' not in outer and time.monotonic()<until:time.sleep(.01);outer = read(receipt)
    if outer.get('status')!='started' or outer.get('procfs_group')!=proc_info(int(os.readlink('/proc/self')))['group']:
        raise ValueError('Active parent supervisor required')
    sys.addaudithook(deny_network)
    worker(job)


def main():
    p = argparse.ArgumentParser(description=__doc__);g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--prepare',type=Path);g.add_argument('--execute',type=Path);g.add_argument('--worker',type=Path,help=argparse.SUPPRESS)
    p.add_argument('--recovery',type=Path);p.add_argument('--accept-plan-sha256');p.add_argument('--accept-offline-control-window',action='store_true')
    a = p.parse_args()
    if a.prepare:
        if not a.recovery:p.error('--recovery required')
        job = prepare(a.recovery)
        with a.prepare.open('x') as f:json.dump(job,f,indent=2);f.write('\n')
        print(json.dumps({'prepared_file':str(a.prepare),'sha256':sha(a.prepare),'execution_enabled':False,'root':job['root'],
            'new_transfer_bytes':0,'prior_charged_body_bytes':CHARGED,'total_seconds':3000,'prefix_pairs':PREFIX_PAIRS,
            'minimum_fragment_union':20,'scope':SCOPE,'clock':'CLOCK_BOOTTIME','raw_execution_ready':False},indent=2))
    elif a.execute:print(json.dumps(execute(a.execute,a.accept_plan_sha256,a.accept_offline_control_window),indent=2))
    else:worker_file(a.worker)


if __name__=='__main__':main()
