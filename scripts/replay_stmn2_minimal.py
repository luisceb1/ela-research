"""Prepare/replay six fixed local STMN2 libraries, or compare result JSONs offline.

No downloader. A comparison of supplied JSON is not evidence of raw execution.
Historical measurement code and scientific filters are imported unchanged.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import shutil
import signal
import subprocess
import sys
import time

import stmn2_paired_control_counts as counter

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'reproduction/stmn2-six-libraries/manifest.json'
TARGET = 'research/references/stmn2_targets_sealed.json'
CODE = [MANIFEST, TARGET, 'scripts/replay_stmn2_minimal.py',
        'scripts/stmn2_paired_control_counts.py']
TARGETS = {'canonical': [79611214, 79636801], 'cryptic': [79611214, 79616821]}
CAPS = dict(wall_seconds=96*3600, cpus=2, process_as_bytes=8*1024**3,
            group_rss_bytes=6*1024**3, output_bytes=100*1024**3,
            reserve_bytes=50*1024**3, admission_free_bytes=150*1024**3)
QC = ('sam_records', 'alignment_groups', 'eligible_groups',
      'marked_duplicate_records', 'rejected_groups')


def read(path):
    path = Path(path)
    if path.stat().st_size > 2_000_000:
        raise ValueError('Oversized JSON')
    def unique(pairs):
        result = {}
        for k, v in pairs:
            if k in result:
                raise ValueError('Duplicate JSON key: '+k)
            result[k] = v
        return result
    return json.loads(path.read_text(), object_pairs_hook=unique)


def write_new(path, obj):
    with Path(path).open('x') as handle:
        json.dump(obj, handle, indent=2)
        handle.write('\n')


def digest(path):
    hashes = [hashlib.md5(), hashlib.sha256()]
    size = 0
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024**2), b''):
            size += len(block)
            for h in hashes:
                h.update(block)
    return dict(bytes=size, md5=hashes[0].hexdigest(), sha256=hashes[1].hexdigest())


def sha(path):
    return digest(path)['sha256']


def reference():
    manifest = read(ROOT/MANIFEST)
    for source in manifest['sources']:
        if sha(ROOT/source['path']) != source['sha256']:
            raise ValueError('Reference source changed: '+source['path'])
    target = read(ROOT/TARGET)
    if (target['junctions'] != TARGETS or target['chromosome'] != 'chr8'
            or target['strand'] != '+'):
        raise ValueError('Sealed target changed')
    return manifest


def compare(paths):
    """Compare exact records; do not certify the provenance of supplied JSONs."""
    ref = reference()
    expected = {r['gsm']: r['expected'] for r in ref['libraries']}
    actual = {}
    supplied = []
    for path in paths:
        obj = read(path)
        supplied.append(dict(path=str(Path(path).resolve()), sha256=sha(path)))
        if 'libraries' in obj:
            if (obj.get('status') != 'completed' or obj.get('project') != ref['project']
                    or obj.get('gene') != ref['gene']):
                raise ValueError('Incomplete or mislabelled aggregate')
            rows = obj['libraries']
        else:
            rows = [obj]
        for row in rows:
            gsm = row.get('gsm')
            if gsm not in expected or gsm in actual:
                raise ValueError('Unexpected or duplicate library: '+str(gsm))
            if (row.get('complete') is not True or row.get('project') != ref['project']
                    or row.get('gene') != ref['gene'] or row.get('unit') != ref['unit']):
                raise ValueError('Incomplete/identity/unit mismatch: '+gsm)
            counts, qc = row['counts'], row['qc']
            if set(counts) != set(TARGETS) or set(qc) != set(QC):
                raise ValueError('Unexpected count/QC fields: '+gsm)
            if any(type(v) is not int or v < 0 for v in [*counts.values(), *qc.values()]):
                raise ValueError('Nonnegative integer counts/QC required')
            if (qc['eligible_groups']+qc['rejected_groups'] != qc['alignment_groups']
                    or qc['sam_records'] < 2*qc['eligible_groups']
                    or any(v > qc['eligible_groups'] for v in counts.values())
                    or type(row.get('positive_control_measured')) is not bool
                    or row['positive_control_measured'] != (counts['canonical'] > 0)
                    or set(row.get('support_at_least_20_groups', {})) != {'cryptic'}
                    or type(row['support_at_least_20_groups']['cryptic']) is not bool
                    or row['support_at_least_20_groups']['cryptic'] != (counts['cryptic'] >= 20)):
                raise ValueError('Inconsistent record: '+gsm)
            actual[gsm] = row
    missing = sorted(set(expected)-set(actual))
    differences = []
    for gsm, row in actual.items():
        for field in ('counts', 'qc'):
            for key, wanted in expected[gsm][field].items():
                if row[field][key] != wanted:
                    differences.append(dict(gsm=gsm, field=field+'.'+key,
                                            expected=wanted, observed=row[field][key]))
    return dict(status='records_match' if not missing and not differences else 'records_differ',
                raw_replay_verified=False, missing_libraries=missing,
                differences=differences, supplied=supplied,
                libraries=[dict(gsm=g, counts=actual[g]['counts'], qc=actual[g]['qc'])
                           for g in sorted(actual)],
                limitation='JSON agreement only; no independent execution or biological replication established.')


def commands(plan, gsm):
    d = Path(plan['run_root'])/gsm
    raw = [r['path'] for r in plan['inputs'] if r['gsm'] == gsm]
    clean = [str(d/f'trimmed_{i}.fq') for i in (1, 2)]
    return dict(fastp=[plan['tools']['fastp']['path'], '-i', raw[0], '-I', raw[1],
                      '-o', clean[0], '-O', clean[1], '--detect_adapter_for_pe',
                      '--dont_eval_duplication', '--thread', '2', '--json',
                      str(d/'fastp.json'), '--html', str(d/'fastp.html')],
                align=[plan['tools']['aligner']['path'], '-x', str(Path(plan['index_dir'])/'genome'),
                       '-1', clean[0], '-2', clean[1], '-S', '/dev/stdout',
                       '--no-mixed', '--no-discordant', '--fr', '-p', '2', '--seed', '0',
                       '-k', '2', '--reorder', '--no-unal', '--no-temp-splicesite',
                       '--summary-file', str(d/'hisat2-summary.txt')],
                plain_files=clean)


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()


def native_linux():
    if sys.platform != 'linux' or 'microsoft' in Path('/proc/sys/kernel/osrelease').read_text().lower():
        raise ValueError('Native Linux required; guest filesystem space does not certify WSL host space')


def inspect(inputs, index_dir, tools, run_root, full=True):
    """Bind local files; never search, copy or download sources."""
    ref = reference()
    native_linux()
    if git('status', '--porcelain', '--untracked-files=all'):
        raise ValueError('Clean checkout required')
    import pysam
    if pysam.__version__ != '0.23.3':
        raise ValueError('PySAM 0.23.3 required')
    if set(inputs) != {r['filename'] for r in ref['inputs']}:
        raise ValueError('Exactly twelve fixed filename-to-local-path entries required')
    root = Path(run_root).resolve()
    if root == ROOT or ROOT in root.parents or root in ROOT.parents or not root.parent.is_dir():
        raise ValueError('New output root outside checkout with an existing parent required')
    records, identities = [], set()
    for r in ref['inputs']:
        p = Path(inputs[r['filename']]).expanduser()
        if not p.is_absolute():
            raise ValueError('Absolute input paths required')
        p = p.resolve(strict=True)
        stat = p.stat()
        identity = (stat.st_dev, stat.st_ino)
        if not p.is_file() or identity in identities or root == p or root in p.parents:
            raise ValueError('Distinct regular inputs outside output root required')
        identities.add(identity)
        if stat.st_size != r['bytes']:
            raise ValueError('FASTQ size mismatch: '+r['filename'])
        if full:
            observed = digest(p)
            if any(observed[k] != r[k] for k in ('bytes', 'md5', 'sha256')):
                raise ValueError('FASTQ digest mismatch: '+r['filename'])
        records.append(dict(gsm=r['gsm'], path=str(p), filename=r['filename'],
                            bytes=r['bytes'], md5=r['md5'], sha256=r['sha256']))
    index_dir = Path(index_dir).expanduser().resolve(strict=True)
    if root == index_dir or root in index_dir.parents:
        raise ValueError('Index must remain outside output root')
    for r in ref['index_files']:
        p = index_dir/r['name']
        if not p.is_file() or p.stat().st_size != r['bytes'] or (full and sha(p) != r['sha256']):
            raise ValueError('Index shard mismatch: '+r['name'])
    checked_tools = {}
    for key, pattern in [('fastp', r'fastp 0\.23\.4(?:\s|$)'),
                         ('aligner', r'hisat2-align-s version 2\.2\.3(?:\s|$)')]:
        p = Path(tools[key]).expanduser().resolve(strict=True)
        if root == p or root in p.parents:
            raise ValueError('Tool must remain outside output root')
        ver = subprocess.run([str(p), '--version'], text=True, capture_output=True, check=True, timeout=10)
        version = ver.stdout+ver.stderr
        if not re.search(pattern, version):
            raise ValueError('Expected native tool version: '+key)
        h = sha(p)
        checked_tools[key] = dict(path=str(p), sha256=h, version=version,
                                  historical_build_match=h == ref['historical_tools'][key])
    plan = dict(schema='stmn2-minimal-replay-v1', repository_commit=git('rev-parse', 'HEAD'),
                python_executable=sys.executable, pysam_version=pysam.__version__,
                code_sha256={p: sha(ROOT/p) for p in CODE}, caps=CAPS,
                inputs=records, index_dir=str(index_dir), tools=checked_tools,
                run_root=str(root), network_policy='No transfer implementation; not OS network isolation.')
    plan['commands'] = {r['gsm']: commands(plan, r['gsm']) for r in ref['libraries']}
    return plan


def validate(plan, full=True):
    paths = {r['filename']: r['path'] for r in plan['inputs']}
    if len(paths) != len(plan['inputs']):
        raise ValueError('Duplicate planned input')
    rebuilt = inspect(paths, plan['index_dir'],
                      {k: v['path'] for k, v in plan['tools'].items()}, plan['run_root'], full)
    if rebuilt != plan:
        raise ValueError('Plan/code/environment binding changed')


def free_check(parent, admission=False):
    threshold = CAPS['admission_free_bytes'] if admission else CAPS['reserve_bytes']
    if shutil.disk_usage(parent).free < threshold:
        raise ValueError('Insufficient filesystem free reserve')


def prepare(paths, index_dir, fastp, aligner, run_root, output):
    root, output = Path(run_root).expanduser().resolve(), Path(output).expanduser().resolve()
    if root.exists() or output.exists() or root == output or root in output.parents or ROOT in output.parents:
        raise ValueError('Fresh output root and separate external plan required')
    # Check destination refusal before reading large files; never overwrite an input.
    free_check(root.parent, admission=True)
    plan = inspect(read(paths), index_dir, dict(fastp=fastp, aligner=aligner), root)
    write_new(output, plan)
    return dict(status='prepared_not_executed', plan=str(output), plan_sha256=sha(output),
                libraries=6, local_input_bytes=sum(r['bytes'] for r in plan['inputs']),
                caps=CAPS, historical_build_matches={k: v['historical_build_match'] for k, v in plan['tools'].items()})


def measure(plan, gsm):
    import pysam
    d = Path(plan['run_root'])/gsm
    d.mkdir()
    cmd = plan['commands'][gsm]
    with (d/'fastp.log').open('xb') as log:
        subprocess.run(cmd['fastp'], stdout=log, stderr=subprocess.STDOUT, check=True)
    if any(not Path(p).is_file() or Path(p).stat().st_size == 0 for p in cmd['plain_files']):
        raise ValueError('Missing preprocessing output')
    with (d/'hisat2.log').open('xb') as log:
        proc = subprocess.Popen(cmd['align'], stdout=subprocess.PIPE, stderr=log)
        try:
            with pysam.AlignmentFile(proc.stdout, 'r') as sam:
                if sam.get_reference_length('chr8') != 145138636:
                    raise ValueError('chr8 header mismatch')
                result = counter.count_records(sam, TARGETS)
            if proc.wait() != 0:
                raise ValueError('Aligner failed')
        finally:
            proc.stdout.close()
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
    result.update(gsm=gsm, project='SRP482832', gene='STMN2', complete=True)
    write_new(d/'stmn2-counts.json', result)
    for p in cmd['plain_files']:
        Path(p).unlink()
    return result


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (CAPS['process_as_bytes'], CAPS['process_as_bytes']))
    os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:CAPS['cpus']])


def group_rss(pgid):
    total = 0
    for p in Path('/proc').glob('[0-9]*/stat'):
        try:
            fields = p.read_text().rsplit(')', 1)[1].split()
            if int(fields[2]) == pgid:
                total += int(fields[21])*os.sysconf('SC_PAGE_SIZE')
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            pass
    return total


def output_bytes(root):
    total = 0
    for p in Path(root).rglob('*'):
        try:
            if p.is_file():
                total += p.stat().st_size
        except FileNotFoundError:
            pass
    return total


def stop_group(proc):
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait(timeout=2)


def worker(path):
    plan = read(path)
    root = Path(plan['run_root'])
    accepted = read(root/'accepted.json')
    if (os.getpgrp() != os.getpid() or accepted['supervisor_pid'] != os.getppid()
            or accepted['plan_sha256'] != sha(path)):
        raise ValueError('Active accepting supervisor required')
    try:
        validate(plan)
        rows = []
        for library in reference()['libraries']:
            rows.append(measure(plan, library['gsm']))
        write_new(root/'result.json', dict(status='completed', project='SRP482832',
                                          gene='STMN2', libraries=rows))
    except BaseException as exc:
        write_new(root/'worker-failure.json', dict(status='failed_partial', error=str(exc)))
        raise


def execute(path, accepted_sha):
    path = Path(path).resolve()
    if sha(path) != accepted_sha:
        raise ValueError('Exact plan SHA256 required')
    plan = read(path)
    validate(plan, full=False)
    root = Path(plan['run_root'])
    if root.exists() or root == path or root in path.parents:
        raise ValueError('Fresh output root; plan outside output required; no resume')
    free_check(root.parent, admission=True)
    write_new(str(path)+'.claimed.json', dict(plan_sha256=accepted_sha))
    root.mkdir()
    write_new(root/'accepted.json', dict(plan_sha256=accepted_sha, supervisor_pid=os.getpid()))
    started, peak_rss, peak_disk = time.monotonic(), 0, 0
    proc, failure, cleanup_error, comparison = None, None, None, None
    try:
        with (root/'worker.log').open('xb') as log:
            proc = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '_worker',
                                     '--plan', str(path)], stdout=log, stderr=subprocess.STDOUT,
                                    start_new_session=True, preexec_fn=limits)
            while True:
                rss, disk = group_rss(proc.pid), output_bytes(root)
                peak_rss, peak_disk = max(peak_rss, rss), max(peak_disk, disk)
                if (time.monotonic()-started > CAPS['wall_seconds'] or rss > CAPS['group_rss_bytes']
                        or disk > CAPS['output_bytes']):
                    raise ValueError('Replay resource cap exceeded')
                free_check(root)
                if proc.poll() is not None:
                    break
                time.sleep(0.5)
            if proc.returncode != 0:
                raise ValueError('Worker failed; preserve and inspect logs')
        comparison = compare([root/'result.json'])
        write_new(root/'comparison.json', comparison)
    except BaseException as exc:
        failure = str(exc) or type(exc).__name__
        raise
    finally:
        if proc is not None:
            try:
                stop_group(proc)
            except BaseException as exc:
                cleanup_error = str(exc)
        status = 'failed' if failure or cleanup_error else comparison['status']
        write_new(root/'supervision.json', dict(status=status, failure=failure,
                  cleanup_error=cleanup_error, plan_sha256=accepted_sha,
                  elapsed_seconds=time.monotonic()-started, caps=CAPS,
                  peak_sampled_group_rss_bytes=peak_rss, peak_sampled_output_bytes=peak_disk,
                  raw_execution_reported=not failure and not cleanup_error,
                  note='Local unsigned execution record; sampled limits are not aggregate kernel quotas; no independent host attestation or network telemetry.'))
        if cleanup_error:
            raise RuntimeError('Process-group cleanup failed: '+cleanup_error)
    return comparison


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='action', required=True)
    a = sub.add_parser('compare')
    a.add_argument('--results', type=Path, nargs='+', required=True)
    a.add_argument('--output', type=Path, required=True)
    a = sub.add_parser('prepare')
    for name in ('paths', 'index-dir', 'fastp', 'aligner', 'run-root', 'output'):
        a.add_argument('--'+name, type=Path, required=True)
    a = sub.add_parser('run')
    a.add_argument('--plan', type=Path, required=True)
    a.add_argument('--accept-plan-sha256', required=True)
    a = sub.add_parser('_worker')
    a.add_argument('--plan', type=Path, required=True)
    args = p.parse_args()
    try:
        if args.action == 'compare':
            out = compare(args.results)
            write_new(args.output, out)
        elif args.action == 'prepare':
            out = prepare(args.paths, args.index_dir, args.fastp, args.aligner,
                          args.run_root, args.output)
        elif args.action == 'run':
            out = execute(args.plan, args.accept_plan_sha256)
        else:
            worker(args.plan)
            return 0
        print(json.dumps(out, indent=2))
        return 1 if out.get('status') == 'records_differ' else 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(json.dumps(dict(status='failed', error=str(exc))), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
