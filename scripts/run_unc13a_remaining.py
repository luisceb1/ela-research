"""Zero-transfer UNC13A measurement in four fixed, already downloaded libraries."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import run_gse252892_local as old
import run_gse252892_stmn2_control as stmn
import run_stmn2_remaining as remaining
import prepare_gse252892_local as prep

ROOT = Path(__file__).resolve().parents[1]
SELECTED = remaining.SELECTED
CAPS = dict(old.CAPS, transfer_bytes=0, network_bytes=0, root_bytes=200*1024**3)
SOURCE_SHA = '0c6e43df6f2b1d5c8474d27c61701e8a487533567e15ac92ae581b93b9ee6462'
HISTORY = {'observed_bytes':40772442278, 'charged_bytes':40773490854}
TARGET = 'research/references/unc13a_targets_sealed.json'
CODE = list(dict.fromkeys(remaining.CODE + ['scripts/run_unc13a_remaining.py',
    'reports/stmn2-remaining-result-20261116/original-verification.json']))
read = old.read_small
save = old.save


def hashes():
    return {p:prep.sha256(ROOT/p) for p in CODE}


def source_record(path, full=True):
    path=Path(path);stmn.regular(path)
    if prep.sha256(path)!=SOURCE_SHA:
        raise ValueError('Exact completed four-library source proposal required')
    prior=read(path);root=Path(prior['run_root'])
    audit=read(ROOT/'reports/stmn2-remaining-result-20261116/original-verification.json')
    if audit['archive_sha256']!='7398e02f2bb43900c918d2e43ecd49dd52ea5fa5c534326a08b0d696dbe8e7d8':
        raise ValueError('Original audit identity changed')
    record={'path':str(path.resolve()),'sha256':SOURCE_SHA,'metadata_sha256':{},'inputs':[]}
    for name in ['result.json','supervision.json','transfer-ledger.json']:
        p=root/name;stmn.regular(p)
        ref=ROOT/'reports/stmn2-remaining-result-20261116/original'/name
        if prep.sha256(p)!=prep.sha256(ref):
            raise ValueError('Original source metadata changed')
        record['metadata_sha256'][name]=prep.sha256(p)
    if prior['inputs']!=remaining.inputs():
        raise ValueError('Fixed source inputs changed')
    for row in prior['inputs']:
        p=root/row['gsm']/Path(row['url']).name;stmn.regular(p)
        receipt=p.with_name(p.name+'.verified.json');stmn.regular(receipt)
        reference=ROOT/'reports/stmn2-remaining-result-20261116/original'/row['gsm']/receipt.name
        if prep.sha256(receipt)!=prep.sha256(reference):
            raise ValueError('Complete-input receipt changed')
        info=read(receipt)
        if info['status']!='verified_complete' or info['bytes']!=int(row['compressed_bytes']) or info['md5']!=row['md5']:
            raise ValueError('Original input identity changed')
        expected={k:info[k] for k in ['bytes','md5','sha256']}
        if full and stmn.raw_digest(p)!=expected:
            raise ValueError('Raw input digest mismatch')
        record['inputs'].append(dict(gsm=row['gsm'],path=str(p),receipt_sha256=prep.sha256(receipt),**expected))
    record['prior_roots']=prior['prior_roots']+[prior['run_root']]
    if len(set(record['prior_roots']))!=8:
        raise ValueError('Eight retained source roots required')
    return prior,record


def commands(plan,gsm):
    cmd=remaining.commands(plan,gsm)
    rows=[r for r in plan['inputs'] if r['gsm']==gsm]
    if len(rows)!=2:
        raise ValueError('Exactly two existing input mates required')
    for flag,row in zip(['-i','-I'],rows):
        cmd['fastp'][cmd['fastp'].index(flag)+1]=row['path']
    return cmd


def validate(plan,full=True):
    if plan.get('schema')!='unc13a-remaining-offline-v1' or plan.get('caps')!=CAPS or plan.get('history')!=HISTORY:
        raise ValueError('Fixed schema/envelope/history changed')
    if plan.get('code_sha256')!=hashes() or plan.get('repository_commit')!=prep.git('rev-parse','HEAD') or prep.git('status','--porcelain','--untracked-files=all'):
        raise ValueError('Pinned clean code required')
    prior,record=source_record(plan['source_record']['path'],full)
    if prior['source']!=plan['source'] or record!=plan['source_record'] or plan['inputs']!=record['inputs']:
        raise ValueError('Source binding changed')
    if plan['fastp']!=prior['fastp'] or plan['python_executable']!=sys.executable:
        raise ValueError('Fixed environment changed')
    for tool in [plan['fastp'],*plan['source']['base']['tools'].values()]:
        if prep.sha256(tool['path'])!=tool['sha256']:
            raise ValueError('Tool changed')
    root=Path(plan['run_root'])
    if not root.is_absolute() or root==ROOT or ROOT in root.parents or root.is_symlink():
        raise ValueError('Separate absolute root required')
    for p in record['prior_roots']:
        p=Path(p)
        if p==root or p in root.parents or root in p.parents:
            raise ValueError('Preserve old roots')
    if plan['commands']!={g:commands(plan,g) for g in SELECTED}:
        raise ValueError('Fixed commands changed')
    seal=read(ROOT/TARGET)
    if seal['chromosome']!='chr19' or seal['strand']!='-' or seal['assembly']!='GRCh38/hg38':
        raise ValueError('UNC13A target convention changed')
    if full:
        import pysam
        if pysam.__version__!='0.23.3':
            raise ValueError('Expected PySAM0.23.3')
        base=plan['source']['base']
        expected=read(ROOT/'reports/hisat2-index-inspection-20261031/verified_index.json')
        if prep.verify_index(base['index_directory'],expected)!=base['index_files']:
            raise ValueError('Index changed')


def prepare(source_plan,root,output):
    root,output=Path(root).resolve(),Path(output).resolve()
    prior,record=source_record(source_plan)
    if root.exists() or output.exists() or root==output or root in output.parents or ROOT in output.parents:
        raise ValueError('Fresh external root/descriptor required')
    if any(output==Path(p) or Path(p) in output.parents for p in record['prior_roots']):
        raise ValueError('Preserve source directories')
    plan={'schema':'unc13a-remaining-offline-v1','source':prior['source'],'source_record':record,
          'inputs':record['inputs'],'fastp':prior['fastp'],'run_root':str(root),
          'caps':CAPS,'history':HISTORY,'code_sha256':hashes(),
          'repository_commit':prep.git('rev-parse','HEAD'),'python_executable':sys.executable}
    plan['commands']={g:commands(plan,g) for g in SELECTED};validate(plan)
    free=old.physical_free();size=sum(old.root_bytes(p) for p in record['prior_roots'])
    if free<150*1024**3 or size+100*1024**3>CAPS['root_bytes']:
        raise ValueError('Require100GiB growth plus50GiB physical reserve and combined disk allowance')
    with output.open('x') as f:
        json.dump(plan,f,indent=2);f.write('\n')
    return {'status':'offline_proposal_not_started','output':str(output),'plan_sha256':prep.sha256(output),
            'network_bytes':0,'input_files':8,'retained_bytes':size,'physical_c_free_bytes':free,'caps':CAPS}


def worker(path):
    plan=read(path);root=Path(plan['run_root']);accepted=read(root/'accepted.json')
    if os.getpgrp()!=os.getpid() or accepted['supervisor_pid']!=os.getppid() or accepted['plan_sha256']!=prep.sha256(path) or accepted['network_bytes']!=0:
        raise ValueError('Active accepting supervisor required')
    try:
        validate(plan)
        result={'project':'SRP482832','gene':'UNC13A','analysis':'descriptive fixed-event counts only',
                'network_bytes':0,'historical_transfer':HISTORY,'libraries':[]}
        for gsm in SELECTED:
            (root/gsm).mkdir()
            result['libraries'].append(measure(plan,gsm,root))
        result['status']='completed';save(root/'result.json',result)
    except BaseException as exc:
        save(root/'worker-failure.json',{'status':'failed_partial_not_interpretable','error':str(exc)})
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='action',required=True)
    a=s.add_parser('prepare');a.add_argument('--source-plan',type=Path,required=True);a.add_argument('--run-root',type=Path,required=True);a.add_argument('--output',type=Path,required=True)
    a=s.add_parser('execute');a.add_argument('--plan',type=Path,required=True);a.add_argument('--accept-plan-sha256',required=True);a.add_argument('--accept-network-bytes',type=int,required=True)
    a=s.add_parser('_worker');a.add_argument('--plan',type=Path,required=True)
    a=p.parse_args()
    if a.action=='prepare':out=prepare(a.source_plan,a.run_root,a.output)
    elif a.action=='execute':out=execute(a.plan,a.accept_plan_sha256,a.accept_network_bytes)
    else:worker(a.plan);out={'status':'worker_finished'}
    print(json.dumps(out,indent=2))


def measure(plan,gsm,root):
    import pysam
    d=root/gsm;cmd=plan['commands'][gsm]
    save(root/'progress.json',{'phase':'fastp','library':gsm,'network_bytes':0})
    with (d/'fastp.log').open('wb') as log:subprocess.run(cmd['fastp'],stdout=log,stderr=subprocess.STDOUT,check=True)
    if any(not Path(p).is_file() or Path(p).stat().st_size==0 for p in cmd['plain_files']):raise ValueError('No retained paired preprocessing output')
    save(root/'progress.json',{'phase':'alignment_and_unc13a_count','library':gsm,'network_bytes':0})
    with (d/'hisat2.log').open('wb') as log:
        proc=subprocess.Popen(cmd['align'],stdout=subprocess.PIPE,stderr=log)
        try:
            with pysam.AlignmentFile(proc.stdout,'r') as sam:
                if sam.get_reference_length('chr19')!=58617616:raise ValueError('chr19 header mismatch')
                result=old.count_records(sam,read(ROOT/TARGET)['junctions'])
            if proc.wait()!=0:raise ValueError('Alignment failed')
        finally:
            if proc.poll() is None:proc.terminate()
    result.update(gsm=gsm,project='SRP482832',gene='UNC13A',complete=True)
    save(d/'unc13a-counts.json',result)
    for p in cmd['plain_files']:Path(p).unlink()
    return result

def execute(path,accepted_sha,network_bytes):
    path=Path(path).resolve()
    if network_bytes!=0 or prep.sha256(path)!=accepted_sha:raise ValueError('Exact proposal SHA and zero network acceptance required')
    plan=read(path);validate(plan,False);old.check_free(old.physical_free());root=Path(plan['run_root'])
    if root.exists():raise ValueError('New root required; no resume')
    with Path(str(path)+'.claimed.json').open('x') as f:json.dump({'plan_sha256':accepted_sha,'network_bytes':0},f)
    root.mkdir();save(root/'accepted.json',{'plan_sha256':accepted_sha,'network_bytes':0,'supervisor_pid':os.getpid()})
    proc=None;started=time.monotonic();peak_rss=peak_disk=0;status='failed';failure=None
    try:
        with (root/'worker.log').open('wb') as log:
            proc=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'_worker','--plan',str(path)],stdout=log,stderr=subprocess.STDOUT,start_new_session=True,preexec_fn=old.child_limits)
            last=0
            while proc.poll() is None:
                elapsed=time.monotonic()-started
                if elapsed>CAPS['wall_seconds']:raise ValueError('Wall cap exceeded')
                rss=old.group_rss(proc.pid);disk=old.root_bytes(root)+sum(old.root_bytes(p) for p in plan['source_record']['prior_roots'])
                peak_rss=max(peak_rss,rss);peak_disk=max(peak_disk,disk)
                if rss>CAPS['group_rss_bytes'] or disk>CAPS['root_bytes']:raise ValueError('Sampled resource cap exceeded')
                if elapsed-last>=30:
                    old.check_free(old.physical_free());last=elapsed
                    progress=read(root/'progress.json') if (root/'progress.json').exists() else {'phase':'verify_sources_index'}
                    print(json.dumps({'elapsed_seconds':round(elapsed),'progress':progress,'network_bytes':0,'sampled_group_rss_bytes':rss,'sampled_combined_root_bytes':disk}),flush=True)
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
            'caps':CAPS,'network_bytes':0,'peak_sampled_group_rss_bytes':peak_rss,'peak_sampled_combined_root_bytes':peak_disk,
            'cleanup_error':cleanup,'limitations':'Sampled RSS/disk are not kernel quotas; uninterruptible I/O limits persist.'})
        if cleanup:raise RuntimeError(cleanup)
    return {'status':status,'run_root':str(root),'network_bytes':0}

if __name__=='__main__':
    main()
