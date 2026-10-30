import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('ambiguity', ROOT / 'scripts/audit_gene_ambiguity.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class AmbiguityTests(unittest.TestCase):
    def setUp(self):
        self.ids = {'ENSG0001': {'symbol': 'A', 'chrom': 'chr1', 'strand': '+', 'start': 1, 'end': 5},
                    'ENSG0002': {'symbol': 'A', 'chrom': 'chr2', 'strand': '+'},
                    'ENSG0003': {'symbol': 'B', 'chrom': 'chr1', 'strand': '+'},
                    'ENSG0004_PAR_Y': {'symbol': 'P', 'chrom': 'chrY', 'strand': '+'}}
        self.symbols = {'A': {'ENSG0001', 'ENSG0002'}, 'B': {'ENSG0003'}, 'P': {'ENSG0004_PAR_Y'}}

    def resolve(self, value, chrom='chr1', strand='+', candidate='ENSG0001'):
        return mod.author_resolution(value, chrom, strand, candidate, self.ids, self.symbols)

    def test_global_ambiguity_can_be_locus_conditional(self):
        r = self.resolve('A')
        self.assertEqual(r['state'], 'conditional_same_gene')
        self.assertEqual(r['excluded_locus_ids'], 'ENSG0002')

    def test_overlap_stays_ambiguous_without_span_heuristic(self):
        self.assertEqual(self.resolve('A,B')['state'], 'multiple_ids_at_chrom_strand')

    def test_unknown_token_blocks_known_match(self):
        self.assertEqual(self.resolve('A,UNKNOWN')['state'], 'unresolved_token')

    def test_explicit_id_and_version_are_not_aliases(self):
        self.assertEqual(self.resolve('ENSG0001.7')['state'], 'conditional_same_gene')
        self.assertEqual(self.resolve('ENSG9999')['state'], 'unresolved_token')

    def test_par_y_is_preserved(self):
        r = self.resolve('ENSG0004.3_PAR_Y', 'chrY', '+', 'ENSG0004_PAR_Y')
        self.assertEqual(r['state'], 'conditional_same_gene')
        self.assertEqual(mod.m.stable('ENSG0004.3_PAR_Y'), 'ENSG0004_PAR_Y')

    def test_wrong_strand_does_not_match(self):
        self.assertEqual(self.resolve('A', strand='-')['state'], 'no_id_at_chrom_strand')

    def test_other_unique_gene_not_promoted(self):
        self.assertEqual(self.resolve('B')['state'], 'conditional_other_gene')

    def test_candidate_id_does_not_require_unique_symbol(self):
        r = {'gene_id': 'ENSG0001', 'chrom': 'chr1', 'strand': '+'}
        self.assertEqual(mod.candidate_id(r, self.ids), 'candidate_id_locus_confirmed')
        r['chrom'] = 'chr2'
        self.assertEqual(mod.candidate_id(r, self.ids), 'reference_locus_discordant')

    def test_empty_token_is_not_silently_dropped(self):
        self.assertEqual(self.resolve('A,')['state'], 'unresolved_token')
