"""Artificial parser/guard controls; fixtures contain no biological observations."""
import copy
import importlib.util
from pathlib import Path
import unittest

P = Path(__file__).resolve().parents[1] / 'scripts/adapt_k26_conditional_source.py'
SPEC = importlib.util.spec_from_file_location('k26_adapter', P)
M = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)

class ConditionalAdapterTests(unittest.TestCase):
    def fixture(self):
        cells = {'A1': 'Figure 4d, Measurement of evoked EPSCs in spinal motor neuron', **M.HEADERS}
        for row, batch in [(4, 'Batch 1'), (17, 'Batch 2'), (32, 'Batch 3')]:
            cells[f'A{row}'] = batch
            for col in 'BCD': cells[f'{col}{row}'] = '0.125'
        return cells

    def parse(self, cells):
        return M.observations(cells, {'Control': 3, 'KD': 3, 'KD_ASO': 3})

    def test_nA_values_and_exact_source_coordinates_survive(self):
        rows = self.parse(self.fixture())
        self.assertEqual(rows[0]['value_nA'], '0.125')
        self.assertEqual(rows[0]['source_cell'], '4d!B4')
        self.assertEqual(rows[0]['condition'], 'KD')
        self.assertNotIn('cell_id', rows[0]); self.assertNotIn('differentiation_id', rows[0])

    def test_blank_is_not_zero_and_counts_must_reconcile(self):
        cells = self.fixture(); del cells['B4']
        with self.assertRaisesRegex(ValueError, 'counts'): self.parse(cells)

    def test_negative_and_nonfinite_values_are_not_repaired(self):
        for v in ['-1', 'NaN', 'inf']:
            with self.subTest(value=v):
                cells = self.fixture(); cells['B4'] = v
                with self.assertRaisesRegex(ValueError, 'Nonfinite/negative'): self.parse(cells)

    def test_missing_or_repeated_blocks_are_rejected(self):
        for replacement in ['', 'Batch 1']:
            cells = self.fixture(); cells['A17'] = replacement
            with self.assertRaises(ValueError): self.parse(cells)

    def test_numeric_entry_cannot_precede_first_batch(self):
        cells = self.fixture(); del cells['A4']
        with self.assertRaisesRegex(ValueError, 'without declared batch'): self.parse(cells)

    def test_header_drift_and_extra_rows_are_rejected(self):
        cells = self.fixture(); cells['B3'] = 'Control'
        with self.assertRaisesRegex(ValueError, 'header'): self.parse(cells)
        cells = self.fixture(); cells['B45'] = '9'
        with self.assertRaisesRegex(ValueError, 'extra data'): self.parse(cells)

    def test_changed_original_bytes_fail_before_zip_parsing(self):
        with self.assertRaisesRegex(ValueError, 'SHA256'): M.pinned_cells(b'artificial invalid source')

    def test_contract_cannot_claim_strict_gate_or_change_units(self):
        contract = {'schema_version': 'FR-K26-4d-conditional-v2', 'enabled_for_conditional_replay': True,
                    'strict_v1_gate_passed': False, 'unit': 'nA_magnitude', 'source_sha256': M.SOURCE_SHA256,
                    'expected_counts': M.COUNTS, 'source_batch_labels': M.BATCHES}
        M.check_contract(contract)
        for key, value in [('strict_v1_gate_passed', True), ('unit', 'pA_magnitude')]:
            changed = copy.deepcopy(contract); changed[key] = value
            with self.assertRaisesRegex(ValueError, 'contract mismatch'): M.check_contract(changed)

if __name__ == '__main__': unittest.main()
