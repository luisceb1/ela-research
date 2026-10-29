import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from scripts.map_isoseq_gtf import check_summary, index_gtf, map_counts

ROOT = Path(__file__).resolve().parents[1]


class TestIsoSeqMapping(unittest.TestCase):
    def fixture(self, directory, name='', count_gene='ENSG00000104435.5', gtf_gene='ENSG00000104435.7', value='3'):
        d = Path(directory)
        attr = f'gene_id "{gtf_gene}"; transcript_id "BambuTx1";'
        if name:
            attr += f' gene_name "{name}";'
        # Real tabs/newlines; the former undiscovered test used literal escapes.
        (d/'a.gtf').write_text(f'chr8\tsrc\ttranscript\t1\t100\t.\t+\t.\t{attr}\nchr8\tsrc\texon\t1\t50\t.\t+\t.\t{attr}\n')
        (d/'a.tsv').write_text(f'TXNAME\tGENEID\tsynthetic_column\nBambuTx1\t{count_gene}\t{value}\n')
        return d

    def mapping(self, d, targets=None):
        return map_counts(d/'a.tsv', index_gtf(d/'a.gtf'), d/'out.tsv', targets or {'STMN2'})

    def test_ensembl_id_without_gene_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self.fixture(tmp)
            x = self.mapping(d)
            check_summary(x, {'STMN2'})
            self.assertEqual(x['by_target'], {'STMN2': 1})
            self.assertEqual(x['gtf_missing_gene_names'], 1)
            with (d/'out.tsv').open() as f:
                row = next(csv.DictReader(f, delimiter='\t'))
            self.assertEqual(row['gene_name'], 'STMN2')
            self.assertEqual(row['n_exons'], '1')

    def test_known_symbol_and_versioned_ids_agree(self):
        with tempfile.TemporaryDirectory() as tmp:
            x = self.mapping(self.fixture(tmp, name='STMN2'))
            self.assertEqual(x['target_transcripts'], 1)
            self.assertEqual(x['gene_id_conflicts'], 0)

    def test_conflicting_gene_ids_not_exported(self):
        with tempfile.TemporaryDirectory() as tmp:
            x = self.mapping(self.fixture(tmp, gtf_gene='ENSG9'))
            self.assertEqual(x['gene_id_conflicts'], 1)
            self.assertEqual(x['target_transcripts'], 0)
            with self.assertRaisesRegex(ValueError, 'identity'):
                check_summary(x, {'STMN2'})

    def test_symbol_cannot_override_wrong_ensembl_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            x = self.mapping(self.fixture(tmp, name='STMN2', count_gene='ENSG9', gtf_gene='ENSG9'))
            self.assertEqual(x['target_transcripts'], 0)
            self.assertEqual(x['symbol_id_conflicts'], 1)

    def test_wrong_symbol_for_correct_id_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            x = self.mapping(self.fixture(tmp, name='UNC13A'))
            with self.assertRaisesRegex(ValueError, 'identity'):
                check_summary(x, {'STMN2'})

    def test_each_requested_positive_control_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            x = self.mapping(self.fixture(tmp), {'STMN2', 'UNC13A'})
            with self.assertRaisesRegex(ValueError, 'UNC13A'):
                check_summary(x, {'STMN2', 'UNC13A'})

    def test_unknown_target_not_silent_empty_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'Unknown'):
                self.mapping(self.fixture(tmp), {'STMN22'})

    def test_nonfinite_negative_and_empty_counts_rejected(self):
        for value in ('nan', 'inf', '-1', ''):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ValueError):
                    self.mapping(self.fixture(tmp, value=value))

    def test_duplicate_count_ids_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self.fixture(tmp)
            with (d/'a.tsv').open('a') as f:
                f.write('BambuTx1\tENSG00000104435.5\t3\n')
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                self.mapping(d)

    def test_conflicting_gtf_identity_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self.fixture(tmp)
            with (d/'a.gtf').open('a') as f:
                f.write('chr19\tsrc\texon\t1\t40\t.\t-\t.\tgene_id "ENSG9"; transcript_id "BambuTx1";\n')
            with self.assertRaisesRegex(ValueError, 'identity'):
                index_gtf(d/'a.gtf')

    def test_cli_zero_targets_fails_without_new_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self.fixture(tmp, count_gene='ENSG9', gtf_gene='ENSG9')
            run = subprocess.run([sys.executable, str(ROOT/'scripts/map_isoseq_gtf.py'), '--counts', str(d/'a.tsv'), '--gtf', str(d/'a.gtf'), '--out', str(d/'result.tsv')], capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn('Positive target controls missing', run.stderr)
            self.assertFalse((d/'result.tsv').exists())
            self.assertEqual(list(d.glob('result.tsv.*')), [])

    def test_cli_valid_target_commits_complete_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self.fixture(tmp)
            run = subprocess.run([sys.executable, str(ROOT/'scripts/map_isoseq_gtf.py'), '--counts', str(d/'a.tsv'), '--gtf', str(d/'a.gtf'), '--out', str(d/'result.tsv'), '--targets', 'STMN2'], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn('BambuTx1', (d/'result.tsv').read_text())
            self.assertEqual(list(d.glob('result.tsv.*')), [])


if __name__ == '__main__':
    unittest.main()
