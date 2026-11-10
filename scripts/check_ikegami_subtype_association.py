#!/usr/bin/env python3
"""Exploratory paired-marker association conditional on pathological subtype.

Only Fig. 2c is read. No cross-sheet joins or redistributed source observations.
See research/plans/2026-11-10-ikegami-subtype-conditioning.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np
import openpyxl
import scipy
from scipy.stats import rankdata

SOURCE_SHA256 = "d72b8ebc18c1b71be8bc4c26ffde1edd6f5da65541a7711c686073f4a36ad385"
GROUPS = ("ALS Type 1", "ALS Type 2a", "ALS Type 2b")
PROTOCOL_COMMIT = "88fc61f998e5ec77791e76ffdbbd9fccd20a9138"


def numeric(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def read_pairs(ws):
    """Use explicit x/y pairing in the deposited scatter-plot sheet only."""
    rows = list(ws.iter_rows(values_only=True))
    headers = [" ".join(str(h or "").replace("\xa0", " ").split()) for h in rows[0]]
    columns = {}
    for col, header in enumerate(headers[1:], 1):
        matched = [g for g in GROUPS if header == g or header.endswith((" " + g, "_" + g))]
        if len(matched) != 1 or matched[0] in columns.values():
            raise ValueError(f"Ambiguous subtype header in column {col + 1}: {header!r}")
        columns[col] = matched[0]
    if set(columns.values()) != set(GROUPS):
        raise ValueError("Expected exactly three subtype columns")
    xs, ys, groups, cells = [], [], [], []
    empty_rows = 0
    for rownum, row in enumerate(rows[1:], 2):
        if all(v is None for v in row):
            empty_rows += 1
            continue
        if not numeric(row[0]) or not math.isfinite(row[0]):
            raise ValueError(f"Missing/nonfinite x at row {rownum}")
        found = 0
        for col, group in columns.items():
            value = row[col] if col < len(row) else None
            if value is None:
                continue
            if not numeric(value) or not math.isfinite(value):
                raise ValueError(f"Nonnumeric/nonfinite y at row {rownum}, column {col + 1}")
            found += 1
            xs.append(float(row[0])); ys.append(float(value)); groups.append(group)
            cells.append([f"A{rownum}", f"{openpyxl.utils.get_column_letter(col+1)}{rownum}"])
        if not found:
            raise ValueError(f"Unpaired x at row {rownum}")
    return np.asarray(xs), np.asarray(ys), np.asarray(groups), {
        "sheet": ws.title, "headers": headers, "pair_cells": cells,
        "empty_rows": empty_rows, "incomplete_pairs": 0,
    }


def validate(x, y, groups):
    x, y, groups = np.asarray(x, dtype=float), np.asarray(y, dtype=float), np.asarray(groups)
    if x.ndim != 1 or x.shape != y.shape or x.shape != groups.shape or len(x) < 3:
        raise ValueError("Expected equally sized one-dimensional paired arrays")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("Nonfinite observations")
    if any(np.count_nonzero(groups == g) < 2 for g in np.unique(groups)):
        raise ValueError("Each subtype needs at least two pairs")
    return x, y, groups


def corr_rows(x, y):
    """Pearson for final-axis rows; undefined constant rows remain NaN."""
    x = x - np.mean(x, axis=-1, keepdims=True)
    y = y - np.mean(y, axis=-1, keepdims=True)
    denominator = np.sqrt(np.sum(x*x, axis=-1) * np.sum(y*y, axis=-1))
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.sum(x*y, axis=-1) / denominator


def residual_ranks(x, y, groups):
    rx = rankdata(x, axis=-1, method="average")
    ry = rankdata(y, axis=-1, method="average")
    for group in np.unique(groups):
        idx = np.flatnonzero(groups == group)
        rx[..., idx] -= rx[..., idx].mean(axis=-1, keepdims=True)
        ry[..., idx] -= ry[..., idx].mean(axis=-1, keepdims=True)
    return rx, ry


def adjusted_rho(x, y, groups):
    x, y, groups = validate(x, y, groups)
    rx, ry = residual_ranks(x, y, groups)
    return float(corr_rows(rx, ry))


def permutation_test(x, y, groups, iterations=99999, seed=20261110):
    x, y, groups = validate(x, y, groups)
    if iterations < 1:
        raise ValueError("Positive permutation count required")
    rx, ry = residual_ranks(x, y, groups)
    observed = float(corr_rows(rx, ry))
    if not math.isfinite(observed):
        raise ValueError("Primary coefficient undefined")
    rng = np.random.default_rng(seed)
    indices = [np.flatnonzero(groups == g) for g in np.unique(groups)]
    extreme = 0
    denominator = float(np.linalg.norm(rx) * np.linalg.norm(ry))
    for _ in range(iterations):
        permuted = ry.copy()
        for idx in indices:
            permuted[idx] = rng.permutation(ry[idx])
        statistic = float(np.dot(rx, permuted) / denominator)
        if abs(statistic) >= abs(observed) - 1e-12:
            extreme += 1
    p = (extreme + 1) / (iterations + 1)
    return {"rho": observed, "p_two_sided": p, "extreme": extreme,
            "iterations": iterations, "seed": seed,
            "monte_carlo_se": float(np.sqrt(p * (1-p) / (iterations + 1)))}


def coefficients(x, y, groups):
    result = {"pooled": corr_rows(rankdata(x, axis=-1), rankdata(y, axis=-1))}
    rx, ry = residual_ranks(x, y, groups)
    result["adjusted"] = corr_rows(rx, ry)
    for group in np.unique(groups):
        mask = groups == group
        result[group] = corr_rows(rankdata(x[..., mask], axis=-1), rankdata(y[..., mask], axis=-1))
    keep = groups != "ALS Type 2b"
    result["pooled_without_2b"] = corr_rows(rankdata(x[..., keep], axis=-1), rankdata(y[..., keep], axis=-1))
    rx, ry = residual_ranks(x[..., keep], y[..., keep], groups[keep])
    result["adjusted_without_2b"] = corr_rows(rx, ry)
    return result


def bootstrap(x, y, groups, iterations=10000, seed=20261111):
    x, y, groups = validate(x, y, groups)
    if iterations < 1:
        raise ValueError("Positive bootstrap count required")
    rng = np.random.default_rng(seed)
    indices = np.tile(np.arange(len(x)), (iterations, 1))
    for group in np.unique(groups):
        idx = np.flatnonzero(groups == group)
        indices[:, idx] = rng.choice(idx, size=(iterations, len(idx)), replace=True)
    sampled = coefficients(x[indices], y[indices], groups)
    out = {}
    for name, values in sampled.items():
        valid = np.isfinite(values)
        undefined = int((~valid).sum())
        ci = np.quantile(values[valid], [.025, .975]).tolist() if undefined <= iterations * .01 else None
        out[name] = {"ci95_percentile": ci, "undefined_replicates": undefined}
    return {"iterations": iterations, "seed": seed, "estimates": out}


def run(path, source_url):
    data = Path(path).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError(f"Source SHA256 mismatch: {digest}")
    wb = openpyxl.load_workbook(path, data_only=True)
    try:
        x, y, groups, inventory = read_pairs(wb["Fig. 2c"])
    finally:
        wb.close()
    x, y, groups = validate(x, y, groups)
    counts = {g: int(np.count_nonzero(groups == g)) for g in GROUPS}
    if list(counts.values()) != [12, 12, 11]:
        raise ValueError(f"Unexpected group sizes: {counts}")
    estimates = {k: float(v) for k, v in coefficients(x, y, groups).items()}
    if abs(estimates["pooled"] - 0.5736694677871148) > 1e-10:
        raise ValueError("Pooled rho does not reproduce the prior source replay")
    primary = permutation_test(x, y, groups)
    uncertainty = bootstrap(x, y, groups)
    loo = [adjusted_rho(np.delete(x,i), np.delete(y,i), np.delete(groups,i)) for i in range(len(x))]
    return {
        "evidence": "exploratory internal observational reanalysis; no independent replication",
        "protocol_commit": PROTOCOL_COMMIT,
        "source": {"url": source_url, "sha256": digest, "bytes": len(data), "inventory": inventory},
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "scipy": scipy.__version__, "openpyxl": openpyxl.__version__},
        "group_sizes": counts, "estimates": estimates,
        "primary_permutation": primary, "bootstrap": uncertainty,
        "adjusted_minus_pooled": estimates["adjusted"] - estimates["pooled"],
        "adjusted_leave_one_out": {"min": min(loo), "max": max(loo), "n": len(loo)},
        "prediction_supported_at_alpha_0_05": primary["rho"] > 0 and primary["p_two_sided"] < .05,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--json", required=True, type=Path)
    args = parser.parse_args()
    result = run(args.workbook, args.source_url)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"estimates": result["estimates"], "primary": result["primary_permutation"]}, indent=2))


if __name__ == "__main__":
    main()
