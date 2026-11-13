"""Bind a consumed ranged attempt and validate its retained complete blocks offline."""
import hashlib
import json
from pathlib import Path

V2_SHA='98a89d95c199fb13e90ac5f68c2b33cec1251daf62313d83ec4b4b1fe649af6d'
V2_CHARGE=2111084972
V2_OBSERVED=1759157246
V2_COMPLETE_BYTES=1645215744


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024**2),b''):h.update(b)
    return h.hexdigest()


def regular(path, directory):
    path=Path(path);directory=Path(directory).resolve()
    if path.is_symlink() or not path.is_file() or path.resolve().parent!=directory:
        raise ValueError('Retained path must be a regular file in the exact expected directory')
    # A symlinked parent is also refused, even when its target stays in the old root.
    if any(p.is_symlink() for p in [path.parent,*path.parents]):
        raise ValueError('Symlink in retained evidence path')
    return path


def record(plan_path, read_small, v1_record, settings, base_sha, cap, current_files=True):
    plan_path=Path(plan_path).resolve()
    if sha(plan_path)!=V2_SHA:raise ValueError('Consumed v2 proposal SHA mismatch')
    old=read_small(plan_path)
    if old.get('schema')!='gse252892-range-v2' or old.get('base_sha256')!=base_sha or old.get('transport')!=settings:
        raise ValueError('Unexpected v2 identity/settings')
    inherited=v1_record(old['lineage']['prior_plan_path'],current_prefix=current_files)
    if inherited!=old['lineage']:raise ValueError('Inherited v1 evidence changed')
    root=Path(old['run_root']);first=old['base']['input_files'][0]
    if first['url']!=inherited['prefix']['url']:raise ValueError('Unexpected v2 first URL')
    paths={n:root/n for n in ['accepted.json','supervision.json','worker-failure.json','transfer-ledger.json']}
    paths['proposal_claim.json']=Path(str(plan_path)+'.claimed.json')
    evidence={n:read_small(p) for n,p in paths.items()};sup=evidence['supervision.json'];ledger=evidence['transfer-ledger.json']
    claim={'plan_sha256':V2_SHA,'transfer_bytes':cap}
    if evidence['proposal_claim.json']!=claim or any(evidence['accepted.json'].get(k)!=v for k,v in claim.items()):raise ValueError('Consumed v2 claim/acceptance changed')
    if sup.get('plan_sha256')!=V2_SHA or sup.get('status')!='failed' or sup.get('cleanup_error') is not None:
        raise ValueError('Prior v2 must be failed and cleaned up')
    if evidence['worker-failure.json'].get('error')!='Short range body / premature EOF':raise ValueError('Unexpected v2 failure')
    expected={'prior_charge_bytes':inherited['prior_charge_bytes'],'new_observed_body_bytes':V2_OBSERVED,
        'actual_body_bytes':V2_CHARGE,'new_charged_upper_bytes':V2_OBSERVED,'body_upper_bound_bytes':V2_CHARGE,
        'cap_bytes':cap,'request_attempts':60,'completed_attempts':60,'active_requests':[]}
    if any(ledger.get(k)!=v for k,v in expected.items()):raise ValueError('Prior v2 cumulative charge/state changed')
    receipts=root/'transport-receipts';files=sorted(receipts.glob('*.json'))
    if [p.name for p in files]!=[f'{i:06d}.json' for i in range(1,61)]:raise ValueError('Expected all 60 attempt receipts')
    if ledger.get('receipt_directory')!=str(receipts):raise ValueError('Receipt directory changed')
    total=int(first['compressed_bytes']);prefix=inherited['prefix'];overlap=(prefix['bytes']-settings['overlap_bytes'],prefix['bytes']-1)
    allowed={(a,min(a+settings['chunk_bytes'],total)-1) for a in range(prefix['bytes'],total,settings['chunk_bytes'])}
    ranges=root/'GSM8009878'/(Path(first['url']).name+'.ranges')
    complete=[];seen=set();observed=charged=complete_bytes=0;statuses=[];receipt_hashes={}
    for i,p in enumerate(files,1):
        regular(p,receipts);r=read_small(p);interval=(r['start'],r['end']);n=r['end']-r['start']+1
        if r['id']!=i or r['url']!=first['url'] or r['total']!=total or interval not in allowed|{overlap} or r['attempt'] not in (1,2,3):
            raise ValueError('Unexpected retained receipt identity/range')
        if r['status'] not in ('complete','failed') or r['inflight_max_bytes']!=0 or r['uncertain_bytes']!=0 or r['charged_bytes']!=r['observed_bytes'] or not 0<=r['observed_bytes']<=n:
            raise ValueError('Unsettled or invalid retained receipt')
        observed+=r['observed_bytes'];charged+=r['charged_bytes'];statuses.append(r['status']);receipt_hashes[p.name]=sha(p)
        if r['status']!='complete':continue
        if r['observed_bytes']!=n or interval in seen:raise ValueError('Duplicate/incomplete successful interval')
        seen.add(interval);complete_bytes+=n
        expected_path=ranges/f'range-{r["start"]:012d}-{r["end"]:012d}-a{r["attempt"]}.ok'
        if Path(r['path'])!=expected_path:raise ValueError('Retained block path changed')
        if current_files:
            regular(expected_path,ranges)
            if expected_path.stat().st_size!=n or sha(expected_path)!=r['sha256']:raise ValueError('Retained block size/hash changed')
        if interval!=overlap:
            complete.append({'path':str(expected_path),'start':r['start'],'end':r['end'],'bytes':n,'sha256':r['sha256'],'url':r['url']})
    if observed!=V2_OBSERVED or charged!=V2_OBSERVED or complete_bytes!=V2_COMPLETE_BYTES or statuses.count('complete')!=50 or len(complete)!=49 or overlap not in seen:
        raise ValueError('Receipt totals disagree with recorded v2 outcome')
    complete.sort(key=lambda x:x['start'])
    return {'prior_plan_path':str(plan_path),'prior_plan_sha256':V2_SHA,'prior_root':str(root),
        'prior_roots':[inherited['prior_root'],str(root)],'prior_charge_bytes':V2_CHARGE,
        'receipt_sha256':{n:sha(p) for n,p in paths.items()},'attempt_receipt_sha256':receipt_hashes,
        'inherited_v1':inherited,'prefix':prefix,'retained_blocks':complete}
