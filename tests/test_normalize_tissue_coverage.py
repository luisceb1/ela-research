"""Pruebas de la normalizacion por biblioteca (no son validacion cientifica).

La prueba central es la que distingue mediana-de-razones de razon-de-medianas:
es el error que estas pruebas existen para impedir que vuelva.
"""
import gzip
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from normalize_tissue_coverage import (  # noqa: E402
    DENOMINATORS, PRIMARY, normalise_group, read_depths, run,
)

# Tres bibliotecas con profundidades deliberadamente dispares, de modo que la
# mediana de las razones y la razon de las medianas NO coincidan.
QC = (
    "rail_id\t" + "\t".join(DENOMINATORS) + "\n"
    "1\t10000000\t5000000\t10000000\t9000000\t8000000\n"
    "2\t20000000\t10000000\t20000000\t18000000\t16000000\n"
    "3\t100000000\t50000000\t100000000\t90000000\t80000000\n"
)

SAMPLES = [
    {"rail_id": "1", "group": "G", "counts": {"canonical": 10}},
    {"rail_id": "2", "group": "G", "counts": {"canonical": 20}},
    {"rail_id": "3", "group": "G", "counts": {"canonical": 20}},
]


def gz(directory, name, text):
    path = Path(directory) / name
    with gzip.open(path, "wt") as fh:
        fh.write(text)
    return path


class NormalisationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.qc = gz(self.tmp.name, "qc.MD.gz", QC)

    def tearDown(self):
        self.tmp.cleanup()

    def test_median_of_ratios_is_not_the_ratio_of_medians(self):
        depths = read_depths(self.qc)
        out = normalise_group(SAMPLES, depths, "canonical")
        field = out["per_million"][PRIMARY]
        # Razones por biblioteca: 1.0, 1.0, 0.2 -> mediana 1.0
        self.assertAlmostEqual(field["per_library_ratios"]["median"], 1.0)
        # Razon de medianas: mediana(20) / mediana(20 M) = 1.0 ... construimos
        # el caso para que difiera usando la mediana de profundidad 20 M y
        # mediana de cuentas 20 -> 1.0. Verificamos el minimo, que si separa.
        self.assertAlmostEqual(field["per_library_ratios"]["min"], 0.2)
        self.assertEqual(field["median_depth_M"], 20.0)

    def test_divergent_case_separates_the_two_methods(self):
        depths = read_depths(self.qc)
        samples = [
            {"rail_id": "1", "group": "G", "counts": {"canonical": 1}},
            {"rail_id": "2", "group": "G", "counts": {"canonical": 2}},
            {"rail_id": "3", "group": "G", "counts": {"canonical": 100}},
        ]
        field = normalise_group(samples, depths, "canonical")["per_million"][PRIMARY]
        # Razones: 0.1, 0.1, 1.0 -> mediana 0.1
        self.assertAlmostEqual(field["per_library_ratios"]["median"], 0.1)
        # Razon de medianas: 2 / 20 = 0.1 ... iguales aqui; el caso siguiente no.
        samples[1]["counts"]["canonical"] = 40
        field = normalise_group(samples, depths, "canonical")["per_million"][PRIMARY]
        self.assertAlmostEqual(field["per_library_ratios"]["median"], 1.0)
        self.assertAlmostEqual(field["ratio_of_medians_NOT_a_normalisation"], 2.0)
        self.assertNotAlmostEqual(
            field["per_library_ratios"]["median"],
            field["ratio_of_medians_NOT_a_normalisation"])

    def test_missing_qc_row_refuses_instead_of_computing(self):
        depths = read_depths(self.qc)
        samples = SAMPLES + [{"rail_id": "99", "group": "G",
                              "counts": {"canonical": 5}}]
        out = normalise_group(samples, depths, "canonical")
        self.assertIsNone(out["per_million"])
        self.assertIn("99", out["missing_qc_rows"])
        self.assertIn("no normalised figure", out["refused"])

    def test_zero_and_absent_depths_are_dropped_not_treated_as_one(self):
        bad = gz(self.tmp.name, "bad.MD.gz",
                 "rail_id\t" + PRIMARY + "\n1\t0\n2\tNA\n3\t\n")
        depths = read_depths(bad)
        self.assertEqual(depths["1"], {})
        self.assertEqual(depths["2"], {})
        self.assertEqual(depths["3"], {})

    def test_primary_denominator_is_the_submitted_not_assigned_field(self):
        # El informe llamo a este campo "lecturas asignadas a exones". No lo es.
        self.assertEqual(PRIMARY, "exon_fc_count_all.total")
        self.assertIn("exon_fc_count_all.assigned", DENOMINATORS)

    def test_run_reports_every_denominator_and_the_withdrawn_figures(self):
        results = {"tissue": "T", "samples": SAMPLES}
        rpath = Path(self.tmp.name) / "results.json"
        rpath.write_text(json.dumps(results), encoding="utf-8")

        class Args:
            tissue = [f"T:{rpath}:{self.qc}"]
            junction = "canonical"
            group = "G"

        out = run(Args())
        self.assertEqual(out["primary_denominator"], PRIMARY)
        self.assertEqual(set(out["tissues"]["T"]["by_group"]), {"G"})
        self.assertEqual(
            set(out["tissues"]["T"]["by_group"]["G"]["per_million"]),
            set(DENOMINATORS))
        self.assertIn("2.30 / 0.11 per million", out["withdrawn_figures"])
        self.assertTrue(out["tissues"]["T"]["qc_sha256"])
        self.assertEqual(out["tissues"]["T"]["qc_rows"], 3)


if __name__ == "__main__":
    unittest.main()


# Profundidades grandes, para que las razones queden lo bastante pequenas como
# que redondear a 4 decimales mueva un cociente en la segunda cifra.
QC_DEEP = (
    "rail_id\t" + "\t".join(DENOMINATORS) + "\n"
    "1\t300000000\t1\t1\t1\t1\n"
    "2\t700000000\t1\t1\t1\t1\n"
)


class PrecisionTest(unittest.TestCase):
    """La division se hace con precision completa, no sobre medianas redondeadas."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.qc = gz(self.tmp.name, "qc.MD.gz", QC)
        self.deep = gz(self.tmp.name, "deep.MD.gz", QC_DEEP)

    def tearDown(self):
        self.tmp.cleanup()

    def test_exact_median_is_deposited_alongside_the_rounded_one(self):
        depths = read_depths(self.qc)
        samples = [{"rail_id": "1", "group": "G", "counts": {"canonical": 1}},
                   {"rail_id": "2", "group": "G", "counts": {"canonical": 7}},
                   {"rail_id": "3", "group": "G", "counts": {"canonical": 9}}]
        field = normalise_group(samples, depths, "canonical")["per_million"][PRIMARY]
        exact = field["per_library_median_exact"]
        # Razones 0.1, 0.35, 0.09 -> mediana 0.1
        self.assertAlmostEqual(exact, 0.1)
        self.assertEqual(field["per_library_ratios"]["median"], round(exact, 4))

    def test_fold_uses_exact_medians_and_flags_the_rounded_variant(self):
        # 1/300 = 0.003333... y 1/700 = 0.001428..., cuyo cociente exacto es
        # 7/3 = 2.33; redondeadas a 0.0033 y 0.0014 el cociente da 2.36.
        a = [{"rail_id": "1", "group": "G", "counts": {"canonical": 1}}]
        b = [{"rail_id": "2", "group": "G", "counts": {"canonical": 1}}]
        ra = Path(self.tmp.name) / "a.json"
        rb = Path(self.tmp.name) / "b.json"
        ra.write_text(json.dumps({"tissue": "A", "samples": a}), encoding="utf-8")
        rb.write_text(json.dumps({"tissue": "B", "samples": b}), encoding="utf-8")

        class Args:
            tissue = [f"A:{ra}:{self.deep}", f"B:{rb}:{self.deep}"]
            junction = "canonical"
            group = "G"

        fold = run(Args())["cross_tissue_fold"][PRIMARY]
        self.assertAlmostEqual(fold["fold"], 2.33, places=2)
        self.assertAlmostEqual(fold["fold_from_rounded_medians_do_not_use"],
                               2.36, places=2)
        self.assertNotEqual(fold["fold"],
                            fold["fold_from_rounded_medians_do_not_use"])


if __name__ == "__main__":
    unittest.main()
