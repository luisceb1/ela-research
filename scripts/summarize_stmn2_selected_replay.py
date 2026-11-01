#!/usr/bin/env python3
"""Validate persisted selected-replay artifacts and export aggregate QC, never read IDs."""
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.replay_stmn2_control2_qc import EXPECTED,SOURCE_READS,SELECTED_READS,SHA256
from scripts.stmn2_target_alignment_qc import validate_histograms
from scripts.gse122069_full_control import concordance,save
ORIGINAL_SHA='cb26604160e43cdc04d2eab0a2525fc02f296059d70f5e0d9d731a32d9f6b4a7'


def validate(replay,own,other,fq):
    if not replay.get('replay_complete') or replay.get('complete_source_library_realigned') is not False:
        raise ValueError('Selected replay not complete in its correct scope')
    if own.get('complete_library') is not False or other.get('complete_library') is not False or not other.get('complete_query_stream'):
        raise ValueError('Selected stream mislabelled as source library')
    concordance(own,other)
    if own.get('fastq_sha256')!=SHA256:raise ValueError('Source hash changed')
    if fq.get('reads')!=SELECTED_READS or fq.get('source_reads_scanned')!=SOURCE_READS or not fq.get('gzip_eof_crc_validated'):
        raise ValueError('Source/selected stream incomplete')
    if own['reads']!=SELECTED_READS or own.get('error') or own.get('watchdog_errors'):
        raise ValueError('Execution error/incomplete reads')
    for anchor,counts in EXPECTED.items():
        for name,value in counts.items():
            if own['counts'][anchor][name]!=value:raise ValueError('Expected counts not reproduced')
    qc=replay['target_qc_histograms'];validate_histograms(qc,own['counts'])
    if qc!=other['target_qc_histograms']:raise ValueError('Independent QC mismatch')
    return qc


def render_histograms(qc):
    stream=io.StringIO(newline='');writer=csv.writer(stream,delimiter='\t',lineterminator='\n')
    writer.writerow(['anchor','target','metric','value_or_missing','alignment_observations'])
    for anchor in ('15','8'):
        for target in ('canonical','cryptic'):
            for metric,hist in sorted(qc[anchor][target]['histograms'].items()):
                for value,count in sorted(hist.items()):writer.writerow([anchor,target,metric,value,count])
    return stream.getvalue().encode()


def summarize(root):
    root=Path(root);e=root/'execution'
    read=lambda p:json.loads(p.read_bytes())
    replay=read(e/'replay-results.json');own=read(e/'full-control-results.json');other=read(e/'htslib-checkpoint.json');fq=read(e/'fastq_qc.json')
    qc=validate(replay,own,other,fq)
    original=ROOT/'reports/gse122069-next-control-20261031/execution/full-control-results.json'
    if hashlib.sha256(original.read_bytes()).hexdigest()!=ORIGINAL_SHA:raise ValueError('Original full-library result changed')
    tsv=render_histograms(qc);(root/'target-qc-histograms.tsv').write_bytes(tsv)
    summary={'status':'selected_technical_replay_complete','source_run':'SRR8144908','source_library_reads':SOURCE_READS,
      'selected_reads_realigned':SELECTED_READS,'target_counts':EXPECTED,'histogram_parsers_concordant':True,
      'original_full_library_result_unchanged':True,'original_full_library_result_sha256':ORIGINAL_SHA,
      'full_library_counts_not_replaced':{'15':{'canonical':111,'cryptic':3},'8':{'canonical':154,'cryptic':4}},
      'gzip_eof_crc_validated':True,'elapsed_seconds_including_identity_checks':replay['elapsed_seconds'],
      'biological_replicates_added':0,'not_assessed':['rates','effect','molecular fraction','clinical implication','functional validation'],
      'selected_subset_minimum_denominator_not_applied':True,
      'generic_engine_coverage_boolean_scope':'Selected stream only; denominator16<20 does not reverse whole-source denominator114>=20. No subset coverage criterion used.',
      'histograms_sha256':hashlib.sha256(tsv).hexdigest()}
    save(root/'summary.json',summary);return summary


if __name__=='__main__':print(json.dumps(summarize(sys.argv[1]),indent=2))
