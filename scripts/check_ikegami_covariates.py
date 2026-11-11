#!/usr/bin/env python3
"""Test the confounders Ikegami/Koike 2026 says do not explain their subtype effect.

Per the addendum of research/plans/2026-11-10-ikegami-source-data-replay.md.

The figure sheets carry no case identifier, so a per-case join to the measures
would rest on row position, which the plan forbids. This script therefore asks
the question that needs no join: do the covariates themselves differ between
pathological subtypes? A covariate that does not differ cannot explain a
difference between those subtypes.

It also reports whether disease duration would serve as a unique join key per
subtype, which is a provenance finding, not an inference.

Usage:
  python -I scripts/check_ikegami_covariates.py TABLES.xlsx [--json OUT]
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np
from openpyxl import load_workbook
from scipy import stats

SUBTYPES = ("Type 1", "Type 2a", "Type 2b")
# Column index in Table S1 -> covariate name. Header row is row index 1.
COVARIATES = {
    2: "age_at_death_years",
    3: "age_at_onset_years",
    4: "disease_duration_months",
    6: "postmortem_interval_hours",
    11: "RIN",
}


def numeric(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip()
        if text in {"", "-", "NA", "n.a.", "ND"}:
            return None
        try:
            return float(text)
        except ValueError:
            return None
    return None


def read_table_s1(wb) -> list[dict]:
    rows = list(wb["Table S1"].iter_rows(values_only=True))
    cases = []
    for row in rows[2:]:
        name = row[0]
        if not isinstance(name, str) or not name.strip().startswith("ALS"):
            continue
        subtype = str(row[7]).strip() if row[7] is not None else ""
        if subtype not in SUBTYPES:
            continue
        case = {"case": name.strip(), "subtype": subtype}
        for idx, label in COVARIATES.items():
            case[label] = numeric(row[idx] if idx < len(row) else None)
        cases.append(case)
    return cases


def read_neuronal_loss(wb) -> dict[str, float]:
    if "Table S2" not in wb.sheetnames:
        return {}
    out = {}
    for row in list(wb["Table S2"].iter_rows(values_only=True))[2:]:
        name = row[0]
        if isinstance(name, str) and name.strip().startswith("ALS"):
            score = numeric(row[2] if len(row) > 2 else None)
            if score is not None:
                out[name.strip()] = score
    return out


def compare(groups: dict[str, list[float]]) -> dict:
    present = {k: v for k, v in groups.items() if len(v) >= 3}
    if len(present) < 2:
        return {"status": "insufficient_data",
                "n_by_subtype": {k: len(v) for k, v in groups.items()}}
    series = [present[k] for k in SUBTYPES if k in present]
    labels = [k for k in SUBTYPES if k in present]
    kw = stats.kruskal(*series)
    pairs = []
    for i, j in combinations(range(len(series)), 2):
        u = stats.mannwhitneyu(series[i], series[j], alternative="two-sided")
        pairs.append({"a": labels[i], "b": labels[j],
                      "mannwhitney_u": float(u.statistic),
                      "p_unadjusted": float(u.pvalue)})
    return {
        "status": "tested",
        "n_by_subtype": {k: len(v) for k, v in present.items()},
        "medians": {k: float(np.median(v)) for k, v in present.items()},
        "kruskal_H": float(kw.statistic),
        "kruskal_p": float(kw.pvalue),
        "differs_at_0_05": bool(kw.pvalue < 0.05),
        "pairwise_unadjusted": pairs,
    }


def join_key_uniqueness(cases: list[dict]) -> dict:
    """Would disease duration uniquely identify a case within its subtype?"""
    out = {}
    for subtype in SUBTYPES:
        values = [c["disease_duration_months"] for c in cases
                  if c["subtype"] == subtype and c["disease_duration_months"] is not None]
        counts = Counter(values)
        duplicates = {str(v): n for v, n in counts.items() if n > 1}
        out[subtype] = {"n": len(values), "unique": not duplicates,
                        "duplicated_values": duplicates}
    return out


def run(path: Path) -> dict:
    data = path.read_bytes()
    wb = load_workbook(path, data_only=True)
    cases = read_table_s1(wb)
    losses = read_neuronal_loss(wb)
    for case in cases:
        case["neuronal_loss_score"] = losses.get(case["case"])

    covariates = list(COVARIATES.values()) + ["neuronal_loss_score"]
    results = {}
    for name in covariates:
        groups = {s: [c[name] for c in cases
                      if c["subtype"] == s and c.get(name) is not None]
                  for s in SUBTYPES}
        results[name] = compare(groups)

    # Six covariates are screened at once, so the family must be corrected
    # before any single nominal p is called a difference.
    tested = [(name, res["kruskal_p"]) for name, res in results.items()
              if res["status"] == "tested"]
    order = sorted(range(len(tested)), key=lambda k: tested[k][1])
    m = len(tested)
    running = 0.0
    for rank, k in enumerate(order):
        name, p = tested[k]
        running = max(running, min(1.0, (m - rank) * p))
        results[name]["kruskal_p_holm"] = running
        results[name]["differs_after_holm"] = bool(running < 0.05)

    out = {
        "source_file": path.name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "versions": {"numpy": np.__version__,
                     "scipy": __import__("scipy").__version__},
        "n_cases": len(cases),
        "cases_by_subtype": dict(Counter(c["subtype"] for c in cases)),
        "neuronal_loss_scores_matched": sum(
            1 for c in cases if c["neuronal_loss_score"] is not None),
        "covariate_tests": results,
        "join_key_uniqueness_disease_duration": join_key_uniqueness(cases),
        "note": ("A covariate that does not differ between subtypes cannot "
                 "explain a difference between those subtypes. Per-case "
                 "correlation with the measures is not computed: the figure "
                 "sheets carry no case identifier and the plan forbids joining "
                 "by row position."),
    }
    wb.close()
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("workbook", type=Path)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args(argv)
    out = run(args.workbook)
    text = json.dumps(out, ensure_ascii=False, indent=1)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
