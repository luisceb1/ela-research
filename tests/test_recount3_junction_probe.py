"""Pruebas de la sonda de uniones recount3 (no son validación científica)."""
import gzip
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from recount3_junction_probe import (  # noqa: E402
    attribute, build_samples, find_target_rows, read_counts,
)

RR = (
    "chromosome\tstart\tend\tlength\tstrand\tannotated\tleft_motif\tright_motif\t"
    "left_annotated\tright_annotated\n"
    "chr1\t100\t200\t101\t+\t1\tGT\tAG\t1\t1\n"
    "chr19\t17641557\t17642844\t1288\t-\t1\tCT\tAC\t1\t1\n"
    "chr19\t17641557\t17642413\t857\t-\t0\tCT\tAC\t1\t0\n"
    "chr19\t17642592\t17642844\t253\t-\t0\tCT\tAC\t0\t1\n"
)
MM = ("%%MatrixMarket matrix coordinate integer general\n%--\n"
      "4\t2\t3\n2\t1\t66\n2\t2\t53\n3\t2\t4\n")
IDS = "rail_id\n111\n222\n"
PROJ = "rail_id\texternal_id\n111\tSRR1\n222\tSRR2\n"
SRA = ("external_id\tsample_name\tsample_title\tsample_attributes\n"
       "SRR1\tGSM1\tscramble rep1\tgenotype;;control|sirna type;;scramble\n"
       "SRR2\tGSM2\tTDP43 rep1\tgenotype;;TDP43 knockdown|sirna type;;TDP43\n")


def gz(directory, name, text):
    path = Path(directory) / name
    with gzip.open(path, "wt") as fh:
        fh.write(text)
    return path


class ProbeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = self.tmp.name
        self.rr = gz(d, "rr.gz", RR)
        self.mm = gz(d, "mm.gz", MM)
        self.ids = gz(d, "ids.gz", IDS)
        self.proj = gz(d, "proj.gz", PROJ)
        self.sra = gz(d, "sra.gz", SRA)
        self.targets = {"canonical": (17641556, 17642844),
                        "cryptic_left": (17641556, 17642413),
                        "cryptic_right": (17642541, 17642844)}

    def tearDown(self):
        self.tmp.cleanup()

    def test_sealed_coordinates_convert_and_match_exactly(self):
        found = find_target_rows(self.rr, "chr19", self.targets)
        self.assertEqual(found["canonical"]["row"], 2)
        self.assertEqual(found["cryptic_left"]["row"], 3)
        self.assertEqual(found["canonical"]["annotated"], "1")
        self.assertEqual(found["cryptic_left"]["annotated"], "0")

    def test_absent_target_is_reported_absent_not_substituted(self):
        found = find_target_rows(self.rr, "chr19", self.targets)
        self.assertTrue(found["cryptic_right"].get("absent"))
        self.assertIsNone(found["cryptic_right"]["row"])
        # The nearest junction is context only and must not become the target.
        self.assertIn("never adopted", found["cryptic_right"]["nearest_junction"]["note"])

    def test_wrong_chromosome_is_not_matched(self):
        found = find_target_rows(self.rr, "chr1", self.targets)
        self.assertTrue(all(v.get("absent") for v in found.values()))

    def test_bad_coordinate_convention_raises_instead_of_guessing(self):
        bad = RR.replace("1288", "1287")
        path = gz(self.tmp.name, "bad.gz", bad)
        with self.assertRaises(ValueError):
            find_target_rows(path, "chr19", self.targets)

    def test_counts_are_read_per_column_and_absent_entries_stay_zero(self):
        counts, header = read_counts(self.mm, {2: "canonical", 3: "cryptic_left"})
        self.assertEqual(header, {"rows": 4, "columns": 2, "nonzeros": 3})
        self.assertEqual(counts["canonical"], {1: 66, 2: 53})
        self.assertEqual(counts["cryptic_left"], {2: 4})
        self.assertNotIn(1, counts["cryptic_left"])

    def test_conditions_come_from_declared_attributes(self):
        samples = build_samples(self.ids, self.proj, self.sra)
        self.assertEqual([s["run"] for s in samples], ["SRR1", "SRR2"])
        self.assertEqual(samples[0]["genotype"], "control")
        self.assertEqual(samples[1]["genotype"], "TDP43 knockdown")
        self.assertEqual(samples[1]["sirna_type"], "TDP43")

    def test_attribute_returns_empty_for_missing_key(self):
        self.assertEqual(attribute("genotype;;control", "sirna type"), "")
        self.assertEqual(attribute("", "genotype"), "")


if __name__ == "__main__":
    unittest.main()
