import gzip
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('issue14', ROOT / 'scripts/reproduce_issue14_aggregates.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class Issue14Tests(unittest.TestCase):
    def header(self):
        return [f'S{i}_{c}' for i in range(1, 8) for c in ['TP', 'TN']]

    def test_missing_pair_rejected(self):
        with self.assertRaises(ValueError):mod.validate_columns(self.header()[:-1])

    def test_duplicate_column_cannot_replace_pair(self):
        h = self.header();h[-1] = h[0]
        with self.assertRaises(ValueError):mod.validate_columns(h)

    def test_order_does_not_define_pairing(self):
        h = list(reversed(self.header()));v = [2 if c.endswith('TN') else 1 for c in h]
        self.assertEqual(mod.paired_differences(v, h), [1] * 7)

    def test_exact_signflip_seven_pairs(self):
        self.assertEqual(mod.signflip([1] * 7), 2 / 128)
        self.assertEqual(mod.signflip([0] * 7), 1)

    def test_nonfinite_not_valid_evidence(self):
        with self.assertRaises(ValueError):mod.signflip([float('nan')])

    def test_median_ratio_uses_only_all_positive_rows(self):
        factors, n = mod.size_factors({'a': [2, 8], 'b': [4, 16], 'c': [0, 999]})
        self.assertEqual(n, 2)
        self.assertAlmostEqual(factors[0], .5)
        self.assertAlmostEqual(factors[1], 2)

    def test_literal_na_rows_kept_for_library_totals(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'counts.gz'
            with gzip.open(p, 'wt') as f:
                f.write('\t'.join(self.header()) + '\n')
                for name in ['STMN2', 'UNC13A', 'TARDBP', 'NA', 'NA']:
                    f.write(name + '\t' + '\t'.join(['1'] * 14) + '\n')
            _, named, total, qc = mod.read_counts(p)
            self.assertEqual(qc['literal_NA_rows'], 2)
            self.assertEqual(total, [5] * 14)
            self.assertNotIn('NA', named)

    def test_duplicate_identifiable_gene_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'counts.gz'
            with gzip.open(p, 'wt') as f:
                f.write('\t'.join(self.header()) + '\n')
                for name in ['STMN2', 'STMN2']:
                    f.write(name + '\t' + '\t'.join(['1'] * 14) + '\n')
            with self.assertRaises(ValueError):mod.read_counts(p)

    def test_interval_overlap_is_chromosome_specific_and_inclusive(self):
        self.assertTrue(mod.overlaps('chr1', 1, 10, ('chr1', 10, 20)))
        self.assertFalse(mod.overlaps('chr2', 1, 10, ('chr1', 10, 20)))
