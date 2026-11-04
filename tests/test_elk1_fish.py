"""Artificial arithmetic controls; none are experimental observations."""
import importlib.util
from pathlib import Path
from fractions import Fraction as F
import unittest

P = Path(__file__).resolve().parents[1]/'scripts/reproduce_elk1_fish.py'
SPEC = importlib.util.spec_from_file_location('elk1_fish', P)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class FishTests(unittest.TestCase):
    def rows(self):
        return [dict(replicate='1', arm=arm, n_nuclei=n,
                     proximal_nuclear=a, proximal_extranuclear=b,
                     distal_nuclear=a, distal_extranuclear=b)
                for arm in ['CTRL', 'TDP'] for n,a,b in [(1,2,2),(9,6,3)]]

    def test_pivot_counts_nuclei_twice_but_fold_is_invariant(self):
        summary=M.aggregate(self.rows())
        self.assertTrue(all(r['pooled_per_nucleus']==2*r['source_pivot_mean'] for r in summary))
        folds=M.fold_changes(summary)
        self.assertTrue(all(r['pooled_per_nucleus']==r['source_pivot_mean'] for r in folds))

    def test_equal_image_and_pooled_estimands_differ(self):
        row=M.aggregate(self.rows())[0]
        self.assertEqual(row['pooled_per_nucleus'],F(13,10))
        self.assertEqual(row['equal_image_per_nucleus'],F(5,2))
        self.assertEqual(row['pooled_nuclear_extranuclear'],F(8,5))
        self.assertEqual(row['equal_image_nuclear_extranuclear'],F(3,2))

    def test_zero_extranuclear_is_undefined_not_imputed(self):
        rows=self.rows();rows[0]['proximal_extranuclear']=0
        row=next(r for r in M.aggregate(rows) if r['arm']=='CTRL' and r['probe']=='proximal')
        self.assertIsNone(row['equal_image_nuclear_extranuclear'])
        self.assertIsNotNone(row['pooled_nuclear_extranuclear'])

    def test_missing_arm_cannot_be_paired(self):
        with self.assertRaises(ValueError): M.fold_changes(M.aggregate(self.rows()[:2]))

    def test_duplicate_image_or_zero_nuclei_rejected(self):
        header='replicate\tcondition\timage\t'+'\t'.join(M.COUNT_FIELDS)+'\n'
        row='1\tCTRL1\tCTRL1\t1\t1\t1\t1\t1\n'
        with self.assertRaises(ValueError): M.read_counts((header+row+row).encode())
        with self.assertRaises(ValueError): M.read_counts((header+row.replace('\t1\t1\t1\t1\t1','\t0\t1\t1\t1\t1')).encode())

    def test_order_does_not_change_summary(self):
        self.assertEqual(M.aggregate(self.rows()),M.aggregate(list(reversed(self.rows()))))


if __name__=='__main__': unittest.main()
