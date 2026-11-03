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
import recover_ctrl_r2 as mod
from process_supervisor_v2 import atomic_json,supervise


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.original=self.root/'failed';self.original.mkdir();self.out=mod.recovery_root(self.original);self.out.mkdir()
        self.data=b'bounded paired FASTQ fixture\n'*100;self.start=73;partial=self.data[:self.start];(self.original/'CTRL_R2.attempt-0.partial').write_bytes(partial)
        self.obs={'root':str(self.original),'partial_bytes':self.start,'partial_sha256':hashlib.sha256(partial).hexdigest(),'charged_body_bytes':mod.CHARGED,'prior_transfer_elapsed_seconds':mod.CARRIED_SECONDS,'prior_global_deadline_epoch':1793702652.9493718,'last_snapshot_cumulative_seconds':7241.245675802231,'read_binding':{}}
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
        self.assertEqual((self.original/'CTRL_R2.attempt-0.partial').read_bytes(),self.data[:self.start])
        self.assertFalse((self.out/'recovery-seal.json').exists())
        result=json.loads((self.out/'recovery-result.json').read_text());self.assertEqual(result['cumulative_body_bytes'],mod.CHARGED+len(self.data)-self.start)
        atomic_json(self.out/'recovery-plan.json',self.plan);atomic_json(self.out/'operator-acceptance.json',{'prepared_sha256':mod.sha(self.out/'recovery-plan.json'),'accepted_additional_time_window':True})
        (self.out/'supervision').mkdir()
        record={'status':'finished','exit_code':0,'violation':None,'live_group_members_after_cleanup':[]};atomic_json(self.out/'supervision/run.json',record)
        with patch.object(mod,'SOURCE',self.source):seal=mod.accept_outer(self.out,self.plan,record)
        self.assertEqual(seal['status'],'sealed_verified_ctrl_r2');self.assertFalse(seal['raw_execution_ready'])
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
        (self.original/'CTRL_R2.attempt-0.partial').write_bytes(b'X'*self.start)
        with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',return_value=self.obs),patch.object(mod.transport,'range_append',side_effect=AssertionError('No HTTP')) as network,self.assertRaises(ValueError):mod.recover(self.budget())
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
            self.assertRaises(TimeoutError,mod.transport.range_append,b,self.out/'tail.partial',self.source,self.start)
            self.assertEqual(b.state['transfer_bytes_consumed'],mod.CHARGED+len(self.data)-self.start)
            self.assertEqual(json.loads((self.out/'range-attempt.json').read_text())['status'],'failed')
            self.assertEqual(opener.return_value.open.call_args.kwargs['timeout'],30)
    def test_external_guard_rejects_refunded_charge(self):
        self.budget();state=json.loads((self.out/'recovery-state.json').read_text());state['transfer_bytes_consumed']=0;atomic_json(self.out/'recovery-state.json',state)
        with patch.object(mod,'disk_guard'):self.assertRaises(RuntimeError,mod.monitor(self.plan,mod.time.monotonic()))
    def test_partial_symlink_refused(self):
        p=self.original/'CTRL_R2.attempt-0.partial';p.unlink();p.symlink_to(self.root/'other')
        with self.assertRaises(ValueError):mod.transport.base.copy_prefix(p,self.out/'copy',{'bytes':self.start,'sha256':self.obs['partial_sha256']},lambda:None)


class ProposalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.original=Path(self.tmp.name)/'failed';self.original.mkdir()
        self.obs={'root':str(self.original),'partial_bytes':284799727,'partial_sha256':'a'*64,'charged_body_bytes':5603756481,'prior_transfer_elapsed_seconds':mod.CARRIED_SECONDS,'prior_global_deadline_epoch':1793702652.9493718,'last_snapshot_cumulative_seconds':7241.245675802231,'read_binding':{}}
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
        for key in ('charged_body_bytes','prior_transfer_elapsed_seconds','prior_global_deadline_epoch'):
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


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'pilot';self.root.mkdir()
        self.binding={'bytes':960856963,'md5':'ed58daa011d6508a3e8d1f05bc39fc29',
                      'cumulative_body_bytes':5318543809,'prior_deadline_epoch':1793698176.656901}
        self.job={'root':str(self.root),'limits':{'fixture':True},'manifest':{
            'recovered_read':self.binding,'sealed_workflow':{'steps':[{
                'name':'CTRL_R2','kind':'http','url':mod.SOURCE['url'],
                'expected':{'bytes':mod.SOURCE['bytes'],'md5':mod.SOURCE['md5']}}]}}}
        atomic_json(self.root/'workflow-job.json',self.job);self.job_sha=mod.sha(self.root/'workflow-job.json')
        atomic_json(self.root/'operator-acceptance.json',{'plan_sha256':self.job_sha,'accepted_new_window_and_disk':True})
        atomic_json(self.root/'cached-preflight.json',{'fixture':True})
        self.state={'fingerprint':mod.FINGERPRINT,'limits':self.job['limits'],'mode':'real-pilot',
                    'transfer_bytes_consumed':mod.CHARGED,'prior_transfer_elapsed_seconds':mod.PRIOR_SECONDS,
                    'transfer_elapsed_seconds':mod.SNAPSHOT_SECONDS,'cumulative_transfer_elapsed_seconds':7241.245675802231,
                    'deadline_epoch':1793702652.9493718,'prior_deadline_epoch':self.binding['prior_deadline_epoch'],
                    'phases':{'preflight':{'status':'verified','receipt':'cached-preflight.json','receipt_sha256':mod.sha(self.root/'cached-preflight.json')},
                    'CTRL_R1':{'status':'verified','local_recovered_source':self.binding,'new_body_bytes':0,
                        'bytes':self.binding['bytes'],'md5':self.binding['md5'],'sha256':mod.pilot.READ_SHA},
                    'CTRL_R2':{'kind':'transfer','status':'started','reservation_start_body_bytes':281018368,
                               'unsettled_body_reservation_bytes':4194304}}}
        atomic_json(self.root/'ledger.json',self.state)
        (self.root/'workflow-receipts').mkdir()
        atomic_json(self.root/'workflow-receipts/run.json',{'status':'finished','exit_code':-9,
            'supervisor_error':'RuntimeError: Cumulative transfer time cap','live_group_members_after_cleanup':[]})
        atomic_json(self.root/'CTRL_R2.attempt-0.json',{'status':'started','attempt':0,'body_bytes':281018368,
            'accounting':'durable-block-reservation-v1','reservation_block_bytes':4194304})
        with (self.root/'CTRL_R2.attempt-0.partial').open('wb') as f:f.truncate(mod.PARTIAL_BYTES)
    def audit(self):
        with patch.object(mod,'JOB_SHA',self.job_sha),patch.object(mod.pilot,'validate_job',return_value=self.root),patch.object(mod.transport.base,'file_hash',return_value={'bytes':mod.PARTIAL_BYTES,'sha256':'a'*64}):
            return mod.inspect(self.root)
    def test_snapshot_and_reserved_block_survive_kill(self):
        obs=self.audit()
        self.assertGreater(obs['partial_bytes'],281018368)
        self.assertEqual(obs['charged_body_bytes']-5318543809-obs['partial_bytes'],412945)
        self.assertEqual(obs['prior_transfer_elapsed_seconds'],mod.PRIOR_SECONDS+1800)
        self.assertGreater(obs['prior_transfer_elapsed_seconds'],obs['last_snapshot_cumulative_seconds'])
    def test_changes_to_charge_reservation_clock_and_later_phase_refused(self):
        for key,value in [('transfer_bytes_consumed',0),('transfer_elapsed_seconds',1800),('prior_transfer_elapsed_seconds',0)]:
            state=copy.deepcopy(self.state);state[key]=value;atomic_json(self.root/'ledger.json',state)
            with self.subTest(key=key),self.assertRaises(ValueError):self.audit()
        state=copy.deepcopy(self.state);state['phases']['CTRL_compute']={'status':'started'};atomic_json(self.root/'ledger.json',state)
        self.assertRaises(ValueError,self.audit)
    def test_worker_group_not_empty_refused(self):
        p=self.root/'workflow-receipts/run.json';r=json.loads(p.read_text());r['live_group_members_after_cleanup']=[123];atomic_json(p,r)
        self.assertRaises(ValueError,self.audit)
    def test_partial_grew_refused(self):
        with (self.root/'CTRL_R2.attempt-0.partial').open('ab') as f:f.write(b'x')
        self.assertRaises(ValueError,self.audit)
    def test_receipt_cannot_refund_reserved_block(self):
        p=self.root/'CTRL_R2.attempt-0.json';r=json.loads(p.read_text());r['body_bytes']=mod.PARTIAL_BYTES;atomic_json(p,r)
        self.assertRaises(ValueError,self.audit)
    def test_preflight_metadata_tamper_refused(self):
        atomic_json(self.root/'cached-preflight.json',{'changed':True})
        self.assertRaises(ValueError,self.audit)
    def test_seven_lineage_roots_counted(self):
        dirs=[Path(self.tmp.name)/f'tree{i}' for i in range(7)]
        for d in dirs:d.mkdir();(d/'data').write_bytes(b'123')
        b={'index':dict(zip(('original_root','recovery_root','index_root'),map(str,dirs[:3]))),
           'original_root':str(dirs[3]),'root':str(dirs[4])}
        p={'original_root':str(dirs[5]),'root':str(dirs[6]),'original_audit':{'read_binding':b},
           'limits':{**mod.LIMITS,'disk_bytes':20,'reserve_bytes':0}}
        self.assertRaises(RuntimeError,mod.disk_guard,p)
    def test_external_deadline_stops_blocked_transfer(self):
        # Parent checks deadlines without relying on another body read.
        out=Path(self.tmp.name)/'parent';out.mkdir();now=mod.time.time()
        state={'limits':mod.LIMITS,'prior_transfer_elapsed_seconds':mod.CARRIED_SECONDS,
               'original_deadline_epoch':1793702652.9493718,'last_epoch':now-1,
               'deadline_epoch':now+100,'transfer_bytes_consumed':mod.CHARGED,
               'phases':{'range':{'status':'started','started_epoch':now-5401,'deadline_epoch':now-1}}}
        atomic_json(out/'recovery-state.json',state)
        p={'root':str(out),'limits':mod.LIMITS,'original_audit':{'prior_global_deadline_epoch':1793702652.9493718}}
        with patch.object(mod,'disk_guard'),self.assertRaisesRegex(RuntimeError,'phase deadline'):
            mod.monitor(p,mod.time.monotonic())()

if __name__=='__main__':unittest.main()
