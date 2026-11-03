"""Synthetic adoption and routing tests; no external HTTP or human alignment."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import recovered_read_pilot as mod
from process_supervisor_v2 import atomic_json,supervise


@unittest.skipUnless(importlib.util.find_spec('pysam'),'Pinned PySAM required')
class PilotTests(unittest.TestCase):
    def setUp(self):
        from test_cached_index_pilot import CachedPilotTests
        CachedPilotTests.setUp(self)
        self.index=self.binding;self.failed=self.root/'failed-read';self.failed.mkdir();self.recovery=self.root/'recovered-read';self.recovery.mkdir()
        self.data=b'synthetic complete recovered gzip stand-in';(self.recovery/'CTRL_R1.fastq.gz').write_bytes(self.data)
        self.b={'root':str(self.recovery),'seal_sha256':'e'*64,'original_root':str(self.failed),'index':self.index,'file':'CTRL_R1.fastq.gz','bytes':len(self.data),'md5':hashlib.md5(self.data).hexdigest(),'sha256':hashlib.sha256(self.data).hexdigest(),'cumulative_body_bytes':mod.CHARGED,'prior_transfer_elapsed_seconds':4300.0,'prior_deadline_epoch':1793698176.656901}
        p=patch.object(mod,'read_binding',return_value=self.b);p.start();self.addCleanup(p.stop)
        with patch.object(mod.real,'check_host',return_value={}):self.job=mod.prepare(self.recovery)
    def runner(self):
        r=mod.Runner(self.job);self.addCleanup(r.close);return r
    def test_exact_three_http_mates_and_ctrl_before_tdp(self):
        steps=self.job['manifest']['sealed_workflow']['steps'];http=[s for s in steps if s['kind']=='http'];names=[s['name'] for s in steps]
        self.assertEqual([s['name'] for s in http],['CTRL_R2','TDP_R1','TDP_R2']);self.assertEqual(sum(s['expected']['bytes'] for s in http),5388846918)
        self.assertEqual(self.job['limits']['disk_bytes'],27*mod.GiB);self.assertEqual(self.job['manifest']['execution_policy']['allocations']['artifacts'],18*mod.GiB)
        self.assertLess(names.index('CTRL_compute'),names.index('TDP_R1'));self.assertEqual(5318543809+5388846918,10707390727)
    def test_prepare_no_process_or_http_and_no_root_creation(self):
        with patch.object(mod.real,'check_host',return_value={}),patch.object(mod,'supervise',side_effect=AssertionError('No process')),patch.object(mod,'transfer_read',side_effect=AssertionError('No HTTP')):job=mod.prepare(self.recovery)
        self.assertFalse(job['execution_enabled']);self.assertFalse(Path(job['root']).exists())
    def test_runner_preserves_charge_time_and_rejects_floor(self):
        r=self.runner();self.assertEqual(r.state['transfer_bytes_consumed'],mod.CHARGED);self.assertEqual(r.state['cumulative_transfer_elapsed_seconds'],4300)
        r.state['transfer_bytes_consumed']=0;self.assertRaises(RuntimeError,r.guard)
    def test_local_adoption_hash_no_http_no_new_body(self):
        r=self.runner()
        with patch.object(mod,'transfer_read',side_effect=AssertionError('No HTTP')):mod.adopt_read(r)
        self.assertEqual((r.root/'CTRL_R1').read_bytes(),self.data);self.assertEqual((self.recovery/'CTRL_R1.fastq.gz').read_bytes(),self.data);self.assertEqual(r.state['transfer_bytes_consumed'],mod.CHARGED)
        self.assertEqual(r.state['phases']['CTRL_R1']['new_body_bytes'],0)
    def test_corrupt_recovered_data_no_promotion(self):
        r=self.runner();(self.recovery/'CTRL_R1.fastq.gz').write_bytes(b'changed')
        self.assertRaises(ValueError,mod.adopt_read,r);self.assertFalse((r.root/'CTRL_R1').exists());self.assertEqual(r.state['phases']['CTRL_R1']['status'],'failed')
    def test_new_job_changes_and_reuse_rejected(self):
        mod.validate_job(self.job)
        for key,value in [('execution_enabled',True),('root',str(self.failed)),('identity',{}),('scope','changed')]:
            j=copy.deepcopy(self.job);j[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):mod.validate_job(j)
        for key,value in [('transfer_bytes',13000000000),('disk_bytes',28*mod.GiB)]:
            j=copy.deepcopy(self.job);j['limits'][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):mod.validate_job(j)
        r=self.runner();r.close();self.assertRaises(ValueError,mod.Runner,self.job)
    def test_no_acceptance_before_descriptor_access(self):
        with patch.object(mod,'sha',side_effect=AssertionError('No filesystem')):self.assertRaises(ValueError,mod.execute,'absent',None,False)
    def test_external_accounting_floor(self):
        r=self.runner();state=copy.deepcopy(r.state);state['transfer_bytes_consumed']=0;atomic_json(r.root/'ledger.json',state)
        with patch.object(mod.real,'local_monitor',return_value=(lambda:None,lambda:None)):guard,_=mod.monitor(self.job,mod.time.monotonic())
        self.assertRaises(RuntimeError,guard)
    def test_failed_lineage_is_charged_to_disk(self):
        r=self.runner();(self.failed/'partial').write_bytes(b'123')
        with patch.object(mod.cached,'lineage_usage',return_value=18*mod.GiB):self.assertRaises(RuntimeError,mod.combined_disk_guard,r.root,r.state,r.manifest,r.state['limits'])
    def test_actual_worker_routing_stops_before_tdp_and_parent_seals(self):
        calls=[]
        def mark(r,name,kind,**extra):
            r.begin(name,kind,'fixture');r.state['phases'][name].update(status='verified',**extra);r.save()
        def pre(r,name):mark(r,name,'process')
        def http(r,step):calls.append(step['name']);mark(r,step['name'],'transfer')
        def pair(r,name):mark(r,name,'paired_fastq')
        def compute(r,name):mark(r,name,'compact',coverage={'adequate':False})
        root=Path(self.job['root']);root.mkdir();atomic_json(root/'workflow-job.json',self.job);atomic_json(root/'operator-acceptance.json',{'plan_sha256':mod.sha(root/'workflow-job.json'),'accepted_new_window_and_disk':True})
        with patch.object(mod.cached,'run_preflight',side_effect=pre),patch.object(mod,'transfer_read',side_effect=http),patch.object(mod.Runner,'paired_fastq',new=pair),patch.object(mod.real,'run_stream',side_effect=compute),patch.object(mod.resource,'setrlimit'):
            mod.worker(self.job)
        self.assertEqual(calls,['CTRL_R2']);self.assertEqual(json.loads((root/'workflow-inner.json').read_text())['status'],'coverage_insufficient')
        (root/'workflow-receipts').mkdir();rec={'status':'finished','exit_code':0,'violation':None,'live_group_members_after_cleanup':[]};atomic_json(root/'workflow-receipts/run.json',rec)
        seal=mod.accept_outer(self.job,rec);self.assertEqual(seal['technical_status'],'coverage_insufficient');self.assertFalse(seal['raw_execution_ready'])
    def test_legacy_stream_binding_uses_same_cache_index_and_engine(self):
        r=self.runner();r.state['phases'].update(preflight={'status':'verified','kind':'process'},CTRL_prefix={'status':'verified','kind':'paired_fastq'})
        with patch.object(mod.cached,'verify_preflight'),patch.object(mod.cached,'verify_phase'),patch.object(mod.real,'validate_aligner'):
            value,_=mod.cached.stream_binding(r,'CTRL_compute')
        self.assertEqual(value['argv'][value['argv'].index('-x')+1],self.index['index_prefix']);self.assertEqual(value['policy'],'real-stream-v1')

    def fake_http(self,mode='ok'):
        import io,email.message
        data=b'synthetic compressed mate stand-in';step={'name':'CTRL_R2','kind':'http','url':'https://example.invalid/fixture','expected':{'bytes':len(data),'md5':hashlib.md5(data).hexdigest()}}
        class Response:
            status=206 if mode=='status' else 200
            headers=email.message.Message()
            def __init__(self):self.f=io.BytesIO(b'X'+data[1:] if mode=='corrupt' else data)
            def read1(self,n):
                if mode=='timeout':raise TimeoutError('fixture read timeout')
                return self.f.read1(n)
            def __enter__(self):return self
            def __exit__(self,*a):pass
        Response.headers['Content-Length']=str(len(data));return data,step,Response()
    def test_remaining_http_verified_and_charged_once(self):
        import urllib.request
        data,step,response=self.fake_http();r=self.runner()
        with patch.object(urllib.request,'build_opener') as op:
            op.return_value.open.return_value=response;mod.transfer_read(r,step)
            self.assertEqual(op.return_value.open.call_args.kwargs['timeout'],30)
        self.assertEqual((r.root/'CTRL_R2').read_bytes(),data);self.assertEqual(r.state['transfer_bytes_consumed'],mod.CHARGED+len(data));self.assertEqual(r.state['phases']['CTRL_R2']['attempts_used'],1)
    def test_remaining_http_bad_status_no_promotion(self):
        import urllib.request
        _,step,response=self.fake_http('status');r=self.runner()
        with patch.object(urllib.request,'build_opener') as op:
            op.return_value.open.return_value=response;self.assertRaises(ValueError,mod.transfer_read,r,step)
        self.assertFalse((r.root/'CTRL_R2').exists());self.assertEqual(r.state['transfer_bytes_consumed'],mod.CHARGED)
    def test_remaining_http_bad_md5_no_promotion(self):
        import urllib.request
        data,step,response=self.fake_http('corrupt');r=self.runner()
        with patch.object(urllib.request,'build_opener') as op:
            op.return_value.open.return_value=response;self.assertRaises(ValueError,mod.transfer_read,r,step)
        self.assertFalse((r.root/'CTRL_R2').exists());self.assertEqual(r.state['transfer_bytes_consumed'],mod.CHARGED+len(data))
    def test_remaining_http_timeout_keeps_reserved_charge(self):
        import urllib.request
        data,step,response=self.fake_http('timeout');r=self.runner()
        with patch.object(urllib.request,'build_opener') as op:
            op.return_value.open.return_value=response;self.assertRaises(TimeoutError,mod.transfer_read,r,step)
        self.assertFalse((r.root/'CTRL_R2').exists());self.assertEqual(r.state['transfer_bytes_consumed'],mod.CHARGED+len(data));self.assertEqual(r.state['phases']['CTRL_R2']['status'],'failed')


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'recovery';self.root.mkdir();self.original=Path(self.tmp.name)/'original';self.original.mkdir();self.index={'fixture':True,'index_root':'/synthetic/index'}
        self.obs={'prior_global_deadline_epoch':1793698176.656901,'prior_transfer_elapsed_seconds':4272.2037699222565,'metadata_sha256':{},'cached_index':self.index}
        self.plan={'root':str(self.root),'original_root':str(self.original),'original_audit':self.obs,'limits':{}}
        atomic_json(self.root/'recovery-plan.json',self.plan);self.plan_sha=mod.sha(self.root/'recovery-plan.json')
        atomic_json(self.root/'operator-acceptance.json',{'prepared_sha256':self.plan_sha,'accepted_additional_time_window':True})
        state={'status':'verified','limits':{},'original_deadline_epoch':self.obs['prior_global_deadline_epoch'],'prior_transfer_elapsed_seconds':self.obs['prior_transfer_elapsed_seconds'],'transfer_bytes_consumed':mod.CHARGED,'phases':{n:{'status':'verified','started_epoch':100,'finished_epoch':120} for n in ('copy','range','verify')}};atomic_json(self.root/'recovery-state.json',state)
        result={'status':'verified_ctrl_r1_pending_outer_seal','state_sha256':mod.sha(self.root/'recovery-state.json'),'source_verified':True,'file':'CTRL_R1.fastq.gz','bytes':mod.recovery.SOURCE['bytes'],'md5':mod.recovery.SOURCE['md5'],'sha256':mod.READ_SHA,'cumulative_body_bytes':mod.CHARGED,'additional_body_bytes':606225236,'additional_transfer_elapsed_seconds':20,'prior_transfer_elapsed_seconds':self.obs['prior_transfer_elapsed_seconds']};atomic_json(self.root/'recovery-result.json',result)
        atomic_json(self.root/'range-attempt.json',{'body_bytes':606225236,'charged_body_bytes':mod.CHARGED,'range_start':354631727,'range_end':960856962,'status':'tail_received_not_source_verified'})
        (self.root/'supervision').mkdir();atomic_json(self.root/'supervision/run.json',{'status':'finished','exit_code':0,'violation':None,'live_group_members_after_cleanup':[]});self.seal()
    def seal(self):atomic_json(self.root/'recovery-seal.json',{'status':'sealed_verified_ctrl_r1','sha256':{n:mod.sha(self.root/n) for n in mod.recovery.SEALED},'file':'CTRL_R1.fastq.gz','file_sha256':mod.READ_SHA,'file_md5':mod.recovery.SOURCE['md5'],'file_bytes':mod.recovery.SOURCE['bytes'],'cumulative_body_bytes':mod.CHARGED,'remaining_body_budget_bytes':12_000_000_000-mod.CHARGED})
    def binding(self):
        with patch.object(mod,'PLAN_SHA',self.plan_sha),patch.object(mod.recovery,'validate_plan',return_value=self.root),patch.object(mod.cached,'index_binding',return_value=self.index):return mod.read_binding(self.root)
    def test_positive_metadata_chain_without_bulk_data_read(self):
        self.assertFalse((self.root/'CTRL_R1.fastq.gz').exists());b=self.binding();self.assertEqual(b['cumulative_body_bytes'],mod.CHARGED);self.assertEqual(b['prior_transfer_elapsed_seconds'],4292.2037699222565)
    def test_changed_receipt_refused_without_bulk_access(self):
        atomic_json(self.root/'recovery-result.json',{'changed':True});self.assertRaises(ValueError,self.binding)
    def test_resealed_bad_result_or_charge_refused(self):
        p=self.root/'recovery-result.json';before=p.read_bytes()
        for key,value in [('cumulative_body_bytes',0),('md5','0'*32),('additional_transfer_elapsed_seconds',0),('sha256','0'*64)]:
            rec=json.loads(before);rec[key]=value;atomic_json(p,rec);self.seal()
            with self.subTest(key=key),self.assertRaises(ValueError):self.binding()
            p.write_bytes(before);self.seal()
    def test_missing_seal_refused(self):
        (self.root/'recovery-seal.json').unlink();self.assertRaises(FileNotFoundError,self.binding)
    def test_actual_supervised_worker_rejects_missing_metadata_before_http(self):
        out=Path(self.tmp.name)/'worker';out.mkdir();job={'schema':'recovered-read-pilot-v1','execution_enabled':False,'root':str(out),'manifest':{'recovered_read':{'root':str(out/'missing')}},'limits':{},'identity':{},'host_observed':{},'scope':mod.SCOPE,'unverified':[]};atomic_json(out/'workflow-job.json',job)
        rec=supervise('run',[sys.executable,str(Path(mod.__file__).resolve()),'--worker',str(out/'workflow-job.json')],out/'workflow-receipts',timeout=10,rss_limit=512*1024**2,address_space=1024**3)
        self.assertEqual(rec['exit_code'],1);self.assertEqual(rec['live_group_members_after_cleanup'],[]);self.assertFalse((out/'ledger.json').exists());self.assertFalse((out/'workflow-seal.json').exists())


if __name__=='__main__':unittest.main()
