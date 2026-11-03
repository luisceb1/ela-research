"""Artificial input controls only. No fixture represents experimental evidence."""
import csv
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_functional_rescue_input.py"
SPEC = importlib.util.spec_from_file_location("functional_rescue_gate", SCRIPT)
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class FunctionalInputGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "ARTIFICIAL.csv"
        self.contract = {
            "schema_version": "FR-K26-4d-v1", "enabled": True,
            "data_file": "ARTIFICIAL.csv", "source_url": "fixture://artificial-only",
            "source_version": "artificial non-biological input test",
            "independence_review": {"approved": True, "reviewer": "fixture", "evidence": "artificial control"},
            "study_version": "K26-accepted-2026-10-06", "panel": "Fig4d", "unit": "pA_magnitude",
            "expected_included_cells": {"control": 34, "KD": 30, "KD_ASO": 25},
            "minimum_independent_differentiations": 3,
        }
        self.rows = []
        for condition, size in self.contract["expected_included_cells"].items():
            for i in range(size):
                block = str(i % 3)
                self.rows.append({
                    "line_id": "artificial-line", "clone_id": "artificial-clone",
                    "differentiation_id": block, "culture_id": block + condition,
                    "coverslip_id": block + condition, "cell_id": str(i),
                    "condition": condition, "value": "1", "unit": "pA_magnitude",
                    "included": "true", "exclusion_reason": "", "record_day": "66",
                    "first_ASO_day": "45" if condition == "KD_ASO" else "",
                    "KD_start_day": "45" if condition != "control" else "",
                    "source_row": condition + str(i),
                })

    def run_gate(self):
        with self.path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=sorted(GATE.FIELDS))
            writer.writeheader()
            writer.writerows(self.rows)
        self.contract["data_sha256"] = hashlib.sha256(self.path.read_bytes()).hexdigest()
        return GATE.check_contract(self.contract, self.path.parent)

    def assertBlocked(self):
        self.assertEqual(self.run_gate()["status"], "blocked")

    def test_artificial_complete_blocks_pass_input_only(self):
        result = self.run_gate()
        self.assertEqual(result["status"], "input_ready_for_design_review")
        self.assertEqual(result["differentiations"], 3)
        self.assertFalse(result["effect_estimated"])

    def test_disabled_contract_never_uses_rows(self):
        self.contract["enabled"] = False
        self.assertBlocked()

    def test_hash_corruption_blocks(self):
        self.run_gate()
        self.path.write_text(self.path.read_text() + "\n", encoding="utf-8")
        self.assertEqual(GATE.check_contract(self.contract, self.path.parent)["status"], "blocked")

    def test_missing_independence_review_blocks(self):
        self.contract["independence_review"]["evidence"] = None
        self.assertBlocked()

    def test_duplicate_cell_blocks(self):
        self.rows.append(dict(self.rows[0], source_row="new-source-row"))
        self.assertBlocked()

    def test_technical_cells_do_not_create_differentiations(self):
        for row in self.rows:
            row["differentiation_id"] = "one-only"
        self.assertBlocked()

    def test_missing_biological_arm_blocks(self):
        for row in self.rows:
            if row["condition"] == "KD_ASO" and row["differentiation_id"] == "2":
                row["differentiation_id"] = "1"
                row["culture_id"] = "new-culture"
                row["coverslip_id"] = "new-slip"
        self.assertBlocked()

    def test_signed_negative_currents_are_not_silently_rectified(self):
        self.rows[0]["value"] = "-1"
        self.assertBlocked()

    def test_nonfinite_values_block(self):
        for value in ("NaN", "inf", "-inf"):
            with self.subTest(value=value):
                self.rows[0]["value"] = value
                self.assertBlocked()

    def test_wrong_units_block(self):
        self.rows[0]["unit"] = "nA"
        self.assertBlocked()

    def test_outside_recording_window_blocks(self):
        self.rows[0]["record_day"] = "44"
        self.assertBlocked()

    def test_unexplained_exclusion_blocks(self):
        self.rows[0]["included"] = "false"
        self.assertBlocked()

    def test_unresolved_timing_blocks(self):
        self.rows[-1]["first_ASO_day"] = "unknown"
        self.assertBlocked()

    def test_counts_cannot_be_relaxed_silently(self):
        self.contract["expected_included_cells"]["KD_ASO"] = 24
        self.assertBlocked()

    def test_conflicting_parent_blocks(self):
        self.rows[0]["culture_id"] = self.rows[1]["culture_id"]
        self.assertBlocked()

    def test_failed_recording_retained_without_inventing_measurement(self):
        self.rows.append(dict(self.rows[0], cell_id="failed-cell", source_row="failed-row",
                              included="false", exclusion_reason="recording_failed",
                              value="", record_day=""))
        result = self.run_gate()
        self.assertEqual(result["status"], "input_ready_for_design_review")
        self.assertEqual(result["excluded_cells"], 1)
        self.assertEqual(sum(result["included_cell_counts"].values()), 89)
        self.assertFalse(result["effect_estimated"])

    def test_non_object_contract_blocks(self):
        self.assertEqual(GATE.check_contract([], self.path.parent)["status"], "blocked")

    def test_non_object_independence_review_blocks(self):
        self.contract["independence_review"] = []
        self.assertBlocked()

    def test_ragged_csv_blocks(self):
        self.run_gate()
        lines = self.path.read_text().splitlines()
        lines[1] += ",unexpected"
        self.path.write_text("\n".join(lines) + "\n")
        self.contract["data_sha256"] = hashlib.sha256(self.path.read_bytes()).hexdigest()
        result = GATE.check_contract(self.contract, self.path.parent)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("more fields", result["reason"])


if __name__ == "__main__":
    unittest.main()
