#!/usr/bin/env python3
"""Exact integrity audit of published culture counts; no inferential model."""
import argparse,csv,gzip,hashlib,json,re,platform
from pathlib import Path

SPECIAL={'_ambiguous','_ambiguous_readpair_position','_empty','_lowaqual','_notaligned'}

def count(value):
    if not re.fullmatch(r'[0-9]+',value):
        raise ValueError('Count must be a nonnegative integer literal')
    return int(value)

def key(value, combined=False):
    pattern=r'(ENSG[0-9]+(?:\+ENSG[0-9]+)*):([0-9]+)' if combined else r'(ENSG[0-9]+(?:\+ENSG[0-9]+)*):E([0-9]+)'
    m=re.fullmatch(pattern,value)
    if not m: raise ValueError('Unexpected fragment identifier: '+value)
    return m[1],int(m[2])

def unique_header(columns):
    if not columns or len(columns)!=len(set(columns)):raise ValueError('Empty or duplicate header')

def compare(a,b):
    if len(a)!=len(b):raise ValueError('Count vector length mismatch')
    return sum(x!=y for x,y in zip(a,b))

def run(combined,dexseq,out):
    matrix={};special={};zeros=0;cells=0
    with gzip.open(combined,'rt',newline='') as f:
        r=csv.reader(f,delimiter='\t');header=next(r);unique_header(header)
        if header[0]!='id':raise ValueError('Missing id header')
        aliases=header[1:]
        for row in r:
            if len(row)!=len(header):raise ValueError('Ragged combined row')
            vals=tuple(map(count,row[1:]));cells+=len(vals);zeros+=vals.count(0)
            if row[0].startswith('_'):
                if row[0] not in SPECIAL or row[0] in special:raise ValueError('Unexpected/duplicate summary row')
                special[row[0]]=dict(cells=len(vals),total=sum(vals));continue
            k=key(row[0],True)
            if k in matrix:raise ValueError('Duplicate combined fragment')
            matrix[k]=vals
    combined_rows=len(matrix);seen={};duplicate_rows=0;duplicate_count_conflicts=0;duplicate_core_conflicts=0;duplicate_annotation_variants=0;result_rows=0;mismatches=0;compared=0;dexzeros=0;allzero=0;id_discordances=0
    with gzip.open(dexseq,'rt',newline='') as f:
        r=csv.DictReader(f);unique_header(r.fieldnames)
        columns=[c for c in r.fieldnames if c.startswith('countData.')]
        if not columns:raise ValueError('No countData')
        ix=[aliases.index(c.removeprefix('countData.')) for c in columns]
        for row in r:
            k=key(row['fragment'])
            result_rows+=1
            if key(row['groupID']+':'+row['featureID'])!=k:id_discordances+=1
            vals=tuple(count(row[c]) for c in columns);dexzeros+=vals.count(0);allzero+=not any(vals)
            annotations={'entrez','symbol','chr','start','end','strand','biotype','description'}
            core=hashlib.sha256(json.dumps({x:v for x,v in row.items() if x not in annotations},sort_keys=True).encode()).digest()
            full=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).digest()
            if k in seen:
                duplicate_rows+=1
                oldvals,oldcore,oldfull=seen[k]
                duplicate_count_conflicts+=vals!=oldvals
                duplicate_core_conflicts+=core!=oldcore
                duplicate_annotation_variants+=(core==oldcore and full!=oldfull)
                continue
            seen[k]=(vals,core,full)
            if k not in matrix:raise ValueError('DEXSeq fragment absent from combined')
            original=matrix.pop(k);mismatches+=compare(vals,tuple(original[i] for i in ix));compared+=len(vals)
    result=dict(combined_fragment_rows=combined_rows,combined_libraries=len(aliases),combined_cells_including_summary=cells,
                combined_zero_cells_including_summary=zeros,summary_rows=special,dexseq_result_rows=result_rows,dexseq_unique_fragments=len(seen),
                duplicate_result_rows=duplicate_rows,duplicate_count_conflicts=duplicate_count_conflicts,
                duplicate_nonannotation_conflicts=duplicate_core_conflicts,duplicate_annotation_variant_rows=duplicate_annotation_variants,
                contrast_columns=len(columns),compared_cells=compared,discordant_cells=mismatches,
                combined_fragments_without_dexseq=len(matrix),fragment_group_feature_discordances=id_discordances,
                contrast_zero_cells_over_result_rows=dexzeros,contrast_all_zero_result_rows=allzero,
                counts_are_nonnegative_integer_literals=True,statistical_refit=False,
                interpretation='Technical concordance of two projections of the same study, not independent biological replication')
    out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    sources=[]
    for p,name in [(combined,'GSE121569_combined.dexseq.txt.gz'),(dexseq,'GSE121569_dexseq-all.csv.gz')]:
        raw=p.read_bytes();sources.append(dict(url='https://ftp.ncbi.nlm.nih.gov/geo/series/GSE121nnn/GSE121569/suppl/'+name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),accessed='2026-10-30',attribution='GEO GSE121569, Klim et al. 2019',license='Separate license not independently verified; raw matrices not redistributed'))
    (out/'sources.json').write_text(json.dumps(sources,indent=2)+'\n')
    (out/'run.json').write_text(json.dumps(dict(python=platform.python_version(),dependencies='stdlib',command='python scripts/audit_dexseq_counts.py --combined <combined.gz> --dexseq <dexseq-all.gz> --out reports/dexseq-qc'),indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--combined',type=Path,required=True);p.add_argument('--dexseq',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.combined,a.dexseq,a.out)
