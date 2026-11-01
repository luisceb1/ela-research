import csv
import importlib.util
import io
from pathlib import Path
import struct
import unittest
import zlib


def module(name):
    path = Path(__file__).resolve().parents[1] / 'scripts' / (name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


audit = module('audit_gse296714_design')
remotezip = module('fetch_gse296714_zip_metadata')


class MatrixControls(unittest.TestCase):
    def valid(self, value='0.5'):
        return 'gene_id,A,B\n' + ''.join(f'{key}.1,{value},2\n' for key in audit.TARGETS)

    def test_fractional_estimates_are_not_rejected_as_corrupt(self):
        result, targets = audit.audit_matrix(io.StringIO(self.valid()), ['A', 'B'])
        self.assertEqual(result['fractional_values'], 3)
        self.assertEqual(len(targets), 6)

    def test_duplicate_columns_rejected(self):
        with self.assertRaises(ValueError):
            audit.audit_matrix(io.StringIO(self.valid().replace('A,B', 'A,A')), ['A', 'B'])

    def test_unlinked_column_rejected(self):
        with self.assertRaises(ValueError):
            audit.audit_matrix(io.StringIO(self.valid()), ['A', 'C'])

    def test_invalid_values_rejected(self):
        for value in ['nan', 'inf', '-1']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                audit.audit_matrix(io.StringIO(self.valid(value)), ['A', 'B'])

    def test_duplicate_gene_version_rejected(self):
        text = self.valid() + f'{next(iter(audit.TARGETS))}.2,1,2\n'
        with self.assertRaises(ValueError):
            audit.audit_matrix(io.StringIO(text), ['A', 'B'])

    def test_missing_target_rejected(self):
        with self.assertRaises(ValueError):
            audit.audit_matrix(io.StringIO('gene_id,A,B\nENSG_other,1,2\n'), ['A', 'B'])


class IdentityControls(unittest.TestCase):
    def sample(self):
        return {'srx': 'SRX1', 'biosample': 'SAMN1', 'library': 'CTRL-1'}

    def run_row(self):
        return {'experiment_accession': 'SRX1', 'sample_accession': 'SAMN1',
                'sample_alias': 'CTRL-1', 'fastq_bytes': '10;20', 'fastq_md5': 'a;b',
                'library_layout': 'PAIRED', 'run_accession': 'SRR1', 'read_count': '15'}

    def test_unrelated_project_samples_are_not_selected(self):
        unrelated = {**self.run_row(), 'experiment_accession': 'SRX2', 'run_accession': 'SRR2'}
        self.assertEqual(len(audit.link_ena([self.sample()], [self.run_row(), unrelated])), 1)

    def test_conflicting_biosample_or_duplicate_run_mapping_rejected(self):
        for rows in [[{**self.run_row(), 'sample_accession': 'SAMN2'}], [self.run_row(), self.run_row()]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                audit.link_ena([self.sample()], rows)

    def test_papa_uses_explicit_author_mapping_and_rejects_collapsed_units(self):
        text = 'le_id\tgene_id\tCTRL_1\tTDP_1\nENSG00000104435.14_1\tENSG00000104435.14\t0.2\t10.3\n'
        result, rows = audit.audit_papa(io.StringIO(text), {'CTRL_1': 'CTRL-1', 'TDP_1': 'TDP-1'})
        self.assertEqual(result['rows'], 1)
        self.assertEqual(rows[0]['estimated_pas_group_count'], 0.2)
        with self.assertRaises(ValueError):
            audit.audit_papa(io.StringIO(text), {'CTRL_1': 'same', 'TDP_1': 'same'})


class ArchiveControls(unittest.TestCase):
    def block(self):
        data, name = b'example metadata', b'allowed.csv'
        compressor = zlib.compressobj(wbits=-15)
        compressed = compressor.compress(data) + compressor.flush()
        crc = zlib.crc32(data)
        block = struct.pack('<4s5H3L2H', b'PK\x03\x04', 20, 0, 8, 0, 0, crc, len(compressed), len(data), len(name), 0) + name + compressed
        entry = {'name': name.decode(), 'compressed': len(compressed), 'uncompressed': len(data), 'crc': crc, 'method': 8}
        return block, entry, data

    def test_member_name_and_crc_checked(self):
        block, entry, data = self.block()
        self.assertEqual(remotezip.extract_member(block, entry), data)
        for changed in [{**entry, 'name': 'wrong.csv'}, {**entry, 'crc': 0}]:
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                remotezip.extract_member(block, changed)

    def test_truncation_and_output_limit_rejected(self):
        block, entry, _ = self.block()
        with self.assertRaises(ValueError):
            remotezip.extract_member(block[:-1], entry)
        with self.assertRaises(ValueError):
            remotezip.extract_member(block, entry, max_uncompressed=1)


if __name__ == '__main__':
    unittest.main()
