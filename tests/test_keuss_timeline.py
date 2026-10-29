import unittest
from scripts.keuss_timeline import classify
class TimelineTests(unittest.TestCase):
 def test_late_kd_with_early_aso_is_prevention(self):self.assertEqual(classify(33,14),'before_perturbation')
 def test_concurrent(self):self.assertEqual(classify(45,45),'concurrent')
 def test_after_kd_is_not_automatically_reversal(self):self.assertEqual(classify(14,33),'after_perturbation_not_yet_proof_of_reversal')
 def test_invalid_day(self):
  with self.assertRaises(ValueError):classify(-1,14)
