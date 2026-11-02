import copy
import gzip
import hashlib
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
try:
    from external_local_stage import run_local_stage
    from pilot_dry_runner import DryRunner
finally:sys.path.pop(0)


def expected(data):return {'bytes':len(data),'md5':hashlib.md5(data).hexdigest(),'sha256':hashlib.sha256(data).hexdigest()}


class ExternalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.stop=threading.Event();self.entered=threading.Event();self.sent=[];self.payload=b'x'*128
        outer=self
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_GET(self):
                outer.entered.set()
                if self.path=='/headers':outer.stop.wait(10);return
                self.send_response(200);self.send_header('Content-Length',str(len(outer.payload)));self.end_headers()
                if self.path=='/body':outer.stop.wait(10);return
                try:
                    if self.path=='/slow':
                        for byte in outer.payload:
                            self.wfile.write(bytes([byte]));self.wfile.flush();outer.sent.append(byte)
                            if outer.stop.wait(.05):break
                    else:self.wfile.write(outer.payload)
                except (BrokenPipeError,ConnectionResetError):pass
        self.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.addCleanup(self.shutdown)
        self.manifest={'fixture':'external-local-synthetic'}
        self.limits={'wall_seconds':30,'transfer_bytes':1024,'disk_bytes':4*1024**2,'reserve_bytes':0}
    def shutdown(self):
        self.stop.set();self.server.shutdown();self.server.server_close();self.thread.join()
    def stage(self,path='/ok'):
        return {'kind':'http','name':'body','url':f'http://127.0.0.1:{self.server.server_port}'+path,'expected':expected(self.payload),'chunk_size':1}
    def run_stage(self,stage=None,**kw):return run_local_stage(self.root,self.manifest,self.limits,self.stage() if stage is None else stage,timeout=kw.pop('timeout',1),**kw)
    def ledger(self):return json.loads((self.root/'ledger.json').read_text())
    def assert_killed(self,rec):
        self.assertEqual(rec['status'],'finished');self.assertEqual(rec['violation'],'timeout')
        self.assertEqual(rec['exit_code'],-9);self.assertEqual(rec['live_group_members_after_cleanup'],[])
        self.assertLess(rec['elapsed_seconds'],5)
        outcome=json.loads((self.root/'external-receipts'/f"{rec['name']}.outcome.json").read_text());self.assertEqual(outcome['status'],'failed')
    def assert_blocked_reopen(self):
        before=self.ledger()
        with self.assertRaises(ValueError):DryRunner(self.root,self.manifest,self.limits)
        after=self.ledger()
        for key in ('deadline_epoch','transfer_bytes_consumed'):self.assertEqual(before[key],after[key])
    def test_success_and_cached_runner_reopen(self):
        rec=self.run_stage(timeout=5);self.assertEqual(rec['exit_code'],0);self.assertIsNone(rec['violation'])
        before=self.ledger();self.assertEqual(before['transfer_bytes_consumed'],128)
        self.assertEqual(before['phases']['body']['unsettled_body_reservation_bytes'],0)
        r=DryRunner(self.root,self.manifest,self.limits)
        try:self.assertEqual(r.state,before)
        finally:r.close()
    def test_blocked_headers_killed_without_body_charge(self):
        rec=self.run_stage(self.stage('/headers'));self.assertTrue(self.entered.is_set());self.assert_killed(rec)
        ledger=self.ledger();self.assertEqual(ledger['transfer_bytes_consumed'],0);self.assertEqual(ledger['phases']['body']['status'],'started');self.assert_blocked_reopen()
    def test_blocked_body_keeps_durable_reservation(self):
        rec=self.run_stage(self.stage('/body'));self.assert_killed(rec)
        ledger=self.ledger();self.assertEqual(ledger['transfer_bytes_consumed'],1)
        self.assertEqual(ledger['phases']['body']['unsettled_body_reservation_bytes'],1)
        self.assertEqual(json.loads((self.root/'body.attempt-0.json').read_text())['status'],'started');self.assert_blocked_reopen()
    def test_slow_progress_cannot_extend_external_timeout(self):
        rec=self.run_stage(self.stage('/slow'));self.assert_killed(rec);self.assertGreater(len(self.sent),2)
        ledger=self.ledger();receipt=json.loads((self.root/'body.attempt-0.json').read_text())
        self.assertGreater(receipt['body_bytes'],2);self.assertGreaterEqual(ledger['transfer_bytes_consumed'],receipt['body_bytes'])
        self.assertEqual(ledger['phases']['body']['unsettled_body_reservation_bytes'],1);self.assert_blocked_reopen()
    def test_global_deadline_clips_outer_limit(self):
        self.limits['wall_seconds']=1.5;rec=self.run_stage(self.stage('/body'),timeout=10);self.assert_killed(rec)
        outcome=json.loads((self.root/'external-receipts/body.outcome.json').read_text())
        self.assertLessEqual(outcome['effective_timeout_seconds'],1.5)
    def prepare_pair(self):
        data=[gzip.compress(b''.join(f'@fixture{i}/{m}\nACGT\n+\nIIII\n'.encode() for i in range(3)),mtime=0) for m in (1,2)]
        self.manifest={'paired_fastq':{'pair':{'prefix_pairs':2,'mates':[{'identity':f'fixture/R{i+1}','transfer':f'mate{i+1}','expected':expected(b)} for i,b in enumerate(data)]}}}
        r=DryRunner(self.root,self.manifest,self.limits)
        try:
            for i,b in enumerate(data):r.transfer(f'mate{i+1}',[b],expected(b))
        finally:r.close()
        return {'kind':'paired_fastq','name':'pair'}
    def test_pair_success_supervised(self):
        stage=self.prepare_pair();rec=self.run_stage(stage,timeout=5);self.assertEqual(rec['exit_code'],0)
        r=DryRunner(self.root,self.manifest,self.limits)
        try:self.assertEqual(r.paired_fastq('pair')['status'],'verified')
        finally:r.close()
    def test_stalled_validator_and_descendant_killed(self):
        stage=self.prepare_pair();before=self.ledger();rec=self.run_stage(stage,synthetic_fault='stall_validator');self.assert_killed(rec)
        self.assertGreaterEqual(rec['max_group_members'],2)
        ledger=self.ledger();self.assertEqual(ledger['phases']['pair']['status'],'started')
        self.assertTrue((self.root/'paired-fastq/pair/prefix-R1.fastq.gz.partial').exists())
        self.assertFalse((self.root/'paired-fastq/pair/receipt.json').exists())
        for key in ('deadline_epoch','transfer_bytes_consumed'):self.assertEqual(before[key],ledger[key])
        self.assert_blocked_reopen()
    def test_non_loopback_and_arbitrary_stage_rejected_before_ledger(self):
        for change in ({'url':'https://127.0.0.1/a'},{'url':'http://example.com/a'},{'kind':'shell'},{'url':'http://localhost/a'}):
            with self.assertRaises(ValueError):self.run_stage({**self.stage(),**change})
        self.assertFalse((self.root/'ledger.json').exists())
    def test_existing_external_receipt_not_overwritten(self):
        self.run_stage(timeout=5);path=self.root/'external-receipts/body.json';before=path.read_bytes()
        with self.assertRaises(FileExistsError):self.run_stage()
        self.assertEqual(path.read_bytes(),before)
    def test_worker_nonzero_retains_external_failure(self):
        rec=self.run_stage(synthetic_fault='crash_worker');self.assertEqual(rec['exit_code'],74);self.assertIsNone(rec['violation'])
        self.assertEqual(json.loads((self.root/'external-receipts/body.outcome.json').read_text())['status'],'failed')


if __name__=='__main__':unittest.main()
