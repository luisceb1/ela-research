"""Pruebas del verificador de citas (no constituyen validación científica)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from verify_matrix_quotes import clean_pdf_text, normalise, verify  # noqa: E402

MATRIX = (
    "source_id\texperiment\tclassification\tlocator\n"
    'S1\tE-1\tprevention\t"treated with ASO on day 3" (Methods)\n'
    'S1\tE-2\tprevention\t"a sentence that is absent from the source"\n'
    "S1\tE-3\tprevention\tno quoted fragment here\n"
    'S9\tE-4\tprevention\t"orphan source mapping check"\n'
)
SOURCE = "Neurons were treated with ASO on day 3 and fixed later.\n"


class VerifyQuotesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        (base / "src.txt").write_text(SOURCE, encoding="utf-8")
        self.matrix = base / "m.tsv"
        self.matrix.write_text(MATRIX, encoding="utf-8")
        self.out = verify(self.matrix, {"S1": "src.txt"}, base)
        self.by_exp = {r["experiment"]: r for r in self.out["results"]}

    def tearDown(self):
        self.tmp.cleanup()

    def test_present_fragment_passes(self):
        self.assertEqual(self.by_exp["E-1"]["status"], "PASS")

    def test_absent_fragment_is_reported(self):
        self.assertEqual(self.by_exp["E-2"]["status"], "MISSING")

    def test_row_without_quotes_is_flagged_separately(self):
        self.assertEqual(self.by_exp["E-3"]["status"], "NO_QUOTES")

    def test_unmapped_source_is_flagged(self):
        self.assertEqual(self.by_exp["E-4"]["status"], "NO_SOURCE_MAPPED")

    def test_problem_count_counts_missing_and_unmapped_only(self):
        self.assertEqual(self.out["rows_with_problems"], 2)

    def test_quotes_are_not_stripped_by_csv_parsing(self):
        """Regression: default csv quoting silently removed every fragment."""
        self.assertTrue(self.by_exp["E-1"].get("checked"))

    def test_micro_sign_matches_ascii_transliteration(self):
        self.assertEqual(normalise("0.1 μg/ml"), normalise("0.1 ug/ml"))

    def test_preprint_boilerplate_and_line_numbers_removed(self):
        raw = (
            "139    at 5 months of age to deplete TDP-43, followed by ICV\n"
            "   bioRxiv preprint doi: https://doi.org/10.0; this version posted\n"
            "140    injection of AAV 2 weeks later.\n"
        )
        cleaned = normalise(clean_pdf_text(raw))
        self.assertIn(normalise("followed by ICV injection of AAV 2 weeks later"), cleaned)
        self.assertNotIn("biorxiv", cleaned)


if __name__ == "__main__":
    unittest.main()
