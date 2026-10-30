import copy
import csv
import unittest
from pathlib import Path
from scripts.audit_dexseq_magnitudes import audit, classify

class MagnitudeTests(unittest.TestCase):
    def rows(self):
        with Path('reports/dexseq-batch-sensitivity/fragment_batch_aggregates.tsv').open() as f:
            return list(csv.DictReader(f, delimiter='\t'))
    def test_threshold_boundary_and_zero(self):
        self.assertEqual(classify(.1, -.1, .1), 'opposite_direction')
        self.assertEqual(classify(.099, -.1, .1), 'below_threshold_or_zero')
        self.assertEqual(classify(0, 1, 0), 'below_threshold_or_zero')
    def test_nonfinite_and_negative_threshold(self):
        for args in [(float('nan'), 1, 0), (1, float('inf'), 0), (1, 1, -1)]:
            with self.assertRaises(ValueError): classify(*args)
    def test_permutation_and_batch_swap(self):
        rs = self.rows(); expected = audit(rs)
        self.assertEqual(audit(list(reversed(rs))), expected)
        swapped = copy.deepcopy(rs)
        for r in swapped:
            r['batch'] = 'Batch 2' if r['batch']=='Batch 1' else 'Batch 1'
            r['scramble_libraries'] = r['KD_libraries'] = '2' if r['batch']=='Batch 1' else '4'
        result = audit(swapped)[1]
        for g in result: self.assertEqual(result[g]['thresholds_pp'], expected[1][g]['thresholds_pp'])
    def test_duplicate_and_incomplete_fail(self):
        rs = self.rows()
        for bad in [rs+[rs[0]], rs[1:]]:
            with self.assertRaises(ValueError): audit(bad)
    def test_corrupt_fraction_delta_and_closure_fail(self):
        for field, val in [('mean_control_count_fraction','nan'), ('mean_KD_count_fraction','-1'), ('change_percentage_points','3')]:
            rs=self.rows(); rs[0][field]=val
            with self.assertRaises(ValueError): audit(rs)
        rs=self.rows(); rs[0]['mean_control_count_fraction']=str(float(rs[0]['mean_control_count_fraction'])+.01)
        rs[0]['change_percentage_points']=str(float(rs[0]['change_percentage_points'])-1)
        with self.assertRaises(ValueError): audit(rs)
    def test_wrong_library_count_and_gene_fail(self):
        for field, val in [('gene','OTHER'), ('scramble_libraries','99'), ('fragment','OTHER:E001')]:
            rs=self.rows(); rs[0][field]=val
            with self.assertRaises(ValueError): audit(rs)
