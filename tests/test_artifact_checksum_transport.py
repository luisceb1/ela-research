import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts';sys.path.insert(0,str(SCRIPTS))
try:
    import bounded_http_transport as http
    from pilot_dry_runner import DryRunner
finally:sys.path.pop(0)


class ChecksumTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.r=DryRunner(self.tmp.name,{},dict(wall_seconds=20,transfer_bytes=100,disk_bytes=1024**2,reserve_bytes=0));self.addCleanup(self.r.close)
        self.data=b'abcdef';self.expected={'bytes':6,'md5':hashlib.md5(self.data).hexdigest(),'sha256':hashlib.sha256(self.data).hexdigest()}
    def fetch(self,expected,*,truncated_first=False,attempts=1):
        data=self.data;calls=[]
        class Response:
            status=200;headers={'Content-Length':'6'}
            def __init__(self,b):self.body=io.BytesIO(b)
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read1(self,n):return self.body.read(n)
        class Opener:
            def open(self,*args,**kw):
                calls.append(1);return Response(data[:3] if truncated_first and len(calls)==1 else data)
        with patch.object(http.urllib.request,'build_opener',return_value=Opener()):return http.transfer_http(self.r,'body','http://127.0.0.1/data',expected,['http://127.0.0.1'],attempts=attempts,reserve_reads=True)
    def test_sha256_only_accepted_without_provider_md5(self):
        p=self.fetch({k:v for k,v in self.expected.items() if k!='md5'});self.assertEqual(p['status'],'verified')
        rec=json.loads((Path(self.tmp.name)/'body.attempt-0.json').read_text());self.assertEqual(rec['expected_checksums'],{'sha256':self.expected['sha256']})
    def test_md5_only_kept(self):self.assertEqual(self.fetch({k:v for k,v in self.expected.items() if k!='sha256'})['status'],'verified')
    def test_both_checksums_are_required_when_supplied(self):
        self.assertRaises(ValueError,self.fetch,{**self.expected,'md5':'0'*32});self.assertEqual(self.r.state['transfer_bytes_consumed'],6)
    def test_wrong_sha_rejected_despite_correct_md5(self):self.assertRaises(ValueError,self.fetch,{**self.expected,'sha256':'0'*64})
    def test_bad_schema_rejected_before_network_or_phase(self):
        cases=[{'bytes':6},{'bytes':6,'sha256':None},{'bytes':True,'sha256':'a'*64},{'bytes':-1,'sha256':'a'*64},{'bytes':6,'sha256':'A'*64},{'bytes':6,'sha256':'a'*63},{'bytes':6,'md5':''},{**self.expected,'unknown':'x'}]
        with patch.object(http.urllib.request,'build_opener') as opener:
            for expected in cases:
                with self.subTest(expected=expected):self.assertRaises(ValueError,http.transfer_http,self.r,'bad','http://127.0.0.1/a',expected,['http://127.0.0.1'])
            opener.assert_not_called()
        self.assertEqual(self.r.state['phases'],{})
    def test_sha_only_retry_preserves_charged_failed_bytes(self):
        self.fetch({'bytes':6,'sha256':self.expected['sha256']},truncated_first=True,attempts=2);self.assertEqual(self.r.state['transfer_bytes_consumed'],9)
    def test_synthetic_transfer_sha_only_and_dual_checksum_rejection(self):
        self.r.transfer('sha',[self.data],{'bytes':6,'sha256':self.expected['sha256']})
        self.assertRaises(ValueError,self.r.transfer,'bad',[self.data],{**self.expected,'sha256':'0'*64})


if __name__=='__main__':unittest.main()
