import importlib.util
import io
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / 'scripts/reproduce_stmn2_papa.py'
spec = importlib.util.spec_from_file_location('reproduce_stmn2_papa', path)
reproduction = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reproduction)


class ReproductionControls(unittest.TestCase):
    def sample(self):
        return [{'gsm': 'GSM1', 'library': 'lib1', 'author_label': 'A', 'group': 'control'}]

    def counts(self):
        return {'g_1': {'A': 1.0}, 'g_2': {'A': 3.0}}

    def test_known_equal_proportion_passes(self):
        ppau = {'g_1': {'A': .25}, 'g_2': {'A': .75}}
        row, = reproduction.compare(self.counts(), ppau, self.sample(), 'g_1', 1e-6, 1.0)
        self.assertEqual(row['status'], 'pass')
        self.assertEqual(row['estimated_count_denominator'], 4)

    def test_documented_percent_units_converted_without_search(self):
        ppau = {'g_1': {'A': 25}, 'g_2': {'A': 75}}
        row, = reproduction.compare(self.counts(), ppau, self.sample(), 'g_1', 1e-6, 100.0)
        self.assertEqual(row['status'], 'pass')
        with self.assertRaises(ValueError):
            reproduction.compare(self.counts(), ppau, self.sample(), 'g_1', 1e-6, 1.0)

    def test_count_and_tpm_estimands_not_forced_to_agree(self):
        ppau = {'g_1': {'A': .1}, 'g_2': {'A': .9}}
        row, = reproduction.compare(self.counts(), ppau, self.sample(), 'g_1', 1e-6, 1.0)
        self.assertEqual(row['status'], 'fail')
        self.assertEqual(row['counts_based_proportion'], .25)
        self.assertEqual(row['author_ppau_proportion'], .1)

    def test_tolerance_failure_retained(self):
        ppau = {'g_1': {'A': .250002}, 'g_2': {'A': .749998}}
        row, = reproduction.compare(self.counts(), ppau, self.sample(), 'g_1', 1e-6, 1.0)
        self.assertEqual(row['status'], 'fail')
        self.assertEqual(row['tolerance'], 1e-6)

    def test_zero_denominator_is_indeterminate_not_zero(self):
        counts = {'g_1': {'A': 0}, 'g_2': {'A': 0}}
        ppau = {'g_1': {'A': 0}, 'g_2': {'A': 0}}
        row, = reproduction.compare(counts, ppau, self.sample(), 'g_1', 1e-6, 1.0)
        self.assertIsNone(row['counts_based_proportion'])
        self.assertEqual(row['status'], 'indeterminate')

    def test_missing_denominator_group_rejected(self):
        with self.assertRaises(ValueError):
            reproduction.compare(self.counts(), {'g_1': {'A': .25}}, self.sample(), 'g_1', 1e-6, 1.0)

    def test_all_target_groups_in_full_table_included(self):
        matrix = 'le_id\tgene_id\tA\ng_1\tg\t1\nother\th\t100\ng_2\tg\t3\ng_3\tg\t6\n'
        counts, n = reproduction.target_matrix(io.StringIO(matrix), 'g', ['A'])
        ppau = {'g_1': {'A': .1}, 'g_2': {'A': .3}, 'g_3': {'A': .6}}
        row, = reproduction.compare(counts, ppau, self.sample(), 'g_1', 1e-6, 1.0)
        self.assertEqual(n, 4)
        self.assertEqual(row['estimated_count_denominator'], 10)
        self.assertEqual(row['status'], 'pass')

    def test_duplicate_column_or_group_rejected(self):
        for text in ['le_id\tgene_id\tA\tA\ng_1\tg\t1\t2\n',
                     'le_id\tgene_id\tA\ng_1\tg\t1\ng_1\tg\t2\n']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                reproduction.target_matrix(io.StringIO(text), 'g', ['A'])

    def test_invalid_target_abundances_rejected(self):
        for value in ['nan', 'inf', '-1']:
            text = f'le_id\tgene_id\tA\ng_1\tg\t{value}\n'
            with self.subTest(value=value), self.assertRaises(ValueError):
                reproduction.target_matrix(io.StringIO(text), 'g', ['A'])


if __name__ == '__main__':
    unittest.main()
