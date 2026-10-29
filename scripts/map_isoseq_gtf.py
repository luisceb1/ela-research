#!/usr/bin/env python3
"""Auditoría reproducible de identidades de transcritos Iso-Seq (sin inferencia biológica).
Uso: python scripts/map_isoseq_gtf.py --counts uniqueCounts.txt.gz --gtf extended_annotations.gtf.gz --out mapping.tsv --targets STMN2 UNC13A
Librería estándar. No calcula p-valores ni compara muestras.
"""
import argparse
import csv
import gzip
import json
import math
import re
import tempfile
from pathlib import Path

def read_text(path):
    return gzip.open(path, "rt", encoding="utf-8") if str(path).endswith(".gz") else open(path, encoding="utf-8")

def attrs(s):
    # Quoted GTF attributes; GFF key=value is not accepted by this parser.
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
            if (x["gene_id"] and a.get("gene_id") and x["gene_id"].split(".")[0] != a["gene_id"].split(".")[0]) or (x["chrom"], x["strand"]) != (p[0], p[6]):
                raise ValueError(f"Conflicting transcript identity: {tx}")
            if x["gene_name"] and a.get("gene_name") and x["gene_name"] != a["gene_name"]:
                raise ValueError(f"Conflicting transcript symbol: {tx}")
            x["gene_id"] = a.get("gene_id", x["gene_id"])
            x["gene_name"] = a.get("gene_name", x["gene_name"])
            if p[2] == "exon":
                x["exons"].add((p[3], p[4]))
    return out

REFERENCE_PATH = Path(__file__).resolve().parents[1] / "research/references/target_gene_ids_gencode_v47.json"
GENE_IDS = {symbol: record["gene_id"] for symbol, record in json.loads(REFERENCE_PATH.read_text())["panel"].items()}


def check_summary(summary, targets):
    """Technical acceptance gate, never a biological absence test."""
    if not summary["total"] or summary["gtf_matched"] != summary["total"]:
        raise ValueError("Incomplete transcript/GTF matching")
    if summary["gene_id_conflicts"] or summary["symbol_id_conflicts"]:
        raise ValueError("Transcript gene identity conflicts")
    absent = sorted(t for t in targets if summary["by_target"].get(t, 0) == 0)
    if absent:
        raise ValueError(f"Positive target controls missing: {absent}; do not infer biological absence")

def map_counts(counts, index, output, targets):
    targets = {t.upper() for t in targets}
    if not targets or targets.difference(GENE_IDS):
        raise ValueError("Unknown or empty target panel; use versioned Ensembl IDs")
    total = matched = selected = mismatches = missing_names = symbol_conflicts = 0
    by_target = {t: 0 for t in sorted(targets)}
    ids_to_symbols = {GENE_IDS[t]: t for t in targets}
    seen = set()
    with read_text(counts) as f, open(output, "w", newline="", encoding="utf-8") as o:
        r = csv.DictReader(f, delimiter="\t")
        if not {"TXNAME", "GENEID"}.issubset(set(r.fieldnames or [])):
            raise ValueError("Faltan columnas TXNAME/GENEID")
        w = csv.writer(o, delimiter="\t")
        w.writerow(["TXNAME", "GENEID_counts", "GENEID_gtf", "gene_name", "n_exons", "counts_sum", "mapping_status"])
        cols = [x for x in r.fieldnames if x not in ("TXNAME", "GENEID")]
        if not cols or len(r.fieldnames) != len(set(r.fieldnames)):
            raise ValueError("Missing or duplicated count columns")
        for row in r:
            if None in row or any(row[k] is None for k in r.fieldnames):
                raise ValueError("Malformed count row")
            total += 1
            tx = row["TXNAME"]
            if not tx or tx in seen:
                raise ValueError("Empty or duplicate transcript ID")
            seen.add(tx)
            g = index.get(tx)
            if g:
                matched += 1
            status = "unmapped" if not g else ("matched" if row["GENEID"].split(".")[0] == g["gene_id"].split(".")[0] else "gene_id_conflict")
            if status == "gene_id_conflict":
                mismatches += 1
            if g and not g["gene_name"]:
                missing_names += 1
            ens = row["GENEID"].split(".")[0]
            target = ids_to_symbols.get(ens)
            name = g["gene_name"].upper() if g else ""
            if g and name and ((target and name != target) or (name in targets and ens != GENE_IDS[name])):
                symbol_conflicts += 1
                continue
            if g and target and status == "matched":
                selected += 1
                by_target[target] += 1
                try:
                    values = [float(row[k]) for k in cols]
                    if any(not math.isfinite(v) or v < 0 for v in values):
                        raise ValueError("Negative or non-finite count")
                    cs = math.fsum(values)
                except ValueError as e:
                    raise ValueError(f"Non-numeric count for {tx}") from e
                w.writerow([tx, row["GENEID"], g["gene_id"], target, len(g["exons"]), cs, status])
    return {"total": total, "gtf_matched": matched, "target_transcripts": selected, "gene_id_conflicts": mismatches, "symbol_id_conflicts": symbol_conflicts, "gtf_missing_gene_names": missing_names, "by_target": by_target}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counts", required=True)
    ap.add_argument("--gtf", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--targets", nargs="+", default=["STMN2", "UNC13A"])
    a = ap.parse_args()
    index = index_gtf(a.gtf)
    output = Path(a.out)
    with tempfile.NamedTemporaryFile(dir=output.parent, prefix=output.name + ".", delete=False) as f:
        temporary = Path(f.name)
    try:
        summary = map_counts(a.counts, index, temporary, set(x.upper() for x in a.targets))
        print(summary)
        check_summary(summary, set(x.upper() for x in a.targets))
        temporary.replace(output)
    except (ValueError, OSError) as exc:
        temporary.unlink(missing_ok=True)
        raise SystemExit(f"ERROR: {exc}") from exc
if __name__ == "__main__":
    main()
