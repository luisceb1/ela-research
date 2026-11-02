import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

scripts=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(scripts))
try:
    spec=importlib.util.spec_from_file_location('pilot_dry_runner',scripts/'pilot_dry_runner.py')
    runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
finally:sys.path.pop(0)

class RunnerTests(unittest.TestCase):
    def limits(self,**extra):return {'wall_seconds':30,'transfer_bytes':100,'disk_bytes':2*1024**2,'reserve_bytes':0,**extra}
    def expected(self,b=b'abc'):return {'bytes':len(b),'md5':hashlib.md5(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest()}
    def test_success_resume_no_new_transfer_and_same_deadline(self):
        with tempfile.TemporaryDirectory() as d:
            a=runner.DryRunner(d,{},self.limits());a.transfer('mate',[b'abc'],self.expected());deadline=a.state['deadline_epoch'];a.close()
            b=runner.DryRunner(d,{},self.limits());b.transfer('mate',[],self.expected())
            self.assertEqual(b.state['transfer_bytes_consumed'],3);self.assertEqual(b.state['deadline_epoch'],deadline);b.close()
    def test_changed_manifest_or_limits_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            a=runner.DryRunner(d,{},self.limits());a.close()
            for manifest,limits in [({'new':1},self.limits()),({},self.limits(transfer_bytes=101))]:
                with self.assertRaises(ValueError):runner.DryRunner(d,manifest,limits)
    def test_failed_transfer_charged_and_not_automatically_resumed(self):
        with tempfile.TemporaryDirectory() as d:
            a=runner.DryRunner(d,{},self.limits(transfer_bytes=5));a.transfer('one',[b'abc'],self.expected())
            with self.assertRaises(RuntimeError):a.transfer('two',[b'abc'],self.expected())
            self.assertEqual(a.state['transfer_bytes_consumed'],6);a.close()
            with self.assertRaises(ValueError):runner.DryRunner(d,{},self.limits(transfer_bytes=5))
    def test_checksum_failure_keeps_partial_and_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            a=runner.DryRunner(d,{},self.limits());bad={**self.expected(),'md5':'0'*32}
            with self.assertRaises(ValueError):a.transfer('one',[b'abc'],bad)
            self.assertEqual(a.state['phases']['one']['status'],'failed');self.assertTrue((Path(d)/'one.partial').exists());a.close()
    def test_verified_file_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            a=runner.DryRunner(d,{},self.limits());a.transfer('one',[b'abc'],self.expected());a.close();(Path(d)/'one').write_bytes(b'xyz')
            with self.assertRaises(ValueError):runner.DryRunner(d,{},self.limits())
    def test_deadline_not_reset_on_resume(self):
        with tempfile.TemporaryDirectory() as d:
            a=runner.DryRunner(d,{},self.limits(),clock=lambda:100);a.close()
            with self.assertRaises(RuntimeError):runner.DryRunner(d,{},self.limits(),clock=lambda:131)
    def test_interrupted_phase_blocks_resume(self):
        with tempfile.TemporaryDirectory() as d:
            a=runner.DryRunner(d,{},self.limits());a.begin('one','transfer','synthetic');a.close()
            with self.assertRaises(ValueError):runner.DryRunner(d,{},self.limits())
    def test_disk_limit_and_phase_type_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            a=runner.DryRunner(d,{},self.limits());a.transfer('one',[b'abc'],self.expected())
            with self.assertRaises(RuntimeError):a.process('one',[sys.executable,'-c','pass'])
            (Path(d)/'big').write_bytes(b'x'*(2*1024**2))
            with self.assertRaises(RuntimeError):a.guard()
            a.close()
    def test_supervisor_process_and_receipt_reuse(self):
        with tempfile.TemporaryDirectory() as d:
            args=[sys.executable,'-c','print("synthetic")'];a=runner.DryRunner(d,{},self.limits());a.process('process',args);a.close()
            b=runner.DryRunner(d,{},self.limits());self.assertEqual(b.process('process',args)['status'],'verified');b.close()
    def test_global_guard_callback_kills_process(self):
        with tempfile.TemporaryDirectory() as d:
            a=runner.DryRunner(d,{},self.limits());calls=[0]
            def stop():
                calls[0]+=1
                if calls[0]>2:raise RuntimeError('injected global guard')
            a.guard=stop
            with self.assertRaises(RuntimeError):a.process('stop',[sys.executable,'-c','import time;time.sleep(2)'])
            self.assertEqual(a.state['phases']['stop']['status'],'failed')
            receipt=json.loads((Path(d)/'process-receipts/stop.json').read_text());self.assertEqual(receipt['status'],'finished');self.assertIn('supervisor_error',receipt);a.close()

if __name__=='__main__':unittest.main()
