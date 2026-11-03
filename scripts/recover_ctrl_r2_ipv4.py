"""New IPv4-only CTRL_R2 recovery after a zero-body TLS handshake timeout.

--prepare only audits local files. HTTPS hostname/certificate checks remain on.
Historical attempts are immutable. Exact SHA and new-window acceptance required.
"""
import argparse
import http.client
import json
import math
import os
from pathlib import Path
import re
import shutil
import socket
import ssl
import sys
import time
import urllib.request

import recover_ctrl_r2 as previous
import recover_ctrl_read as transport
from bounded_http_transport import NoRedirect, read_reserved_blocks
from process_supervisor_v2 import atomic_json, supervise, proc_info
from workflow_seal import read, sha, check_outer
from pilot_execution_policy import iter_files

GiB = 1024**3
CHARGED = previous.CHARGED
PARTIAL_BYTES = previous.PARTIAL_BYTES
SOURCE = previous.SOURCE
LIMITS = dict(previous.LIMITS)
FIRST_PLAN_SHA = '532778b69d5511020cdbc9198d4961e6b7be69e0adb8b78edd33163835657c71'
META = ('recovery-plan.json', 'operator-acceptance.json', 'recovery-state.json',
        'range-attempt.json', 'supervision/run.json', 'supervision/run.log')
SEALED = previous.SEALED
CODE = tuple(sorted(set(previous.CODE + ('recover_ctrl_r2_ipv4.py',))))
SCOPE = 'recover CTRL_R2 only over verified HTTPS/IPv4; no other mates, decompression, alignment or pilot restart'
TIME_REVIEW = 'NEW6000s total/5400s HTTP; failed TLS attempt time and all body charges retained; disk27GiB unchanged'


def identity():
    return {'python_sha256': transport.base.file_hash(sys.executable)['sha256'],
            'code_sha256': {n: transport.base.file_hash(Path(__file__).with_name(n))['sha256'] for n in CODE}}


def recovery_root(original):
    return Path(original).with_name(Path(original).name + '-ipv4-01')


def inspect(original, guard=lambda: None):
    original = Path(original).resolve()
    if any((original/n).is_symlink() for n in META):
        raise ValueError('Historical metadata symlink')
    hashes = {n: sha(original/n) for n in META}
    if hashes['recovery-plan.json'] != FIRST_PLAN_SHA:
        raise ValueError('Exact failed accepted recovery required')
    plan = read(original/'recovery-plan.json')
    if previous.validate_plan(plan) != original:
        raise ValueError('Failed recovery root changed')
    audit = previous.inspect(plan['original_root'], guard)
    if audit != plan['original_audit']:
        raise ValueError('Original pilot changed')
    accept = read(original/'operator-acceptance.json')
    outer = read(original/'supervision/run.json')
    state = read(original/'recovery-state.json')
    attempt = read(original/'range-attempt.json')
    if (accept.get('prepared_sha256') != FIRST_PLAN_SHA or
        accept.get('accepted_additional_time_window') is not True or
        outer.get('status') != 'finished' or outer.get('exit_code') != 1 or
        outer.get('violation') is not None or outer.get('supervisor_error') is not None or
        outer.get('live_group_members_after_cleanup') != []):
        raise ValueError('Failed stopped recovery/acceptance required')
    if (state.get('status') != 'failed' or state.get('error_type') != 'URLError' or
        state.get('limits') != previous.LIMITS or state.get('transfer_bytes_consumed') != CHARGED or
        state.get('prior_transfer_elapsed_seconds') != previous.CARRIED_SECONDS or
        state.get('original_deadline_epoch') != audit['prior_global_deadline_epoch'] or
        set(state.get('phases', {})) != {'copy', 'range'}):
        raise ValueError('Exact zero-body failed recovery required')
    copy, phase = state['phases']['copy'], state['phases']['range']
    if (copy.get('status') != 'verified' or phase.get('status') != 'failed' or
        phase.get('error_type') != 'URLError' or 'unsettled_body_reservation_bytes' in phase):
        raise ValueError('No body reservation may have started')
    for p, cap in ((copy, LIMITS['copy_seconds']), (phase, LIMITS['transfer_seconds'])):
        elapsed = p['finished_epoch'] - p['started_epoch']
        if not math.isfinite(elapsed) or not 0 <= elapsed < cap:
            raise ValueError('Historical phase clock invalid')
    elapsed = phase['finished_epoch'] - phase['started_epoch']
    if (attempt.get('status') != 'failed' or attempt.get('error_type') != 'URLError' or
        attempt.get('body_bytes') != 0 or attempt.get('attempts') != 1 or
        attempt.get('prior_charged_bytes') != CHARGED or attempt.get('range_start') != PARTIAL_BYTES or
        attempt.get('range_end') != SOURCE['bytes']-1):
        raise ValueError('Failed request must have received zero body bytes')
    log = (original/'supervision/run.log').read_text()
    if 'The handshake operation timed out' not in log:
        raise ValueError('TLS handshake timeout evidence required')
    if (original/'recovery-result.json').exists() or (original/'recovery-seal.json').exists():
        raise ValueError('No failed attempt may have a successful result')
    partial = original/'recovered-CTRL_R2.partial'
    if partial.is_symlink() or partial.stat().st_size != PARTIAL_BYTES:
        raise ValueError('Copied prefix size changed')
    actual = transport.base.file_hash(partial, guard)
    if actual != {'bytes': audit['partial_bytes'], 'sha256': audit['partial_sha256']}:
        raise ValueError('Copied prefix differs from audited original')
    if hashes != {n: sha(original/n) for n in META}:
        raise ValueError('Failed recovery changed during audit')
    return {'root': str(original), 'metadata_sha256': hashes,
            'partial_bytes': actual['bytes'], 'partial_sha256': actual['sha256'],
            'charged_body_bytes': CHARGED,
            'prior_transfer_elapsed_seconds': previous.CARRIED_SECONDS+elapsed,
            'previous_transfer_elapsed_seconds': previous.CARRIED_SECONDS,
            'failed_tls_transfer_elapsed_seconds': elapsed,
            'prior_global_deadline_epoch': state['deadline_epoch'],
            'pilot_audit': audit}


def require_space(original):
    previous.require_space(original)


def prepare(original):
    original = Path(original).expanduser().resolve()
    root = recovery_root(original)
    if root.exists():
        raise ValueError('Exclusive IPv4 root exists; no retry')
    obs = inspect(original)
    require_space(original)
    return {'schema': 'ctrl-r2-ipv4-only-range-recovery-v1', 'execution_enabled': False,
            'original_root': str(original), 'root': str(root), 'original_audit': obs,
            'source': dict(SOURCE), 'limits': dict(LIMITS), 'identity': identity(),
            'range_start': obs['partial_bytes'], 'range_end': SOURCE['bytes']-1,
            'scope': SCOPE, 'time_review': TIME_REVIEW, 'address_family': 'IPv4'}


def validate_plan(plan):
    keys = {'schema', 'execution_enabled', 'original_root', 'root', 'original_audit', 'source',
            'limits', 'identity', 'range_start', 'range_end', 'scope', 'time_review', 'address_family'}
    if (not isinstance(plan, dict) or set(plan) != keys or
        plan['schema'] != 'ctrl-r2-ipv4-only-range-recovery-v1' or plan['execution_enabled'] is not False):
        raise ValueError('Disabled fixed IPv4 recovery required')
    original, root, obs = Path(plan['original_root']), Path(plan['root']), plan['original_audit']
    if (not original.is_absolute() or original != original.resolve() or root != recovery_root(original) or
        root != root.resolve() or obs['root'] != str(original)):
        raise ValueError('Exclusive canonical lineage required')
    if (plan['source'] != SOURCE or plan['limits'] != LIMITS or plan['identity'] != identity() or
        plan['scope'] != SCOPE or plan['time_review'] != TIME_REVIEW or plan['address_family'] != 'IPv4'):
        raise ValueError('Fixed IPv4 source/resources/code changed')
    if (type(plan['range_start']) is not int or plan['range_start'] != PARTIAL_BYTES or
        obs['partial_bytes'] != PARTIAL_BYTES or plan['range_end'] != SOURCE['bytes']-1 or
        not re.fullmatch('[0-9a-f]{64}', str(obs['partial_sha256']))):
        raise ValueError('Exact copied prefix required')
    seconds = obs['failed_tls_transfer_elapsed_seconds']
    if (not math.isfinite(seconds) or not 0 <= seconds < LIMITS['transfer_seconds'] or
        obs['charged_body_bytes'] != CHARGED or obs['previous_transfer_elapsed_seconds'] != previous.CARRIED_SECONDS or
        obs['prior_transfer_elapsed_seconds'] != previous.CARRIED_SECONDS+seconds or
        not math.isfinite(obs['prior_global_deadline_epoch'])):
        raise ValueError('Historical body/time cannot be refunded')
    if CHARGED+SOURCE['bytes']-PARTIAL_BYTES > LIMITS['transfer_bytes']:
        raise ValueError('Cumulative body cap')
    return root


def disk_guard(plan):
    a = plan['original_audit']['pilot_audit']
    b = a['read_binding']
    index = b['index']
    roots = [index[k] for k in ('original_root', 'recovery_root', 'index_root')]
    roots += [b['original_root'], b['root'], a['root'], plan['original_root'], plan['root']]
    if len(set(roots)) != 8:
        raise ValueError('Eight distinct lineage roots required')
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
        raise RuntimeError('Eight-tree disk cap/reserve')


def connect_ipv4(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
    """One AF_INET TCP candidate; retain the hostname in HTTPSConnection for TLS."""
    host, port = address
    family, kind, protocol, _, endpoint = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)[0]
    if family != socket.AF_INET:
        raise ValueError('IPv4 resolver contract')
    sock = socket.socket(family, kind, protocol)
    try:
        if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
            sock.settimeout(timeout)
        if source_address:
            sock.bind(source_address)
        sock.connect(endpoint)
        return sock
    except BaseException:
        sock.close()
        raise


class IPv4HTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_connection = connect_ipv4


class IPv4HTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(IPv4HTTPSConnection, req, context=self._context)


def ipv4_opener(context=None):
    context = context if context is not None else ssl.create_default_context()
    if context.verify_mode != ssl.CERT_REQUIRED or not context.check_hostname:
        raise ValueError('TLS certificate and hostname checks required')
    return urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect(), IPv4HTTPSHandler(context=context))


def range_append(budget, target, source, start):
    remaining = source['bytes']-start
    phase = budget.state['phases']['range']
    if remaining <= 0 or remaining > budget.state['limits']['transfer_bytes']-budget.state['transfer_bytes_consumed']:
        raise ValueError('Remaining range exceeds body cap')
    if Path(target).is_symlink() or Path(target).stat().st_size != start:
        raise ValueError('Exact copied prefix required')
    request = urllib.request.Request(source['url'], headers={'Accept-Encoding': 'identity', 'Range': f"bytes={start}-{source['bytes']-1}"})
    receipt = budget.root/'range-attempt.json'
    rec = {'status': 'started', 'body_bytes': 0, 'range_start': start, 'range_end': source['bytes']-1,
           'prior_charged_bytes': budget.state['transfer_bytes_consumed'], 'attempts': 1,
           'address_family': 'IPv4', 'budget_scope': 'HTTP entity-body read, not wire bytes'}
    atomic_json(receipt, rec)
    try:
        with ipv4_opener().open(request, timeout=min(budget.plan['limits']['socket_seconds'], budget.remaining())) as response:
            def single(name, value):
                if response.headers.get_all(name) != [value]:
                    raise ValueError('Recovery response '+name+' mismatch')
            if response.status != 206:
                raise ValueError('HTTP206 required')
            single('Content-Length', str(remaining))
            single('Content-Range', f"bytes {start}-{source['bytes']-1}/{source['bytes']}")
            if (response.headers.get('Content-Encoding', 'identity') != 'identity' or
                response.headers.get('Transfer-Encoding') or response.headers.get('Content-Type', '').lower().startswith('multipart/')):
                raise ValueError('Encoded/chunked/multipart response refused')
            with Path(target).open('ab') as out:
                read_reserved_blocks(budget, phase, response, out, receipt, rec, {'bytes': remaining}, 65536, 4194304)
                out.flush()
                os.fsync(out.fileno())
        budget.guard()
        if rec['body_bytes'] != remaining or Path(target).stat().st_size != source['bytes']:
            raise ValueError('Tail/file size mismatch')
        rec.update(status='tail_received_not_source_verified', charged_body_bytes=budget.state['transfer_bytes_consumed'])
        atomic_json(receipt, rec)
    except BaseException as exc:
        rec.update(status='failed', error_type=type(exc).__name__)
        atomic_json(receipt, rec)
        raise


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
        result.get('status') != 'verified_ctrl_r2_ipv4_pending_outer_seal' or result.get('source_verified') is not True or
        result.get('state_sha256') != sha(root/'recovery-state.json') or result.get('file') != 'CTRL_R2.fastq.gz' or
        result.get('bytes') != SOURCE['bytes'] or result.get('md5') != SOURCE['md5'] or
        not re.fullmatch('[0-9a-f]{64}', str(result.get('sha256', ''))) or
        result.get('prior_transfer_elapsed_seconds') != plan['original_audit']['prior_transfer_elapsed_seconds'] or
        result.get('additional_transfer_elapsed_seconds') != elapsed):
        raise ValueError('Incomplete whole-file result/clocks')
    if (state['transfer_bytes_consumed'] != expected or result.get('cumulative_body_bytes') != expected or
        result.get('additional_body_bytes') != SOURCE['bytes']-plan['range_start'] or
        tail.get('address_family') != 'IPv4' or tail.get('status') != 'tail_received_not_source_verified' or tail.get('body_bytes') != SOURCE['bytes']-plan['range_start'] or
        tail.get('charged_body_bytes') != expected or tail.get('range_start') != plan['range_start'] or tail.get('range_end') != plan['range_end']):
        raise ValueError('Body accounting mismatch')
    out = root/'CTRL_R2.fastq.gz'
    if out.is_symlink() or not out.is_file() or out.stat().st_size != SOURCE['bytes']:
        raise ValueError('Recovered output missing')
    seal = {'status': 'sealed_verified_ctrl_r2_ipv4', 'sha256': {n: sha(root/n) for n in SEALED},
            'address_family': 'IPv4', 'file': out.name, 'file_sha256': result['sha256'], 'file_md5': result['md5'],
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
              'proposed_disk_gib': 27, 'address_family': 'IPv4', 'prior_transfer_seconds_carried_conservatively': plan['original_audit']['prior_transfer_elapsed_seconds'],
              'raw_execution_ready': False}, indent=2))
    elif a.execute:
        print(json.dumps(execute(a.execute, a.accept_plan_sha256, a.accept_additional_time_window), indent=2))
    else:
        worker_file(a.worker)


if __name__ == '__main__':
    main()
