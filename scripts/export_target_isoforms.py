#!/usr/bin/env python3
"""Export target transcript counts by sample and exon coordinates; descriptive only."""
import argparse
import csv
import gzip
import json
import re
from pathlib import Path

TARGETS = {"ENSG00000104435": "STMN2", "ENSG00000130477": "UNC13A"}
def opentext(p):
    return gzip.open(p, "rt") if str(p).endswith(".gz") else open(p, "rt")

def gtf_info(p):
    result={}
    with opentext(p) as fh:
        for line in fh:
            if line.startswith("#"): continue
            items=line.rstrip("\n").split("\t")
            if len(items)!=9 or items[2] not in ("transcript","exon"):continue
            at=dict(re.findall(r'(\w+)\s+"([^"]*)"',items[8]))
            gene=at.get("gene_id","").split(".")[0]
            if gene not in TARGETS: continue
            tx=at.get("transcript_id")
            if not tx:continue
            v=result.setdefault(tx,dict(gene=TARGETS[gene],chrom=items[0],strand=items[6],exons=set()))
            if items[2]=="exon": v["exons"].add((int(items[3]),int(items[4])))
    return result

def run(counts,gtf,out):
    info=gtf_info(gtf)
    Path(out).mkdir(parents=True,exist_ok=True)
    with opentext(counts) as f:
        reader=csv.DictReader(f,delimiter="\t")
        cols=[x for x in reader.fieldnames if x not in ("TXNAME","GENEID")]
        rows=[]
        for row in reader:
            tx=row["TXNAME"]
            if tx not in info:continue
            ref=info[tx]
            raw={k:int(row[k]) for k in cols}
            rows.append(dict(TXNAME=tx,gene=ref["gene"],model="novel_id_BambuTx" if tx.startswith("BambuTx") else "reference_id_ENST",**raw))
    with open(Path(out)/"target_counts.tsv","w",newline="") as o:
        w=csv.DictWriter(o,fieldnames=["TXNAME","gene","model"]+cols,delimiter="\t");w.writeheader();w.writerows(rows)
    with open(Path(out)/"target_exons.tsv","w",newline="") as o:
        w=csv.writer(o,delimiter="\t");w.writerow(["TXNAME","gene","chrom","strand","exon_start","exon_end"])
        for tx,v in info.items():
            for st,en in sorted(v["exons"]):w.writerow([tx,v["gene"],v["chrom"],v["strand"],st,en])
    with open(Path(out)/"target_summary.json","w") as o:
        json.dump({"counts_rows":len(rows),"gtf_target_transcripts":len(info),"sample_columns":cols,"bambu_count_rows":sum(z["model"]=="novel_id_BambuTx" for z in rows)},o,indent=2)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--counts",required=True);p.add_argument("--gtf",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();run(a.counts,a.gtf,a.out)
