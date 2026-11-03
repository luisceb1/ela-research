"""Synthetic local HTTP only; no human FASTQ or index downloads."""
import copy
import hashlib
import http.server
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import recover_ctrl_r2_ipv4 as mod
from process_supervisor_v2 import atomic_json,supervise


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.original=self.root/'failed';self.original.mkdir();self.out=mod.recovery_root(self.original);self.out.mkdir()
        self.data=b'bounded paired FASTQ fixture\n'*100;self.start=73;partial=self.data[:self.start];(self.original/'recovered-CTRL_R2.partial').write_bytes(partial)
        self.obs={'root':str(self.original),'partial_bytes':self.start,'partial_sha256':hashlib.sha256(partial).hexdigest(),'charged_body_bytes':mod.CHARGED,'prior_transfer_elapsed_seconds':(mod.previous.CARRIED_SECONDS+32.35191988945007),'prior_global_deadline_epoch':1793704088.6492767,'previous_transfer_elapsed_seconds':mod.previous.CARRIED_SECONDS,'failed_tls_transfer_elapsed_seconds':32.35191988945007,'pilot_audit':{}}
        self.source={'url':'http://127.0.0.1/unused','bytes':len(self.data),'md5':hashlib.md5(self.data).hexdigest()}
        self.plan={'root':str(self.out),'original_root':str(self.original),'original_audit':self.obs,'source':self.source,'range_start':self.start,'range_end':len(self.data)-1,'limits':mod.LIMITS}
    def budget(self):return mod.Budget(self.plan)
    def server(self,mode='ok'):
        data=self.data;start=self.start
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(s):
                if s.headers.get('Range')!=f'bytes={start}-{len(data)-1}':s.send_error(400);return
                if mode=='redirect':s.send_response(302);s.send_header('Location','/elsewhere');s.end_headers();return
                body=data[start:]
                if mode=='corrupt':body=b'X'+body[1:]
                if mode=='short':body=body[:-1]
                s.send_response(200 if mode=='full' else 206)
                s.send_header('Content-Length',str(len(data)-start if mode!='length' else len(data)))
                s.send_header('Content-Range',f'bytes {start if mode!="range" else start+1}-{len(data)-1}/{len(data)}')
                if mode=='encoding':s.send_header('Content-Encoding','gzip')
                if mode=='chunked':s.send_header('Transfer-Encoding','chunked')
                if mode=='duplicate':s.send_header('Content-Length',str(len(body)))
                if mode=='multipart':s.send_header('Content-Type','multipart/byteranges')
                s.end_headers();s.wfile.write(body)
            def log_message(self,*args):pass
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        self.addCleanup(lambda:(server.shutdown(),server.server_close(),thread.join()))
        self.source['url']=f'http://127.0.0.1:{server.server_port}/fixture';return server
    def test_positive_actual_range_whole_hash_and_outer_seal(self):
        self.server()
        with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',return_value=self.obs):mod.recover(self.budget())
        self.assertEqual((self.out/'CTRL_R2.fastq.gz').read_bytes(),self.data)
        self.assertEqual((self.original/'recovered-CTRL_R2.partial').read_bytes(),self.data[:self.start])
        self.assertFalse((self.out/'recovery-seal.json').exists())
        result=json.loads((self.out/'recovery-result.json').read_text());self.assertEqual(result['cumulative_body_bytes'],mod.CHARGED+len(self.data)-self.start)
        atomic_json(self.out/'recovery-plan.json',self.plan);atomic_json(self.out/'operator-acceptance.json',{'prepared_sha256':mod.sha(self.out/'recovery-plan.json'),'accepted_additional_time_window':True})
        (self.out/'supervision').mkdir()
        record={'status':'finished','exit_code':0,'violation':None,'live_group_members_after_cleanup':[]};atomic_json(self.out/'supervision/run.json',record)
        with patch.object(mod,'SOURCE',self.source):seal=mod.accept_outer(self.out,self.plan,record)
        self.assertEqual(seal['status'],'sealed_verified_ctrl_r2_ipv4');self.assertFalse(seal['raw_execution_ready'])
    def test_bad_headers_redirect_or_short_body_never_promoted(self):
        for mode in ('full','range','length','encoding','chunked','duplicate','multipart','redirect','short'):
            with self.subTest(mode=mode):
                if (self.out/'recovery-state.json').exists():(self.out/'recovery-state.json').unlink()
                for name in ('recovered-CTRL_R2.partial','CTRL_R2.fastq.gz'):
                    if (self.out/name).exists():(self.out/name).unlink()
                self.server(mode)
                with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',return_value=self.obs),self.assertRaises(Exception):mod.recover(self.budget())
                self.assertFalse((self.out/'CTRL_R2.fastq.gz').exists());self.assertFalse((self.out/'recovery-seal.json').exists())
    def test_corrupt_whole_md5_rejected(self):
        self.server('corrupt')
        with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',return_value=self.obs),self.assertRaisesRegex(ValueError,'MD5'):mod.recover(self.budget())
        self.assertFalse((self.out/'CTRL_R2.fastq.gz').exists())
    def test_changed_partial_rejected_before_http(self):
        (self.original/'recovered-CTRL_R2.partial').write_bytes(b'X'*self.start)
        with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',return_value=self.obs),patch.object(mod,'range_append',side_effect=AssertionError('No HTTP')) as network,self.assertRaises(ValueError):mod.recover(self.budget())
        network.assert_not_called()
    def test_original_changed_during_recovery_no_promotion(self):
        self.server()
        with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',side_effect=[self.obs,{**self.obs,'changed':True}]),self.assertRaises(ValueError):mod.recover(self.budget())
        self.assertFalse((self.out/'CTRL_R2.fastq.gz').exists())
    def test_prior_charge_floor_and_deadline(self):
        with patch.object(mod,'disk_guard'):
            b=self.budget();b.state['transfer_bytes_consumed']=mod.CHARGED-1
            self.assertRaises(RuntimeError,b.guard);b.state['transfer_bytes_consumed']=mod.CHARGED;b.state['deadline_epoch']=0
            self.assertRaises(RuntimeError,b.guard)
    def test_no_automatic_budget_reopen(self):
        self.budget();self.assertRaises(ValueError,self.budget)
    def test_missing_time_or_sha_acceptance_before_filesystem(self):
        with patch.object(mod,'read',side_effect=AssertionError('No descriptor access')),patch.object(mod,'sha',side_effect=AssertionError('No SHA access')):
            self.assertRaises(ValueError,mod.execute,'absent',None,False)
        with patch.object(mod,'read',side_effect=AssertionError('No descriptor access')):self.assertRaises(ValueError,mod.execute,'absent','bad',True)
    def test_read_timeout_keeps_reserved_charge_and_failed_receipt(self):
        import email.message
        self.out.joinpath('tail.partial').write_bytes(self.data[:self.start])
        class Response:
            status=206
            headers=email.message.Message()
            def __enter__(s):return s
            def __exit__(s,*a):pass
            def read1(s,n):raise TimeoutError('synthetic socket stall')
        Response.headers['Content-Length']=str(len(self.data)-self.start);Response.headers['Content-Range']=f'bytes {self.start}-{len(self.data)-1}/{len(self.data)}'
        with patch.object(mod,'disk_guard'),patch.object(mod.transport.urllib.request,'build_opener') as opener:
            opener.return_value.open.return_value=Response();b=self.budget();b.begin('range')
            self.assertRaises(TimeoutError,mod.range_append,b,self.out/'tail.partial',self.source,self.start)
            self.assertEqual(b.state['transfer_bytes_consumed'],mod.CHARGED+len(self.data)-self.start)
            self.assertEqual(json.loads((self.out/'range-attempt.json').read_text())['status'],'failed')
            self.assertEqual(opener.return_value.open.call_args.kwargs['timeout'],30)
    def test_external_guard_rejects_refunded_charge(self):
        self.budget();state=json.loads((self.out/'recovery-state.json').read_text());state['transfer_bytes_consumed']=0;atomic_json(self.out/'recovery-state.json',state)
        with patch.object(mod,'disk_guard'):self.assertRaises(RuntimeError,mod.monitor(self.plan,mod.time.monotonic()))
    def test_partial_symlink_refused(self):
        p=self.original/'recovered-CTRL_R2.partial';p.unlink();p.symlink_to(self.root/'other')
        with self.assertRaises(ValueError):mod.transport.base.copy_prefix(p,self.out/'copy',{'bytes':self.start,'sha256':self.obs['partial_sha256']},lambda:None)


class ProposalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.original=Path(self.tmp.name)/'failed';self.original.mkdir()
        self.obs={'root':str(self.original),'partial_bytes':284799727,'partial_sha256':'a'*64,'charged_body_bytes':5603756481,'prior_transfer_elapsed_seconds':(mod.previous.CARRIED_SECONDS+32.35191988945007),'prior_global_deadline_epoch':1793704088.6492767,'previous_transfer_elapsed_seconds':mod.previous.CARRIED_SECONDS,'failed_tls_transfer_elapsed_seconds':32.35191988945007,'pilot_audit':{}}
    def plan(self):
        with patch.object(mod,'inspect',return_value=self.obs),patch.object(mod,'identity',return_value={}),patch.object(mod.shutil,'disk_usage',return_value=type('D',(),{'free':100*mod.GiB})()):return mod.prepare(self.original)
    def test_prepare_never_network_or_process(self):
        with patch.object(mod.transport.urllib.request,'build_opener',side_effect=AssertionError('No network')),patch.object(mod,'supervise',side_effect=AssertionError('No process')):p=self.plan()
        self.assertFalse(p['execution_enabled']);self.assertEqual(p['source']['bytes']-p['range_start'],712749730)
        self.assertEqual(p['original_audit']['charged_body_bytes']+712749730,6316506211)
    def test_fixed_plan_mutations_rejected(self):
        p=self.plan()
        with patch.object(mod,'identity',return_value={}):self.assertEqual(mod.validate_plan(p),mod.recovery_root(self.original))
        for key,value in [('execution_enabled',True),('range_start',0),('range_end',0),('root',str(self.original)),('scope','other'),('limits',{}),('source',{})]:
            q=copy.deepcopy(p);q[key]=value
            with self.subTest(key=key),patch.object(mod,'identity',return_value={}),self.assertRaises(ValueError):mod.validate_plan(q)
        for key in ('charged_body_bytes','prior_transfer_elapsed_seconds','previous_transfer_elapsed_seconds'):
            q=copy.deepcopy(p);q['original_audit'][key]=0
            with self.subTest(key=key),patch.object(mod,'identity',return_value={}),self.assertRaises(ValueError):mod.validate_plan(q)
    def test_existing_root_refused(self):
        mod.recovery_root(self.original).mkdir()
        with patch.object(mod,'inspect',side_effect=AssertionError('No audit')):self.assertRaises(ValueError,mod.prepare,self.original)
    def test_low_disk_refused(self):
        with patch.object(mod,'inspect',return_value=self.obs),patch.object(mod.shutil,'disk_usage',return_value=type('D',(),{'free':1})()):self.assertRaises(ValueError,mod.prepare,self.original)
    def test_actual_supervised_worker_fails_before_http(self):
        p=self.plan();p['identity']=mod.identity();out=Path(p['root']);out.mkdir();atomic_json(out/'recovery-plan.json',p);atomic_json(out/'operator-acceptance.json',{'prepared_sha256':mod.sha(out/'recovery-plan.json'),'accepted_additional_time_window':True})
        record=supervise('run',[sys.executable,str(Path(mod.__file__).resolve()),'--worker',str(out/'recovery-plan.json')],out/'supervision',timeout=10,rss_limit=mod.LIMITS['rss_bytes'],address_space=mod.LIMITS['address_space_bytes'])
        self.assertEqual(record['exit_code'],1);self.assertEqual(record['live_group_members_after_cleanup'],[]);self.assertFalse((out/'range-attempt.json').exists());self.assertFalse((out/'recovery-seal.json').exists())


class IPv4TLSTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import subprocess, ssl
        cls.tmp=tempfile.TemporaryDirectory();p=Path(cls.tmp.name);cls.cert=p/'cert.pem';cls.key=p/'key.pem'
        subprocess.run(['openssl','req','-x509','-newkey','rsa:2048','-nodes','-keyout',str(cls.key),
                        '-out',str(cls.cert),'-days','1','-subj','/CN=localhost',
                        '-addext','subjectAltName=DNS:localhost'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def tls_server(self):
        import ssl
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(s):
                s.send_response(206);s.send_header('Content-Length','4');s.send_header('Content-Range','bytes 2-5/6');s.end_headers();s.wfile.write(b'cdef')
            def log_message(self,*a):pass
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
        ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);ctx.load_cert_chain(self.cert,self.key)
        server.socket=ctx.wrap_socket(server.socket,server_side=True)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        self.addCleanup(lambda:(server.shutdown(),server.server_close(),thread.join()))
        return server
    def test_actual_https_uses_ipv4_and_validates_trusted_hostname(self):
        import ssl
        server=self.tls_server();context=ssl.create_default_context(cafile=str(self.cert))
        native=mod.socket.getaddrinfo;families=[]
        def lookup(host,port,family,*args):families.append(family);return native(host,port,family,*args)
        with patch.object(mod.socket,'getaddrinfo',side_effect=lookup):
            with mod.ipv4_opener(context).open(f'https://localhost:{server.server_port}/fixture',timeout=3) as response:
                self.assertEqual(response.read(),b'cdef');self.assertEqual(response.status,206)
        self.assertEqual(families,[mod.socket.AF_INET])
    def test_complete_recovery_over_actual_verified_tls_ipv4(self):
        import ssl
        server=self.tls_server();context=ssl.create_default_context(cafile=str(self.cert))
        with tempfile.TemporaryDirectory() as scratch:
            original=Path(scratch)/'failed';original.mkdir();out=Path(scratch)/'new';out.mkdir()
            (original/'recovered-CTRL_R2.partial').write_bytes(b'ab')
            data=b'abcdef';source={'url':f'https://localhost:{server.server_port}/fixture',
                'bytes':6,'md5':hashlib.md5(data).hexdigest()}
            obs={'root':str(original),'partial_bytes':2,'partial_sha256':hashlib.sha256(b'ab').hexdigest(),
                 'charged_body_bytes':mod.CHARGED,'prior_transfer_elapsed_seconds':mod.previous.CARRIED_SECONDS+32,
                 'prior_global_deadline_epoch':1793704088.6492767}
            plan={'root':str(out),'original_root':str(original),'original_audit':obs,'source':source,
                  'range_start':2,'range_end':5,'limits':mod.LIMITS}
            opener=mod.ipv4_opener(context)
            with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',return_value=obs),patch.object(mod,'ipv4_opener',return_value=opener):
                mod.recover(mod.Budget(plan))
            self.assertEqual((out/'CTRL_R2.fastq.gz').read_bytes(),data)
            result=json.loads((out/'recovery-result.json').read_text())
            self.assertEqual(result['md5'],source['md5']);self.assertEqual(result['cumulative_body_bytes'],mod.CHARGED+4)
            self.assertFalse((out/'recovery-seal.json').exists())
            self.assertEqual(json.loads((out/'range-attempt.json').read_text())['address_family'],'IPv4')

    def test_untrusted_certificate_is_rejected(self):
        server=self.tls_server()
        import urllib.error, ssl
        with self.assertRaises(urllib.error.URLError) as err:
            mod.ipv4_opener().open(f'https://localhost:{server.server_port}/fixture',timeout=3)
        self.assertIsInstance(err.exception.reason,ssl.SSLCertVerificationError)
    def test_hostname_mismatch_is_rejected_with_trusted_certificate(self):
        import ssl
        server=self.tls_server();context=ssl.create_default_context(cafile=str(self.cert))
        native=mod.socket.getaddrinfo
        def lookup(host,port,family,*args):return native('127.0.0.1',port,family,*args)
        with patch.object(mod.socket,'getaddrinfo',side_effect=lookup):
            import urllib.error
            with self.assertRaises(urllib.error.URLError) as err:
                mod.ipv4_opener(context).open(f'https://wrong.invalid:{server.server_port}/fixture',timeout=3)
            self.assertIsInstance(err.exception.reason,ssl.SSLCertVerificationError)
    def test_insecure_context_is_refused(self):
        import ssl
        self.assertRaises(ValueError,mod.ipv4_opener,ssl._create_unverified_context())
    def test_ipv4_connect_error_closes_socket_without_ipv6_retry(self):
        with patch.object(mod.socket,'getaddrinfo',return_value=[(mod.socket.AF_INET,mod.socket.SOCK_STREAM,6,'',('127.0.0.1',443))]) as dns,patch.object(mod.socket,'socket') as create:
            create.return_value.connect.side_effect=TimeoutError('fixture connect')
            self.assertRaises(TimeoutError,mod.connect_ipv4,('example.invalid',443),3)
            create.return_value.close.assert_called_once();dns.assert_called_once_with('example.invalid',443,mod.socket.AF_INET,mod.socket.SOCK_STREAM)


class FailedRecoveryAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'failed';self.root.mkdir()
        self.audit={'partial_bytes':mod.PARTIAL_BYTES,'partial_sha256':'a'*64,'prior_global_deadline_epoch':1793702652.9493718}
        self.plan={'original_root':str(self.root/'pilot'),'original_audit':self.audit}
        atomic_json(self.root/'recovery-plan.json',self.plan);self.sha=mod.sha(self.root/'recovery-plan.json')
        atomic_json(self.root/'operator-acceptance.json',{'prepared_sha256':self.sha,'accepted_additional_time_window':True})
        (self.root/'supervision').mkdir()
        atomic_json(self.root/'supervision/run.json',{'status':'finished','exit_code':1,'violation':None,'live_group_members_after_cleanup':[]})
        (self.root/'supervision/run.log').write_text('URLError: The handshake operation timed out')
        self.state={'status':'failed','error_type':'URLError','limits':mod.previous.LIMITS,
                    'transfer_bytes_consumed':mod.CHARGED,'prior_transfer_elapsed_seconds':mod.previous.CARRIED_SECONDS,
                    'original_deadline_epoch':1793702652.9493718,'deadline_epoch':1793704088.6492767,
                    'phases':{'copy':{'status':'verified','started_epoch':100,'finished_epoch':102},
                              'range':{'status':'failed','error_type':'URLError','started_epoch':103,'finished_epoch':135}}}
        atomic_json(self.root/'recovery-state.json',self.state)
        atomic_json(self.root/'range-attempt.json',{'status':'failed','error_type':'URLError','body_bytes':0,
            'attempts':1,'prior_charged_bytes':mod.CHARGED,'range_start':mod.PARTIAL_BYTES,'range_end':mod.SOURCE['bytes']-1})
        with (self.root/'recovered-CTRL_R2.partial').open('wb') as f:f.truncate(mod.PARTIAL_BYTES)
    def audit_call(self):
        with patch.object(mod,'FIRST_PLAN_SHA',self.sha),patch.object(mod.previous,'validate_plan',return_value=self.root),patch.object(mod.previous,'inspect',return_value=self.audit),patch.object(mod.transport.base,'file_hash',return_value={'bytes':mod.PARTIAL_BYTES,'sha256':'a'*64}):return mod.inspect(self.root)
    def test_zero_body_retains_failed_handshake_seconds(self):
        obs=self.audit_call();self.assertEqual(obs['charged_body_bytes'],mod.CHARGED)
        self.assertEqual(obs['prior_transfer_elapsed_seconds'],mod.previous.CARRIED_SECONDS+32)
    def test_body_received_or_refunded_clock_refused(self):
        p=self.root/'range-attempt.json';before=p.read_bytes();r=json.loads(before);r['body_bytes']=1;atomic_json(p,r)
        self.assertRaises(ValueError,self.audit_call);p.write_bytes(before)
        self.state['prior_transfer_elapsed_seconds']=0;atomic_json(self.root/'recovery-state.json',self.state)
        self.assertRaises(ValueError,self.audit_call)
    def test_nonempty_group_refused(self):
        p=self.root/'supervision/run.json';r=json.loads(p.read_text());r['live_group_members_after_cleanup']=[123];atomic_json(p,r)
        self.assertRaises(ValueError,self.audit_call)
    def test_changed_copied_prefix_refused(self):
        with patch.object(mod,'FIRST_PLAN_SHA',self.sha),patch.object(mod.previous,'validate_plan',return_value=self.root),patch.object(mod.previous,'inspect',return_value=self.audit),patch.object(mod.transport.base,'file_hash',return_value={'bytes':mod.PARTIAL_BYTES,'sha256':'b'*64}):
            self.assertRaises(ValueError,mod.inspect,self.root)
    def test_reserved_body_or_success_result_refused(self):
        self.state['phases']['range']['unsettled_body_reservation_bytes']=1;atomic_json(self.root/'recovery-state.json',self.state)
        self.assertRaises(ValueError,self.audit_call)
    def test_eight_lineage_trees_counted(self):
        dirs=[Path(self.tmp.name)/f'tree{i}' for i in range(8)]
        for d in dirs:d.mkdir();(d/'x').write_bytes(b'123')
        b={'index':dict(zip(('original_root','recovery_root','index_root'),map(str,dirs[:3]))),'original_root':str(dirs[3]),'root':str(dirs[4])}
        p={'original_root':str(dirs[6]),'root':str(dirs[7]),'original_audit':{'pilot_audit':{'root':str(dirs[5]),'read_binding':b}},'limits':{**mod.LIMITS,'disk_bytes':23,'reserve_bytes':0}}
        self.assertRaises(RuntimeError,mod.disk_guard,p)

if __name__=='__main__':unittest.main()
