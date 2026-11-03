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
import recover_ctrl_r2_resume as mod
from process_supervisor_v2 import atomic_json,supervise


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.original=self.root/'failed';self.original.mkdir();self.out=mod.recovery_root(self.original);self.out.mkdir()
        self.data=b'bounded paired FASTQ fixture\n'*100;self.start=73;partial=self.data[:self.start];(self.original/'recovered-CTRL_R2.partial').write_bytes(partial)
        self.obs={'root':str(self.original),'partial_bytes':self.start,'partial_sha256':hashlib.sha256(partial).hexdigest(),'charged_body_bytes':mod.CHARGED,'prior_transfer_elapsed_seconds':14500.072928190231,'prior_global_deadline_epoch':1793707865.1037116,'previous_transfer_elapsed_seconds':12700.072928190231,'interrupted_transfer_window_seconds_reserved':1800,'previous_audit':{},'prior_wsl_charged_bytes':mod.WSL_CHARGED,'manual_browser_reserved_body_bytes':mod.MANUAL_BROWSER_RESERVE,'manual_browser_exact_body_known':False}
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
        atomic_json(self.out/'recovery-plan.json',self.plan);atomic_json(self.out/'operator-acceptance.json',{'prepared_sha256':mod.sha(self.out/'recovery-plan.json'),'accepted_additional_time_window':True,'browser_stopped_and_manual_reserve_accepted':True})
        (self.out/'supervision').mkdir()
        record={'status':'finished','exit_code':0,'violation':None,'live_group_members_after_cleanup':[]};atomic_json(self.out/'supervision/run.json',record)
        with patch.object(mod.previous.previous,'SOURCE',self.source):seal=mod.accept_outer(self.out,self.plan,record)
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
        self.obs={'root':str(self.original),'partial_bytes':900375051,'partial_sha256':'a'*64,'charged_body_bytes':mod.CHARGED,'prior_transfer_elapsed_seconds':14500.072928190231,'prior_global_deadline_epoch':1793707865.1037116,'previous_transfer_elapsed_seconds':12700.072928190231,'interrupted_transfer_window_seconds_reserved':1800,'previous_audit':{},'prior_wsl_charged_bytes':mod.WSL_CHARGED,'manual_browser_reserved_body_bytes':mod.MANUAL_BROWSER_RESERVE,'manual_browser_exact_body_known':False}
    def plan(self):
        with patch.object(mod,'inspect',return_value=self.obs),patch.object(mod,'identity',return_value={}),patch.object(mod.shutil,'disk_usage',return_value=type('D',(),{'free':100*mod.GiB})()):return mod.prepare(self.original)
    def test_prepare_never_network_or_process(self):
        with patch.object(mod.transport.urllib.request,'build_opener',side_effect=AssertionError('No network')),patch.object(mod,'supervise',side_effect=AssertionError('No process')):p=self.plan()
        self.assertFalse(p['execution_enabled']);self.assertEqual(p['source']['bytes']-p['range_start'],97174406)
        self.assertEqual(p['original_audit']['charged_body_bytes']+97174406,7319237336)
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
        p=self.plan();p['identity']=mod.identity();out=Path(p['root']);out.mkdir();atomic_json(out/'recovery-plan.json',p);atomic_json(out/'operator-acceptance.json',{'prepared_sha256':mod.sha(out/'recovery-plan.json'),'accepted_additional_time_window':True,'browser_stopped_and_manual_reserve_accepted':True})
        record=supervise('run',[sys.executable,str(Path(mod.__file__).resolve()),'--worker',str(out/'recovery-plan.json')],out/'supervision',timeout=10,rss_limit=mod.LIMITS['rss_bytes'],address_space=mod.LIMITS['address_space_bytes'])
        self.assertEqual(record['exit_code'],1);self.assertEqual(record['live_group_members_after_cleanup'],[]);self.assertFalse((out/'range-attempt.json').exists());self.assertFalse((out/'recovery-seal.json').exists())


class InterruptedResumeAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'interrupted';self.root.mkdir()
        self.audit={'root':str(self.root/'previous'),'prior_transfer_elapsed_seconds':12700.072928190231,'prior_global_deadline_epoch':1793705199.6269245}
        self.plan={'original_root':self.audit['root'],'original_audit':self.audit}
        atomic_json(self.root/'recovery-plan.json',self.plan);self.sha=mod.sha(self.root/'recovery-plan.json')
        atomic_json(self.root/'operator-acceptance.json',{'prepared_sha256':self.sha,'accepted_additional_time_window':True})
        (self.root/'supervision').mkdir()
        self.outer={'status':'finished','exit_code':-9,'supervisor_error':'KeyboardInterrupt: ','live_group_members_after_cleanup':[]}
        atomic_json(self.root/'supervision/run.json',self.outer);(self.root/'supervision/run.log').write_text('')
        self.state={'status':'started','limits':mod.previous.LIMITS,'transfer_bytes_consumed':mod.WSL_CHARGED,
            'prior_transfer_elapsed_seconds':12700.072928190231,'original_deadline_epoch':1793705199.6269245,
            'deadline_epoch':1793707865.1037116,'phases':{'copy':{'status':'verified'},'range':{
                'status':'started','started_epoch':1793705473.6378129,'deadline_epoch':1793707273.6378129,
                'reservation_start_body_bytes':20971520,'unsettled_body_reservation_bytes':4194304}}}
        atomic_json(self.root/'recovery-state.json',self.state)
        self.attempt={'status':'started','body_bytes':20971520,'range_start':876279389,'range_end':997549456,
            'prior_charged_bytes':6199347649,'attempts':1,'address_family':'IPv4',
            'accounting':'durable-block-reservation-v1','reservation_block_bytes':4194304}
        atomic_json(self.root/'range-attempt.json',self.attempt)
        with (self.root/'recovered-CTRL_R2.partial').open('wb') as f:f.truncate(mod.PARTIAL_BYTES)
    def call(self):
        with patch.object(mod,'PRIOR_PLAN_SHA',self.sha),patch.object(mod.previous,'validate_plan',return_value=self.root),patch.object(mod.previous,'inspect',return_value=self.audit),patch.object(mod.transport.base,'file_hash',return_value={'bytes':mod.PARTIAL_BYTES,'sha256':'a'*64}):return mod.inspect(self.root)
    def test_keyboard_interrupt_partial_charge_and_browser_reserve(self):
        obs=self.call();self.assertEqual(obs['prior_wsl_charged_bytes'],6224513473)
        self.assertEqual(obs['reserved_minus_actual_body_bytes'],1070162)
        self.assertEqual(obs['manual_browser_reserved_body_bytes'],997549457)
        self.assertFalse(obs['manual_browser_exact_body_known'])
        self.assertEqual(obs['charged_body_bytes'],7222062930)
        self.assertEqual(obs['charged_body_bytes']+997549457-900375051,7319237336)
        self.assertEqual(obs['prior_transfer_elapsed_seconds'],14500.072928190231)
    def test_changed_charge_clock_or_later_phase_refused(self):
        for key,value in [('transfer_bytes_consumed',0),('prior_transfer_elapsed_seconds',0),('deadline_epoch',0)]:
            r=copy.deepcopy(self.state);r[key]=value;atomic_json(self.root/'recovery-state.json',r)
            with self.subTest(key=key),self.assertRaises(ValueError):self.call()
        r=copy.deepcopy(self.state);r['phases']['verify']={'status':'started'};atomic_json(self.root/'recovery-state.json',r)
        self.assertRaises(ValueError,self.call)
    def test_changed_receipt_or_reservation_refused(self):
        for key,value in [('body_bytes',0),('address_family','IPv6'),('reservation_block_bytes',0)]:
            r=copy.deepcopy(self.attempt);r[key]=value;atomic_json(self.root/'range-attempt.json',r)
            with self.subTest(key=key),self.assertRaises(ValueError):self.call()
        atomic_json(self.root/'range-attempt.json',self.attempt)
    def test_wrong_stop_reason_or_group_refused(self):
        for key,value in [('live_group_members_after_cleanup',[123]),('supervisor_error','different')]:
            r=copy.deepcopy(self.outer);r[key]=value;atomic_json(self.root/'supervision/run.json',r)
            with self.subTest(key=key),self.assertRaises(ValueError):self.call()
        atomic_json(self.root/'supervision/run.json',self.outer)
    def test_partial_grew_refused(self):
        with (self.root/'recovered-CTRL_R2.partial').open('ab') as f:f.write(b'x')
        self.assertRaises(ValueError,self.call)
    def test_browser_stop_acceptance_before_any_read(self):
        with patch.object(mod,'sha',side_effect=AssertionError('No filesystem')):
            self.assertRaises(ValueError,mod.execute,'absent','a'*64,True,False)
    def test_same_tls_ipv4_transport(self):
        self.assertIs(mod.range_append,mod.previous.range_append)
    def test_ten_roots_counted(self):
        dirs=[Path(self.tmp.name)/f'tree{i}' for i in range(10)]
        for d in dirs:d.mkdir();(d/'x').write_bytes(b'123')
        b={'index':dict(zip(('original_root','recovery_root','index_root'),map(str,dirs[:3]))),'original_root':str(dirs[3]),'root':str(dirs[4])}
        tls={'root':str(dirs[6]),'pilot_audit':{'root':str(dirs[5]),'read_binding':b}}
        ipv4={'root':str(dirs[7]),'ipv4_audit':tls}
        p={'original_root':str(dirs[8]),'root':str(dirs[9]),'original_audit':{'previous_audit':ipv4},'limits':{**mod.LIMITS,'disk_bytes':29,'reserve_bytes':0}}
        self.assertRaises(RuntimeError,mod.disk_guard,p)

if __name__=='__main__':unittest.main()
