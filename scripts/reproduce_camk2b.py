"""Reproduce aggregate transcript-model comparison; no donor-level output.

Uses public GTF/counts pinned by the GEO audit. Does not run received scripts.
An absent catalog model is not evidence of an absent biological junction.
"""
import argparse
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path

try:
    from scripts.map_isoforms import junctions, read_local_exons
except ModuleNotFoundError:
    from map_isoforms import junctions, read_local_exons

ROOT = Path(__file__).resolve().parents[1]
GENES = {"CAMK2B": "ENSG00000058404", "STMN2": "ENSG00000104435", "HDGFL2": "ENSG00000167674"}
CANDIDATES = {"CAMK2B": "BambuTx9181", "STMN2": "BambuTx9249", "HDGFL2": "BambuTx8683"}
TARGET = ("chr7", "-", 44220901, 44222117)


def keys(record):
    return {(record["chrom"], record["strand"], a, b) for a, b in junctions(record["exons"])}


def matching_models(records, gene, key):
    return sorted(tx for tx, r in records.items()
                  if r["geneid"].split(".")[0] == gene and key in keys(r))


def aggregate_counts(path, models):
    totals, seen, gene_totals = {}, set(), {}
    with gzip.open(path, "rt") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        if header[:2] != ["TXNAME", "GENEID"] or len(header) != len(set(header)):
            raise ValueError("Invalid count columns")
        n = len(header) - 2
        for row in reader:
            if len(row) != len(header):
                raise ValueError("Malformed count row")
            tx, gene = row[:2]
            if gene.split(".")[0] not in GENES.values():
                continue
            if tx in seen or tx not in models or models[tx]["geneid"].split(".")[0] != gene.split(".")[0]:
                raise ValueError("Duplicate or inconsistent target transcript")
            seen.add(tx)
            values = [float(v) for v in row[2:]]
            if any(not math.isfinite(v) or v < 0 for v in values):
                raise ValueError("Invalid deposited count")
            totals[tx] = math.fsum(values)
            vec = gene_totals.setdefault(gene.split(".")[0], [0.0] * n)
            for i, value in enumerate(values):
                vec[i] += value
        if seen != set(models):
            raise ValueError("Target catalog and counts do not match")
    return {"transcript_totals": totals, "libraries": n,
            "gene_qc": {g: {"libraries_with_positive_gene_sum": sum(v > 0 for v in vec),
                             "gene_assigned_count_sum": math.fsum(vec)}
                        for g, vec in gene_totals.items()}}


def run(cache):
    sources = json.loads((ROOT / "reports/geo-audit/sources.json").read_text())
    datasets, source_checks = {}, []
    for gse, label in [("GSE310723", "i3N"), ("GSE315972", "NYGC")]:
        paths = []
        for suffix in ["extended_annotations.gtf.gz", "uniqueCounts_transcript.txt.gz"]:
            path = cache / f"{gse}_{label}_isoseq_{suffix}"
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != sources[path.name]["source_sha256"]:
                raise ValueError(f"Source hash mismatch: {path.name}")
            source_checks.append({"file": path.name, "sha256": digest, "url": sources[path.name]["url"], "matches_prior_geo_audit": True})
            paths.append(path)
        models = read_local_exons(paths[0], GENES.values())
        counts = aggregate_counts(paths[1], models)
        datasets[gse] = {"models": models, "counts": counts}
    cell, brain = datasets["GSE310723"], datasets["GSE315972"]
    candidate = cell["models"].get(CANDIDATES["CAMK2B"])
    if candidate is None or candidate["geneid"].split(".")[0] != GENES["CAMK2B"] or TARGET not in keys(candidate):
        raise ValueError("Original CAMK2B candidate identity not verified")
    summary, structure = [], []
    for gse, data in datasets.items():
        for symbol, gene in GENES.items():
            models = {tx: r for tx, r in data["models"].items() if r["geneid"].split(".")[0] == gene}
            hits = matching_models(models, gene, TARGET) if symbol == "CAMK2B" else []
            summary.append({"dataset": gse, "gene": symbol, "models": len(models),
                            "ENST_models": sum(tx.startswith("ENST") for tx in models),
                            "CAMK2B_target_matches": len(hits) if symbol == "CAMK2B" else None,
                            "CAMK2B_target_transcript_assigned_sum": math.fsum(data["counts"]["transcript_totals"][tx] for tx in hits) if symbol == "CAMK2B" else None,
                            "libraries": data["counts"]["libraries"],
                            **data["counts"]["gene_qc"][gene]})
    for symbol, tx in CANDIDATES.items():
        rec = cell["models"].get(tx)
        if rec is None or rec["geneid"].split(".")[0] != GENES[symbol]:
            raise ValueError("Control candidate identity missing")
        for key in sorted(keys(rec)):
            hits = matching_models(brain["models"], GENES[symbol], key)
            structure.append({"gene": symbol, "cell_candidate_txname": tx,
                              "chrom": key[0], "strand": key[1],
                              "left_exonic_boundary_1based": key[2], "right_exonic_boundary_1based": key[3],
                              "brain_models_with_exact_junction": len(hits),
                              "brain_assigned_sum_matching_models_not_junction_reads": math.fsum(brain["counts"]["transcript_totals"][x] for x in hits)})
    c = next(r for r in summary if r["dataset"] == "GSE310723" and r["gene"] == "CAMK2B")
    b = next(r for r in summary if r["dataset"] == "GSE315972" and r["gene"] == "CAMK2B")
    return {"scope": "technical reproduction on identical public processed files; not independent biological replication",
            "coordinate_system": "GRCh38 GTF exonic boundary bases, 1-based inclusive, sorted genomic order even on minus strand",
            "sources": source_checks, "summary": summary, "candidate_junctions": structure,
            "prior_report_predictions": {"cell_matching_models_is_1": c["CAMK2B_target_matches"] == 1,
                                         "cell_target_assigned_sum_is_32": c["CAMK2B_target_transcript_assigned_sum"] == 32,
                                         "brain_CAMK2B_models_is_49": b["models"] == 49,
                                         "brain_matching_models_is_0": b["CAMK2B_target_matches"] == 0},
            "new_pvalues_or_effect_sizes": False, "individual_rows_exported": False}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cache", type=Path, default=ROOT / "data/cache")
    p.add_argument("--output", type=Path, default=ROOT / "reports/camk2b-reproduction/audit.json")
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = run(args.cache)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
