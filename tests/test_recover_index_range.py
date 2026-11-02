"""Only loopback synthetic data. No S3/human download or alignment."""
import copy
import hashlib
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import recover_index_range as recovery
from process_supervisor_v2 import atomic_json


class RangeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.base=Path(self.tmp.name)
        self.original=self.base/'original';self.original.mkdir();self.root=self.base/'recovery';self.root.mkdir()
        self.data=bytes(range(256))*1024;self.start=23456;self.prefix=self.data[:self.start]
        (self.original/'index_archive.attempt-0.partial').write_bytes(self.prefix)
        self.requests=[];self.mode='ok';outer=self
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*a):pass
            def do_GET(self):
                outer.requests.append({'path':self.path,'range':self.headers.get('Range')})
                if outer.mode=='redirect':self.send_response(302);self.send_header('Location','/other');self.end_headers();return
                status=200 if outer.mode=='full' else 206;tail=outer.data[outer.start:]
                if outer.mode=='corrupt':tail=bytes([tail[0]^1])+tail[1:]
                self.send_response(status)
                self.send_header('Content-Length',str(len(tail) if outer.mode!='length' else len(tail)+1))
                expected=f'bytes {outer.start}-{len(outer.data)-1}/{len(outer.data)}'
                self.send_header('Content-Range',expected if outer.mode!='range' else expected.replace(str(outer.start),str(outer.start+1),1))
                if outer.mode=='duplicate':self.send_header('Content-Range',expected)
                if outer.mode!='version':self.send_header('x-amz-version-id','toy-version')
                if outer.mode=='encoded':self.send_header('Content-Encoding','gzip')
                if outer.mode=='chunked':self.send_header('Transfer-Encoding','chunked')
                self.end_headers()
                try:self.wfile.write(tail if outer.mode!='truncated' else tail[:100])
                except (BrokenPipeError,ConnectionResetError):pass
        self.server=ThreadingHTTPServer(('127.0.0.1',0),Handler);self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start();self.addCleanup(self.shutdown)
        obs={'partial_bytes':self.start,'partial_sha256':hashlib.sha256(self.prefix).hexdigest(),'charged_body_bytes':self.start+16384,'prior_transfer_elapsed_seconds':3600.001265,'prior_global_deadline_epoch':1793658000.877632,'source_verified':False}
        self.plan={'original_root':str(self.original),'root':str(self.root),'original_audit':obs,'source':{'url':f'http://127.0.0.1:{self.server.server_port}/index?versionId=toy-version','version_id':'toy-version','bytes':len(self.data),'sha256':hashlib.sha256(self.data).hexdigest()},'range_start':self.start,'range_end':len(self.data)-1,'limits':{**recovery.LIMITS,'wall_seconds':60,'copy_seconds':10,'transfer_seconds':10,'verify_seconds':10,'transfer_bytes':len(self.data)+16384,'disk_bytes':32*1024**2,'reserve_bytes':0,'reservation_block_bytes':65536}}
    def shutdown(self):self.server.shutdown();self.server.server_close();self.thread.join()
    def run_recovery(self,audits=None):
        budget=recovery.Budget(self.plan)
        with patch.object(recovery.audit,'inspect',side_effect=audits or [self.plan['original_audit'],self.plan['original_audit']]):
            result=recovery.recover(budget)
        return budget,result
    def test_exact_range_full_hash_and_cumulative_charge_without_touching_original(self):
        before=(self.original/'index_archive.attempt-0.partial').read_bytes();budget,result=self.run_recovery()
        self.assertEqual((self.root/'hg38_genome.tar.gz').read_bytes(),self.data)
        self.assertEqual((self.original/'index_archive.attempt-0.partial').read_bytes(),before)
        self.assertEqual(len(self.requests),1);self.assertEqual(self.requests[0]['range'],f'bytes={self.start}-{len(self.data)-1}')
        self.assertEqual(result['cumulative_body_bytes'],len(self.data)+16384)
        self.assertEqual(result['additional_body_bytes'],len(self.data)-self.start)
        self.assertFalse((self.root/'recovery-seal.json').exists())
        self.assertEqual(budget.state['original_deadline_epoch'],self.plan['original_audit']['prior_global_deadline_epoch'])
    def assert_failed(self):
        self.assertFalse((self.root/'hg38_genome.tar.gz').exists());self.assertFalse((self.root/'recovery-seal.json').exists())
        self.assertEqual(json.loads((self.root/'recovery-state.json').read_text())['status'],'failed')
    def test_http200_never_appended_or_charged_as_tail(self):
        self.mode='full';self.assertRaises(ValueError,self.run_recovery);self.assert_failed()
        self.assertEqual((self.root/'recovered-index.partial').read_bytes(),self.prefix)
        self.assertEqual(recovery.read(self.root/'recovery-state.json')['transfer_bytes_consumed'],self.start+16384)
    def test_wrong_content_range_rejected(self):self.mode='range';self.assertRaises(ValueError,self.run_recovery);self.assert_failed()
    def test_duplicate_content_range_rejected(self):self.mode='duplicate';self.assertRaises(ValueError,self.run_recovery);self.assert_failed()
    def test_wrong_length_rejected(self):self.mode='length';self.assertRaises(ValueError,self.run_recovery);self.assert_failed()
    def test_missing_version_rejected(self):self.mode='version';self.assertRaises(ValueError,self.run_recovery);self.assert_failed()
    def test_encoded_or_chunked_response_rejected(self):
        self.mode='encoded';self.assertRaises(ValueError,self.run_recovery);self.assert_failed()
    def test_chunked_response_rejected(self):self.mode='chunked';self.assertRaises(ValueError,self.run_recovery);self.assert_failed()
    def test_redirect_refused_without_second_request(self):
        self.mode='redirect';self.assertRaises(ValueError,self.run_recovery);self.assertEqual(len(self.requests),1);self.assert_failed()
    def test_truncated_tail_never_promoted(self):self.mode='truncated';self.assertRaises(ValueError,self.run_recovery);self.assert_failed()
    def test_corrupted_tail_fails_whole_hash(self):self.mode='corrupt';self.assertRaises(ValueError,self.run_recovery);self.assert_failed()
    def test_changed_prefix_refused_before_http(self):
        (self.original/'index_archive.attempt-0.partial').write_bytes(b'z'*self.start)
        self.assertRaises(ValueError,self.run_recovery);self.assertEqual(self.requests,[]);self.assert_failed()
    def test_original_metadata_change_after_transfer_prevents_promotion(self):
        changed={**self.plan['original_audit'],'changed':True}
        self.assertRaises(ValueError,self.run_recovery,[self.plan['original_audit'],changed]);self.assert_failed()
    def test_failed_external_supervision_prevents_seal_after_inner_success(self):
        self.run_recovery()
        self.assertRaises(ValueError,recovery.accept_outer,self.root,self.plan,{'status':'finished','exit_code':7})
        self.assertFalse((self.root/'recovery-seal.json').exists())
    def test_successful_outer_decision_seals_metadata_only_after_clean_receipt(self):
        self.run_recovery();record={'status':'finished','exit_code':0,'violation':None,'supervisor_error':None,'live_group_members_after_cleanup':[]}
        (self.root/'supervision').mkdir();atomic_json(self.root/'supervision/run.json',record)
        atomic_json(self.root/'recovery-plan.json',self.plan)
        atomic_json(self.root/'operator-acceptance.json',{'prepared_sha256':recovery.meta_sha(self.root/'recovery-plan.json'),'accepted_additional_time_window':True})
        seal=recovery.accept_outer(self.root,self.plan,record)
        self.assertEqual(seal['status'],'sealed_verified_index_archive');self.assertEqual(seal['cumulative_body_bytes'],len(self.data)+16384)
    def test_no_reopening_attempted_recovery(self):
        recovery.Budget(self.plan);self.assertRaises(ValueError,recovery.Budget,self.plan)
    def test_copy_cap_and_symlink_and_hash(self):
        expected={'bytes':self.start,'sha256':hashlib.sha256(self.prefix).hexdigest()}
        source=self.original/'index_archive.attempt-0.partial';target=self.root/'copy'
        self.assertRaises(ValueError,recovery.copy_prefix,source,target,{**expected,'bytes':10},lambda:None)
        target.unlink();self.assertRaises(ValueError,recovery.copy_prefix,source,target,{**expected,'sha256':'0'*64},lambda:None)
        alias=self.root/'alias';alias.symlink_to(source)
        self.assertRaises(ValueError,recovery.copy_prefix,alias,self.root/'copy2',expected,lambda:None)
    def test_fixed_time_and_body_caps(self):
        clock=[100.0];budget=recovery.Budget(self.plan,clock=lambda:clock[0]);budget.begin('copy');clock[0]+=11
        self.assertRaises(RuntimeError,budget.guard)
        clock[0]=100.0;budget.state['transfer_bytes_consumed']=0;self.assertRaises(RuntimeError,budget.guard)
    def test_time_and_hash_acceptance_before_plan_access(self):
        absent=self.root/'absent'
        self.assertRaises(ValueError,recovery.execute,absent,None,False)
        self.assertRaises(ValueError,recovery.execute,absent,None,True)


class ProposalTests(unittest.TestCase):
    def setUp(self):
        from test_inspect_interrupted_pilot import InterruptedAuditTests
        self.fixture=InterruptedAuditTests();self.fixture.setUp();self.addCleanup(self.fixture.doCleanups)
    def test_prepare_disabled_and_strict_mutations_and_no_original_writes(self):
        fixture=self.fixture;before=fixture.snapshot();plan=recovery.prepare(fixture.root)
        self.assertEqual(before,fixture.snapshot());self.assertFalse(plan['execution_enabled'])
        recovery.validate_plan(plan)
        for field in ('range','source','time','bytes','root','identity'):
            p=copy.deepcopy(plan)
            if field=='range':p['range_start']+=1
            elif field=='source':p['source']['url']='https://example.com'
            elif field=='time':p['limits']['transfer_seconds']+=1
            elif field=='bytes':p['limits']['transfer_bytes']+=1
            elif field=='root':p['root']+='-second-attempt'
            else:p['identity']['python_sha256']='0'*64
            self.assertRaises(ValueError,recovery.validate_plan,p)
    def test_actual_supervised_worker_refuses_changed_prefix_before_http(self):
        import shutil
        fixture=self.fixture;plan=recovery.prepare(fixture.root);root=Path(plan['root'])
        self.addCleanup(lambda:shutil.rmtree(root,ignore_errors=True))
        prepared=fixture.root/'prepared.json';atomic_json(prepared,plan)
        (fixture.root/'index_archive.attempt-0.partial').write_bytes(b'z'*256)
        free=shutil.disk_usage(fixture.root)
        with patch.object(recovery.shutil,'disk_usage',return_value=type(free)(free.total,free.used,recovery.LIMITS['disk_bytes']+recovery.LIMITS['reserve_bytes']+1024)):
            self.assertRaises(ValueError,recovery.execute,prepared,recovery.meta_sha(prepared),True)
        state=recovery.read(root/'recovery-state.json');outer=recovery.read(root/'supervision/run.json')
        self.assertEqual(set(state['phases']),{'copy'});self.assertEqual(state['status'],'failed')
        self.assertEqual(state['transfer_bytes_consumed'],256);self.assertFalse((root/'range-attempt.json').exists())
        self.assertEqual(outer['exit_code'],1);self.assertEqual(outer['live_group_members_after_cleanup'],[])
        self.assertFalse((root/'recovery-seal.json').exists())
    def test_existing_lineage_root_refuses_new_plan(self):
        recovery.recovery_root(self.fixture.root).mkdir()
        self.addCleanup(recovery.recovery_root(self.fixture.root).rmdir)
        self.assertRaises(ValueError,recovery.prepare,self.fixture.root)


if __name__=='__main__':unittest.main()
