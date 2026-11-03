"""Explicit IPv4 recovery of the remaining 97174406 bytes after operator interruption of CTRL_R2.

Offline preparation only by default. Prior attempts, charges and clocks remain
immutable. Exact SHA and an additional 40-minute window are required to execute.
"""
import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
import time

import recover_ctrl_r2_final as previous
import recover_ctrl_read as transport
from process_supervisor_v2 import atomic_json, supervise, proc_info
from workflow_seal import read, sha
from pilot_execution_policy import iter_files

GiB = 1024**3
WSL_CHARGED = 6224513473
MANUAL_BROWSER_RESERVE = 997549457
CHARGED = WSL_CHARGED + MANUAL_BROWSER_RESERVE
PARTIAL_BYTES = 900375051
SOURCE = previous.SOURCE
LIMITS = {**previous.LIMITS, 'wall_seconds': 2400, 'transfer_seconds': 1800}
PRIOR_PLAN_SHA = 'cbf56db777078a172be126d8b957477815da70df856df79c0aeca631361f66b8'
META = previous.META
CODE = tuple(sorted(set(previous.CODE + ('recover_ctrl_r2_resume.py',))))
SCOPE = 'resume interrupted CTRL_R2 range only over verified HTTPS/IPv4; no other mates, decompression, alignment or pilot restart'
TIME_REVIEW = 'NEW2400s total/1800s HTTP; prior interrupted 1800s window carried conservatively; one full-file browser reserve; disk27GiB unchanged'
range_append = previous.range_append


def identity():
    return {'python_sha256': transport.base.file_hash(sys.executable)['sha256'],
            'code_sha256': {n: transport.base.file_hash(Path(__file__).with_name(n))['sha256'] for n in CODE}}


def recovery_root(original):
    return Path(original).with_name(Path(original).name + '-resume-01')


def inspect(original, guard=lambda: None):
    original = Path(original).resolve()
    if any((original/n).is_symlink() for n in META):
        raise ValueError('Historical metadata symlink')
    hashes = {n: sha(original/n) for n in META}
    if hashes['recovery-plan.json'] != PRIOR_PLAN_SHA:
        raise ValueError('Exact accepted interrupted recovery required')
    plan = read(original/'recovery-plan.json')
    if previous.validate_plan(plan) != original:
        raise ValueError('Interrupted recovery root changed')
    audit = previous.inspect(plan['original_root'], guard)
    if audit != plan['original_audit']:
        raise ValueError('Previous IPv4 lineage changed')
    accept, outer, state, attempt = (read(original/n) for n in
        ('operator-acceptance.json', 'supervision/run.json', 'recovery-state.json', 'range-attempt.json'))
    if (accept.get('prepared_sha256') != PRIOR_PLAN_SHA or accept.get('accepted_additional_time_window') is not True or
        outer.get('status') != 'finished' or outer.get('exit_code') != -9 or
        outer.get('supervisor_error') != 'KeyboardInterrupt: ' or
        outer.get('violation') is not None or outer.get('live_group_members_after_cleanup') != []):
        raise ValueError('Stopped exhausted IPv4 worker/acceptance required')
    if (state.get('status') != 'started' or state.get('limits') != previous.LIMITS or
        state.get('transfer_bytes_consumed') != WSL_CHARGED or
        state.get('prior_transfer_elapsed_seconds') != audit['prior_transfer_elapsed_seconds'] or
        state.get('prior_transfer_elapsed_seconds') != 12700.072928190231 or
        state.get('original_deadline_epoch') != audit['prior_global_deadline_epoch'] or
        state.get('deadline_epoch') != 1793707865.1037116 or
        set(state.get('phases', {})) != {'copy', 'range'}):
        raise ValueError('Exact exhausted state/counters required')
    copied, phase = state['phases']['copy'], state['phases']['range']
    if (copied.get('status') != 'verified' or phase.get('status') != 'started' or 'finished_epoch' in phase or
        phase.get('started_epoch') != 1793705473.6378129 or phase.get('deadline_epoch') != 1793707273.6378129 or
        phase.get('reservation_start_body_bytes') != 20971520 or
        phase.get('unsettled_body_reservation_bytes') != 4194304):
        raise ValueError('Exact interrupted range/reservation required')
    if (attempt.get('status') != 'started' or attempt.get('body_bytes') != 20971520 or
        attempt.get('range_start') != previous.PARTIAL_BYTES or attempt.get('range_end') != SOURCE['bytes']-1 or
        attempt.get('prior_charged_bytes') != previous.CHARGED or attempt.get('attempts') != 1 or
        attempt.get('address_family') != 'IPv4' or attempt.get('accounting') != 'durable-block-reservation-v1' or
        attempt.get('reservation_block_bytes') != 4194304):
        raise ValueError('Interrupted IPv4 request receipt changed')
    if WSL_CHARGED != previous.CHARGED+attempt['body_bytes']+4194304:
        raise ValueError('Conservative body accounting changed')
    partial = original/'recovered-CTRL_R2.partial'
    durable = attempt['range_start']+attempt['body_bytes']
    if not durable <= PARTIAL_BYTES <= durable+4194304:
        raise ValueError('Partial outside reserved block')
    if partial.is_symlink() or partial.stat().st_size != PARTIAL_BYTES:
        raise ValueError('Exact final partial size required')
    if (original/'recovery-result.json').exists() or (original/'recovery-seal.json').exists():
        raise ValueError('Interrupted attempt must not have a successful result')
    actual = transport.base.file_hash(partial, guard)
    if actual['bytes'] != PARTIAL_BYTES or hashes != {n: sha(original/n) for n in META}:
        raise ValueError('Partial/metadata changed during audit')
    return {'root': str(original), 'metadata_sha256': hashes,
            'partial_bytes': actual['bytes'], 'partial_sha256': actual['sha256'],
            'charged_body_bytes': CHARGED,
            'prior_transfer_elapsed_seconds': audit['prior_transfer_elapsed_seconds']+1800,
            'previous_transfer_elapsed_seconds': audit['prior_transfer_elapsed_seconds'],
            'interrupted_transfer_window_seconds_reserved': 1800,
            'prior_global_deadline_epoch': state['deadline_epoch'], 'previous_audit': audit,
            'clock_accounting': 'full interrupted 1800s window reserved conservatively, not measured elapsed',
            'prior_wsl_charged_bytes': WSL_CHARGED,
            'manual_browser_reserved_body_bytes': MANUAL_BROWSER_RESERVE,
            'manual_browser_reported_mb': 74,
            'manual_browser_exact_body_known': False,
            'reserved_minus_actual_body_bytes': WSL_CHARGED-previous.CHARGED-(PARTIAL_BYTES-previous.PARTIAL_BYTES)}


def require_space(original):
    previous.require_space(original)


def prepare(original):
    original = Path(original).expanduser().resolve()
    root = recovery_root(original)
    if root.exists():
        raise ValueError('Exclusive final root exists; no retry')
    obs = inspect(original)
    require_space(original)
    return {'schema': 'ctrl-r2-interrupted-resume-v1', 'execution_enabled': False,
            'original_root': str(original), 'root': str(root), 'original_audit': obs,
            'source': dict(SOURCE), 'limits': dict(LIMITS), 'identity': identity(),
            'range_start': obs['partial_bytes'], 'range_end': SOURCE['bytes']-1,
            'scope': SCOPE, 'time_review': TIME_REVIEW, 'address_family': 'IPv4'}


def validate_plan(plan):
    keys = {'schema', 'execution_enabled', 'original_root', 'root', 'original_audit', 'source',
            'limits', 'identity', 'range_start', 'range_end', 'scope', 'time_review', 'address_family'}
    if (not isinstance(plan, dict) or set(plan) != keys or plan['schema'] != 'ctrl-r2-interrupted-resume-v1' or
        plan['execution_enabled'] is not False):
        raise ValueError('Disabled fixed final IPv4 recovery required')
    original, root, obs = Path(plan['original_root']), Path(plan['root']), plan['original_audit']
    if (not original.is_absolute() or original != original.resolve() or root != recovery_root(original) or
        root != root.resolve() or obs['root'] != str(original)):
        raise ValueError('Exclusive canonical lineage required')
    if (plan['source'] != SOURCE or plan['limits'] != LIMITS or plan['identity'] != identity() or
        plan['scope'] != SCOPE or plan['time_review'] != TIME_REVIEW or plan['address_family'] != 'IPv4'):
        raise ValueError('Fixed source/IPv4/resources/code changed')
    if (type(plan['range_start']) is not int or plan['range_start'] != PARTIAL_BYTES or
        obs['partial_bytes'] != PARTIAL_BYTES or plan['range_end'] != SOURCE['bytes']-1 or
        not re.fullmatch('[0-9a-f]{64}', str(obs['partial_sha256']))):
        raise ValueError('Exact final prefix required')
    if (obs['charged_body_bytes'] != CHARGED or obs['prior_wsl_charged_bytes'] != WSL_CHARGED or obs['manual_browser_reserved_body_bytes'] != MANUAL_BROWSER_RESERVE or obs['manual_browser_exact_body_known'] is not False or obs['previous_transfer_elapsed_seconds'] != 12700.072928190231 or
        obs['interrupted_transfer_window_seconds_reserved'] != 1800 or
        obs['prior_transfer_elapsed_seconds'] != 14500.072928190231 or
        obs['prior_global_deadline_epoch'] != 1793707865.1037116 or
        CHARGED+SOURCE['bytes']-PARTIAL_BYTES > LIMITS['transfer_bytes']):
        raise ValueError('Prior charges/clocks cannot be refunded')
    return root


def disk_guard(plan):
    ipv4 = plan['original_audit']['previous_audit']
    tls = ipv4['ipv4_audit']
    a = tls['pilot_audit']
    b = a['read_binding']
    index = b['index']
    roots = [index[k] for k in ('original_root', 'recovery_root', 'index_root')]
    roots += [b['original_root'], b['root'], a['root'], tls['root'], ipv4['root'], plan['original_root'], plan['root']]
    if len(set(roots)) != 10:
        raise ValueError('Ten distinct lineage roots required')
    total = 0
    for root in roots:
        for path in iter_files(root):
            try:
                if path.is_symlink():
                    raise ValueError('Lineage symlink')
                if path.is_file():
                    total += path.stat().st_size
            except FileNotFoundError:
                pass
    if total > plan['limits']['disk_bytes'] or shutil.disk_usage(plan['original_root']).free < plan['limits']['reserve_bytes']:
        raise RuntimeError('Ten-tree disk cap/reserve')


class Budget(transport.base.Budget):
    def guard(self):
        now = self.clock()
        if not math.isfinite(now) or now < self.state['last_epoch'] or now >= self.state['deadline_epoch']:
            raise RuntimeError('Recovery clock/deadline')
        self.state['last_epoch'] = now
        if any(p['status'] == 'started' and now >= p['deadline_epoch'] for p in self.state['phases'].values()):
            raise RuntimeError('Recovery phase deadline')
        if not CHARGED <= self.state['transfer_bytes_consumed'] <= self.plan['limits']['transfer_bytes']:
            raise RuntimeError('Cumulative body cap/floor')
        tick = time.monotonic()
        if tick - getattr(self, 'last_disk', float('-inf')) >= .1:
            disk_guard(self.plan)
            self.last_disk = tick


def recover(budget):
    p, root = budget.plan, budget.root
    target = root/'recovered-CTRL_R2.partial'
    try:
        budget.begin('copy')
        if inspect(p['original_root'], budget.guard) != p['original_audit']:
            raise ValueError('Original changed')
        transport.base.copy_prefix(Path(p['original_root'])/'recovered-CTRL_R2.partial', target,
                                   {'bytes': p['range_start'], 'sha256': p['original_audit']['partial_sha256']}, budget.guard)
        budget.finish('copy')
        budget.begin('range')
        range_append(budget, target, p['source'], p['range_start'])
        budget.finish('range')
        budget.begin('verify')
        actual = transport.whole_hash(target, budget.guard)
        if actual['bytes'] != p['source']['bytes'] or actual['md5'] != p['source']['md5']:
            raise ValueError('Whole recovered FASTQ MD5/size mismatch')
        if inspect(p['original_root'], budget.guard) != p['original_audit']:
            raise ValueError('Original changed during recovery')
        budget.guard()
        os.replace(target, root/'CTRL_R2.fastq.gz')
        directory = os.open(root, os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        budget.finish('verify')
        budget.state['status'] = 'verified'
        budget.save()
        atomic_json(root/'recovery-result.json', {
            'status': 'verified_ctrl_r2_ipv4_pending_outer_seal', 'file': 'CTRL_R2.fastq.gz', **actual,
            'state_sha256': sha(root/'recovery-state.json'),
            'cumulative_body_bytes': budget.state['transfer_bytes_consumed'],
            'additional_body_bytes': budget.state['transfer_bytes_consumed']-p['original_audit']['charged_body_bytes'],
            'prior_transfer_elapsed_seconds': p['original_audit']['prior_transfer_elapsed_seconds'],
            'additional_transfer_elapsed_seconds': budget.state['phases']['range']['finished_epoch']-budget.state['phases']['range']['started_epoch'],
            'source_verified': True, 'raw_execution_ready': False})
    except BaseException as exc:
        for phase in budget.state['phases'].values():
            if phase['status'] == 'started':
                phase.update(status='failed', error_type=type(exc).__name__, finished_epoch=budget.clock())
        budget.state.update(status='failed', error_type=type(exc).__name__)
        budget.save()
        raise


def monitor(plan, start):
    last_disk = [float('-inf')]
    def guard():
        if time.monotonic()-start >= plan['limits']['wall_seconds']:
            raise RuntimeError('External monotonic total cap')
        path = Path(plan['root'])/'recovery-state.json'
        if path.exists():
            state = read(path)
            if (state.get('limits') != plan['limits'] or
                state.get('prior_transfer_elapsed_seconds') != plan['original_audit']['prior_transfer_elapsed_seconds'] or
                state.get('original_deadline_epoch') != plan['original_audit']['prior_global_deadline_epoch']):
                raise RuntimeError('External historical accounting changed')
            now = time.time()
            if now < state['last_epoch'] or now >= state['deadline_epoch'] or not CHARGED <= state['transfer_bytes_consumed'] <= LIMITS['transfer_bytes']:
                raise RuntimeError('External clock/body cap')
            for name, phase in state['phases'].items():
                cap = plan['limits'][{'copy': 'copy_seconds', 'range': 'transfer_seconds', 'verify': 'verify_seconds'}[name]]
                if phase['status'] == 'started' and now >= min(phase['deadline_epoch'], phase['started_epoch']+cap):
                    raise RuntimeError('External phase deadline')
        tick = time.monotonic()
        if tick - last_disk[0] >= .1:
            disk_guard(plan)
            last_disk[0] = tick
    return guard


def accept_outer(root, plan, record):
    acceptance = read(Path(root)/'operator-acceptance.json')
    if acceptance.get('browser_stopped_and_manual_reserve_accepted') is not True:
        raise ValueError('Manual browser reserve/stop acceptance missing')
    seal = previous.accept_outer(root, plan, record)
    seal.update(prior_wsl_charged_body_bytes=WSL_CHARGED,
                manual_browser_reserved_body_bytes=MANUAL_BROWSER_RESERVE,
                manual_browser_exact_body_known=False)
    atomic_json(Path(root)/'recovery-seal.json', seal)
    return seal


def execute(path, accepted, accept_time=False, browser_stopped=False):
    if not browser_stopped:
        raise ValueError('Stop browser download and explicitly acknowledge manual reserve')
    if not accept_time:
        raise ValueError('Explicit additional 40-minute window acceptance required')
    if not re.fullmatch('[0-9a-f]{64}', accepted or '') or sha(path) != accepted:
        raise ValueError('Exact prepared SHA acceptance required')
    plan = read(path)
    root = validate_plan(plan)
    if root.exists():
        raise ValueError('Attempted recovery cannot be reused')
    disk_guard(plan)
    require_space(plan['original_root'])
    root.mkdir(exist_ok=False)
    with (root/'recovery-plan.json').open('xb') as f:
        f.write(Path(path).read_bytes())
        f.flush()
        os.fsync(f.fileno())
    atomic_json(root/'operator-acceptance.json', {'prepared_sha256': accepted,
                'accepted_additional_time_window': True, 'browser_stopped_and_manual_reserve_accepted': True, 'accepted_epoch': time.time()})
    rec = supervise('run', [sys.executable, str(Path(__file__).resolve()), '--worker', str(root/'recovery-plan.json')],
                    root/'supervision', timeout=LIMITS['wall_seconds'], rss_limit=LIMITS['rss_bytes'],
                    address_space=LIMITS['address_space_bytes'], checkpoint=monitor(plan, time.monotonic()))
    return accept_outer(root, plan, rec)


def worker_file(path):
    plan = read(path)
    root = validate_plan(plan)
    if Path(path).resolve() != root/'recovery-plan.json':
        raise ValueError('Fixed worker path')
    a = read(root/'operator-acceptance.json')
    if a.get('prepared_sha256') != sha(path) or a.get('accepted_additional_time_window') is not True or a.get('browser_stopped_and_manual_reserve_accepted') is not True:
        raise ValueError('Missing worker acceptance')
    receipt = root/'supervision/run.json'
    outer = read(receipt)
    until = time.monotonic()+2
    while outer.get('status') == 'started' and 'procfs_group' not in outer and time.monotonic() < until:
        time.sleep(.01)
        outer = read(receipt)
    if outer.get('status') != 'started' or outer.get('procfs_group') != proc_info(int(os.readlink('/proc/self')))['group']:
        raise ValueError('Active supervisor required')
    recover(Budget(plan))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--prepare', type=Path)
    g.add_argument('--execute', type=Path)
    g.add_argument('--worker', type=Path, help=argparse.SUPPRESS)
    p.add_argument('--original', type=Path)
    p.add_argument('--accept-plan-sha256')
    p.add_argument('--accept-additional-time-window', action='store_true')
    p.add_argument('--accept-browser-stopped-and-manual-reserve', action='store_true')
    a = p.parse_args()
    if a.prepare:
        if not a.original:
            p.error('--original required')
        plan = prepare(a.original)
        with a.prepare.open('x') as f:
            json.dump(plan, f, indent=2)
            f.write('\n')
        remaining = SOURCE['bytes']-plan['range_start']
        print(json.dumps({'prepared_file': str(a.prepare), 'sha256': sha(a.prepare), 'execution_enabled': False,
              'root': plan['root'], 'scope': SCOPE, 'remaining_read_body_bytes': remaining,
              'prior_charged_body_bytes': CHARGED, 'prior_wsl_charged_body_bytes': WSL_CHARGED, 'manual_browser_reserved_body_bytes': MANUAL_BROWSER_RESERVE, 'expected_cumulative_body_bytes_after_recovery': CHARGED+remaining,
              'additional_transfer_seconds': LIMITS['transfer_seconds'], 'new_wall_seconds': LIMITS['wall_seconds'],
              'proposed_disk_gib': 27, 'address_family': 'IPv4', 'prior_transfer_seconds_carried_conservatively': plan['original_audit']['prior_transfer_elapsed_seconds'],
              'raw_execution_ready': False}, indent=2))
    elif a.execute:
        print(json.dumps(execute(a.execute, a.accept_plan_sha256, a.accept_additional_time_window, a.accept_browser_stopped_and_manual_reserve), indent=2))
    else:
        worker_file(a.worker)


if __name__ == '__main__':
    main()
