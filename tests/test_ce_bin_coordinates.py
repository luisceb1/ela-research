import unittest
from scripts.audit_ce_bin_coordinates import interval,relation

class CECoordinateTests(unittest.TestCase):
    def i(self,s,e,**kw):return interval(kw.get('chrom','chr8'),s,e,kw.get('assembly','hg19'),kw.get('strand'))
    def test_identical_positive_control(self):self.assertEqual(relation(self.i(10,20),self.i(10,20))['overlap_bp'],11)
    def test_containment_positive_control(self):self.assertEqual(relation(self.i(1,30),self.i(10,20))['overlap_bp'],11)
    def test_shared_endpoint_and_adjacency(self):
        self.assertEqual(relation(self.i(10,20),self.i(20,30))['overlap_bp'],1)
        self.assertEqual(relation(self.i(10,20),self.i(21,30)),dict(overlap_bp=0,boundary_distance_bp=1,intervening_bases=0))
    def test_gap_not_boundary_distance(self):
        self.assertEqual(relation(self.i(10,20),self.i(25,30)),dict(overlap_bp=0,boundary_distance_bp=5,intervening_bases=4))
    def test_assembly_mismatch_rejected(self):
        with self.assertRaises(ValueError):relation(self.i(10,20),self.i(10,20,assembly='hg38'))
    def test_chromosome_strand_and_unspecified_strand(self):
        self.assertIsNone(relation(self.i(10,20),self.i(10,20,chrom='chr19')))
        self.assertIsNone(relation(self.i(10,20,strand='+'),self.i(10,20,strand='-')))
        self.assertEqual(relation(self.i(10,20,strand='+'),self.i(10,20))['overlap_bp'],11)
    def test_invalid_coordinates(self):
        for args in [('chr8',0,20,'hg19'),('chr8',20,10,'hg19'),('8',10,20,'hg19'),('chr8',1.5,20,'hg19')]:
            with self.assertRaises(ValueError):interval(*args)
