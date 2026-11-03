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
import recover_ctrl_r2_clock as mod
from process_supervisor_v2 import atomic_json,supervise


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.original=self.root/'failed';self.original.mkdir();self.out=mod.recovery_root(self.original);self.out.mkdir()
        self.data=b'bounded paired FASTQ fixture\n'*100;self.start=73;partial=self.data[:self.start];(self.original/'recovered-CTRL_R2.partial').write_bytes(partial)
        self.obs={'root':str(self.original),'partial_bytes':self.start,'partial_sha256':hashlib.sha256(partial).hexdigest(),'charged_body_bytes':mod.CHARGED,'prior_transfer_elapsed_seconds':16300.072928190231,'prior_global_deadline_epoch':1793709745.7293887,'previous_transfer_elapsed_seconds':12700.072928190231,'interrupted_transfer_window_seconds_reserved':1800,'resume_audit':{},'prior_wsl_charged_bytes':6228707777,'manual_browser_reserved_body_bytes':mod.MANUAL_BROWSER_RESERVE,'manual_browser_exact_body_known':False}
        self.source={'url':'http://127.0.0.1/unused','bytes':len(self.data),'md5':hashlib.md5(self.data).hexdigest()}
        self.plan={'clock_policy':mod.clock_policy(),'root':str(self.out),'original_root':str(self.original),'original_audit':self.obs,'source':self.source,'range_start':self.start,'range_end':len(self.data)-1,'limits':mod.LIMITS}
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
        atomic_json(self.out/'recovery-plan.json',self.plan);atomic_json(self.out/'operator-acceptance.json',{'prepared_sha256':mod.sha(self.out/'recovery-plan.json'),'accepted_elapsed_clock_window':True})
        (self.out/'supervision').mkdir()
        record={'status':'finished','exit_code':0,'violation':None,'live_group_members_after_cleanup':[]};atomic_json(self.out/'supervision/run.json',record)
        with patch.object(mod.previous.previous,'SOURCE',self.source):seal=mod.accept_outer(self.out,self.plan,record)
        self.assertEqual(seal['status'],'sealed_verified_ctrl_r2_elapsed');self.assertFalse(seal['raw_execution_ready'])
    def test_complete_recovery_and_seal_despite_wall_clock_jumps(self):
        self.server()
        stamps=iter([1000.0,1001.0,999.0,10000000.0,2.0]+[5.0]*200)
        with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',return_value=self.obs):
            b=mod.Budget(self.plan,wall_clock=lambda:next(stamps));mod.recover(b)
        self.assertTrue(b.state.get('wall_clock_adjustments'))
        atomic_json(self.out/'recovery-plan.json',self.plan)
        atomic_json(self.out/'operator-acceptance.json',{'prepared_sha256':mod.sha(self.out/'recovery-plan.json'),'accepted_elapsed_clock_window':True})
        (self.out/'supervision').mkdir()
        rec={'status':'finished','exit_code':0,'violation':None,'live_group_members_after_cleanup':[]}
        atomic_json(self.out/'supervision/run.json',rec)
        seal=mod.accept_outer(self.out,self.plan,rec)
        self.assertEqual(seal['status'],'sealed_verified_ctrl_r2_elapsed')
        self.assertEqual((self.out/'CTRL_R2.fastq.gz').read_bytes(),self.data)
    def test_sealer_rejects_elapsed_deadline_even_with_matching_state_hash(self):
        self.server()
        with patch.object(mod,'disk_guard'),patch.object(mod,'inspect',return_value=self.obs):mod.recover(self.budget())
        atomic_json(self.out/'recovery-plan.json',self.plan)
        atomic_json(self.out/'operator-acceptance.json',{'prepared_sha256':mod.sha(self.out/'recovery-plan.json'),'accepted_elapsed_clock_window':True})
        (self.out/'supervision').mkdir();rec={'status':'finished','exit_code':0,'violation':None,'live_group_members_after_cleanup':[]}
        atomic_json(self.out/'supervision/run.json',rec)
        s=read_json(self.out/'recovery-state.json');s['phases']['range']['finished_tick']=s['phases']['range']['deadline_tick'];atomic_json(self.out/'recovery-state.json',s)
        r=read_json(self.out/'recovery-result.json');r['state_sha256']=mod.sha(self.out/'recovery-state.json');atomic_json(self.out/'recovery-result.json',r)
        self.assertRaisesRegex(ValueError,'phase elapsed',mod.accept_outer,self.out,self.plan,rec)
        self.assertFalse((self.out/'recovery-seal.json').exists())
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
            self.assertRaises(RuntimeError,b.guard);b.state['transfer_bytes_consumed']=mod.CHARGED;b.state['deadline_tick']=0
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
        with patch.object(mod,'disk_guard'):self.assertRaises(RuntimeError,mod.monitor(self.plan,mod.tick()))
    def test_partial_symlink_refused(self):
        p=self.original/'recovered-CTRL_R2.partial';p.unlink();p.symlink_to(self.root/'other')
        with self.assertRaises(ValueError):mod.transport.base.copy_prefix(p,self.out/'copy',{'bytes':self.start,'sha256':self.obs['partial_sha256']},lambda:None)


class ProposalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.original=Path(self.tmp.name)/'failed';self.original.mkdir()
        self.obs={'root':str(self.original),'partial_bytes':900998714,'partial_sha256':'a'*64,'charged_body_bytes':mod.CHARGED,'prior_transfer_elapsed_seconds':16300.072928190231,'prior_global_deadline_epoch':1793709745.7293887,'previous_transfer_elapsed_seconds':12700.072928190231,'interrupted_transfer_window_seconds_reserved':1800,'resume_audit':{},'prior_wsl_charged_bytes':6228707777,'manual_browser_reserved_body_bytes':mod.MANUAL_BROWSER_RESERVE,'manual_browser_exact_body_known':False}
    def plan(self):
        with patch.object(mod,'inspect',return_value=self.obs),patch.object(mod,'identity',return_value={}),patch.object(mod.previous.shutil,'disk_usage',return_value=type('D',(),{'free':100*mod.previous.GiB})()):return mod.prepare(self.original)
    def test_prepare_never_network_or_process(self):
        with patch.object(mod.transport.urllib.request,'build_opener',side_effect=AssertionError('No network')),patch.object(mod,'supervise',side_effect=AssertionError('No process')):p=self.plan()
        self.assertFalse(p['execution_enabled']);self.assertEqual(p['source']['bytes']-p['range_start'],96550743)
        self.assertEqual(p['original_audit']['charged_body_bytes']+96550743,7322807977)
    def test_fixed_plan_mutations_rejected(self):
        p=self.plan()
        with patch.object(mod,'identity',return_value={}):self.assertEqual(mod.validate_plan(p),mod.recovery_root(self.original))
        for key,value in [('execution_enabled',True),('range_start',0),('range_end',0),('root',str(self.original)),('scope','other'),('limits',{}),('source',{})]:
            q=copy.deepcopy(p);q[key]=value
            with self.subTest(key=key),patch.object(mod,'identity',return_value={}),self.assertRaises(ValueError):mod.validate_plan(q)
        for key in ('charged_body_bytes','prior_transfer_elapsed_seconds','manual_browser_reserved_body_bytes'):
            q=copy.deepcopy(p);q['original_audit'][key]=0
            with self.subTest(key=key),patch.object(mod,'identity',return_value={}),self.assertRaises(ValueError):mod.validate_plan(q)
    def test_existing_root_refused(self):
        mod.recovery_root(self.original).mkdir()
        with patch.object(mod,'inspect',side_effect=AssertionError('No audit')):self.assertRaises(ValueError,mod.prepare,self.original)
    def test_low_disk_refused(self):
        with patch.object(mod,'inspect',return_value=self.obs),patch.object(mod.previous.shutil,'disk_usage',return_value=type('D',(),{'free':1})()):self.assertRaises(ValueError,mod.prepare,self.original)
    def test_actual_supervised_worker_fails_before_http(self):
        p=self.plan();p['identity']=mod.identity();out=Path(p['root']);out.mkdir();atomic_json(out/'recovery-plan.json',p);atomic_json(out/'operator-acceptance.json',{'prepared_sha256':mod.sha(out/'recovery-plan.json'),'accepted_elapsed_clock_window':True})
        record=supervise('run',[sys.executable,str(Path(mod.__file__).resolve()),'--worker',str(out/'recovery-plan.json')],out/'supervision',timeout=10,rss_limit=mod.LIMITS['rss_bytes'],address_space=mod.LIMITS['address_space_bytes'])
        self.assertEqual(record['exit_code'],1);self.assertEqual(record['live_group_members_after_cleanup'],[]);self.assertFalse((out/'range-attempt.json').exists());self.assertFalse((out/'recovery-seal.json').exists())


class ElapsedClockTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.clocks={'tick':100.0,'wall':1000.0}
        self.plan={'root':str(self.root),'limits':mod.LIMITS,'clock_policy':mod.clock_policy(),
                   'original_audit':{'charged_body_bytes':mod.CHARGED,'prior_transfer_elapsed_seconds':16300.072928190231,
                                     'prior_global_deadline_epoch':1793709745.7293887}}
        self.b=mod.Budget(self.plan,elapsed_clock=lambda:self.clocks['tick'],wall_clock=lambda:self.clocks['wall'])
    def test_reproduces_old_guard_on_small_backward_civil_adjustment(self):
        old=mod.previous.Budget.__new__(mod.previous.Budget)
        old.clock=lambda:1001.0;old.state={'last_epoch':1002.0,'deadline_epoch':3400.0}
        self.assertRaisesRegex(RuntimeError,'clock/deadline',old.guard)
    def test_backward_and_large_forward_wall_adjustments_do_not_expire_elapsed_clock(self):
        with patch.object(mod,'disk_guard'):
            self.b.begin('range')
            for tick,wall in ((101.0,999.0),(102.0,9999999.0),(103.0,3.0)):
                self.clocks.update(tick=tick,wall=wall);self.b.guard();self.b.save()
            self.assertAlmostEqual(self.b.remaining(),1797.0)
            self.b.finish('range')
        self.assertEqual(self.b.state['phases']['range']['finished_tick'],103.0)
        self.assertEqual(len(self.b.state['wall_clock_adjustments']),3)
    def test_actual_phase_elapsed_expiry_remains_enforced(self):
        with patch.object(mod,'disk_guard'):
            self.b.begin('range');self.clocks.update(tick=1900.0,wall=1.0)
            self.assertRaisesRegex(RuntimeError,'phase deadline',self.b.guard)
    def test_actual_total_elapsed_expiry_remains_enforced(self):
        self.clocks.update(tick=2500.0,wall=1.0)
        self.assertRaisesRegex(RuntimeError,'Total elapsed',self.b.guard)
    def test_elapsed_clock_backwards_still_refused(self):
        self.clocks['tick']=99.0
        self.assertRaises(RuntimeError,self.b.guard)
    def test_parent_checks_blocked_worker_without_using_wall_time(self):
        with patch.object(mod,'disk_guard'):
            self.b.begin('range');self.b.save()
        state=read_json(self.root/'recovery-state.json');state['last_epoch']=99999999999;atomic_json(self.root/'recovery-state.json',state)
        with patch.object(mod,'disk_guard'):
            monitor=mod.monitor(self.plan,100.0,elapsed_clock=lambda:self.clocks['tick'])
            self.clocks['tick']=101.0;monitor()
            self.clocks['tick']=1900.0;self.assertRaisesRegex(RuntimeError,'phase deadline',monitor)
    def test_parent_samples_clock_after_reading_concurrent_worker_state(self):
        state=read_json(self.root/'recovery-state.json');state['last_tick']=101.0
        calls=iter((100.5,102.0))
        with patch.object(mod,'read',return_value=state),patch.object(mod,'disk_guard'):
            mod.monitor(self.plan,100.0,elapsed_clock=lambda:next(calls))()
    def test_boot_change_refused(self):
        with patch.object(mod,'clock_policy',return_value={'clock':'CLOCK_BOOTTIME','boot_id':'other'}),patch.object(mod,'disk_guard'):
            self.assertRaisesRegex(RuntimeError,'boot identity',mod.monitor(self.plan,100.0,elapsed_clock=lambda:101.0))
    def test_phase_cannot_restart_or_budget_reopen(self):
        with patch.object(mod,'disk_guard'):
            self.b.begin('copy');self.b.finish('copy');self.assertRaises(ValueError,self.b.begin,'copy')
        self.assertRaises(ValueError,mod.Budget,self.plan)
    def test_elapsed_clock_sealer_refuses_forged_deadline(self):
        s=self.b.state;s['deadline_tick']=99.0
        self.assertRaisesRegex(RuntimeError,'Total elapsed',mod.check_elapsed,s,100.0,self.plan['clock_policy'],mod.CHARGED)


def read_json(path):return json.loads(Path(path).read_text())


class ClockFailureAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'failed';self.root.mkdir()
        self.audit={'root':str(self.root/'previous'),'prior_transfer_elapsed_seconds':14500.072928190231,
                    'prior_global_deadline_epoch':1793707865.1037116}
        self.plan={'original_root':self.audit['root'],'original_audit':self.audit}
        atomic_json(self.root/'recovery-plan.json',self.plan);self.sha=mod.sha(self.root/'recovery-plan.json')
        atomic_json(self.root/'operator-acceptance.json',{'prepared_sha256':self.sha,'accepted_additional_time_window':True,'browser_stopped_and_manual_reserve_accepted':True})
        (self.root/'supervision').mkdir()
        self.outer={'status':'finished','exit_code':-9,'supervisor_error':'RuntimeError: External clock/body cap','live_group_members_after_cleanup':[]}
        atomic_json(self.root/'supervision/run.json',self.outer);(self.root/'supervision/run.log').write_text('')
        self.state={'status':'failed','error_type':'RuntimeError','limits':mod.LIMITS,'transfer_bytes_consumed':mod.CHARGED,
            'prior_transfer_elapsed_seconds':14500.072928190231,'original_deadline_epoch':1793707865.1037116,
            'deadline_epoch':1793709745.7293887,'phases':{'copy':{'status':'verified'},'range':{'status':'failed','error_type':'RuntimeError',
                'reservation_start_body_bytes':0,'unsettled_body_reservation_bytes':4194304}}}
        atomic_json(self.root/'recovery-state.json',self.state)
        self.attempt={'status':'failed','error_type':'RuntimeError','body_bytes':623663,'range_start':900375051,'range_end':997549456,
            'prior_charged_bytes':7222062930,'attempts':1,'address_family':'IPv4','accounting':'durable-block-reservation-v1','reservation_block_bytes':4194304}
        atomic_json(self.root/'range-attempt.json',self.attempt)
        with (self.root/'recovered-CTRL_R2.partial').open('wb') as f:f.truncate(mod.PARTIAL_BYTES)
    def call(self):
        with patch.object(mod.previous,'validate_plan',return_value=self.root),patch.object(mod.previous,'inspect',return_value=self.audit),patch.object(mod.transport.base,'file_hash',return_value={'bytes':mod.PARTIAL_BYTES,'sha256':'a'*64}):return mod.inspect(self.root)
    def test_chain_preserves_body_and_manual_reserve(self):
        obs=self.call();self.assertEqual(obs['charged_body_bytes'],7226257234)
        self.assertEqual(obs['manual_browser_reserved_body_bytes'],997549457)
        self.assertEqual(obs['prior_transfer_elapsed_seconds'],16300.072928190231)
    def test_wrong_stop_reason_or_live_group_refused(self):
        for key,value in [('supervisor_error','different'),('live_group_members_after_cleanup',[123])]:
            r=copy.deepcopy(self.outer);r[key]=value;atomic_json(self.root/'supervision/run.json',r)
            with self.subTest(key=key),self.assertRaises(ValueError):self.call()
        atomic_json(self.root/'supervision/run.json',self.outer)
    def test_refunded_charge_or_changed_partial_refused(self):
        self.state['transfer_bytes_consumed']=0;atomic_json(self.root/'recovery-state.json',self.state)
        self.assertRaises(ValueError,self.call)
    def test_eleven_lineage_roots_counted(self):
        dirs=[Path(self.tmp.name)/f'tree{i}' for i in range(11)]
        for d in dirs:d.mkdir();(d/'x').write_bytes(b'123')
        b={'index':dict(zip(('original_root','recovery_root','index_root'),map(str,dirs[:3]))),'original_root':str(dirs[3]),'root':str(dirs[4])}
        pilot={'root':str(dirs[5]),'read_binding':b};ipv4={'root':str(dirs[6]),'pilot_audit':pilot}
        final={'root':str(dirs[7]),'ipv4_audit':ipv4};resume={'root':str(dirs[8]),'previous_audit':final}
        plan={'original_root':str(dirs[9]),'root':str(dirs[10]),'original_audit':{'resume_audit':resume}}
        with patch.object(mod,'LIMITS',{**mod.LIMITS,'disk_bytes':32,'reserve_bytes':0}):
            self.assertRaises(RuntimeError,mod.disk_guard,plan)

if __name__=='__main__':unittest.main()
