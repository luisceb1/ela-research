#!/usr/bin/env python3
"""Per-library depth normalisation of sealed-junction counts, by group.

Deposited on 2026-11-11 to make reproducible a figure that two earlier
versions of reports/target-als-cervical-20261111/REPORT.md stated without any
committed procedure behind it. Both earlier figures were wrong, in different
ways:

  * The first ("canonical per million" of 2.30 and 0.11) divided the GROUP
    MEDIAN count by a SINGLE project-level median depth of 44.4 M applied to
    both tissues. That is a ratio of medians, not a per-library
    normalisation. The 44.4 M was also mislabelled in the report as "reads
    assigned to exons"; it is `exon_fc_count_all.total`, the reads SUBMITTED
    to featureCounts. The reads actually assigned differ between the two
    tissues (about 20.3 M against 23.9 M), so the claim that depth was
    "identical" held only for the field that was not named.

  * The second (2.530 and 0.113, "22.3x") was right, but was announced with
    no procedure committed and with the denominator named wrongly. An
    external reader could not reproduce it: trying `.assigned` gives 0.2055
    and input reads give 0.1150 for the cervical ALS group, neither of which
    is 0.113. It reproduces exactly against `exon_fc_count_all.total`, which
    is the field the report should have named. An unreproducible correct
    figure is not an acceptable state for a published report, which is why
    this script exists.

This script replaces both. For each library it divides that library's
junction count by that library's own depth, then takes the median of those
ratios within a group. It reports every candidate denominator rather than one,
because the choice of denominator moves the figure by a factor of two and the
reader is entitled to see that.

It refuses to produce a figure when any sample in a group has no QC row, so a
silent partial match cannot be mistaken for a complete one.

PERSONAL DATA: reads only rail_id and the numeric QC columns named below from
the QC table, and only the group label already present in the cycle's
results.json. No clinical or demographic field is read.

Usage:
  python -I scripts/normalize_tissue_coverage.py \
      --tissue 'Cortex:reports/.../results.json:qc.MD.gz' \
      --tissue 'Cervical:reports/.../results.json:qc_cerv.MD.gz' \
      [--junction canonical] [--json OUT]
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

# Candidate per-library denominators, in the order they are reported. The
# first is the primary: it is the field the original report had in hand, so
# quoting it keeps the correction comparable with what it corrects.
DENOMINATORS = (
    "exon_fc_count_all.total",
    "exon_fc_count_all.assigned",
    "star.number_of_input_reads",
    "star.all_mapped_reads",
    "star.uniquely_mapped_reads_number",
)
PRIMARY = DENOMINATORS[0]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_depths(qc_path: Path) -> dict[str, dict[str, float]]:
    """rail_id -> {denominator field: value}, reading no other column."""
    out: dict[str, dict[str, float]] = {}
    with gzip.open(qc_path, "rt") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            rail = (row.get("rail_id") or "").strip()
            if not rail:
                continue
            entry = {}
            for field in DENOMINATORS:
                raw = (row.get(field) or "").strip()
                if raw in ("", "NA"):
                    continue
                try:
                    value = float(raw)
                except ValueError:
                    continue
                if value > 0:
                    entry[field] = value
            out[rail] = entry
    return out


def describe(values: list[float]) -> dict:
    return {
        "n": len(values),
        "median": round(statistics.median(values), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def normalise_group(samples: list[dict], depths: dict[str, dict[str, float]],
                    junction: str) -> dict:
    """Per-library ratios for one group, plus the ratio of medians for contrast."""
    missing = [s["rail_id"] for s in samples if s["rail_id"] not in depths]
    out: dict = {"n_samples": len(samples), "missing_qc_rows": missing}
    if missing:
        # Deliberate: an incomplete match is reported as a refusal, not as a
        # figure computed over whatever happened to match.
        out["per_million"] = None
        out["refused"] = (
            f"{len(missing)} of {len(samples)} samples have no QC row; "
            "no normalised figure is produced")
        return out

    counts = [s["counts"].get(junction, 0) for s in samples]
    per_field = {}
    for field in DENOMINATORS:
        usable = [s for s in samples if field in depths[s["rail_id"]]]
        if len(usable) != len(samples):
            per_field[field] = {
                "refused": f"field absent for {len(samples) - len(usable)} samples"}
            continue
        ratios = [s["counts"].get(junction, 0)
                  / (depths[s["rail_id"]][field] / 1e6) for s in usable]
        median_depth = statistics.median(
            depths[s["rail_id"]][field] for s in usable)
        per_field[field] = {
            "per_library_ratios": describe(ratios),
            "median_depth_M": round(median_depth / 1e6, 3),
            "ratio_of_medians_NOT_a_normalisation": round(
                statistics.median(counts) / (median_depth / 1e6), 4),
        }
    out["raw_counts"] = describe([float(c) for c in counts])
    out["per_million"] = per_field
    return out


def run(args) -> dict:
    tissues: dict = {}
    for spec in args.tissue:
        label, results_path, qc_path = spec.split(":", 2)
        results = json.loads(Path(results_path).read_text(encoding="utf-8"))
        depths = read_depths(Path(qc_path))
        by_group = {}
        for sample in results["samples"]:
            by_group.setdefault(sample["group"], []).append(sample)
        tissues[label] = {
            "results_file": results_path,
            "results_sha256": sha256(Path(results_path)),
            "qc_file": Path(qc_path).name,
            "qc_sha256": sha256(Path(qc_path)),
            "qc_rows": len(depths),
            "tissue_in_results": results.get("tissue", ""),
            "by_group": {
                group: normalise_group(samples, depths, args.junction)
                for group, samples in sorted(by_group.items())
            },
        }

    # Cross-tissue fold differences, for the primary group only, computed from
    # the per-library medians under every denominator. An unpaired comparison
    # between different sample sets: reported as a descriptive fold, never as
    # an effect.
    folds = {}
    labels = list(tissues)
    if len(labels) == 2 and args.group:
        a, b = labels
        for field in DENOMINATORS:
            try:
                va = tissues[a]["by_group"][args.group]["per_million"][field][
                    "per_library_ratios"]["median"]
                vb = tissues[b]["by_group"][args.group]["per_million"][field][
                    "per_library_ratios"]["median"]
            except (KeyError, TypeError):
                continue
            if vb > 0:
                folds[field] = {
                    f"{a}_per_million": va,
                    f"{b}_per_million": vb,
                    "fold": round(va / vb, 2),
                }

    return {
        "generated": "2026-11-11",
        "junction": args.junction,
        "group_for_fold": args.group,
        "method": (
            "per-library ratio = count / (that library's depth / 1e6); the "
            "group figure is the MEDIAN OF THOSE RATIOS. The ratio of medians "
            "is reported alongside only to show what the withdrawn figures did."),
        "denominator_fields": list(DENOMINATORS),
        "primary_denominator": PRIMARY,
        "primary_denominator_note": (
            "exon_fc_count_all.total is the reads SUBMITTED to featureCounts, "
            "not the reads assigned to exons. The report must not call it the "
            "latter."),
        "withdrawn_figures": {
            "2.30 / 0.11 per million": "ratio of medians against a single 44.4 M applied to both tissues",
            "2.530 / 0.113 per million (22.3x)": "arithmetically correct against exon_fc_count_all.total per library, but published with no deposited procedure and with the denominator named wrongly; superseded by this script",
        },
        "unpaired": (
            "Different sample sets, no donor pairing used here, unmeasured "
            "confounders. Folds are descriptive, not effects."),
        "tissues": tissues,
        "cross_tissue_fold": folds,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tissue", action="append", required=True,
                    metavar="LABEL:RESULTS_JSON:QC_MD_GZ")
    ap.add_argument("--junction", default="canonical")
    ap.add_argument("--group", default="ALS Spectrum MND")
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
