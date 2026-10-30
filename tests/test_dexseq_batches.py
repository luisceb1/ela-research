import unittest
from scripts.describe_dexseq_batches import fractions,direction
class BatchTests(unittest.TestCase):
    def test_library_scaling_invariance(self):
        fs=fractions([{'a':'1','b':'10'},{'a':'3','b':'30'}],['a','b'])
        self.assertEqual(fs[0]['a'],fs[0]['b'])
        self.assertEqual(sum(r['a'] for r in fs),1)
    def test_zero_denominator_rejected(self):
        with self.assertRaises(ValueError):fractions([{'a':'0'}],['a'])
    def test_sign_reversal(self):self.assertEqual(direction(.1,-.1),'opposite_direction')
    def test_zero_not_concordance(self):self.assertEqual(direction(0,.1),'zero_in_at_least_one_batch')
