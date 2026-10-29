"""Exact same-gene GENCODE junction lookup; no novelty/crypticity inference."""
import argparse
from collections import Counter,defaultdict
import csv,gzip,hashlib,json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.map_isoseq_gtf import attrs


def junction_keys(gene,chrom,strand,exons):
    chain=sorted(set(exons))
    if any(a<1 or b<a for a,b in chain):raise ValueError('Invalid exon')
    if any(b[0]<=a[1] for a,b in zip(chain,chain[1:])):raise ValueError('Overlapping exons')
    return {(gene,chrom,a[1]+1,b[0]-1,strand) for a,b in zip(chain,chain[1:]) if a[1]+1<=b[0]-1}


def reference_lookup(path,wanted):
    genes={};txs={}
    with gzip.open(path,'rt') as f:
        for line in f:
            if line.startswith('#'):continue
            p=line.rstrip('\n').split('\t')
            if len(p)!=9:raise ValueError('Malformed GTF')
            a=attrs(p[8]);g=a.get('gene_id','').split('.')[0]
            if g not in wanted:continue
            if p[2]=='gene':
                rec={'symbol':a.get('gene_name',''),'gene_type':a.get('gene_type',''),'chrom':p[0],'strand':p[6]}
                if g in genes and genes[g]!=rec:raise ValueError('Ambiguous reference gene')
                genes[g]=rec
            if p[2]!='exon':continue
            t=a['transcript_id'];rec=txs.setdefault(t,{'gene':g,'chrom':p[0],'strand':p[6],'exons':[]})
            if (rec['gene'],rec['chrom'],rec['strand'])!=(g,p[0],p[6]):raise ValueError('Conflicting transcript identity')
            rec['exons'].append((int(p[3]),int(p[4])))
    lookup=defaultdict(list)
    for t,r in txs.items():
        for key in junction_keys(r['gene'],r['chrom'],r['strand'],r['exons']):lookup[key].append(t)
    return genes,lookup


def classify(key,genes,lookup):
    gene,chrom,_,_,strand=key
    if gene not in genes:return 'gene_not_in_v47'
    if (genes[gene]['chrom'],genes[gene]['strand'])!=(chrom,strand):return 'gene_locus_discordant'
    return 'exact_same_gene_junction' if key in lookup else 'junction_not_found_same_gene'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--reference',type=Path,required=True);a=p.parse_args()
    ref=json.loads((ROOT/'research/references/target_gene_ids_gencode_v47.json').read_text())
    digest=hashlib.sha256(a.reference.read_bytes()).hexdigest()
    if digest!=ref['source_sha256']:raise ValueError('Reference hash mismatch')
    src=ROOT/'reports/junction-filter-reconciliation/structural_membership.tsv'
    expected=json.loads((ROOT/'reports/junction-filter-reconciliation/repeat_verification.json').read_text())['structural_membership_sha256']
    if hashlib.sha256(src.read_bytes()).hexdigest()!=expected:raise ValueError('Input membership hash mismatch')
    with src.open() as f:rows=[r for r in csv.DictReader(f,delimiter='\t') if r['grouped_positive_after_ENST']=='True']
    keys=[(r['gene_id'],r['chrom'],int(r['intron_start']),int(r['intron_end']),r['strand']) for r in rows]
    if len(keys)!=len(set(keys)):raise ValueError('Duplicate input')
    genes,lookup=reference_lookup(a.reference,{k[0] for k in keys});out=ROOT/'reports/gencode-junction-annotation';out.mkdir(parents=True,exist_ok=True)
    counts=Counter();annotated=[]
    for k in sorted(keys):
        status=classify(k,genes,lookup);counts[status]+=1;r=genes.get(k[0],{})
        annotated.append([*k,r.get('symbol',''),r.get('gene_type',''),status,len(lookup.get(k,[])),';'.join(sorted(lookup.get(k,[]))) or '.'])
    with (out/'annotation.tsv').open('w') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['gene_id','chrom','intron_start','intron_end','strand','reference_symbol','reference_gene_type','status','reference_transcripts','reference_txnames']);w.writerows(annotated)
    result={'scope':'annotation lookup only; not novel/cryptic/protein validation','input_junctions':len(keys),'input_genes':len({k[0] for k in keys}),'reference_recognized_genes':len(genes),'statuses':dict(sorted(counts.items())),'input_sha256':expected,'reference_sha256':digest,'reference_url':ref['source_url'],'catalog_of_authors_compared':False,'individual_data_exported':False}
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(result)


if __name__=='__main__':main()
