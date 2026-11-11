import gzip
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('audit', Path(__file__).resolve().parents[1] / 'scripts/audit_stmn2_units.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class TechnicalUnitAuditTests(unittest.TestCase):
    def sample(self, rail='1', c=30, k=0):
        return dict(rail_id=rail, group='test', counts=dict(canonical=c, cryptic=k))

    def test_exact_suffix_distinguishes_libraries(self):
        rows = [dict(key='LIB', donor='D1', tissue='R'), dict(key='LIB-2', donor='D2', tissue='R')]
        idx, bad = a.build_index(rows, ('key',), 'donor', 'tissue')
        project = [dict(rail_id='1', external_id='LIB-2', project='R')]
        joined, failures = a.join_samples([self.sample()], project, idx, bad, 'R')
        self.assertEqual(joined['1']['donor'], 'D2')
        self.assertFalse(failures)

    def test_conflicting_metadata_quarantined(self):
        rows = [dict(key='L', donor=d, tissue='R') for d in ['D1','D1','D2']]
        idx, bad = a.build_index(rows, ('key',), 'donor', 'tissue')
        self.assertNotIn('L', idx)
        self.assertEqual(bad, {'L'})

    def test_consistent_duplicate_rows_collapse(self):
        row = dict(key='L', donor='D1', tissue='R')
        idx, bad = a.build_index([row, row], ('key',), 'donor', 'tissue')
        self.assertEqual(len(idx), 1)
        self.assertFalse(bad)

    def test_rail_ids_are_scoped_to_region(self):
        project = [dict(rail_id='1', external_id='A', project='R'), dict(rail_id='1', external_id='B', project='S')]
        idx = {'A': ('D1', 'R', ()), 'B': ('D2', 'S', ())}
        joined, failures = a.join_samples([self.sample()], project, idx, set(), 'R')
        self.assertEqual(joined['1']['external'], 'A')
        self.assertFalse(failures)

    def test_conflicting_rail_within_region_rejected(self):
        project = [dict(rail_id='1', external_id=k, project='R') for k in ['A','B']]
        joined, failures = a.join_samples([self.sample()], project, {}, set(), 'R')
        self.assertFalse(joined)
        self.assertEqual(failures['conflicting_project_rail'], 1)

    def test_missing_donor_and_wrong_tissue_rejected(self):
        project = [dict(rail_id=str(i), external_id=k, project='R') for i,k in [(1,'A'),(2,'B')]]
        idx = {'A': ('','R',()), 'B': ('D2','S',())}
        joined, failures = a.join_samples([self.sample('1'), self.sample('2')], project, idx, set(), 'R')
        self.assertFalse(joined)
        self.assertEqual(dict(failures), dict(missing_donor=1, metadata_region_mismatch=1))

    def test_duplicate_input_rail_not_silently_collapsed(self):
        with self.assertRaisesRegex(ValueError, 'duplicate rail'):
            a.join_samples([self.sample(), self.sample()], [], {}, set(), 'R')

    def test_project_mismatch_rejected_even_with_matching_region(self):
        project = [dict(rail_id='1', external_id='L', project='R')]
        joined, failures = a.join_samples([self.sample()], project,
            {'L':('D','R',('OTHER',))}, set(), 'R', 'TARGET')
        self.assertFalse(joined)
        self.assertEqual(failures['metadata_project_mismatch'], 1)

    def test_denominator_filter_does_not_require_cryptic_positive(self):
        stats = a.descriptives([self.sample('1', 30, 0), self.sample('2', 0, 2), self.sample('3', 0, 0)])['test']
        self.assertEqual(stats['nonzero_denominator'], dict(n=2, median=0.5, max=1.0))
        self.assertEqual(stats['denominator_ge20'], dict(n=1, median=0.0, max=0.0))

    def test_chain_maps_bases_not_gap_or_constant_offset(self):
        chain = 'chain 1 chr8 1000 + 100 125 chr8 2000 + 200 229 1\n10 5 9\n10\n\nchain 1 chr9 1000 + 10 20 chr9 1000 - 100 110 2\n10\n'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'chain.gz'
            path.write_bytes(gzip.compress(chain.encode()))
            out = a.mapped_chain_positions(path, 'chr8', [109,110,115,124,125])
            self.assertEqual(out[109][0]['position0'], 209)
            self.assertEqual(out[110], [])
            self.assertEqual(out[115][0]['position0'], 219)
            self.assertEqual(out[125], [])
            reverse = a.mapped_chain_positions(path, 'chr9', [10,19])
            self.assertEqual([reverse[p][0]['position0'] for p in [10,19]], [899,890])

    def test_aggregate_summary_counts_donors_without_exporting_keys(self):
        samples = [self.sample('1',30,20), self.sample('2',30,21)]
        joined = {k:dict(donor='SENSITIVE_SYNTHETIC_DONOR') for k in ['1','2']}
        result = a.mapping_summary(samples, joined, {})
        self.assertEqual(result['distinct_declared_donors_with_cryptic_ge20'], 1)
        self.assertEqual(result['donors_with_multiple_samples_in_this_region'], 1)
        self.assertNotIn('SENSITIVE_SYNTHETIC_DONOR', json.dumps(result))

    def test_normalize_before_median_and_reject_nonpositive_depth(self):
        x = [self.sample('1',10), self.sample('2',100), self.sample('3',30)]
        y = [self.sample('1',1), self.sample('2',50), self.sample('3',1)]
        for sample in x+y:
            sample['group'] = 'ALS Spectrum MND'
        fields = ['star.number_of_input_reads_both','star.uniquely_mapped_reads_number_both','exon_fc_count_all.assigned']
        qc = [dict(rail_id=str(i), **{f:depth for f in fields}) for i,depth in [(1,100),(2,10000),(3,100)]]
        result = a.coverage_recheck(x,y,qc)['results'][fields[0]]
        self.assertEqual(result['ratio_of_medians'], 10)
        self.assertNotEqual(result['ratio_of_medians'], 30/1)
        qc[0][fields[0]] = 0
        with self.assertRaisesRegex(ValueError, 'nonpositive'):
            a.coverage_recheck(x,y,qc)


if __name__ == '__main__':
    unittest.main()
