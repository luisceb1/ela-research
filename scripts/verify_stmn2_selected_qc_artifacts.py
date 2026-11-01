#!/usr/bin/env python3
"""Replay exporters on saved aggregate JSON and reject controlled corrupted copies."""
import copy
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.summarize_stmn2_selected_replay import validate
from scripts.write_stmn2_selected_qc_report import write_report
from scripts.gse122069_full_control import save


def verify(root):
    root=Path(root);e=root/'execution'
    inputs=[json.loads((e/name).read_bytes()) for name in ['replay-results.json','full-control-results.json','htslib-checkpoint.json','fastq_qc.json']]
    validate(*inputs)
    projections=[]
    names=['summary.json','target-qc-histograms.tsv','REPORT.md']
    for _ in range(2):
        write_report(root);projections.append({name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in names})
    if projections[0]!=projections[1]:raise ValueError('Repeated aggregate exports differ')
    errors={}
    for case in ['false_source_completion','source_hash_changed','source_crc_missing','expected_counts_changed','histogram_incomplete','independent_histograms_disagree']:
        r,a,b,f=copy.deepcopy(inputs)
        if case=='false_source_completion':a['complete_library']=True
        elif case=='source_hash_changed':a['fastq_sha256']='0'*64
        elif case=='source_crc_missing':f['gzip_eof_crc_validated']=False
        elif case=='expected_counts_changed':
            a['counts']['15']['cryptic']+=1;b['counts']['15']['cryptic']+=1
        elif case=='histogram_incomplete':r['target_qc_histograms']['15']['cryptic']['histograms']['NM'].clear()
        else:b['target_qc_histograms']['15']['cryptic']['histograms']['MAPQ']={'0':3}
        try:validate(r,a,b,f)
        except ValueError as exc:errors[case]=str(exc)
        else:raise ValueError('Corrupted copy was accepted: '+case)
    result={'status':'passed','aggregate_export_repeated_byte_identical':True,'exports_sha256':projections[0],
            'controlled_corrupted_copies_rejected':errors,'original_execution_artifacts_not_mutated':True,
            'additional_fastq_alignment_or_biological_replicates':0}
    save(root/'artifact-verification.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':verify(sys.argv[1])
