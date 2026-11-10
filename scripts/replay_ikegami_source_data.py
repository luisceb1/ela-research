#!/usr/bin/env python3
"""Descriptive replay of the Ikegami/Koike 2026 deposited source data.

Reproduces the published statistics of
Acta Neuropathol Commun 14:229, DOI 10.1186/s40478-026-02400-0
from Additional file 3 (Source Data), per the prespecified plan in
research/plans/2026-11-10-ikegami-source-data-replay.md.

This is internal reproducibility only: the same subjects and the same
measurements. It is NOT independent replication, NOT biological validation and
carries NO junction counts, so it does not advance issue #37.

The source workbook is not redistributed; only its SHA256 and derived
statistics are recorded.

Usage:
  python -I scripts/replay_ikegami_source_data.py SOURCE_DATA.xlsx [--json OUT]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
from openpyxl import load_workbook
from scipy import stats

SUBTYPES = ("ALS Type 1", "ALS Type 2a", "ALS Type 2b")


def nbsp(text: str) -> str:
    """Sheet headers use non-breaking spaces; normalise before matching."""
    return " ".join(str(text).replace("\xa0", " ").split())


def sheet_columns(workbook, name: str) -> dict[str, list[float]]:
    ws = workbook[name]
    rows = list(ws.iter_rows(values_only=True))
    headers = [nbsp(h) if h is not None else "" for h in rows[0]]
    out: dict[str, list[float]] = {h: [] for h in headers}
    for row in rows[1:]:
        for header, value in zip(headers, row):
            if isinstance(value, (int, float)):
                out[header].append(float(value))
    return out


def paired(workbook, name: str) -> tuple[list[float], list[float], list[str]]:
    """Read a paired sheet: column 0 is x; the remaining columns are y by subtype."""
    ws = workbook[name]
    rows = list(ws.iter_rows(values_only=True))
    headers = [nbsp(h) if h is not None else "" for h in rows[0]]
    xs: list[float] = []
    ys: list[float] = []
    groups: list[str] = []
    for row in rows[1:]:
        x = row[0]
        if not isinstance(x, (int, float)):
            continue
        for idx in range(1, len(headers)):
            y = row[idx] if idx < len(row) else None
            if isinstance(y, (int, float)):
                xs.append(float(x))
                ys.append(float(y))
                groups.append(headers[idx])
    return xs, ys, groups


def dunn_holm(groups: list[list[float]], labels: list[str]) -> list[dict]:
    """Dunn's post-hoc test on pooled mid-ranks, Holm-adjusted.

    Prism applies its own multiplicity correction; the published paper reports
    'Dunn's multiple comparisons correction' without naming the family method,
    so the adjustment here may differ from theirs. Treat the unadjusted z and
    the direction as the comparable quantities.
    """
    pooled = np.concatenate([np.asarray(g, dtype=float) for g in groups])
    ranks = stats.rankdata(pooled)
    sizes = [len(g) for g in groups]
    starts = np.cumsum([0] + sizes)
    mean_ranks = [float(ranks[starts[i]:starts[i + 1]].mean()) for i in range(len(groups))]
    total = len(pooled)
    # Tie correction for the variance of the rank sums.
    _, counts = np.unique(pooled, return_counts=True)
    ties = float(((counts ** 3) - counts).sum())
    raw = []
    for i, j in combinations(range(len(groups)), 2):
        sigma = np.sqrt(
            (total * (total + 1) / 12.0 - ties / (12.0 * (total - 1)))
            * (1.0 / sizes[i] + 1.0 / sizes[j])
        )
        z = (mean_ranks[i] - mean_ranks[j]) / sigma
        raw.append({"a": labels[i], "b": labels[j], "z": float(z),
                    "p_unadjusted": float(2 * stats.norm.sf(abs(z)))})
    order = sorted(range(len(raw)), key=lambda k: raw[k]["p_unadjusted"])
    m = len(raw)
    running = 0.0
    for rank, k in enumerate(order):
        adj = min(1.0, (m - rank) * raw[k]["p_unadjusted"])
        running = max(running, adj)
        raw[k]["p_holm"] = running
    return raw


def leave_one_out_spearman(xs: list[float], ys: list[float]) -> dict:
    rhos = []
    for drop in range(len(xs)):
        kx = [v for i, v in enumerate(xs) if i != drop]
        ky = [v for i, v in enumerate(ys) if i != drop]
        rhos.append(float(stats.spearmanr(kx, ky).statistic))
    return {"min": min(rhos), "max": max(rhos), "n": len(rhos)}


def permutation_control(groups: list[list[float]], seed: int, iterations: int = 2000) -> dict:
    """Negative control: shuffling subtype labels must destroy the difference."""
    rng = np.random.default_rng(seed)
    pooled = np.concatenate([np.asarray(g, dtype=float) for g in groups])
    sizes = [len(g) for g in groups]
    observed = float(stats.kruskal(*groups).statistic)
    worse = 0
    for _ in range(iterations):
        rng.shuffle(pooled)
        starts = np.cumsum([0] + sizes)
        parts = [pooled[starts[i]:starts[i + 1]] for i in range(len(sizes))]
        if float(stats.kruskal(*parts).statistic) >= observed:
            worse += 1
    return {"observed_H": observed, "iterations": iterations,
            "p_permutation": (worse + 1) / (iterations + 1), "seed": seed}


def run(path: Path) -> dict:
    data = path.read_bytes()
    wb = load_workbook(path, data_only=True)
    out: dict = {
        "source_file": path.name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "versions": {"numpy": np.__version__, "scipy": stats.__name__ and __import__("scipy").__version__},
        "sheets": wb.sheetnames,
    }

    # R3: declared group sizes.
    unc13a = sheet_columns(wb, "Fig. 2a")
    stmn2 = sheet_columns(wb, "Fig. 2b")
    out["R3_group_sizes"] = {
        "UNC13A_cryptic_qRT_PCR": {nbsp(k): len(v) for k, v in unc13a.items()},
        "truncated_STMN2_qRT_PCR": {nbsp(k): len(v) for k, v in stmn2.items()},
        "published": {"ALS Type 1": 12, "ALS Type 2a": 12, "ALS Type 2b": 11},
    }

    # R1: Spearman between the two measures, paired per case (Fig. 2c).
    xs, ys, groups = paired(wb, "Fig. 2c")
    rho = stats.spearmanr(xs, ys)
    out["R1_spearman_unc13a_vs_stmn2"] = {
        "n_pairs": len(xs),
        "rho": float(rho.statistic),
        "p_value": float(rho.pvalue),
        "published_rho": 0.58,
        "delta_vs_published": float(rho.statistic) - 0.58,
        "tie_handling": "scipy.stats.spearmanr, average ranks",
        "leave_one_out": leave_one_out_spearman(xs, ys),
        "pairs_per_subtype": {s: groups.count(next(g for g in set(groups) if s in g))
                              for s in SUBTYPES if any(s in g for g in groups)},
    }

    # R2: subtype differences for both measures.
    out["R2_subtype_differences"] = {}
    for label, cols in (("UNC13A_cryptic_qRT_PCR", unc13a),
                        ("truncated_STMN2_qRT_PCR", stmn2)):
        keys = [k for k in cols if nbsp(k) in SUBTYPES]
        keys.sort(key=lambda k: SUBTYPES.index(nbsp(k)))
        series = [cols[k] for k in keys]
        kw = stats.kruskal(*series)
        out["R2_subtype_differences"][label] = {
            "kruskal_H": float(kw.statistic),
            "kruskal_p": float(kw.pvalue),
            "medians": {nbsp(k): float(np.median(cols[k])) for k in keys},
            "dunn_holm": dunn_holm(series, [nbsp(k) for k in keys]),
            "permutation_control": permutation_control(series, seed=20261110),
        }

    # R4: ddPCR versus qRT-PCR concordance (Fig. S5e/S5f).
    out["R4_ddpcr_concordance"] = {}
    for sheet, name in (("Fig. S5e", "UNC13A_cryptic"),
                        ("Fig. S5f", "truncated_STMN2")):
        if sheet not in wb.sheetnames:
            continue
        dx, dy, _ = paired(wb, sheet)
        r = stats.spearmanr(dx, dy)
        out["R4_ddpcr_concordance"][name] = {
            "sheet": sheet, "n_pairs": len(dx),
            "spearman_rho": float(r.statistic), "p_value": float(r.pvalue),
            "published_claim": "strong correlations (no coefficient stated in the abstract)",
        }

    # Alternative explanation the paper says does not account for the pattern.
    out["alternative_disease_duration"] = {}
    for sheet, name in (("Fig. S3a", "UNC13A_cryptic"),
                        ("Fig. S3b", "truncated_STMN2")):
        if sheet not in wb.sheetnames:
            continue
        ax, ay, _ = paired(wb, sheet)
        r = stats.spearmanr(ax, ay)
        out["alternative_disease_duration"][name] = {
            "sheet": sheet, "n_pairs": len(ax),
            "spearman_rho": float(r.statistic), "p_value": float(r.pvalue),
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
