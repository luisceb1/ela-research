"""Bounded two-library measurement; preparation never transfers raw data."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import stat
import subprocess
import sys
import time
import urllib.error
import urllib.request

import prepare_gse252892_local as prep
import gse252892_range_transport as ranged
import gse252892_retained_blocks as retained
import gse252892_after_sampler as after_sampler
import gse252892_after_interop as after_interop
import gse252892_drvfs as drvfs

ROOT = Path(__file__).resolve().parents[1]
CAPS = {'transfer_bytes': 14_000_000_000, 'wall_seconds': 172800, 'root_bytes': 100*1024**3,
        'windows_reserve_bytes': 50*1024**3, 'group_rss_bytes': 6*1024**3,
        'process_as_bytes': 8*1024**3, 'cpus': 2}
BASE_SHA = '97a578839d72088bab1403b0c9ef6bd9b8e3ff064bbe3008314fb34545b6af26'
CODE = ['scripts/run_gse252892_local.py', 'scripts/prepare_gse252892_local.py',
        'scripts/gse252892_range_transport.py', 'scripts/gse252892_retained_blocks.py', 'scripts/gse252892_after_sampler.py', 'scripts/gse252892_after_interop.py', 'scripts/gse252892_drvfs.py',
        'research/references/unc13a_targets_sealed.json',
        'reports/local-raw-feasibility-20261112/fastq-manifest.tsv']
PRIOR_PLAN_SHA='911c5be6f8a470d085ab57279ee8d3ce40bb31edcb990a3064238d9c4b9d9a9f'
PRIOR_BYTES=351927726
PREFIX_SHA='ee7762da8dc57e0ab9878fbf449cb7f933fd7f95c6a32c4e93be5dc2c3c5d2aa'


def save(path, value):
    path = Path(path)
    tmp = path.with_name(path.name+'.tmp')
    with tmp.open('w') as f:
        json.dump(value, f, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def read_small(path):
    path = Path(path)
    if path.stat().st_size > 2_000_000:
        raise ValueError('Oversized descriptor')
    return json.loads(path.read_text())


def windows_powershell():
    candidates=[shutil.which('powershell.exe'),
        '/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe']
    for candidate in candidates:
        if candidate and Path(candidate).is_file():return str(candidate)
    raise ValueError('Cannot locate Windows PowerShell in PATH or its standard /mnt/c/Windows/System32/WindowsPowerShell/v1.0 path; real C: free space is still required')


def windows_free():
    exe = windows_powershell()
    try:
        text = subprocess.check_output([exe, '-NoProfile', '-NonInteractive', '-Command',
            '(Get-PSDrive -Name C).Free'], text=True, timeout=15).strip().lstrip('\ufeff')
    except (OSError,subprocess.CalledProcessError,subprocess.TimeoutExpired) as exc:
        raise ValueError('Cannot query real C: free space through '+exe+'; verify Windows executable interop in this WSL distribution') from exc
    if not text.isdigit():
        raise ValueError('Cannot parse physical Windows C: free bytes')
    return int(text)


def physical_free():
    value=drvfs.free_bytes()
    return windows_free() if value is None else value


def check_free(value):
    if value < CAPS['windows_reserve_bytes']:
        raise ValueError('Physical C: reserve below 50 GiB')


def code_hashes():
    return {p: prep.sha256(ROOT/p) for p in CODE}


def version(path, token):
    result = subprocess.run([str(path), '--version'], text=True, capture_output=True,
                            timeout=10, check=True)
    out = result.stdout+result.stderr
    if token not in out:
        raise ValueError('Unexpected tool version: '+str(path))
    return out


def check_options(path, options):
    result=subprocess.run([str(path),'--help'],text=True,capture_output=True,timeout=10)
    text=result.stdout+result.stderr
    missing=[opt for opt in options if opt not in text]
    if missing:raise ValueError('Required CLI options absent from help: '+','.join(missing))


def prior_record(plan_path, current_prefix=True):
    plan_path=Path(plan_path).resolve()
    if prep.sha256(plan_path)!=PRIOR_PLAN_SHA:raise ValueError('Prior consumed proposal SHA mismatch')
    old=read_small(plan_path);root=Path(old['run_root'])
    paths={name:root/name for name in ['accepted.json','supervision.json','worker-failure.json','transfer-ledger.json']}
    paths['proposal_claim.json']=Path(str(plan_path)+'.claimed.json')
    receipt={name:read_small(path) for name,path in paths.items()}
    sup=receipt['supervision.json'];ledger=receipt['transfer-ledger.json']
    if old.get('schema')!='gse252892-bounded-v1' or old.get('base_sha256')!=BASE_SHA:
        raise ValueError('Unexpected prior execution identity')
    if receipt['accepted.json']['plan_sha256']!=PRIOR_PLAN_SHA or sup['plan_sha256']!=PRIOR_PLAN_SHA or sup['status']!='failed' or sup['cleanup_error'] is not None:
        raise ValueError('Prior attempt must be failed and cleaned up')
    if receipt['proposal_claim.json']!={'plan_sha256':PRIOR_PLAN_SHA,'transfer_bytes':CAPS['transfer_bytes']}:
        raise ValueError('Prior proposal must remain consumed with its accepted budget')
    if receipt['worker-failure.json']['error']!='Raw length/MD5 mismatch':raise ValueError('Unexpected prior failure')
    requests=ledger['requests']
    first=prep.selected_inputs(ROOT/'reports/local-raw-feasibility-20261112/fastq-manifest.tsv')[0]
    if len(requests)!=1 or requests[0]['url']!=first['url'] or requests[0]['expected_bytes']!=int(first['compressed_bytes']):
        raise ValueError('Prior source URL/length mismatch')
    req=requests[0]
    if ledger['actual_body_bytes']!=PRIOR_BYTES or ledger['body_upper_bound_bytes']!=PRIOR_BYTES or req['actual_bytes']!=PRIOR_BYTES or req['status']!='failed' or req['inflight_max_bytes']!=0 or req['observed_body_prefix_sha256']!=PREFIX_SHA:
        raise ValueError('Prior transfer charge/prefix record changed')
    prefix=root/'GSM8009878'/(Path(first['url']).name+'.partial')
    if current_prefix:
        if prefix.is_symlink() or prefix.stat().st_size!=PRIOR_BYTES or prep.sha256(prefix)!=PREFIX_SHA:
            raise ValueError('Prior partial bytes/hash changed')
        with prefix.open('rb') as f:
            if f.read(2)!=b'\x1f\x8b':raise ValueError('Prior partial is not a gzip prefix')
    return {'prior_plan_path':str(plan_path),'prior_plan_sha256':PRIOR_PLAN_SHA,'prior_root':str(root),
        'prior_charge_bytes':PRIOR_BYTES,'receipt_sha256':{n:prep.sha256(p) for n,p in paths.items()},
        'prefix':{'path':str(prefix),'bytes':PRIOR_BYTES,'sha256':PREFIX_SHA,'url':first['url']}}


def recovery_record(plan_path,current_files=True):
    return retained.record(plan_path,read_small,prior_record,ranged.SETTINGS,BASE_SHA,CAPS['transfer_bytes'],current_files)


def after_sampler_record(plan_path,current_files=True):
    return after_sampler.record(plan_path,read_small,recovery_record,ranged.RECOVERY_SETTINGS,BASE_SHA,CAPS['transfer_bytes'],current_files)


def after_interop_record(plan_path,current_files=True):
    return after_interop.record(plan_path,read_small,after_sampler_record,ranged.RECOVERY_SETTINGS,BASE_SHA,CAPS['transfer_bytes'],current_files)


def commands(plan, gsm):
    d = Path(plan['run_root'])/gsm
    run = {'GSM8009878':'SRR27477544', 'GSM8009881':'SRR27477541'}[gsm]
    raw = [str(d/f'{run}_{i}.fastq.gz') for i in (1,2)]
    clean = [str(d/f'trimmed_{i}.fq') for i in (1,2)]
    fastp = [plan['fastp']['path'], '-i',raw[0],'-I',raw[1],'-o',clean[0],'-O',clean[1],
             '--detect_adapter_for_pe','--dont_eval_duplication','--thread','2',
             '--json',str(d/'fastp.json'),'--html',str(d/'fastp.html')]
    align = [plan['base']['tools']['aligner']['path'], '-x',str(Path(plan['base']['index_directory'])/'genome'),
             '-1',clean[0],'-2',clean[1],'-S','/dev/stdout','--no-mixed','--no-discordant',
             '--fr','-p','2','--seed','0','-k','2','--reorder','--no-unal','--no-temp-splicesite',
             '--summary-file',str(d/'hisat2-summary.txt')]
    return {'fastp':fastp,'align':align,'plain_files':clean}


def validate_plan(plan, current_files=True):
    if plan.get('schema') != 'gse252892-drvfs-v5' or plan.get('caps') != CAPS or plan.get('transport')!=ranged.RECOVERY_SETTINGS:
        raise ValueError('Execution schema/caps changed')
    if plan.get('base_sha256') != BASE_SHA or plan['base'].get('execution_enabled') is not False:
        raise ValueError('Expected exact disabled base')
    rows = prep.selected_inputs(ROOT/'reports/local-raw-feasibility-20261112/fastq-manifest.tsv')
    if plan['base'].get('input_files') != rows or plan['base'].get('advertised_raw_input_bytes') != prep.EXPECTED_INPUT_BYTES:
        raise ValueError('Fixed input identity changed')
    if plan.get('code_sha256') != code_hashes() or plan.get('repository_commit') != prep.git('rev-parse','HEAD'):
        raise ValueError('Runner/code commit changed')
    if prep.git('status','--porcelain','--untracked-files=all'):
        raise ValueError('Checkout must remain clean')
    lineage=after_interop_record(plan['lineage']['prior_plan_path'],current_files=current_files)
    if lineage!=plan['lineage']:raise ValueError('Prior evidence/charge changed')
    root = Path(plan['run_root'])
    if not root.is_absolute() or root == ROOT or ROOT in root.parents or root.is_symlink():
        raise ValueError('Run root must be a separate absolute path')
    if {g:commands(plan,g) for g in prep.SELECTED} != plan['commands']:
        raise ValueError('Commands changed')
    if prep.sha256(plan['base_path']) != BASE_SHA:
        raise ValueError('Base descriptor bytes changed')
    if read_small(plan['base_path']) != plan['base']:
        raise ValueError('Base descriptor fields changed')
    if current_files:
        import pysam
        if pysam.__version__!='0.23.3' or sys.executable != plan['python_executable']:
            raise ValueError('Expected Python environment/PySAM')
        for info in [plan['fastp'],*plan['base']['tools'].values()]:
            if prep.sha256(info['path']) != info['sha256']:
                raise ValueError('Tool binary changed')
        expected = read_small(ROOT/'reports/hisat2-index-inspection-20261031/verified_index.json')
        verified = prep.verify_index(plan['base']['index_directory'],expected)
        if verified != plan['base']['index_files']:
            raise ValueError('Base index record changed')
        if prep.sha256(ROOT/'research/references/unc13a_targets_sealed.json') != plan['base']['targets_sha256']:
            raise ValueError('Targets changed')
    return rows


def prepare(base, fastp, root, output, prior_plan):
    base = Path(base).resolve(); root = Path(root).expanduser().resolve()
    output = Path(output).expanduser().resolve()
    if output.exists() or root.exists() or output == root:
        raise ValueError('New output and new run root required')
    if ROOT in output.parents or output == ROOT:
        raise ValueError('Descriptor must be outside checkout')
    if prep.sha256(base)!=BASE_SHA:
        raise ValueError('Base SHA does not match the user-reported descriptor')
    data = read_small(base)
    fastp = Path(fastp).resolve(strict=True)
    lineage=after_interop_record(prior_plan)
    if any(root==Path(p) or Path(p) in root.parents or root in Path(p).parents for p in lineage['prior_roots']):
        raise ValueError('New root must preserve the prior root')
    plan = {'schema':'gse252892-drvfs-v5','prepared_for_review':True,
            'base_path':str(base),'base_sha256':BASE_SHA,'base':data,
            'repository_commit':prep.git('rev-parse','HEAD'),'python_executable':sys.executable,
            'fastp':{'path':str(fastp),'sha256':prep.sha256(fastp),'version_output':version(fastp,'fastp 0.23.4')},
            'run_root':str(root),'caps':CAPS.copy(),'transport':ranged.RECOVERY_SETTINGS.copy(),'lineage':lineage,'code_sha256':code_hashes(),
            'endpoint':'fragment/event/library with primary anchor 15; no inference',
            'protocol':'research/plans/2026-11-13-gse252892-drvfs-continuation.md'}
    plan['commands'] = {g:commands(plan,g) for g in prep.SELECTED}
    check_options(fastp,['--detect_adapter_for_pe','--dont_eval_duplication','--thread'])
    check_options(data['tools']['aligner']['path'],['--no-temp-splicesite','--reorder','--no-mixed','--no-discordant','--summary-file'])
    validate_plan(plan)
    free = physical_free(); check_free(free); plan['windows_free_bytes_at_preparation']=free
    encoded=(json.dumps(plan,indent=2)+'\n').encode()
    with output.open('xb') as f:f.write(encoded)
    return {'status':'execution_proposal_not_started','output':str(output),
            'descriptor_sha256':hashlib.sha256(encoded).hexdigest(),'advertised_input_bytes':prep.EXPECTED_INPUT_BYTES,
            'maximum_transfer_bytes':CAPS['transfer_bytes'],'wall_seconds':CAPS['wall_seconds'],
            'prior_charge_bytes':lineage['prior_charge_bytes'],'prior_observed_body_bytes':lineage['prior_observed_body_bytes'],
            'prior_reserved_bytes_charged':lineage['prior_charge_bytes']-lineage['prior_observed_body_bytes'],'complete_inputs_proposed_for_reuse':len(lineage['complete_inputs']),
            'complete_input_bytes':sum(p['bytes'] for p in lineage['complete_inputs']),
            'retained_complete_blocks':len(lineage['retained_blocks']),
            'retained_complete_block_bytes':sum(p['bytes'] for p in lineage['retained_blocks']),
            'minimum_new_body_bytes_if_reuse_valid':prep.EXPECTED_INPUT_BYTES-sum(p['bytes'] for p in lineage['complete_inputs'])-sum(p['bytes'] for p in lineage['retained_blocks'])+(ranged.RECOVERY_SETTINGS['overlap_bytes'] if lineage['retained_blocks'] else 0),
            'raw_bytes_downloaded':0,'caps':CAPS,'transport':ranged.RECOVERY_SETTINGS}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise ValueError('Redirect refused; no alternate raw URL')


def download(item, directory, ledger, ledger_path, opener=None):
    expected=int(item['compressed_bytes'])
    if expected > CAPS['transfer_bytes']-ledger['actual_body_bytes']:
        raise ValueError('Remaining transfer budget too small')
    path = Path(directory)/Path(item['url']).name
    partial = path.with_name(path.name+'.partial')
    if path.exists() or partial.exists():raise ValueError('No overwrite/resume')
    rec={'url':item['url'],'expected_bytes':expected,'actual_bytes':0,'status':'started'}
    ledger['requests'].append(rec);save(ledger_path,ledger)
    digest=hashlib.md5(); strong=hashlib.sha256()
    def persist():
        ledger['body_upper_bound_bytes']=ledger['actual_body_bytes']+sum(x.get('inflight_max_bytes',0) for x in ledger['requests'])
        save(ledger_path,ledger)
    def charged_read(stream,n):
        # Preserve an upper bound if the worker dies during a blocking read.
        rec['inflight_max_bytes']=n;persist()
        b=stream.read(n)
        rec['actual_bytes']+=len(b);ledger['actual_body_bytes']+=len(b)
        digest.update(b);strong.update(b)
        rec['inflight_max_bytes']=0;persist()
        return b
    try:
        req=urllib.request.Request(item['url'],headers={'Accept-Encoding':'identity','User-Agent':'ela-research/bounded-local'})
        op=opener or urllib.request.build_opener(NoRedirect())
        try:
            resp=op.open(req,timeout=30)
        except urllib.error.HTTPError as exc:
            # Error bodies consume budget too. No retry follows.
            with exc:
                while True:
                    n=min(65536,CAPS['transfer_bytes']-ledger['actual_body_bytes'])
                    if n<=0:break
                    b=charged_read(exc,n)
                    if not b:break
            raise
        with resp, partial.open('xb') as out:
            rec['http_status']=resp.status
            if resp.status!=200 or resp.geturl()!=item['url'] or resp.headers.get('Content-Encoding','identity')!='identity':
                raise ValueError('Unexpected raw response status/URL/encoding')
            declared=resp.headers.get('Content-Length')
            if declared is None or int(declared)!=expected:raise ValueError('Content-Length mismatch')
            while True:
                left=min(expected-rec['actual_bytes']+1,CAPS['transfer_bytes']-ledger['actual_body_bytes'])
                if left<=0:raise ValueError('Actual response-body cap reached')
                b=charged_read(resp,min(1024*1024,left))
                if not b:break
                out.write(b)
                if rec['actual_bytes']>expected:raise ValueError('Raw response larger than advertised')
        if rec['actual_bytes']!=expected or digest.hexdigest()!=item['md5']:
            raise ValueError('Raw length/MD5 mismatch')
        with partial.open('rb') as f:
            if f.read(2)!=b'\x1f\x8b':raise ValueError('Not gzip')
        os.replace(partial,path)
        rec.update(status='verified',md5=digest.hexdigest(),sha256=strong.hexdigest())
        return path
    except BaseException as exc:
        rec.update(status='failed',error=str(exc));raise
    finally:
        rec['observed_body_prefix_sha256']=strong.hexdigest()
        persist()


def events(read, targets):
    if read.reference_name!='chr19' or not read.has_tag('XS') or read.get_tag('XS')!='-':return set()
    cigar=read.cigartuples or [];cursor=read.reference_start;hits=set()
    for i,(op,n) in enumerate(cigar):
        if op==3:
            anchors=[]
            for side in (reversed(cigar[:i]),iter(cigar[i+1:])):
                anchor=0
                for o,k in side:
                    if o not in (0,7,8):break
                    anchor+=k
                anchors.append(anchor)
            if min(anchors)>=15:
                for label,interval in targets.items():
                    if (cursor,cursor+n)==tuple(interval):hits.add(label)
        if op in (0,2,3,7,8):cursor+=n
    return hits


def pair_hits(group,targets):
    if len(group)!=2:return None
    if {bool(r.is_read1) for r in group}!={True,False} or any(r.is_read1==r.is_read2 for r in group):return None
    for r in group:
        if (not r.is_paired or not r.is_proper_pair or r.is_unmapped or r.mate_is_unmapped or r.is_secondary or r.is_supplementary or r.is_qcfail or not 20<=r.mapping_quality<255 or not r.has_tag('NH') or r.get_tag('NH')!=1):return None
    a,b=group
    if a.next_reference_id!=b.reference_id or b.next_reference_id!=a.reference_id or a.next_reference_start!=b.reference_start or b.next_reference_start!=a.reference_start:return None
    return events(a,targets)|events(b,targets)


def count_records(records,targets):
    counts={k:0 for k in targets};qc=Counter();group=[];name=None
    def consume():
        qc['alignment_groups']+=1
        hits=pair_hits(group,targets)
        if hits is None:qc['rejected_groups']+=1;return
        qc['eligible_groups']+=1
        qc['marked_duplicate_records']+=sum(r.is_duplicate for r in group)
        for key in hits:counts[key]+=1
    for r in records:
        qc['sam_records']+=1
        if group and r.query_name!=name:consume();group=[]
        name=r.query_name;group.append(r)
        if len(group)>8:raise ValueError('Unexpected query group >8 records; stop')
    if group:consume()
    return {'counts':counts,'qc':dict(qc),'unit':'contiguous paired query group/event/library; anchor 15',
            'positive_control_measured':counts['canonical']>0,
            'support_at_least_20_groups':{k:counts[k]>=20 for k in ('cryptic_left','cryptic_right')},
            'interpretation':'Below-diagnostic support is insufficient, not a biological zero. No effect or ratio.'}


def stage(plan,gsm,ledger,root):
    import pysam
    d=root/gsm;d.mkdir()
    save(root/'progress.json',{'phase':'download','library':gsm})
    for row in plan['base']['input_files']:
        if row['gsm']==gsm:
            source=next((p for p in plan['lineage']['complete_inputs'] if p['url']==row['url']),None)
            if source:after_sampler.copy_complete(row,source,d,save)
            else:ranged.download(row,d,ledger,settings=plan['transport'],retained=[p for p in plan['lineage']['retained_blocks'] if p['url']==row['url']])
    cmd=plan['commands'][gsm]
    save(root/'progress.json',{'phase':'fastp','library':gsm})
    with (d/'fastp.log').open('wb') as log:
        subprocess.run(cmd['fastp'],stdout=log,stderr=subprocess.STDOUT,check=True)
    if any(not Path(p).is_file() or Path(p).stat().st_size==0 for p in cmd['plain_files']):
        raise ValueError('No retained paired FASTQ after preprocessing')
    save(root/'progress.json',{'phase':'alignment_and_count','library':gsm})
    targets=read_small(ROOT/'research/references/unc13a_targets_sealed.json')['junctions']
    with (d/'hisat2.log').open('wb') as log:
        proc=subprocess.Popen(cmd['align'],stdout=subprocess.PIPE,stderr=log)
        try:
            with pysam.AlignmentFile(proc.stdout,'r') as sam:
                if sam.get_reference_length('chr19')!=58617616:raise ValueError('chr19 header length mismatch')
                result=count_records(sam,targets)
            if proc.wait()!=0:raise ValueError('HISAT2 failed; no completed count verdict')
        finally:
            if proc.poll() is None:proc.terminate()
    result.update(gsm=gsm,project='SRP482832',complete=True)
    save(d/'junction-counts.json',result)
    for p in cmd['plain_files']:Path(p).unlink()
    return result


def worker(plan_path):
    plan=read_small(plan_path);root=Path(plan['run_root'])
    accepted=read_small(root/'accepted.json')
    if os.getpgrp()!=os.getpid() or accepted['supervisor_pid']!=os.getppid() or accepted['plan_sha256']!=prep.sha256(plan_path) or accepted['transfer_bytes']!=CAPS['transfer_bytes']:
        raise ValueError('Worker requires an active accepting supervisor/process group')
    ledger=ranged.Budget(root/'transfer-ledger.json',CAPS['transfer_bytes'],plan.get('lineage',{}).get('prior_charge_bytes',0),prior_observed=plan.get('lineage',{}).get('prior_observed_body_bytes'))
    try:
        validate_plan(plan)
        # Inspector is supervised, and this does not transfer genomic inputs.
        with (root/'index-summary.txt').open('wb') as f:
            subprocess.run([plan['base']['tools']['inspector']['path'],'-s',str(Path(plan['base']['index_directory'])/'genome')],stdout=f,stderr=subprocess.STDOUT,check=True)
        text=(root/'index-summary.txt').read_text()
        if not any('chr19' in l.split() and l.split()[-1]=='58617616' for l in text.splitlines()):raise ValueError('Index chr19 summary mismatch')
        result={'project':'SRP482832','libraries':[],'analysis':'technical descriptive counts only'}
        for gsm in prep.SELECTED:
            one=stage(plan,gsm,ledger,root);result['libraries'].append(one)
            if gsm==prep.SELECTED[0] and not one['positive_control_measured']:
                result.update(status='control_failed_KD_not_downloaded');save(root/'result.json',result);return
        result['status']='completed';save(root/'result.json',result)
    except BaseException as exc:
        save(root/'worker-failure.json',{'status':'failed_partial_not_interpretable','error':str(exc)})
        raise


def root_bytes(root):
    root=Path(root)
    mode=root.lstat().st_mode
    if stat.S_ISLNK(mode):raise ValueError('Symlink in run root')
    if not stat.S_ISDIR(mode):raise ValueError('Expected run-root directory')
    def walk_error(error):raise error
    total=0
    for directory,dirs,files in os.walk(root,followlinks=False,onerror=walk_error):
        for name in dirs+files:
            p=Path(directory)/name
            try:info=p.lstat()
            except FileNotFoundError:
                # Atomic receipt/block promotion may remove a name after listing.
                # This remains a sampled disk guard, not a transactional quota.
                continue
            if stat.S_ISLNK(info.st_mode):raise ValueError('Symlink in run root')
            if stat.S_ISREG(info.st_mode):total+=info.st_size
    return total


def group_rss(pgid):
    total=0
    for p in Path('/proc').glob('[0-9]*/stat'):
        try:
            fields=p.read_text().rsplit(')',1)[1].split()
            if int(fields[2])==pgid:total+=int(fields[21])*os.sysconf('SC_PAGE_SIZE')
        except (FileNotFoundError,ProcessLookupError,PermissionError):pass
    return total


def child_limits():
    resource.setrlimit(resource.RLIMIT_AS,(CAPS['process_as_bytes'],CAPS['process_as_bytes']))
    os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:CAPS['cpus']])


def stop_group(proc):
    for sig,wait in [(signal.SIGTERM,2),(signal.SIGKILL,1)]:
        try:os.killpg(proc.pid,sig)
        except ProcessLookupError:break
        try:proc.wait(timeout=wait)
        except subprocess.TimeoutExpired:continue
    if proc.poll() is None:raise RuntimeError('Worker did not terminate; inspect process group manually')


def execute(path,accepted_sha,accepted_transfer):
    path=Path(path).resolve()
    if prep.sha256(path)!=accepted_sha or accepted_transfer!=CAPS['transfer_bytes']:
        raise ValueError('Explicit exact descriptor SHA and transfer cap acceptance required')
    plan=read_small(path);validate_plan(plan,current_files=False);check_free(physical_free())
    root=Path(plan['run_root'])
    if root.exists():raise ValueError('New run root required; no resume/overwrite')
    claim=Path(str(path)+'.claimed.json')
    with claim.open('x') as f:json.dump({'plan_sha256':accepted_sha,'transfer_bytes':accepted_transfer},f)
    root.mkdir()
    save(root/'accepted.json',{'plan_sha256':accepted_sha,'transfer_bytes':accepted_transfer,'supervisor_pid':os.getpid()})
    started=time.monotonic();peak_rss=0;peak_disk=0;proc=None;status='failed';reason=None
    try:
        with (root/'worker.log').open('wb') as log:
            proc=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'_worker','--plan',str(path)],
                stdout=log,stderr=subprocess.STDOUT,start_new_session=True,preexec_fn=child_limits)
            last_windows=0
            while proc.poll() is None:
                elapsed=time.monotonic()-started
                if elapsed>CAPS['wall_seconds']:raise ValueError('Wall time cap exceeded')
                rss=group_rss(proc.pid);size=root_bytes(root)
                if plan.get('lineage'):
                    size+=sum(root_bytes(p) for p in plan['lineage']['prior_roots'])
                peak_rss=max(peak_rss,rss);peak_disk=max(peak_disk,size)
                if rss>CAPS['group_rss_bytes']:raise ValueError('Sampled group RSS cap exceeded')
                if size>CAPS['root_bytes']:raise ValueError('Sampled root disk cap exceeded')
                if elapsed-last_windows>=30:
                    check_free(physical_free());last_windows=elapsed
                    progress=read_small(root/'progress.json') if (root/'progress.json').exists() else {'phase':'verify_inputs_and_index'}
                    transfer=read_small(root/'transfer-ledger.json') if (root/'transfer-ledger.json').exists() else {}
                    print(json.dumps({'elapsed_seconds':round(elapsed),'progress':progress,'raw_body_bytes_this_attempt':transfer.get('new_observed_body_bytes',0),'lineage_body_upper_bound_bytes':transfer.get('body_upper_bound_bytes',0),'sampled_group_rss_bytes':rss,'sampled_combined_root_bytes':size}),flush=True)
                time.sleep(0.5)
            if proc.returncode:raise ValueError('Worker failed; inspect worker.log/failure receipt')
            if not (root/'result.json').is_file():raise ValueError('No final result')
            status=read_small(root/'result.json')['status']
    except BaseException as exc:
        reason=str(exc) or type(exc).__name__
        raise
    finally:
        cleanup_error=None
        try:
            if proc is not None:stop_group(proc)
        except BaseException as exc:
            cleanup_error=str(exc)
        save(root/'supervision.json',{'status':status,'failure':reason,'elapsed_seconds':time.monotonic()-started,
            'peak_sampled_group_rss_bytes':peak_rss,'peak_sampled_combined_root_bytes':peak_disk,'caps':CAPS,
            'limitations':'RSS/disk are sampled, not kernel aggregate quotas; uninterruptible I/O/escape not guaranteed controllable',
            'raw_transfer_ledger':'transfer-ledger.json','plan_sha256':accepted_sha,'cleanup_error':cleanup_error})
        if cleanup_error:raise RuntimeError(cleanup_error)
    return {'status':status,'run_root':str(root)}


def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='action',required=True)
    p=sub.add_parser('prepare');p.add_argument('--base-descriptor',type=Path,required=True);p.add_argument('--fastp',type=Path,required=True);p.add_argument('--run-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--prior-plan',type=Path,required=True)
    p=sub.add_parser('execute');p.add_argument('--plan',type=Path,required=True);p.add_argument('--accept-plan-sha256',required=True);p.add_argument('--accept-transfer-bytes',type=int,required=True)
    p=sub.add_parser('_worker');p.add_argument('--plan',type=Path,required=True)
    a=ap.parse_args()
    if a.action=='prepare':out=prepare(a.base_descriptor,a.fastp,a.run_root,a.output,a.prior_plan)
    elif a.action=='execute':out=execute(a.plan,a.accept_plan_sha256,a.accept_transfer_bytes)
    else:worker(a.plan);out={'status':'worker_finished'}
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
