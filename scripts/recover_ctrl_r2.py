"""Recover only the interrupted CTRL_R2. Preparation is offline and disabled.

Never reopen the failed pilot. Exact SHA and an additional 100-minute window
are required; 90 minutes are reserved for one HTTP Range request. No alignment.
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

import recovered_read_pilot as pilot
import recover_ctrl_read as transport
from process_supervisor_v2 import atomic_json, supervise, proc_info
from workflow_seal import read, sha, check_outer
from pilot_execution_policy import iter_files

GiB = 1024**3
JOB_SHA = '1a982933968c1d808c9e0e6e0fdc274548ad1f694275288868147c10e7b4887a'
FINGERPRINT = 'a9e12dd04196340d726c6777a1ce53e60516be85bcce55cfe4f805c8e70a917e'
PARTIAL_BYTES = 284799727
CHARGED = 5603756481
SNAPSHOT_SECONDS = 1773.5246675014496
PRIOR_SECONDS = 5467.721008300781
# The parent reached the 1800s cap after the last durable snapshot. Carry the
# whole authorized window conservatively; do not call the stale 1773s final.
CARRIED_SECONDS = PRIOR_SECONDS + 1800
SOURCE = {'url': 'https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR334/016/SRR33425816/SRR33425816_2.fastq.gz',
          'bytes': 997549457, 'md5': '007d66223fe35f394284e4ebd631eaef'}
LIMITS = {**transport.LIMITS, 'wall_seconds': 6000, 'transfer_seconds': 5400,
          'disk_bytes': 27*GiB}
META = ('workflow-job.json', 'operator-acceptance.json', 'ledger.json',
        'cached-preflight.json', 'CTRL_R2.attempt-0.json', 'workflow-receipts/run.json')
SEALED = transport.SEALED
CODE = tuple(sorted(set(pilot.CODE + ('recover_ctrl_r2.py',))))
SCOPE = 'recover CTRL_R2 only; no other mates, decompression, alignment or pilot restart'
TIME_REVIEW = 'NEW6000s total/5400s HTTP; historical 1800s window carried conservatively; disk27GiB unchanged'


def identity():
    return {'python_sha256': transport.base.file_hash(sys.executable)['sha256'],
            'code_sha256': {n: transport.base.file_hash(Path(__file__).with_name(n))['sha256'] for n in CODE}}


def recovery_root(original):
    return Path(original).with_name(Path(original).name + '-CTRL_R2-recovery-01')


def inspect(original, guard=lambda: None):
    original = Path(original).resolve()
    if any((original/n).is_symlink() for n in META):
        raise ValueError('Original metadata symlink')
    hashes = {n: sha(original/n) for n in META}
    if hashes['workflow-job.json'] != JOB_SHA:
        raise ValueError('Exact accepted failed pilot required')
    job = read(original/'workflow-job.json')
    if pilot.validate_job(job) != original:
        raise ValueError('Failed pilot root changed')
    accept = read(original/'operator-acceptance.json')
    if accept.get('plan_sha256') != JOB_SHA or accept.get('accepted_new_window_and_disk') is not True:
        raise ValueError('Original acceptance missing')
    state = read(original/'ledger.json')
    outer = read(original/'workflow-receipts/run.json')
    attempt = read(original/'CTRL_R2.attempt-0.json')
    if (outer.get('status') != 'finished' or outer.get('exit_code') != -9 or
        outer.get('supervisor_error') != 'RuntimeError: Cumulative transfer time cap' or
        outer.get('violation') is not None or outer.get('live_group_members_after_cleanup') != []):
        raise ValueError('Stopped exhausted worker with empty group required')
    phases = state.get('phases', {})
    if set(phases) != {'preflight', 'CTRL_R1', 'CTRL_R2'}:
        raise ValueError('No later processing may have started')
    pre, local, active = (phases[n] for n in ('preflight', 'CTRL_R1', 'CTRL_R2'))
    binding = job['manifest']['recovered_read']
    if (state.get('fingerprint') != FINGERPRINT or state.get('limits') != job['limits'] or
        state.get('mode') != 'real-pilot' or pre.get('status') != 'verified' or
        pre.get('receipt') != 'cached-preflight.json' or pre.get('receipt_sha256') != hashes['cached-preflight.json'] or
        local.get('status') != 'verified' or local.get('local_recovered_source') != binding or
        local.get('new_body_bytes') != 0 or local.get('bytes') != binding['bytes'] or
        local.get('sha256') != pilot.READ_SHA or local.get('md5') != binding['md5']):
        raise ValueError('Verified index/local CTRL_R1 provenance changed')
    if (state.get('transfer_bytes_consumed') != CHARGED or
        state.get('prior_transfer_elapsed_seconds') != PRIOR_SECONDS or
        state.get('transfer_elapsed_seconds') != SNAPSHOT_SECONDS or
        state.get('cumulative_transfer_elapsed_seconds') != 7241.245675802231 or
        state.get('deadline_epoch') != 1793702652.9493718 or
        state.get('prior_deadline_epoch') != binding['prior_deadline_epoch']):
        raise ValueError('Observed charge/clock changed')
    if (active.get('kind') != 'transfer' or active.get('status') != 'started' or
        'finished_epoch' in active or active.get('reservation_start_body_bytes') != 281018368 or
        active.get('unsettled_body_reservation_bytes') != 4194304 or
        attempt.get('status') != 'started' or attempt.get('attempt') != 0 or
        attempt.get('body_bytes') != 281018368 or attempt.get('reservation_block_bytes') != 4194304 or
        attempt.get('accounting') != 'durable-block-reservation-v1'):
        raise ValueError('Exact interrupted reservation required')
    if CHARGED != binding['cumulative_body_bytes'] + 281018368 + 4194304:
        raise ValueError('Reservation charge mismatch')
    step = next(s for s in job['manifest']['sealed_workflow']['steps'] if s['name'] == 'CTRL_R2')
    if step != {'name': 'CTRL_R2', 'kind': 'http', 'url': SOURCE['url'],
                'expected': {'bytes': SOURCE['bytes'], 'md5': SOURCE['md5']}}:
        raise ValueError('Pinned CTRL_R2 source differs')
    partial = original/'CTRL_R2.attempt-0.partial'
    if partial.is_symlink() or partial.stat().st_size != PARTIAL_BYTES:
        raise ValueError('Exact partial size required')
    actual = transport.base.file_hash(partial, guard)
    if actual['bytes'] != PARTIAL_BYTES or hashes != {n: sha(original/n) for n in META}:
        raise ValueError('Original changed during audit')
    return {'root': str(original), 'metadata_sha256': hashes, 'partial_bytes': actual['bytes'],
            'partial_sha256': actual['sha256'], 'charged_body_bytes': CHARGED,
            'prior_transfer_elapsed_seconds': CARRIED_SECONDS,
            'last_snapshot_cumulative_seconds': state['cumulative_transfer_elapsed_seconds'],
            'clock_accounting': 'prior + full exhausted 1800s window; snapshot is not final',
            'prior_global_deadline_epoch': state['deadline_epoch'], 'read_binding': binding}


def prepare(original):
    original = Path(original).expanduser().resolve()
    root = recovery_root(original)
    if root.exists():
        raise ValueError('Attempted recovery root exists; no retry')
    obs = inspect(original)
    require_space(original)
    return {'schema': 'ctrl-r2-only-range-recovery-v1', 'execution_enabled': False,
            'original_root': str(original), 'root': str(root), 'original_audit': obs,
            'source': dict(SOURCE), 'limits': dict(LIMITS), 'identity': identity(),
            'range_start': obs['partial_bytes'], 'range_end': SOURCE['bytes']-1,
            'scope': SCOPE, 'time_review': TIME_REVIEW}


def require_space(original):
    if shutil.disk_usage(original).free < LIMITS['disk_bytes'] + LIMITS['reserve_bytes']:
        raise ValueError('35 GiB free required before recovery')


def validate_plan(plan):
    keys = {'schema', 'execution_enabled', 'original_root', 'root', 'original_audit',
            'source', 'limits', 'identity', 'range_start', 'range_end', 'scope', 'time_review'}
    if (not isinstance(plan, dict) or set(plan) != keys or
        plan['schema'] != 'ctrl-r2-only-range-recovery-v1' or plan['execution_enabled'] is not False):
        raise ValueError('Disabled fixed CTRL_R2 recovery required')
    original, root, obs = Path(plan['original_root']), Path(plan['root']), plan['original_audit']
    if (not original.is_absolute() or original != original.resolve() or
        root != recovery_root(original) or root != root.resolve() or obs['root'] != str(original)):
        raise ValueError('Canonical exclusive recovery lineage required')
    if (plan['source'] != SOURCE or plan['limits'] != LIMITS or plan['identity'] != identity() or
        plan['scope'] != SCOPE or plan['time_review'] != TIME_REVIEW):
        raise ValueError('Fixed source/resources/code changed')
    if (type(plan['range_start']) is not int or plan['range_start'] != PARTIAL_BYTES or
        obs['partial_bytes'] != PARTIAL_BYTES or plan['range_end'] != SOURCE['bytes']-1 or
        not re.fullmatch('[0-9a-f]{64}', str(obs['partial_sha256']))):
        raise ValueError('Exact interrupted partial required')
    if (obs['charged_body_bytes'] != CHARGED or obs['prior_transfer_elapsed_seconds'] != CARRIED_SECONDS or
        obs['prior_global_deadline_epoch'] != 1793702652.9493718 or
        obs['last_snapshot_cumulative_seconds'] != 7241.245675802231):
        raise ValueError('Prior charges/clocks cannot be refunded')
    if CHARGED + SOURCE['bytes'] - PARTIAL_BYTES > LIMITS['transfer_bytes']:
        raise ValueError('Cumulative body cap')
    return root


def disk_guard(plan):
    b = plan['original_audit']['read_binding']
    index = b['index']
    roots = [index[k] for k in ('original_root', 'recovery_root', 'index_root')]
    roots += [b['original_root'], b['root'], plan['original_root'], plan['root']]
    if len(set(roots)) != 7:
        raise ValueError('Seven distinct lineage roots required')
    size = 0
    for root in roots:
        for path in iter_files(root):
            try:
                if path.is_symlink():
                    raise ValueError('Lineage symlink')
                if path.is_file():
                    size += path.stat().st_size
            except FileNotFoundError:
                pass
    if size > plan['limits']['disk_bytes'] or shutil.disk_usage(plan['original_root']).free < plan['limits']['reserve_bytes']:
        raise RuntimeError('Whole lineage disk cap/reserve')


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
        transport.base.copy_prefix(Path(p['original_root'])/'CTRL_R2.attempt-0.partial', target,
                                   {'bytes': p['range_start'], 'sha256': p['original_audit']['partial_sha256']}, budget.guard)
        budget.finish('copy')
        budget.begin('range')
        transport.range_append(budget, target, p['source'], p['range_start'])
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
            'status': 'verified_ctrl_r2_pending_outer_seal', 'file': 'CTRL_R2.fastq.gz', **actual,
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
                state.get('prior_transfer_elapsed_seconds') != CARRIED_SECONDS or
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
    check_outer(record)
    root = Path(root)
    if read(root/'supervision/run.json') != record or read(root/'recovery-plan.json') != plan:
        raise ValueError('Outer receipt/plan changed')
    acceptance = read(root/'operator-acceptance.json')
    if acceptance.get('prepared_sha256') != sha(root/'recovery-plan.json') or acceptance.get('accepted_additional_time_window') is not True:
        raise ValueError('Acceptance missing')
    state, result, tail = (read(root/n) for n in ('recovery-state.json', 'recovery-result.json', 'range-attempt.json'))
    if (state.get('status') != 'verified' or state.get('limits') != plan['limits'] or
        state.get('prior_transfer_elapsed_seconds') != plan['original_audit']['prior_transfer_elapsed_seconds'] or
        state.get('original_deadline_epoch') != plan['original_audit']['prior_global_deadline_epoch'] or
        set(state.get('phases', {})) != {'copy', 'range', 'verify'} or
        any(p.get('status') != 'verified' for p in state['phases'].values())):
        raise ValueError('Incomplete state')
    expected = plan['original_audit']['charged_body_bytes']+plan['source']['bytes']-plan['range_start']
    phase = state['phases']['range']
    elapsed = phase['finished_epoch']-phase['started_epoch']
    if (not 0 <= elapsed < plan['limits']['transfer_seconds'] or
        result.get('status') != 'verified_ctrl_r2_pending_outer_seal' or result.get('source_verified') is not True or
        result.get('state_sha256') != sha(root/'recovery-state.json') or result.get('file') != 'CTRL_R2.fastq.gz' or
        result.get('bytes') != SOURCE['bytes'] or result.get('md5') != SOURCE['md5'] or
        not re.fullmatch('[0-9a-f]{64}', str(result.get('sha256', ''))) or
        result.get('prior_transfer_elapsed_seconds') != plan['original_audit']['prior_transfer_elapsed_seconds'] or
        result.get('additional_transfer_elapsed_seconds') != elapsed):
        raise ValueError('Incomplete whole-file result/clocks')
    if (state['transfer_bytes_consumed'] != expected or result.get('cumulative_body_bytes') != expected or
        result.get('additional_body_bytes') != SOURCE['bytes']-plan['range_start'] or
        tail.get('status') != 'tail_received_not_source_verified' or tail.get('body_bytes') != SOURCE['bytes']-plan['range_start'] or
        tail.get('charged_body_bytes') != expected or tail.get('range_start') != plan['range_start'] or tail.get('range_end') != plan['range_end']):
        raise ValueError('Body accounting mismatch')
    out = root/'CTRL_R2.fastq.gz'
    if out.is_symlink() or not out.is_file() or out.stat().st_size != SOURCE['bytes']:
        raise ValueError('Recovered output missing')
    seal = {'status': 'sealed_verified_ctrl_r2', 'sha256': {n: sha(root/n) for n in SEALED},
            'file': out.name, 'file_sha256': result['sha256'], 'file_md5': result['md5'],
            'file_bytes': result['bytes'], 'cumulative_body_bytes': expected,
            'remaining_body_budget_bytes': LIMITS['transfer_bytes']-expected, 'raw_execution_ready': False}
    atomic_json(root/'recovery-seal.json', seal)
    return seal


def execute(path, accepted, accept_time=False):
    if not accept_time:
        raise ValueError('Explicit additional 100-minute window acceptance required')
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
                'accepted_additional_time_window': True, 'accepted_epoch': time.time()})
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
    if a.get('prepared_sha256') != sha(path) or a.get('accepted_additional_time_window') is not True:
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
              'prior_charged_body_bytes': CHARGED, 'expected_cumulative_body_bytes_after_recovery': CHARGED+remaining,
              'additional_transfer_seconds': LIMITS['transfer_seconds'], 'new_wall_seconds': LIMITS['wall_seconds'],
              'proposed_disk_gib': 27, 'prior_transfer_seconds_carried_conservatively': CARRIED_SECONDS,
              'raw_execution_ready': False}, indent=2))
    elif a.execute:
        print(json.dumps(execute(a.execute, a.accept_plan_sha256, a.accept_additional_time_window), indent=2))
    else:
        worker_file(a.worker)


if __name__ == '__main__':
    main()
