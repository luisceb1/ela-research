import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import bounded_http_transport as transport
from pilot_dry_runner import DryRunner


class BlockReservationTests(unittest.TestCase):
    def invoke(self,data,block=None,short=16384,fail_at=None,truncate=None,inspect_read=None,md5=None):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);root=Path(self.tmp.name)
        r=DryRunner(root,{},{'wall_seconds':30,'transfer_bytes':len(data),'disk_bytes':32*1024**2,'reserve_bytes':0});self.addCleanup(r.close)
        self.runner=r;self.root=root
        class Response:
            status=200;headers={'Content-Length':str(len(data))}
            def __init__(self):self.stream=io.BytesIO(data if truncate is None else data[:truncate])
            def __enter__(self):return self
            def __exit__(self,*a):pass
            def read1(self,n):
                if inspect_read:inspect_read(r,self.stream.tell(),n)
                if fail_at is not None and self.stream.tell()>=fail_at:raise TimeoutError('uncertain read')
                return self.stream.read(min(n,short))
        class Opener:
            def open(self,*a,**k):return Response()
        expected={'bytes':len(data),'md5':md5 or hashlib.md5(data).hexdigest()}
        with patch.object(transport.urllib.request,'build_opener',return_value=Opener()):
            return transport.transfer_http(r,'payload','http://127.0.0.1/a',expected,['http://127.0.0.1'],reserve_reads=True,reservation_block_bytes=block)
    def test_credit_durable_before_each_short_read(self):
        data=b'a'*(1024**2+13);block=256*1024
        def check(r,pos,n):
            ledger=json.loads((r.root/'ledger.json').read_text())
            self.assertGreaterEqual(ledger['transfer_bytes_consumed'],pos+n)
            self.assertLessEqual(ledger['transfer_bytes_consumed'],len(data))
        phase=self.invoke(data,block,inspect_read=check)
        self.assertEqual(phase['sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(self.runner.state['transfer_bytes_consumed'],len(data))
        self.assertEqual(phase['unsettled_body_reservation_bytes'],0)
    def test_unknown_read_exception_keeps_entire_pending_block(self):
        data=b'a'*1024**2
        self.assertRaises(TimeoutError,self.invoke,data,256*1024,fail_at=16384)
        self.assertEqual(self.runner.state['transfer_bytes_consumed'],256*1024)
        self.assertEqual(self.runner.state['phases']['payload']['unsettled_body_reservation_bytes'],256*1024)
        self.assertEqual(self.runner.state['phases']['payload']['status'],'failed')
        self.assertFalse((self.root/'payload').exists())
    def test_known_eof_refunds_only_proven_unused_credit(self):
        data=b'a'*1024**2
        self.assertRaises(ValueError,self.invoke,data,256*1024,truncate=12345)
        self.assertEqual(self.runner.state['transfer_bytes_consumed'],12345)
        self.assertFalse((self.root/'payload').exists())
    def test_checksum_mismatch_not_promoted(self):
        self.assertRaises(ValueError,self.invoke,b'a'*100000,65536,md5='0'*32)
        self.assertFalse((self.root/'payload').exists())
    def test_fewer_syncs_with_identical_verified_result(self):
        actual=transport.os.fsync;counts=[];hashes=[]
        for block in (None,1024**2):
            counter=[0]
            def sync(fd):counter[0]+=1;return actual(fd)
            with patch.object(transport.os,'fsync',side_effect=sync):
                phase=self.invoke(b'z'*(2*1024**2),block)
            counts.append(counter[0]);hashes.append(phase['sha256'])
        self.assertEqual(hashes[0],hashes[1]);self.assertGreater(counts[0],counts[1]*10)
    def test_failed_block_cannot_be_automatically_reopened(self):
        self.assertRaises(TimeoutError,self.invoke,b'a'*1024**2,256*1024,fail_at=16384)
        self.runner.close()
        self.assertRaises(ValueError,DryRunner,self.root,{},self.runner.state['limits'])
    def test_sigkill_mid_block_keeps_durable_credit_and_blocks_adoption(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);script=root/'kill-control.py';run=root/'run'
            code="""import io,os,signal,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,SCRIPTS)
import bounded_http_transport as t
from pilot_dry_runner import DryRunner
r=DryRunner(ROOT,{}, {'wall_seconds':30,'transfer_bytes':1048576,'disk_bytes':2097152,'reserve_bytes':0})
class Response:
 status=200;headers={'Content-Length':'1048576'}
 def __init__(self):self.calls=0
 def __enter__(self):return self
 def __exit__(self,*a):pass
 def read1(self,n):
  self.calls+=1
  if self.calls>1:os.kill(os.getpid(),signal.SIGKILL)
  return b'a'*16384
class Opener:
 def open(self,*a,**k):return Response()
with patch.object(t.urllib.request,'build_opener',return_value=Opener()):
 t.transfer_http(r,'body','http://127.0.0.1/a',{'bytes':1048576,'md5':'0'*32},['http://127.0.0.1'],reserve_reads=True,reservation_block_bytes=1048576)
"""
            code=code.replace('SCRIPTS',repr(str(Path(__file__).resolve().parents[1]/'scripts'))).replace('ROOT',repr(str(run)))
            script.write_text(code);result=subprocess.run([sys.executable,str(script)],capture_output=True,timeout=10)
            self.assertEqual(result.returncode,-9,result.stderr.decode())
            ledger=json.loads((run/'ledger.json').read_text())
            self.assertEqual(ledger['transfer_bytes_consumed'],1048576)
            self.assertEqual(ledger['phases']['body']['status'],'started')
            self.assertGreaterEqual(ledger['transfer_bytes_consumed'],(run/'body.attempt-0.partial').stat().st_size)
            self.assertRaises(ValueError,DryRunner,run,{},ledger['limits'])
    def test_invalid_block_rejected_before_phase(self):
        for value in (0,True,65535,8*1024**2+1):
            with self.subTest(value=value):
                self.assertRaises(ValueError,self.invoke,b'a'*1024**2,value)
                self.assertEqual(self.runner.state['phases'],{})


if __name__=='__main__':unittest.main()
