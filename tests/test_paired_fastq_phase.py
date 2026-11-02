import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import unittest
from unittest.mock import patch

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
try:
    from pilot_dry_runner import DryRunner
    import paired_fastq_phase as phase_module
    from bounded_http_transport import transfer_http
finally:sys.path.pop(0)


class PhaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.data=[gzip.compress(b''.join(f'@fixture{i}/{m}\nACGT\n+\nIIII\n'.encode() for i in range(3)),mtime=0) for m in (1,2)]
        self.expected=[{'bytes':len(b),'md5':hashlib.md5(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest()} for b in self.data]
        self.manifest={'paired_fastq':{'pair':{'mates':[{'identity':f'fixture/R{i+1}','transfer':f'mate{i+1}','expected':e} for i,e in enumerate(self.expected)],'prefix_pairs':2}}}
        self.limits={'wall_seconds':100,'transfer_bytes':10000,'disk_bytes':2*1024**2,'reserve_bytes':0}
        self.a=None
        self.addCleanup(self.close)
    def close(self):
        if self.a:self.a.close();self.a=None
    def open(self):
        self.a=DryRunner(self.root,self.manifest,self.limits,clock=lambda:100);return self.a
    def ready(self):
        a=self.open()
        for i,b in enumerate(self.data):a.transfer(f'mate{i+1}',[b],self.expected[i])
        return a
    def verified(self):
        a=self.ready();a.paired_fastq('pair');return a
    def reopen_rejected(self):
        self.close()
        with self.assertRaises((ValueError,FileNotFoundError)):self.open()
    def test_success_resume_same_deadline_consumption_and_prefix(self):
        a=self.verified();before=json.loads(json.dumps(a.state));out=self.root/'paired-fastq/pair';stamp=(out/'prefix-R1.fastq.gz').stat().st_mtime_ns
        self.close();b=self.open();b.paired_fastq('pair')
        self.assertEqual(b.state,before);self.assertEqual((out/'prefix-R1.fastq.gz').stat().st_mtime_ns,stamp)
        result=json.loads((out/'result.json').read_text());self.assertEqual(result['pairs_scanned'],3)
        self.assertEqual(before['transfer_bytes_consumed'],sum(map(len,self.data)))
    def test_changed_manifest_identity_or_order_rejected(self):
        self.verified();self.close();original=copy.deepcopy(self.manifest)
        for mutation in ('identity','order','prefix'):
            self.manifest=copy.deepcopy(original);spec=self.manifest['paired_fastq']['pair']
            if mutation=='identity':spec['mates'][0]['identity']='other'
            elif mutation=='order':spec['mates'].reverse()
            else:spec['prefix_pairs']=1
            with self.assertRaises(ValueError):self.open()
    def test_changed_limits_rejected(self):
        self.verified();self.close();self.limits['wall_seconds']+=1
        with self.assertRaises(ValueError):self.open()
    def test_source_tamper_on_same_instance_rejected(self):
        a=self.verified();(self.root/'mate1').write_bytes(b'changed')
        with self.assertRaises(ValueError):a.paired_fastq('pair')
    def test_prefix_tamper_on_reopen_rejected(self):
        self.verified();(self.root/'paired-fastq/pair/prefix-R2.fastq.gz').write_bytes(b'partial');self.reopen_rejected()
    def test_pair_receipt_tamper_rejected(self):
        self.verified();(self.root/'paired-fastq/pair/receipt.json').write_text('{"status":"started"}');self.reopen_rejected()
    def test_result_missing_rejected(self):
        self.verified();(self.root/'paired-fastq/pair/result.json').unlink();self.reopen_rejected()
    def test_transfer_receipt_changed_rejected(self):
        a=self.verified();a.state['phases']['mate1']['signature']='changed';a.save();self.reopen_rejected()
    def test_manifest_expected_mismatch_before_start(self):
        a=self.ready();a.manifest['paired_fastq']['pair']['mates'][0]['expected']['md5']='0'*32
        with self.assertRaises(ValueError):a.paired_fastq('pair')
        self.assertNotIn('pair',a.state['phases'])
    def test_unverified_transfer_rejected(self):
        a=self.ready();a.state['phases']['mate1']['status']='started'
        with self.assertRaises(ValueError):a.paired_fastq('pair')
    def test_crc_failure_after_prefix_blocks_resume(self):
        bad=bytearray(self.data[1]);bad[-8]^=1;self.data[1]=bytes(bad)
        self.expected[1].update(md5=hashlib.md5(bad).hexdigest(),sha256=hashlib.sha256(bad).hexdigest())
        a=self.ready()
        with self.assertRaises(gzip.BadGzipFile):a.paired_fastq('pair')
        self.assertEqual(a.state['phases']['pair']['status'],'failed');self.reopen_rejected()
    def test_keyboard_interrupt_marks_failed(self):
        a=self.ready()
        with patch.object(phase_module,'validate_pair',side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):a.paired_fastq('pair')
        self.assertEqual(a.state['phases']['pair']['status'],'failed');self.reopen_rejected()
    def test_hard_exit_leaves_started_partial_and_preserves_budget(self):
        a=self.ready();before=copy.deepcopy(a.state);self.close()
        code="""import sys,os,json
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from pilot_dry_runner import DryRunner
import paired_fastq_phase as phase
root=Path(sys.argv[2]);manifest=json.loads(sys.argv[3]);limits=json.loads(sys.argv[4])
r=DryRunner(root,manifest,limits,clock=lambda:100)
original=phase.validate_pair
def interrupted(*args,**kwargs):
    guard=kwargs['checkpoint'];count=[0]
    def stop():
        guard();count[0]+=1
        if count[0]==5:os._exit(73)
    kwargs['checkpoint']=stop
    return original(*args,**kwargs)
phase.validate_pair=interrupted
r.paired_fastq('pair')
"""
        p=subprocess.run([sys.executable,'-c',code,str(SCRIPTS),str(self.root),json.dumps(self.manifest),json.dumps(self.limits)],capture_output=True)
        self.assertEqual(p.returncode,73,p.stderr.decode());after=json.loads((self.root/'ledger.json').read_text())
        self.assertEqual(after['phases']['pair']['status'],'started')
        self.assertTrue((self.root/'paired-fastq/pair/prefix-R1.fastq.gz.partial').exists())
        for key in ('deadline_epoch','transfer_bytes_consumed'):self.assertEqual(before[key],after[key])
        self.reopen_rejected()
    def test_existing_orphan_output_not_adopted(self):
        a=self.ready();(self.root/'paired-fastq/pair').mkdir(parents=True)
        with self.assertRaises(FileExistsError):a.paired_fastq('pair')
        self.assertEqual(a.state['phases']['pair']['status'],'failed')
    def test_mutation_during_scan_rejected_before_phase_verified(self):
        a=self.ready();original=phase_module.validate_pair
        def mutate(*args,**kwargs):
            result=original(*args,**kwargs);(self.root/'mate1').write_bytes(b'changed');return result
        with patch.object(phase_module,'validate_pair',side_effect=mutate):
            with self.assertRaises(ValueError):a.paired_fastq('pair')
        self.assertFalse((self.root/'paired-fastq/pair/receipt.json').exists());self.reopen_rejected()
    def test_http_receipt_is_bound_and_rechecked(self):
        a=self.ready();p=a.state['phases']['mate1'];p['attempts_used']=1
        receipt=self.root/'mate1.attempt-0.json';rec={'status':'verified','attempt':0,'body_bytes':p['bytes'],'md5':p['md5'],'sha256':p['sha256']}
        receipt.write_text(json.dumps(rec));a.save();a.paired_fastq('pair')
        rec['attempt']=99;receipt.write_text(json.dumps(rec));self.reopen_rejected()
    def test_http_incomplete_receipt_rejected(self):
        a=self.ready();a.state['phases']['mate1']['attempts_used']=1
        (self.root/'mate1.attempt-0.json').write_text('{"status":"started"}')
        with self.assertRaises(ValueError):a.paired_fastq('pair')
    def test_loopback_http_to_pair_and_resume(self):
        payloads=self.data;requests=[]
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_GET(self):
                requests.append(self.path);data=payloads[int(self.path[-1])-1]
                self.send_response(200);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            a=self.open();origin=f'http://127.0.0.1:{server.server_port}'
            for i,e in enumerate(self.expected,1):transfer_http(a,f'mate{i}',origin+f'/mate{i}',e,[origin])
            a.paired_fastq('pair');before=copy.deepcopy(a.state);self.close()
            b=self.open();b.paired_fastq('pair');self.assertEqual(before,b.state);self.assertEqual(len(requests),2)
        finally:server.shutdown();server.server_close();thread.join()
    def test_deadline_reached_no_reset(self):
        a=self.verified();deadline=a.state['deadline_epoch'];self.close()
        with self.assertRaises(RuntimeError):DryRunner(self.root,self.manifest,self.limits,clock=lambda:deadline)


if __name__=='__main__':unittest.main()
