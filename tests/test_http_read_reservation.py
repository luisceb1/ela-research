import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts';sys.path.insert(0,str(SCRIPTS))
try:
    import bounded_http_transport as transport
    from pilot_dry_runner import DryRunner
finally:sys.path.pop(0)


class ReservationTests(unittest.TestCase):
    def test_read_exception_keeps_maximum_charged_and_blocks_resume(self):
        with tempfile.TemporaryDirectory() as d:
            limits={'wall_seconds':20,'transfer_bytes':8,'disk_bytes':1024**2,'reserve_bytes':0};r=DryRunner(d,{},limits)
            class Response:
                status=200;headers={'Content-Length':'8'}
                def __enter__(self):return self
                def __exit__(self,*args):pass
                def read1(self,n):
                    ledger=json.loads((Path(d)/'ledger.json').read_text())
                    self_test.assertEqual(ledger['transfer_bytes_consumed'],n)
                    raise TimeoutError('unknown body delivered before error')
            self_test=self
            class Opener:
                def open(self,*args,**kw):return Response()
            with patch.object(transport.urllib.request,'build_opener',return_value=Opener()):
                with self.assertRaises(TimeoutError):transport.transfer_http(r,'body','http://127.0.0.1/a',{'bytes':8,'md5':'0'*32},['http://127.0.0.1'],chunk_size=8,reserve_reads=True)
            self.assertEqual(r.state['transfer_bytes_consumed'],8);r.close()
            with self.assertRaises(ValueError):DryRunner(d,{},limits)
    def test_short_read_refunds_only_proven_unused_reservation(self):
        import hashlib
        with tempfile.TemporaryDirectory() as d:
            data=b'abc';r=DryRunner(d,{},{'wall_seconds':20,'transfer_bytes':3,'disk_bytes':1024**2,'reserve_bytes':0})
            class Response:
                status=200;headers={'Content-Length':'3'}
                def __init__(self):self.stream=io.BytesIO(data)
                def __enter__(self):return self
                def __exit__(self,*args):pass
                def read1(self,n):return self.stream.read(1)
            class Opener:
                def open(self,*args,**kw):return Response()
            try:
                with patch.object(transport.urllib.request,'build_opener',return_value=Opener()):transport.transfer_http(r,'body','http://127.0.0.1/a',{'bytes':3,'md5':hashlib.md5(data).hexdigest()},['http://127.0.0.1'],reserve_reads=True)
                self.assertEqual(r.state['transfer_bytes_consumed'],3);self.assertEqual(r.state['phases']['body']['unsettled_body_reservation_bytes'],0)
            finally:r.close()


if __name__=='__main__':unittest.main()
