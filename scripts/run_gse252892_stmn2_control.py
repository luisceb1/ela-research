"""Offline prepare and supervised zero-network STMN2 control on existing run06 inputs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import run_gse252892_local as old
import prepare_gse252892_local as prep
import stmn2_paired_control_counts as counter

ROOT=Path(__file__).resolve().parents[1]
SOURCE_SHA='61c5f2c73e762ed23d9c940ce7db2b3043713169311e4594d8f87e51d0332369'
CAPS=dict(old.CAPS,network_bytes=0)
TARGET='research/references/stmn2_targets_sealed.json'
CODE=list(dict.fromkeys(old.CODE+['scripts/stmn2_paired_control_counts.py','scripts/run_gse252892_stmn2_control.py',TARGET,
    'reports/gse252892-audit-verification-20261114/verification.json']))
EXPECTED_TARGETS={'canonical':[79611214,79636801],'cryptic':[79611214,79616821]}
read=old.read_small
save=old.save

def hashes():return {p:prep.sha256(ROOT/p) for p in CODE}

def raw_digest(path):
    md5=hashlib.md5();sha=hashlib.sha256();n=0
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024**2),b''):n+=len(b);md5.update(b);sha.update(b)
    return {'bytes':n,'md5':md5.hexdigest(),'sha256':sha.hexdigest()}

def regular(path):
    p=Path(path)
    if not p.is_file() or any(q.is_symlink() for q in [p,*p.parents]):raise ValueError('Expected regular nonsymlink source')

def commands(plan,gsm):
    # Reuse the exact old option sequence; only raw source and output paths differ.
    shim={'run_root':plan['run_root'],'fastp':plan['fastp'],'base':plan['source']['base']}
    cmd=old.commands(shim,gsm)
    sources=[r['path'] for r in plan['inputs'] if r['gsm']==gsm]
    if len(sources)!=2:raise ValueError('Exactly two fixed input mates required')
    for flag,path in zip(['-i','-I'],sources):cmd['fastp'][cmd['fastp'].index(flag)+1]=path
    return cmd

def source_record(path,full=True):
    path=Path(path).resolve();regular(path)
    if prep.sha256(path)!=SOURCE_SHA:raise ValueError('Exact completed source proposal required')
    source=read(path);root=Path(source['run_root'])
    record={'path':str(path),'sha256':SOURCE_SHA,'metadata_sha256':{}}
    for name in ['result.json','supervision.json','transfer-ledger.json']:
        p=root/name;regular(p);ref=ROOT/'reports/gse252892-audit-verification-20261114/original'/name
        if prep.sha256(p)!=prep.sha256(ref):raise ValueError('Original source metadata changed')
        record['metadata_sha256'][name]=prep.sha256(p)
    audit=read(ROOT/'reports/gse252892-audit-verification-20261114/verification.json')
    if audit['zip_sha256']!='c8751b9610512791ba40a613449ad332833ff557e8c371f96e118636361e4617':raise ValueError('Audited archive identity changed')
    expected=audit['recorded_complete_inputs']
    inputs=[]
    for row,verified in zip(source['base']['input_files'],expected):
        p=root/row['gsm']/Path(row['url']).name;receipt=p.with_name(p.name+'.verified.json');info=read(receipt)
        wanted={'bytes':int(row['compressed_bytes']),'md5':row['md5'],'sha256':verified['recorded_sha256']}
        if verified['gsm']!=row['gsm'] or verified['file']!=p.name or info.get('status')!='verified_complete' or any(info.get(k)!=v for k,v in wanted.items()):raise ValueError('Input identity/receipt changed')
        regular(p)
        if full and raw_digest(p)!=wanted:raise ValueError('Original FASTQ digest mismatch')
        inputs.append(dict(gsm=row['gsm'],path=str(p),url=row['url'],receipt_sha256=prep.sha256(receipt),**wanted))
    if len(inputs)!=4:raise ValueError('Four fixed source inputs required')
    record['inputs']=inputs;record['prior_roots']=source['lineage']['prior_roots']+[str(root)]
    if len(set(record['prior_roots']))!=6:raise ValueError('Six retained source roots required')
    return source,record

def validate(plan,full=True):
    if plan.get('schema')!='gse252892-stmn2-response-v1' or plan.get('caps')!=CAPS:raise ValueError('Fixed schema/envelope changed')
    if plan.get('code_sha256')!=hashes() or plan.get('repository_commit')!=prep.git('rev-parse','HEAD') or prep.git('status','--porcelain','--untracked-files=all'):raise ValueError('Pinned clean checkout/code required')
    targets=read(ROOT/TARGET)
    if plan.get('targets_sha256')!=prep.sha256(ROOT/TARGET):raise ValueError('Target file hash changed')
    if targets['junctions']!=EXPECTED_TARGETS or targets['chromosome']!='chr8' or targets['strand']!='+':raise ValueError('STMN2 target seal changed')
    source,record=source_record(plan['source_record']['path'],full)
    if source!=plan['source'] or record!=plan['source_record'] or record['inputs']!=plan['inputs']:raise ValueError('Source binding changed')
    if plan['python_executable']!=sys.executable:raise ValueError('Python environment changed')
    for tool in [plan['fastp'],*source['base']['tools'].values()]:
        if prep.sha256(tool['path'])!=tool['sha256']:raise ValueError('Tool binary changed')
    if full:
        import pysam
        if pysam.__version__!='0.23.3':raise ValueError('Expected PySAM0.23.3')
        expected=read(ROOT/'reports/hisat2-index-inspection-20261031/verified_index.json')
        if prep.verify_index(source['base']['index_directory'],expected)!=source['base']['index_files']:raise ValueError('Index changed')
    if {g:commands(plan,g) for g in prep.SELECTED}!=plan['commands']:raise ValueError('Fixed commands changed')
    root=Path(plan['run_root'])
    if not root.is_absolute() or root==ROOT or ROOT in root.parents or root.is_symlink():raise ValueError('Separate absolute run root required')
    if any(root==Path(p) or root in Path(p).parents or Path(p) in root.parents for p in record['prior_roots']):raise ValueError('Preserve old roots')

def prepare(source_plan,root,output):
    root=Path(root).expanduser().resolve();output=Path(output).expanduser().resolve()
    if root.exists() or output.exists() or root==output or ROOT in output.parents:raise ValueError('New external root/proposal required')
    source,record=source_record(source_plan)
    if root in output.parents or any(Path(p) in output.parents for p in record['prior_roots']):raise ValueError('Preserve source/run directories; proposal outside roots required')
    plan={'schema':'gse252892-stmn2-response-v1','source':source,'source_record':record,'inputs':record['inputs'],
        'run_root':str(root),'python_executable':sys.executable,'repository_commit':prep.git('rev-parse','HEAD'),
        'caps':CAPS,'fastp':source['fastp'],'code_sha256':hashes(),'targets_sha256':prep.sha256(ROOT/TARGET),
        'protocol':'research/plans/2026-11-14-gse252892-stmn2-execution.md'}
    plan['commands']={g:commands(plan,g) for g in prep.SELECTED};validate(plan)
    old.check_free(old.physical_free())
    prior_bytes=sum(old.root_bytes(p) for p in record['prior_roots'])
    if prior_bytes>=CAPS['root_bytes']:raise ValueError('Retained roots already fill the combined disk allowance')
    candidates=[]
    for prior in record['prior_roots']:
        for gsm in prep.SELECTED:
            for name in ['trimmed_1.fq','trimmed_2.fq']:
                p=Path(prior)/gsm/name
                if p.exists():regular(p);candidates.append({'path':str(p),'bytes':p.stat().st_size})
    b=(json.dumps(plan,indent=2)+'\n').encode()
    with output.open('xb') as f:f.write(b)
    return {'status':'stmn2_proposal_not_started','output':str(output),'descriptor_sha256':hashlib.sha256(b).hexdigest(),
        'input_files':4,'input_bytes':sum(r['bytes'] for r in record['inputs']),'network_bytes':0,'caps':CAPS,
        'retained_roots_bytes_at_preparation':prior_bytes,'available_combined_root_allowance_bytes':CAPS['root_bytes']-prior_bytes,
        'cleanup_inventory_only':candidates,'sources_deleted':0,
        'note':'Descriptive orthogonal junction control only; no efficacy/PSI/effect inference.'}

def stage(plan,gsm,root):
    import pysam
    d=root/gsm;d.mkdir();cmd=plan['commands'][gsm]
    save(root/'progress.json',{'phase':'fastp','library':gsm,'network_bytes':0})
    with (d/'fastp.log').open('wb') as log:subprocess.run(cmd['fastp'],stdout=log,stderr=subprocess.STDOUT,check=True)
    if any(not Path(p).is_file() or Path(p).stat().st_size==0 for p in cmd['plain_files']):raise ValueError('No retained paired preprocessing output')
    save(root/'progress.json',{'phase':'alignment_and_stmn2_count','library':gsm,'network_bytes':0})
    with (d/'hisat2.log').open('wb') as log:
        proc=subprocess.Popen(cmd['align'],stdout=subprocess.PIPE,stderr=log)
        try:
            with pysam.AlignmentFile(proc.stdout,'r') as sam:
                if sam.get_reference_length('chr8')!=145138636:raise ValueError('chr8 header mismatch')
                result=counter.count_records(sam,EXPECTED_TARGETS)
            if proc.wait()!=0:raise ValueError('Alignment failed')
        finally:
            if proc.poll() is None:proc.terminate()
    result.update(gsm=gsm,project='SRP482832',gene='STMN2',complete=True)
    save(d/'stmn2-counts.json',result)
    for p in cmd['plain_files']:Path(p).unlink()
    return result

def worker(path):
    plan=read(path);root=Path(plan['run_root']);accepted=read(root/'accepted.json')
    if os.getpgrp()!=os.getpid() or accepted['supervisor_pid']!=os.getppid() or accepted['plan_sha256']!=prep.sha256(path) or accepted['network_bytes']!=0:raise ValueError('Active accepting supervisor required')
    try:
        validate(plan)
        result={'project':'SRP482832','gene':'STMN2','analysis':'orthogonal descriptive splice response only; no protein efficacy/effect/PSI','libraries':[],'network_bytes':0}
        for gsm in prep.SELECTED:result['libraries'].append(stage(plan,gsm,root))
        result['status']='completed';save(root/'result.json',result)
    except BaseException as exc:
        save(root/'worker-failure.json',{'status':'failed_partial_not_interpretable','error':str(exc)});raise

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
if __name__=='__main__':main()
