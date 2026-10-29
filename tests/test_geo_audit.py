"""Offline failure controls; these tests do not validate biology."""
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts import geo_audit as a


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def gz(self, name, content):
        p = self.root / name
        p.write_bytes(gzip.compress(content.encode()))
        return p

    def table(self, rows):
        return self.gz('counts.gz', 'TXNAME\tGENEID\ta\tb\n' + rows)

    def test_bad_counts_fail_closed(self):
        for bad in ('-1', 'nan', 'inf', 'junk'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                list(a.count_rows(self.table(f't\tg\t{bad}\t0\n')))

    def test_ragged_and_duplicate_ids(self):
        with self.assertRaises(ValueError):
            list(a.count_rows(self.table('t\tg\t1\n')))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            a.qc_counts(self.table('t\tg\t1\t0\nt\tg\t1\t2\n'), {})

    def test_mapping_exact_versions_and_gene_conflicts(self):
        qc, _ = a.qc_counts(self.table('t.1\tg.1\t2\t0\nu\tg.2\t0\t3\n'),
                            {'t.2': ('g.1', 'chr1', '+'), 'u': ('g.1', 'chr1', '+')})
        self.assertEqual(qc['unmapped'], [('t.1', 'g.1', 'missing_gtf_transcript')])
        self.assertEqual(qc['gene_mismatches'], [('u', 'g.2', 'g.1')])
        self.assertEqual(qc['assigned_counts'], [2, 3])
        self.assertEqual(qc['detected_transcripts'], [1, 1])

    def test_gtf_conflicting_identity(self):
        p = self.gz('g.gz', 'chr1\tx\texon\t1\t2\t.\t+\t.\tgene_id "g"; transcript_id "t";\n'
                    'chr2\tx\texon\t3\t4\t.\t+\t.\tgene_id "g"; transcript_id "t";\n')
        with self.assertRaisesRegex(ValueError, 'Conflicting GTF'):
            a.gtf_index(p)

    def test_invalid_gtf_coords(self):
        p = self.gz('g.gz', 'chr1\tx\texon\t3\t2\t.\t+\t.\tgene_id "g"; transcript_id "t";\n')
        with self.assertRaises(ValueError):
            a.gtf_index(p)

    def test_gtf_attribute_inventory_counts_rows(self):
        p = self.gz('g.gz', 'chr1\tx\ttranscript\t1\t4\t.\t+\t.\tgene_id "g"; transcript_id "t";\n'
                    'chr1\tx\texon\t1\t2\t.\t+\t.\tgene_id "g"; transcript_id "t"; exon_number "1";\n')
        index, _, features, attributes = a.gtf_index(p)
        self.assertEqual(attributes, {'gene_id': 2, 'transcript_id': 2, 'exon_number': 1})
        self.assertEqual(features, {'transcript': 1, 'exon': 1})
        self.assertEqual(index['t'], ('g', 'chr1', '+'))

    def test_unique_counts_cannot_exceed_total(self):
        u = self.gz('u.gz', 'TXNAME\tGENEID\ta\nt\tg\t3\n')
        c = self.gz('c.gz', 'TXNAME\tGENEID\ta\nt\tg\t2.5\n')
        with self.assertRaisesRegex(ValueError, 'uniqueCounts > counts'):
            a.compare_counts(u, c)

    def test_count_order_mismatch_rejected(self):
        u = self.gz('u.gz', 'TXNAME\tGENEID\ta\nt\tg\t1\n')
        c = self.gz('c.gz', 'TXNAME\tGENEID\ta\nu\tg\t1\n')
        with self.assertRaisesRegex(ValueError, 'identities/order'):
            a.compare_counts(u, c)

    def test_bambutx_ids_are_dataset_scoped(self):
        p = self.table('BambuTx1\tgeneA\t1\t0\n')
        qc, _ = a.qc_counts(p, {'BambuTx1': ('geneB', 'chr1', '+')})
        self.assertEqual(len(qc['gene_mismatches']), 1)

    def test_metadata_allowlist(self):
        raw = b'!Sample_title = library\n!Sample_contact_email = private@example.invalid\n!Sample_characteristics_ch1 = age: 88\n!Sample_characteristics_ch1 = tissue: cortex\n'
        out = json.loads(a.technical_projection(raw))
        self.assertNotIn('!Sample_contact_email', out)
        self.assertEqual(out['!Sample_characteristics_ch1'], ['tissue: cortex'])

    def test_cache_hash_mismatch(self):
        p = self.root / 'cache'
        p.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'Unverified cache'):
            a.fetch('https://example.invalid', p, {'cache': {'cache_sha256': 'incorrect'}})

    def test_bad_gzip_rejected(self):
        p = self.root / 'bad.gz'
        p.write_bytes(b'not-gzip')
        with self.assertRaises(gzip.BadGzipFile):
            list(a.count_rows(p))

    def test_unknown_treatment_and_ambiguous_sample_fail(self):
        (self.root / 'GSE310723.soft').write_text('!Series_sample_id = GSMtest\n')
        p = self.root / 'GSMtest.technical.json'
        data = {'!Sample_title': ['culture replicate 1'], '!Sample_characteristics_ch1': ['treatment: unrecognized']}
        p.write_text(json.dumps(data))
        with patch.object(a, 'DATA', self.root), self.assertRaisesRegex(ValueError, 'Unrecognized treatment'):
            a.match_samples('GSE310723', ['i3N_Ctrl_noAza_a'])
        data['!Sample_characteristics_ch1'] = ['treatment: Control']
        p.write_text(json.dumps(data))
        with patch.object(a, 'DATA', self.root), self.assertRaisesRegex(ValueError, 'Ambiguous/unmatched'):
            a.match_samples('GSE310723', ['i3N_Ctrl_noAza_a', 'i3N_Ctrl_noAza_b'])


if __name__ == '__main__':
    unittest.main()
