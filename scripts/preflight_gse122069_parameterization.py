#!/usr/bin/env python3
"""Synthetic SAM/configuration regression only; never opens a real FASTQ or runs HISAT2."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.gse122069_run_config import load_rows,configure,aligner_command,validate_receipt
from scripts.gse122069_full_control import Bins,count_text,concordance
from scripts.summarize_gse122069_full_control import summarize
from scripts.fetch_gse122069_ranges import download_plan


def read(path):return json.loads(Path(path).read_text())
def save(path,value):Path(path).write_text(json.dumps(value,indent=2)+'\n')


def main():
    os.chdir(ROOT)
    out=Path('reports/gse122069-parameterization-20261031')
    rows=load_rows('reports/gse122069-resource-plan/input_manifest.json')
    legacy=read('reports/gse122069-full-control-20261031/execution/full-control-results.json')
    pilot=read('reports/gse122069-pilot-20261031/pilot_results.json')
    pilot_cmd=read('reports/gse122069-pilot-20261031/pilot_command.json')['command']
    full_cmd=legacy['command']
    assert aligner_command(pilot_cmd[3],pilot_cmd[pilot_cmd.index('-x')+1],1000000)==pilot_cmd
    assert aligner_command(full_cmd[3],full_cmd[full_cmd.index('-x')+1],37518164)==full_cmd
    base=Path('reports/gse122069-full-control-20261031')
    summary=summarize(legacy,read(base/'execution/text-checkpoint.json'),read(base/'execution/htslib-checkpoint.json'),pilot)
    assert summary==read(base/'summary.json')
    old_receipt=read(base/'fastq-download.json')
    validate_receipt(configure(rows),old_receipt)
    old_download_plan=download_plan({'rows':rows})
    for key in ('run','gsm','url','expected_bytes','expected_md5'):
        assert old_download_plan[key]==old_receipt[key]
    next_download_plan=download_plan({'rows':rows},'SRR8144908')
    assert next_download_plan['verified'] is False and next_download_plan['etag_verification_pending']
    cfg2=configure(rows,'SRR8144908',54292655,True,1000000,2700)
    negatives=[]
    for label,call in [('crossed_download_receipt',lambda:validate_receipt(cfg2,old_receipt)),
                       ('wrong_complete_count',lambda:configure(rows,'SRR8144908',37518164,True)),
                       ('unknown_accession',lambda:configure(rows,'SRR9999999')),
                       ('deadline_over_cap',lambda:configure(rows,deadline=2701)),
                       ('crossed_summary',lambda:summarize(legacy,{}, {},run='SRR8144908'))]:
        try:call()
        except ValueError as exc:negatives.append({'control':label,'rejected':True,'error':'ValueError: '+str(exc)})
        else:raise AssertionError('Expected rejection not observed: '+label)
    save(out/'negative-controls.json',negatives)
    all_matrices=[];measurements=[]
    affinity=sorted(os.sched_getaffinity(0))[:2];os.sched_setaffinity(0,affinity)
    for repeat in (1,2):
        matrix=[]
        for config_run in ('SRR8144907','SRR8144908'):
            for fixture in ('genome','mini'):
                path=Path('reports/hisat2-synthetic-gate-20261031')/(fixture+'.sam')
                lines=path.read_text().splitlines(True)
                expected=sum(not x.startswith('@') and not int(x.split('\t')[1])&(256|2048) for x in lines)
                config=configure(rows,config_run,expected,False,7,1800)
                bins=Bins(config['bin_size'],config['max_reads']);count_text(lines,bins);own=bins.finish()
                target=out/f'htslib-{config_run}-{fixture}-repeat{repeat}.json'
                cmd=['prlimit','--as=268435456','--',str(ROOT/'data/tools/venv/bin/python'),str(ROOT/'scripts/gse122069_full_control.py'),'htslib','--out',str(target),'--max-reads',str(expected),'--bin-size','7']
                with path.open() as stream:
                    proc=subprocess.run(cmd,stdin=stream,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=60,check=True)
                other=read(target);concordance(own,other)
                measurements.append({'repeat':repeat,'configuration_run':config_run,'fixture':fixture,'worker_maxrss_kib':other['self_maxrss_kib'],'stderr':proc.stderr,'worker_command':cmd})
                # Raw worker receipt may vary in memory measurement; stable scientific
                # projection below is compared independently of resource measurements.
                matrix.append({'input_kind':'historical synthetic SAM, not public SRR reads','configuration_run_not_observed_sample':config_run,
                               'fixture':str(path),'fixture_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                               'queries':expected,'sam_records':own['sam_records'],'bin_reads':[b['reads'] for b in own['completed_bins']],
                               'counts':own['counts'],'locus_bins':other['locus_bins'],'parsers_concordant':True,
                               'pysam':other['pysam'],'htslib':other['htslib']})
        save(out/f'synthetic-matrix-repeat{repeat}.json',matrix);all_matrices.append(matrix)
    assert all_matrices[0]==all_matrices[1]
    assert (out/'synthetic-matrix-repeat1.json').read_bytes()==(out/'synthetic-matrix-repeat2.json').read_bytes()
    save(out/'measurements.json',measurements)
    save(out/'preflight.json',{'python':platform.python_version(),'cpu_affinity':affinity,
         'default_one_million_argv_equal_historical':True,'default_full_control_argv_equal_historical':True,
         'historical_summary_all_fields_equal':True,'historical_receipt_metadata_still_valid':True,
         'historical_download_identity_fields_equal':True,'next_download_plan_not_a_verified_receipt':True,
         'two_configuration_contexts_two_fixtures_each':True,'unique_synthetic_queries_in_reused_fixtures':28,
         'two_replays_byte_identical_stable_projection':True,'negative_controls_rejected':len(negatives),
         'next_control_full_partition':cfg2['bin_reads'],'new_real_fastq_reads_processed':0,'new_hisat2_alignments_executed':0,
         'not_biological_replicates_or_new_mapping_sensitivity_calibration':True,
         'future_real_download_and_resource_review_still_required':True})
    print('Synthetic matrix concordant, repeats byte-identical; historical argv/summary unchanged; five negative controls rejected.')

if __name__=='__main__':main()
