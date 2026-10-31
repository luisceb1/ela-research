import copy
import gzip
import io
from pathlib import Path
import tempfile
import unittest
from scripts.gse122069_full_control import Bins, feed_fastq, concordance, count_text


class FullControlTests(unittest.TestCase):
    def test_boundary_secondary_records_and_final_partial(self):
        saved=[]; b=Bins(2,3,saved.append)
        for name,primary in [('a',False),('a',True),('b',True),('c',True),('c',False)]:
            b.start(name,primary)
        r=b.finish()
        self.assertEqual([x['reads'] for x in r['completed_bins']],[2,1])
        self.assertEqual([x['sam_records'] for x in r['completed_bins']],[3,2])
        self.assertEqual([x['primary_records'] for x in r['completed_bins']],[2,1])
        self.assertNotIn('name',str(r));self.assertEqual(saved[0]['reads'],2)
    def test_missing_primary_rejected_at_boundary(self):
        b=Bins(2,2);b.start('a',False)
        with self.assertRaises(ValueError):b.start('b',True)
    def test_duplicate_primary_rejected(self):
        b=Bins(2,2);b.start('a',True)
        with self.assertRaises(ValueError):b.start('a',True)
    def test_short_sam_rejected(self):
        b=Bins(2,2);b.start('a',True)
        with self.assertRaises(ValueError):b.finish()
    def test_extra_sam_rejected(self):
        b=Bins(1,1);b.start('a',True)
        with self.assertRaises(ValueError):b.start('b',True)
    def test_invalid_budget_rejected(self):
        with self.assertRaises(ValueError):Bins(0,2)
    def fq(self,d,body):
        p=Path(d)/'test.gz';p.write_bytes(gzip.compress(body));return p
    def test_full_fastq_qc_and_crc(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.fq(d,b'@a\nACGN\n+\nIIII\n');out=io.StringIO()
            r=feed_fastq(p,out,1,True)
            self.assertTrue(r['gzip_eof_crc_validated']);self.assertEqual(r['N_bases'],1)
            self.assertEqual(r['mean_quality_if_phred33'],40)
    def test_extra_fastq_rejected_and_subset_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.fq(d,b'@a\nACGT\n+\nIIII\n@b\nACGT\n+\nIIII\n')
            with self.assertRaises(ValueError):feed_fastq(p,io.StringIO(),1,True)
            self.assertFalse(feed_fastq(p,io.StringIO(),1,False)['gzip_eof_crc_validated'])
    def test_truncated_gzip_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.fq(d,b'@a\nACGT\n+\nIIII\n');p.write_bytes(p.read_bytes()[:-5])
            with self.assertRaises(EOFError):feed_fastq(p,io.StringIO(),1,True)
    def test_invalid_fastq_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            for body in (b'@a\nACGT\n+\nIII\n',b'@a\nACGZ\n+\nIIII\n',b'@a\nACGT\n+\n'):
                with self.assertRaises(ValueError):feed_fastq(self.fq(d,body),io.StringIO(),1,True)
    def test_concordance_rejects_bin_mismatch_even_equal_totals(self):
        b=Bins(1,2);b.start('a',True);b.start('b',True);r=b.finish();s=copy.deepcopy(r)
        concordance(r,s);s['completed_bins'][0]['sam_records']+=1
        with self.assertRaises(ValueError):concordance(r,s)
    def test_completed_prefix_excludes_unfinished_group(self):
        b=Bins(1,3);b.start('a',True);b.start('b',True)
        self.assertEqual(b.snapshot(False)['reads'],1)
        self.assertFalse(b.snapshot(False)['complete_library'])


if __name__=='__main__':unittest.main()
