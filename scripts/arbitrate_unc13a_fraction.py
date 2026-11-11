#!/usr/bin/env python3
"""Measure TDP-43 knockdown efficiency and library shape from recount3 gene sums.

Per research/plans/2026-11-11-unc13a-fraction-discrepancy.md, which reoriented
issue #37 towards arbitrating a four-to-five-fold disagreement in the UNC13A
cryptic fraction between a whole-transcriptome project and an amplicon project.

A cryptic *fraction* does not depend on sequencing depth, so depth cannot
explain the disagreement. Knockdown efficiency can, and this script quantifies
it from deposited gene-level counts.

It refuses to do so for a library whose gene counts are not transcriptome-wide:
in an amplicon run the counts reflect the amplified locus, not expression, so a
TARDBP "level" read off them would be meaningless. The script reports that
condition instead of producing a number.

Usage:
  python -I scripts/arbitrate_unc13a_fraction.py \
      --gene-sums GS.gz --qc QC.gz --sra SRA.MD.gz --label NAME [--json OUT]
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path

GENES = {
    "TARDBP": "ENSG00000120948",
    "UNC13A": "ENSG00000130477",
    "STMN2": "ENSG00000104435",
}
# A transcriptome-wide library expresses many thousands of genes. An amplicon
# run concentrates nearly all of its signal in a handful, so this is the test
# that decides whether a knockdown level may be computed at all.
MIN_GENES_DETECTED = 5000
MAX_TOP_GENE_SHARE = 0.5


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_gene_sums(path: Path) -> tuple[list[str], dict[str, list[int]], dict[str, dict]]:
    """Return sample order, counts for the genes of interest, and per-sample shape."""
    wanted = {v.split(".")[0]: k for k, v in GENES.items()}
    with gzip.open(path, "rt") as fh:
        header = None
        for line in fh:
            if line.startswith("##"):
                continue
            header = line.rstrip("\n").split("\t")
            break
        if header is None:
            raise ValueError("gene_sums file has no header")
        samples = header[1:]
        totals = [0] * len(samples)
        detected = [0] * len(samples)
        top = [0] * len(samples)
        found: dict[str, list[int]] = {}
        for line in fh:
            fields = line.rstrip("\n").split("\t")
            if len(fields) != len(header):
                continue
            base = fields[0].split(".")[0]
            values = [int(v) for v in fields[1:]]
            for i, value in enumerate(values):
                totals[i] += value
                if value > 0:
                    detected[i] += 1
                if value > top[i]:
                    top[i] = value
            name = wanted.get(base)
            if name:
                found[name] = values
    shape = {}
    for i, sample in enumerate(samples):
        share = (top[i] / totals[i]) if totals[i] else 0.0
        shape[sample] = {
            "total_counts": totals[i],
            "genes_detected": detected[i],
            "top_gene_share": round(share, 4),
            "transcriptome_wide": bool(detected[i] >= MIN_GENES_DETECTED
                                       and share <= MAX_TOP_GENE_SHARE),
        }
    return samples, found, shape


def read_lengths(path: Path) -> dict[str, dict]:
    out = {}
    with gzip.open(path, "rt") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            key = row.get("rail_id") or row.get("external_id") or ""
            out[key] = {
                "mode_length": row.get("bc_frag.mode_length"),
                "kallisto_mean_length": row.get("bc_frag.kallisto_mean_length"),
                "unique_pct": row.get("bc_auc.unique_%"),
            }
    return out


def conditions(path: Path) -> dict[str, dict]:
    def attr(blob: str, key: str) -> str:
        for part in (blob or "").split("|"):
            if part.startswith(key + ";;"):
                return part.split(";;", 1)[1]
        return ""

    out = {}
    with gzip.open(path, "rt") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            blob = row.get("sample_attributes", "")
            genotype = attr(blob, "genotype")
            treatment = attr(blob, "treatment")
            declared = genotype or treatment
            depleted = ("knockdown" in declared.lower()
                        or "shtdp" in declared.lower().replace("-", ""))
            out[row["external_id"]] = {
                "declared": declared,
                "cell_line": attr(blob, "cell line"),
                "group": "TDP43_depleted" if depleted else "control",
                "title": row.get("sample_title", ""),
            }
    return out


def run(args) -> dict:
    gs, qc, sra = Path(args.gene_sums), Path(args.qc), Path(args.sra)
    samples, genes, shape = read_gene_sums(gs)
    cond = conditions(sra)
    lengths = read_lengths(qc)

    rows = []
    for i, sample in enumerate(samples):
        info = cond.get(sample, {})
        entry = {"sample": sample, "group": info.get("group", "unknown"),
                 "declared": info.get("declared", ""),
                 "cell_line": info.get("cell_line", ""),
                 "shape": shape[sample]}
        total = shape[sample]["total_counts"]
        for name in GENES:
            value = genes.get(name, [0] * len(samples))[i]
            entry[name] = value
            entry[name + "_per_million"] = round(value / total * 1e6, 2) if total else None
        rows.append(entry)

    wide = [r for r in rows if r["shape"]["transcriptome_wide"]]
    verdict: dict = {
        "samples": len(rows),
        "transcriptome_wide_samples": len(wide),
        "knockdown_efficiency_computable": len(wide) == len(rows) and bool(rows),
    }
    if verdict["knockdown_efficiency_computable"]:
        for name in GENES:
            dep = [r[name + "_per_million"] for r in rows
                   if r["group"] == "TDP43_depleted"]
            ctl = [r[name + "_per_million"] for r in rows if r["group"] == "control"]
            if dep and ctl:
                med_dep = sorted(dep)[len(dep) // 2]
                med_ctl = sorted(ctl)[len(ctl) // 2]
                verdict[name] = {
                    "median_cpm_depleted": med_dep,
                    "median_cpm_control": med_ctl,
                    "ratio_depleted_over_control":
                        round(med_dep / med_ctl, 4) if med_ctl else None,
                    "percent_reduction":
                        round((1 - med_dep / med_ctl) * 100, 1) if med_ctl else None,
                }
    else:
        verdict["refusal_reason"] = (
            "Gene counts are not transcriptome-wide for every sample, so a "
            "knockdown level read off them would not measure expression. No "
            "number is produced; see the per-sample shape field.")
    return {
        "label": args.label,
        "inputs": {p.name: {"sha256": sha256(p), "bytes": p.stat().st_size}
                   for p in (gs, qc, sra)},
        "gene_ids": GENES,
        "shape_thresholds": {"min_genes_detected": MIN_GENES_DETECTED,
                             "max_top_gene_share": MAX_TOP_GENE_SHARE},
        "read_length_by_rail_id": lengths,
        "verdict": verdict,
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for flag in ("gene-sums", "qc", "sra", "label"):
        ap.add_argument(f"--{flag}", required=True)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args(argv)
    out = run(args)
    text = json.dumps(out, ensure_ascii=False, indent=1)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
