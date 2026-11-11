import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from paired_stmn2 import select_pairs, summarize, sign_test

class PairedSTMN2Tests(unittest.TestCase):
    def row(self, donor='D', c=30, k=0, prep='Manual KAPA Total'):
        return dict(donor=donor,c=c,k=k,prep=prep,group='ALS Spectrum MND')

    def test_exact_sign_tail_and_ties(self):
        self.assertEqual(sign_test([1]*5+[0]*100),0.0625)
        self.assertEqual(sign_test([1,-1]),1)
        self.assertIsNone(sign_test([0,0]))
        self.assertEqual(sign_test([1]*10),2/1024)

    def test_zero_cryptic_control_is_eligible(self):
        pairs,_=select_pairs([self.row()],[self.row(k=10)],'ALS Spectrum MND',20)
        self.assertEqual(len(pairs),1)

    def test_multiplicity_rejected_before_coverage(self):
        pairs,flow=select_pairs([self.row(),self.row(c=0)],[self.row(k=10)],'ALS Spectrum MND',20)
        self.assertEqual(pairs,[])
        self.assertEqual(flow['exclusions_in_order'],{'multiplicity':1})

    def test_mismatched_preparation_excluded(self):
        pairs,flow=select_pairs([self.row()],[self.row(prep='Automated KAPA Total')],'ALS Spectrum MND',20)
        self.assertFalse(pairs)
        self.assertEqual(flow['exclusions_in_order'],{'preparation_mismatch':1})

    def test_gate_enforces_pairs_and_nonzero_differences(self):
        self.assertIsNone(summarize([(self.row(),self.row(k=10))]*9,True)['two_sided_exact_sign_p'])
        self.assertIsNone(summarize([(self.row(),self.row())]*10,True)['two_sided_exact_sign_p'])
        result=summarize([(self.row(),self.row(k=10))]*10,True)
        self.assertEqual(result['two_sided_exact_sign_p'],2/1024)
        self.assertEqual(result['median_paired_difference'],.25)

    def test_threshold_applies_to_both_regions(self):
        pairs,_=select_pairs([self.row(c=19)],[self.row(k=20)],'ALS Spectrum MND',20)
        self.assertFalse(pairs)

if __name__=='__main__':unittest.main()
