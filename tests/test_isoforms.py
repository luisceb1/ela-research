"""Structural controls independent of observed ELA results."""
import gzip
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts import geo_audit as a
from scripts import map_isoforms as m


class IsoformTests(unittest.TestCase):
    def test_chain_validation(self):
        self.assertEqual(m.validated_chain([(30, 40), (1, 10)]), ((1, 10), (30, 40)))
        for bad in ([], [(0, 3)], [(3, 2)], [(1, 3), (3, 5)], [(1, 3), (1, 3)]):
            with self.subTest(chain=bad), self.assertRaises(ValueError):
                m.validated_chain(bad)

    def test_junction_boundaries_not_intron_coordinates(self):
        self.assertEqual(m.junctions(((1, 10), (30, 40))), ((10, 30),))
        self.assertEqual(m.junctions(((1, 10),)), ())

    def test_annotated_exons_do_not_imply_annotated_chain(self):
        r = {'chrom': 'chr1', 'strand': '+', 'exons': ((1, 10), (30, 40))}
        reference = {'chains': set(), 'exons': {('chr1', '+', 1, 10), ('chr1', '+', 30, 40)}, 'junctions': set()}
        result = m.classify(r, reference)
        self.assertFalse(result['full_chain_in_gencode_v47'])
        self.assertEqual(result['n_unannotated_exons'], 0)
        self.assertEqual(result['n_unannotated_junctions'], 1)

    def test_terminal_difference_not_internal_exon(self):
        rec = {'chrom': 'chr1', 'strand': '-', 'exons': ((1, 10), (30, 40), (50, 70))}
        ref = {'chains': set(), 'exons': {('chr1', '-', 30, 40)}, 'junctions': set()}
        result = m.classify(rec, ref)
        self.assertEqual(result['n_unannotated_exons'], 2)
        self.assertEqual(result['n_unannotated_internal_exons'], 0)

    def test_strand_is_part_of_identity(self):
        rec = {'chrom': 'chr1', 'strand': '-', 'exons': ((1, 10),)}
        ref = {'chains': {('chr1', '+', ((1, 10),))}, 'exons': {('chr1', '+', 1, 10)}, 'junctions': set()}
        self.assertFalse(m.classify(rec, ref)['full_chain_in_gencode_v47'])
        self.assertEqual(m.classify(rec, ref)['n_unannotated_exons'], 1)

    def test_gencode_repeated_tag_is_valid(self):
        attr = a.attrs('gene_id "g"; transcript_id "t"; tag "basic"; tag "canonical"; ont "one"; ont "two";')
        self.assertEqual(attr['transcript_id'], 't')
        with self.assertRaises(ValueError):
            a.attrs('gene_id "g"; gene_id "different";')

    def test_external_symbol_disagreement_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'ref.gz'
            p.write_bytes(gzip.compress(b'chr1\tref\texon\t1\t10\t.\t+\t.\tgene_id "g.1"; transcript_id "t"; gene_name "WRONG";\n'))
            with patch.object(m, 'GENES', {'EXPECTED': 'g'}), self.assertRaisesRegex(ValueError, 'symbol/ID'):
                m.read_reference(p)

    def test_overlap_is_not_target_assignment(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'local.gz'
            p.write_bytes(gzip.compress(('chr1\tx\ttranscript\t1\t20\t.\t+\t.\tgene_id "g.1"; transcript_id "target";\n'
                'chr1\tx\ttranscript\t15\t40\t.\t+\t.\tgene_id "other"; transcript_id "overlap";\n'
                'chr1\tx\ttranscript\t15\t40\t.\t-\t.\tgene_id "antisense"; transcript_id "opposite";\n'
                'chr1\tx\ttranscript\t50\t60\t.\t+\t.\tgene_id "far"; transcript_id "outside";\n').encode()))
            ref = {'TARGET': {'exons': {('chr1', '+', 1, 20)}}}
            with patch.object(a, 'TARGETS', {'TARGET': 'g'}):
                result = m.locus_candidates(p, ref)
            self.assertEqual([r['txname'] for r in result], ['overlap', 'opposite'])
            self.assertEqual([r['same_strand_as_target'] for r in result], [True, False])
            self.assertTrue(all(r['assignment'] == 'not_reassigned_overlap_only' for r in result))


if __name__ == '__main__':
    unittest.main()
