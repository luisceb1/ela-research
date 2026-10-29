"""Numerical and small-group failure controls, without inferential testing."""
import unittest
from scripts import describe_targets as d


class DescriptiveTests(unittest.TestCase):
    def test_zero_baseline_is_na_not_pseudocount(self):
        self.assertEqual(d.ratio(24, 0), '')
        self.assertEqual(d.ratio(0, 0), '')
        self.assertEqual(d.ratio(0, 2), 0)

    def test_small_group_loo_can_reverse_direction(self):
        result = d.loo_summary([1., 3.], [2., 2.])
        self.assertEqual(result['mean_ratio_to_CTL'], 1.)
        self.assertEqual(result['sensitivity_ratio_min'], .5)
        self.assertEqual(result['sensitivity_ratio_max'], 1.5)
        self.assertTrue(result['direction_spans_one'])
        self.assertEqual(result['undefined_ratios'], 0)

    def test_zero_control_deletion_not_silently_removed(self):
        result = d.loo_summary([2., 2.], [0., 2.])
        self.assertEqual(result['undefined_ratios'], 1)
        self.assertEqual(result['sensitivity_ratio_min'], 1.)
        self.assertEqual(result['sensitivity_ratio_max'], 2.)

    def test_all_zero_controls_are_not_finite_fold_change(self):
        result = d.loo_summary([2., 4.], [0., 0.])
        self.assertEqual(result['mean_ratio_to_CTL'], '')
        self.assertEqual(result['sensitivity_ratio_min'], '')
        self.assertEqual(result['undefined_ratios'], 5)

    def test_single_library_group_rejected(self):
        with self.assertRaises(ValueError):
            d.loo_summary([1.], [1., 2.])


if __name__ == '__main__':
    unittest.main()
