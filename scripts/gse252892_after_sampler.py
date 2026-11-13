"""Offline continuation evidence after a supervisor stop, preserving reserved bytes."""
import hashlib
import os
from pathlib import Path
import gse252892_retained_blocks as oldblocks

V3_SHA='e131b017001b8f8f5b877c2aeb1aa4589609f9639f1c5b4093af9de359fac1ca'
V3_UPPER=3963540735
V3_OBSERVED=1851407187
V3_COMPLETE_BYTES=1809305882
FIRST_SHA='ddd42a540b6d01ca2405692cd6bf65ae35485c8b5e66f8eda2aec5fc62086bb6'


def full_digest(path):
    md5=hashlib.md5();sha=hashlib.sha256();n=0
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024**2),b''):md5.update(b);sha.update(b);n+=len(b)
    return n,md5.hexdigest(),sha.hexdigest()


def reconcile(ledger,records):
    """Deduplicate a durable receipt also present in an interrupted active snapshot."""
    byid={r['id']:r for r in records}
    if len(byid)!=len(records):raise ValueError('Duplicate durable request ID')
    active=ledger['active_requests']
    if len({r['id'] for r in active})!=len(active):raise ValueError('Duplicate active request ID')
    observed={i:r['observed_bytes'] for i,r in byid.items()}
    upper={i:r['charged_bytes']+r['inflight_max_bytes'] for i,r in byid.items()}
    for r in active:
        i=r['id']
        if i in byid:
            done=byid[i]
            for k in ['url','start','end','total','attempt','observed_bytes','charged_bytes','uncertain_bytes']:
                if done[k]!=r[k]:raise ValueError('Durable/active request snapshot disagrees')
        observed[i]=max(observed.get(i,0),r['observed_bytes'])
        upper[i]=max(upper.get(i,0),r['charged_bytes']+r['inflight_max_bytes'])
    if set(upper)!=set(range(1,ledger['request_attempts']+1)):raise ValueError('Missing request identity in final accounting')
    if sum(observed.values())!=ledger['new_observed_body_bytes']:raise ValueError('Observed per-request totals disagree')
    charge=ledger['prior_charge_bytes']+sum(upper.values())
    if charge!=ledger['body_upper_bound_bytes']:raise ValueError('Conservative per-request totals disagree')
    return charge


def record(plan_path,read_small,v2_record,settings,base_sha,cap,current_files=True):
    plan_path=Path(plan_path).resolve()
    if oldblocks.sha(plan_path)!=V3_SHA:raise ValueError('Consumed v3 SHA mismatch')
    old=read_small(plan_path)
    if old.get('schema')!='gse252892-retained-v3' or old.get('base_sha256')!=base_sha or old.get('transport')!=settings:
        raise ValueError('Unexpected v3 identity/settings')
    inherited=v2_record(old['lineage']['prior_plan_path'],current_files=current_files)
    if inherited!=old['lineage']:raise ValueError('Inherited v2 evidence changed')
    root=Path(old['run_root']);rows=old['base']['input_files'];first,second=rows[:2]
    if first['gsm']!='GSM8009878' or second['gsm']!='GSM8009878':raise ValueError('Unexpected fixed control identity')
    paths={n:root/n for n in ['accepted.json','supervision.json','transfer-ledger.json']}
    paths['proposal_claim.json']=Path(str(plan_path)+'.claimed.json')
    evidence={n:read_small(p) for n,p in paths.items()};sup=evidence['supervision.json'];ledger=evidence['transfer-ledger.json']
    claim={'plan_sha256':V3_SHA,'transfer_bytes':cap}
    if evidence['proposal_claim.json']!=claim or any(evidence['accepted.json'].get(k)!=v for k,v in claim.items()):raise ValueError('Consumed v3 claim/acceptance changed')
    expected_failure=f"[Errno 2] No such file or directory: '{root}/transport-receipts/000232.json.tmp'"
    if sup.get('plan_sha256')!=V3_SHA or sup.get('status')!='failed' or sup.get('cleanup_error') is not None or sup.get('failure')!=expected_failure:
        raise ValueError('Expected cleaned-up sampler failure')
    if (root/'worker-failure.json').exists():raise ValueError('Unexpected worker failure receipt')
    expected={'prior_charge_bytes':inherited['prior_charge_bytes'],'new_observed_body_bytes':V3_OBSERVED,
        'actual_body_bytes':inherited['prior_charge_bytes']+V3_OBSERVED,'new_charged_upper_bytes':V3_OBSERVED,
        'body_upper_bound_bytes':V3_UPPER,'cap_bytes':cap,'request_attempts':233,'completed_attempts':231}
    if any(ledger.get(k)!=v for k,v in expected.items()) or [r['id'] for r in ledger['active_requests']]!=[232,233]:raise ValueError('Final v3 ledger changed')
    for i,r in enumerate(ledger['active_requests']):
        a=(122+i)*settings['chunk_bytes']
        if r['url']!=second['url'] or r['total']!=int(second['compressed_bytes']) or (r['start'],r['end'])!=(a,a+settings['chunk_bytes']-1) or r['attempt']!=1 or r['status']!='started' or r['observed_bytes']!=(settings['chunk_bytes'] if i==0 else settings['chunk_bytes']//2) or r['charged_bytes']!=r['observed_bytes'] or r['uncertain_bytes']!=0 or r['inflight_max_bytes']!=(0 if i==0 else settings['overlap_bytes']):
            raise ValueError('Interrupted v3 active snapshot changed')
    receipt_dir=root/'transport-receipts';files=sorted(receipt_dir.glob('*.json'))
    if [p.name for p in files]!=[f'{i:06d}.json' for i in range(1,233)] or ledger['receipt_directory']!=str(receipt_dir):raise ValueError('Expected all 232 durable v3 receipts')
    records=[];receipt_hashes={};sources={r['url']:r for r in [first,second]};pieces=[];seen=set()
    for i,p in enumerate(files,1):
        oldblocks.regular(p,receipt_dir);r=read_small(p);source=sources.get(r['url']);n=r['end']-r['start']+1
        if source is None or r['id']!=i or r['total']!=int(source['compressed_bytes']) or not 0<=r['start']<=r['end']<r['total'] or not 0<n<=settings['chunk_bytes'] or r['attempt'] not in range(1,6):
            raise ValueError('Unexpected v3 receipt source/identity/interval')
        if r['status'] not in ('complete','failed') or r['inflight_max_bytes']!=0 or r['uncertain_bytes']!=0 or r['charged_bytes']!=r['observed_bytes'] or not 0<=r['observed_bytes']<=n:
            raise ValueError('Invalid completed v3 receipt accounting')
        records.append(r);receipt_hashes[p.name]=oldblocks.sha(p)
        if r['url']!=second['url'] or r['status']!='complete':continue
        interval=(r['start'],r['end'])
        if r['observed_bytes']!=n or interval in seen or r['start']%settings['chunk_bytes']!=0 or n!=settings['chunk_bytes']:
            raise ValueError('Invalid retained second-file interval')
        seen.add(interval);directory=root/'GSM8009878'/(Path(second['url']).name+'.ranges')
        path=directory/f'range-{r["start"]:012d}-{r["end"]:012d}-a{r["attempt"]}.ok'
        if Path(r['path'])!=path:raise ValueError('Second-file retained path changed')
        if current_files:
            oldblocks.regular(path,directory)
            if path.stat().st_size!=n or oldblocks.sha(path)!=r['sha256']:raise ValueError('Second-file block size/hash changed')
        pieces.append({'path':str(path),'start':r['start'],'end':r['end'],'bytes':n,'sha256':r['sha256'],'url':r['url']})
    if sum(r['status']=='complete' for r in records)!=217 or sum(r['observed_bytes'] for r in records if r['status']=='complete')!=V3_COMPLETE_BYTES:
        raise ValueError('Durable v3 receipt totals changed')
    prior_charge=reconcile(ledger,records)
    pieces.sort(key=lambda p:p['start'])
    if len(pieces)!=123 or [(p['start'],p['end']) for p in pieces]!=[(i*settings['chunk_bytes'],(i+1)*settings['chunk_bytes']-1) for i in range(123)]:raise ValueError('Expected 123 contiguous retained second-file blocks')
    path=root/'GSM8009878'/Path(first['url']).name;receipt=path.with_name(path.name+'.verified.json');info=read_small(receipt)
    if info.get('status')!='verified_complete' or info.get('path')!=str(path) or info.get('bytes')!=int(first['compressed_bytes']) or info.get('md5')!=first['md5'] or info.get('sha256')!=FIRST_SHA:
        raise ValueError('First complete-file identity changed')
    if current_files:
        oldblocks.regular(path,path.parent)
        if full_digest(path)!=(info['bytes'],info['md5'],info['sha256']):raise ValueError('First complete-file digest changed')
    paths['first_file_verified.json']=receipt
    return {'prior_plan_path':str(plan_path),'prior_plan_sha256':V3_SHA,'prior_root':str(root),
        'prior_roots':inherited['prior_roots']+[str(root)],'prior_charge_bytes':prior_charge,
        'prior_observed_body_bytes':ledger['actual_body_bytes'],
        'receipt_sha256':{n:oldblocks.sha(p) for n,p in paths.items()},'attempt_receipt_sha256':receipt_hashes,
        'worker_failure_absent':True,'inherited_v2':inherited,'retained_blocks':pieces,
        'complete_inputs':[{'url':first['url'],'path':str(path),'bytes':info['bytes'],'md5':info['md5'],'sha256':info['sha256']}]}


def copy_complete(item,source,directory,save):
    """Copy a verified full input without changing or linking the old source."""
    directory=Path(directory);target=directory/Path(item['url']).name;temp=target.with_name(target.name+'.copying')
    if target.exists() or temp.exists():raise ValueError('No complete-input overwrite')
    oldblocks.regular(source['path'],Path(source['path']).parent)
    if source['url']!=item['url'] or source['bytes']!=int(item['compressed_bytes']) or source['md5']!=item['md5']:raise ValueError('Copied complete-input source mismatch')
    md5=hashlib.md5();sha=hashlib.sha256();n=0
    with Path(source['path']).open('rb') as src,temp.open('xb') as dst:
        for b in iter(lambda:src.read(1024**2),b''):dst.write(b);md5.update(b);sha.update(b);n+=len(b)
        dst.flush();os.fsync(dst.fileno())
    if (n,md5.hexdigest(),sha.hexdigest())!=(source['bytes'],source['md5'],source['sha256']):raise ValueError('Copied complete-file digest mismatch')
    os.replace(temp,target)
    save(target.with_name(target.name+'.verified.json'),{'path':str(target),'bytes':n,'md5':md5.hexdigest(),'sha256':sha.hexdigest(),'status':'verified_complete','copied_from':source['path'],'raw_body_bytes':0})
    return target
