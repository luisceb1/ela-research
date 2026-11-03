import gzip
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
scripts=Path(__file__).resolve().parents[1]/'scripts';sys.path.insert(0,str(scripts))
try:import paired_fastq_integrity as fq
finally:sys.path.pop(0)


def fastq(mate,n=3,kind='slash'):
    records=[]
    for i in range(n):
        name=f'fixture{i}'+(f'/{mate}' if kind=='slash' else '')
        if kind=='casava':name+=f' {mate}:N:0:TEST'
        records.append(f'@{name}\nACGTN\n+\nIIIII\n'.encode())
    return b''.join(records)


class FastqTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.a=self.root/'R1.gz';self.b=self.root/'R2.gz';self.out=self.root/'out';self.put()
    def put(self,a=None,b=None):
        self.a.write_bytes(gzip.compress(fastq(1) if a is None else a,mtime=0));self.b.write_bytes(gzip.compress(fastq(2) if b is None else b,mtime=0))
    def run_pair(self,**kw):return fq.validate_pair(self.a,self.b,self.out,kw.pop('prefix_pairs',2),**kw)
    def rejected(self,exc=ValueError):
        with self.assertRaises(exc):self.run_pair()
        self.assertEqual(json.loads((self.out/'result.json').read_text())['status'],'failed')
        self.assertFalse((self.out/'prefix-R1.fastq.gz').exists())
    def test_success_full_scan_exact_prefix(self):
        r=self.run_pair();self.assertEqual(r['pairs_scanned'],3);self.assertEqual(r['prefix_pairs_written'],2);self.assertTrue(r['source_gzip_eof_crc_validated'])
        self.assertEqual(gzip.decompress((self.out/'prefix-R1.fastq.gz').read_bytes()),fastq(1,n=2))
    def test_deterministic_prefix_and_aggregate_result(self):
        a=self.run_pair();b=fq.validate_pair(self.a,self.b,self.root/'again',2);self.assertEqual(a,b)
        self.assertEqual((self.out/'prefix-R1.fastq.gz').read_bytes(),(self.root/'again/prefix-R1.fastq.gz').read_bytes())
    def test_supported_name_conventions(self):
        for kind in ('same','casava'):
            self.put(fastq(1,kind=kind),fastq(2,kind=kind));r=fq.validate_pair(self.a,self.b,self.root/kind,2);self.assertEqual(r['status'],'verified')
    def test_crc_after_prefix_rejected(self):
        data=bytearray(self.b.read_bytes());data[-8]^=1;self.b.write_bytes(data);self.rejected(gzip.BadGzipFile)
    def test_truncated_gzip_rejected(self):
        self.a.write_bytes(self.a.read_bytes()[:-4]);self.rejected(EOFError)
    def test_mate_extra_rejected_after_prefix(self):self.put(b=fastq(2,n=4));self.rejected()
    def test_mate_missing_rejected(self):self.put(b=fastq(2,n=2));self.rejected()
    def test_order_mismatch_rejected(self):self.put(b=fastq(2).replace(b'fixture1',b'different'));self.rejected()
    def test_wrong_mate_label_rejected(self):self.put(b=fastq(1));self.rejected()
    def test_conflicting_labels_rejected(self):self.put(a=fastq(1).replace(b'/1\n',b'/1 2:N:0:TEST\n'));self.rejected()
    def test_quality_length_rejected(self):self.put(a=fastq(1).replace(b'IIIII',b'IIII',1));self.rejected()
    def test_bad_base_rejected(self):self.put(a=fastq(1).replace(b'ACGTN',b'ACGTZ',1));self.rejected()
    def test_plus_identity_rejected(self):self.put(a=fastq(1).replace(b'+\n',b'+other\n',1));self.rejected()
    def test_repeated_plus_identity_supported(self):
        a=fastq(1).replace(b'+\n',b'+fixture0/1\n',1);self.put(a=a);self.assertEqual(self.run_pair()['status'],'verified')
    def test_prefix_too_large_fails(self):
        with self.assertRaises(ValueError):self.run_pair(prefix_pairs=4)
        self.assertEqual(json.loads((self.out/'result.json').read_text())['status'],'failed')
    def test_reject_existing_output(self):self.run_pair();self.assertRaises(FileExistsError,self.run_pair)
    def test_same_input_and_boolean_prefix_rejected(self):
        self.assertRaises(ValueError,fq.validate_pair,self.a,self.a,self.out,2)
        self.assertRaises(ValueError,fq.validate_pair,self.a,self.b,self.out,True)
    def test_guard_failure_no_prefix_certified(self):
        def stop():raise RuntimeError('synthetic global stop')
        with self.assertRaises(RuntimeError):self.run_pair(checkpoint=stop)
        self.assertEqual(json.loads((self.out/'result.json').read_text())['status'],'failed')
    def test_empty_source_not_certified(self):self.put(a=b'',b=b'');self.rejected()
    def test_multiline_rejected(self):self.put(a=fastq(1).replace(b'ACGTN\n',b'AC\nGTN\n',1));self.rejected()
    def test_concatenated_gzip_member_is_not_ignored(self):
        self.a.write_bytes(self.a.read_bytes()+gzip.compress(fastq(1,n=1),mtime=0));self.rejected()
