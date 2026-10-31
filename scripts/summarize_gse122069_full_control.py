#!/usr/bin/env python3
"""Validate and export only aggregate ordered-bin QC of a fixed manifest culture."""
import csv
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.gse122069_full_control import concordance, save
from scripts.gse122069_run_config import DEFAULT_RUN, load_rows, configure, partition


def summarize(result, text, hts, pilot=None, *, run=DEFAULT_RUN, expected_reads=37518164, bin_size=1000000):
    if result.get('run', DEFAULT_RUN)!=run:
        raise ValueError('Summary run does not match selected culture')
    if run!=DEFAULT_RUN and pilot:
        raise ValueError('Historical pilot belongs only to the first control')
    common=min(len(text['completed_bins']),len(hts['completed_bins']))
    left,right=text['completed_bins'][:common],hts['completed_bins'][:common]
    if left!=right:raise ValueError('Completed prefix parser mismatch')
    complete=result.get('complete_library',False)
    if complete:
        concordance(text,hts)
        if result.get('run')!=run or not hts['complete_library'] or text['reads']!=expected_reads or result['reads']!=expected_reads:
            raise ValueError('False complete-library claim')
        if [b['reads'] for b in left]!=partition(expected_reads,bin_size):
            raise ValueError('Complete ordered-bin partition mismatch')
    last=0
    counts={a:{k:0 for k in text['counts'][a]} for a in ('8','15')}
    for b in left:
        if b['first_read']!=last+1 or b['last_read']-last!=b['reads'] or b['primary_records']!=b['reads']:
            raise ValueError('Noncontiguous bins or invalid primary totals')
        last=b['last_read']
        for a in counts:
            for k in counts[a]:counts[a][k]+=b['counts'][a][k]
    first_agrees=None
    if pilot and run==DEFAULT_RUN and left and left[0]['reads']==1000000:
        first_agrees=left[0]['counts']==pilot['counts'] and left[0]['sam_records']==pilot['sam_qc']['sam_records']
        if not first_agrees:raise ValueError('First bin differs from historical fixed pilot')
    if len(hts.get('locus_bins',[]))<common:raise ValueError('Missing locus QC for completed bins')
    locus={}
    for b in hts.get('locus_bins',[])[:common]:
        for k,v in b.items():locus[k]=locus.get(k,0)+v
    denominator=counts['15']['canonical']+counts['15']['cryptic']
    return {'run':run,'complete_library':complete,'concordant_completed_bins':common,
            'concordant_completed_reads':last,'sam_records':sum(b['sam_records'] for b in left),
            'counts':counts,'locus_qc':locus,'first1M_matches_historical_pilot':first_agrees,
            'minimum_denominator':20,'denominator':denominator,
            ('complete_control_coverage_criterion_met' if run==DEFAULT_RUN else 'complete_library_coverage_criterion_met'):denominator>=20 if complete else None,
            'scope':('one public control' if run==DEFAULT_RUN else 'one public library')+'; bins are technical partitions, not independent replicates; no PSI/effect/biological absence',
            'input_qc_may_include_streamed_reads_ahead_of_validated_alignment_prefix':True}


def main(out,run=DEFAULT_RUN,manifest=None,bin_size=1000000):
    manifest=manifest or ROOT/'reports/gse122069-resource-plan/input_manifest.json'
    config=configure(load_rows(manifest),run,bin_size=bin_size)
    out=Path(out);exe=out/'execution'
    r=json.loads((exe/'full-control-results.json').read_text())
    text=json.loads((exe/'text-checkpoint.json').read_text())
    hts=json.loads((exe/'htslib-checkpoint.json').read_text())
    pilot=json.loads((ROOT/'reports/gse122069-pilot-20261031/pilot_results.json').read_text()) if run==DEFAULT_RUN else None
    summary=summarize(r,text,hts,pilot,run=run,expected_reads=config['expected_library_reads'],bin_size=bin_size)
    save(out/'summary.json',summary)
    keys=['bin','first_read','last_read','reads','sam_records','primary_records','total_introns_anchor8','total_introns_anchor15','canonical_anchor8','cryptic_anchor8','canonical_anchor15','cryptic_anchor15','locus_primary_block_overlap','locus_unique_mapq_block_overlap','exon1_unique_overlap','exon2_unique_overlap','locus_unique_spliced_reads']
    with (out/'bin-qc.tsv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=keys,delimiter='\t',lineterminator='\n');writer.writeheader()
        for i,b in enumerate(text['completed_bins'][:summary['concordant_completed_bins']]):
            row={k:b[k] for k in ('first_read','last_read','reads','sam_records','primary_records')};row['bin']=i+1
            for a in ('8','15'):
                row['total_introns_anchor'+a]=b['counts'][a]['eligible_intron_observations']
                for k in ('canonical','cryptic'):row[k+'_anchor'+a]=b['counts'][a][k]
            locus=hts['locus_bins'][i]
            for label,k in [('locus_primary_block_overlap','primary_block_overlap'),('locus_unique_mapq_block_overlap','unique_mapq_block_overlap'),('exon1_unique_overlap','exon1_unique_overlap'),('exon2_unique_overlap','exon2_unique_overlap'),('locus_unique_spliced_reads','unique_spliced_reads')]:row[label]=locus.get(k,0)
            writer.writerow(row)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(__doc__);parser.add_argument('out');parser.add_argument('--run-accession',default=DEFAULT_RUN);parser.add_argument('--manifest');parser.add_argument('--bin-size',type=int,default=1000000)
    a=parser.parse_args();main(a.out,a.run_accession,a.manifest,a.bin_size)
