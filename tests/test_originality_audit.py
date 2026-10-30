import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('originality', ROOT / 'scripts/audit_originality.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class OriginalityAuditTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'research/references/originality_evidence_20261029.json').read_text())

    def test_curated_register_consistent(self):
        self.assertEqual(mod.validate(self.data), [])

    def test_preprint_not_independent_replication(self):
        duplicate = copy.deepcopy(self.data['studies'][0])
        duplicate['id'] = 'duplicate_version'
        self.data['studies'].append(duplicate)
        self.assertIn('version assigned to multiple families', mod.validate(self.data))

    def test_abstract_cannot_verify_methods(self):
        self.data['studies'][0].update(access='abstract', methods_verified=True)
        self.assertTrue(any('abstract cannot' in e for e in mod.validate(self.data)))

    def test_post_knockdown_is_not_measured_deficit(self):
        self.data['studies'][0]['after_measured_deficit'] = 'yes'
        self.data['studies'][0].pop('baseline_locator', None)
        self.assertTrue(any('baseline locator' in e for e in mod.validate(self.data)))

    def test_negative_search_cannot_certify_novelty(self):
        self.data['claims'][0]['novelty_proven'] = True
        self.assertTrue(any('novelty not established' in e for e in mod.validate(self.data)))

    def test_future_sources_excluded(self):
        self.data['studies'][0]['date'] = '2027-01-01'
        self.assertTrue(any('after cutoff' in e for e in mod.validate(self.data)))

    def test_evidence_must_have_locator(self):
        self.data['studies'][0]['locator'] = ''
        self.assertTrue(any('missing evidence locator' in e for e in mod.validate(self.data)))

    def test_unknown_sources_rejected(self):
        self.data['claims'][0]['studies'].append('invented')
        self.assertTrue(any('unknown study' in e for e in mod.validate(self.data)))
