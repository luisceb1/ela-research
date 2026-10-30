import importlib.util
import io
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('global_geometry', ROOT / 'scripts/audit_global_geometry.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def exon(g, t, s, e, strand='+', chrom='chr1'):
    return f'{chrom}\ttest\texon\t{s}\t{e}\t.\t{strand}\t.\tgene_id "{g}"; transcript_id "{t}";\n'


class GlobalGeometryTests(unittest.TestCase):
    def lookup(self, lines, wanted=None):
        return mod.global_lookup(lambda: io.StringIO(''.join(lines)), wanted or {('chr1', 11, 30, '+')})

    def test_exact_union_any_gene(self):
        _, hits, _ = self.lookup([exon('G', 'T', 1, 10), exon('G', 'T', 31, 40)])
        self.assertEqual(hits['chr1', 11, 30, '+'], {('G', 'T')})
        self.assertEqual(mod.classify('H', hits['chr1', 11, 30, '+']), 'other_gene_only_exact')

    def test_intermediate_exon_prevents_false_bridge(self):
        _, hits, qc = self.lookup([exon('G', 'T', 1, 10), exon('G', 'T', 16, 20), exon('G', 'T', 31, 40)])
        self.assertFalse(hits)
        self.assertEqual(qc['all_exons_in_selected_groups'], 3)

    def test_interleaved_transcripts_not_joined(self):
        _, hits, _ = self.lookup([exon('G', 'A', 1, 10), exon('G', 'B', 1, 12),
                                exon('G', 'A', 31, 40), exon('G', 'B', 41, 50)])
        self.assertEqual(hits['chr1', 11, 30, '+'], {('G', 'A')})

    def test_hebra_and_chromosome_required(self):
        for strand, chrom in [('-', 'chr1'), ('+', 'chr2')]:
            _, hits, _ = self.lookup([exon('G', 'T', 1, 10, strand, chrom), exon('G', 'T', 31, 40, strand, chrom)])
            self.assertFalse(hits)

    def test_same_name_in_two_genes_preserves_both(self):
        lines = [exon(g, 'T', s, e) for g in ['G', 'H'] for s, e in [(1, 10), (31, 40)]]
        _, hits, _ = self.lookup(lines)
        self.assertEqual(hits['chr1', 11, 30, '+'], {('G', 'T'), ('H', 'T')})
        self.assertEqual(mod.classify('G', hits['chr1', 11, 30, '+']), 'same_gene_exact')

    def test_one_end_is_not_enough(self):
        _, hits, _ = self.lookup([exon('G', 'T', 1, 10), exon('G', 'T', 32, 40)])
        self.assertFalse(hits)

    def test_version_removal_preserves_par_y(self):
        _, hits, _ = self.lookup([exon('ENSG1.2_PAR_Y', 'T', 1, 10), exon('ENSG1.2_PAR_Y', 'T', 31, 40)])
        self.assertIn(('ENSG1_PAR_Y', 'T'), hits['chr1', 11, 30, '+'])

    def test_invalid_intron_rejected(self):
        with self.assertRaises(ValueError):
            self.lookup([], {('chr1', 0, 30, '+')})

    def test_no_match_not_novelty_class(self):
        self.assertEqual(mod.classify('G', set()), 'not_found_in_v47_any_gene')

    def test_joint_absence_keeps_coverage_and_identity_limits(self):
        absent = 'not_found_in_v47_any_gene'
        self.assertEqual(mod.coverage_group(absent, 'not_found_in_eligible_culture_subset'), 'not_found_in_two_inspected_resources')
        self.assertEqual(mod.coverage_group(absent, 'coordinate_match_gene_unresolved'), 'author_or_reference_identity_unresolved')
        self.assertEqual(mod.coverage_group(absent, 'TE_transcript_context_only'), 'author_catalog_representation_only')
        self.assertEqual(mod.coverage_group('other_gene_only_exact', 'not_found_in_eligible_culture_subset'), 'reference_geometry_annotated')
