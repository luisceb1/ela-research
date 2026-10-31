#!/usr/bin/env python3
"""Resource extrapolation from one observed full control, never an execution result."""
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def project(rows,observed):
    if not observed.get('complete_library') or observed['reads']!=37518164 or observed['run']!='SRR8144907':
        raise ValueError('Require the verified fixed complete-control benchmark')
    if observed.get('watchdog_errors') or not observed.get('independent_parser_concordant'):
        raise ValueError('Benchmark QC did not pass')
    remaining=[r for r in rows if r['run']!=observed['run']]
    if len(remaining)!=5:raise ValueError('Expected only the other five fixed runs')
    return [{'run':r['run'],'gsm':r['gsm'],'published_group':r['published_group'],'expected_reads':r['reads'],
             'compressed_bytes':r['fastq_bytes'],
             'linear_point_estimate_seconds_not_measured':round(observed['elapsed_seconds']*r['reads']/observed['reads'],2),
             'new_run_executed':False} for r in remaining]

if __name__=='__main__':
    out=ROOT/'reports/gse122069-design-20261031'
    manifest=ROOT/'reports/gse122069-resource-plan/input_manifest.json'
    observed=ROOT/'reports/gse122069-full-control-20261031/execution/full-control-results.json'
    rows=json.loads(manifest.read_text())['rows'];benchmark=json.loads(observed.read_text());estimates=project(rows,benchmark)
    result={'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (manifest,observed)},
            'benchmark_run':benchmark['run'],'observed_seconds':benchmark['elapsed_seconds'],
            'linear_scaling_is_unvalidated_not_a_guarantee':True,'other_runs':estimates,
            'remaining_reads':sum(r['expected_reads'] for r in estimates),'remaining_compressed_bytes':sum(r['compressed_bytes'] for r in estimates),
            'proposed_next_fixed_run':'SRR8144908','proposed_future_phase_deadline_seconds':2700,
            'future_phase_not_started':True,'no_automatic_budget_extension':True,
            'next_authorized_preparation':'parameterize runner and validate synthetic boundary/control tests only; no new FASTQ'}
    (out/'remaining-resource-proposal.json').write_text(json.dumps(result,indent=2)+'\n')
    with (out/'remaining-resource-estimates.tsv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(estimates[0]),delimiter='\t',lineterminator='\n');writer.writeheader();writer.writerows(estimates)
    print(json.dumps(result,indent=2))
