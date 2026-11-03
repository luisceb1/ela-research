"""Demonstrate partial offline review against archived proposal and synthetic JSON."""
import copy
import json
from pathlib import Path
import sys
import platform
import audit_cached_pilot_descriptor as audit
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from test_cached_pilot_descriptor_review import fixture,negatives


def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    profile,sha=audit.load(audit.PROFILE)
    if sha!=audit.PROFILE_SHA256:raise ValueError('Changed review profile')
    root=Path(__file__).resolve().parents[1]
    proposal,input_sha=audit.load(root/'reports/cached-index-pilot-20261102/execution-proposal.json')
    actual=audit.proposal_review(proposal,profile);actual['source_file_sha256']=input_sha
    (out/'archived-proposal-review.json').write_text(json.dumps(actual,indent=2)+'\n')
    job=fixture(profile);a=audit.review(job,profile);b=audit.review(copy.deepcopy(job),profile)
    one=json.dumps(a,indent=2)+'\n';two=json.dumps(b,indent=2)+'\n'
    if one!=two:raise ValueError('Repeated fixture review differs')
    (out/'synthetic-descriptor.json').write_text(json.dumps(job,indent=2)+'\n')
    (out/'synthetic-review-1.json').write_text(one);(out/'synthetic-review-2.json').write_text(two)
    rejected=[]
    for name,value in negatives(job):
        try:audit.review(value,profile)
        except ValueError as exc:rejected.append({'synthetic_case':name,'error':str(exc)})
        else:raise AssertionError('Mutated descriptor unexpectedly passed: '+name)
    (out/'negative-cases.json').write_text(json.dumps(rejected,indent=2)+'\n')
    (out/'summary.json').write_text(json.dumps({'python':platform.python_version(),'worker_source_commit':profile['worker_source_commit'],
      'real_proposal_metadata_checked':True,'real_WSL_descriptor_provided':False,'synthetic_descriptor_only':True,
      'negative_mutations_rejected':len(rejected),'repeated_review_byte_identical':True,
      'host_files_accessed':False,'network_or_worker_execution':False,'new_data_transfer_bytes':0,
      'window_authorized':False,'execution_enabled':False,'raw_execution_ready':False},indent=2)+'\n')
    print('Archived proposal arithmetic checked; synthetic-only descriptor and',len(rejected),'negative cases persisted')


if __name__=='__main__':run(sys.argv[1])
