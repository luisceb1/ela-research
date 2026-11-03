"""Gate only for K26 Fig4d. Never estimates rescue or verifies biology from IDs."""
import argparse
import csv
import hashlib
import io
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


FIELDS = {
    "line_id", "clone_id", "differentiation_id", "culture_id", "coverslip_id",
    "cell_id", "condition", "value", "unit", "included", "exclusion_reason",
    "record_day", "first_ASO_day", "KD_start_day", "source_row",
}
CONDITIONS = {"control", "KD", "KD_ASO"}


class _InputRejected(Exception):
    """Expected input rejection; args[0] retains the original JSON reason."""


def _validate_contract(contract):
    """Check provenance and the fixed study contract before opening a file."""
    if not isinstance(contract, dict):
        raise _InputRejected("Contract must be a JSON object")
    if contract.get("schema_version") != "FR-K26-4d-v1":
        raise _InputRejected("Unrecognized contract version")
    if contract.get("enabled") is not True:
        raise _InputRejected(contract.get("disabled_reason", "Contract disabled"))
    review = contract.get("independence_review", {})
    if not isinstance(review, dict):
        raise _InputRejected("Independence review must be a JSON object")
    if (review.get("approved") is not True or
            not str(review.get("reviewer") or "").strip() or
            not str(review.get("evidence") or "").strip()):
        raise _InputRejected("Biological independence requires a documented human review")
    for field in ("data_file", "data_sha256", "source_url", "source_version"):
        if not str(contract.get(field) or "").strip():
            raise _InputRejected("Missing provenance: " + field)
    if (contract.get("study_version") != "K26-accepted-2026-10-06" or
            contract.get("panel") != "Fig4d" or
            contract.get("unit") != "pA_magnitude" or
            contract.get("expected_included_cells") != {"control": 34, "KD": 30, "KD_ASO": 25} or
            contract.get("minimum_independent_differentiations") != 3):
        raise _InputRejected("Design changed: amend plan and contract before analysis")


def _read_source(contract, contract_dir):
    path = Path(contract["data_file"])
    if not path.is_absolute():
        path = Path(contract_dir) / path
    if not path.is_file():
        raise _InputRejected("Original data file not available")
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != contract["data_sha256"]:
        raise _InputRejected("SHA256 mismatch")
    try:
        # Parse the exact immutable bytes verified above, even if the path changes.
        with io.StringIO(data.decode("utf-8-sig"), newline="") as handle:
            reader = csv.DictReader(handle)
            headers = reader.fieldnames or []
            if len(headers) != len(set(headers)):
                raise _InputRejected("Duplicate CSV column names")
            if not FIELDS.issubset(set(headers)):
                raise _InputRejected("Missing required columns")
            rows = list(reader)
    except (OSError, UnicodeError, csv.Error) as error:
        raise _InputRejected("Cannot parse original CSV: " + str(error))
    if not rows:
        raise _InputRejected("Empty table")
    return digest, rows


def _validate_cell_metadata(row, index):
    if None in row:
        raise _InputRejected("CSV row has more fields than its header")
    required = FIELDS - {"exclusion_reason", "first_ASO_day", "KD_start_day"}
    if row.get("included") == "false":
        required -= {"value", "record_day"}
    if any(not str(row.get(key) or "").strip() for key in required):
        raise _InputRejected("Missing cell metadata at CSV line " + str(index))
    if row["condition"] not in CONDITIONS or row["included"] not in {"true", "false"}:
        raise _InputRejected("Unknown condition/inclusion flag")
    if row["unit"] != "pA_magnitude":
        raise _InputRejected("Unit/polarity unresolved; do not silently take abs or rescale")


def _validate_recording(row):
    """Validate inclusion, amplitude and timing; return whether the cell is included."""
    # Failed recordings can have no amplitude or recording day. Retain their
    # identities/reasons, but never invent measurements to pass the gate.
    if row["included"] == "false":
        if not row["exclusion_reason"].strip():
            raise _InputRejected("Excluded cell without reason")
        return False
    if row["exclusion_reason"].strip():
        raise _InputRejected("Included cell has exclusion reason")
    try:
        value, record = float(row["value"]), float(row["record_day"])
        if not math.isfinite(value) or value < 0 or not math.isfinite(record):
            raise _InputRejected("Nonfinite or negative amplitude / nonfinite time")
        if not 60 <= record <= 70:
            raise _InputRejected("Recording day differs from published DIV60-70 window")
        # Raw sign must already be resolved and documented in source_version/review.
        if row["condition"] != "control":
            kd = float(row["KD_start_day"])
            if kd != 45 or record <= kd:
                raise _InputRejected("KD timing differs from selected experiment")
        if row["condition"] == "KD_ASO":
            if float(row["first_ASO_day"]) != 45:
                raise _InputRejected("ASO timing differs from concurrent Fig4d design")
        elif row["first_ASO_day"].strip():
            raise _InputRejected("Unexpected active ASO in reference arm")
        if row["condition"] == "control" and row["KD_start_day"].strip():
            raise _InputRejected("Unexpected KD in healthy control")
    except (ValueError, TypeError):
        raise _InputRejected("Unparseable amplitude or timing")
    return True


def _validate_cells(rows):
    counts = Counter()
    blocks = defaultdict(set)
    seen_cells, seen_source_rows = set(), set()
    culture_map, coverslip_map = {}, {}
    excluded = 0
    for index, row in enumerate(rows, 2):
        _validate_cell_metadata(row, index)
        # IDs must be globally scoped by the reviewed source map, not guessed suffixes.
        cell_key = (row["differentiation_id"], row["culture_id"], row["coverslip_id"], row["cell_id"])
        if cell_key in seen_cells or row["source_row"] in seen_source_rows:
            raise _InputRejected("Duplicate cell or source row; repeated measures are not independent cells")
        seen_cells.add(cell_key)
        seen_source_rows.add(row["source_row"])
        parent = (row["line_id"], row["clone_id"], row["differentiation_id"])
        culture = row["culture_id"]
        coverslip = row["coverslip_id"]
        if culture in culture_map and culture_map[culture] != parent:
            raise _InputRejected("Culture assigned to conflicting differentiation/line")
        culture_map[culture] = parent
        slip_parent = (parent, culture, row["condition"])
        if coverslip in coverslip_map and coverslip_map[coverslip] != slip_parent:
            raise _InputRejected("Coverslip assigned to conflicting parent or treatment")
        coverslip_map[coverslip] = slip_parent
        if not _validate_recording(row):
            excluded += 1
            continue
        counts[row["condition"]] += 1
        blocks[parent].add(row["condition"])
    return counts, blocks, excluded


def _validate_design(contract, counts, blocks):
    if dict(counts) != contract["expected_included_cells"]:
        raise _InputRejected("Cell counts differ from publication; reconcile before analysis")
    # A differentiation key cannot silently join different lines or clones.
    differentiation_ids = [key[2] for key in blocks]
    if len(differentiation_ids) != len(set(differentiation_ids)):
        raise _InputRejected("Differentiation ID has conflicting line/clone")
    if len(blocks) < 3 or any(groups != CONDITIONS for groups in blocks.values()):
        raise _InputRejected("Incomplete biological blocks; revise design without imputation")


def check_contract(contract, contract_dir):
    """Validate an explicitly reviewed original table. No statistical analysis."""
    try:
        _validate_contract(contract)
        digest, rows = _read_source(contract, contract_dir)
        counts, blocks, excluded = _validate_cells(rows)
        _validate_design(contract, counts, blocks)
    except _InputRejected as error:
        return {"status": "blocked", "reason": error.args[0], "effect_estimated": False}
    return {
        "status": "input_ready_for_design_review", "effect_estimated": False,
        "sha256": digest, "included_cell_counts": dict(sorted(counts.items())),
        "differentiations": len(blocks), "excluded_cells": excluded,
        "warning": "IDs do not prove independence; no model fit, efficacy or equivalence established",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
        result = check_contract(contract, args.contract.parent)
    except (OSError, ValueError, TypeError) as error:
        result = {"status": "blocked", "reason": "Invalid contract: " + str(error), "effect_estimated": False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "input_ready_for_design_review" else 2


if __name__ == "__main__":
    raise SystemExit(main())


