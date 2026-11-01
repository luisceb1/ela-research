import copy
import unittest
from scripts.gse122069_full_control import Bins
from scripts.summarize_gse122069_full_control import summarize


class FullSummaryTests(unittest.TestCase):
    def data(self):
        b=Bins(1,2);b.start('a',True);b.start('b',True);text=b.finish();hts=copy.deepcopy(text);hts['locus_bins']=[{},{}]
        return text,hts
    def test_partial_does_not_classify_full_coverage(self):
        a,b=self.data();s=summarize({'complete_library':False},a,b,{})
        self.assertIsNone(s['complete_control_coverage_criterion_met']);self.assertEqual(s['concordant_completed_reads'],2)
    def test_false_full_claim_rejected(self):
        a,b=self.data()
        with self.assertRaises(ValueError):summarize({'complete_library':True},a,b,{})
    def test_completed_prefix_mismatch_rejected(self):
        a,b=self.data();b['completed_bins'][0]['sam_records']+=1
        with self.assertRaises(ValueError):summarize({},a,b,{})
    def test_noncontiguous_prefix_rejected(self):
        a,b=self.data();a['completed_bins'][1]['first_read']=3;b=copy.deepcopy(a)
        with self.assertRaises(ValueError):summarize({},a,b,{})

if __name__=='__main__':unittest.main()
