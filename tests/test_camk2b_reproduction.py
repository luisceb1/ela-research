import gzip
from pathlib import Path
import tempfile
import unittest

from scripts.map_isoforms import validated_chain
from scripts.reproduce_camk2b import GENES, TARGET, aggregate_counts, keys, matching_models


def model(chrom="chr7", strand="-", gene=GENES["CAMK2B"]):
    return {"geneid": gene, "chrom": chrom, "strand": strand,
            "exons": validated_chain([(44222117, 44222200), (44220800, 44220901)])}


class CAMK2BReproductionTests(unittest.TestCase):
    def test_minus_strand_uses_genomic_boundaries_without_reversal(self):
        self.assertIn(TARGET, keys(model()))

    def test_coordinate_match_requires_gene_chromosome_and_strand(self):
        records = {"right": model(), "chrom": model(chrom="chr8"),
                   "strand": model(strand="+"), "gene": model(gene=GENES["STMN2"])}
        self.assertEqual(matching_models(records, GENES["CAMK2B"], TARGET), ["right"])

    def test_absent_model_returns_empty_without_biological_absence_claim(self):
        self.assertEqual(matching_models({"other": model(strand="+")}, GENES["CAMK2B"], TARGET), [])

    def test_nonfinite_counts_and_duplicate_transcripts_fail(self):
        for rows in ["tx\tENSG00000058404\tnan\n", "tx\tENSG00000058404\t1\ntx\tENSG00000058404\t1\n"]:
            with self.subTest(rows=rows), tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp) / "counts.gz"
                with gzip.open(p, "wt") as f:
                    f.write("TXNAME\tGENEID\tsynthetic_column\n" + rows)
                with self.assertRaises(ValueError):
                    aggregate_counts(p, {"tx": model()})

    def test_aggregates_do_not_export_library_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "counts.gz"
            with gzip.open(p, "wt") as f:
                f.write("TXNAME\tGENEID\tsynthetic_a\tsynthetic_b\ntx\tENSG00000058404\t2\t0\n")
            r = aggregate_counts(p, {"tx": model()})
            self.assertNotIn("synthetic_a", str(r))
            self.assertEqual(r["transcript_totals"], {"tx": 2.0})
            self.assertEqual(r["gene_qc"][GENES["CAMK2B"]]["libraries_with_positive_gene_sum"], 1)
