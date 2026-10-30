import unittest

from scripts import match_author_junctions as m


def gene_data():
    ids = {'ENSG1': {'symbol': 'GENE1', 'chrom': 'chr1', 'strand': '+'},
           'ENSG2': {'symbol': 'GENE2', 'chrom': 'chr1', 'strand': '+'},
           'ENSG3': {'symbol': 'SHARED', 'chrom': 'chr2', 'strand': '-'}}
    return ids, {'GENE1': {'ENSG1'}, 'GENE2': {'ENSG2'}, 'SHARED': {'ENSG3', 'ENSG4'}}


def bed():
    return {'A': 'chr1', 'B': '100', 'C': '170', 'D': 'molecular-id', 'F': '+',
            'J': '2', 'K': '20,10', 'L': '0,60', 'M': 'GENE1', 'N': 'chr1:120-161(+)'}


class AuthorJunctionMatchTests(unittest.TestCase):
    def test_conversion_dedup_and_no_unvalidated_label(self):
        row = bed();row['N'] += ';chr1:120-161(+);chr1:121-160(+);chr1:120-161(-)'
        keys, excluded = m.eligible_keys(row, 'S8')
        self.assertEqual(keys, {('chr1', 121, 160, '+')})
        self.assertEqual(excluded, 2)
        self.assertNotIn(('chr1', 120, 161, '+'), keys)

    def test_invalid_blocks_never_rescued_by_matching_label(self):
        row = bed();row['K'] = '2010'
        with self.assertRaisesRegex(ValueError, 'block_count'):
            m.eligible_keys(row, 'S8')

    def test_s7_context_is_distinct_from_s8_cryptic_label(self):
        keys, excluded = m.eligible_keys(bed(), 'S7')
        self.assertEqual(keys, {('chr1', 121, 160, '+')})
        evidence = [{'category': 'S7', 'gene_resolution': 'exact_same_gene'}]
        self.assertEqual(m.classify('reference_identity_resolved', evidence), 'TE_transcript_context_only')
        evidence += [{'category': 'S8', 'gene_resolution': 'exact_same_gene'}]
        self.assertEqual(m.classify('reference_identity_resolved', evidence), 'exact_nonTE_label_match')

    def test_symbol_resolution_missing_multigene_unknown_and_ambiguous(self):
        _, symbols = gene_data()
        expected = [('None', 'missing_author_gene'), ('GENE1,GENE2', 'multiple_author_symbols'),
                    ('SHARED', 'ambiguous_reference_symbol'), ('old-alias', 'symbol_not_in_reference')]
        for value, status in expected:
            self.assertEqual(m.resolve(value, symbols), (status, None))
        self.assertEqual(m.resolve(' GENE1,GENE1 ', symbols), ('unique_reference_gene', 'ENSG1'))

    def test_wrong_gene_and_locus_are_not_strict_matches(self):
        ids, symbols = gene_data()
        row = bed()
        self.assertEqual(m.evidence_identity(row, ('ENSG2',), ids, symbols), 'different_unique_gene')
        row['F'] = '-'
        self.assertEqual(m.evidence_identity(row, ('ENSG1',), ids, symbols), 'author_gene_locus_discordant')

    def test_candidate_reference_identity_not_inferred_from_geometry(self):
        ids, symbols = gene_data()
        candidate = {'gene_id': 'ENSG1', 'chrom': 'chr1', 'intron_start': '121',
                     'intron_end': '160', 'strand': '+', 'reference_symbol': 'GENE1'}
        self.assertEqual(m.candidate_identity(candidate, ids, symbols), 'reference_identity_resolved')
        candidate['reference_symbol'] = 'GENE2'
        self.assertEqual(m.candidate_identity(candidate, ids, symbols), 'reference_symbol_not_unique_for_id')
        candidate['gene_id'] = 'ENSG9'
        self.assertEqual(m.candidate_identity(candidate, ids, symbols), 'reference_gene_missing')

    def test_unresolved_not_found_and_wrong_gene_stay_separate(self):
        self.assertEqual(m.classify('reference_identity_resolved', []), 'not_found_in_eligible_culture_subset')
        ev = [{'category': 'S8', 'gene_resolution': 'different_unique_gene'}]
        self.assertEqual(m.classify('reference_identity_resolved', ev), 'coordinate_match_different_gene')
        ev[0]['gene_resolution'] = 'multiple_author_symbols'
        self.assertEqual(m.classify('reference_identity_resolved', ev), 'coordinate_match_gene_unresolved')
        ev[0]['gene_resolution'] = 'exact_same_gene'
        self.assertEqual(m.classify('reference_gene_missing', ev), 'reference_identity_unresolved')

    def test_minus_strand_not_reversed_and_par_identity_preserved(self):
        row = bed();row.update({'F': '-', 'N': 'chr1:120-161(-)'})
        self.assertEqual(m.eligible_keys(row, 'S8')[0], {('chr1', 121, 160, '-')})
        self.assertEqual(m.stable('ENSG1.12_PAR_Y'), 'ENSG1_PAR_Y')
        self.assertEqual(m.stable('ENSG1.12'), 'ENSG1')

    def test_real_coordinate_control_and_partial_anchor_are_not_conflated(self):
        raw = {'A': 'chr8', 'F': '+', 'M': 'STMN2', 'B': '79611096',
               'J': '2', 'L': '0,5725', 'K': '1182973'}
        bad = {'sheet': 'S7B', 'sheet_row': 10, 'fields_by_column': raw, 'block_valid': False}
        good = {'sheet': 'S8D', 'sheet_row': 11, 'fields_by_column': raw, 'block_valid': True,
                'intronic_keys': [list(m.CANONICAL_STMN2)]}
        result = m.control_eligibility([bad, good])
        self.assertTrue(result['canonical_geometry_control']['recovered'])
        self.assertEqual(result['cryptic_control_source_eligibility'], 'not_evaluable_due_to_invalid_blocks')
        self.assertTrue(result['invalid_block_partial_anchor_rows'][0]['not_a_full_junction_match'])
        good['intronic_keys'] = [m.CANONICAL_STMN2]
        self.assertTrue(m.control_eligibility([good])['canonical_geometry_control']['recovered'])

    def test_control_wrong_strand_never_passes(self):
        wrong = {'sheet': 'S8D', 'sheet_row': 11, 'fields_by_column': {'A': 'chr8', 'F': '-', 'M': 'STMN2'},
                 'block_valid': True, 'intronic_keys': [list(m.CANONICAL_STMN2)]}
        self.assertFalse(m.control_eligibility([wrong])['canonical_geometry_control']['recovered'])


if __name__ == '__main__':
    unittest.main()
