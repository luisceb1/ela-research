"""Bind a zero-transfer user-interrupted run without resetting its old claim."""
from pathlib import Path
import gse252892_retained_blocks as b

PLAN_SHA='7a39bc2df33e54d95846bb309292d57aa5f0aa35607427f80c8d4d7aaaadaec0'


def record(plan_path,read_small,v4_record,settings,base_sha,cap,current_files=True):
    plan_path=Path(plan_path).resolve()
    if b.sha(plan_path)!=PLAN_SHA:raise ValueError('Interrupted consumed proposal SHA mismatch')
    old=read_small(plan_path)
    if old.get('schema')!='gse252892-drvfs-v5' or old.get('transport')!=settings or old.get('base_sha256')!=base_sha:raise ValueError('Unexpected interrupted identity/settings')
    inherited=v4_record(old['lineage']['prior_plan_path'],current_files=current_files)
    if inherited!=old['lineage']:raise ValueError('Interrupted inherited evidence changed')
    root=Path(old['run_root']);paths={n:root/n for n in ['accepted.json','supervision.json','transfer-ledger.json']}
    paths['proposal_claim.json']=Path(str(plan_path)+'.claimed.json')
    evidence={n:read_small(p) for n,p in paths.items()};sup=evidence['supervision.json'];ledger=evidence['transfer-ledger.json']
    claim={'plan_sha256':PLAN_SHA,'transfer_bytes':cap}
    if evidence['proposal_claim.json']!=claim or any(evidence['accepted.json'].get(k)!=v for k,v in claim.items()):raise ValueError('Interrupted consumed claim/acceptance changed')
    if sup.get('status')!='failed' or sup.get('failure')!='KeyboardInterrupt' or sup.get('cleanup_error') is not None or sup.get('plan_sha256')!=PLAN_SHA:raise ValueError('Expected cleaned-up user interruption')
    expected={'prior_charge_bytes':inherited['prior_charge_bytes'],'prior_observed_body_bytes':inherited['prior_observed_body_bytes'],
        'prior_unobserved_bytes_charged':inherited['prior_charge_bytes']-inherited['prior_observed_body_bytes'],
        'new_observed_body_bytes':0,'actual_body_bytes':inherited['prior_observed_body_bytes'],'new_charged_upper_bytes':0,
        'body_upper_bound_bytes':inherited['prior_charge_bytes'],'cap_bytes':cap,'request_attempts':0,'completed_attempts':0,'active_requests':[],'last_completed':None}
    if any(ledger.get(k)!=v for k,v in expected.items()):raise ValueError('Expected exact zero-transfer interrupted ledger')
    receipts=root/'transport-receipts'
    if ledger['receipt_directory']!=str(receipts) or receipts.is_symlink() or not receipts.is_dir() or any(receipts.iterdir()):raise ValueError('Unexpected zero-transfer request evidence')
    for p in [root/'result.json',root/'worker-failure.json',root/'GSM8009878'/'junction-counts.json']:
        if p.exists():raise ValueError('Unexpected interrupted result/worker/count receipt')
    return {'prior_plan_path':str(plan_path),'prior_plan_sha256':PLAN_SHA,'prior_root':str(root),
        'prior_roots':inherited['prior_roots']+[str(root)],'prior_charge_bytes':inherited['prior_charge_bytes'],
        'prior_observed_body_bytes':inherited['prior_observed_body_bytes'],'receipt_sha256':{n:b.sha(p) for n,p in paths.items()},
        'inherited_v4':inherited,'complete_inputs':inherited['complete_inputs'],'retained_blocks':[],
        'zero_transfer_interruption':True}
