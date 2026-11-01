import unittest
from pathlib import Path
from scripts.audit_stmn2_exon1_mappability import tile,rc,evaluate_tile,audit_definition


class ExonMappabilityTests(unittest.TestCase):
    def test_exhaustive_tiles_and_shared_interval(self):
        s=('ACGT'*25)[:98]
        a=list(tile('exon1',s,79611116,50));b=list(tile('exon1',s,79611116,51))
        self.assertEqual((len(a),len(b)),(98,96))
        self.assertEqual(sum(r['inside_shared63'] for r in a+b),54)
        self.assertEqual(len({r['name'] for r in a+b}),194)
    def test_tile_source_coordinates_and_reverse(self):
        rows=list(tile('exon2','AACCGGTT',100,5))
        self.assertEqual(rows[0]['expected_pos_1based'],101)
        self.assertEqual(rows[-1]['expected_pos_1based'],104)
        self.assertEqual(rows[1]['sequence'],rc(rows[0]['sequence']))
    def test_invalid_lengths_rejected(self):
        for n in (0,5):
            with self.assertRaises(ValueError):list(tile('exon2','ACGT',0,n))
    def test_reverse_complement_roundtrip(self):
        s='AACCGT';self.assertEqual(rc(rc(s)),s)
    def expected(self):return {'expected_pos_1based':123,'reverse':False,'length':50}
    def record(self,**extra):
        r={'flag':0,'NH':1,'MAPQ':60,'chrom':'chr8','pos':123,'cigar':'50M','NM':0};r.update(extra);return r
    def test_perfect_source_passes(self):
        self.assertEqual(evaluate_tile(self.expected(),self.record()),'exact_unique_source')
    def test_multimap_and_low_mapq_not_accepted(self):
        for r in [self.record(NH=2),self.record(NH=None),self.record(MAPQ=19),self.record(MAPQ=255)]:
            self.assertNotEqual(evaluate_tile(self.expected(),r),'exact_unique_source')
    def test_wrong_coordinate_orientation_or_partial_rejected(self):
        for r in [self.record(pos=124),self.record(chrom='chr19'),self.record(flag=16),self.record(cigar='1S49M'),self.record(NM=1)]:
            self.assertNotEqual(evaluate_tile(self.expected(),r),'exact_unique_source')
    def test_versioned_definition(self):
        root=Path(__file__).resolve().parents[1]
        r=audit_definition(root/'reports/isoforms/exons.tsv')
        self.assertEqual(len(r['selected_exons']),6)
        self.assertTrue(r['not_independent_GTF_reconstruction'])


if __name__=='__main__':unittest.main()
