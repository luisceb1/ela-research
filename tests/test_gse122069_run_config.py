import copy
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch
from scripts.gse122069_run_config import load_rows,configure,partition,validate_receipt,aligner_command
from scripts.gse122069_full_control import run,Bins
from scripts.summarize_gse122069_full_control import summarize

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'reports/gse122069-resource-plan/input_manifest.json'

class RunConfigurationTests(unittest.TestCase):
    def rows(self):return load_rows(MANIFEST)
    def receipt(self,config):
        # Synthetic metadata fixture; no assertion that any file was downloaded.
        return {'run':config['run'],'gsm':config['gsm'],'expected_bytes':config['expected_fastq_bytes'],
                'bytes':config['expected_fastq_bytes'],'expected_md5':config['expected_md5'],
                'md5':config['expected_md5'],'sha256':'a'*64,'verified':True}
    def counts(self,n=2,size=1):
        bins=Bins(size,n)
        for i in range(n):bins.start('synthetic'+str(i),True)
        own=bins.finish();hts=copy.deepcopy(own);hts['locus_bins']=[{} for b in hts['completed_bins']]
        return own,hts
    def test_frozen_manifest_and_default_selection(self):
        c=configure(self.rows());self.assertEqual(c['run'],'SRR8144907');self.assertEqual(c['max_reads'],1000000)
        self.assertEqual(c['phase_deadline_seconds'],1800);self.assertEqual(c['primary_anchor'],15)
    def test_manifest_byte_change_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'manifest.json';p.write_bytes(MANIFEST.read_bytes()+b'\n')
            with self.assertRaises(ValueError):load_rows(p)
    def test_unknown_or_duplicate_selection_rejected(self):
        rows=self.rows()
        with self.assertRaises(ValueError):configure(rows,'SRR9999999')
        with self.assertRaises(ValueError):configure(rows+[rows[0]])
    def test_complete_count_bound_to_selected_library(self):
        with self.assertRaises(ValueError):configure(self.rows(),'SRR8144908',37518164,True)
        c=configure(self.rows(),'SRR8144908',54292655,True)
        self.assertEqual(c['bin_reads'],[1000000]*54+[292655])
    def test_nonpositive_or_excess_reads_rejected(self):
        for n in (0,-1,True,54292656):
            with self.assertRaises(ValueError):configure(self.rows(),'SRR8144908',n)
    def test_deadline_requires_explicit_selection(self):
        self.assertEqual(configure(self.rows(),'SRR8144908')['phase_deadline_seconds'],1800)
        self.assertEqual(configure(self.rows(),'SRR8144908',deadline=2700)['phase_deadline_seconds'],2700)
        for deadline in (0,-1,2701,True):
            with self.assertRaises(ValueError):configure(self.rows(),deadline=deadline)
    def test_partition_guard_before_large_allocation(self):
        with self.assertRaises(ValueError):partition(66940547,1)
        with self.assertRaises(ValueError):partition(26,0)
    def test_legacy_one_million_alignment_argv_identical(self):
        old=json.loads((ROOT/'reports/gse122069-pilot-20261031/pilot_command.json').read_text())['command']
        self.assertEqual(aligner_command(old[3],old[old.index('-x')+1],1000000),old)
    def test_legacy_full_alignment_argv_identical(self):
        old=json.loads((ROOT/'reports/gse122069-full-control-20261031/execution/full-control-results.json').read_text())['command']
        self.assertEqual(aligner_command(old[3],old[old.index('-x')+1],37518164),old)
    def test_historical_receipt_still_binds_first_control(self):
        receipt=json.loads((ROOT/'reports/gse122069-full-control-20261031/fastq-download.json').read_text())
        self.assertEqual(validate_receipt(configure(self.rows()),receipt),receipt['sha256'])
    def test_crossed_receipt_fields_rejected(self):
        c=configure(self.rows(),'SRR8144908');receipt=self.receipt(c)
        validate_receipt(c,receipt)
        for key,bad in [('run','SRR8144907'),('gsm','GSM3454242'),('bytes',1),('expected_bytes',1),('md5','0'*32),('expected_md5','0'*32),('verified','yes'),('sha256','not_a_hash'),('sha256',None),('sha256',9)]:
            with self.subTest(field=key),self.assertRaises(ValueError):validate_receipt(c,dict(receipt,**{key:bad}))
    def test_nonempty_output_refused_before_input_access(self):
        with tempfile.TemporaryDirectory() as d,patch('scripts.gse122069_full_control.verify_file') as verify:
            (Path(d)/'prior-result').write_text('preserve')
            with self.assertRaises(ValueError):run(SimpleNamespace(out=d))
            verify.assert_not_called();self.assertEqual((Path(d)/'prior-result').read_text(),'preserve')
    def test_crossed_receipt_fails_before_opening_fastq(self):
        with tempfile.TemporaryDirectory() as d,patch('scripts.gse122069_full_control.verify_file') as verify:
            receipt=Path(d)/'receipt.json';receipt.write_text(json.dumps(self.receipt(configure(self.rows()))))
            args=SimpleNamespace(out=str(Path(d)/'out'),run_accession='SRR8144908',manifest=str(MANIFEST),max_reads=1000000,bin_size=1000000,complete_library=False,phase_deadline_seconds=1800,download_record=str(receipt),fastq='MUST_NOT_OPEN')
            with self.assertRaises(ValueError):run(args)
            verify.assert_not_called();r=json.loads((Path(args.out)/'full-control-results.json').read_text());self.assertFalse(r['complete_library']);self.assertIn('receipt',r['error'])
    def test_summary_rejects_crossed_run(self):
        a,b=self.counts()
        with self.assertRaises(ValueError):summarize({'run':'SRR8144907'},a,b,run='SRR8144908')
    def test_summary_never_reuses_first_control_pilot_for_other_library(self):
        a,b=self.counts()
        with self.assertRaises(ValueError):summarize({'run':'SRR8144908'},a,b,{'counts':{}},run='SRR8144908')
    def test_partial_second_control_is_not_complete_or_pilot_compared(self):
        a,b=self.counts();r=summarize({'run':'SRR8144908','complete_library':False},a,b,run='SRR8144908',expected_reads=54292655)
        self.assertIsNone(r['complete_library_coverage_criterion_met']);self.assertIsNone(r['first1M_matches_historical_pilot'])
        self.assertEqual(r['concordant_completed_reads'],2)
    def test_synthetic_full_summary_validates_selected_partition(self):
        a,b=self.counts(8,3);r=summarize({'run':'SRR8144908','complete_library':True,'reads':8},a,b,run='SRR8144908',expected_reads=8,bin_size=3)
        self.assertTrue(r['complete_library']);self.assertEqual(r['concordant_completed_bins'],3)
        with self.assertRaises(ValueError):summarize({'run':'SRR8144908','complete_library':True,'reads':8},a,b,run='SRR8144908',expected_reads=8,bin_size=4)
    def test_summary_requires_locus_qc_for_completed_prefix(self):
        a,b=self.counts();b['locus_bins']=[]
        with self.assertRaises(ValueError):summarize({'run':'SRR8144908'},a,b,run='SRR8144908')


class DownloadSelectionTests(unittest.TestCase):
    def test_download_plan_cannot_be_used_as_verified_receipt(self):
        from scripts.fetch_gse122069_ranges import download_plan
        rows=load_rows(MANIFEST);plan=download_plan({'rows':rows},'SRR8144908')
        self.assertEqual(plan['expected_bytes'],1640602052);self.assertTrue(plan['etag_verification_pending'])
        with self.assertRaises(ValueError):validate_receipt(configure(rows,'SRR8144908'),plan)
    def test_planning_never_calls_network(self):
        from scripts.fetch_gse122069_ranges import download_plan
        with patch('urllib.request.urlopen') as network:
            plan=download_plan({'rows':load_rows(MANIFEST)})
            self.assertEqual(plan['run'],'SRR8144907');network.assert_not_called()


class TransportDeadlineTests(unittest.TestCase):
    def test_global_deadline_kills_synthetic_process_and_marks_unverified(self):
        import sys,time
        from scripts.fetch_gse122069_ranges import bounded_download,download_plan
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'receipt.json';plan=download_plan({'rows':load_rows(MANIFEST)},'SRR8144908');start=time.monotonic()
            with self.assertRaises(RuntimeError):bounded_download([sys.executable,'-c','import time; time.sleep(10)'],p,plan,deadline=0.02)
            r=json.loads(p.read_text());self.assertFalse(r['verified']);self.assertIn('TimeoutError',r['error']);self.assertLess(time.monotonic()-start,3)
    def test_successful_exit_without_verified_receipt_fails_closed(self):
        import sys
        from scripts.fetch_gse122069_ranges import bounded_download,download_plan
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'receipt.json';plan=download_plan({'rows':load_rows(MANIFEST)})
            with self.assertRaises(RuntimeError):bounded_download([sys.executable,'-c','pass'],p,plan,deadline=2)
            self.assertFalse(json.loads(p.read_text())['verified'])
    def test_existing_receipt_is_preserved_before_process_launch(self):
        from scripts.fetch_gse122069_ranges import bounded_download
        with tempfile.TemporaryDirectory() as d,patch('subprocess.Popen') as launch:
            p=Path(d)/'receipt.json';p.write_text('prior receipt')
            with self.assertRaises(ValueError):bounded_download(['must_not_launch'],p,{})
            launch.assert_not_called();self.assertEqual(p.read_text(),'prior receipt')


class InvalidChildReceiptTests(unittest.TestCase):
    def test_interrupted_or_invalid_child_json_cannot_escape_failure_record(self):
        import sys
        from scripts.fetch_gse122069_ranges import bounded_download,download_plan
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'receipt.json';plan=download_plan({'rows':load_rows(MANIFEST)})
            cmd=[sys.executable,'-c','import sys; from pathlib import Path; Path(sys.argv[1]).write_text("invalid JSON")',str(p)]
            with self.assertRaises(RuntimeError):bounded_download(cmd,p,plan,deadline=2)
            r=json.loads(p.read_text());self.assertFalse(r['verified']);self.assertIn('invalid child',r['error']);self.assertIn('invalid_child_receipt_sha256',r)


class SuccessfulChildReceiptTests(unittest.TestCase):
    def test_supervisor_preserves_valid_historical_receipt_schema(self):
        import sys
        from scripts.fetch_gse122069_ranges import bounded_download,download_plan
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'receipt.json';plan=download_plan({'rows':load_rows(MANIFEST)})
            source=ROOT/'reports/gse122069-full-control-20261031/fastq-download.json'
            cmd=[sys.executable,'-c','import shutil,sys; shutil.copyfile(sys.argv[1],sys.argv[2])',str(source),str(p)]
            result=bounded_download(cmd,p,plan,deadline=2)
            self.assertTrue(result['verified']);self.assertEqual(result['run'],'SRR8144907')
            self.assertEqual(result['sha256'],json.loads(source.read_text())['sha256'])

if __name__=='__main__':unittest.main()
