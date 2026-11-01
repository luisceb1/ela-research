"""Small-fixture regression tests; run: python -m unittest discover -s tests -p 'test_nygc_metadata.py'."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from nygc_unc13a_metadata_audit import build_metadata_lookup


def row(sample="S1", pathology="ALS-TDP", donor="D1"):
    return dict(sample=sample, external_subject_id=donor,
                tdp_proteinopathy=pathology,
                rna_tissue_source_simplified="Cortex_Motor",
                rin="7.0", disease_primary="ALS")


class MetadataTests(unittest.TestCase):
    def test_redundant_rows_retained_once(self):
        lookup, redundant = build_metadata_lookup([row(), row(), row(), row("S2", donor="D2")])
        self.assertEqual((len(lookup), redundant), (2, 2))

    def test_conflicting_diagnosis_fails(self):
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            build_metadata_lookup([row(), row(pathology="Control")])

    def test_conflicting_donor_fails(self):
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            build_metadata_lookup([row(), row(donor="D9")])

    def test_blank_sample_fails(self):
        with self.assertRaisesRegex(ValueError, "Missing"):
            build_metadata_lookup([row(sample=" ")])

    def test_distinct_samples(self):
        lookup, redundant = build_metadata_lookup([row("S1"), row("S2")])
        self.assertEqual((len(lookup), redundant), (2, 0))


if __name__ == "__main__":
    unittest.main()
