import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from scripts.inspect_hisat2_index import safe_name, check_space, extract
from scripts.compare_hisat2_reference import overlap_piece


class IndexGuardTests(unittest.TestCase):
    def test_window_crosses_stream_chunks(self):
        self.assertEqual(overlap_piece('ACGT',0,2,6)+overlap_piece('TAGC',4,2,6),'GTTA')
        self.assertEqual(overlap_piece('ACGT',0,10,12),'')
    def test_reject_unsafe_paths(self):
        for p in ['/absolute', '../escape', 'a/../../b', 'a\\b', '.']:
            with self.subTest(path=p), self.assertRaises(ValueError): safe_name(p)

    def test_valid_path(self):
        self.assertEqual(str(safe_name('hg38/genome.1.ht2')), 'hg38/genome.1.ht2')

    def test_disk_guards(self):
        check_space(100, 80, 99, 100)
        for args in [(79,80,99,100),(100,80,101,100)]:
            with self.assertRaises(ValueError): check_space(*args)

    def fixture(self, root, name='hg38/genome.1.ht2', content=b'index', link=False):
        p=root/'tiny.tar.gz'
        with tarfile.open(p,'w:gz') as t:
            m=tarfile.TarInfo(name)
            if link: m.type=tarfile.SYMTYPE; m.linkname='/outside'
            else: m.size=len(content)
            t.addfile(m, None if link else io.BytesIO(content))
        manifest={'size_bytes':p.stat().st_size,'resource_limits':{'reserve_disk_bytes':0,'additional_disk_bytes':100000}}
        record={'complete':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        return p,manifest,record

    def test_extract_crc_sizes_hashes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,m,r=self.fixture(root)
            out=extract(p,root/'out',m,r,root/'result.json')
            self.assertTrue(out['gzip_crc_validated'])
            self.assertEqual(out['extracted_bytes'],5)
            self.assertEqual((root/'out/hg38/genome.1.ht2').read_bytes(),b'index')
            self.assertFalse(out['index_accepted'])

    def test_tamper_archive_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,m,r=self.fixture(root);b=bytearray(p.read_bytes());b[0]^=1;p.write_bytes(b)
            with self.assertRaises(ValueError): extract(p,root/'out',m,r,root/'result.json')

    def test_incomplete_download_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,m,r=self.fixture(root);r['complete']=False
            with self.assertRaises(ValueError): extract(p,root/'out',m,r,root/'result.json')

    def test_tar_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,m,r=self.fixture(root,link=True)
            with self.assertRaises(ValueError): extract(p,root/'out',m,r,root/'result.json')

    def test_tar_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,m,r=self.fixture(root,name='../escape')
            with self.assertRaises(ValueError): extract(p,root/'out',m,r,root/'result.json')

    def test_extracted_size_budget_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,m,r=self.fixture(root);m['resource_limits']['additional_disk_bytes']=p.stat().st_size+4
            with self.assertRaises(ValueError): extract(p,root/'out',m,r,root/'result.json')

    def test_corrupt_gzip_crc_even_rehashed_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,m,r=self.fixture(root);b=bytearray(p.read_bytes());b[-8]^=1;p.write_bytes(b);r['sha256']=hashlib.sha256(b).hexdigest()
            with self.assertRaises((gzip.BadGzipFile,tarfile.ReadError)):
                extract(p,root/'out',m,r,root/'result.json')


if __name__=='__main__': unittest.main()
