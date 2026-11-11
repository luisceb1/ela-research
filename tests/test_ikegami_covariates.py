"""Pruebas del cribado de covariables de Ikegami (no son validación científica)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

try:
    from check_ikegami_covariates import compare, join_key_uniqueness, numeric
    HAVE_DEPS = True
except ImportError:
    HAVE_DEPS = False


@unittest.skipUnless(HAVE_DEPS, "scipy/openpyxl no instalados")
class CovariateHelpersTest(unittest.TestCase):
    def test_numeric_treats_placeholders_as_missing(self):
        for placeholder in ("-", "", "NA", "n.a.", "ND", "texto"):
            self.assertIsNone(numeric(placeholder))
        self.assertEqual(numeric("7.6"), 7.6)
        self.assertEqual(numeric(3), 3.0)

    def test_compare_detects_a_real_difference(self):
        groups = {"Type 1": [1.0, 2, 3, 4], "Type 2a": [1.5, 2.5, 3.5, 4.5],
                  "Type 2b": [40.0, 50, 60, 70]}
        out = compare(groups)
        self.assertEqual(out["status"], "tested")
        self.assertTrue(out["differs_at_0_05"])

    def test_compare_does_not_flag_identical_groups(self):
        groups = {s: [1.0, 2, 3, 4] for s in ("Type 1", "Type 2a", "Type 2b")}
        self.assertFalse(compare(groups)["differs_at_0_05"])

    def test_compare_refuses_thin_groups_instead_of_guessing(self):
        groups = {"Type 1": [1.0, 2], "Type 2a": [], "Type 2b": [3.0]}
        out = compare(groups)
        self.assertEqual(out["status"], "insufficient_data")
        self.assertNotIn("kruskal_p", out)

    def test_join_key_uniqueness_flags_duplicates(self):
        cases = [
            {"subtype": "Type 1", "disease_duration_months": 10.0},
            {"subtype": "Type 1", "disease_duration_months": 20.0},
            {"subtype": "Type 2a", "disease_duration_months": 30.0},
            {"subtype": "Type 2a", "disease_duration_months": 30.0},
        ]
        out = join_key_uniqueness(cases)
        self.assertTrue(out["Type 1"]["unique"])
        self.assertFalse(out["Type 2a"]["unique"])
        self.assertEqual(out["Type 2a"]["duplicated_values"], {"30.0": 2})

    def test_missing_durations_are_not_counted_as_a_key(self):
        cases = [{"subtype": "Type 1", "disease_duration_months": None},
                 {"subtype": "Type 1", "disease_duration_months": 5.0}]
        self.assertEqual(join_key_uniqueness(cases)["Type 1"]["n"], 1)


if __name__ == "__main__":
    unittest.main()
