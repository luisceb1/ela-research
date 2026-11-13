"""Bind failed interop execution and revalidate both complete control inputs."""
from pathlib import Path
import gse252892_retained_blocks as b
import gse252892_after_sampler as a

V4_SHA='c7a2fee183c48f5fd8c925bd65402ead0f9e44127df89ea8a690b48944a93528'
CHARGE=5859663274
OBSERVED=5858614698
NEW_OBSERVED=1896122539
SECOND_SHA='3dbaa49e5d28084c261921199c25044b7fe9e89129278df037c64e90e7c27354'


def record(plan_path,read_small,v3_record,settings,base_sha,cap,current_files=True):
    plan_path=Path(plan_path).resolve()
    if b.sha(plan_path)!=V4_SHA:raise ValueError('Consumed v4 proposal SHA mismatch')
    old=read_small(plan_path)
    if old.get('schema')!='gse252892-after-sampler-v4' or old.get('transport')!=settings or old.get('base_sha256')!=base_sha:raise ValueError('Unexpected v4 identity/settings')
    inherited=v3_record(old['lineage']['prior_plan_path'],current_files=current_files)
    if inherited!=old['lineage']:raise ValueError('Inherited v3 evidence changed')
    root=Path(old['run_root']);claim={'plan_sha256':V4_SHA,'transfer_bytes':cap}
    paths={n:root/n for n in ['accepted.json','supervision.json','transfer-ledger.json']}
    paths['proposal_claim.json']=Path(str(plan_path)+'.claimed.json')
    evidence={n:read_small(p) for n,p in paths.items()};sup=evidence['supervision.json'];ledger=evidence['transfer-ledger.json']
    if evidence['proposal_claim.json']!=claim or any(evidence['accepted.json'].get(k)!=v for k,v in claim.items()):raise ValueError('Consumed v4 claim/acceptance changed')
    if sup.get('status')!='failed' or sup.get('cleanup_error') is not None or sup.get('plan_sha256')!=V4_SHA or not sup.get('failure','').startswith('Cannot query real C: free space through '):raise ValueError('Expected cleaned-up interop failure')
    for p in [root/'worker-failure.json',root/'result.json',root/'GSM8009878'/'junction-counts.json']:
        if p.exists():raise ValueError('Unexpected worker/result/count receipt; inspect before continuation')
    expected={'prior_charge_bytes':inherited['prior_charge_bytes'],'prior_observed_body_bytes':inherited['prior_observed_body_bytes'],
        'prior_unobserved_bytes_charged':inherited['prior_charge_bytes']-inherited['prior_observed_body_bytes'],
        'new_observed_body_bytes':NEW_OBSERVED,'actual_body_bytes':OBSERVED,'new_charged_upper_bytes':NEW_OBSERVED,
        'body_upper_bound_bytes':CHARGE,'cap_bytes':cap,'request_attempts':233,'completed_attempts':233,'active_requests':[]}
    if any(ledger.get(k)!=v for k,v in expected.items()):raise ValueError('Final settled v4 ledger changed')
    rows=old['base']['input_files'][:2];directory=root/'GSM8009878';complete=[]
    for row,wanted_sha in zip(rows,[a.FIRST_SHA,SECOND_SHA]):
        path=directory/Path(row['url']).name;receipt=path.with_name(path.name+'.verified.json');info=read_small(receipt)
        if row['gsm']!='GSM8009878' or info.get('status')!='verified_complete' or info.get('path')!=str(path) or (info.get('bytes'),info.get('md5'),info.get('sha256'))!=(int(row['compressed_bytes']),row['md5'],wanted_sha):raise ValueError('Complete control input identity changed')
        if current_files:
            b.regular(path,directory)
            if a.full_digest(path)!=(info['bytes'],info['md5'],info['sha256']):raise ValueError('Complete control input digest changed')
        paths[path.name+'.verified.json']=receipt
        complete.append({'url':row['url'],'path':str(path),'bytes':info['bytes'],'md5':info['md5'],'sha256':info['sha256']})
    receipts=root/'transport-receipts';files=sorted(receipts.glob('*.json'));hashes={};observed=charged=0
    if [p.name for p in files]!=[f'{i:06d}.json' for i in range(1,234)] or ledger['receipt_directory']!=str(receipts):raise ValueError('Expected all 233 settled v4 receipts')
    for i,p in enumerate(files,1):
        b.regular(p,receipts);r=read_small(p)
        if r['id']!=i or r['url']!=rows[1]['url'] or r['total']!=int(rows[1]['compressed_bytes']) or r['status'] not in ('complete','failed') or r['inflight_max_bytes']!=0 or r['uncertain_bytes']!=0 or r['charged_bytes']!=r['observed_bytes'] or not 0<=r['observed_bytes']<=r['end']-r['start']+1:
            raise ValueError('Invalid settled v4 request receipt')
        observed+=r['observed_bytes'];charged+=r['charged_bytes'];hashes[p.name]=b.sha(p)
    if observed!=NEW_OBSERVED or charged!=NEW_OBSERVED:raise ValueError('Settled v4 per-request totals disagree')
    for name in ['fastp.log','fastp.json']:paths[name]=directory/name
    return {'prior_plan_path':str(plan_path),'prior_plan_sha256':V4_SHA,'prior_root':str(root),
        'prior_roots':inherited['prior_roots']+[str(root)],'prior_charge_bytes':CHARGE,'prior_observed_body_bytes':OBSERVED,
        'receipt_sha256':{n:b.sha(p) for n,p in paths.items()},'attempt_receipt_sha256':hashes,'inherited_v3':inherited,
        'complete_inputs':complete,'retained_blocks':[],'worker_and_count_receipts_absent':True}
