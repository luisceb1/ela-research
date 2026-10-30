import tempfile
import unittest
from pathlib import Path
from scripts.audit_dexseq_coverage import scaled, aggregate, load_design

class CoverageTests(unittest.TestCase):
    def test_library_scaling_invariant(self):
        self.assertEqual(scaled(2,10,100),scaled(20,100,1000))
    def test_zero_bin_not_pseudocounted(self):
        self.assertEqual(scaled(0,10,100),{'within_gene_pp':0,'other_bins_ratio':0,'assigned_bin_CPM':0})
    def test_only_bin_other_denominator_not_evaluable(self):
        self.assertIsNone(scaled(10,10,100)['other_bins_ratio'])
    def test_bad_hierarchy_and_noninteger_rejected(self):
        for args in [(11,10,100),(1,10,9),(0,0,100),(-1,10,100),(1.0,10,100),(1,10,float('nan'))]:
            with self.assertRaises(ValueError):scaled(*args)
    def test_zeros_counts_and_order_aggregated(self):
        self.assertEqual(aggregate([0,10,20,30]),aggregate([30,20,10,0]))
        self.assertEqual(aggregate([0,10,20,30]),dict(min_count=0,median_count=15,max_count=30,sum_count=60,zero_libraries=1,libraries_ge10=3))
    def test_invalid_vectors(self):
        for values in [[],[0,-1],[1,float('inf')],[float('nan')]]:
            with self.assertRaises(ValueError):aggregate(values)
    def test_duplicate_or_incomplete_design(self):
        src=Path('reports/gse121569-design/dexseq_column_map.tsv').read_text().splitlines()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'design.tsv'
            for rows in [src[:-1],src[:-1]+[src[1]]]:
                p.write_text('\n'.join(rows)+'\n')
                with self.assertRaises(ValueError):load_design(p)
