import hashlib
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import importlib.util
from pathlib import Path
import sys
import tempfile
import threading
import unittest

scripts=Path(__file__).resolve().parents[1]/'scripts';sys.path.insert(0,str(scripts))
try:
    import bounded_http_transport as http
    from pilot_dry_runner import DryRunner
finally:sys.path.pop(0)

DATA=b'0123456789abcdef'
class Handler(BaseHTTPRequestHandler):
    counts={}
    def log_message(self,*args):pass
    def do_GET(self):
        self.counts[self.path]=self.counts.get(self.path,0)+1
        if self.path=='/redirect':
            self.send_response(302);self.send_header('Location','/ok');self.end_headers();return
        self.send_response(200);self.send_header('Content-Length',str(len(DATA)+1 if self.path=='/badlength' else len(DATA)));self.end_headers()
        data=DATA
        if self.path=='/truncated' or (self.path=='/retry' and self.counts[self.path]==1):data=DATA[:5]
        self.wfile.write(data);self.close_connection=True

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.origin='http://127.0.0.1:'+str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def setUp(self):Handler.counts={};self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
    def runner(self,cap=100):
        r=DryRunner(self.tmp.name,{'synthetic':True},{'wall_seconds':20,'transfer_bytes':cap,'disk_bytes':2*1024**2,'reserve_bytes':0});self.addCleanup(r.close);return r
    def expected(self):return {'bytes':len(DATA),'md5':hashlib.md5(DATA).hexdigest(),'sha256':hashlib.sha256(DATA).hexdigest()}
    def fetch(self,r,path,**kw):return http.transfer_http(r,'body',self.origin+path,self.expected(),[self.origin],chunk_size=3,**kw)
    def test_success_and_cached_reuse(self):
        r=self.runner();self.fetch(r,'/ok');self.fetch(r,'/ok');self.assertEqual(r.state['transfer_bytes_consumed'],len(DATA));self.assertEqual(Handler.counts['/ok'],1)
    def test_truncated_bytes_charged(self):
        r=self.runner()
        with self.assertRaises(ValueError):self.fetch(r,'/truncated')
        self.assertEqual(r.state['transfer_bytes_consumed'],5);self.assertEqual(r.state['phases']['body']['status'],'failed')
    def test_retry_keeps_failed_bytes_and_both_receipts(self):
        r=self.runner();self.fetch(r,'/retry',attempts=2);self.assertEqual(r.state['transfer_bytes_consumed'],5+len(DATA));self.assertEqual(len(list(Path(self.tmp.name).glob('body.attempt-*.json'))),2)
    def test_retry_refused_if_budget_insufficient(self):
        r=self.runner(cap=len(DATA))
        with self.assertRaises(RuntimeError):self.fetch(r,'/retry',attempts=2)
        self.assertEqual(r.state['transfer_bytes_consumed'],5);self.assertEqual(Handler.counts['/retry'],1)
    def test_length_rejected_before_body_read(self):
        r=self.runner()
        with self.assertRaises(ValueError):self.fetch(r,'/badlength')
        self.assertEqual(r.state['transfer_bytes_consumed'],0)
    def test_budget_rejected_before_connection(self):
        r=self.runner(cap=8)
        with self.assertRaises(RuntimeError):self.fetch(r,'/ok')
        self.assertEqual(Handler.counts,{})
    def test_read_sizes_never_exceed_balance_or_expected_remainder(self):
        import io
        from unittest.mock import patch
        class Response:
            status=200;headers={'Content-Length':str(len(DATA))}
            def __init__(self):self.stream=io.BytesIO(DATA);self.requests=[]
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read1(self,n):self.requests.append(n);return self.stream.read(n)
        response=Response()
        class Opener:
            def open(self,*args,**kw):return response
        r=self.runner(cap=len(DATA))
        with patch.object(http.urllib.request,'build_opener',return_value=Opener()):self.fetch(r,'/ok')
        self.assertEqual(response.requests,[3,3,3,3,3,1]);self.assertEqual(r.state['transfer_bytes_consumed'],16)
    def test_hash_failure_still_charged(self):
        r=self.runner();e={**self.expected(),'md5':'0'*32}
        with self.assertRaises(ValueError):http.transfer_http(r,'body',self.origin+'/ok',e,[self.origin])
        self.assertEqual(r.state['transfer_bytes_consumed'],len(DATA))
    def test_redirect_and_origin_refused(self):
        r=self.runner()
        with self.assertRaises(ValueError):self.fetch(r,'/redirect')
        self.assertNotIn('/ok',Handler.counts)
        with self.assertRaises(ValueError):http.transfer_http(r,'other','http://not-allowed.invalid/a',self.expected(),[self.origin])

if __name__=='__main__':unittest.main()
