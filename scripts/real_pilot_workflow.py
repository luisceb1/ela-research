"""Prepared two-library real pilot. Default CLI is read-only preparation.

Real execution requires --execute plus acceptance of the exact prepared file's
SHA256. No command in this module runs at import. This is technical feasibility,
not a biological contrast. Existing synthetic entrypoints stay disabled for real
policies. Human-scale runtime/index compatibility is not certified by unit tests.
"""
import argparse
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import resource
import shutil
import subprocess
import sys
import time

import pilot_execution_policy as execution
from pilot_dry_runner import DryRunner, digest
from process_supervisor_v2 import atomic_json, supervise
from workflow_seal import read, sha as metadata_sha, check_outer, assert_seal, FILES
from paired_fastq_integrity import file_digest
from paired_fastq_phase import verify_phase
from archive_ledger_phase import verify_archive
from compact_ledger_phase import decoder_identity, coverage
from sealed_local_workflow import monitor
from plan_b4_execution_policy import proposal

REPO=Path(__file__).resolve().parents[1]
GiB=1024**3
SOURCES={
    'reports/pilot-readiness-audit-20261102/execution-proposal.json':'26e37170d60aa5ac63cd611dcc1c97f8e33c1daf3cf7f14d24e90b010473421f',
    'reports/unc13a-reference-strand-20261102/contract.json':'a20ea058d038142b9a774bbd8a8c63656202ab914624cee642321408e303f7fe',
}
CODE=('real_pilot_workflow.py','plan_b4_execution_policy.py','sealed_local_workflow.py',
      'workflow_seal.py','bounded_http_transport.py','artifact_checksums.py',
      'archive_ledger_phase.py','paired_fastq_phase.py','paired_fastq_integrity.py',
      'pilot_dry_runner.py','pilot_execution_policy.py','compact_pe_pipeline.py',
      'compact_ledger_phase.py','pe_fragment_contract.py','process_supervisor_v2.py',
      'external_local_stage.py','synthetic_sam_producer.py')


def sources():
    values=[]
    for path,expected in SOURCES.items():
        if metadata_sha(REPO/path)!=expected:raise ValueError('Pinned source changed: '+path)
        values.append(read(REPO/path))
    return values


def identity():
    return {'python_sha256':file_digest(sys.executable)['sha256'],
            'code_sha256':{n:file_digest(Path(__file__).with_name(n))['sha256'] for n in CODE},
            'decoder':decoder_identity()}


def validate_aligner(spec):
    if not isinstance(spec,dict) or set(spec)!={'path','sha256','version','source_commit','inspect_path','inspect_sha256'} or spec['version']!='2.2.3' or spec['source_commit']!='0d244324f98de541bce04d45c75e83bc3522f7f4':raise ValueError('Pinned HISAT2 2.2.3 source contract required')
    p=Path(spec['path'])
    if not p.is_absolute() or p.name!='hisat2-align-s' or p.is_symlink() or not p.is_file() or not os.access(p,os.X_OK):raise ValueError('Absolute regular hisat2-align-s executable required')
    with p.open('rb') as f:
        if f.read(4)!=b'\x7fELF':raise ValueError('Native ELF aligner required')
    if file_digest(p)['sha256']!=spec['sha256']:raise ValueError('Aligner binary changed')
    inspector=Path(spec['inspect_path'])
    if not inspector.is_absolute() or inspector.name!='hisat2-inspect-s' or inspector.is_symlink() or not inspector.is_file() or not os.access(inspector,os.X_OK):raise ValueError('Absolute regular hisat2-inspect-s required')
    with inspector.open('rb') as f:
        if f.read(4)!=b'\x7fELF':raise ValueError('Native ELF inspector required')
    if file_digest(inspector)['sha256']!=spec['inspect_sha256']:raise ValueError('Index inspector binary changed')


def make_manifest(aligner):
    validate_aligner(aligner)
    old,reference=sources();planned=proposal();policy=copy.deepcopy(planned['execution_policy'])
    policy.update(schema='pilot-b4-real-v1',production_enabled=True)
    # Spend 120 of the existing 480 spare seconds on runtime index inspection.
    policy['phases']['index_probe']={'kind':'process','wall_seconds':120,'rss_bytes':6*GiB,'address_space_bytes':8*GiB}
    ref=old['reference'];expected={'bytes':ref['expected_bytes'],'sha256':ref['sha256']}
    steps=[{'name':'preflight','kind':'process'}, {'name':'index_archive','kind':'http','url':ref['url'],'expected':expected}, {'name':'index_extract','kind':'archive'}, {'name':'index_probe','kind':'process'}]
    manifest={'transport':{'read_chunk_bytes':65536,'reservation_block_bytes':4*1024**2,'attempts':1},'execution_policy':policy,'aligner':aligner,'archives':{'index_extract':{
        'transfer':'index_archive','identity':'pinned-hg38-hisat2-index','expected':expected,
        'members':ref['members'],'max_members':16,'max_expanded_bytes':sum(m['bytes'] for m in ref['members']),
        'max_tar_bytes':sum(m['bytes']+((-m['bytes'])%512)+512 for m in ref['members'])+1024*1024}},
        'paired_fastq':{},'real_compute':{}}
    targets=[[reference['chromosome'],e['start0'],e['end0'],reference['transcript_strand']] for e in reference['events']]
    for label,selected in zip(('CTRL','TDP'),old['selected']):
        mates=[]
        for i,mate in enumerate(selected['mates'],1):
            name=f'{label}_R{i}';expected={'bytes':mate['bytes'],'md5':mate['md5']}
            steps.append({'name':name,'kind':'http','url':mate['url'],'expected':expected})
            mates.append({'transfer':name,'identity':selected['run']+f'/{i}','expected':expected})
        pair=label+'_prefix';calc=label+'_compute'
        manifest['paired_fastq'][pair]={'mates':mates,'prefix_pairs':1_000_000}
        # Plain prefix staging (2 GiB total) and compact runs (4 GiB) share
        # the existing 6 GiB temporary allocation. No larger disk envelope.
        manifest['real_compute'][calc]={'library':selected['library'],'run':selected['run'],
            'paired_phase':pair,'archive_phase':'index_extract','index_prefix':'hg38/genome',
            'targets':targets,'minimum_fragment_union':20,'max_plaintext_bytes':2*GiB,
            'limits':{**planned['compact_limits'],'max_temp_bytes':4*GiB}}
        steps.extend([{'name':pair,'kind':'paired_fastq'},{'name':calc,'kind':'stream_compute'}])
    manifest['sealed_workflow']={'schema':'b5-fixed-real-v1','mode':'real-pilot',
        'origins':['https://genome-idx.s3.amazonaws.com','https://ftp.sra.ebi.ac.uk'],
        'steps':steps,'producer':identity()}
    return manifest,planned['limits']


def validate_manifest(manifest,limits):
    expected,expected_limits=make_manifest(manifest.get('aligner'))
    if manifest!=expected or limits!=expected_limits:raise ValueError('Fixed real manifest/limits changed; no sample, origin, command or cap overrides')
    execution.validate(manifest['execution_policy'],limits,allow_real=True)
    return manifest['sealed_workflow']


def version_probe(aligner):
    validate_aligner(aligner)
    process=subprocess.Popen([aligner['path'],'--version'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    try:
        output=process.stdout.read(65537)
        if len(output)>65536:raise ValueError('Version output cap')
        if process.wait(timeout=10)!=0:raise ValueError('HISAT2 version probe failed')
        text=output.decode('utf-8','strict')
        if re.search(r'\bhisat2-align-s version 2\.2\.3(?:\s|$)',text) is None:raise ValueError('HISAT2 runtime version mismatch')
        validate_aligner(aligner)
        return {'argv':[aligner['path'],'--version'],'output':text,'sha256':aligner['sha256']}
    finally:
        process.stdout.close()
        if process.poll() is None:process.kill()
        process.wait()


def index_probe(runner):
    phase=runner.state['phases'].get('index_extract',{})
    if phase.get('status')!='verified':raise ValueError('Verified extracted index required')
    verify_archive(runner,'index_extract',phase);validate_aligner(runner.manifest['aligner'])
    argv=[runner.manifest['aligner']['inspect_path'],'-s',str(runner.root/'archives/index_extract/files/hg38/genome')]
    process=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    try:
        output=process.stdout.read(65537)
        if len(output)>65536:raise ValueError('Index summary cap')
        if process.wait(timeout=runner.remaining('index_probe','process'))!=0:raise ValueError('Index inspector failed')
        text=output.decode('utf-8','strict')
        if len(re.findall(r'^Sequence-\d+\tchr19\t58617616$',text,re.M))!=1:raise ValueError('Expected hg38 chr19 identity/length absent from index')
        verify_archive(runner,'index_extract',phase);validate_aligner(runner.manifest['aligner'])
        return {'argv':argv,'output':text,'inspect_sha256':runner.manifest['aligner']['inspect_sha256'],
                'archive_phase_sha256':digest(phase),'scope':'index summary only; not full sequence equality or alignment benchmark'}
    finally:
        process.stdout.close()
        if process.poll() is None:process.kill()
        process.wait()


def host_report(parent):
    parent=Path(parent)
    while not parent.exists():parent=parent.parent
    memory={}
    for line in Path('/proc/meminfo').read_text().splitlines():
        if line.startswith(('MemTotal:','MemAvailable:')):
            key,val,*_=line.split();memory[key.rstrip(':')]=int(val)*1024
    # /proc may describe the host while cgroups constrain this process.
    ceiling=memory['MemTotal'];available=memory['MemAvailable']
    cgroup=Path('/sys/fs/cgroup/memory.max');current=Path('/sys/fs/cgroup/memory.current')
    if cgroup.exists() and cgroup.read_text().strip()!='max':
        maximum=int(cgroup.read_text());ceiling=min(ceiling,maximum)
        if current.exists():available=min(available,max(0,maximum-int(current.read_text())))
    return {'scope':'observed on the host executing this command, not another computer',
        'platform':platform.platform(),'architecture':platform.machine(),'python':platform.python_version(),
        'cpu_affinity_count':len(os.sched_getaffinity(0)),'memory_ceiling_bytes':ceiling,
        'memory_available_bytes':available,'disk_free_bytes':shutil.disk_usage(parent).free,
        'pysam_version':decoder_identity()['pysam_version']}


def check_host(root,limits):
    h=host_report(Path(root).parent)
    if platform.system()!='Linux' or h['architecture']!='x86_64':raise ValueError('Linux x86_64 host required')
    if sys.version_info[:2] not in ((3,11),(3,12)) or h['pysam_version']!='0.23.3':raise ValueError('Validated Python 3.11/3.12 and pinned PySAM required')
    if h['cpu_affinity_count']<2:raise ValueError('Two CPUs required')
    if h['memory_ceiling_bytes']<7*GiB or h['memory_available_bytes']<6*GiB:raise ValueError('Insufficient available RAM for proposed cap; close applications and reassess, do not auto-raise WSL memory')
    if h['disk_free_bytes']<limits['disk_bytes']+limits['reserve_bytes']:raise ValueError('33 GiB free required before pilot')
    return h


def source_commit_at(folder):
    # Observe checkout identity, not a cryptographic build attestation.
    commit=subprocess.check_output(['git','-C',str(folder),'rev-parse','HEAD'],timeout=10,text=True).strip()
    if commit!='0d244324f98de541bce04d45c75e83bc3522f7f4':raise ValueError('HISAT2 checkout does not match pinned source commit')
    subprocess.run(['git','-C',str(folder),'diff','--quiet','HEAD','--'],check=True,timeout=10)
    return commit


def prepare(root,aligner_path):
    p=Path(aligner_path).expanduser().resolve()
    commit=source_commit_at(p.parent)
    aligner={'path':str(p),'sha256':file_digest(p)['sha256'],'version':'2.2.3','source_commit':commit,
             'inspect_path':str(p.with_name('hisat2-inspect-s')),'inspect_sha256':file_digest(p.with_name('hisat2-inspect-s'))['sha256']}
    manifest,limits=make_manifest(aligner)
    return {'schema':'b5-prepared-real-pilot-v1','execution_enabled':False,'root':str(Path(root).expanduser().resolve()),
        'manifest':manifest,'limits':limits,'host_observed':check_host(root,limits),
        'unverified':['index archive dialect on this host','human alignment compatibility and resource performance'],
        'scope':'two technical libraries only; no PSI, biological effect, functional or clinical inference'}


def validate_job(job):
    if not isinstance(job,dict) or set(job)!={'schema','execution_enabled','root','manifest','limits','host_observed','unverified','scope'} or job['schema']!='b5-prepared-real-pilot-v1' or job['execution_enabled'] is not False:raise ValueError('Disabled prepared job required')
    root=Path(job['root'])
    if not root.is_absolute() or root!=root.resolve():raise ValueError('Canonical absolute output root required')
    validate_manifest(job['manifest'],job['limits'])
    return root


def stage_plain_prefixes(runner,name,spec):
    """Bounded gzip->regular FASTQ; sources already fully pair/CRC verified."""
    folder=runner.root/'alignment-inputs'/name;folder.mkdir(parents=True,exist_ok=False)
    source=runner.root/'paired-fastq'/spec['paired_phase'];results=[];total=0
    for i in (1,2):
        path=folder/f'R{i}.fastq';partial=folder/f'R{i}.partial';h=hashlib.sha256();size=0
        with gzip.open(source/f'prefix-R{i}.fastq.gz','rb') as inp,partial.open('xb') as out:
            while True:
                runner.guard();data=inp.read(min(65536,spec['max_plaintext_bytes']-total+1))
                if not data:break
                total+=len(data);size+=len(data)
                if total>spec['max_plaintext_bytes']:raise ValueError('Plaintext prefix cap')
                out.write(data);h.update(data);runner.guard()
            out.flush();os.fsync(out.fileno())
        os.replace(partial,path);results.append({'path':str(path),'bytes':size,'sha256':h.hexdigest()})
    return results


def alignment_argv(root,spec,aligner):
    index=Path(root)/'archives'/spec['archive_phase']/'files'/spec['index_prefix']
    folder=Path(root)/'alignment-inputs'/(('CTRL' if spec['run']=='SRR33425816' else 'TDP')+'_compute')
    return [aligner['path'],'-x',str(index),'-1',str(folder/'R1.fastq'),'-2',str(folder/'R2.fastq'),
            '-S','/dev/stdout','--no-mixed','--no-discordant','--fr','-p','2','--seed','0']


def stream_binding(runner,name):
    spec=runner.manifest['real_compute'][name]
    paired=runner.state['phases'].get(spec['paired_phase'],{});archive=runner.state['phases'].get(spec['archive_phase'],{})
    probe=runner.state['phases'].get('index_probe',{})
    if probe.get('status')!='verified':raise ValueError('Runtime index probe required before alignment')
    verify_preflight(runner,probe)
    if paired.get('status')!='verified' or archive.get('status')!='verified' or paired.get('kind')!='paired_fastq' or archive.get('kind')!='archive':raise ValueError('Verified pair/index provenance required')
    verify_phase(runner,spec['paired_phase'],paired);verify_archive(runner,spec['archive_phase'],archive)
    if runner.manifest['sealed_workflow']['producer']!=identity():raise ValueError('Code or decoder changed')
    validate_aligner(runner.manifest['aligner'])
    binding={'policy':'real-stream-v1','spec':spec,'fingerprint':runner.state['fingerprint'],
             'paired_sha256':digest(paired),'archive_sha256':digest(archive),
             'argv':alignment_argv(runner.root,spec,runner.manifest['aligner']),
             'aligner':runner.manifest['aligner'],'producer':identity()}
    return binding,digest(binding)


def run_stream(runner,name):
    # Called only by the real worker after explicit exact-plan acceptance.
    spec=runner.manifest['real_compute'][name]
    # Start before expensive input rehash: producer cap covers preparation too.
    signature=digest({'spec':spec,'fingerprint':runner.state['fingerprint']})
    if not runner.begin(name,'compact',signature):verify_stream(runner,name,runner.state['phases'][name]);return
    phase=runner.state['phases'][name];process=None
    try:
        binding,_=stream_binding(runner,name);phase['binding']=binding;runner.save()
        plain=stage_plain_prefixes(runner,name,spec)
        logs=runner.root/'producer-logs';logs.mkdir(exist_ok=True)
        from compact_pe_pipeline import run
        with (logs/(name+'.log')).open('xb') as log:
            process=subprocess.Popen(binding['argv'],stdout=subprocess.PIPE,stderr=log)
            def finish():
                code=process.wait(timeout=runner.remaining(name,'compact'))
                if code==0:runner.compact_reduction(name)
                return code
            with process.stdout as stream:
                result=run(stream,runner.root/'compact'/name,spec['library'],spec['targets'],spec['limits'],finish,checkpoint=runner.guard)
        for item in plain:
            if file_digest(item['path'],runner.guard)!={'bytes':item['bytes'],'sha256':item['sha256']}:raise ValueError('Plaintext prefix changed during alignment')
        if stream_binding(runner,name)[0]!=binding:raise ValueError('Input provenance changed')
        metric=coverage(result,spec);out=runner.root/'compact'/name
        atomic_json(out/'receipt.json',{'status':'verified','binding':binding,'result_sha256':metadata_sha(out/'result.json'),
            'coverage':metric,'plaintext_prefixes':plain,'plaintext_removed_on_success':True,
            'technical_real_execution':True,'raw_execution_ready':False})
        # Reclaim plaintext before next library, never promote it as a cache.
        for item in plain:Path(item['path']).unlink()
        (runner.root/'alignment-inputs'/name).rmdir()
        phase.update(status='verified',receipt_sha256=metadata_sha(out/'receipt.json'),coverage=metric)
        runner.guard();runner.save()
    except BaseException as exc:
        if process is not None:
            if process.poll() is None:process.kill()
            process.wait()
        phase.update(status='failed',error_type=type(exc).__name__);runner.save();raise


def verify_stream(runner,name,phase):
    binding,_=stream_binding(runner,name);spec=binding['spec']
    if binding!=phase['binding'] or phase['signature']!=digest({'spec':spec,'fingerprint':runner.state['fingerprint']}):raise ValueError('Real stream binding changed')
    out=runner.root/'compact'/name;receipt=read(out/'receipt.json');result=read(out/'result.json')
    if metadata_sha(out/'receipt.json')!=phase['receipt_sha256'] or receipt.get('status')!='verified' or receipt.get('binding')!=binding or receipt.get('result_sha256')!=metadata_sha(out/'result.json'):raise ValueError('Real result receipt changed')
    if result.get('status')!='verified' or result.get('producer_exit_code')!=0 or receipt.get('coverage')!=coverage(result,spec) or phase.get('coverage')!=receipt['coverage']:raise ValueError('Real producer/coverage incomplete')
    if (runner.root/'alignment-inputs'/name).exists():raise ValueError('Unexpected retained plaintext inputs')


def run_preflight(runner,name='preflight'):
    signature=digest({'aligner':runner.manifest['aligner'],'producer':runner.manifest['sealed_workflow']['producer'],'name':name})
    if not runner.begin(name,'process',signature):raise ValueError('No adopted preflight')
    p=runner.state['phases'][name]
    try:
        host=check_host(runner.root,runner.state['limits']) if name=='preflight' else None
        probe=version_probe(runner.manifest['aligner']) if name=='preflight' else index_probe(runner)
        runner.guard();path=runner.root/(name+'-result.json')
        atomic_json(path,{'host':host,'probe':probe,'status':'verified','name':name})
        p.update(status='verified',receipt=path.name,receipt_sha256=metadata_sha(path));runner.save()
    except BaseException as exc:p.update(status='failed',error_type=type(exc).__name__);runner.save();raise


def verify_preflight(runner,phase):
    if phase.get('receipt') not in ('preflight-result.json','index_probe-result.json'):raise ValueError('Unknown preflight receipt')
    path=runner.root/phase['receipt']
    if metadata_sha(path)!=phase['receipt_sha256']:raise ValueError('Real preflight receipt changed')
    rec=read(path);name=rec.get('name')
    expected=digest({'aligner':runner.manifest['aligner'],'producer':runner.manifest['sealed_workflow']['producer'],'name':name})
    key='sha256' if name=='preflight' else 'inspect_sha256'
    if phase['signature']!=expected or rec.get('status')!='verified' or rec.get('probe',{}).get(key)!=runner.manifest['aligner'][key]:raise ValueError('Real preflight incomplete')
    if name=='index_probe' and rec['probe'].get('archive_phase_sha256')!=digest(runner.state['phases']['index_extract']):raise ValueError('Index probe provenance changed')


def worker(job,verify=False):
    validate_job(job)
    runner=DryRunner(job['root'],job['manifest'],job['limits'],real_pilot=True)
    try:
        if verify:
            verify_preflight(runner,runner.state['phases']['preflight'])
            atomic_json(runner.root/'real-verification.json',{'status':'verified','no_new_transfer':True,'ledger_sha256':metadata_sha(runner.root/'ledger.json')});return
        completed=[];outcome='complete'
        for step in job['manifest']['sealed_workflow']['steps']:
            name=step['name'];kind=step['kind'];caps=runner.phase_policy(name,{'http':'transfer','stream_compute':'compact'}.get(kind,kind))
            _,hard=resource.getrlimit(resource.RLIMIT_AS);resource.setrlimit(resource.RLIMIT_AS,(caps['address_space_bytes'],hard))
            if kind=='process':run_preflight(runner,name)
            elif kind=='http':
                from bounded_http_transport import transfer_http
                transport=job['manifest']['transport']
                transfer_http(runner,name,step['url'],step['expected'],job['manifest']['sealed_workflow']['origins'],attempts=transport['attempts'],chunk_size=transport['read_chunk_bytes'],reserve_reads=True,reservation_block_bytes=transport['reservation_block_bytes'])
            elif kind=='archive':runner.archive(name)
            elif kind=='paired_fastq':runner.paired_fastq(name)
            else:run_stream(runner,name)
            completed.append(name)
            if runner.state['phases'][name].get('coverage',{}).get('adequate') is False:outcome='coverage_insufficient';break
        atomic_json(runner.root/'workflow-inner.json',{'status':outcome,'completed_steps':completed,
            'ledger_sha256':metadata_sha(runner.root/'ledger.json'),'technical_real_execution':True,'raw_execution_ready':False})
    finally:runner.close()


def execute(prepared_file,accepted_sha256):
    # Acceptance is an explicit operator action, not a security signature.
    if not re.fullmatch('[0-9a-f]{64}',accepted_sha256 or '') or metadata_sha(prepared_file)!=accepted_sha256:raise ValueError('Explicit acceptance of exact prepared file SHA256 required before execution')
    job=read(prepared_file);root=validate_job(job);check_host(root,job['limits'])
    root.mkdir(parents=True,exist_ok=False)
    with (root/'workflow-job.json').open('xb') as f:
        f.write(Path(prepared_file).read_bytes());f.flush();os.fsync(f.fileno())
    atomic_json(root/'operator-acceptance.json',{'prepared_file_sha256':accepted_sha256,'accepted_epoch':time.time(),'scope':job['scope']})
    start=time.monotonic();checkpoint,memory=monitor(root,job['manifest'],job['limits'],start);caps=job['limits']['process_caps']
    rec=supervise('run',[sys.executable,str(Path(__file__).resolve()),'--worker',str(root/'workflow-job.json')],root/'workflow-receipts',timeout=job['limits']['wall_seconds'],rss_limit=caps['rss_bytes'],address_space=caps['address_space_bytes'],checkpoint=checkpoint,group_checkpoint=memory)
    check_outer(rec);inner=read(root/'workflow-inner.json');ledger=read(root/'ledger.json')
    steps=[s['name'] for s in job['manifest']['sealed_workflow']['steps']]
    done=inner.get('completed_steps',[])
    if inner.get('status') not in ('complete','coverage_insufficient') or not done or done!=steps[:len(done)] or inner.get('ledger_sha256')!=metadata_sha(root/'ledger.json') or set(ledger['phases'])!=set(done) or any(p['status']!='verified' for p in ledger['phases'].values()):raise ValueError('Incomplete real workflow result')
    if inner['status']=='complete' and done!=steps:raise ValueError('Incomplete real step inventory')
    if inner['status']=='coverage_insufficient' and ledger['phases'][done[-1]].get('coverage',{}).get('adequate') is not False:raise ValueError('Missing insufficient coverage evidence')
    seal={'status':'sealed','technical_status':inner['status'],'sha256':{n:metadata_sha(root/n) for n in FILES},'technical_real_execution':True,'raw_execution_ready':False}
    atomic_json(root/'workflow-seal.json',seal);return seal


def verify(root):
    root=Path(root).resolve();job=read(root/'workflow-job.json');validate_job(job);assert_seal(root,job['manifest'],job['limits'])
    state=read(root/'ledger.json');remaining=state['deadline_epoch']-time.time()
    if remaining<=0:raise RuntimeError('Original deadline expired; no automatic extension')
    checkpoint,memory=monitor(root,job['manifest'],job['limits'],time.monotonic());caps=job['limits']['process_caps']
    rec=supervise('reuse',[sys.executable,str(Path(__file__).resolve()),'--worker',str(root/'workflow-job.json'),'--verify-worker'],root/'real-verification-receipts',timeout=min(remaining,caps['wall_seconds']),rss_limit=caps['rss_bytes'],address_space=caps['address_space_bytes'],checkpoint=checkpoint,group_checkpoint=memory)
    check_outer(rec);return read(root/'real-verification.json')


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--prepare',type=Path);g.add_argument('--execute',type=Path);g.add_argument('--verify',type=Path);g.add_argument('--host',action='store_true');g.add_argument('--worker',type=Path,help=argparse.SUPPRESS)
    p.add_argument('--root',type=Path);p.add_argument('--aligner',type=Path);p.add_argument('--accept-plan-sha256');p.add_argument('--verify-worker',action='store_true',help=argparse.SUPPRESS);a=p.parse_args()
    if a.host:result=host_report(Path.home())
    elif a.prepare:
        if not a.root or not a.aligner:p.error('--prepare requires --root and --aligner')
        result=prepare(a.root,a.aligner)
        with a.prepare.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
        result={'prepared_file':str(a.prepare),'sha256':metadata_sha(a.prepare),'execution_enabled':False,'raw_execution_ready':False,'unverified':result['unverified']}
    elif a.execute:result=execute(a.execute,a.accept_plan_sha256)
    elif a.verify:result=verify(a.verify)
    else:
        # A worker cannot be used as an unsupervised execution bypass: require
        # a started outer receipt and the exact same procfs process group.
        job=read(a.worker);root=validate_job(job);folder='real-verification-receipts' if a.verify_worker else 'workflow-receipts';name='reuse' if a.verify_worker else 'run'
        receipt_path=root/folder/(name+'.json')
        outer=read(receipt_path)
        until=time.monotonic()+2
        while outer.get('status')=='started' and 'procfs_group' not in outer and time.monotonic()<until:
            time.sleep(.01);outer=read(receipt_path)
        from process_supervisor_v2 import proc_info
        group=proc_info(int(os.readlink('/proc/self')))['group']
        if outer.get('status')!='started' or outer.get('procfs_group')!=group:raise ValueError('Worker requires active parent supervisor')
        # The descriptor and explicit acceptance must also be coherent. This
        # is an accidental-misuse guard, not a sandbox against its owner.
        acceptance=read(root/'operator-acceptance.json')
        if acceptance.get('prepared_file_sha256')!=metadata_sha(a.worker):raise ValueError('Missing exact-plan operator acceptance')
        worker(job,a.verify_worker);return
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
