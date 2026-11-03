"""Read-only partial policy review. Never imports or executes the real worker.

This review cannot authorize execution or verify host files, binaries, code, seals,
decoders or the complete manifest. It never follows paths/URLs inside a descriptor.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path,PurePosixPath

PROFILE=Path(__file__).resolve().parents[1]/'research/references/cached_pilot_review_20261103.json'
PROFILE_SHA256='ac40773e9a8a63d55eee8dfad736364c192878d45c998e4c830e9a9fc3c7c1e3'

def fail(message):raise ValueError(message)

def pairs_unique(pairs):
    out={}
    for k,v in pairs:
        if k in out:fail('Duplicate JSON key')
        out[k]=v
    return out

def load(path):
    with Path(path).open('rb') as f:data=f.read(2*1024**2+1)
    if len(data)>2*1024**2:fail('JSON size cap')
    def invalid(_):fail('Non-finite JSON number')
    def finite_float(value):
        n=float(value)
        if not math.isfinite(n):fail('Non-finite JSON float')
        return n
    return json.loads(data,object_pairs_hook=pairs_unique,parse_constant=invalid,parse_float=finite_float),hashlib.sha256(data).hexdigest()

def strict_equal(actual,expected):
    if type(actual) is not type(expected):return False
    if isinstance(expected,dict):return set(actual)==set(expected) and all(strict_equal(actual[k],v) for k,v in expected.items())
    if isinstance(expected,list):return len(actual)==len(expected) and all(strict_equal(a,b) for a,b in zip(actual,expected))
    return actual==expected

def require_equal(actual,expected,message):
    if not strict_equal(actual,expected):fail(message)

def path(value):
    if not isinstance(value,str) or not value.startswith('/') or any(ord(c)<32 for c in value) or any(p in ('.','..','') for p in value.split('/')[1:]):fail('Non-canonical absolute POSIX path')
    return PurePosixPath(value)

def proposal_review(proposal,profile):
    require_equal(proposal,profile['proposal'],'Proposal changed from reviewed snapshot')
    p=proposal
    if sum(step['expected']['bytes'] for step in profile['steps'] if step['kind']=='http')!=p['planned_read_body_bytes']:fail('Read body total differs from four frozen mates')
    if p['prior_charged_body_bytes']+p['planned_read_body_bytes']!=p['minimum_final_body_bytes']:fail('Cumulative charge arithmetic')
    if p['original_body_cap']-p['minimum_final_body_bytes']!=p['remaining_margin_bytes'] or p['remaining_margin_bytes']<0:fail('Body cap arithmetic')
    return {'status':'archived_proposal_arithmetic_passed','prior_body_bytes':p['prior_charged_body_bytes'],
            'planned_read_body_bytes':p['planned_read_body_bytes'],'cumulative_if_both_downloaded':p['minimum_final_body_bytes'],
            'margin_bytes':p['remaining_margin_bytes'],'disabled_descriptor_provided':False,**disabled()}

def disabled():
    return {'execution_enabled':False,'raw_execution_ready':False,'host_files_verified':False,'window_authorized':False}

def review(job,profile):
    if not isinstance(job,dict) or set(job)!={'schema','execution_enabled','root','manifest','limits','host_observed','unverified','scope'}:fail('Prepared job schema')
    if job['schema']!='b5-prepared-real-pilot-v1' or job['execution_enabled'] is not False:fail('Disabled job required')
    require_equal(job['limits'],profile['limits'],'Fixed limits changed')
    m=job['manifest']
    if not isinstance(m,dict) or set(m)!={'transport','execution_policy','aligner','archives','paired_fastq','real_compute','sealed_workflow','cached_index','cached_guard_sample_seconds'}:fail('Manifest schema')
    require_equal(m['execution_policy'],profile['execution_policy'],'Phase/order/resource policy changed')
    require_equal(m['transport'],{'read_chunk_bytes':65536,'reservation_block_bytes':4194304,'attempts':1},'Transport policy changed')
    require_equal(m['archives'],{},'Index transfer/extraction forbidden in this route')
    require_equal(m['paired_fastq'],profile['paired_fastq'],'Fixed paired inputs/prefix changed')
    if type(m['cached_guard_sample_seconds']) is not float or m['cached_guard_sample_seconds']!=.1:fail('Sampling policy changed')
    sealed=m['sealed_workflow']
    if not isinstance(sealed,dict) or set(sealed)!={'schema','mode','origins','steps','producer'}:fail('Workflow schema')
    require_equal({k:sealed[k] for k in ('schema','mode','origins','steps')},{'schema':'cached-index-pilot-v1','mode':'real-pilot','origins':['https://ftp.sra.ebi.ac.uk'],'steps':profile['steps']},'Fixed origins, libraries or stage order changed')
    b=m['cached_index'];p=profile['proposal']
    if not isinstance(b,dict):fail('Cache binding required')
    for key,expected in [('schema','sealed-extracted-index-v1'),('cumulative_body_bytes',p['prior_charged_body_bytes']),('remaining_body_budget_bytes',p['original_body_cap']-p['prior_charged_body_bytes']),('prior_global_deadline_epoch',p['prior_global_deadline_epoch']),('members',profile['index_members'])]:
        require_equal(b.get(key),expected,'Cache history/inventory changed: '+key)
    elapsed=b.get('prior_transfer_elapsed_seconds')
    try:valid=type(elapsed) in (int,float) and math.isfinite(elapsed) and abs(elapsed-p['prior_transfer_elapsed_seconds'])<=1e-6
    except OverflowError:valid=False
    if not valid:fail('Prior spent time changed')
    idx=path(b.get('index_root'));original=path(b.get('original_root'));recovery=path(b.get('recovery_root'))
    if len({idx,original,recovery})!=3:fail('Distinct lineage roots required')
    if path(b.get('index_prefix'))!=idx/'index/files/hg38/genome':fail('Index prefix changed')
    if path(job['root'])!=idx.with_name(idx.name+'-reads-01'):fail('Exclusive derived root changed')
    require_equal(b.get('aligner'),m['aligner'],'Aligner binding differs')
    if set(m['real_compute'])!=set(profile['compute_fields']):fail('Compute libraries changed')
    for name,expected in profile['compute_fields'].items():
        actual=m['real_compute'][name]
        if not isinstance(actual,dict) or set(actual)!=set(expected)|{'limits'}:fail('Compute spec schema')
        require_equal({k:actual[k] for k in expected},expected,'Compute target/coverage/sample changed')
        if not isinstance(actual['limits'],dict) or type(actual['limits'].get('max_temp_bytes')) is not int or actual['limits']['max_temp_bytes']!=4*1024**3:fail('Compact temporary allocation changed')
    result=proposal_review(p,profile)
    result.update(status='declared_offline_policy_checks_passed',disabled_descriptor_provided=True,descriptor_source_not_authenticated=True,
                  worker_source_commit=profile['worker_source_commit'],
                  not_verified=['host filesystem/seals/index','binary/Python/producer/decoder identities','complete compact reducer policy','resource observation','operator acceptance'],
                  replaces_worker_validation=False)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(__doc__);g=parser.add_mutually_exclusive_group(required=True);g.add_argument('--plan');g.add_argument('--proposal');args=parser.parse_args()
    profile,profile_sha=load(PROFILE)
    if profile_sha!=PROFILE_SHA256:fail('Review profile hash changed')
    value,sha=load(args.plan or args.proposal)
    result=review(value,profile) if args.plan else proposal_review(value,profile)
    result['input_file_sha256']=sha;print(json.dumps(result,indent=2))
