"""Software fixtures only; none are biological evidence."""
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from openpyxl import Workbook
from scipy.stats import rankdata

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_ikegami_subtype_association import (
    GROUPS, adjusted_rho, bootstrap, coefficients, permutation_test,
    read_pairs, residual_ranks, run, validate,
)


class SubtypeAssociationTest(unittest.TestCase):
    def setUp(self):
        self.groups = np.repeat(GROUPS, 4)
        self.x = np.concatenate([np.arange(4) + 100*i for i in range(3)])
        self.y = np.concatenate([np.array([1,3,0,2]) + 100*i for i in range(3)])

    def test_group_only_association_disappears(self):
        out = coefficients(self.x, self.y, self.groups)
        self.assertGreater(out["pooled"], .8)
        self.assertAlmostEqual(out["adjusted"], 0, places=12)
        self.assertEqual(permutation_test(self.x, self.y, self.groups, 99)["p_two_sided"], 1)

    def test_within_group_association_persists(self):
        self.assertAlmostEqual(adjusted_rho(self.x, self.x**3, self.groups), 1)
        result = permutation_test(self.x, self.x**3, self.groups, 999, seed=91)
        self.assertLess(result["p_two_sided"], .01)

    def test_matches_least_squares_residualization_with_ties(self):
        x = np.array([0,0,2,3,1,2,2,4,0,1,3,3])
        y = np.array([2,3,0,1,4,1,2,2,3,0,1,1])
        design = np.column_stack([self.groups == g for g in GROUPS]).astype(float)
        rx = rankdata(x); ry = rankdata(y)
        rx -= design @ np.linalg.lstsq(design, rx, rcond=None)[0]
        ry -= design @ np.linalg.lstsq(design, ry, rcond=None)[0]
        self.assertAlmostEqual(adjusted_rho(x,y,self.groups), np.corrcoef(rx,ry)[0,1], places=12)

    def test_stratified_permutation_matches_independent_manual_loop(self):
        seed, count = 9, 39
        y = self.y.copy(); y[0] = .2
        rx, ry = residual_ranks(self.x,y,self.groups)
        rng = np.random.default_rng(seed)
        observed = adjusted_rho(self.x,y,self.groups)
        extreme = 0
        for _ in range(count):
            p = ry.copy()
            for g in np.unique(self.groups):
                idx = np.flatnonzero(self.groups == g)
                p[idx] = rng.permutation(ry[idx])
                np.testing.assert_array_equal(np.sort(p[idx]), np.sort(ry[idx]))
            extreme += abs(np.corrcoef(rx,p)[0,1]) >= abs(observed)-1e-12
        got = permutation_test(self.x,y,self.groups,count,seed)
        self.assertEqual(got["p_two_sided"], (extreme+1)/(count+1))
        self.assertEqual(got, permutation_test(self.x,y,self.groups,count,seed))

    def test_bootstrap_keeps_pairing_for_perfect_association(self):
        got = bootstrap(self.x,self.x,self.groups,200,seed=17)
        self.assertEqual(got, bootstrap(self.x,self.x,self.groups,200,seed=17))
        np.testing.assert_allclose(got["estimates"]["adjusted"]["ci95_percentile"], [1,1])

    def test_degenerate_bootstrap_interval_is_unavailable(self):
        got = bootstrap(np.ones(12),self.y,self.groups,20)
        self.assertIsNone(got["estimates"]["adjusted"]["ci95_percentile"])
        self.assertEqual(got["estimates"]["adjusted"]["undefined_replicates"],20)
        with self.assertRaises(ValueError):
            permutation_test(np.ones(12),self.y,self.groups,10)

    def test_rejects_invalid_arrays(self):
        for x,y,g in [([1,2],[1,2,3],["a","a"]),
                      ([1,2,3],[1,float("nan"),3],["a"]*3),
                      ([1,2,3],[1,2,3],["a","a","b"])]:
            with self.assertRaises(ValueError):validate(x,y,g)

    def test_reads_explicit_sheet_pairs_and_rejects_orphans(self):
        ws=Workbook().active;ws.title="Fig. 2c"
        ws.append(["marker x",*["truncated STMN2 RNA_"+g for g in GROUPS]])
        ws.append([1,2,None,None]);ws.append([3,None,4,None])
        x,y,g,provenance=read_pairs(ws)
        np.testing.assert_array_equal(x,[1,3]);np.testing.assert_array_equal(y,[2,4])
        self.assertEqual(provenance["pair_cells"],[["A2","B2"],["A3","C3"]])
        ws.append([5,None,None,None])
        with self.assertRaises(ValueError):read_pairs(ws)

    def test_rejects_ambiguous_labels_and_nonfinite_cells(self):
        for headers, values in [(["x","unknown",GROUPS[1],GROUPS[2]],[1,2,None,None]),
                                (["x",*GROUPS],[1,float("inf"),None,None]),
                                (["x",*GROUPS],[True,2,None,None])]:
            ws=Workbook().active;ws.append(headers);ws.append(values)
            with self.assertRaises(ValueError):read_pairs(ws)

    def test_rejects_wrong_source_before_workbook_parsing(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"wrong.xlsx";p.write_bytes(b"not the verified workbook")
            with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):run(p,"fixture")


if __name__ == "__main__":
    unittest.main()
