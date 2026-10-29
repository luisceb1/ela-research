#!/usr/bin/env python3
"""Reconstruct BambuTx junction intersection across two GEO long-read datasets.
Exploratory: transcript-assigned reads, NOT junction-spanning reads.
"""
import argparse, csv, gzip, re, collections, json
from pathlib import Path

ATTR=re.compile(r'(\w+)\s+"([^"]*)"')
def opener(path):
    return gzip.open(path,"rt") if str(path).endswith(".gz") else open(path,encoding="utf-8")
def stable(s):return s.split(".")[0]
def counts(path):
    rows={}
    with opener(path) as f:
        reader=csv.DictReader(f,delimiter="\t")
        samples=[x for x in reader.fieldnames if x not in ("TXNAME","GENEID")]
        for r in reader:
            tx=r["TXNAME"]
            if tx.startswith("BambuTx"):
                rows[tx]=(stable(r["GENEID"]),tuple(int(float(r[k])) for k in samples))
    return samples,rows
def junction_index(gtf,rows):
    txinfo={}
    with opener(gtf) as f:
        for line in f:
            if line.startswith("#"):continue
            p=line.rstrip("\n").split("\t")
            if len(p)!=9 or p[2]!="exon":continue
            a=dict(ATTR.findall(p[8]))
            tx=a.get("transcript_id","")
            if tx not in rows and not tx.startswith("ENST"):continue
            gene=stable(a.get("gene_id",""))
            if not gene.startswith("ENSG"):continue
            if tx in rows and rows[tx][0]!=gene: continue
            if tx not in txinfo:
                txinfo[tx]=(gene,p[0],p[6],[])
            prior=txinfo[tx]
            if prior[:3]!=(gene,p[0],p[6]):continue
            prior[3].append((int(p[3]),int(p[4])))
    novel=collections.defaultdict(list); reference=set()
    for tx,(gene,chrom,strand,exons) in txinfo.items():
        exons.sort()
        for left,right in zip(exons,exons[1:]):
            if left[1]>=right[0]:continue
            junction=(gene,chrom,left[1]+1,right[0]-1,strand)
            if tx.startswith("BambuTx"):
                novel[junction].append(tx)
            elif tx.startswith("ENST"):
                reference.add(junction)
    return novel,reference
def run(c1,g1,c2,g2,out):
    samples1,r1=counts(c1);samples2,r2=counts(c2)
    nov1,ref1=junction_index(g1,r1);nov2,ref2=junction_index(g2,r2)
    shared=sorted(set(nov1)&set(nov2)-ref1-ref2)
    Path(out).mkdir(parents=True,exist_ok=True)
    outrows=[]
    for gene,chrom,start,end,strand in shared:
        key=(gene,chrom,start,end,strand)
        t1=sorted(set(nov1[key]));t2=sorted(set(nov2[key]))
        row=dict(gene_id=gene,chrom=chrom,intron_start=start,intron_end=end,strand=strand,
                 culture_tx=";".join(t1),brain_tx=";".join(t2))
        for col,txs,rows,samples in [("culture",t1,r1,samples1),("brain",t2,r2,samples2)]:
            for i,sample in enumerate(samples):
                row[col+"__"+sample]=sum(rows[x][1][i] for x in txs)
        outrows.append(row)
    columns=["gene_id","chrom","intron_start","intron_end","strand","culture_tx","brain_tx"]+["culture__"+x for x in samples1]+["brain__"+x for x in samples2]
    with open(Path(out)/"junctions_shared.tsv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=columns,delimiter="\t");w.writeheader();w.writerows(outrows)
    stats=dict(shared_junctions=len(shared),genes=len(set(k[0] for k in shared)),
               n_culture_bambu=len(r1),n_brain_bambu=len(r2),
               n_culture_junctions=len(nov1),n_brain_junctions=len(nov2),
               cultured_samples=samples1,brain_samples=samples2,
               caveat="No biological replicates for cultured condition; transcript-assigned reads are not junction-spanning read counts; unannotated internally != novel.")
    (Path(out)/"summary.json").write_text(json.dumps(stats,indent=2))
    print(json.dumps(stats,indent=2))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    for v in ["culture-counts","culture-gtf","brain-counts","brain-gtf","out"]:
        p.add_argument("--"+v,required=True)
    a=p.parse_args()
    run(a.culture_counts,a.culture_gtf,a.brain_counts,a.brain_gtf,a.out)
