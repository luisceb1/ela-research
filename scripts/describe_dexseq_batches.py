"""Within-group count fractions, not molecular fractions or PSI."""
import argparse,csv,gzip,json,hashlib,statistics
from pathlib import Path
from scripts.audit_dexseq_counts import count
GENES={'ENSG00000104435':'STMN2','ENSG00000130477':'UNC13A','ENSG00000120948':'TARDBP'}

def fractions(rows,cols):
    totals={c:sum(count(r[c]) for r in rows) for c in cols}
    if any(v==0 for v in totals.values()):raise ValueError('Zero within-group denominator')
    return [{c:count(r[c])/totals[c] for c in cols} for r in rows]

def direction(a,b):
    if a==0 or b==0:return 'zero_in_at_least_one_batch'
    return 'same_direction' if (a>0)==(b>0) else 'opposite_direction'

def run(source,mapping,out):
    with mapping.open() as f:design=list(csv.DictReader(f,delimiter='\t'))
    cols=[r['column'] for r in design]
    if len(cols)!=12 or len(set(cols))!=12:raise ValueError('Expected 12 unique contrast columns')
    groups={g:[] for g in GENES}
    with gzip.open(source,'rt') as f:
        for r in csv.DictReader(f):
            if r['groupID'] in groups:groups[r['groupID']].append(r)
    output=[];summary={}
    for gid,rs in groups.items():
        if not rs or len({r['fragment'] for r in rs})!=len(rs):raise ValueError('Missing/duplicate target fragments')
        fs=fractions(rs,cols);changes={};batchsizes={}
        for batch in ['Batch 1','Batch 2']:
            cs=[r['column'] for r in design if r['published_batch']==batch and r['condition']=='scramble']
            ks=[r['column'] for r in design if r['published_batch']==batch and r['condition']=='TDP43']
            if not cs or not ks:raise ValueError('Uncrossed batch')
            batchsizes[batch]={'scramble':len(cs),'KD':len(ks)}
            changes[batch]=[]
            for r,fr in zip(rs,fs):
                c=statistics.mean(fr[x] for x in cs);k=statistics.mean(fr[x] for x in ks);changes[batch].append(k-c)
                output.append(dict(gene=GENES[gid],fragment=r['fragment'],batch=batch,scramble_libraries=len(cs),KD_libraries=len(ks),mean_control_count_fraction=c,mean_KD_count_fraction=k,change_percentage_points=100*(k-c)))
        labels=[direction(a,b) for a,b in zip(changes['Batch 1'],changes['Batch 2'])]
        summary[GENES[gid]]=dict(fragments=len(rs),**{x:labels.count(x) for x in ['same_direction','opposite_direction','zero_in_at_least_one_batch']},library_counts=batchsizes)
    out.mkdir(parents=True,exist_ok=True)
    with (out/'fragment_batch_aggregates.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(output[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(output)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'provenance.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),design_sha256=hashlib.sha256(mapping.read_bytes()).hexdigest(),date='2026-10-30',method='library-level within-group count fraction, then unweighted condition mean within each published batch; no inferential tests',targets=GENES),indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--mapping',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.source,a.mapping,a.out)
