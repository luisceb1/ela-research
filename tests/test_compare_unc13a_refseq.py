"""Coordinate and provenance controls for the independent annotation comparison."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import compare_unc13a_refseq as mod

ROOT = Path(__file__).resolve().parents[1]


class RefSeqTests(unittest.TestCase):
    def setUp(self):
        self.inventory = json.loads((ROOT / 'reports/unc13a-control-annotation-20261103/operator-audit-seal.json').read_bytes())
        self.reference = json.loads((ROOT / 'reports/source-gate-issue37-20261103/inputs/refseq-hg38.json').read_bytes())

    def test_real_frozen_inventory_reclassifies_only_one_prior_unmatched_junction(self):
        result = mod.compare(self.inventory, self.reference)
        self.assertEqual(result['reference_distinct_junctions'], 49)
        self.assertEqual(result['routes']['text15'], dict(observed=31, exact_matches=30, no_exact_match=1))
        self.assertEqual(result['routes']['text8'], dict(observed=33, exact_matches=32, no_exact_match=1))
        rows = [r for r in result['rows'] if (r['start0'], r['end0']) == (17627940, 17629242)]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r['curated_NM'] == 'NM_001387022.1' and r['predicted_XM'] == 'XM_017026502.2' for r in rows))
        self.assertFalse(result['gate_promoted'])

    def test_one_base_and_strand_mismatches_are_not_repaired(self):
        edges, _ = mod.reference_edges(self.reference)
        self.assertIn(('chr19', 17641556, 17642844, '-'), edges)
        self.assertNotIn(('chr19', 17641556, 17642845, '-'), edges)
        self.assertNotIn(('chr19', 17641556, 17642844, '+'), edges)
        self.assertNotIn(('chr19', 17648988, 17649507, '-'), edges)

    def test_invalid_or_truncated_reference_is_rejected(self):
        for change in ('genome', 'count', 'exons', 'empty', 'duplicate'):
            ref = copy.deepcopy(self.reference)
            if change == 'genome': ref['genome'] = 'hg19'
            elif change == 'count': ref['itemsReturned'] += 1
            elif change == 'exons': ref['ncbiRefSeq'][0]['exonCount'] += 1
            elif change == 'empty': ref['ncbiRefSeq'] = []; ref['itemsReturned'] = 0
            else: ref['ncbiRefSeq'].append(copy.deepcopy(ref['ncbiRefSeq'][0])); ref['itemsReturned'] += 1
            with self.subTest(change=change):
                self.assertRaises(ValueError, mod.reference_edges, ref)

    def test_partial_promoted_or_duplicate_inventory_is_rejected(self):
        for change in ('partial', 'promoted', 'duplicate', 'support'):
            inv = copy.deepcopy(self.inventory)
            if change == 'partial': inv['console_inventory_is_summary'] = True
            elif change == 'promoted': inv['gate_promoted'] = True
            elif change == 'duplicate':
                rows = inv['regional_audit']['routes']['text15']['junctions']; rows.append(copy.deepcopy(rows[0]))
            else: inv['regional_audit']['routes']['text15']['junctions'][0]['fragments'] = 0
            with self.subTest(change=change):
                self.assertRaises(ValueError, mod.compare, inv, self.reference)


if __name__ == '__main__':
    unittest.main()
