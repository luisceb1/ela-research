"""Coordinate convention/strand and measurement controls, offline."""
import unittest
import json
from scripts import check_event_reference as e


class EventReferenceTests(unittest.TestCase):
    def article(self, assembly='GRCh38.primary_assembly', coords='chr8:79611214:79616822', doi=e.DOI):
        return (f'<article><front><article-meta><article-id pub-id-type="doi">{doi}</article-id></article-meta></front>'
                f'<body><sec><p>{assembly}</p></sec><fig id="Fig5"><caption><p>STMN2 {coords}</p></caption></fig></body></article>').encode()

    def test_primary_source_projection_retains_coordinates_not_subjects(self):
        d = json.loads(e.project_article(self.article()))
        self.assertEqual((d['chrom'],d['left_exonic_boundary'],d['right_exonic_boundary']),('chr8',79611214,79616822))
        self.assertIsNone(d['strand_in_caption'])
        self.assertEqual(d['claim_scope'],'junction_identity_only_not_full_transcript_or_polyA')

    def test_wrong_assembly_and_doi_rejected(self):
        for args in [{'assembly':'hg19'}, {'doi':'wrong'}]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                e.project_article(self.article(**args))

    def test_missing_and_ambiguous_coordinates_rejected(self):
        for coords in ['no coordinates','chr8:79611214:79616822 chr8:79611214:79616823']:
            with self.subTest(coords=coords), self.assertRaises(ValueError):
                e.project_article(self.article(coords=coords))

    def test_exact_junction_and_negative_controls(self):
        d=json.loads(e.project_article(self.article()))
        self.assertTrue(e.junction_matches(d,'chr8','+',79611214,79616822,'+'))
        for chrom,strand,left,right in [('chr8','-',79611214,79616822),('chr8','+',79611215,79616822),
                                       ('chr8','+',79611214,79616821),('chr8','+',79611214,79636802),
                                       ('chr19','+',79611214,79616822)]:
            with self.subTest(coords=(chrom,strand,left,right)):
                self.assertFalse(e.junction_matches(d,chrom,strand,left,right,'+'))

    def test_full_length_and_unique_are_not_nested(self):
        self.assertEqual(e.quant_violations(unique=5,full=7,total=10),[])
        self.assertEqual(e.quant_violations(unique=7,full=5,total=10),[])
        self.assertEqual(e.quant_violations(unique=11,full=5,total=10),['unique_exceeds_total'])
        self.assertEqual(e.quant_violations(unique=5,full=11,total=10),['full_length_exceeds_total'])

    def test_rounding_tolerance_does_not_hide_material_violations(self):
        self.assertEqual(e.quant_violations(1,2.00001,2),[])
        self.assertEqual(e.quant_violations(1,2.001,2),['full_length_exceeds_total'])

    def test_scalar_source_formula_does_not_require_even_output(self):
        # This is an algebraic witness, explicitly not execution of R/Bambu.
        self.assertEqual(e.one_isoform_unique_witness([1]),1.)
        self.assertEqual(e.one_isoform_unique_witness([1,2]),3.)
        self.assertEqual(e.one_isoform_unique_witness([0]),0.)


if __name__=='__main__':
    unittest.main()
