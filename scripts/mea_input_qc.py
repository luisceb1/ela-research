"""Structural preflight for this SYNTHETIC MEA prototype, not a real-data importer.

No effect estimates, classification, statistical inference or file I/O. Thresholds
for biological eligibility cannot be established by this validator.
"""
from collections import defaultdict
import math

REQUIRED = {"scenario", "differentiation_id", "well_id", "arm", "time_index",
            "synchrony", "viability", "qc_ok", "status", "t0_index"}
ARMS = {"sham", "early_reference", "late_ASO", "damage_control", "screen_fail", "unpaired_not_randomized"}
RANDOMIZED = {"late_ASO", "damage_control"}
STATUSES = {"observed", "technical_missing", "dead"}


def missing(value):
    return value is None or (isinstance(value, (float, int)) and math.isnan(value))


def number(value, name, *, integer=False):
    try:
        v = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"{name}: numeric value required") from None
    if not math.isfinite(v) or (integer and v != int(v)):
        raise ValueError(f"{name}: finite {'integer' if integer else 'number'} required")
    return int(v) if integer else v


def validate_synthetic_rows(rows, *, provenance):
    if provenance != "synthetic":
        raise ValueError("Only explicitly synthetic fixtures are supported; real-data workflow not validated")
    if not rows:
        raise ValueError("Empty fixture")
    wells, blocks, sham = defaultdict(list), defaultdict(set), defaultdict(list)
    seen = set()
    for original in rows:
        if REQUIRED.difference(original):
            raise ValueError("Required fields missing")
        row = dict(original)
        if any(not isinstance(row[k], str) or not row[k].strip() for k in ("scenario", "differentiation_id", "well_id")):
            raise ValueError("Empty or invalid identifier")
        if row["arm"] not in ARMS or row["status"] not in STATUSES:
            raise ValueError("Invalid arm or status")
        t = row["time_index"] = number(row["time_index"], "time_index", integer=True)
        if t < 0:
            raise ValueError("Negative time_index")
        viab = row["viability"] = number(row["viability"], "viability")
        qc = row["qc_ok"] = number(row["qc_ok"], "qc_ok", integer=True)
        if not 0 <= viab <= 1 or qc not in {0, 1}:
            raise ValueError("viability or qc_ok outside prototype domain")
        if row["status"] == "observed":
            y = row["synchrony"] = number(row["synchrony"], "synchrony")
            if not 0 <= y <= 1 or qc != 1:
                raise ValueError("Observed row needs valid normalized synchrony and QC")
        elif not missing(row["synchrony"]) or qc != 0:
            raise ValueError("Non-observed row needs missing synchrony and qc_ok=0")
        if row["status"] == "dead" and viab != 0:
            raise ValueError("Death requires viability=0")
        if row["arm"] in RANDOMIZED:
            row["t0_index"] = number(row["t0_index"], "t0_index", integer=True)
            if row["t0_index"] <= 2:
                raise ValueError("T0 must follow all three baseline indices")
        key = (row["scenario"], row["well_id"], t)
        if key in seen:
            raise ValueError("Duplicate well x time")
        seen.add(key)
        wells[key[:2]].append(row)
        block = (row["scenario"], row["differentiation_id"])
        if row["arm"] in RANDOMIZED:
            blocks[block].add(row["arm"])
        if row["arm"] == "sham" and row["status"] == "observed":
            sham[block + (t,)].append(row["synchrony"])
    if not blocks:
        raise ValueError("No randomized blocks")
    randomized_rows = []
    for group in wells.values():
        if len({(r["arm"], r["differentiation_id"]) for r in group}) != 1:
            raise ValueError("Arm or differentiation changes within well")
        by_time = {r["time_index"]: r for r in group}
        if any(t not in by_time or by_time[t]["status"] != "observed" for t in (0, 1, 2)):
            raise ValueError("Three valid observed baseline records required by this prototype")
        dead = False
        for r in sorted(group, key=lambda x: x["time_index"]):
            if dead and r["status"] != "dead":
                raise ValueError("Death is absorbing; later status cannot revive a well")
            dead |= r["status"] == "dead"
            if not sham[(r["scenario"], r["differentiation_id"], r["time_index"])]:
                raise ValueError("Missing valid same-block sham at a required time")
        if group[0]["arm"] not in RANDOMIZED:
            continue
        if len({r["t0_index"] for r in group}) != 1:
            raise ValueError("T0 changes within well")
        t0 = group[0]["t0_index"]
        if any(t not in by_time or by_time[t]["status"] != "observed" for t in (t0 - 1, t0)):
            raise ValueError("Two valid screening records required at T0-1 and T0")
        if any(t not in by_time for t in (t0 + 3, t0 + 4)):
            raise ValueError("Explicit follow-up rows required, including missing/dead status")
        randomized_rows.extend(group)
    for block, arms in blocks.items():
        if arms != RANDOMIZED:
            raise ValueError("Each analyzed block requires both randomized arms")
        for arm in RANDOMIZED:
            for follow in (3, 4):
                support = [r for r in randomized_rows if (r["scenario"], r["differentiation_id"]) == block
                           and r["arm"] == arm and r["time_index"] == r["t0_index"] + follow
                           and r["status"] in {"observed", "dead"}]
                if not support:
                    raise ValueError("Entire arm x block x endpoint has technical missingness; summary not supported")
    return {"status": "synthetic_structural_qc_only", "rows": len(rows), "wells": len(wells),
            "randomized_blocks": len(blocks), "biological_eligibility_verified": False,
            "experimental_analysis_validated": False}
