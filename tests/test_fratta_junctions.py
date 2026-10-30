import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('fratta', ROOT / 'scripts/audit_fratta_junctions.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def record(count='2', start='10', label='STMN2_cryptic'):
    return ('chr1', start, '20', 'FTD_S1_TDP_43_positive.SJ.out', count, '+', label)


class FrattaTests(unittest.TestCase):
    def test_exact_dedup_does_not_sum_support(self):
        r = record();table = mod.pivot(sorted(set([r, r, r])))
        self.assertEqual(next(iter(table.values()))['STMN2_cryptic'], 2)

    def test_different_count_same_sample_class_is_conflict(self):
        with self.assertRaises(ValueError):mod.pivot([record(), record(count='3')])

    def test_different_geometry_cannot_be_silently_collapsed(self):
        with self.assertRaises(ValueError):mod.pivot([record(), record(start='11')])

    def test_zero_denominator_not_zero_index(self):
        row = {k: 0 for k in mod.LABELS}
        self.assertEqual(mod.ratio(row, 'UNC13A'), (None, 0))

    def test_unknown_class_rejected(self):
        with self.assertRaises(ValueError):mod.parse('\t'.join(record(label='unknown')))

    def test_zero_fill_is_an_explicit_transform(self):
        table = mod.pivot([record()]);row = next(iter(table.values()))
        self.assertEqual(row['STMN2_annotated'], 0)
        self.assertEqual(row['STMN2_cryptic'], 2)

    def test_opaque_unit_prefix_not_merged(self):
        first, _ = mod.sample_identity('FTD_S1_TDP_43_positive.SJ.out')
        second, _ = mod.sample_identity('FTD_ALS_S1_TDP_43_negative.SJ.out')
        self.assertNotEqual(first, second)
        with self.assertRaises(ValueError):mod.sample_identity('OTHER_S1_TDP_43_positive.SJ.out')

    def test_incomplete_pair_set_rejected(self):
        with self.assertRaises(ValueError):mod.summarize(mod.pivot([record()]), 'STMN2', 'fixture')

    def test_two_and_three_class_formulas_are_distinct(self):
        row = {k: 0 for k in mod.LABELS}
        row.update(UNC13A_3prime=1, UNC13A_5prime=1, UNC13A_5prime_2=2, UNC13A_annotated=2)
        self.assertEqual(mod.ratio(row, 'UNC13A', False), (.5, 4))
        self.assertAlmostEqual(mod.ratio(row, 'UNC13A', True)[0], 2 / 3)

    def test_negative_counts_rejected(self):
        with self.assertRaises(ValueError):mod.parse('\t'.join(record(count='-1')))
