"""Offline original-metadata audit; no raw-data replay or network access."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
SHA = '7398e02f2bb43900c918d2e43ecd49dd52ea5fa5c534326a08b0d696dbe8e7d8'
PLAN = 'ela-stmn2-restantes-plan-20261115.json'
PLAN_SHA = '0c6e43df6f2b1d5c8474d27c61701e8a487533567e15ac92ae581b93b9ee6462'
RUNTIME = '4fb71a9b3bdd146d44c5dc8dd0e5197d36ed47cb'
GSMS = ['GSM8009879','GSM8009880','GSM8009882','GSM8009883']


def sha(b):
    return hashlib.sha256(b).hexdigest()


def verify(path):
    archive = Path(path).read_bytes()
    assert sha(archive) == SHA
    with tarfile.open(path, 'r:gz') as t:
        ms=t.getmembers()
        assert len({m.name for m in ms}) == len(ms)
        assert all(m.isfile() or (m.isdir() and m.name=='transport-receipts') for m in ms)
        assert all(not Path(m.name).is_absolute() and '..' not in Path(m.name).parts and m.size<2_000_000 for m in ms)
        assert sum(m.size for m in ms) < 10_000_000
        data={m.name:t.extractfile(m).read() for m in ms if m.isfile()}
    j=lambda n:json.loads(data[n])
    plan,result,sup,ledger=j(PLAN),j('result.json'),j('supervision.json'),j('transfer-ledger.json')
    assert sha(data[PLAN]) == PLAN_SHA and plan['repository_commit']==RUNTIME
    for n in [PLAN+'.claimed.json','accepted.json','supervision.json']:
        assert j(n)['plan_sha256']==PLAN_SHA and j(n)['transfer_bytes']==40_000_000_000
    for n,actual in [('result',result),('supervision',sup),('transfer-ledger',ledger)]:
        expected=json.loads((ROOT/f'reports/stmn2-remaining-result-20261116/user-reported-{n}.json').read_bytes())
        assert actual==expected,n
    assert result['status']==sup['status']=='completed'
    assert sup['failure'] is None and sup['cleanup_error'] is None
    assert j('worker.log')=={'status':'worker_finished'}
    assert sup['caps']==plan['caps']
    for measured,cap in [('elapsed_seconds','wall_seconds'),('peak_sampled_group_rss_bytes','group_rss_bytes'),('peak_sampled_combined_root_bytes','root_bytes')]:
        assert 0<=sup[measured]<plan['caps'][cap]
    for p,h in plan['code_sha256'].items():
        assert sha(subprocess.check_output(['git','show',RUNTIME+':'+p],cwd=ROOT))==h,p
    source=(ROOT/'reports/gse252892-stmn2-result-20261115/original/ela-gse252892-stmn2-control-20261114.json').read_bytes()
    assert sha(source)=='8379c7e56c0546623fac80c732935f29113f17e048b8625d85e1163e3f61b557'
    source=json.loads(source)
    assert source['source']==plan['source']
    assert plan['prior_roots']==source['source_record']['prior_roots']+[source['run_root']]
    import sys
    sys.path.insert(0,str(ROOT/'scripts'))
    import run_stmn2_remaining as runner
    assert plan['inputs']==runner.inputs() and plan['caps']==runner.CAPS
    assert plan['history']==runner.HISTORY and result['historical_transfer']==runner.HISTORY
    assert plan['transport']==runner.ranged.RECOVERY_SETTINGS
    assert plan['commands']=={g:runner.commands(plan,g) for g in GSMS}
    assert [x['gsm'] for x in result['libraries']]==GSMS
    for lib in result['libraries']:
        g=lib['gsm'];q=lib['qc'];assert lib==j(g+'/stmn2-counts.json')
        assert q['eligible_groups']+q['rejected_groups']==q['alignment_groups']
        assert 2*q['eligible_groups']+4*q['rejected_groups']==q['sam_records']
        assert lib['positive_control_measured']==(lib['counts']['canonical']>0)
        assert lib['support_at_least_20_groups']['cryptic']==(lib['counts']['cryptic']>=20)
        summary=data[g+'/hisat2-summary.txt'].decode()
        assert data[g+'/hisat2.log']==data[g+'/hisat2-summary.txt']
        pairs=int(re.search(r'^(\d+) reads;',summary)[1])
        unique=int(re.search(r'^\s*(\d+) .*aligned concordantly exactly 1 time',summary,re.M)[1])
        multi=int(re.search(r'^\s*(\d+) .*aligned concordantly >1 times',summary,re.M)[1])
        zero=int(re.search(r'^\s*(\d+) .*aligned concordantly 0 times',summary,re.M)[1])
        assert unique==q['eligible_groups'] and multi==q['rejected_groups'] and unique+multi+zero==pairs
        fastp=j(g+'/fastp.json')
        assert fastp['summary']['fastp_version']=='0.23.4'
        assert fastp['summary']['after_filtering']['total_reads']==2*pairs
        assert fastp['command'].split()==plan['commands'][g]['fastp']
        assert ' '.join(plan['commands'][g]['fastp']) in data[g+'/fastp.log'].decode()
    receipts=sorted([j(n) for n in data if n.startswith('transport-receipts/')],key=lambda r:r['id'])
    assert [r['id'] for r in receipts]==list(range(1,3370))
    assert ledger['active_requests']==[] and ledger['request_attempts']==ledger['completed_attempts']==len(receipts)
    assert ledger['prior_charge_bytes']==ledger['prior_observed_body_bytes']==0
    observed=sum(r['observed_bytes'] for r in receipts)
    charged=sum(r['charged_bytes'] for r in receipts)
    assert observed==ledger['actual_body_bytes']==ledger['new_observed_body_bytes']
    assert charged==ledger['new_charged_upper_bytes']==ledger['body_upper_bound_bytes']
    assert charged<=ledger['cap_bytes']==plan['caps']['transfer_bytes']
    wanted={r['url']:r for r in plan['inputs']}
    assert {r['url'] for r in receipts}==set(wanted)
    for r in receipts:
        assert r['total']==int(wanted[r['url']]['compressed_bytes'])
        assert r['status'] in ('complete','failed') and r['inflight_max_bytes']==0
        assert 1<=r['attempt']<=5 and 0<=r['start']<=r['end']<r['total']
        assert r['charged_bytes']==r['observed_bytes']+r['uncertain_bytes']
    expected={PLAN,PLAN+'.claimed.json','accepted.json','result.json','supervision.json','transfer-ledger.json','worker.log'}
    for g in GSMS:
        expected.update(g+'/'+n for n in ['stmn2-counts.json','fastp.json','fastp.log','hisat2.log','hisat2-summary.txt'])
    input_records=[]
    for url,row in wanted.items():
        name=row['gsm']+'/'+Path(url).name+'.verified.json';expected.add(name);v=j(name)
        assert v['status']=='verified_complete' and v['bytes']==int(row['compressed_bytes']) and v['md5']==row['md5']
        assert re.fullmatch('[0-9a-f]{64}',v['sha256'])
        assert v['reused_complete_block_bytes']==v['reused_prefix_bytes']==v['remote_overlap_bytes']==0
        complete=sorted([r for r in receipts if r['url']==url and r['status']=='complete'],key=lambda r:r['start'])
        offset=0
        for r in complete:
            assert r['start']==offset and r['observed_bytes']==r['end']-r['start']+1
            assert re.fullmatch('[0-9a-f]{64}',r['sha256']);offset=r['end']+1
        assert offset==v['bytes'] and len(complete)==v['range_blocks']
        input_records.append({'gsm':row['gsm'],'file':Path(url).name,'bytes':v['bytes'],'md5':v['md5'],'recorded_sha256':v['sha256']})
    assert set(data)==expected|{f'transport-receipts/{r["id"]:06d}.json' for r in receipts}
    failed=[r for r in receipts if r['status']=='failed']
    extra=sum(r['observed_bytes'] for r in failed)
    assert observed-sum(int(r['compressed_bytes']) for r in plan['inputs'])==extra
    last=receipts[-1]
    assert ledger['last_completed']=={k:last[k] for k in ['id','status','observed_bytes','charged_bytes']}
    return {'status':'passed','archive_sha256':SHA,'archive_bytes':len(archive),'metadata_files':len(data),
            'metadata_bytes':sum(map(len,data.values())),'plan_sha256':PLAN_SHA,'runtime_commit':RUNTIME,
            'runtime_hashes_checked':len(plan['code_sha256']),'request_receipts':len(receipts),
            'receipt_statuses':dict(Counter(r['status'] for r in receipts)),
            'failed_error_counts':dict(Counter(r['error'] for r in failed)),
            'new_observed_bytes':observed,'new_charged_bytes':charged,'failed_attempt_observed_bytes':extra,
            'new_uncertain_bytes':charged-observed,'recorded_inputs':input_records,
            'prediction_met':all(x['positive_control_measured'] and x['support_at_least_20_groups']['cryptic'] for x in result['libraries'][2:]),
            'limitations':['Metadata/provenance coherence only; raw FASTQ/index/binaries were not rehashed/replayed by agent.',
                           'Recorded resource/network evidence is not independent host telemetry or biological validation.'],
            'members':{n:{'bytes':len(b),'sha256':sha(b)} for n,b in sorted(data.items())}}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archive',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=verify(a.archive);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('members','recorded_inputs')},indent=2))
