"""Audit supplied replay records offline; never attest the original host or raw data."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shlex
import subprocess
import tarfile
import tempfile

import replay_stmn2_minimal as replay

COMMIT = 'b72c877acf02b62fc34ef6a170e7142a9889de69'
PLAN_SHA = '423ccc524120b098c6ed1e7f8b98b76522487c369048d952509e78f0cecb9dd4'
PREFIX = 'ela-stmn2-replay-01/'
PLAN = 'ela-stmn2-replay-plan-01.json'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_bundle(path):
    """Bound input size; inspect members without extracting or following links."""
    data = {}
    total = 0
    with tarfile.open(path, 'r:gz') as archive:
        for member in archive:
            p = PurePosixPath(member.name)
            require(not p.is_absolute() and '..' not in p.parts and member.name not in data,
                    'Unsafe or duplicate archive path')
            require(member.isdir() or member.isfile(), 'Nonregular archive member')
            if member.isdir():
                continue
            total += member.size
            require(0 <= member.size <= 12_000_000 and total <= 20_000_000,
                    'Oversized evidence archive')
            data[member.name] = archive.extractfile(member).read()
    return data


def audit(path):
    data = load_bundle(path)
    obj = lambda name: json.loads(data[name])
    require(sha(data[PLAN]) == PLAN_SHA, 'Unexpected original plan hash')
    plan = obj(PLAN)
    require(plan['repository_commit'] == COMMIT and plan['schema'] == 'stmn2-minimal-replay-v2',
            'Unexpected execution code/schema')
    require(plan['caps'] == replay.CAPS and plan['pysam_version'] == '0.23.3', 'Changed caps/dependency')
    require(set(plan['code_sha256']) == set(replay.CODE), 'Missing/extra code bindings')
    for name, wanted in plan['code_sha256'].items():
        require(sha(subprocess.check_output(['git', '-C', str(replay.ROOT), 'show', COMMIT+':'+name])) == wanted,
                'Execution-commit code hash mismatch: '+name)
    ref = replay.reference()
    require(len(plan['inputs']) == 12, 'Wrong input count')
    for recorded, expected in zip(plan['inputs'], ref['inputs']):
        require(all(recorded[k] == expected[k] for k in ('gsm', 'filename', 'bytes', 'md5', 'sha256')),
                'Changed declared raw identity')
    for name in ('fastp', 'aligner'):
        require(plan['tools'][name]['sha256'] == ref['historical_tools'][name]
                and plan['tools'][name]['historical_build_match'] is True, 'Tool build mismatch')
    require(plan['commands'] == {r['gsm']: replay.commands(plan, r['gsm']) for r in ref['libraries']},
            'Changed scientific command options')
    sup = obj(PREFIX+'supervision.json')
    accepted = obj(PREFIX+'accepted.json')
    claimed = obj(PLAN+'.claimed.json')
    require(all(x['plan_sha256'] == PLAN_SHA for x in (sup, accepted, claimed)), 'Plan receipt mismatch')
    require(type(accepted['supervisor_pid']) is int and accepted['supervisor_pid'] > 0,
            'Invalid accepting supervisor record')
    require(sup['status'] == 'records_match' and sup['failure'] is None
            and sup['cleanup_error'] is None and sup['raw_execution_reported'] is True,
            'Failed/incomplete supervision')
    require(sup['caps'] == plan['caps'] and sup['host'] == plan['host'], 'Supervisor binding mismatch')
    for observed, cap in [('elapsed_seconds', 'wall_seconds'),
                          ('peak_sampled_group_rss_bytes', 'group_rss_bytes'),
                          ('peak_sampled_output_bytes', 'output_bytes')]:
        require(0 <= sup[observed] <= plan['caps'][cap], 'Exceeded recorded '+cap)
    require(sup['minimum_sampled_physical_c_available_bytes'] >= plan['caps']['reserve_bytes'],
            'Physical reserve not met')
    require(not any('failure' in n or 'trimmed_' in n for n in data), 'Failure/intermediate present')
    original = obj(PREFIX+'result.json')
    with tempfile.TemporaryDirectory() as tmp:
        result_path = Path(tmp)/'result.json'
        result_path.write_bytes(data[PREFIX+'result.json'])
        comparison = replay.compare([result_path])
    require(comparison['status'] == 'records_match', 'Exact count/QC comparison failed')
    archived = obj(PREFIX+'comparison.json')
    require(all(archived[k] == comparison[k] for k in
                ('status', 'raw_replay_verified', 'missing_libraries', 'differences', 'libraries')),
            'Archived comparison inconsistent')
    require(len(archived['supplied']) == 1 and archived['supplied'][0]['sha256'] == sha(data[PREFIX+'result.json']),
            'Compared result digest mismatch')
    require([r['gsm'] for r in original['libraries']] == [r['gsm'] for r in ref['libraries']],
            'Changed library order')
    rows = []
    for row in original['libraries']:
        gsm, qc = row['gsm'], row['qc']
        prefix = PREFIX+gsm+'/'
        require(obj(prefix+'stmn2-counts.json') == row, 'Per-library record mismatch: '+gsm)
        fastp = obj(prefix+'fastp.json')
        require(fastp['summary']['fastp_version'] == '0.23.4', 'fastp version mismatch')
        require(shlex.split(fastp['command']) == plan['commands'][gsm]['fastp'], 'fastp command mismatch')
        hisat = data[prefix+'hisat2-summary.txt']
        require(hisat == data[prefix+'hisat2.log'], 'HISAT log/summary mismatch')
        text = hisat.decode()
        pairs = int(re.search(r'^(\d+) reads;', text)[1])
        unique = int(re.search(r'(\d+) \([^\n]+\) aligned concordantly exactly 1 time', text)[1])
        multiple = int(re.search(r'(\d+) \([^\n]+\) aligned concordantly >1 times', text)[1])
        require(fastp['summary']['after_filtering']['total_reads'] == 2*pairs,
                'Preprocessing/alignment pair mismatch')
        require(qc['eligible_groups'] == unique and qc['rejected_groups'] == multiple
                and qc['alignment_groups'] == unique+multiple
                and qc['sam_records'] == 2*unique+4*multiple, 'Alignment/count QC mismatch')
        log = data[prefix+'fastp.log'].decode()
        require('fastp v0.23.4, time used:' in log and (prefix+'fastp.html') in data,
                'Missing preprocessing logs')
        rows.append(dict(gsm=gsm, counts=row['counts'], qc=qc, aligned_input_pairs=pairs))
    return dict(status='supplied_replay_records_consistent', archive_sha256=sha(Path(path).read_bytes()),
                plan_sha256=PLAN_SHA, execution_commit=COMMIT, file_count=len(data),
                member_sha256={n: sha(b) for n, b in sorted(data.items())},
                input_identities_in_plan=12, index_identities_in_manifest=8,
                historical_tool_builds_match=True, exact_count_fields_matched=12,
                exact_qc_fields_matched=30, libraries=rows,
                supervision={k: sup[k] for k in ('status', 'failure', 'cleanup_error', 'elapsed_seconds',
                    'peak_sampled_group_rss_bytes', 'peak_sampled_output_bytes',
                    'minimum_sampled_physical_c_available_bytes', 'raw_execution_reported')},
                limitations=['Supplied unsigned host records, not independent execution attestation.',
                             'Actual FASTQs, index and installed binaries are not present for agent rehashing.',
                             'Same operator, machine and biological inputs; no independent biological replication.'])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    replay.write_new(args.output, audit(args.bundle))


if __name__ == '__main__':
    main()
