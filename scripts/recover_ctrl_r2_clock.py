"""CTRL_R2 continuation with elapsed-clock deadlines; wall time is diagnostic.

Linux CLOCK_BOOTTIME is shared by parent/worker. Same 2400/1800/300/300s caps,
prior accounting retained; no retry or old-run reopening. Preparation is offline.
"""
import argparse
import json
import math
import os
from pathlib import Path
import re
import sys
import time

import recover_ctrl_r2_resume as previous
from process_supervisor_v2 import atomic_json, supervise, proc_info
from workflow_seal import read, sha, check_outer
from pilot_execution_policy import iter_files

transport = previous.transport
SOURCE = previous.SOURCE
LIMITS = dict(previous.LIMITS)
CHARGED = 7226257234
PARTIAL_BYTES = 900998714
MANUAL_BROWSER_RESERVE = previous.MANUAL_BROWSER_RESERVE
CODE = tuple(sorted(set(previous.CODE + ('recover_ctrl_r2_clock.py',))))
META = previous.META
SEALED = previous.previous.previous.SEALED
SCOPE = 'recover CTRL_R2 only over verified HTTPS/IPv4; elapsed-clock deadlines; no other mates or alignment'
range_append = previous.range_append


def tick():
    return time.clock_gettime(time.CLOCK_BOOTTIME)


def boot_id():
    return Path('/proc/sys/kernel/random/boot_id').read_text().strip()


def clock_policy():
    if not hasattr(time, 'CLOCK_BOOTTIME'):
        raise ValueError('Linux CLOCK_BOOTTIME required')
    return {'clock': 'CLOCK_BOOTTIME', 'boot_id': boot_id(), 'wall_time': 'diagnostic only'}


def identity():
    return {'python_sha256': transport.base.file_hash(sys.executable)['sha256'],
            'code_sha256': {n: transport.base.file_hash(Path(__file__).with_name(n))['sha256'] for n in CODE}}


def recovery_root(original):
    return Path(original).with_name(Path(original).name+'-clock-01')


def inspect(original, guard=lambda: None):
    original = Path(original).resolve()
    if any((original/n).is_symlink() for n in META):
        raise ValueError('Historical metadata symlink')
    hashes = {n: sha(original/n) for n in META}
    p = read(original/'recovery-plan.json')
    if previous.validate_plan(p) != original:
        raise ValueError('Previous fixed continuation required')
    prior = previous.inspect(p['original_root'], guard)
    if prior != p['original_audit']:
        raise ValueError('Previous lineage changed')
    a, state, outer, attempt = (read(original/n) for n in
        ('operator-acceptance.json', 'recovery-state.json', 'supervision/run.json', 'range-attempt.json'))
    if (a.get('prepared_sha256') != hashes['recovery-plan.json'] or
        a.get('accepted_additional_time_window') is not True or
        a.get('browser_stopped_and_manual_reserve_accepted') is not True or
        outer.get('status') != 'finished' or outer.get('exit_code') != -9 or
        outer.get('supervisor_error') != 'RuntimeError: External clock/body cap' or
        outer.get('violation') is not None or outer.get('live_group_members_after_cleanup') != []):
        raise ValueError('Stopped clock-failed accepted continuation required')
    if (state.get('status') != 'failed' or state.get('error_type') != 'RuntimeError' or
        state.get('limits') != LIMITS or state.get('transfer_bytes_consumed') != CHARGED or
        state.get('prior_transfer_elapsed_seconds') != 14500.072928190231 or
        state.get('prior_transfer_elapsed_seconds') != prior['prior_transfer_elapsed_seconds'] or
        state.get('original_deadline_epoch') != prior['prior_global_deadline_epoch'] or
        state.get('deadline_epoch') != 1793709745.7293887 or set(state.get('phases', {})) != {'copy', 'range'}):
        raise ValueError('Exact failed state/counters required')
    phase = state['phases']['range']
    if (state['phases']['copy'].get('status') != 'verified' or phase.get('status') != 'failed' or
        phase.get('error_type') != 'RuntimeError' or phase.get('reservation_start_body_bytes') != 0 or
        phase.get('unsettled_body_reservation_bytes') != 4194304 or
        attempt.get('status') != 'failed' or attempt.get('error_type') != 'RuntimeError' or
        attempt.get('body_bytes') != 623663 or attempt.get('range_start') != previous.PARTIAL_BYTES or
        attempt.get('range_end') != SOURCE['bytes']-1 or attempt.get('prior_charged_bytes') != previous.CHARGED or
        attempt.get('attempts') != 1 or attempt.get('address_family') != 'IPv4' or
        attempt.get('accounting') != 'durable-block-reservation-v1' or attempt.get('reservation_block_bytes') != 4194304):
        raise ValueError('Exact failed request/reservation required')
    if CHARGED != previous.CHARGED+4194304:
        raise ValueError('No reservation refund')
    partial = original/'recovered-CTRL_R2.partial'
    if partial.is_symlink() or partial.stat().st_size != PARTIAL_BYTES or PARTIAL_BYTES != previous.PARTIAL_BYTES+623663:
        raise ValueError('Exact preserved partial required')
    if (original/'recovery-result.json').exists() or (original/'recovery-seal.json').exists():
        raise ValueError('Failed attempt must not have a successful result')
    actual = transport.base.file_hash(partial, guard)
    if actual['bytes'] != PARTIAL_BYTES or hashes != {n: sha(original/n) for n in META}:
        raise ValueError('Historical files changed during audit')
    return {'root': str(original), 'metadata_sha256': hashes, 'partial_bytes': PARTIAL_BYTES,
            'partial_sha256': actual['sha256'], 'charged_body_bytes': CHARGED,
            'prior_transfer_elapsed_seconds': prior['prior_transfer_elapsed_seconds']+1800,
            'clock_carry_policy': 'reserve prior full 1800s window; not measured elapsed',
            'prior_global_deadline_epoch': state['deadline_epoch'], 'resume_audit': prior,
            'manual_browser_reserved_body_bytes': MANUAL_BROWSER_RESERVE,
            'manual_browser_exact_body_known': False}


def roots_for(plan):
    resume = plan['original_audit']['resume_audit']
    final = resume['previous_audit']
    ipv4 = final['ipv4_audit']
    pilot = ipv4['pilot_audit']
    b = pilot['read_binding']
    roots = [b['index'][k] for k in ('original_root', 'recovery_root', 'index_root')]
    roots += [b['original_root'], b['root'], pilot['root'], ipv4['root'], final['root'],
              resume['root'], plan['original_root'], plan['root']]
    if len(set(roots)) != 11:
        raise ValueError('Eleven distinct lineage roots required')
    return roots


def disk_guard(plan):
    size = 0
    for root in roots_for(plan):
        for path in iter_files(root):
            try:
                if path.is_symlink():
                    raise ValueError('Lineage symlink')
                if path.is_file():
                    size += path.stat().st_size
            except FileNotFoundError:
                pass
    if size > LIMITS['disk_bytes'] or previous.shutil.disk_usage(plan['original_root']).free < LIMITS['reserve_bytes']:
        raise RuntimeError('Lineage disk cap/reserve')


def prepare(original):
    original = Path(original).expanduser().resolve()
    root = recovery_root(original)
    if root.exists():
        raise ValueError('Attempted root exists; no retry')
    obs = inspect(original)
    previous.require_space(original)
    return {'schema': 'ctrl-r2-elapsed-clock-v1', 'execution_enabled': False, 'original_root': str(original),
            'root': str(root), 'original_audit': obs, 'source': dict(SOURCE), 'limits': dict(LIMITS),
            'identity': identity(), 'clock_policy': clock_policy(), 'range_start': PARTIAL_BYTES,
            'range_end': SOURCE['bytes']-1, 'scope': SCOPE}


def validate_plan(p):
    keys = {'schema', 'execution_enabled', 'original_root', 'root', 'original_audit', 'source', 'limits',
            'identity', 'clock_policy', 'range_start', 'range_end', 'scope'}
    if not isinstance(p, dict) or set(p) != keys or p['schema'] != 'ctrl-r2-elapsed-clock-v1' or p['execution_enabled'] is not False:
        raise ValueError('Disabled fixed elapsed-clock plan required')
    old, root, obs = Path(p['original_root']), Path(p['root']), p['original_audit']
    if not old.is_absolute() or old != old.resolve() or root != recovery_root(old) or root != root.resolve() or obs['root'] != str(old):
        raise ValueError('Exclusive canonical roots required')
    if (p['source'] != SOURCE or p['limits'] != LIMITS or p['identity'] != identity() or
        p['clock_policy'] != clock_policy() or p['scope'] != SCOPE or
        type(p['range_start']) is not int or p['range_start'] != PARTIAL_BYTES or
        obs['partial_bytes'] != PARTIAL_BYTES or p['range_end'] != SOURCE['bytes']-1 or
        not re.fullmatch('[0-9a-f]{64}', str(obs['partial_sha256']))):
        raise ValueError('Fixed source/code/clock/partial changed')
    if (obs['charged_body_bytes'] != CHARGED or obs['prior_transfer_elapsed_seconds'] != 16300.072928190231 or
        obs['prior_global_deadline_epoch'] != 1793709745.7293887 or
        obs['manual_browser_reserved_body_bytes'] != MANUAL_BROWSER_RESERVE or obs['manual_browser_exact_body_known'] is not False or
        CHARGED+SOURCE['bytes']-PARTIAL_BYTES > LIMITS['transfer_bytes']):
        raise ValueError('Historical accounting changed')
    return root


def check_elapsed(state, now, policy, floor):
    if state.get('clock_policy') != policy:
        raise RuntimeError('Elapsed clock/boot identity changed')
    if not math.isfinite(now) or now < state['last_tick']:
        raise RuntimeError('Elapsed clock invalid/backwards')
    if now >= state['deadline_tick']:
        raise RuntimeError('Total elapsed deadline')
    if not floor <= state['transfer_bytes_consumed'] <= state['limits']['transfer_bytes']:
        raise RuntimeError('Body cap/floor')
    for name, phase in state['phases'].items():
        if phase['status'] == 'started' and now >= phase['deadline_tick']:
            raise RuntimeError('Elapsed phase deadline: '+name)


class Budget:
    def __init__(self, plan, elapsed_clock=tick, wall_clock=time.time):
        self.plan, self.root = plan, Path(plan['root'])
        self.elapsed_clock, self.clock = elapsed_clock, wall_clock
        now, wall = elapsed_clock(), wall_clock()
        self.observed_tick = now
        self.state = {'status': 'started', 'limits': plan['limits'], 'clock_policy': plan['clock_policy'],
                      'started_tick': now, 'last_tick': now, 'deadline_tick': now+plan['limits']['wall_seconds'],
                      'started_epoch': wall, 'last_epoch': wall, 'deadline_epoch_informational': wall+plan['limits']['wall_seconds'],
                      'transfer_bytes_consumed': plan['original_audit']['charged_body_bytes'],
                      'prior_transfer_elapsed_seconds': plan['original_audit']['prior_transfer_elapsed_seconds'],
                      'original_deadline_epoch': plan['original_audit']['prior_global_deadline_epoch'], 'phases': {}}
        if (self.root/'recovery-state.json').exists():
            raise ValueError('Never reopen an attempted run')
        self.save()
    def save(self):
        now, wall = self.elapsed_clock(), self.clock()
        if now < self.observed_tick:
            raise RuntimeError('Elapsed clock moved backwards')
        self.observed_tick = now
        offset_change = (wall-self.state['last_epoch'])-(now-self.state['last_tick'])
        if abs(offset_change) > .5:
            events = self.state.setdefault('wall_clock_adjustments', [])
            if len(events) < 16:
                events.append({'tick': now, 'wall_epoch': wall, 'offset_change_seconds': offset_change})
        self.state.update(last_tick=now, last_epoch=wall)
        atomic_json(self.root/'recovery-state.json', self.state)
    def guard(self):
        now = self.elapsed_clock()
        if now < self.observed_tick:
            raise RuntimeError('Elapsed clock moved backwards')
        self.observed_tick = now
        check_elapsed(self.state, now, self.plan['clock_policy'], self.plan['original_audit']['charged_body_bytes'])
        if now-getattr(self, 'last_disk', float('-inf')) >= .1:
            disk_guard(self.plan)
            self.last_disk = now
    def begin(self, name):
        self.guard()
        if name in self.state['phases'] or any(p['status'] == 'started' for p in self.state['phases'].values()):
            raise ValueError('Exclusive sequential phase required')
        now = self.elapsed_clock()
        cap = self.plan['limits'][{'copy': 'copy_seconds', 'range': 'transfer_seconds', 'verify': 'verify_seconds'}[name]]
        self.state['phases'][name] = {'status': 'started', 'started_tick': now,
            'deadline_tick': min(now+cap, self.state['deadline_tick']), 'started_epoch': self.clock()}
        self.save()
    def finish(self, name):
        self.guard()
        self.state['phases'][name].update(status='verified', finished_tick=self.elapsed_clock(), finished_epoch=self.clock())
        self.save()
    def remaining(self):
        self.guard()
        deadlines = [self.state['deadline_tick']]+[p['deadline_tick'] for p in self.state['phases'].values() if p['status'] == 'started']
        return min(deadlines)-self.elapsed_clock()


def monitor(plan, start, elapsed_clock=tick):
    last_disk = [float('-inf')]
    def guard():
        now = elapsed_clock()
        if not math.isfinite(now) or now < start or now-start >= plan['limits']['wall_seconds']:
            raise RuntimeError('External total elapsed deadline')
        if clock_policy() != plan['clock_policy']:
            raise RuntimeError('External boot identity changed')
        path = Path(plan['root'])/'recovery-state.json'
        if path.exists():
            s = read(path)
            if (s['limits'] != plan['limits'] or s['prior_transfer_elapsed_seconds'] != plan['original_audit']['prior_transfer_elapsed_seconds'] or
                s['original_deadline_epoch'] != plan['original_audit']['prior_global_deadline_epoch']):
                raise RuntimeError('External historical accounting changed')
            # Sample AFTER reading the receipt: the worker can save between
            # the parent's first sample and the file read.
            check_elapsed(s, elapsed_clock(), plan['clock_policy'], plan['original_audit']['charged_body_bytes'])
        if now-last_disk[0] >= .1:
            disk_guard(plan)
            last_disk[0] = now
    return guard


def recover(b):
    p, root = b.plan, b.root
    target = root/'recovered-CTRL_R2.partial'
    try:
        b.begin('copy')
        if inspect(p['original_root'], b.guard) != p['original_audit']:
            raise ValueError('Original changed')
        transport.base.copy_prefix(Path(p['original_root'])/'recovered-CTRL_R2.partial', target,
                                   {'bytes': p['range_start'], 'sha256': p['original_audit']['partial_sha256']}, b.guard)
        b.finish('copy')
        b.begin('range')
        range_append(b, target, p['source'], p['range_start'])
        b.finish('range')
        b.begin('verify')
        actual = transport.whole_hash(target, b.guard)
        if actual['bytes'] != p['source']['bytes'] or actual['md5'] != p['source']['md5']:
            raise ValueError('Whole recovered FASTQ MD5/size mismatch')
        if inspect(p['original_root'], b.guard) != p['original_audit']:
            raise ValueError('Original changed during recovery')
        b.guard()
        os.replace(target, root/'CTRL_R2.fastq.gz')
        fd = os.open(root, os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
        b.finish('verify')
        b.state['status'] = 'verified'
        b.save()
        phase = b.state['phases']['range']
        atomic_json(root/'recovery-result.json', {'status': 'verified_ctrl_r2_elapsed_pending_outer_seal',
            'file': 'CTRL_R2.fastq.gz', **actual, 'state_sha256': sha(root/'recovery-state.json'),
            'cumulative_body_bytes': b.state['transfer_bytes_consumed'],
            'additional_body_bytes': b.state['transfer_bytes_consumed']-p['original_audit']['charged_body_bytes'],
            'prior_transfer_elapsed_seconds': p['original_audit']['prior_transfer_elapsed_seconds'],
            'additional_transfer_elapsed_seconds': phase['finished_tick']-phase['started_tick'],
            'clock_policy': p['clock_policy'], 'source_verified': True, 'raw_execution_ready': False})
    except BaseException as exc:
        for phase in b.state['phases'].values():
            if phase['status'] == 'started':
                phase.update(status='failed', error_type=type(exc).__name__, finished_tick=b.elapsed_clock(), finished_epoch=b.clock())
        b.state.update(status='failed', error_type=type(exc).__name__)
        b.save()
        raise


def accept_outer(root, plan, record):
    check_outer(record)
    root = Path(root)
    if read(root/'supervision/run.json') != record or read(root/'recovery-plan.json') != plan:
        raise ValueError('Outer receipt/plan changed')
    a = read(root/'operator-acceptance.json')
    if a.get('prepared_sha256') != sha(root/'recovery-plan.json') or a.get('accepted_elapsed_clock_window') is not True:
        raise ValueError('Elapsed clock acceptance missing')
    s, r, tail = (read(root/n) for n in ('recovery-state.json', 'recovery-result.json', 'range-attempt.json'))
    if (s.get('status') != 'verified' or s.get('limits') != plan['limits'] or s.get('clock_policy') != plan['clock_policy'] or
        s.get('prior_transfer_elapsed_seconds') != plan['original_audit']['prior_transfer_elapsed_seconds'] or
        s.get('original_deadline_epoch') != plan['original_audit']['prior_global_deadline_epoch'] or
        set(s.get('phases', {})) != {'copy', 'range', 'verify'} or any(p.get('status') != 'verified' for p in s['phases'].values())):
        raise ValueError('Incomplete elapsed-clock state')
    if not 0 <= s['last_tick']-s['started_tick'] < plan['limits']['wall_seconds']:
        raise ValueError('Final total elapsed cap')
    for name, p in s['phases'].items():
        cap = plan['limits'][{'copy': 'copy_seconds', 'range': 'transfer_seconds', 'verify': 'verify_seconds'}[name]]
        if not s['started_tick'] <= p['started_tick'] <= p['finished_tick'] < min(p['deadline_tick'], s['deadline_tick']) or p['finished_tick']-p['started_tick'] >= cap:
            raise ValueError('Final phase elapsed cap')
    elapsed = s['phases']['range']['finished_tick']-s['phases']['range']['started_tick']
    expected = plan['original_audit']['charged_body_bytes']+plan['source']['bytes']-plan['range_start']
    if (r.get('status') != 'verified_ctrl_r2_elapsed_pending_outer_seal' or r.get('source_verified') is not True or
        r.get('state_sha256') != sha(root/'recovery-state.json') or r.get('bytes') != plan['source']['bytes'] or
        r.get('md5') != plan['source']['md5'] or r.get('file') != 'CTRL_R2.fastq.gz' or
        not re.fullmatch('[0-9a-f]{64}', str(r.get('sha256'))) or r.get('clock_policy') != plan['clock_policy'] or
        r.get('prior_transfer_elapsed_seconds') != plan['original_audit']['prior_transfer_elapsed_seconds'] or
        r.get('additional_transfer_elapsed_seconds') != elapsed):
        raise ValueError('Incomplete whole-file result')
    if (s['transfer_bytes_consumed'] != expected or r.get('cumulative_body_bytes') != expected or
        r.get('additional_body_bytes') != plan['source']['bytes']-plan['range_start'] or
        tail.get('status') != 'tail_received_not_source_verified' or tail.get('body_bytes') != plan['source']['bytes']-plan['range_start'] or
        tail.get('charged_body_bytes') != expected or tail.get('address_family') != 'IPv4' or
        tail.get('range_start') != plan['range_start'] or tail.get('range_end') != plan['range_end']):
        raise ValueError('Body accounting mismatch')
    out = root/'CTRL_R2.fastq.gz'
    if out.is_symlink() or not out.is_file() or out.stat().st_size != plan['source']['bytes']:
        raise ValueError('Recovered output missing')
    seal = {'status': 'sealed_verified_ctrl_r2_elapsed', 'sha256': {n: sha(root/n) for n in SEALED},
        'file': out.name, 'file_sha256': r['sha256'], 'file_md5': r['md5'], 'file_bytes': r['bytes'],
        'clock_policy': plan['clock_policy'], 'cumulative_body_bytes': expected,
        'manual_browser_reserved_body_bytes': MANUAL_BROWSER_RESERVE, 'manual_browser_exact_body_known': False,
        'remaining_body_budget_bytes': plan['limits']['transfer_bytes']-expected, 'raw_execution_ready': False}
    atomic_json(root/'recovery-seal.json', seal)
    return seal


def execute(path, accepted, accept_window=False):
    if not accept_window:
        raise ValueError('Explicit elapsed-clock 40-minute window acceptance required')
    if not re.fullmatch('[0-9a-f]{64}', accepted or '') or sha(path) != accepted:
        raise ValueError('Exact prepared SHA acceptance required')
    p = read(path)
    root = validate_plan(p)
    if root.exists():
        raise ValueError('Attempted recovery cannot be reused')
    disk_guard(p)
    previous.require_space(p['original_root'])
    root.mkdir(exist_ok=False)
    with (root/'recovery-plan.json').open('xb') as f:
        f.write(Path(path).read_bytes())
        f.flush()
        os.fsync(f.fileno())
    atomic_json(root/'operator-acceptance.json', {'prepared_sha256': accepted, 'accepted_elapsed_clock_window': True, 'accepted_epoch': time.time()})
    record = supervise('run', [sys.executable, str(Path(__file__).resolve()), '--worker', str(root/'recovery-plan.json')],
        root/'supervision', timeout=LIMITS['wall_seconds'], rss_limit=LIMITS['rss_bytes'], address_space=LIMITS['address_space_bytes'],
        checkpoint=monitor(p, tick()))
    return accept_outer(root, p, record)


def worker_file(path):
    p = read(path)
    root = validate_plan(p)
    if Path(path).resolve() != root/'recovery-plan.json':
        raise ValueError('Fixed worker path')
    a = read(root/'operator-acceptance.json')
    if a.get('prepared_sha256') != sha(path) or a.get('accepted_elapsed_clock_window') is not True:
        raise ValueError('Missing worker acceptance')
    receipt = root/'supervision/run.json'
    outer = read(receipt)
    until = time.monotonic()+2
    while outer.get('status') == 'started' and 'procfs_group' not in outer and time.monotonic() < until:
        time.sleep(.01)
        outer = read(receipt)
    if outer.get('status') != 'started' or outer.get('procfs_group') != proc_info(int(os.readlink('/proc/self')))['group']:
        raise ValueError('Active supervisor required')
    recover(Budget(p))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--prepare', type=Path)
    g.add_argument('--execute', type=Path)
    g.add_argument('--worker', type=Path, help=argparse.SUPPRESS)
    p.add_argument('--original', type=Path)
    p.add_argument('--accept-plan-sha256')
    p.add_argument('--accept-elapsed-clock-window', action='store_true')
    a = p.parse_args()
    if a.prepare:
        if not a.original:
            p.error('--original required')
        plan = prepare(a.original)
        with a.prepare.open('x') as f:
            json.dump(plan, f, indent=2)
            f.write('\n')
        print(json.dumps({'prepared_file': str(a.prepare), 'sha256': sha(a.prepare), 'execution_enabled': False,
            'root': plan['root'], 'remaining_read_body_bytes': SOURCE['bytes']-PARTIAL_BYTES,
            'prior_charged_body_bytes': CHARGED, 'expected_cumulative_body_bytes_after_recovery': CHARGED+SOURCE['bytes']-PARTIAL_BYTES,
            'new_wall_seconds': LIMITS['wall_seconds'], 'additional_transfer_seconds': LIMITS['transfer_seconds'],
            'clock': 'CLOCK_BOOTTIME', 'proposed_disk_gib': 27, 'scope': SCOPE, 'raw_execution_ready': False}, indent=2))
    elif a.execute:
        print(json.dumps(execute(a.execute, a.accept_plan_sha256, a.accept_elapsed_clock_window), indent=2))
    else:
        worker_file(a.worker)


if __name__ == '__main__':
    main()
