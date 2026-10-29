import unittest
from scripts.audit_regeneration_timing import extract
class TimingTests(unittest.TestCase):
 def test_injury_not_genetic_deficiency(self):
  r=extract('3 d after transduction, neurons were axotomized')
  self.assertEqual(r['intervention_minus_axotomy_days'],-3)
  self.assertIn('not genetic',r['time_origin'])
 def test_generic_wording_not_enough(self):
  with self.assertRaises(ValueError):extract('Restoration rescued regeneration after injury')
 def test_explicit_interval_preserved(self):self.assertEqual(extract('5 d after transduction, neurons were axotomized')['intervention_minus_axotomy_days'],-5)
