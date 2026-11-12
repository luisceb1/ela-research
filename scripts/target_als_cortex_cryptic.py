#!/usr/bin/env python3
"""UNC13A cryptic junction load in TARGET_ALS motor cortex, by subject group.

Per research/plans/2026-11-11-target-als-motor-cortex.md.

Reuses the sealed-coordinate lookup and the targeted-assay guard from
scripts/recount3_junction_probe.py rather than restating them, so the junction
definitions and the coordinate-convention check cannot drift between cycles.

PERSONAL DATA: the deposit's sample metadata carries sex, ethnicity, ages and
site of onset for pseudonymised post-mortem donors. This script reads ONLY the
subject-group column and deliberately drops every other such field, so no
individual clinical row can reach the output. Results are group aggregates.

It computes a within-gene ratio, cryptic / (cryptic + canonical), which
partially controls for expression and cell composition but does not remove
either. No effect, p-value or inferential PSI is produced.

Usage:
  python -I scripts/target_als_cortex_cryptic.py \
      --rr RR.gz --mm MM.gz --ids ID.gz --study STUDY.MD.gz \
      --targets targets.json [--min-coverage 20] [--json OUT]
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from recount3_junction_probe import assay_shape, find_target_rows, read_counts

# The only metadata column this script is allowed to read. Everything else in
# the deposit's sample table is clinical or demographic and stays unread.
GROUP_COLUMN = "Subject Group"
UNLABELLED = "(unlabelled)"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_groups(study_path: Path) -> dict[str, str]:
    """rail_id -> subject group, reading no other metadata column."""
    out = {}
    with gzip.open(study_path, "rt") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            rail = (row.get("rail_id") or "").strip()
            if not rail:
                continue
            group = (row.get(GROUP_COLUMN) or "").strip()
            out[rail] = group or UNLABELLED
    return out


def summed_ratio(counts: dict[str, int], control: str) -> float | None:
    """Sum of both cryptic junctions over that sum plus the canonical one.

    Kept for continuity with the earlier cycles, which all used this form, so
    figures stay comparable across reports. It is NOT a molecular inclusion
    fraction: see inclusion_psi.
    """
    cryptic = sum(v for k, v in counts.items() if k != control)
    total = cryptic + counts.get(control, 0)
    return (cryptic / total) if total else None


def inclusion_psi(counts: dict[str, int], control: str) -> float | None:
    """Inclusion estimate that does not double-count included molecules.

    A transcript carrying the cryptic exon offers TWO junctions a read can
    span (exon20-CE and CE-exon21); a transcript without it offers ONE
    (exon20-exon21). So at equal molecular abundance the two cryptic junctions
    together collect about twice the reads of the canonical one, and summing
    them inflates the ratio roughly twofold at low values.

    Averaging the two cryptic junctions puts inclusion and exclusion on the
    same per-junction footing, which is the usual PSI convention.
    """
    cryptic = [v for k, v in counts.items() if k != control]
    if not cryptic:
        return None
    inclusion = sum(cryptic) / len(cryptic)
    total = inclusion + counts.get(control, 0)
    return (inclusion / total) if total else None


def summarise(values: list[float]) -> dict:
    clean = [v for v in values if v is not None]
    if not clean:
        return {"n": 0}
    return {
        "n": len(clean),
        "median": round(statistics.median(clean), 5),
        "min": round(min(clean), 5),
        "max": round(max(clean), 5),
    }


def run(args) -> dict:
    spec = json.loads(Path(args.targets).read_text(encoding="utf-8"))
    chromosome = spec["chromosome"]
    control = spec.get("positive_control")
    targets = {k: tuple(v) for k, v in spec["junctions"].items()}

    shape = assay_shape(Path(args.rr), chromosome)
    located = find_target_rows(Path(args.rr), chromosome, targets)
    row_map = {info["row"]: name for name, info in located.items() if info.get("row")}
    counts, header = read_counts(Path(args.mm), row_map) if row_map else ({}, {})

    with gzip.open(args.ids, "rt") as fh:
        rails = [line.strip() for line in fh
                 if line.strip() and line.strip() != "rail_id"]
    groups = read_groups(Path(args.study))

    samples = []
    for column, rail in enumerate(rails, start=1):
        per = {name: counts.get(name, {}).get(column, 0) for name in targets}
        samples.append({
            "rail_id": rail,
            "group": groups.get(rail, UNLABELLED),
            "counts": per,
            "summed_ratio": summed_ratio(per, control),
            "inclusion_psi": inclusion_psi(per, control),
        })

    by_group: dict[str, dict] = {}
    for sample in samples:
        entry = by_group.setdefault(sample["group"], {
            "n": 0, "summed": [], "psi": [], "cryptic_any": 0,
            "cryptic_at_threshold": 0, "canonical": [],
            "per_junction": {name: [] for name in targets},
        })
        entry["n"] += 1
        entry["summed"].append(sample["summed_ratio"])
        entry["psi"].append(sample["inclusion_psi"])
        for name, value in sample["counts"].items():
            entry["per_junction"][name].append(value)
        cryptic_values = [v for k, v in sample["counts"].items() if k != control]
        if any(v > 0 for v in cryptic_values):
            entry["cryptic_any"] += 1
        if any(v >= args.min_coverage for v in cryptic_values):
            entry["cryptic_at_threshold"] += 1
        entry["canonical"].append(sample["counts"].get(control, 0))

    group_summary = {}
    for name, entry in by_group.items():
        group_summary[name] = {
            "n": entry["n"],
            "samples_with_any_cryptic_read": entry["cryptic_any"],
            "samples_with_cryptic_at_or_above_threshold": entry["cryptic_at_threshold"],
            "summed_ratio": summarise(entry["summed"]),
            "inclusion_psi": summarise(entry["psi"]),
            "per_junction_counts": {
                name: {"median": statistics.median(vals),
                       "min": min(vals), "max": max(vals),
                       "samples_with_any_read": sum(1 for v in vals if v > 0),
                       "samples_at_or_above_threshold":
                           sum(1 for v in vals if v >= args.min_coverage)}
                for name, vals in entry["per_junction"].items()
            },
            "canonical_counts": {
                "median": statistics.median(entry["canonical"]),
                "min": min(entry["canonical"]), "max": max(entry["canonical"]),
            },
        }

    return {
        "tissue": spec.get("tissue", ""),
        "coordinate_conversion":
            "sealed intronic 0-based half-open -> [start0+1, end0] 1-based inclusive",
        "inputs": {Path(p).name: {"sha256": sha256(Path(p)),
                                  "bytes": Path(p).stat().st_size}
                   for p in (args.rr, args.mm, args.ids, args.study)},
        "assay_shape": shape,
        "matrix_header": header,
        "positive_control": control,
        "located": located,
        "min_coverage": args.min_coverage,
        "metadata_columns_read": [GROUP_COLUMN],
        "personal_data_note": (
            "Only the subject-group column was read. Sex, ethnicity, ages and "
            "site of onset were deliberately not read, and no individual "
            "clinical row appears in this output."),
        "n_samples": len(samples),
        "by_group": group_summary,
        "ratio_definitions": {
            "summed_ratio": "(cryptic_left + cryptic_right) / (that sum + canonical); kept for continuity, inflated about twofold at low values",
            "inclusion_psi": "mean(cryptic_left, cryptic_right) / (that mean + canonical); puts inclusion and exclusion on the same per-junction footing",
        },
        "samples": [{"rail_id": s["rail_id"], "group": s["group"],
                     "counts": s["counts"],
                     "summed_ratio": (round(s["summed_ratio"], 5)
                                      if s["summed_ratio"] is not None else None),
                     "inclusion_psi": (round(s["inclusion_psi"], 5)
                                       if s["inclusion_psi"] is not None else None)}
                    for s in samples],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for flag in ("rr", "mm", "ids", "study", "targets"):
        ap.add_argument(f"--{flag}", required=True)
    ap.add_argument("--min-coverage", type=int, default=20)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args(argv)
    out = run(args)
    text = json.dumps(out, ensure_ascii=False, indent=1)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
