import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('conflicts', ROOT / 'scripts/audit_gene_conflicts.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def exon(gid, tx, start, end, strand='+'):
    return f'chr1\ttest\texon\t{start}\t{end}\t.\t{strand}\t.\tgene_id "{gid}"; transcript_id "{tx}";\n'


class ConflictTests(unittest.TestCase):
    def test_interleaved_exons_remain_in_one_transcript(self):
        lines = [exon('G', 'A', 1, 10), exon('G', 'B', 5, 15), exon('G', 'A', 31, 40), exon('G', 'B', 41, 50)]
        index, n = mod.models(lines, {'G'})
        self.assertEqual(n, 2)
        self.assertEqual(index[('G', 'chr1', '11', '30', '+')], {'A'})
        self.assertEqual(index[('G', 'chr1', '16', '40', '+')], {'B'})

    def test_same_geometry_different_genes_stays_separate(self):
        lines = [exon(g, 'same_name', s, e) for g in ['G', 'H'] for s, e in [(1, 10), (31, 40)]]
        index, n = mod.models(lines, {'G', 'H'})
        self.assertEqual(n, 2)
        self.assertEqual(len(index), 2)

    def test_strand_part_of_model_identity(self):
        lines = [exon('G', 'T', s, e, strand) for strand in ['+', '-'] for s, e in [(1, 10), (31, 40)]]
        index, n = mod.models(lines, {'G'})
        self.assertEqual(n, 2)
        self.assertIn(('G', 'chr1', '11', '30', '-'), index)

    def test_overlap_not_silently_repaired(self):
        with self.assertRaises(ValueError):
            mod.junctions([(1, 10), (8, 20)])

    def test_duplicate_exon_and_adjacent_exon(self):
        self.assertEqual(mod.junctions([(1, 10), (1, 10), (11, 20)]), set())

    def test_reference_support_not_gene_resolution(self):
        self.assertEqual(mod.canonical_category(False, True), 'author_reference_only')
        self.assertEqual(mod.canonical_category(True, True), 'both_reference_genes')
        self.assertEqual(mod.canonical_category(False, False), 'neither_reference_gene')

    def test_non_target_gene_exons_excluded(self):
        index, n = mod.models([exon('H', 'T', 1, 10), exon('H', 'T', 31, 40)], {'G'})
        self.assertEqual(n, 0)
        self.assertFalse(index)
