#!/usr/bin/env python3
"""Export per-library QC of two complete public controls; no pooling or effects."""
import csv
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.gse122069_run_config import load_rows


def read(path):return json.loads(path.read_text())


def build():
    roots=[('SRR8144907',ROOT/'reports/gse122069-full-control-20261031'),
           ('SRR8144908',ROOT/'reports/gse122069-next-control-20261031')]
    rows={r['run']:r for r in load_rows(ROOT/'reports/gse122069-resource-plan/input_manifest.json')}
    table=[];inputs=[]
    for run,root in roots:
        row=rows[run]
        receipt_name='fastq-download.json' if run=='SRR8144907' else 'download.json'
        paths=[root/'summary.json',root/'execution/full-control-results.json',root/'execution/fastq_qc.json',root/receipt_name]
        summary,result,fastq,receipt=map(read,paths)
        if result['run']!=run or summary['run']!=run or receipt['run']!=run:raise ValueError('QC identity mismatch')
        if not all([summary['complete_library'],result['complete_library'],receipt['verified'],fastq['gzip_eof_crc_validated'],result['independent_parser_concordant']]):
            raise ValueError('Require complete verified library QC; no partial pooling')
        if not (summary['concordant_completed_reads']==result['reads']==fastq['reads']==row['reads']):raise ValueError('QC read counts disagree')
        if receipt['md5']!=row['md5'] or result['fastq_sha256']!=receipt['sha256']:raise ValueError('QC source hash mismatch')
        if summary['counts']!=result['counts']:raise ValueError('QC target/global totals disagree')
        locus=summary['locus_qc'];counts=summary['counts']
        table.append({'run':run,'gsm':row['gsm'],'published_group':row['published_group'],
                      'complete_reads':row['reads'],'concordant_bins':summary['concordant_completed_bins'],
                      'sam_records':summary['sam_records'],'canonical_anchor15':counts['15']['canonical'],
                      'cryptic_anchor15':counts['15']['cryptic'],'canonical_anchor8':counts['8']['canonical'],
                      'cryptic_anchor8':counts['8']['cryptic'],'eligible_introns_anchor15':counts['15']['eligible_intron_observations'],
                      'eligible_introns_anchor8':counts['8']['eligible_intron_observations'],
                      'exon1_unique_overlap':locus.get('exon1_unique_overlap',0),'exon2_unique_overlap':locus.get('exon2_unique_overlap',0),
                      'minimum_denominator20_met':counts['15']['canonical']+counts['15']['cryptic']>=20,
                      'sha256_fastq':receipt['sha256']})
        inputs += [{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
    out=roots[1][1]
    with (out/'two-control-technical-qc.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(table[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(table)
    record={'rows':table,'input_metadata_sha256':inputs,'scope':'two public control libraries of the same published study; no pooling, molecular PSI, effect or inference; biological unit/batch/pair map unresolved; historical first1M is contained in first full library, not added as another sample'}
    (out/'two-control-technical-qc.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))

if __name__=='__main__':build()
