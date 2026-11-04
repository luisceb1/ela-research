"""Rounding/denominator controls; these fixtures are not experimental evidence."""
from decimal import Decimal
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from reproduce_asadollahi_fig3s_descriptive import arithmetic_mean, check_mean, published_mean, reproduce


class DescriptiveReproductionTests(unittest.TestCase):
    def test_published_precision_sets_rounding_tolerance(self):
        self.assertEqual(published_mean('24.2 ± ignored')[2], Decimal('.05'))
        self.assertEqual(published_mean('24.20 ± ignored')[2], Decimal('.005'))

    def test_boundary_is_inclusive_and_just_outside_fails(self):
        self.assertTrue(check_mean([Decimal('24.25')], '24.2 ± ignored')['within_published_rounding'])
        self.assertFalse(check_mean([Decimal('24.250001')], '24.2 ± ignored')['within_published_rounding'])

    def test_all_values_and_zero_are_in_the_denominator(self):
        self.assertEqual(arithmetic_mean([Decimal(0), Decimal(3), Decimal(3)]), Decimal(2))
        with self.assertRaisesRegex(ValueError, 'empty_group'):
            arithmetic_mean([])

    def test_ambiguous_or_nonfinite_data_are_not_repaired(self):
        with self.assertRaisesRegex(ValueError, 'published_mean_not_unambiguous_decimal'):
            published_mean('24,2 ± ignored')
        with self.assertRaisesRegex(ValueError, 'nonfinite_observation'):
            arithmetic_mean([Decimal('NaN')])

    def test_count_mismatch_stops_before_summary_comparison(self):
        rows = [{'source_cell': 'I4', 'published_group': 'UNC13AWT', 'initial_epsc_charge_pC': '1'},
                {'source_cell': 'J4', 'published_group': 'UNC13AR202H', 'initial_epsc_charge_pC': '1'}]
        with self.assertRaisesRegex(ValueError, 'published_count_mismatch'):
            reproduce(rows, {'UNC13AWT': '1 ± ignored', 'UNC13AR202H': '1 ± ignored'},
                      {'UNC13AWT': 2, 'UNC13AR202H': 1})


if __name__ == '__main__':
    unittest.main()
