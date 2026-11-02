"""Read-only audit of the first interrupted real index transfer.

Never opens a URL, edits the run, resumes a phase, resets a deadline or promotes
partial data. Streaming SHA of the partial is identity, not source verification.
Standalone stdlib so an old job can be audited without importing a newer worker.
"""
import argparse
import hashlib
import json
from pathlib import Path
import stat

MAX_METADATA=1024**2
INDEX_BYTES=4355786349
INDEX_SHA='1848784403a0fb3ee7735b2f891d8be96fd2782e08aed3d8212d922666f077a5'
INDEX_URL='https://genome-idx.s3.amazonaws.com/hisat/hg38_genome.tar.gz?versionId=8z.MUbL_W4wij.Nmcia5c4mT7tlz0cU.'
RAW_BYTES=6349703881


def metadata(path):
    if path.is_symlink() or not path.is_file():raise ValueError('Regular metadata required: '+path.name)
    with path.open('rb') as f:data=f.read(MAX_METADATA+1)
    if len(data)>MAX_METADATA:raise ValueError('Metadata cap')
    return json.loads(data),hashlib.sha256(data).hexdigest()


def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def inspect(root):
    root=Path(root).resolve()
    names=('workflow-job.json','operator-acceptance.json','ledger.json','preflight-result.json',
           'index_archive.attempt-0.json','workflow-receipts/run.json')
    snapshots={name:metadata(root/name) for name in names}
    job,jsha=snapshots['workflow-job.json'];acceptance,_=snapshots['operator-acceptance.json']
    ledger,_=snapshots['ledger.json'];outer,_=snapshots['workflow-receipts/run.json']
    http,_=snapshots['index_archive.attempt-0.json']
    if job.get('root')!=str(root) or acceptance.get('prepared_file_sha256')!=jsha:raise ValueError('Job/acceptance/root mismatch')
    if ledger.get('fingerprint')!=digest({'manifest':job['manifest'],'limits':job['limits']}):raise ValueError('Ledger fingerprint mismatch')
    if ledger.get('limits')!=job['limits']:raise ValueError('Ledger limits mismatch')
    phases=ledger.get('phases',{})
    if set(phases)!={'preflight','index_archive'} or phases['preflight'].get('status')!='verified' or phases['index_archive'].get('status') not in ('started','failed'):raise ValueError('Only interrupted first index transfer supported')
    if phases['preflight'].get('receipt_sha256')!=snapshots['preflight-result.json'][1] or snapshots['preflight-result.json'][0].get('status')!='verified':raise ValueError('Preflight identity mismatch')
    step=next((s for s in job['manifest']['sealed_workflow']['steps'] if s['name']=='index_archive'),None)
    if not step or step.get('url')!=INDEX_URL or step.get('expected')!={'bytes':INDEX_BYTES,'sha256':INDEX_SHA}:raise ValueError('Pinned index descriptor mismatch')
    if outer.get('status')!='finished' or outer.get('live_group_members_after_cleanup')!=[] or outer.get('exit_code')==0:raise ValueError('Failed supervisor with no remaining group required')
    if (root/'workflow-seal.json').exists() or (root/'index_archive').exists():raise ValueError('Unexpected promoted result; separate audit required')
    path=root/'index_archive.attempt-0.partial'
    if path.is_symlink():raise ValueError('Partial symlink refused')
    before=path.stat()
    if not stat.S_ISREG(before.st_mode) or not 0<before.st_size<INDEX_BYTES:raise ValueError('Bounded nonempty incomplete regular partial required')
    charged=ledger.get('transfer_bytes_consumed')
    if type(charged) is not int or charged<before.st_size or charged>job['limits']['transfer_bytes']:raise ValueError('Partial exceeds charged body budget')
    if type(http.get('body_bytes')) is not int or not 0<=http['body_bytes']<=charged or http.get('status') not in ('started','failed'):raise ValueError('HTTP attempt inconsistent')
    h=hashlib.sha256();count=0
    with path.open('rb') as f:
        while True:
            block=f.read(min(1024**2,INDEX_BYTES-count+1))
            if not block:break
            count+=len(block)
            if count>=INDEX_BYTES:raise ValueError('Partial grew during audit')
            h.update(block)
    after=path.stat()
    if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns) or count!=before.st_size:raise ValueError('Partial changed during audit')
    for name,(_,sha) in snapshots.items():
        if metadata(root/name)[1]!=sha:raise ValueError('Run metadata changed during audit')
    elapsed=ledger.get('transfer_elapsed_seconds',0)
    return {'status':'AUDITED_INTERRUPTED_NOT_RESUMABLE','root':str(root),'source_verified':False,
        'metadata_sha256':{name:sha for name,(_,sha) in snapshots.items()},
        'expected_index_bytes':INDEX_BYTES,'partial_bytes':count,'partial_sha256':h.hexdigest(),
        'partial_percent':round(100*count/INDEX_BYTES,2),'charged_body_bytes':charged,
        'charged_minus_partial_bytes':charged-count,'remaining_body_budget_bytes':job['limits']['transfer_bytes']-charged,
        'minimum_remaining_body_if_range_is_later_validated':INDEX_BYTES-count+RAW_BYTES,
        'prior_transfer_elapsed_seconds':elapsed,'observed_average_body_bytes_per_second':round(charged/elapsed,2) if elapsed>0 else None,
        'prior_global_deadline_epoch':ledger['deadline_epoch'],'outer_exit_code':outer.get('exit_code'),
        'outer_error':outer.get('supervisor_error'),'worker_group_empty_at_cleanup':True,
        'next':'explicit recovery design and time-budget review required; no automatic renewal, retry or range request'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True)
    print(json.dumps(inspect(p.parse_args().root),indent=2))
