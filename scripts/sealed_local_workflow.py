"""Fixed local synthetic workflow with parent seal after group supervision.

Production is disabled. HTTP origins must be literal loopback. The only executed
producer replays an existing synthetic SAM and checks prefix names, not alignment.
"""
import argparse
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import resource
import shutil
import subprocess
import sys
import time
from urllib.parse import urlsplit

import pilot_execution_policy as execution
from paired_fastq_integrity import file_digest
from paired_fastq_phase import digest,sha,verify_phase
from archive_ledger_phase import verify_archive
from compact_ledger_phase import decoder_identity,coverage
from process_supervisor_v2 import atomic_json,supervise
from workflow_seal import read as read_metadata,sha as metadata_sha,assert_seal,check_outer,FILES,MAX_METADATA

PRODUCTION_ENABLED=False


def producer_identity():
    return {'python_sha256':sha(sys.executable),'script_sha256':sha(Path(__file__).with_name('synthetic_sam_producer.py')),
            'worker_sha256':sha(__file__),'seal_code_sha256':sha(Path(__file__).with_name('workflow_seal.py'))}


def validate_descriptor(manifest,limits):
    execution.validate(manifest.get('execution_policy'),limits)
    spec=manifest.get('sealed_workflow')
    if not isinstance(spec,dict) or set(spec)!={'schema','mode','origins','steps','producer'} or spec['schema']!='b1-local-workflow-v1' or spec['mode']!='synthetic-only':raise ValueError('Synthetic sealed workflow required; production disabled')
    if not isinstance(spec['origins'],list) or not 1<=len(spec['origins'])<=4:raise ValueError('Exact bounded origin inventory required')
    for origin in spec['origins']:
        p=urlsplit(origin)
        if p.scheme!='http' or p.username or p.password or p.path or p.query or p.fragment or not ipaddress.ip_address(p.hostname).is_loopback:raise ValueError('Literal loopback origins only')
    if not isinstance(spec['steps'],list) or not 1<=len(spec['steps'])<=32:raise ValueError('Fixed bounded steps required')
    names=[]
    for step in spec['steps']:
        if not isinstance(step,dict) or not re.fullmatch('[A-Za-z0-9_-]+',step.get('name','')):raise ValueError('Named workflow step required')
        name=step['name'];kind=step.get('kind');names.append(name)
        if kind=='http':
            if set(step)!={'name','kind','url','expected'}:raise ValueError('HTTP step schema')
            p=urlsplit(step['url'])
            if f'{p.scheme}://{p.netloc}' not in spec['origins'] or p.username or p.password or p.fragment:raise ValueError('Workflow origin mismatch')
            from artifact_checksums import validate_expected
            validate_expected(step['expected'])
        elif kind in ('archive','paired_fastq','stream_compute'):
            if set(step)!={'name','kind'}:raise ValueError('Fixed workflow step schema')
            if kind=='stream_compute' and manifest.get('stream_compute',{}).get(name,{}).get('scope')!='synthetic-replay-only':raise ValueError('Real aligner disabled in local descriptor')
        else:raise ValueError('Free commands or unsupported workflow step')
        cap=manifest['execution_policy']['phases'].get(name)
        expected_kind={'http':'transfer','stream_compute':'compact'}.get(kind,kind)
        if cap is None or cap['kind']!=expected_kind:raise ValueError('Workflow step lacks matching policy')
    if len(names)!=len(set(names)):raise ValueError('Duplicate workflow phase')
    return spec


def stream_contract(runner,name,rehash=True):
    spec=runner.manifest.get('stream_compute',{}).get(name)
    keys={'scope','paired_phase','archive_phase','fixture_transfer','index_prefix','library','targets','limits','decoder','minimum_fragment_union','behavior'}
    if isinstance(spec,dict) and spec.get('scope')=='fixed-hisat2-disabled':keys=keys|{'aligner'}
    if not isinstance(spec,dict) or set(spec)!=keys or spec['scope'] not in ('synthetic-replay-only','fixed-hisat2-disabled') or spec['behavior'] not in ('ok','exit7','stall'):raise ValueError('Fixed stream contract required')
    if type(spec['minimum_fragment_union']) is not int or spec['minimum_fragment_union']<=0:raise ValueError('Union threshold required')
    from compact_pe_pipeline import validate
    validate(spec['library'],spec['targets'],spec['limits'])
    if spec['decoder']!=decoder_identity() or runner.manifest['sealed_workflow']['producer']!=producer_identity():raise ValueError('Worker/producer/decoder identity changed')
    if spec['limits']['max_temp_bytes']>runner.policy['allocations']['temporaries'] or 2*spec['limits']['max_result_bytes']>runner.policy['allocations']['receipts']:raise ValueError('Stream budgets exceed policy')
    pair=runner.state['phases'].get(spec['paired_phase'],{});archive=runner.state['phases'].get(spec['archive_phase'],{});fixture=runner.state['phases'].get(spec['fixture_transfer'],{})
    inputs=(pair,archive,fixture) if spec['scope']=='synthetic-replay-only' else (pair,archive)
    if pair.get('kind')!='paired_fastq' or archive.get('kind')!='archive' or (spec['scope']=='synthetic-replay-only' and fixture.get('kind')!='transfer') or any(p.get('status')!='verified' for p in inputs):raise ValueError('Verified input provenance required')
    if spec['scope']=='fixed-hisat2-disabled' and (spec['fixture_transfer'] is not None or spec['behavior']!='ok'):raise ValueError('Real adapter cannot replay fixture or inject behavior')
    from archive_ledger_phase import safe_name
    index=safe_name(spec['index_prefix'])
    expected_members={index+f'.{i}.ht2' for i in range(1,9)}
    inventory={m['name'] for m in runner.manifest['archives'][spec['archive_phase']]['members']}
    if not expected_members<=inventory:raise ValueError('Eight index members required')
    if rehash:
        verify_phase(runner,spec['paired_phase'],pair);verify_archive(runner,spec['archive_phase'],archive)
        if spec['scope']=='synthetic-replay-only' and file_digest(runner.root/spec['fixture_transfer'],runner.guard)!={'bytes':fixture['bytes'],'sha256':fixture['sha256']}:raise ValueError('Replay source changed')
    binding={'policy':'sealed-stream-v1','spec':spec,'fingerprint':runner.state['fingerprint'],'paired_phase_sha256':digest(pair),'archive_phase_sha256':digest(archive),'fixture_transfer_sha256':digest(fixture),'producer':producer_identity()}
    if spec['scope']=='fixed-hisat2-disabled':binding['real_argv_plan']=fixed_hisat2_plan(runner.root,spec)
    if 'attempts_used' in fixture:
        path=runner.root/f"{spec['fixture_transfer']}.attempt-{fixture['attempts_used']-1}.json";r=read_metadata(path)
        if r.get('status')!='verified' or r.get('sha256')!=fixture['sha256'] or r.get('body_bytes')!=fixture['bytes']:raise ValueError('Replay HTTP receipt incomplete')
        binding['fixture_http_sha256']=metadata_sha(path)
    return binding,digest(binding)


def alignment_plan(root,spec):
    from archive_ledger_phase import safe_name
    if any(not isinstance(spec.get(k),str) or not re.fullmatch('[A-Za-z0-9_-]+',spec[k]) for k in ('archive_phase','paired_phase')):raise ValueError('Named alignment provenance required')
    safe_name(spec['index_prefix'])
    root=Path(root);prefix=root/'archives'/spec['archive_phase']/'files'/spec['index_prefix'];pair=root/'paired-fastq'/spec['paired_phase']
    return {'execution_enabled':False,'argv':['<verified-hisat2-align-s>','-x',str(prefix),'-1',str(pair/'prefix-R1.fastq.gz'),'-2',str(pair/'prefix-R2.fastq.gz'),'-S','/dev/stdout','--no-mixed','--no-discordant','--fr','-p','2','--seed','0'],
            'scope':'plan only; synthetic index bytes are not a HISAT2 index; replay does not align or derive SAM from FASTQ/index'}


def fixed_hisat2_plan(root,spec):
    aligner=spec.get('aligner')
    if not isinstance(aligner,dict) or set(aligner)!={'path','sha256','version'} or aligner['version']!='2.2.3':raise ValueError('Pinned HISAT2 descriptor required')
    executable=Path(aligner['path'])
    if not executable.is_absolute() or not executable.is_file() or not os.access(executable,os.X_OK) or sha(executable)!=aligner['sha256']:raise ValueError('Aligner binary changed or not executable')
    plan=alignment_plan(root,spec);plan['argv'][0]=str(executable)
    plan.update(scope='fixed HISAT2 argv contract; binary/index runtime validation remains B5',execution_enabled=False,aligner=aligner)
    return plan


def run_stream(runner,name):
    requested=runner.manifest.get('stream_compute',{}).get(name,{})
    if requested.get('scope')=='fixed-hisat2-disabled' and not PRODUCTION_ENABLED:raise ValueError('Production alignment execution disabled')
    binding,signature=stream_contract(runner,name,rehash=False)
    if not runner.begin(name,'compact',signature):verify_stream(runner,name,runner.state['phases'][name]);return
    phase=runner.state['phases'][name];phase['binding']=binding;runner.save();process=None
    try:
        if stream_contract(runner,name)!=(binding,signature):raise ValueError('Input binding changed')
        spec=binding['spec'];prefix=runner.root/'paired-fastq'/spec['paired_phase']
        logs=runner.root/'producer-logs';logs.mkdir(exist_ok=True)
        argv=fixed_hisat2_plan(runner.root,spec)['argv'] if spec['scope']=='fixed-hisat2-disabled' else [sys.executable,str(Path(__file__).with_name('synthetic_sam_producer.py')),'--sam',str(runner.root/spec['fixture_transfer']),'--r1',str(prefix/'prefix-R1.fastq.gz'),'--r2',str(prefix/'prefix-R2.fastq.gz'),'--behavior',spec['behavior']]
        from compact_pe_pipeline import run
        with (logs/(name+'.log')).open('xb') as log:
            process=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=log)
            def finish():
                code=process.wait(timeout=runner.remaining(name,'compact'))
                if code==0:runner.compact_reduction(name)
                return code
            with process.stdout as stream:result=run(stream,runner.root/'compact'/name,spec['library'],spec['targets'],spec['limits'],finish,checkpoint=runner.guard)
        if (spec['scope']=='synthetic-replay-only' and result['source_sha256']!=runner.state['phases'][spec['fixture_transfer']]['sha256']) or stream_contract(runner,name)!=(binding,signature):raise ValueError('Producer stream/provenance changed')
        metric=coverage(result,spec);out=runner.root/'compact'/name
        atomic_json(out/'receipt.json',{'status':'verified','binding':binding,'result_sha256':sha(out/'result.json'),'coverage':metric,'producer_argv':argv,'alignment_plan':alignment_plan(runner.root,spec),'raw_execution_ready':False})
        phase.update(status='verified',receipt_sha256=sha(out/'receipt.json'),coverage=metric);runner.guard();runner.save()
    except BaseException as exc:
        if process is not None:
            if process.poll() is None:process.kill()
            process.wait()
        phase.update(status='failed',error_type=type(exc).__name__);runner.save();raise


def verify_stream(runner,name,phase):
    binding,signature=stream_contract(runner,name)
    if binding!=phase['binding'] or signature!=phase['signature']:raise ValueError('Stream binding changed')
    out=runner.root/'compact'/name
    if sha(out/'receipt.json')!=phase['receipt_sha256']:raise ValueError('Stream receipt changed')
    receipt=read_metadata(out/'receipt.json');result=read_metadata(out/'result.json')
    if receipt.get('status')!='verified' or receipt['binding']!=binding or receipt['result_sha256']!=sha(out/'result.json') or result.get('status')!='verified' or result.get('producer_exit_code')!=0:raise ValueError('Incomplete sealed stream result')
    if (binding['spec']['scope']=='synthetic-replay-only' and result['source_sha256']!=runner.state['phases'][binding['spec']['fixture_transfer']]['sha256']) or receipt['coverage']!=coverage(result,binding['spec']) or phase['coverage']!=receipt['coverage']:raise ValueError('Stream result/coverage mismatch')


def worker(job,verify_name=None):
    from pilot_dry_runner import DryRunner
    root=Path(job['root']);manifest=job['manifest'];limits=job['limits'];spec=validate_descriptor(manifest,limits)
    if verify_name is not None and not re.fullmatch('[A-Za-z0-9_-]+',verify_name):raise ValueError('Verification receipt name')
    r=DryRunner(root,manifest,limits)
    try:
        if verify_name:
            folder=root/'verifications';folder.mkdir(exist_ok=True)
            atomic_json(folder/(verify_name+'.json'),{'status':'verified','seal_sha256':metadata_sha(root/'workflow-seal.json'),'ledger_sha256':metadata_sha(root/'ledger.json'),'no_new_transfer':True});return
        if spec['producer']!=producer_identity():raise ValueError('Producer code changed')
        completed=[];outcome='complete'
        for step in spec['steps']:
            name=step['name'];kind=step['kind'];caps=r.phase_policy(name,{'http':'transfer','stream_compute':'compact'}.get(kind,kind))
            _,hard=resource.getrlimit(resource.RLIMIT_AS);resource.setrlimit(resource.RLIMIT_AS,(caps['address_space_bytes'],hard))
            if kind=='http':
                from bounded_http_transport import transfer_http
                transfer_http(r,name,step['url'],step['expected'],spec['origins'],reserve_reads=True)
            elif kind=='archive':r.archive(name)
            elif kind=='paired_fastq':r.paired_fastq(name)
            else:run_stream(r,name)
            completed.append(name)
            if r.state['phases'][name].get('coverage',{}).get('adequate') is False:outcome='coverage_insufficient';break
        atomic_json(root/'workflow-inner.json',{'status':outcome,'completed_steps':completed,'ledger_sha256':metadata_sha(root/'ledger.json'),'raw_execution_ready':False})
    finally:r.close()


def monitor(root,manifest,limits,start):
    policy=manifest['execution_policy']
    def clocks_disk():
        if time.monotonic()-start>=policy['total_seconds']:raise RuntimeError('Workflow total monotonic cap')
        if (root/'ledger.json').exists():
            state=read_metadata(root/'ledger.json');now=time.time()
            if now>=state['deadline_epoch']:raise RuntimeError('Workflow global deadline')
            execution.guard_clocks(state,policy,now)
            usage=execution.disk_usage(root,state)
            if sum(usage.values())>limits['disk_bytes'] or any(usage[k]>policy['allocations'][k] for k in usage):raise RuntimeError('Workflow disk budget')
        if shutil.disk_usage(root).free<limits['reserve_bytes']:raise RuntimeError('Workflow disk reserve')
    def memory(rss,members,identity):
        if not (root/'ledger.json').exists():return
        state=read_metadata(root/'ledger.json')
        active=[p for n,p in state['phases'].items() if p['status']=='started']
        if active:
            name=next(n for n,p in state['phases'].items() if p['status']=='started')
            if rss>policy['phases'][name]['rss_bytes']:raise RuntimeError('Workflow phase RSS cap')
    return clocks_disk,memory


def run_workflow(root,manifest,limits):
    validate_descriptor(manifest,limits);root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True)
    job={'root':str(root),'manifest':manifest,'limits':limits}
    payload=(json.dumps(job,sort_keys=True)+'\n').encode()
    if len(payload)>MAX_METADATA:raise ValueError('Descriptor size cap')
    with (root/'workflow-job.json').open('xb') as f:f.write(payload);f.flush();os.fsync(f.fileno())
    start=time.monotonic();checkpoint,memory=monitor(root,manifest,limits,start)
    caps=limits['process_caps']
    rec=supervise('run',[sys.executable,str(Path(__file__).resolve()),'--job',str(root/'workflow-job.json')],root/'workflow-receipts',timeout=limits['wall_seconds'],rss_limit=caps['rss_bytes'],address_space=caps['address_space_bytes'],checkpoint=checkpoint,group_checkpoint=memory)
    check_outer(rec);inner=read_metadata(root/'workflow-inner.json');ledger=read_metadata(root/'ledger.json')
    if inner.get('status') not in ('complete','coverage_insufficient') or inner.get('ledger_sha256')!=metadata_sha(root/'ledger.json') or any(p['status']!='verified' for p in ledger['phases'].values()):raise ValueError('Workflow inner result incomplete')
    seal={'status':'sealed','technical_status':inner['status'],'sha256':{name:metadata_sha(root/name) for name in FILES},'raw_execution_ready':False}
    atomic_json(root/'workflow-seal.json',seal)
    return seal


def verify_workflow(root,name='reuse'):
    if not re.fullmatch('[A-Za-z0-9_-]+',name):raise ValueError('Verification receipt name')
    root=Path(root).resolve();job=read_metadata(root/'workflow-job.json');assert_seal(root,job['manifest'],job['limits'])
    state=read_metadata(root/'ledger.json');remaining=state['deadline_epoch']-time.time()
    if remaining<=0:raise RuntimeError('Original workflow deadline expired')
    checkpoint,memory=monitor(root,job['manifest'],job['limits'],time.monotonic());caps=job['limits']['process_caps']
    rec=supervise(name,[sys.executable,str(Path(__file__).resolve()),'--job',str(root/'workflow-job.json'),'--verify',name],root/'workflow-verification-receipts',timeout=min(remaining,caps['wall_seconds']),rss_limit=caps['rss_bytes'],address_space=caps['address_space_bytes'],checkpoint=checkpoint,group_checkpoint=memory)
    check_outer(rec);return read_metadata(root/'verifications'/(name+'.json'))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--job',type=Path,required=True);p.add_argument('--verify');a=p.parse_args();worker(read_metadata(a.job),a.verify)
