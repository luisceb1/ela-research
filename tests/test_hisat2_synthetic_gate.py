import unittest
from scripts.hisat2_synthetic_gate import reverse_complement, accepted_pysam


class FakeRead:
    is_paired=False
    is_unmapped=False
    is_secondary=False
    is_supplementary=False
    is_qcfail=False
    mapping_quality=60
    def __init__(self, **values):
        self.tags={'NH':1,'XS':'+'}
        self.__dict__.update(values)
    def has_tag(self,k):return k in self.tags
    def get_tag(self,k):return self.tags[k]


class SyntheticGateUnitTests(unittest.TestCase):
    def test_reverse_complement_involution(self):
        s='AACCGTNN';self.assertEqual(reverse_complement(s),'NNACGGTT')
        self.assertEqual(reverse_complement(reverse_complement(s)),s)
    def test_primary_unique_pass(self):
        self.assertTrue(accepted_pysam(FakeRead()))
    def test_multi_and_missing_tags_rejected(self):
        for tags in [{'NH':2,'XS':'+'},{'NH':1},{'XS':'+'},{'NH':1,'XS':'.'}]:
            self.assertFalse(accepted_pysam(FakeRead(tags=tags)))
    def test_mapq_policy(self):
        for q in [0,19,255]:self.assertFalse(accepted_pysam(FakeRead(mapping_quality=q)))
        self.assertTrue(accepted_pysam(FakeRead(mapping_quality=20)))
    def test_excluded_record_classes(self):
        for flag in ['is_unmapped','is_secondary','is_supplementary','is_qcfail']:
            self.assertFalse(accepted_pysam(FakeRead(**{flag:True})))
    def test_paired_records_not_silently_accepted(self):
        with self.assertRaises(ValueError):accepted_pysam(FakeRead(is_paired=True))


if __name__=='__main__':unittest.main()
