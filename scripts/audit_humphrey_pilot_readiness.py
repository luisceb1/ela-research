"""Read-only source/environment audit and offline interface probes; no data CLI."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

import bounded_http_transport as transport
from external_local_stage import validate_stage
from pilot_dry_runner import DryRunner

REPORT='reports/pilot-readiness-audit-20261102'


def sha256(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def probes():
    findings={}
    with tempfile.TemporaryDirectory() as folder:
        limits={'wall_seconds':30,'transfer_bytes':100,'disk_bytes':2*1024**2,'reserve_bytes':0}
        runner=DryRunner(folder,{'fixture':'audit-only'},limits)
        try:
            try:runner.process('disabled',['never-executed'],production=True)
            except ValueError as exc:findings['production_process']={'rejected':True,'reason':str(exc),'phase_created':bool(runner.state['phases'])}
            try:validate_stage({'kind':'http','name':'index','url':'https://genome-idx.s3.amazonaws.com/hisat/hg38_genome.tar.gz','expected':{},'chunk_size':65536})
            except ValueError as exc:findings['external_http_worker']={'rejected':True,'reason':str(exc)}
            data=b'abc'
            class Response:
                status=200;headers={'Content-Length':'3'}
                def __init__(self):self.body=io.BytesIO(data)
                def __enter__(self):return self
                def __exit__(self,*args):pass
                def read1(self,n):return self.body.read(n)
            class Opener:
                def open(self,*args,**kw):return Response()
            try:
                with patch.object(transport.urllib.request,'build_opener',return_value=Opener()):
                    transport.transfer_http(runner,'sha_only','http://127.0.0.1/fixture',{'bytes':3,'sha256':hashlib.sha256(data).hexdigest()},['http://127.0.0.1'],reserve_reads=True)
            except KeyError as exc:
                findings['sha_only_transfer']={'rejected':True,'exception':'KeyError','missing_key':str(exc),'synthetic_bytes_charged':runner.state['transfer_bytes_consumed'],'phase_status':runner.state['phases']['sha_only']['status']}
        finally:runner.close()
    if set(findings)!={'production_process','external_http_worker','sha_only_transfer'}:raise ValueError('Baseline interface behavior changed; review audit')
    findings['network_used']=False;findings['alignments_executed']=False
    return findings


def audit(repo):
    repo=Path(repo);report=repo/REPORT
    manifest=json.loads((report/'source-manifest.json').read_text())
    inputs=[]
    for entry in manifest['inputs']:
        data=(repo/entry['path']).read_bytes()
        git_sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\x00'+data).hexdigest()
        if git_sha!=entry['git_blob_sha']:raise ValueError('Source changed: '+entry['path'])
        inputs.append({**entry,'sha256':hashlib.sha256(data).hexdigest()})
    plan=json.loads((repo/'reports/gse296714-raw-pilot-plan-20261101/PLAN.json').read_text())
    index=json.loads((repo/'reports/hisat2-index-inspection-20261031/verified_index.json').read_text())
    pre=json.loads((repo/'reports/bounded-http-local-20261102/preflight.json').read_text())
    extraction=json.loads((repo/'reports/hisat2-index-inspection-20261031/extraction.json').read_text())
    mini=json.loads((repo/'reports/unc13a-minigenome-20261102/result.json').read_text())
    env=json.loads((report/'environment.json').read_text())
    pe=json.loads((repo/'reports/pe-synthetic-contract-20261102/validation.json').read_text())
    paired=json.loads((repo/'reports/paired-fastq-ledger-20261102/validation.json').read_text())
    local=json.loads((repo/'reports/paired-fastq-local-20261102/executed-final/summary.json').read_text())
    supervised=json.loads((repo/'reports/external-local-supervision-20261102/validation.json').read_text())
    samples_path=repo/'reports/gse296714-design-20261101/samples.tsv'
    ena_path=repo/'reports/gse296714-raw-pilot-plan-20261101/ena-metadata.tsv'
    with samples_path.open() as f:samples=list(csv.DictReader(f,delimiter='\t'))
    with ena_path.open() as f:ena={r['run_accession']:r for r in csv.DictReader(f,delimiter='\t')}
    selection_verified=True
    for lib in plan['selected']:
        selected=min((s for s in samples if s['group']==lib['group']),key=lambda s:(int(s['fastq_bytes_ena']),s['run']))
        row=ena[lib['run']]
        expected_mates=[{'url':'https://'+u,'bytes':int(n),'md5':h} for u,n,h in zip(row['fastq_ftp'].split(';'),row['fastq_bytes'].split(';'),row['fastq_md5'].split(';'))]
        selection_verified &= all(selected[k]==lib[k] for k in ('library','gsm','srx','biosample','run')) and row['sample_alias']==lib['library'] and row['experiment_accession']==lib['srx'] and row['sample_accession']==lib['biosample'] and row['library_layout']=='PAIRED' and expected_mates==lib['mates']
    raw=sum(m['bytes'] for lib in plan['selected'] for m in lib['mates'])
    extracted=sum(f['bytes'] for f in index['verified_files'])
    checks={'two_libraries_four_mates':len(plan['selected'])==2 and all(len(v['mates'])==2 for v in plan['selected']),
            'library_totals_consistent':all(sum(m['bytes'] for m in lib['mates'])==lib['fastq_bytes'] for lib in plan['selected']),
            'raw_total_consistent':raw==plan['selected_fastq_bytes']==6349703881,
            'archive_hash_consistent':index['archive_sha256']==extraction['archive_sha256']==pre['reference']['sha256'],
            'archive_size_consistent':index['size_bytes']==pre['reference']['bytes'],
            'extraction_size_consistent':extracted==extraction['extracted_bytes'],
            'eight_index_members':len([f for f in index['verified_files'] if f['name'].endswith('.ht2')])==8,
            'preflight_transfer_total_consistent':raw+index['size_bytes']==pre['minimum_entity_body_bytes'],
            'limits_consistent':plan['limits']==pre['limits'],
            'miniature_function_pass':mini['passed'],
            'miniature_references_pass':all(v['pass'] and v['text_equals_htslib'] for v in mini['references'].values()),
            'pe_receipt_pass':pe['tests_passed']==17 and pe['parser_comparisons']==22,
            'paired_ledger_receipt_pass':paired['success'] and paired['failures']==0 and paired['errors']==0,
            'full_fastq_fixture_receipt_pass':local['full_scan_eof_crc_validated'] and local['crc_corruption_after_prefix_rejected'],
            'external_supervision_receipt_pass':supervised['success'] and supervised['failures']==0 and supervised['errors']==0,
            'sample_table_sha_matches_plan':sha256(samples_path)==plan['samples_sha256'],
            'ena_snapshot_sha_matches_plan':sha256(ena_path)==plan['ena_metadata_sha256'],
            'selection_minimum_and_identity_verified':bool(selection_verified),
            'all12_size_matches_plan':len(samples)==12 and sum(int(s['fastq_bytes_ena']) for s in samples)==plan['all12_fastq_bytes']}
    if not all(checks.values()):raise ValueError('Metadata inconsistency: '+str(checks))
    limits=plan['limits'];body=raw+index['size_bytes'];margin=limits['raw_plus_reference_transfer_bytes']-body
    baseline_disk=raw+index['size_bytes']+extracted
    budget={'units':'bytes unless stated; GB=10^9, GiB=2^30','raw_four_mates':raw,'reference_archive':index['size_bytes'],'reference_extracted_including_recipe':extracted,
            'minimum_transfer':body,'transfer_cap':limits['raw_plus_reference_transfer_bytes'],'transfer_margin_before_dependencies_retries':margin,
            'all_artifacts_coexisting_disk_baseline':baseline_disk,'additional_disk_cap':limits['additional_disk_bytes'],'disk_margin_before_prefixes_temporaries_outputs':limits['additional_disk_bytes']-baseline_disk,
            'reserve_disk':limits['reserve_free_disk_bytes'],'free_disk_observed':env['disk']['free'],'nominal_additional_plus_reserve_fits':env['disk']['free']>=limits['additional_disk_bytes']+limits['reserve_free_disk_bytes'],
            'memory_limit_proposed':limits['memory_bytes'],'cgroup_memory_max_observed':int(env['memory_max']),'nominal_memory_limit_below_cgroup':limits['memory_bytes']<int(env['memory_max']),
            'minimum_body_rate_for_3600s_bytes_per_second':body/limits['all_transfer_elapsed_seconds'],'rate_is_requirement_not_measurement':True,
            'full_single_artifact_retry_fits_after_all_base_downloads':[{'artifact':lib['run']+f'_R{i}','bytes':m['bytes'],'fits':m['bytes']<=margin} for lib in plan['selected'] for i,m in enumerate(lib['mates'],1)]+[{'artifact':'hg38_index_archive','bytes':index['size_bytes'],'fits':index['size_bytes']<=margin}]}
    review=json.loads((report/'gate-review.json').read_text())
    proposal={'status':'BLOCKED_NOT_EXECUTABLE','execution_enabled':False,'raw_execution_ready':False,'source_commit':manifest['source_commit'],'scope':'two-library technical feasibility only; not biological comparison',
              'selected':plan['selected'],'prefix_pairs_per_library':limits['prefix_pairs_per_library'],'target_contract':'reports/unc13a-reference-strand-20261102/contract.json',
              'reference':{'url':index['pinned_url'],'expected_bytes':index['size_bytes'],'sha256':index['archive_sha256'],'md5_expected':None,'members':index['verified_files']},
              'resource_limits_from_original_plan':limits,
              'proposed_new_total_wall_seconds':9000,'new_total_wall_requires_review':True,
              'proposed_phase_caps_seconds':{'preflight':120,'all_transfers_cumulative':3600,'index_extract_verify':600,'paired_integrity_prefix_per_library':900,'align_per_library':900,'collate_count_per_library':300},
              'phase_cap_sum_two_libraries':8520,'all_phase_caps_are_stop_limits_not_runtime_estimates':True,
              'prospective_alignment_argv_template':['<verified_hisat2-align-s>','-x','<verified_hg38_prefix>','-1','<verified_prefix_R1>','-2','<verified_prefix_R2>','-S','<supervised_stream_not_full_SAM_file>','--no-mixed','--no-discordant','--fr','-p','2','--seed','0'],
              'omit_options':['--rna-strandness','--tmo'],'argv_is_design_only_not_launchable':True,
              'parser_policy':{'unit':'fragment/event/library','primary_anchor':15,'sensitivity_anchor':8,'mapq':'20 <= MAPQ < 255','NH':1,'required_XS':'-','marked_duplicates':'count and label, no molecular deduplication','independence':'CIGAR decoding only; shared pair selection/reduction'},
              'coverage_threshold_per_library':20,'coverage_threshold_definition':'valid canonical + either cryptic-junction fragment support; event supports may overlap within a fragment; report separately and do not label this sum unique molecules',
              'stop_on':['any blocking gate','hash/identity/schema mismatch','resource/deadline violation','incomplete receipt','decoder disagreement','coverage below threshold: insufficient, do not expand automatically'],
              'receipt_requirements':['transfer ledger with durable pending-read reservation','per-attempt HTTP receipt','archive and all eight index members verified','full EOF/CRC paired result and prefix hashes','argv/version/hash and supervisor receipt per stage','decoder QC/count agreement and final artifact manifest'],
              'prohibited_interpretations':['PSI or biological group effect','p-values or biological pairing','functional rescue or clinical benefit'],
              'blocking_gate_ids':[g['id'] for g in review if g['status']=='blocked']}
    result={'source_commit':manifest['source_commit'],'status':'BLOCKED','raw_execution_ready':False,'consistency_checks':checks,'source_inputs':inputs,'budget':budget,'offline_interface_probes':probes(),
            'blocked_gate_count':len(proposal['blocking_gate_ids']),'next_task':'checksum schema accepting SHA256-only plus bounded archive extraction receipt, tested only with synthetic archive; no remote restore'}
    for name,obj in [('audit.json',result),('execution-proposal.json',proposal)]:
        (report/name).write_text(json.dumps(obj,indent=2)+'\n')
    with (report/'gates.tsv').open('w') as out:
        out.write('id\tstatus\tgate\tevidence\tclosure\n')
        for g in review:out.write('\t'.join([g['id'],g['status'],g['gate'],'; '.join(g['evidence']),g['closure']])+'\n')
    return {'status':result['status'],'blocking_gate_count':result['blocked_gate_count'],'checks_passed':len(checks),'budget':budget,'probes':result['offline_interface_probes']}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);args=p.parse_args();print(json.dumps(audit(args.repo_root),indent=2))
