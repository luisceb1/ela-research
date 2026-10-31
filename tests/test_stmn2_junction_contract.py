import copy
import json
import unittest
from pathlib import Path
from scripts.audit_stmn2_junction_contract import boundaries, parse_cigar, sam_junctions, build_contract


def sam(cigar='8M5607N8M', pos=79611207, flag=0, chrom='chr8', mapq=60, tags='NH:i:1\tXS:A:+', seq='*'):
    return f'q\t{flag}\t{chrom}\t{pos}\t{mapq}\t{cigar}\t*\t0\t0\t{seq}\t*\t{tags}'


class JunctionContractTests(unittest.TestCase):
    def test_coordinates(self):
        b = boundaries(79611214, 79616822)
        self.assertEqual((b['intron_start_1based'], b['intron_end_1based']), (79611215, 79616821))
        self.assertEqual((b['intron_bed_start_0based'], b['intron_bed_end_exclusive']), (79611214, 79616821))
        self.assertEqual(b['skipped_reference_bases'], 5607)

    def test_invalid_boundaries(self):
        for a, b in [(0, 2), (2, 3), (4, 2), (True, 4), (1.0, 4)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError): boundaries(a, b)

    def test_exact_cryptic(self):
        self.assertEqual(sam_junctions(sam()), [('chr8', 79611214, 79616822, '+')])

    def test_canonical(self):
        self.assertEqual(sam_junctions(sam('8M25587N8M')), [('chr8', 79611214, 79636802, '+')])

    def test_offset_controls(self):
        target = ('chr8', 79611214, 79616822, '+')
        for pos in [79611206, 79611208]: self.assertNotIn(target, sam_junctions(sam(pos=pos)))
        for n in [5606, 5608]: self.assertNotIn(target, sam_junctions(sam(f'8M{n}N8M')))

    def test_reverse_flag_not_strand(self):
        self.assertEqual(sam_junctions(sam(flag=16)), sam_junctions(sam()))
        self.assertEqual(sam_junctions(sam(tags='NH:i:1\tXS:A:-'))[0][-1], '-')

    def test_wrong_chromosome_is_not_target(self):
        self.assertNotEqual(sam_junctions(sam(chrom='chr19'))[0], sam_junctions(sam())[0])

    def test_missing_strand_or_nh(self):
        for tags in ['NH:i:1', 'XS:A:+', 'NM:i:0']: self.assertEqual(sam_junctions(sam(tags=tags)), [])

    def test_multimapping_mapq(self):
        self.assertEqual(sam_junctions(sam(tags='NH:i:2\tXS:A:+')), [])
        for q in [0, 19, 255]: self.assertEqual(sam_junctions(sam(mapq=q)), [])
        self.assertEqual(len(sam_junctions(sam(mapq=20))), 1)

    def test_flags(self):
        for f in [4, 256, 512, 2048]: self.assertEqual(sam_junctions(sam(flag=f)), [])
        self.assertEqual(len(sam_junctions(sam(flag=1024))), 1)  # duplicate flag retained
        with self.assertRaises(ValueError): sam_junctions(sam(flag=1))

    def test_short_anchors(self):
        for cigar in ['7M5607N8M', '8M5607N7M', '8M5607N1I8M', '8M1D5607N8M']:
            self.assertEqual(sam_junctions(sam(cigar)), [])

    def test_equal_mismatch_anchor(self):
        self.assertEqual(sam_junctions(sam('4=4X5607N8=')), sam_junctions(sam()))

    def test_soft_hard_clipping(self):
        self.assertEqual(sam_junctions(sam('2H3S8M5607N8M3S2H')), sam_junctions(sam()))

    def test_indels_advance_reference_correctly(self):
        self.assertEqual(sam_junctions(sam('3M2D8M5607N8M', pos=79611202)), sam_junctions(sam()))
        self.assertEqual(sam_junctions(sam('3M2I8M5607N8M', pos=79611204)), sam_junctions(sam()))

    def test_two_junctions(self):
        self.assertEqual(sam_junctions(sam('8M20N8M30N8M', pos=10)), [('chr8', 17, 38, '+'), ('chr8', 45, 76, '+')])

    def test_deletion_is_not_splice(self):
        self.assertEqual(sam_junctions(sam('8M5607D8M')), [])

    def test_bad_cigars(self):
        for c in ['*', '0M', '8M0N8M', '8M2S8M', '8M1P8M', '8Mgarbage', '2S2H8M', '8M2H2S']:
            with self.subTest(c=c), self.assertRaises(ValueError): parse_cigar(c)

    def test_numeric_fields(self):
        for kwargs in [dict(pos=0), dict(mapq=-1), dict(mapq=256), dict(flag=-1)]:
            with self.assertRaises(ValueError): sam_junctions(sam(**kwargs))

    def test_bad_tags(self):
        for t in ['NH:i:0\tXS:A:+', 'NH:i:nan\tXS:A:+', 'NH:i:1\tNH:i:1', 'NH:i:1\tXS:A:?']:
            with self.assertRaises(ValueError): sam_junctions(sam(tags=t))

    def test_sequence_length(self):
        with self.assertRaises(ValueError): sam_junctions(sam(seq='A'*15))
        self.assertEqual(len(sam_junctions(sam(seq='A'*16))), 1)

    def test_header(self):
        self.assertEqual(sam_junctions('@SQ\tSN:chr8\tLN:145138636'), [])

    def test_manifest_contract_and_tamper(self):
        root = Path(__file__).resolve().parents[1]
        m = json.loads((root / 'research/references/stmn2_junction_contract_20261031.json').read_text())
        c = build_contract(m)
        self.assertFalse(c['pilot_ready'])
        self.assertEqual(c['raw_reads_processed'], 0)
        self.assertEqual(c['events']['canonical']['right_exon_start_1based'], 79636802)
        bad = copy.deepcopy(m)
        bad['inputs']['reports/isoforms/junctions.tsv'] = '0'*64
        with self.assertRaises(ValueError): build_contract(bad)


if __name__ == '__main__': unittest.main()
