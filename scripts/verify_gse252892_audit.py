"""Verify supplied metadata archive without extraction or sequencing-data replay."""
import argparse
from collections import Counter
import hashlib,json,re,subprocess,zipfile
from pathlib import Path,PurePosixPath

EXPECTED_ZIP='c8751b9610512791ba40a613449ad332833ff557e8c371f96e118636361e4617'
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(path):
    raw=Path(path).read_bytes();assert len(raw)==1091994 and sha(raw)==EXPECTED_ZIP,'Unexpected archive'
    with zipfile.ZipFile(path) as z:
        infos=z.infolist();names=[i.filename for i in infos]
        assert len(names)==len(set(names))==1464
        assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names)
        assert sum(i.file_size for i in infos)<55*1024**2
        data={n:z.read(n) for n in names};manifest=json.loads(data['MANIFEST.json'])
    records=manifest['files'];assert len(records)==1463
    assert set(data)=={'MANIFEST.json',*(r['member'] for r in records)}
    assert sum(r['bytes'] for r in records)==manifest['metadata_bytes']==1959447
    for r in records:assert len(data[r['member']])==r['bytes'] and sha(data[r['member']])==r['sha256']
    assert not any(n.endswith(('.fastq','.fq','.fastq.gz','.fq.gz','.sam','.bam','.ht2','.partial')) for n in names)
    source={r['source']:r['member'] for r in records};assert len(source)==len(records)
    get=lambda n:json.loads(data[n])
    code_checks=0;bindings=set();plans=[]
    def embedded(node):
        if isinstance(node,dict):
            if 'prior_plan_path' in node:
                p=node['prior_plan_path'];assert sha(data[source[p]])==node['prior_plan_sha256'];bindings.add(p)
            if 'receipt_sha256' in node:
                for alias,h in node['receipt_sha256'].items():
                    if alias=='proposal_claim.json':p=node['prior_plan_path']+'.claimed.json'
                    elif alias=='first_file_verified.json':p=node['complete_inputs'][0]['path']+'.verified.json'
                    elif alias.endswith('.verified.json') or alias in ('fastp.log','fastp.json'):p=node['prior_root']+'/GSM8009878/'+alias
                    else:p=node['prior_root']+'/'+alias
                    assert sha(data[source[p]])==h,(p,'receipt binding');bindings.add(p)
            for alias,h in node.get('attempt_receipt_sha256',{}).items():
                p=node['prior_root']+'/transport-receipts/'+alias;assert sha(data[source[p]])==h;bindings.add(p)
            for v in node.values():embedded(v)
        elif isinstance(node,list):
            for v in node:embedded(v)
    for n in names:
        if not n.startswith('plans/') or not n.endswith('.json') or n.endswith('.claimed.json'):continue
        p=get(n);plans.append({'member':n,'sha256':sha(data[n]),'runtime_commit':p.get('repository_commit')});embedded(p.get('lineage',{}))
        if 'schema' in p:
            claim=get(n+'.claimed.json');assert claim=={'plan_sha256':sha(data[n]),'transfer_bytes':14000000000}
        for f,h in p.get('code_sha256',{}).items():
            b=subprocess.check_output(['git','show',p['repository_commit']+':'+f],cwd=ROOT);assert sha(b)==h,(n,f);code_checks+=1
    runs=[];previous=0
    for i in range(1,7):
        prefix=f'runs/{i:02d}/';sup=get(prefix+'supervision.json');ledger=get(prefix+'transfer-ledger.json')
        assert sup['cleanup_error'] is None;assert sup['status']==('completed' if i==6 else 'failed')
        plan_source=next(p for p in plans if p['sha256']==sup['plan_sha256']);assert plan_source
        req=[get(n) for n in names if n.startswith(prefix+'transport-receipts/')]
        if i==1:
            observed=sum(r['actual_bytes'] for r in ledger['requests']);assert observed==ledger['actual_body_bytes']==ledger['body_upper_bound_bytes']
        else:
            assert ledger['prior_charge_bytes']==previous
            ids={r['id']:r for r in req};assert len(ids)==len(req)
            byid={j:(r['observed_bytes'],r['charged_bytes']+r['inflight_max_bytes']) for j,r in ids.items()}
            for a in ledger['active_requests']:
                j=a['id'];v=byid.get(j,(0,0));byid[j]=(max(v[0],a['observed_bytes']),max(v[1],a['charged_bytes']+a['inflight_max_bytes']))
            assert set(byid)==set(range(1,ledger['request_attempts']+1))
            observed=sum(v[0] for v in byid.values());upper=sum(v[1] for v in byid.values())
            assert observed==ledger['new_observed_body_bytes']
            assert ledger['prior_charge_bytes']+upper==ledger['body_upper_bound_bytes']
            if not ledger['active_requests']:assert len(req)==ledger['completed_attempts']==ledger['request_attempts']
        previous=ledger['body_upper_bound_bytes'];assert previous<=14000000000
        runs.append({'run':i,'status':sup['status'],'failure':sup['failure'],'durable_requests':len(req),'durable_statuses':dict(Counter(r['status'] for r in req)),
                     'new_observed_bytes':observed,'conservative_lineage_bytes':previous})
    actual=get('runs/06/result.json');expected=json.loads((ROOT/'reports/gse252892-local-result-20261114/user-reported-result.json').read_text());assert actual==expected
    assert get('runs/06/supervision.json')==json.loads((ROOT/'reports/gse252892-local-result-20261114/user-reported-supervision.json').read_text())
    inputs=[]
    plan=get(next(p['member'] for p in plans if p['sha256']==manifest['source_plan_sha256']))
    assert sha(data[source[plan['base_path']]])==plan['base_sha256']
    for row in plan['base']['input_files']:
        n='runs/06/'+row['gsm']+'/'+Path(row['url']).name+'.verified.json';info=get(n)
        assert info['status']=='verified_complete' and info['bytes']==int(row['compressed_bytes']) and info['md5']==row['md5']
        inputs.append({'gsm':row['gsm'],'file':Path(row['url']).name,'bytes':info['bytes'],'recorded_md5':info['md5'],'recorded_sha256':info['sha256']})
    for lib in actual['libraries']:
        gsm=lib['gsm'];assert get('runs/06/'+gsm+'/junction-counts.json')==lib
        fastp=get('runs/06/'+gsm+'/fastp.json');assert fastp['filtering_result']['passed_filter_reads']==2*int(re.search(r'^(\d+) reads',data['runs/06/'+gsm+'/hisat2-summary.txt'].decode())[1])
        q=lib['qc'];assert q['eligible_groups']+q['rejected_groups']==q['alignment_groups']
    final=get('runs/06/transfer-ledger.json');assert final['active_requests']==[] and final['body_upper_bound_bytes']-final['actual_body_bytes']==1048576
    return {'status':'passed','zip_sha256':sha(raw),'zip_bytes':len(raw),'metadata_members':1463,'manifest_sha256':sha(data['MANIFEST.json']),
        'metadata_payload_bytes':1959447,'plan_count':len(plans),'runtime_code_hash_checks':code_checks,'distinct_embedded_file_bindings':len(bindings),
        'plans':plans,'runs':runs,'recorded_complete_inputs':inputs,'counts':{lib['gsm']:lib['counts'] for lib in actual['libraries']},
        'final_observed_bytes':final['actual_body_bytes'],'final_conservative_charge_bytes':final['body_upper_bound_bytes'],
        'uncertain_reservation_carried_bytes':1048576,'raw_inputs_replayed_or_rehashed':False,'external_independent_review':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive',type=Path);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    out=verify(a.archive);a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
