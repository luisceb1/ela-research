import copy
import unittest

from scripts.mea_input_qc import validate_synthetic_rows


from scripts.mea_audit_fixtures import cases, synthetic_fixture


class MEAInputQCTests(unittest.TestCase):
    def test_valid_fixture_is_not_experimental_validation_and_is_unchanged(self):
        rows = synthetic_fixture(); before = copy.deepcopy(rows)
        r = validate_synthetic_rows(rows, provenance="synthetic")
        self.assertFalse(r["experimental_analysis_validated"])
        self.assertFalse(r["biological_eligibility_verified"])
        self.assertEqual(rows, before)

    def test_six_original_importer_counterexamples_rejected(self):
        for name, rows in cases().items():
            if name == "valid": continue
            with self.subTest(case=name), self.assertRaises(ValueError):
                validate_synthetic_rows(rows, provenance="synthetic")

    def test_real_or_unlabeled_data_not_supported(self):
        for label in ("real", "unknown", ""):
            with self.subTest(label=label), self.assertRaises(ValueError):
                validate_synthetic_rows(synthetic_fixture(), provenance=label)

    def test_fractional_time_and_nonfinite_viability_rejected(self):
        for field, value in [("time_index", .5), ("viability", float("nan")), ("viability", float("inf"))]:
            rows = synthetic_fixture(); rows[0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                validate_synthetic_rows(rows, provenance="synthetic")

    def test_technical_missing_does_not_become_zero_or_death(self):
        rows = synthetic_fixture()
        # One well's endpoint is missing but another observed well in the same arm supplies support.
        extra = [dict(r, well_id="synthetic_extra") for r in rows if r["arm"] == "late_ASO"]
        next(r for r in extra if r["time_index"] == 8).update(status="technical_missing", synchrony=None, qc_ok=0)
        rows += extra
        validate_synthetic_rows(rows, provenance="synthetic")
        self.assertIsNone(next(r for r in extra if r["time_index"] == 8)["synchrony"])

    def test_absorbing_death_is_allowed_as_composite_support(self):
        rows = synthetic_fixture()
        for r in rows:
            if r["arm"] == "late_ASO" and r["time_index"] >= 8:
                r.update(status="dead", synchrony=None, qc_ok=0, viability=0)
        validate_synthetic_rows(rows, provenance="synthetic")

    def test_wholly_missing_arm_endpoint_is_not_negative_evidence(self):
        rows = synthetic_fixture()
        for r in rows:
            if r["arm"] == "damage_control" and r["time_index"] == 8:
                r.update(status="technical_missing", synchrony=None, qc_ok=0)
        with self.assertRaisesRegex(ValueError, "Entire arm"):
            validate_synthetic_rows(rows, provenance="synthetic")

    def test_duplicate_and_arm_changes_rejected(self):
        rows = synthetic_fixture(); rows.append(dict(rows[0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate_synthetic_rows(rows, provenance="synthetic")
        rows = synthetic_fixture(); rows[8]["arm"] = "damage_control"
        with self.assertRaisesRegex(ValueError, "changes"):
            validate_synthetic_rows(rows, provenance="synthetic")
