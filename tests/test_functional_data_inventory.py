import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('functional_inventory', ROOT / 'scripts/inventory_functional_data.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class InventoryTests(unittest.TestCase):
    def record(self):
        return dict(id='synthetic_contract', version='synthetic_not_experiment', locator='fixture',
                    timing='post_deficit', data_access='retrieved', verified={k: True for k in mod.REQUIRED})

    def test_complete_contract_positive_control(self):
        self.assertTrue(mod.assess(self.record())['reconstructible_from_inspected_materials'])

    def test_each_missing_link_blocks(self):
        for key in mod.REQUIRED:
            with self.subTest(key=key):
                r = self.record();r['verified'][key] = None
                self.assertFalse(mod.assess(r)['reconstructible_from_inspected_materials'])

    def test_numeric_rows_are_not_replication(self):
        r = self.record();r['verified']['biological_batch_key'] = 133
        with self.assertRaises(ValueError):mod.assess(r)

    def test_prevention_does_not_become_post_deficit(self):
        for timing in mod.KNOWN_OTHER_TIMING:
            r = self.record();r['timing'] = timing
            self.assertFalse(mod.assess(r)['reconstructible_from_inspected_materials'])

    def test_declaration_is_not_downloaded_data(self):
        r = self.record();r['data_access'] = 'declared_only'
        self.assertFalse(mod.assess(r)['reconstructible_from_inspected_materials'])

    def test_unknown_distinct_from_missing(self):
        r = self.record();r['verified']['unit_key'] = None
        self.assertIn('unit_key:not_verified', mod.assess(r)['blockers'])
        r['verified']['unit_key'] = False
        self.assertIn('unit_key:missing_in_inspected_projection', mod.assess(r)['blockers'])

    def test_locator_required(self):
        r = self.record();r['locator'] = ''
        with self.assertRaises(ValueError):mod.assess(r)
