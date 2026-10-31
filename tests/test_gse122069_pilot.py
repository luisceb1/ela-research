import gzip
import hashlib
from pathlib import Path
import tempfile
import unittest
from scripts.gse122069_pilot import fastq_qc,verify_file,empty_counts
from scripts.fetch_gse122069_ranges import validate_range


class PilotInputTests(unittest.TestCase):
    def test_range_identity_guards(self):
        headers={'Content-Range':'bytes 0-3/10','ETag':'fixed','Content-Length':'4'}
        validate_range(206,headers,0,3,10,'fixed')
        for status,h in [(200,headers),(206,dict(headers,ETag='changed')),(206,dict(headers,**{'Content-Range':'bytes 4-7/10'}))]:
            with self.assertRaises(ValueError):validate_range(status,h,0,3,10,'fixed')
    def make(self,root,body):
        path=Path(root)/'sample.fastq.gz'
        with gzip.open(path,'wb') as f:f.write(body)
        return path
    def test_valid_first_records_qc(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.make(d,b'@one\nACGN\n+\nIIII\n@two\nACGT\n+\n!!!!\n@ignored\nINVALID\n')
            r=fastq_qc(p,limit=2);self.assertEqual(r['reads'],2);self.assertEqual(r['N_bases'],1)
            self.assertEqual(r['length_histogram'],{4:2});self.assertEqual(r['mean_quality_if_phred33'],20)
    def test_truncated_record_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):fastq_qc(self.make(d,b'@one\nACGT\n+\n'),limit=1)
    def test_quality_length_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):fastq_qc(self.make(d,b'@one\nACGT\n+\nIII\n'),limit=1)
    def test_invalid_base_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):fastq_qc(self.make(d,b'@one\nACGZ\n+\nIIII\n'),limit=1)
    def test_too_few_records_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):fastq_qc(self.make(d,b'@one\nACGT\n+\nIIII\n'),limit=2)
    def test_input_digest_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data';p.write_bytes(b'known')
            md5=hashlib.md5(b'known').hexdigest();sha=hashlib.sha256(b'known').hexdigest()
            self.assertEqual(verify_file(p,5,md5,sha),sha)
            p.write_bytes(b'other')
            with self.assertRaises(ValueError):verify_file(p,5,md5,sha)
    def test_policy_counters_are_independent(self):
        counts=empty_counts();counts['15']['canonical']+=1
        self.assertEqual(counts['8']['canonical'],0)


if __name__=='__main__':unittest.main()
