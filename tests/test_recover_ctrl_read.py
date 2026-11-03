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
import recover_ctrl_read as mod
from process_supervisor_v2 import atomic_json,supervise


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.original=self.root/'failed';self.original.mkdir();self.out=mod.recovery_root(self.original);self.out.mkdir()
        self.data=b'bounded paired FASTQ fixture\n'*100;self.start=73;partial=self.data[:self.start];(self.original/'CTRL_R1.attempt-0.partial').write_bytes(partial)
        self.obs={'root':str(self.original),'partial_bytes':self.start,'partial_sha256':hashlib.sha256(partial).hexdigest(),'charged_body_bytes':1500,'prior_transfer_elapsed_seconds':4272.2037699222565,'prior_global_deadline_epoch':1793698176.656901,'cached_index':{}}
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
        self.assertEqual((self.out/'CTRL_R1.fastq.gz').read_bytes(),self.data)
        self.assertEqual((self.original/'CTRL_R1.attempt-0.partial').read_bytes(),self.data[:self.start])
        self.assertFalse((self.out/'recovery-seal.json').exists())
        result=json.loads((self.out/'recovery-result.json').read_text());self.assertEqual(result['cumulative_body_bytes'],1500+len(self.data)-self.start)
        atomic_json(self.out/'recovery-plan.json',self.plan);atomic_json(self.out/'operator-acceptance.json',{'prepared_sha256':mod.meta_sha(self.out/'recovery-plan.json'),'accepted_additional_time_window':True})
        (self.out/'supervision').mkdir()
        record={'status':'finished','exit_code':0,'violation':None,'live_group_members_after_cleanup':[]};atomic_json(self.out/'supervision/run.json',record)
        with patch.object(mod,'SOURCE',self.source):seal=mod.accept_outer(self.out,self.plan,record)
        self.assertEqual(seal['status'],'sealed_verified_ctrl_r1');self.assertFalse(seal['raw_execution_ready'])
    def test_bad_headers_redirect_or_short_body_never_promoted(self):
        for mode in ('full','range','length','encoding','chunked','duplicate','multipart','redirect','short'):
            with self.subTest(mode=mode):
                if (self.out/'recovery-state.json').exists():(self.out/'recovery-state.json').unlink()
                for name in ('recovered-CTRL_R1.partial','CTRL_R1.fastq.gz'):
                    if (self.out/name).exists():(self.out/name).unlink()
                self.server(mode)
                with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',return_value=self.obs),self.assertRaises(Exception):mod.recover(self.budget())
                self.assertFalse((self.out/'CTRL_R1.fastq.gz').exists());self.assertFalse((self.out/'recovery-seal.json').exists())
    def test_corrupt_whole_md5_rejected(self):
        self.server('corrupt')
        with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',return_value=self.obs),self.assertRaisesRegex(ValueError,'MD5'):mod.recover(self.budget())
        self.assertFalse((self.out/'CTRL_R1.fastq.gz').exists())
    def test_changed_partial_rejected_before_http(self):
        (self.original/'CTRL_R1.attempt-0.partial').write_bytes(b'X'*self.start)
        with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',return_value=self.obs),patch.object(mod,'range_append',side_effect=AssertionError('No HTTP')) as network,self.assertRaises(ValueError):mod.recover(self.budget())
        network.assert_not_called()
    def test_original_changed_during_recovery_no_promotion(self):
        self.server()
        with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',side_effect=[self.obs,{**self.obs,'changed':True}]),self.assertRaises(ValueError):mod.recover(self.budget())
        self.assertFalse((self.out/'CTRL_R1.fastq.gz').exists())
    def test_prior_charge_floor_and_deadline(self):
        with patch.object(mod,'disk_guard'):
            b=self.budget();b.state['transfer_bytes_consumed']=1499
            self.assertRaises(RuntimeError,b.guard);b.state['transfer_bytes_consumed']=1500;b.state['deadline_epoch']=0
            self.assertRaises(RuntimeError,b.guard)
    def test_no_automatic_budget_reopen(self):
        self.budget();self.assertRaises(ValueError,self.budget)
    def test_missing_time_or_sha_acceptance_before_filesystem(self):
        with patch.object(mod,'read',side_effect=AssertionError('No descriptor access')),patch.object(mod,'meta_sha',side_effect=AssertionError('No SHA access')):
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
        with patch.object(mod,'disk_guard'),patch.object(mod.urllib.request,'build_opener') as opener:
            opener.return_value.open.return_value=Response();b=self.budget();b.begin('range')
            self.assertRaises(TimeoutError,mod.range_append,b,self.out/'tail.partial',self.source,self.start)
            self.assertEqual(b.state['transfer_bytes_consumed'],1500+len(self.data)-self.start)
            self.assertEqual(json.loads((self.out/'range-attempt.json').read_text())['status'],'failed')
            self.assertEqual(opener.return_value.open.call_args.kwargs['timeout'],30)
    def test_external_guard_rejects_refunded_charge(self):
        self.budget();state=json.loads((self.out/'recovery-state.json').read_text());state['transfer_bytes_consumed']=0;atomic_json(self.out/'recovery-state.json',state)
        with patch.object(mod,'disk_guard'):self.assertRaises(RuntimeError,mod.monitor(self.plan,mod.time.monotonic()))
    def test_lineage_disk_includes_all_five_roots(self):
        dirs=[self.root/f'lineage{i}' for i in range(3)]
        for d in dirs:d.mkdir();(d/'x').write_bytes(b'12345')
        self.obs['cached_index']=dict(zip(('original_root','recovery_root','index_root'),map(str,dirs)))
        p=copy.deepcopy(self.plan);p['limits']={**mod.LIMITS,'disk_bytes':14,'reserve_bytes':0}
        self.assertRaises(RuntimeError,mod.disk_guard,p)
    def test_partial_symlink_refused(self):
        p=self.original/'CTRL_R1.attempt-0.partial';p.unlink();p.symlink_to(self.root/'other')
        with self.assertRaises(ValueError):mod.base.copy_prefix(p,self.out/'copy',{'bytes':self.start,'sha256':self.obs['partial_sha256']},lambda:None)


class ProposalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.original=Path(self.tmp.name)/'failed';self.original.mkdir()
        self.obs={'root':str(self.original),'partial_bytes':354631727,'partial_sha256':'a'*64,'charged_body_bytes':4712318573,'prior_transfer_elapsed_seconds':4272.2037699222565,'prior_global_deadline_epoch':1793698176.656901,'cached_index':{}}
    def plan(self):
        with patch.object(mod,'inspect',return_value=self.obs),patch.object(mod,'identity',return_value={}),patch.object(mod.shutil,'disk_usage',return_value=type('D',(),{'free':100*mod.GiB})()):return mod.prepare(self.original)
    def test_prepare_never_network_or_process(self):
        with patch.object(mod.urllib.request,'build_opener',side_effect=AssertionError('No network')),patch.object(mod,'supervise',side_effect=AssertionError('No process')):p=self.plan()
        self.assertFalse(p['execution_enabled']);self.assertEqual(p['source']['bytes']-p['range_start'],606225236)
        self.assertEqual(p['original_audit']['charged_body_bytes']+606225236,5318543809)
    def test_fixed_plan_mutations_rejected(self):
        p=self.plan()
        with patch.object(mod,'identity',return_value={}):self.assertEqual(mod.validate_plan(p),mod.recovery_root(self.original))
        for key,value in [('execution_enabled',True),('range_start',0),('range_end',0),('root',str(self.original)),('scope','other'),('limits',{}),('source',{})]:
            q=copy.deepcopy(p);q[key]=value
            with self.subTest(key=key),patch.object(mod,'identity',return_value={}),self.assertRaises(ValueError):mod.validate_plan(q)
        for key in ('charged_body_bytes','prior_transfer_elapsed_seconds','prior_global_deadline_epoch'):
            q=copy.deepcopy(p);q['original_audit'][key]=0
            with self.subTest(key=key),patch.object(mod,'identity',return_value={}),self.assertRaises(ValueError):mod.validate_plan(q)
    def test_existing_root_refused(self):
        mod.recovery_root(self.original).mkdir()
        with patch.object(mod,'inspect',side_effect=AssertionError('No audit')):self.assertRaises(ValueError,mod.prepare,self.original)
    def test_low_disk_refused(self):
        with patch.object(mod,'inspect',return_value=self.obs),patch.object(mod.shutil,'disk_usage',return_value=type('D',(),{'free':1})()):self.assertRaises(ValueError,mod.prepare,self.original)
    def test_actual_supervised_worker_fails_before_http(self):
        p=self.plan();p['identity']=mod.identity();out=Path(p['root']);out.mkdir();atomic_json(out/'recovery-plan.json',p);atomic_json(out/'operator-acceptance.json',{'prepared_sha256':mod.meta_sha(out/'recovery-plan.json'),'accepted_additional_time_window':True})
        record=supervise('run',[sys.executable,str(Path(mod.__file__).resolve()),'--worker',str(out/'recovery-plan.json')],out/'supervision',timeout=10,rss_limit=mod.LIMITS['rss_bytes'],address_space=mod.LIMITS['address_space_bytes'])
        self.assertEqual(record['exit_code'],1);self.assertEqual(record['live_group_members_after_cleanup'],[]);self.assertFalse((out/'range-attempt.json').exists());self.assertFalse((out/'recovery-seal.json').exists())


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.binding={'fixture':True,'index_root':'/synthetic/index'};job={'root':str(self.root),'manifest':{'cached_index':self.binding}};atomic_json(self.root/'workflow-job.json',job);self.sha=mod.meta_sha(self.root/'workflow-job.json')
        atomic_json(self.root/'operator-acceptance.json',{'prepared_file_sha256':self.sha,'accepted_cached_run_window':True})
        atomic_json(self.root/'cached-preflight.json',{'status':'verified','cached_index':self.binding})
        state={'fingerprint':mod.FINGERPRINT,'mode':'real-pilot','transfer_bytes_consumed':4712318573,'transfer_elapsed_seconds':523.6879758834839,'cumulative_transfer_elapsed_seconds':4272.2037699222565,'prior_transfer_elapsed_seconds':3748.5157940387726,'deadline_epoch':1793698176.656901,'phases':{'preflight':{'status':'verified','receipt':'cached-preflight.json','receipt_sha256':mod.meta_sha(self.root/'cached-preflight.json')},'CTRL_R1':{'status':'failed','error':'TimeoutError: The read operation timed out','reservation_start_body_bytes':352321536,'unsettled_body_reservation_bytes':4194304}}}
        atomic_json(self.root/'ledger.json',state);(self.root/'workflow-receipts').mkdir();atomic_json(self.root/'workflow-receipts/run.json',{'status':'finished','exit_code':1,'violation':None,'live_group_members_after_cleanup':[]})
        atomic_json(self.root/'CTRL_R1.attempt-0.json',{'status':'failed','attempt':0,'body_bytes':354631727,'expected_checksums':{'md5':mod.SOURCE['md5']},'accounting':'durable-block-reservation-v1','reservation_block_bytes':4194304,'reserve_reads':True,'error':'TimeoutError: The read operation timed out'})
        with (self.root/'CTRL_R1.attempt-0.partial').open('wb') as f:f.truncate(354631727)
    def audit(self):
        with patch.object(mod,'JOB_SHA',self.sha),patch.object(mod.real,'validate_job'),patch.object(mod.cached,'index_binding',return_value=self.binding),patch.object(mod.base,'file_hash',return_value={'bytes':354631727,'sha256':'a'*64}):return mod.inspect(self.root)
    def test_audit_preserves_reserved_difference(self):
        obs=self.audit();self.assertEqual(obs['charged_body_bytes']-4355802733-obs['partial_bytes'],1884113)
        self.assertEqual(obs['prior_transfer_elapsed_seconds'],4272.2037699222565)
    def test_audit_rejects_changed_charge_attempt_and_supervision(self):
        for name,key,value in [('ledger.json','transfer_bytes_consumed',0),('CTRL_R1.attempt-0.json','body_bytes',1),('workflow-receipts/run.json','live_group_members_after_cleanup',[123]),('operator-acceptance.json','accepted_cached_run_window',False)]:
            path=self.root/name;before=path.read_bytes();rec=json.loads(before);rec[key]=value;atomic_json(path,rec)
            with self.subTest(name=name),self.assertRaises(ValueError):self.audit()
            path.write_bytes(before)

if __name__=='__main__':unittest.main()
