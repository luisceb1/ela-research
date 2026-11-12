"""Pruebas del arbitraje de la fracción críptica (no son validación científica)."""
import gzip
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from arbitrate_unc13a_fraction import (  # noqa: E402
    GENES, conditions, read_gene_sums, read_lengths,
)


def gz(directory, name, text):
    path = Path(directory) / name
    with gzip.open(path, "wt") as fh:
        fh.write(text)
    return path


def gene_sums(rows, samples):
    head = "##annotation=G026\ngene_id\t" + "\t".join(samples) + "\n"
    return head + "".join(f"{g}\t" + "\t".join(str(v) for v in vals) + "\n"
                          for g, vals in rows)


class ArbitrationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_gene_of_interest_is_matched_ignoring_version_suffix(self):
        rows = [(GENES["TARDBP"] + ".17", [100, 40]), ("ENSG00000999999.1", [5, 5])]
        path = gz(self.d, "gs.gz", gene_sums(rows, ["S1", "S2"]))
        samples, found, _ = read_gene_sums(path)
        self.assertEqual(samples, ["S1", "S2"])
        self.assertEqual(found["TARDBP"], [100, 40])

    def test_amplicon_shape_is_detected_and_blocks_a_knockdown_number(self):
        # One gene carries every count: an amplicon, not expression.
        rows = [(GENES["TARDBP"] + ".17", [0, 0]), ("ENSG00000130477.16", [9000, 9000])]
        path = gz(self.d, "gs.gz", gene_sums(rows, ["S1", "S2"]))
        _, _, shape = read_gene_sums(path)
        self.assertEqual(shape["S1"]["top_gene_share"], 1.0)
        self.assertFalse(shape["S1"]["transcriptome_wide"])

    def test_transcriptome_wide_shape_needs_many_genes(self):
        rows = [(f"ENSG{i:011d}.1", [1, 1]) for i in range(6000)]
        path = gz(self.d, "gs.gz", gene_sums(rows, ["S1", "S2"]))
        _, _, shape = read_gene_sums(path)
        self.assertGreaterEqual(shape["S1"]["genes_detected"], 5000)
        self.assertTrue(shape["S1"]["transcriptome_wide"])

    def test_zero_counts_are_not_counted_as_detected(self):
        rows = [(f"ENSG{i:011d}.1", [0, 1]) for i in range(10)]
        path = gz(self.d, "gs.gz", gene_sums(rows, ["S1", "S2"]))
        _, _, shape = read_gene_sums(path)
        self.assertEqual(shape["S1"]["genes_detected"], 0)
        self.assertEqual(shape["S2"]["genes_detected"], 10)

    def test_groups_come_from_declared_genotype_or_treatment(self):
        sra = ("external_id\tsample_name\tsample_title\tsample_attributes\n"
               "A\tG1\tctl\tgenotype;;control\n"
               "B\tG2\tkd\tgenotype;;TDP43 knockdown\n"
               "C\tG3\tsh\ttreatment;;shTDP-43|cell line;;NDS1\n"
               "D\tG4\tscr\ttreatment;;shScramble\n")
        path = gz(self.d, "sra.gz", sra)
        out = conditions(path)
        self.assertEqual(out["A"]["group"], "control")
        self.assertEqual(out["B"]["group"], "TDP43_depleted")
        self.assertEqual(out["C"]["group"], "TDP43_depleted")
        self.assertEqual(out["C"]["cell_line"], "NDS1")
        self.assertEqual(out["D"]["group"], "control")

    def test_read_lengths_are_keyed_and_parsed(self):
        qc = ("rail_id\tbc_frag.mode_length\tbc_frag.kallisto_mean_length\tbc_auc.unique_%\n"
              "7\t136\t189.770\t138.08\n")
        path = gz(self.d, "qc.gz", qc)
        out = read_lengths(path)
        self.assertEqual(out["7"]["mode_length"], "136")
        self.assertEqual(out["7"]["kallisto_mean_length"], "189.770")


if __name__ == "__main__":
    unittest.main()
