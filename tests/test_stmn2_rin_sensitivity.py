import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from stmn2_rin_sensitivity import compatibility,qc_pass,interpretation,guard_baseline

class RINSensitivityTests(unittest.TestCase):
    def record(self):return dict(donor='D',prep='Manual KAPA Total')
    def qc(self,**kw):return dict(dict(donor_id='D',rna_prep='Manual KAPA Total',tissue_full='R',rin='6'),**kw)
    def test_compatible_zero_cryptic_not_excluded(self):
        r=self.record();r.update(c=30,k=0)
        self.assertEqual(compatibility(r,[self.qc()],'R'),(6,None))
    def test_nonfinite_missing_and_out_of_range(self):
        for value in ['',None,'NaN','inf','0','11']:
            q=self.qc();q['rin']=value
            self.assertEqual(compatibility(self.record(),[q],'R')[1],'invalid_rin')
    def test_mismatches_and_duplicate_records(self):
        for field,value,reason in [('donor_id','X','donor_mismatch'),('tissue_full','S','region_mismatch'),('rna_prep','X','preparation_mismatch')]:
            q=self.qc();q[field]=value
            self.assertEqual(compatibility(self.record(),[q],'R')[1],reason)
        self.assertEqual(compatibility(self.record(),[self.qc(),self.qc()],'R')[1],'missing_or_duplicate_metadata')
    def test_inclusive_threshold_and_pair_difference(self):
        self.assertTrue(qc_pass(({'rin':6},{'rin':7}),6))
        self.assertFalse(qc_pass(({'rin':5.99},{'rin':6}),6))
        self.assertFalse(qc_pass(({'rin':6},{'rin':7.01}),6))
    def test_baseline_guard_and_small_n(self):
        with self.assertRaises(ValueError):guard_baseline([1]*44)
        guard_baseline([1]*45)
        self.assertEqual(interpretation(9,.1),'insufficient_pairs')
        self.assertEqual(interpretation(10,0),'directional_prediction_not_supported')
        self.assertEqual(interpretation(10,.1),'positive_median_persists_descriptively')

if __name__=='__main__':unittest.main()
