"""Bounded metadata seal for a local workflow; never hashes bulk data in parent."""
import hashlib
import json
from pathlib import Path

MAX_METADATA=1024**2
FILES=('workflow-job.json','ledger.json','workflow-inner.json','workflow-receipts/run.json')


def read(path):
    with Path(path).open('rb') as f:data=f.read(MAX_METADATA+1)
    if len(data)>MAX_METADATA:raise ValueError('Workflow metadata cap')
    return json.loads(data)


def sha(path):
    with Path(path).open('rb') as f:data=f.read(MAX_METADATA+1)
    if len(data)>MAX_METADATA:raise ValueError('Workflow metadata cap')
    return hashlib.sha256(data).hexdigest()


def check_outer(record):
    if record.get('status')!='finished' or record.get('exit_code')!=0 or record.get('violation') is not None or record.get('supervisor_error') is not None or record.get('live_group_members_after_cleanup')!=[]:raise ValueError('Workflow supervision did not finish cleanly')


def assert_seal(root,manifest,limits):
    root=Path(root);path=root/'workflow-seal.json'
    if not path.exists():raise ValueError('Workflow has no external seal; do not adopt inner results')
    seal=read(path)
    if seal.get('status')!='sealed' or set(seal.get('sha256',{}))!=set(FILES):raise ValueError('Incomplete workflow seal')
    for name in FILES:
        if sha(root/name)!=seal['sha256'][name]:raise ValueError('Workflow sealed metadata changed: '+name)
    job=read(root/'workflow-job.json');ledger=read(root/'ledger.json');inner=read(root/'workflow-inner.json')
    if job.get('root')!=str(root.resolve()) or job.get('manifest')!=manifest or job.get('limits')!=limits:raise ValueError('Workflow descriptor identity changed')
    if inner.get('status') not in ('complete','coverage_insufficient') or inner.get('ledger_sha256')!=sha(root/'ledger.json'):raise ValueError('Incomplete workflow result')
    if any(p.get('status')!='verified' for p in ledger['phases'].values()):raise ValueError('Workflow contains incomplete phase')
    check_outer(read(root/'workflow-receipts/run.json'))
    return seal
