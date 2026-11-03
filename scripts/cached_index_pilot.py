"""Prepare a bounded technical pilot using a sealed extracted index.

No index download, copy or extraction. --prepare only emits a disabled plan.
--execute accepts the exact plan SHA, including a NEW7200s/1800s transfer window.
The previous byte charge and spent clocks are preserved, never silently reset.
"""
import argparse
import copy
import os
from pathlib import Path
import shutil
import sys
import time
import json

import real_pilot_workflow as real
import prepare_verified_index as offline
import pilot_execution_policy as execution
from pilot_dry_runner import digest
from paired_fastq_integrity import file_digest
from paired_fastq_phase import verify_phase
from workflow_seal import read,sha as meta_sha,check_outer
from process_supervisor_v2 import atomic_json

GiB=1024**3
INDEX_FILES=('index-job.json','index-state.json','preflight.json','index/extraction.json','index-summary.json','index-result.json','supervision/run.json')
CODE=tuple(sorted(set(offline.CODE+('cached_index_pilot.py',))))


def identity():
    return {'python_sha256':file_digest(sys.executable)['sha256'],
        'code_sha256':{n:file_digest(Path(__file__).with_name(n))['sha256'] for n in CODE},
        'decoder':real.decoder_identity()}


def index_binding(root):
    root=Path(root).resolve();seal=read(root/'index-seal.json')
    if seal.get('status')!='sealed_verified_extracted_index' or set(seal.get('sha256',{}))!=set(INDEX_FILES):raise ValueError('Sealed extracted index required')
    for name in INDEX_FILES:
        if (root/name).is_symlink() or meta_sha(root/name)!=seal['sha256'][name]:raise ValueError('Sealed index metadata changed')
    job=read(root/'index-job.json');result=read(root/'index-result.json');state=read(root/'index-state.json');check_outer(read(root/'supervision/run.json'))
    recovered=offline.recovery_binding(job['recovery']['root'])
    expected_spec=offline.make_spec();prefix=str(root/'index/files/hg38/genome')
    if job.get('schema')!='offline-verified-index-v1' or job.get('root')!=str(root) or job.get('recovery')!=recovered or job.get('archive_spec')!=expected_spec:raise ValueError('Index provenance/inventory changed')
    if state.get('status')!='verified' or set(state.get('phases',{}))!=set(offline.PHASES) or any(p.get('status')!='verified' for p in state['phases'].values()):raise ValueError('Index phases incomplete')
    if result.get('status')!='verified_index_pending_outer_seal' or result.get('state_sha256')!=meta_sha(root/'index-state.json') or result.get('members')!=expected_spec['members'] or result.get('index_prefix')!=prefix or seal.get('index_prefix')!=prefix or seal.get('member_count')!=9 or result.get('source_archive_sha256')!=recovered['expected']['sha256']:raise ValueError('Index result incomplete')
    for rec in (seal,result,state):
        if rec.get('new_transfer_bytes')!=0 or rec.get('cumulative_body_bytes')!=recovered['cumulative_body_bytes']:raise ValueError('Index cumulative accounting mismatch')
    if result.get('remaining_body_budget_bytes')!=recovered['remaining_body_budget_bytes'] or seal.get('remaining_body_budget_bytes')!=recovered['remaining_body_budget_bytes']:raise ValueError('Index remaining body cap mismatch')
    recovery_result=read(Path(recovered['root'])/'recovery-result.json')
    return {'schema':'sealed-extracted-index-v1','index_root':str(root),'index_prefix':prefix,
        'index_seal_sha256':meta_sha(root/'index-seal.json'),'recovery_root':recovered['root'],
        'original_root':recovered['original_root'],'cumulative_body_bytes':recovered['cumulative_body_bytes'],
        'remaining_body_budget_bytes':recovered['remaining_body_budget_bytes'],
        'prior_transfer_elapsed_seconds':recovery_result['prior_transfer_elapsed_seconds']+recovery_result['additional_transfer_elapsed_seconds'],
        'prior_global_deadline_epoch':read(Path(recovered['root'])/'recovery-plan.json')['original_audit']['prior_global_deadline_epoch'],
        'aligner':job['aligner'],'members':expected_spec['members']}


def output_root(binding):return Path(binding['index_root']).with_name(Path(binding['index_root']).name+'-reads-01')


def make_manifest(aligner,binding):
    observed=index_binding(binding['index_root'])
    if observed!=binding or aligner!=binding['aligner']:raise ValueError('Cached index or aligner identity changed')
    manifest,limits=real.make_manifest(aligner);manifest=copy.deepcopy(manifest);limits=copy.deepcopy(limits)
    manifest['cached_index']=binding;manifest['cached_guard_sample_seconds']=.1
    limits['wall_seconds']=7200
    policy=manifest['execution_policy'];policy['total_seconds']=7200;policy['transfer_seconds']=1800
    for name in ('index_archive','index_extract','index_probe'):policy['phases'].pop(name)
    policy['phases']['preflight']['wall_seconds']=180
    for p in policy['phases'].values():
        if p['kind']=='transfer':p['wall_seconds']=1800
    manifest['archives']={}
    manifest['sealed_workflow'].update(schema='cached-index-pilot-v1',origins=['https://ftp.sra.ebi.ac.uk'],
        steps=[s for s in manifest['sealed_workflow']['steps'] if s['name'] not in ('index_archive','index_extract','index_probe')],producer=identity())
    for spec in manifest['real_compute'].values():spec['archive_phase']='cached_index'
    execution.validate(policy,limits,allow_real=True)
    if sum(s['expected']['bytes'] for s in manifest['sealed_workflow']['steps'] if s['kind']=='http')>limits['transfer_bytes']-binding['cumulative_body_bytes']:raise ValueError('Reads exceed remaining original body cap')
    return manifest,limits


def validate_manifest(manifest,limits):
    binding=manifest.get('cached_index')
    if not isinstance(binding,dict):raise ValueError('Verified cache binding required')
    expected,caps=make_manifest(manifest.get('aligner'),binding)
    if manifest!=expected or limits!=caps:raise ValueError('Fixed cached pilot origins/samples/caps/code changed')
    return manifest['sealed_workflow']


def prepare(root):
    binding=index_binding(Path(root).expanduser().resolve());manifest,limits=make_manifest(binding['aligner'],binding)
    out=output_root(binding)
    if out.exists():raise ValueError('Cached pilot directory exists; no retry or renewed budget')
    return {'schema':'b5-prepared-real-pilot-v1','execution_enabled':False,'root':str(out),'manifest':manifest,'limits':limits,
        'host_observed':real.check_host(out,limits),'unverified':['actual human alignment resources and target coverage'],
        'scope':'NEW cached-index pilot window7200s total/1800s additional HTTP; old spent clocks and body charges preserved; two technical libraries, no biological inference'}


def lineage_usage(binding):
    total=0
    for root in (binding['original_root'],binding['recovery_root'],binding['index_root']):
        for path in execution.iter_files(root):
            try:
                if path.is_symlink():raise ValueError('Cached lineage symlink refused')
                if path.is_file():total+=path.stat().st_size
            except FileNotFoundError:pass
    return total


def combined_disk_guard(root,state,manifest,limits):
    usage=execution.disk_usage(root,state);extra=lineage_usage(manifest['cached_index']);usage['artifacts']+=extra
    if sum(usage.values())>limits['disk_bytes'] or any(usage[k]>manifest['execution_policy']['allocations'][k] for k in usage):raise RuntimeError('Cached pilot cumulative disk/partition cap')
    if shutil.disk_usage(root).free<limits['reserve_bytes']:raise RuntimeError('Cached pilot free disk reserve')


def guard_runner(runner,now):
    if runner.state['transfer_bytes_consumed']<runner.manifest['cached_index']['cumulative_body_bytes']:raise RuntimeError('Prior body charge cannot be reset/refunded')
    tick=time.monotonic()
    if tick-getattr(runner,'cached_last_disk_check',float('-inf'))>=runner.manifest['cached_guard_sample_seconds']:
        combined_disk_guard(runner.root,runner.state,runner.manifest,runner.state['limits']);runner.cached_last_disk_check=tick


def monitor(root,manifest,limits,start):
    clocks,memory=real.local_monitor(root,manifest,limits,start);root=Path(root);last=[float('-inf')]
    def guard():
        clocks()
        if (root/'ledger.json').exists():
            state=read(root/'ledger.json')
            if state['transfer_bytes_consumed']<manifest['cached_index']['cumulative_body_bytes']:raise RuntimeError('External prior body charge reset')
            tick=time.monotonic()
            if tick-last[0]>=.1:combined_disk_guard(root,state,manifest,limits);last[0]=tick
    return guard,memory


def verify_index_data(binding,guard):
    if index_binding(binding['index_root'])!=binding:raise ValueError('Cached index metadata changed')
    offline.verify_members(Path(binding['index_root'])/'index',offline.make_spec(),guard)


def run_preflight(runner,name):
    if name!='preflight':raise ValueError('Cached pilot has only one fixed preflight')
    binding=runner.manifest['cached_index'];signature=digest({'cached_index':binding,'producer':runner.manifest['sealed_workflow']['producer']})
    if not runner.begin(name,'process',signature):raise ValueError('Do not adopt cached preflight')
    phase=runner.state['phases'][name]
    try:
        host=real.check_host(runner.root,runner.state['limits']);probe=real.version_probe(runner.manifest['aligner'])
        verify_index_data(binding,runner.guard);runner.guard()
        path=runner.root/'cached-preflight.json';atomic_json(path,{'status':'verified','host':host,'probe':probe,'cached_index':binding})
        phase.update(status='verified',receipt=path.name,receipt_sha256=meta_sha(path));runner.save()
    except BaseException as exc:phase.update(status='failed',error_type=type(exc).__name__);runner.save();raise


def verify_preflight(runner,phase):
    binding=runner.manifest['cached_index'];path=runner.root/'cached-preflight.json'
    if phase.get('receipt')!=path.name or meta_sha(path)!=phase['receipt_sha256']:raise ValueError('Cached preflight receipt changed')
    rec=read(path)
    if rec.get('status')!='verified' or rec.get('cached_index')!=binding or rec.get('probe',{}).get('sha256')!=runner.manifest['aligner']['sha256'] or phase.get('signature')!=digest({'cached_index':binding,'producer':runner.manifest['sealed_workflow']['producer']}):raise ValueError('Cached preflight binding changed')
    verify_index_data(binding,runner.guard)


def stream_binding(runner,name):
    spec=runner.manifest['real_compute'][name];cached=runner.manifest['cached_index'];preflight=runner.state['phases'].get('preflight',{})
    if preflight.get('status')!='verified' or preflight.get('kind')!='process':raise ValueError('Verified cached preflight required')
    verify_preflight(runner,preflight)
    paired=runner.state['phases'].get(spec['paired_phase'],{})
    if paired.get('status')!='verified' or paired.get('kind')!='paired_fastq':raise ValueError('Verified paired prefix required')
    verify_phase(runner,spec['paired_phase'],paired)
    if runner.manifest['sealed_workflow']['producer']!=identity():raise ValueError('Cached pilot code/decoder changed')
    real.validate_aligner(runner.manifest['aligner']);argv=real.alignment_argv(runner.root,spec,runner.manifest['aligner']);argv[argv.index('-x')+1]=cached['index_prefix']
    value={'policy':'real-stream-v1','spec':spec,'fingerprint':runner.state['fingerprint'],
        'paired_sha256':digest(paired),'cached_index':cached,'preflight_sha256':digest(preflight),
        'argv':argv,'aligner':runner.manifest['aligner'],'producer':identity()}
    return value,digest(value)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--prepare',type=Path);g.add_argument('--execute',type=Path);p.add_argument('--index',type=Path);p.add_argument('--accept-plan-sha256');p.add_argument('--accept-new-run-window',action='store_true');a=p.parse_args()
    if a.prepare:
        if not a.index:p.error('--prepare requires --index')
        job=prepare(a.index)
        with a.prepare.open('x') as f:json.dump(job,f,indent=2);f.write('\n')
        binding=job['manifest']['cached_index'];needed=sum(s['expected']['bytes'] for s in job['manifest']['sealed_workflow']['steps'] if s['kind']=='http')
        print(json.dumps({'prepared_file':str(a.prepare),'sha256':meta_sha(a.prepare),'execution_enabled':False,
            'root':job['root'],'new_index_transfer_bytes':0,'planned_read_body_bytes':needed,
            'prior_charged_body_bytes':binding['cumulative_body_bytes'],'expected_cumulative_body_bytes_if_both_libraries_downloaded':binding['cumulative_body_bytes']+needed,
            'new_total_wall_seconds':job['limits']['wall_seconds'],'new_transfer_seconds':job['manifest']['execution_policy']['transfer_seconds'],
            'scope':job['scope'],'raw_execution_ready':False},indent=2))
    else:print(json.dumps(real.execute(a.execute,a.accept_plan_sha256,accept_cached_window=a.accept_new_run_window),indent=2))
