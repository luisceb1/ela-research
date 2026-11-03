"""Compare reported local UNC13A junctions to cached hg38 annotation; no alignment.

Handles console top20 summaries without presenting missing rows as zeros. The
input is operator-reported evidence, not independent verification of WSL files.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re

REGION=['chr19',17600000,17690000]


def load_inventory(path):
    text=Path(path).read_text(encoding='utf-8-sig')
    try:return json.loads(text)
    except json.JSONDecodeError:
        matches=list(re.finditer(r'\{\s*"status":\s*"sealed_exploratory_locus_audit"',text))
        if len(matches)!=1:raise ValueError('Exactly one reported audit JSON required')
        return json.JSONDecoder().raw_decode(text[matches[0].start():])[0]


def reference_edges(annotation):
    if annotation.get('genome')!='hg38' or annotation.get('chrom')!='chr19' or annotation.get('track')!='wgEncodeGencodeCompV47':raise ValueError('Expected cached hg38 chr19 GENCODE v47 annotation')
    edges={};transcripts=[]
    for row in annotation['wgEncodeGencodeCompV47']:
        if row['name2']!='UNC13A':continue
        if row['chrom']!='chr19' or row['strand']!='-':raise ValueError('Unexpected UNC13A reference identity')
        starts=[int(x) for x in row['exonStarts'].strip(',').split(',')];ends=[int(x) for x in row['exonEnds'].strip(',').split(',')]
        if len(starts)!=len(ends) or not starts or any(a<0 or a>=b for a,b in zip(starts,ends)) or any(a>=b for a,b in zip(ends,starts[1:])):raise ValueError('Invalid reference exon geometry')
        transcripts.append(row['name'])
        for start,end in zip(ends,starts[1:]):edges.setdefault(('chr19',start,end,'-'),set()).add(row['name'])
    if not transcripts:raise ValueError('No UNC13A transcript in cached annotation')
    return edges,sorted(set(transcripts))


def event_key(row):
    e=row['event'];n=row['fragments']
    if (not isinstance(e,list) or len(e)!=4 or e[0]!='chr19' or e[3] not in ('-','+') or
        type(e[1]) is not int or type(e[2]) is not int or not 0<=e[1]<e[2] or
        not e[1]<REGION[2] or not e[2]>REGION[1] or type(n) is not int or n<=0):raise ValueError('Invalid regional junction/support')
    return tuple(e)


def compare(inventory,annotation):
    if inventory.get('status')!='sealed_exploratory_locus_audit' or inventory.get('gate_promoted') is not False or inventory.get('original_control_gate')!='coverage_insufficient' or inventory.get('same_prefix_target_and_qc_replay_identical') is not True:raise ValueError('Expected operator-reported insufficient-control audit with identical replay')
    partial=inventory.get('console_inventory_is_summary') is True
    regional=inventory if partial else inventory['regional_audit']
    if regional['window']!=REGION:raise ValueError('Unexpected audit window')
    edges,transcripts=reference_edges(annotation);rows=[];totals={}
    for route in ('text15','text8'):
        data=regional['routes'][route]
        observed=data['top20_by_support']+data['all_target_neighbors_within_2bp'] if partial else data['junctions']
        by_event={}
        for row in observed:
            event=event_key(row)
            if event in by_event and by_event[event]['fragments']!=row['fragments']:raise ValueError('Conflicting duplicate junction counts')
            by_event[event]=row
        reported=data['distinct_junctions'] if partial else len(by_event)
        if type(reported) is not int or reported<len(by_event):raise ValueError('Invalid reported inventory size')
        if not partial and len(observed)!=len(by_event):raise ValueError('Duplicate full-inventory junction')
        for event,row in sorted(by_event.items()):
            names=sorted(edges.get(event,[]))
            rows.append({'route':route,'chrom':event[0],'start0':event[1],'end0':event[2],'strand':event[3],'fragments':row['fragments'],
                         'annotation_status':'exact_cached_UNC13A' if names else 'not_in_cached_UNC13A_annotation','transcripts':';'.join(names)})
        totals[route]={'reported_distinct_junctions':reported,'available_distinct_junctions':len(by_event),
                       'unavailable_distinct_junctions':reported-len(by_event),'exact_cached_annotation_matches':sum(event in edges for event in by_event),
                       'not_in_cached_annotation':sum(event not in edges for event in by_event),
                       'available_event_support_sum_not_unique_groups':sum(r['fragments'] for r in by_event.values())}
    return {'status':'partial_console_comparison' if partial else 'complete_reported_inventory_comparison','operator_report_not_independent_WSL_verification':True,
            'all_inventory_rows_available':not partial,'reference_transcripts':transcripts,'reference_distinct_junctions':len(edges),
            'coordinate_convention':'intronic 0-based half-open','window':REGION,'routes':totals,'rows':rows,
            'annotation_scope':'cached transcripts overlapping the original retrieval window; one UCSC provider, not exhaustive isoform validation',
            'missing_rows_are_not_zero':True,'gate_promoted':False,'biological_inference':False,'new_downloads':0}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,required=True)
    p.add_argument('--annotation',type=Path,required=True);p.add_argument('--retrievals',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    receipts=json.loads(a.retrievals.read_text());receipt=next(r for r in receipts if r['name']=='annotation.json')
    if not receipt['saved'] or hashlib.sha256(a.annotation.read_bytes()).hexdigest()!=receipt['sha256']:raise ValueError('Cached annotation checksum mismatch')
    result=compare(load_inventory(a.inventory),json.loads(a.annotation.read_text()))
    result['input_sha256']={str(path):hashlib.sha256(path.read_bytes()).hexdigest() for path in (a.inventory,a.annotation,a.retrievals)}
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    with (a.out/'junctions.tsv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(result['rows'][0]) if result['rows'] else ['route','chrom','start0','end0','strand','fragments','annotation_status','transcripts'],delimiter='\t');writer.writeheader();writer.writerows(result['rows'])
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))


if __name__=='__main__':main()
