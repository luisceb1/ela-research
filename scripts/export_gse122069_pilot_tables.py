#!/usr/bin/env python3
"""Export only completed pilot aggregates, with canonical LF line endings."""
import argparse
import csv
import json
from pathlib import Path


def export(pilot_dir,diagnostic_dir):
    p=json.loads((pilot_dir/'pilot_results.json').read_text())
    d=json.loads((diagnostic_dir/'pilot_results.json').read_text())
    if not p['complete'] or not d['complete'] or p['counts']!=d['counts']:
        raise ValueError('Require completed concordant technical passes')
    with (pilot_dir/'target_support.tsv').open('w',newline='') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n')
        w.writerow(['run','GSM','subset_reads','min_anchor','event','support_count','denominator_ge20','interpretation'])
        for a in (15,8):
            adequate=p['counts'][str(a)]['canonical']+p['counts'][str(a)]['cryptic']>=20
            for event in ('canonical','cryptic'):
                w.writerow([p['run'],p['gsm'],p['sam_qc']['primary_records'],a,event,p['counts'][str(a)][event],adequate,
                            'fixed technical subset; not molecular absence or biological inference'])
    loc=d['locus_qc']['block_overlap_counts']
    with (diagnostic_dir/'locus_summary.tsv').open('w',newline='') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['metric','count','scope'])
        for key in ('primary_block_overlap','unique_mapq_block_overlap','exon1_unique_overlap','exon2_unique_overlap','unique_spliced_reads'):
            # Counters enumerate all qualifying alignments in a completed pass;
            # absent counter keys are observed zero, not missing sample data.
            w.writerow([key,loc.get(key,0),'same first1M, no read IDs'])


if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__);p.add_argument('--pilot-dir',required=True);p.add_argument('--diagnostic-dir',required=True);a=p.parse_args()
    export(Path(a.pilot_dir),Path(a.diagnostic_dir))
