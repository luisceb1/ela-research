import unittest
from pathlib import Path
import tempfile
import zipfile

from scripts.audit_chan_timing import caption, normalize, timing7, timing8, workbook_metadata


class ChanTimingTests(unittest.TestCase):
    def test_second_dose_is_not_delayed_initiation(self):
        r = timing7("Single dose on DIV 4, double doses on DIV 4 and DIV 7")
        self.assertEqual(r["repeated_doses_DIV"][0], r["single_dose_DIV"][0])
        self.assertIsNone(r["delayed_initiation_arm_verified"])

    def test_endpoint_does_not_become_treatment_delay(self):
        r = timing8("Axotomy was performed on DIV 14 and treatment with ASO was performed straight after injury. immunostained 3 days after injury")
        self.assertEqual(r["first_ASO_DIV"], 14)
        self.assertEqual(r["endpoint_DIV"], 17)
        self.assertIsNone(r["injury_to_ASO_days_exact"])

    def test_missing_treatment_is_unknown_not_preventive(self):
        r = timing8("Axotomy was performed on DIV 14. immunostained 3 days after injury")
        self.assertIsNone(r["first_ASO_DIV"])
        self.assertEqual(r["timing_category"], "unknown")
        self.assertIsNone(r["persistent_functional_deficit_eligibility_verified"])

    def test_missing_caption_fails_instead_of_borrowing_other_figures(self):
        with self.assertRaisesRegex(ValueError, "Missing or ambiguous"):
            caption("Fig. 1 | Endpoint 10 days after injury", 8)

    def test_ambiguous_caption_rejected(self):
        with self.assertRaises(ValueError):
            caption("Fig. 8 | first Fig. 8 | second", 8)

    def test_pdf_ligature_and_line_break_normalization(self):
        self.assertEqual(normalize("deﬁcit\n  measured"), "deficit measured")

    def test_hyphenated_pdf_word_without_destroying_gene_name(self):
        self.assertEqual(normalize("immu-\nnostained TDP-\n43"), "immunostained TDP- 43")
        r = timing8("Axotomy was performed on DIV 14. immu-\nnostained 3 days after injury")
        self.assertEqual(r["endpoint_DIV"], 17)

    def test_absent_explicit_dates_fail(self):
        with self.assertRaises(ValueError):
            timing7("ASO treatment happened later")
        with self.assertRaises(ValueError):
            timing8("post-injury treatment")

    def test_sparse_workbook_times_are_not_interpolated_or_replicated(self):
        sheets = ["Figure 7f", "Figure 7g", "Figure 7h", "Figure 7i", "Figure 8b", "Figure 8c"]
        xmlns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "synthetic.xlsx"
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("xl/workbook.xml", f'<workbook xmlns="{xmlns}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + ''.join(f'<sheet name="{name}" r:id="r{i}"/>' for i, name in enumerate(sheets)) + '</sheets></workbook>')
                z.writestr("xl/_rels/workbook.xml.rels", '<Relationships>' + ''.join(f'<Relationship Id="r{i}" Target="worksheets/s{i}.xml"/>' for i in range(6)) + '</Relationships>')
                for i in range(6):
                    z.writestr(f"xl/worksheets/s{i}.xml", f'<worksheet xmlns="{xmlns}"><dimension ref="A1:B13"/><sheetData><row r="5"><c r="A5"><v>0</v></c><c r="B5"><v>10</v></c></row><row r="6"><c r="B6"><v>11</v></c></row><row r="13"><c r="A13"><v>2</v></c></row></sheetData></worksheet>')
            before = path.read_bytes()
            r = workbook_metadata(path)["selected_sheets"][0]
            self.assertEqual(r["explicit_DIV_labels_only_no_interpolation"], [{"cell": "A5", "DIV": 0.0}, {"cell": "A13", "DIV": 2.0}])
            self.assertFalse(r["experiment_or_differentiation_mapping_verified"])
            self.assertEqual(path.read_bytes(), before)
