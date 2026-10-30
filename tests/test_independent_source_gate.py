import tempfile
from pathlib import Path
import unittest
from scripts.audit_independent_source_gate import (checked_sources, collapse_sdrf, digest,
                                                   link_processed_keys, ready, sdrf_conflicts, soft_samples)


def row(assay='NT_inhibitor_cytosol_1_S22', run='ERR15663627',
        file='NT_NMD_nucleus_1.quant.sf', compartment='cytosol'):
    return {'Assay Name': assay, 'Comment[ENA_RUN]': run,
            'Comment[ENA_EXPERIMENT]': 'ERX15068093', 'Comment[ENA_SAMPLE]': 'ERS26958238',
            'Derived Array Data File': file, 'Characteristics[cell line]': 'SH-SY5Y',
            'Factor Value[organism part]': compartment,
            'Factor Value[stimulus]': 'control cells NMDi SMG1i inhibition'}


class IndependentSourceGateTests(unittest.TestCase):
    def test_paired_fastq_rows_do_not_double_replication(self):
        r = row(); r2 = r | {'Comment[FASTQ_URI]': 'mate2.fastq.gz'}
        self.assertEqual(len(collapse_sdrf([r, r2])), 1)

    def test_conflicting_technical_rows_not_silently_collapsed(self):
        with self.assertRaises(ValueError):
            collapse_sdrf([row(), row(compartment='nucleus')])

    def test_one_run_cannot_be_counted_as_two_assays(self):
        with self.assertRaises(ValueError):
            collapse_sdrf([row(), row(assay='another_assay')])

    def test_real_compartment_conflict_preserved_and_collision_reported(self):
        records = collapse_sdrf([row(), row(assay='NT_inhibitor_nucleus_1_S26',
                                            run='ERR15663630', compartment='nucleus')])
        conflicts, collisions = sdrf_conflicts(records)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]['source_compartment'], 'cytosol')
        self.assertEqual(collisions['NT_NMD_nucleus_1.quant.sf'], ['ERR15663627', 'ERR15663630'])

    def test_library_count_does_not_certify_independence(self):
        c = {'criteria': {k: True for k in ['public_attributable', 'direct_junction_counts',
             'event_identity_linked', 'independent_units_documented',
             'perturbation_control_documented', 'new_experimental_source']},
             'minimum_independent_units_per_condition': 3, 'libraries': 22}
        self.assertTrue(ready(c)[0])
        c['criteria']['independent_units_documented'] = None
        self.assertFalse(ready(c)[0])
        c['criteria']['independent_units_documented'] = True
        c['minimum_independent_units_per_condition'] = 2
        self.assertFalse(ready(c)[0])

    def test_coverage_or_tpm_is_not_direct_counts(self):
        c = {'criteria': {'public_attributable': True, 'direct_junction_counts': False},
             'minimum_independent_units_per_condition': 3}
        self.assertIn('direct_junction_counts', ready(c)[1])

    def test_public_gsm_projection_excludes_other_metadata_and_duplicate_ids_fail(self):
        s = '^SAMPLE = GSM1\n!Sample_title = siControl 1\n!Sample_contact_email = excluded\n!Sample_characteristics_ch1 = genotype: excluded\n'
        r = soft_samples(s)
        self.assertEqual(r[0]['fields'], {'!Sample_title': ['siControl 1']})
        with self.assertRaises(ValueError):
            soft_samples(s + s)

    def test_absent_and_ambiguous_filename_link_not_filled_or_repaired(self):
        records = collapse_sdrf([row(), row(assay='NT_inhibitor_nucleus_1_S26',
                                            run='ERR15663630', compartment='nucleus')])
        links = link_processed_keys(['nt_nmd_cytosol_1', 'nt_nmd_nucleus_1'], records)
        self.assertEqual([x['status'] for x in links], ['unmatched', 'ambiguous'])
        self.assertEqual(links[0]['runs'], [])

    def test_corrupted_source_is_rejected_before_projection(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'source'; p.write_bytes(b'original')
            m = {'sources': [{'cache_file': 'source', 'sha256': digest(p), 'id': 'test'}]}
            checked_sources(Path(d), m)
            p.write_bytes(b'changed')
            with self.assertRaises(ValueError):
                checked_sources(Path(d), m)


if __name__ == '__main__':
    unittest.main()
