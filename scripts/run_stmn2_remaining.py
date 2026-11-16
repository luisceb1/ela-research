"""Fixed four-library descriptive STMN2 run with a separate bounded transfer ledger."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import run_gse252892_local as old
import run_gse252892_stmn2_control as stmn
import gse252892_range_transport as ranged
import prepare_gse252892_local as prep

ROOT = Path(__file__).resolve().parents[1]
SELECTED = ('GSM8009879', 'GSM8009880', 'GSM8009882', 'GSM8009883')
CAPS = dict(old.CAPS, transfer_bytes=40_000_000_000, wall_seconds=96*3600,
            root_bytes=200*1024**3)
HISTORY = {'charged_bytes': 13007068985, 'observed_bytes': 13006020409}
MANIFEST = 'reports/stmn2-remaining-libraries-20261115/manifest-disabled.json'
SOURCE_SHA = '8379c7e56c0546623fac80c732935f29113f17e048b8625d85e1163e3f61b557'
CODE = list(dict.fromkeys(stmn.CODE + ['scripts/run_stmn2_remaining.py', MANIFEST]))
read = old.read_small
save = old.save


def inputs():
    rows = read(ROOT/MANIFEST)['input_files']
    if len(rows) != 8 or tuple(dict.fromkeys(r['gsm'] for r in rows)) != SELECTED:
        raise ValueError('Fixed eight inputs/order changed')
    if sum(int(r['compressed_bytes']) for r in rows) != 27762593667:
        raise ValueError('Fixed input bytes changed')
    return rows


def hashes():
    return {p: prep.sha256(ROOT/p) for p in CODE}


def source_record(path):
    path = Path(path)
    if prep.sha256(path) != SOURCE_SHA:
        raise ValueError('Exact completed STMN2 source descriptor required')
    prior = read(path)
    source, record = stmn.source_record(prior['source_record']['path'], False)
    if source != prior['source'] or record != prior['source_record']:
        raise ValueError('Prior source binding changed')
    for name in ('result.json', 'supervision.json'):
        p = Path(prior['run_root'])/name
        ref = ROOT/'reports/gse252892-stmn2-result-20261115/original'/name
        if prep.sha256(p) != prep.sha256(ref):
            raise ValueError('Prior STMN2 metadata changed')
    roots = record['prior_roots'] + [prior['run_root']]
    if len(set(roots)) != 7:
        raise ValueError('Seven distinct retained roots required')
    return prior, roots


def commands(plan, gsm):
    # Keep old option order; substitute only the fixed library/run paths.
    rows = [r for r in inputs() if r['gsm'] == gsm]
    if len(rows) != 2:
        raise ValueError('Exactly two mates required')
    template = old.commands({'run_root': plan['run_root'], 'fastp': plan['fastp'],
                             'base': plan['source']['base']}, 'GSM8009878')
    for key in ('fastp', 'align', 'plain_files'):
        template[key] = [v.replace('GSM8009878', gsm).replace('SRR27477544', rows[0]['run'])
                         for v in template[key]]
    return template


def validate(plan, full=True):
    if plan.get('schema') != 'stmn2-remaining-v1' or plan.get('caps') != CAPS:
        raise ValueError('Fixed schema/caps changed')
    if plan.get('history') != HISTORY or plan.get('transport') != ranged.RECOVERY_SETTINGS:
        raise ValueError('Historical accounting/transport changed')
    if plan.get('code_sha256') != hashes() or plan.get('repository_commit') != prep.git('rev-parse', 'HEAD'):
        raise ValueError('Pinned code changed')
    if prep.git('status', '--porcelain', '--untracked-files=all'):
        raise ValueError('Clean checkout required')
    prior, roots = source_record(plan['source_plan_path'])
    if prior['source'] != plan['source'] or roots != plan['prior_roots'] or plan['inputs'] != inputs():
        raise ValueError('Input/source binding changed')
    if plan['fastp'] != prior['fastp'] or plan['python_executable'] != sys.executable:
        raise ValueError('Tool/environment changed')
    for tool in [plan['fastp'], *plan['source']['base']['tools'].values()]:
        if prep.sha256(tool['path']) != tool['sha256']:
            raise ValueError('Binary changed')
    if read(ROOT/stmn.TARGET)['junctions'] != stmn.EXPECTED_TARGETS:
        raise ValueError('Sealed targets changed')
    root = Path(plan['run_root'])
    if not root.is_absolute() or root.is_symlink() or root == ROOT or ROOT in root.parents:
        raise ValueError('Separate absolute root required')
    for p in roots:
        p = Path(p)
        if root == p or root in p.parents or p in root.parents:
            raise ValueError('Preserve prior roots')
    if {g: commands(plan, g) for g in SELECTED} != plan['commands']:
        raise ValueError('Fixed command changed')
    if full:
        import pysam
        if pysam.__version__ != '0.23.3':
            raise ValueError('Expected PySAM0.23.3')
        expected = read(ROOT/'reports/hisat2-index-inspection-20261031/verified_index.json')
        base = plan['source']['base']
        if prep.verify_index(base['index_directory'], expected) != base['index_files']:
            raise ValueError('Index changed')


def prepare(source_path, root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    prior, roots = source_record(source_path)
    if root.exists() or output.exists() or root == output or root in output.parents or ROOT in output.parents:
        raise ValueError('Fresh external root/proposal required')
    if any(Path(p) == output or Path(p) in output.parents for p in roots):
        raise ValueError('Proposal must preserve prior roots')
    plan = {'schema': 'stmn2-remaining-v1', 'source_plan_path': str(Path(source_path).resolve()),
            'source': prior['source'], 'prior_roots': roots, 'run_root': str(root),
            'fastp': prior['fastp'], 'inputs': inputs(), 'caps': CAPS, 'history': HISTORY,
            'transport': ranged.RECOVERY_SETTINGS, 'code_sha256': hashes(),
            'repository_commit': prep.git('rev-parse', 'HEAD'), 'python_executable': sys.executable}
    plan['commands'] = {g: commands(plan, g) for g in SELECTED}
    validate(plan)
    free = old.physical_free()
    if free < 150*1024**3:
        raise ValueError('Require100GiB growth headroom plus50GiB physical C: reserve')
    retained = sum(old.root_bytes(p) for p in roots)
    if retained + 100*1024**3 > CAPS['root_bytes']:
        raise ValueError('Combined disk cap lacks100GiB growth headroom')
    b = (json.dumps(plan, indent=2)+'\n').encode()
    with output.open('xb') as f:
        f.write(b)
    return {'status': 'proposal_not_started', 'output': str(output), 'plan_sha256': prep.sha256(output),
            'caps': CAPS, 'historical_transfer': HISTORY, 'physical_c_free_bytes': free,
            'retained_root_bytes': retained, 'new_advertised_bytes': 27762593667}


def worker(path):
    plan = read(path)
    root = Path(plan['run_root'])
    accepted = read(root/'accepted.json')
    if os.getpgrp() != os.getpid() or accepted['supervisor_pid'] != os.getppid() or accepted['plan_sha256'] != prep.sha256(path) or accepted['transfer_bytes'] != CAPS['transfer_bytes']:
        raise ValueError('Active accepting supervisor required')
    try:
        validate(plan)
        ledger = ranged.Budget(root/'transfer-ledger.json', CAPS['transfer_bytes'], 0)
        result = {'project': 'SRP482832', 'gene': 'STMN2', 'analysis': 'descriptive library-level support only',
                  'historical_transfer': HISTORY, 'libraries': []}
        for gsm in SELECTED:
            d = root/gsm
            d.mkdir()
            save(root/'progress.json', {'phase': 'download', 'library': gsm})
            for row in plan['inputs']:
                if row['gsm'] == gsm:
                    ranged.download(row, d, ledger, settings=plan['transport'])
            result['libraries'].append(measure(plan, gsm, root))
        result['status'] = 'completed'
        save(root/'result.json', result)
    except BaseException as exc:
        save(root/'worker-failure.json', {'status': 'failed_partial_not_interpretable', 'error': str(exc)})
        raise


def main():
    p = argparse.ArgumentParser(description=__doc__)
    s = p.add_subparsers(dest='action', required=True)
    a = s.add_parser('prepare')
    a.add_argument('--source-plan', type=Path, required=True)
    a.add_argument('--run-root', type=Path, required=True)
    a.add_argument('--output', type=Path, required=True)
    a = s.add_parser('execute')
    a.add_argument('--plan', type=Path, required=True)
    a.add_argument('--accept-plan-sha256', required=True)
    a.add_argument('--accept-transfer-bytes', type=int, required=True)
    a = s.add_parser('_worker')
    a.add_argument('--plan', type=Path, required=True)
    a = p.parse_args()
    if a.action == 'prepare':
        out = prepare(a.source_plan, a.run_root, a.output)
    elif a.action == 'execute':
        out = execute(a.plan, a.accept_plan_sha256, a.accept_transfer_bytes)
    else:
        worker(a.plan)
        out = {'status': 'worker_finished'}
    print(json.dumps(out, indent=2))


def measure(plan,gsm,root):
    import pysam
    d=root/gsm;cmd=plan['commands'][gsm]
    save(root/'progress.json',{'phase':'fastp','library':gsm,'network_bytes':0})
    with (d/'fastp.log').open('wb') as log:subprocess.run(cmd['fastp'],stdout=log,stderr=subprocess.STDOUT,check=True)
    if any(not Path(p).is_file() or Path(p).stat().st_size==0 for p in cmd['plain_files']):raise ValueError('No retained paired preprocessing output')
    save(root/'progress.json',{'phase':'alignment_and_stmn2_count','library':gsm,'network_bytes':0})
    with (d/'hisat2.log').open('wb') as log:
        proc=subprocess.Popen(cmd['align'],stdout=subprocess.PIPE,stderr=log)
        try:
            with pysam.AlignmentFile(proc.stdout,'r') as sam:
                if sam.get_reference_length('chr8')!=145138636:raise ValueError('chr8 header mismatch')
                result=stmn.counter.count_records(sam,stmn.EXPECTED_TARGETS)
            if proc.wait()!=0:raise ValueError('Alignment failed')
        finally:
            if proc.poll() is None:proc.terminate()
    result.update(gsm=gsm,project='SRP482832',gene='STMN2',complete=True)
    save(d/'stmn2-counts.json',result)
    for p in cmd['plain_files']:Path(p).unlink()
    return result

def execute(path,accepted_sha,transfer_bytes):
    path=Path(path).resolve()
    if transfer_bytes!=CAPS['transfer_bytes'] or prep.sha256(path)!=accepted_sha:raise ValueError('Exact proposal SHA and fixed transfer acceptance required')
    plan=read(path);validate(plan,False);old.check_free(old.physical_free());root=Path(plan['run_root'])
    if root.exists():raise ValueError('New root required; no resume')
    with Path(str(path)+'.claimed.json').open('x') as f:json.dump({'plan_sha256':accepted_sha,'transfer_bytes':CAPS['transfer_bytes']},f)
    root.mkdir();save(root/'accepted.json',{'plan_sha256':accepted_sha,'transfer_bytes':CAPS['transfer_bytes'],'supervisor_pid':os.getpid()})
    proc=None;started=time.monotonic();peak_rss=peak_disk=0;status='failed';failure=None
    try:
        with (root/'worker.log').open('wb') as log:
            proc=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'_worker','--plan',str(path)],stdout=log,stderr=subprocess.STDOUT,start_new_session=True,preexec_fn=old.child_limits)
            last=0
            while proc.poll() is None:
                elapsed=time.monotonic()-started
                if elapsed>CAPS['wall_seconds']:raise ValueError('Wall cap exceeded')
                rss=old.group_rss(proc.pid);disk=old.root_bytes(root)+sum(old.root_bytes(p) for p in plan['prior_roots'])
                peak_rss=max(peak_rss,rss);peak_disk=max(peak_disk,disk)
                if rss>CAPS['group_rss_bytes'] or disk>CAPS['root_bytes']:raise ValueError('Sampled resource cap exceeded')
                if elapsed-last>=30:
                    old.check_free(old.physical_free());last=elapsed
                    progress=read(root/'progress.json') if (root/'progress.json').exists() else {'phase':'verify_sources_index'}
                    print(json.dumps({'elapsed_seconds':round(elapsed),'progress':progress,'transfer_ledger':read(root/'transfer-ledger.json') if (root/'transfer-ledger.json').exists() else None,'sampled_group_rss_bytes':rss,'sampled_combined_root_bytes':disk}),flush=True)
                time.sleep(0.5)
            if proc.returncode or not (root/'result.json').exists():raise ValueError('Worker failed; inspect retained logs')
            status=read(root/'result.json')['status']
    except BaseException as exc:failure=str(exc) or type(exc).__name__;raise
    finally:
        cleanup=None
        try:
            if proc is not None:old.stop_group(proc)
        except BaseException as exc:cleanup=str(exc)
        save(root/'supervision.json',{'status':status,'failure':failure,'elapsed_seconds':time.monotonic()-started,'plan_sha256':accepted_sha,
            'caps':CAPS,'transfer_bytes':CAPS['transfer_bytes'],'peak_sampled_group_rss_bytes':peak_rss,'peak_sampled_combined_root_bytes':peak_disk,
            'cleanup_error':cleanup,'limitations':'Sampled RSS/disk are not kernel quotas; uninterruptible I/O limits persist.'})
        if cleanup:raise RuntimeError(cleanup)
    return {'status':status,'run_root':str(root),'transfer_bytes':CAPS['transfer_bytes']}

if __name__ == '__main__':
    main()
