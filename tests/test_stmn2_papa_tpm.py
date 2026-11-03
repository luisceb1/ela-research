import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

path = Path(__file__).resolve().parents[1] / 'scripts/reproduce_stmn2_papa_tpm.py'
spec = importlib.util.spec_from_file_location('reproduce_stmn2_papa_tpm', path)
tpm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tpm)


class TPMMeasurementControls(unittest.TestCase):
    def test_tpm_measurement_preserves_value_and_removes_count_labels(self):
        rows = [{'estimated_count_numerator': 10, 'estimated_count_denominator': 100,
                 'counts_based_proportion': .1, 'status': 'pass'}]
        converted, = tpm.tpm_rows(rows)
        self.assertEqual(converted['tpm_numerator'], 10)
        self.assertEqual(converted['tpm_denominator'], 100)
        self.assertEqual(converted['tpm_based_proportion'], .1)
        self.assertFalse(any('count' in key for key in converted))
        self.assertIn('counts_based_proportion', rows[0])

    def test_correct_tpm_formula_passes_while_different_count_estimand_fails(self):
        samples = [{'gsm': 'GSM1', 'library': 'A', 'author_label': 'A', 'group': 'control'}]
        published = {'g_1': {'A': .1}, 'g_2': {'A': .9}}
        abundance = {'g_1': {'A': 10}, 'g_2': {'A': 90}}
        length_scaled_counts = {'g_1': {'A': 25}, 'g_2': {'A': 75}}
        positive, = tpm.shared.compare(abundance, published, samples, 'g_1', 1e-6, 1)
        negative, = tpm.shared.compare(length_scaled_counts, published, samples, 'g_1', 1e-6, 1)
        self.assertEqual(positive['status'], 'pass')
        self.assertEqual(negative['status'], 'fail')

    def test_changed_input_rejected_by_pinned_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / 'tpm.tsv'
            file.write_bytes(b'original')
            expected = {'tpm': hashlib.sha256(b'original').hexdigest()}
            self.assertEqual(tpm.verify_inputs({'tpm': file}, expected), expected)
            file.write_bytes(b'altered')
            with self.assertRaises(ValueError):
                tpm.verify_inputs({'tpm': file}, expected)


if __name__ == '__main__':
    unittest.main()
