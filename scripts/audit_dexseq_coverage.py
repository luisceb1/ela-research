"""Aggregate culture-bin counts and denominator sensitivity, without inference."""
import argparse
import csv
import gzip
import hashlib
import json
import math
import platform
import statistics
from pathlib import Path
from scripts.audit_dexseq_counts import count, key, SPECIAL, unique_header
from scripts.describe_dexseq_batches import GENES, direction

HASHES = {'dexseq':'daaf355a7cbd48b617d30201ba289d8f0c4efc9fbc2a23ca2f991c84e1d814f4',
          'combined':'ded981755f00d546bac0fdf5d68bd3530891afffb3d335d3e78f2b4a708fea6e'}
FOCAL = {'ENSG00000104435:E009','ENSG00000130477:E026','ENSG00000130477:E030','ENSG00000130477:E054'}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def scaled(value, gene_total, library_total):
    if any(not isinstance(x, int) or isinstance(x, bool) or x < 0 for x in (value,gene_total,library_total)):
        raise ValueError('Counts/totals must be nonnegative integers')
    if gene_total < value or library_total < gene_total or gene_total == 0 or library_total == 0:
        raise ValueError('Invalid denominator hierarchy')
    return {'within_gene_pp':100*value/gene_total,
            'other_bins_ratio':value/(gene_total-value) if gene_total > value else None,
            'assigned_bin_CPM':1e6*value/library_total}

def aggregate(values):
    if not values or any(not isinstance(x,int) or x<0 for x in values): raise ValueError('Invalid count vector')
    return dict(min_count=min(values),median_count=statistics.median(values),max_count=max(values),
                sum_count=sum(values),zero_libraries=values.count(0),libraries_ge10=sum(v>=10 for v in values))

def load_design(path):
    with path.open() as f: rows=list(csv.DictReader(f,delimiter='\t'))
    if len(rows)!=12 or len({r['column'] for r in rows})!=12: raise ValueError('Expected 12 unique columns')
    for b,n in [('Batch 1',2),('Batch 2',4)]:
        for c in ['scramble','TDP43']:
            if sum(r['published_batch']==b and r['condition']==c for r in rows)!=n:
                raise ValueError('Unexpected batch/condition design')
    return rows

def assigned_totals(path, cols):
    totals={c:0 for c in cols}; seen=set(); special=set()
    with gzip.open(path,'rt') as f:
        r=csv.reader(f,delimiter='\t'); header=next(r); unique_header(header)
        ix={c:header.index(c.removeprefix('countData.')) for c in cols}
        for row in r:
            if len(row)!=len(header): raise ValueError('Ragged original count row')
            if row[0].startswith('_'):
                if row[0] not in SPECIAL or row[0] in special: raise ValueError('Invalid summary row')
                special.add(row[0]); continue
            k=key(row[0],True)
            if k in seen: raise ValueError('Duplicate assigned bin')
            seen.add(k)
            for c,i in ix.items(): totals[c]+=count(row[i])
    if special!=SPECIAL or len(seen)!=585869 or any(v<=0 for v in totals.values()):
        raise ValueError('Unexpected original matrix dimensions/totals')
    return totals

def compute(groups,design,totals):
    cols=[r['column'] for r in design]; coverage=[]; effects=[]; denominators=[]
    for gid,rs in groups.items():
        if len(rs)!={'STMN2':10,'UNC13A':62,'TARDBP':30}[GENES[gid]] or len({r['fragment'] for r in rs})!=len(rs):
            raise ValueError('Invalid target catalogue')
        gt={c:sum(count(r[c]) for r in rs) for c in cols}
        for batch in ['Batch 1','Batch 2']:
            for condition in ['scramble','TDP43']:
                cs=[r['column'] for r in design if r['published_batch']==batch and r['condition']==condition]
                denominators.append(dict(gene=GENES[gid],batch=batch,condition=condition,
                                         min_gene_bin_total=min(gt[c] for c in cs),max_gene_bin_total=max(gt[c] for c in cs),
                                         min_library_assigned_bin_total=min(totals[c] for c in cs),max_library_assigned_bin_total=max(totals[c] for c in cs)))
                for row in rs:
                    coverage.append(dict(gene=GENES[gid],fragment=row['fragment'],focal_previous_discordance=row['fragment'] in FOCAL,
                                         batch=batch,condition=condition,libraries=len(cs),**aggregate([count(row[c]) for c in cs])))
            for row in rs:
                vals={c:scaled(count(row[c]),gt[c],totals[c]) for c in cols}
                for method in ['within_gene_pp','other_bins_ratio','assigned_bin_CPM']:
                    means={}
                    for condition in ['scramble','TDP43']:
                        vs=[vals[r['column']][method] for r in design if r['published_batch']==batch and r['condition']==condition]
                        means[condition]=statistics.mean(vs) if all(v is not None for v in vs) else None
                    delta=means['TDP43']-means['scramble'] if all(v is not None for v in means.values()) else None
                    effects.append(dict(gene=GENES[gid],fragment=row['fragment'],focal_previous_discordance=row['fragment'] in FOCAL,
                                        batch=batch,method=method,mean_control=means['scramble'],mean_KD=means['TDP43'],delta=delta))
    return coverage,effects,denominators

def main(dexseq,combined,mapping,previous,out):
    for name,p in [('dexseq',dexseq),('combined',combined)]:
        if sha(p)!=HASHES[name]: raise ValueError('Original source hash mismatch: '+name)
    design=load_design(mapping); cols=[r['column'] for r in design]
    totals=assigned_totals(combined,cols); groups={g:[] for g in GENES}
    with gzip.open(dexseq,'rt') as f:
        for r in csv.DictReader(f):
            if r['groupID'] in groups:groups[r['groupID']].append(r)
    coverage,effects,denominators=compute(groups,design,totals)
    with previous.open() as f: old=list(csv.DictReader(f,delimiter='\t'))
    current={(r['fragment'],r['batch']):r for r in effects if r['method']=='within_gene_pp'}
    if len(old)!=204 or len({(r['fragment'],r['batch']) for r in old})!=204: raise ValueError('Prior table incomplete/duplicated')
    for r in old:
        c=current[(r['fragment'],r['batch'])]
        for a,b in [('mean_control_count_fraction','mean_control'),('mean_KD_count_fraction','mean_KD')]:
            if not math.isclose(100*float(r[a]),c[b],abs_tol=1e-10,rel_tol=1e-12): raise ValueError('Prior mean mismatch')
        if not math.isclose(float(r['change_percentage_points']),c['delta'],abs_tol=1e-10,rel_tol=1e-12):raise ValueError('Prior delta mismatch')
    labels=[]
    for frag in sorted({r['fragment'] for r in effects}):
        for method in ['within_gene_pp','other_bins_ratio','assigned_bin_CPM']:
            rows=[r for r in effects if r['fragment']==frag and r['method']==method]
            ds={r['batch']:r['delta'] for r in rows}; a,b=ds['Batch 1'],ds['Batch 2']
            labels.append(dict(gene=rows[0]['gene'],fragment=frag,focal_previous_discordance=frag in FOCAL,method=method,
                               delta_batch1=a,delta_batch2=b,classification=direction(a,b) if a is not None and b is not None else 'not_evaluable'))
    focal=[]
    for frag in sorted(FOCAL):
        cov=[r for r in coverage if r['fragment']==frag]; labs=[r for r in labels if r['fragment']==frag]
        focal.append(dict(fragment=frag,min_count_all_libraries=min(r['min_count'] for r in cov),zero_libraries=sum(r['zero_libraries'] for r in cov),
                          H1_all_counts_ge10=all(r['min_count']>=10 for r in cov),
                          H2_discordant_all_denominators=all(r['classification']=='opposite_direction' for r in labs),
                          direction_by_method={r['method']:r['classification'] for r in labs}))
    summary=dict(focal=focal,prior_rows_reproduced=204,coverage_rows=len(coverage),effect_rows=len(effects),
                 direction_counts={g:{m:{label:sum(r['gene']==g and r['method']==m and r['classification']==label for r in labels)
                     for label in ['same_direction','opposite_direction','zero_in_at_least_one_batch','not_evaluable']}
                     for m in ['within_gene_pp','other_bins_ratio','assigned_bin_CPM']} for g in GENES.values()},
                 no_inferential_tests=True,coverage_definition='Assigned counts per bin, not base or junction coverage')
    out.mkdir(parents=True,exist_ok=True)
    for name,rows in [('coverage_aggregates',coverage),('denominator_aggregates',denominators),('effects',effects),('direction_sensitivity',labels)]:
        with (out/(name+'.tsv')).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    (out/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    (out/'run.json').write_text(json.dumps(dict(python=platform.python_version(),date='2026-10-30',dependencies='stdlib',random_seed=None,
        parent_commit='0e8543c29e0945c4c03b5e2ae5516769438c6d9f',hashes={str(p):sha(p) for p in [dexseq,combined,mapping,previous,Path(__file__)]},
        cache_reused=True,new_download=False,technical_count_threshold=10,no_pseudocount=True),indent=2)+'\n')
    (out/'output_hashes.json').write_text(json.dumps({p.name:sha(p) for p in sorted(out.glob('*')) if p.suffix in {'.tsv','.json'} and p.name!='output_hashes.json'},indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for arg in ['dexseq','combined','mapping','previous','out']:p.add_argument('--'+arg,type=Path,required=True)
    a=p.parse_args();main(a.dexseq,a.combined,a.mapping,a.previous,a.out)
