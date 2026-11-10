"""Pruebas del replay descriptivo de Ikegami (no son validación científica)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

try:
    from replay_ikegami_source_data import (  # noqa: E402
        dunn_holm, leave_one_out_spearman, nbsp, permutation_control,
    )
    HAVE_DEPS = True
except ImportError:  # scipy/openpyxl absent
    HAVE_DEPS = False


@unittest.skipUnless(HAVE_DEPS, "scipy/openpyxl no instalados")
class ReplayHelpersTest(unittest.TestCase):
    def test_nbsp_normalises_non_breaking_spaces(self):
        self.assertEqual(nbsp("ALS\xa0Type\xa02b"), "ALS Type 2b")
        self.assertEqual(nbsp("  a \xa0 b  "), "a b")

    def test_dunn_detects_the_separated_group_only(self):
        a = [1.0, 2, 3, 4, 5]
        b = [1.5, 2.5, 3.5, 4.5, 5.5]
        c = [100.0, 200, 300, 400, 500]
        res = {(r["a"], r["b"]): r for r in dunn_holm([a, b, c], ["A", "B", "C"])}
        self.assertGreater(res[("A", "B")]["p_holm"], 0.05)
        self.assertLess(res[("A", "C")]["p_holm"], 0.05)
        self.assertLess(res[("B", "C")]["p_holm"], 0.05)

    def test_holm_adjustment_is_monotone_and_bounded(self):
        res = dunn_holm([[1.0, 2, 3], [4.0, 5, 6], [7.0, 8, 9]], ["A", "B", "C"])
        for r in res:
            self.assertGreaterEqual(r["p_holm"], r["p_unadjusted"] - 1e-12)
            self.assertLessEqual(r["p_holm"], 1.0)

    def test_leave_one_out_reports_one_rho_per_observation(self):
        xs = [1.0, 2, 3, 4, 5, 6]
        ys = [1.0, 2, 3, 4, 5, 60]
        out = leave_one_out_spearman(xs, ys)
        self.assertEqual(out["n"], len(xs))
        self.assertLessEqual(out["min"], out["max"])

    def test_permutation_control_is_reproducible_and_finds_real_separation(self):
        groups = [[1.0, 2, 3, 4], [5.0, 6, 7, 8], [90.0, 100, 110, 120]]
        first = permutation_control(groups, seed=7, iterations=200)
        again = permutation_control(groups, seed=7, iterations=200)
        self.assertEqual(first["p_permutation"], again["p_permutation"])
        self.assertLess(first["p_permutation"], 0.05)

    def test_permutation_control_does_not_flag_identical_groups(self):
        same = [[1.0, 2, 3, 4], [1.0, 2, 3, 4], [1.0, 2, 3, 4]]
        out = permutation_control(same, seed=7, iterations=200)
        self.assertGreater(out["p_permutation"], 0.05)


if __name__ == "__main__":
    unittest.main()
