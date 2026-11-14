"""Offline preparation controls only; fixture files are not biological evidence."""
import csv
import importlib.util
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('local_prepare', ROOT / 'scripts/prepare_gse252892_local.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class LocalPrepareTests(unittest.TestCase):
    def test_fixed_manifest(self):
        rows = m.selected_inputs(m.REPORT / 'fastq-manifest.tsv')
        self.assertEqual(len(rows), 4)
        self.assertEqual(sum(int(x['compressed_bytes']) for x in rows), 12826593031)
        self.assertEqual({x['run'] for x in rows}, {'SRR27477544', 'SRR27477541'})

    def test_duplicate_file_refused(self):
        rows = m.selected_inputs(m.REPORT / 'fastq-manifest.tsv')
        rows[1]['url'] = rows[0]['url']
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'manifest.tsv'
            with p.open('w') as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t')
                w.writeheader(); w.writerows(rows)
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                m.selected_inputs(p)

    def test_missing_index_refused(self):
        import json
        expected = json.loads((ROOT / 'reports/hisat2-index-inspection-20261031/verified_index.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'Index missing'):
                m.verify_index(tmp, expected)

    def test_changed_index_digest_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            expected = {'verified_files': []}
            for name in [*(f'genome.{i}.ht2' for i in range(1,9)), 'make_hg38.sh']:
                p = Path(tmp) / name; p.write_bytes(b'fixture')
                expected['verified_files'].append({'name': 'hg38/'+name, 'bytes': 7, 'sha256': '0'*64})
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                m.verify_index(tmp, expected)

    def test_existing_output_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'keep.json'; p.write_text('keep')
            with self.assertRaisesRegex(ValueError, 'already exists'):
                m.prepare(Path(tmp), Path(tmp), Path(tmp), p)
            self.assertEqual(p.read_text(), 'keep')

    def test_output_inside_checkout_refused(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            m.prepare(ROOT, ROOT, ROOT, ROOT / 'not-created-local-descriptor.json')

    def test_success_descriptor_stays_disabled_with_mocked_host(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'disabled.json'
            tool = Path(tmp) / 'tool'; tool.write_text('fixture')
            with patch.object(m, 'git', side_effect=['', 'fixture-commit']), patch.object(m, 'verify_index', return_value=[{'fixture': True}] * 9), patch.object(m.subprocess, 'run', return_value=SimpleNamespace(stdout='fixture version 2.2.3')), patch.dict('sys.modules', {'pysam': SimpleNamespace(__version__='0.23.3')}):
                result = m.prepare(tmp, tool, tool, output)
            descriptor = json.loads(output.read_text())
            self.assertFalse(descriptor['execution_enabled'])
            self.assertEqual(descriptor['status'], 'prepared_disabled')
            self.assertEqual(result['raw_bytes_downloaded'], 0)
            self.assertEqual(result['input_files'], 4)
            self.assertEqual(result['descriptor_sha256'], m.sha256(output))


if __name__ == '__main__':
    unittest.main()
