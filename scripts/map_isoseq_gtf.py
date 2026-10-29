#!/usr/bin/env python3
"""Auditoría reproducible de identidades de transcritos Iso-Seq (sin inferencia biológica).
Uso: python scripts/map_isoseq_gtf.py --counts uniqueCounts.txt.gz --gtf extended_annotations.gtf.gz --out mapping.tsv --targets STMN2 UNC13A
Librería estándar. No calcula p-valores ni compara muestras.
"""
import argparse
import csv
import gzip
import re
from pathlib import Path

def read_text(path):
    return gzip.open(path, "rt", encoding="utf-8") if str(path).endswith(".gz") else open(path, encoding="utf-8")

def attrs(s):
    # GTF: key "value"; or GFF-style key=value (record separately if format differs).
    return dict(re.findall(r'(\w+)\s+"([^"]*)"', s))

def index_gtf(path):
    out = {}
    with read_text(path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) != 9 or p[2] not in ("transcript", "exon"):
                continue
            a = attrs(p[8])
            tx = a.get("transcript_id")
            if not tx:
                continue
            x = out.setdefault(tx, {"gene_id": "", "gene_name": "", "chrom": p[0], "strand": p[6], "exons": set()})
            x["gene_id"] = a.get("gene_id", x["gene_id"])
            x["gene_name"] = a.get("gene_name", x["gene_name"])
            if p[2] == "exon":
                x["exons"].add((p[3], p[4]))
    return out

GENE_IDS = {"STMN2": "ENSG00000104435", "UNC13A": "ENSG00000130477"}  # NCBI Gene/HGNC, GRCh38

def map_counts(counts, index, output, targets):
    total = matched = selected = mismatches = missing_names = 0
    by_target = {t: 0 for t in targets}
    with read_text(counts) as f, open(output, "w", newline="", encoding="utf-8") as o:
        r = csv.DictReader(f, delimiter="\t")
        if not {"TXNAME", "GENEID"}.issubset(set(r.fieldnames or [])):
            raise ValueError("Faltan columnas TXNAME/GENEID")
        w = csv.writer(o, delimiter="\t")
        w.writerow(["TXNAME", "GENEID_counts", "GENEID_gtf", "gene_name", "n_exons", "counts_sum", "mapping_status"])
        cols = [x for x in r.fieldnames if x not in ("TXNAME", "GENEID")]
        for row in r:
            total += 1
            tx = row["TXNAME"]
            g = index.get(tx)
            if g:
                matched += 1
            status = "unmapped" if not g else ("matched" if row["GENEID"].split(".")[0] == g["gene_id"].split(".")[0] else "gene_id_conflict")
            if status == "gene_id_conflict":
                mismatches += 1
            if g and not g["gene_name"]:
                missing_names += 1
            ens = row["GENEID"].split(".")[0]
            target = next((symbol for symbol in targets if ens == GENE_IDS.get(symbol) or (g and g["gene_name"].upper() == symbol)), None)
            if g and target:
                selected += 1
                by_target[target] += 1
                try:
                    cs = sum(float(row[k] or 0) for k in cols)
                except ValueError as e:
                    raise ValueError(f"Non-numeric count for {tx}") from e
                w.writerow([tx, row["GENEID"], g["gene_id"], target, len(g["exons"]), cs, status])
    return {"total": total, "gtf_matched": matched, "target_transcripts": selected, "gene_id_conflicts": mismatches, "gtf_missing_gene_names": missing_names, "by_target": by_target}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counts", required=True)
    ap.add_argument("--gtf", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--targets", nargs="+", default=["STMN2", "UNC13A"])
    a = ap.parse_args()
    index = index_gtf(a.gtf)
    summary = map_counts(a.counts, index, a.out, set(x.upper() for x in a.targets))
    print(summary)
    if summary["gtf_matched"] == 0:
        raise SystemExit("ERROR: no transcript identifiers match GTF")
if __name__ == "__main__":
    main()
