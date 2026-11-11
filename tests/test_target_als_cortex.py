"""Pruebas del ciclo de corteza motora TARGET_ALS (no son validación científica)."""
import gzip
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from target_als_cortex_cryptic import (  # noqa: E402
    GROUP_COLUMN, UNLABELLED, inclusion_psi, read_groups, summarise, summed_ratio,
)

STUDY = (
    "rail_id\texternal_id\tSex\tEthnicity\t" + GROUP_COLUMN + "\tAge at Death\n"
    "11\tCG-1\tMale\tUnknown\tALS Spectrum MND\t68\n"
    "12\tCG-2\tFemale\tUnknown\tNon-Neurological Control\t81\n"
    "13\tCG-3\tMale\tUnknown\t\t70\n"
)


def gz(directory, name, text):
    path = Path(directory) / name
    with gzip.open(path, "wt") as fh:
        fh.write(text)
    return path


class CortexCycleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.study = gz(self.tmp.name, "study.gz", STUDY)

    def tearDown(self):
        self.tmp.cleanup()

    def test_only_the_group_column_is_read(self):
        groups = read_groups(self.study)
        self.assertEqual(groups["11"], "ALS Spectrum MND")
        self.assertEqual(groups["12"], "Non-Neurological Control")
        # No clinical or demographic value may appear anywhere in the result.
        flat = " ".join(groups.values())
        for leaked in ("Male", "Female", "68", "81", "Unknown"):
            self.assertNotIn(leaked, flat)

    def test_blank_group_becomes_an_explicit_unlabelled_marker(self):
        self.assertEqual(read_groups(self.study)["13"], UNLABELLED)

    def test_summed_ratio_is_within_gene_and_excludes_the_control(self):
        counts = {"canonical": 90, "cryptic_left": 6, "cryptic_right": 4}
        self.assertAlmostEqual(summed_ratio(counts, "canonical"), 0.1)

    def test_summed_ratio_double_counts_included_molecules(self):
        # Equal molecular abundance: the two cryptic junctions together collect
        # about twice the canonical junction's reads, so the summed form reads
        # 0.667 where the per-junction estimate reads 0.5.
        counts = {"canonical": 100, "cryptic_left": 100, "cryptic_right": 100}
        self.assertAlmostEqual(summed_ratio(counts, "canonical"), 2 / 3)
        self.assertAlmostEqual(inclusion_psi(counts, "canonical"), 0.5)

    def test_inclusion_psi_averages_the_two_cryptic_junctions(self):
        counts = {"canonical": 90, "cryptic_left": 6, "cryptic_right": 4}
        self.assertAlmostEqual(inclusion_psi(counts, "canonical"), 5 / 95)

    def test_both_ratios_are_none_when_the_locus_has_no_reads(self):
        counts = {"canonical": 0, "cryptic_left": 0, "cryptic_right": 0}
        self.assertIsNone(summed_ratio(counts, "canonical"))
        self.assertIsNone(inclusion_psi(counts, "canonical"))

    def test_all_cryptic_and_no_canonical_gives_one_for_both(self):
        counts = {"canonical": 0, "cryptic_left": 5, "cryptic_right": 5}
        self.assertEqual(summed_ratio(counts, "canonical"), 1.0)
        self.assertEqual(inclusion_psi(counts, "canonical"), 1.0)

    def test_summarise_ignores_missing_values(self):
        out = summarise([0.0, None, 0.5, 0.25])
        self.assertEqual(out["n"], 3)
        self.assertEqual(out["median"], 0.25)
        self.assertEqual(out["max"], 0.5)

    def test_summarise_reports_nothing_when_every_value_is_missing(self):
        self.assertEqual(summarise([None, None]), {"n": 0})


if __name__ == "__main__":
    unittest.main()
