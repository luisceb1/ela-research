import copy
import gzip
import hashlib
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import importlib.util
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import threading
import unittest
from unittest.mock import patch

REPO=Path(__file__).resolve().parents[1];SCRIPTS=REPO/'scripts';sys.path.insert(0,str(SCRIPTS))
try:
    import sealed_local_workflow as workflow
    from workflow_seal import assert_seal
    from compact_ledger_phase import decoder_identity
    from compact_pe_pipeline import DEFAULT_LIMITS
    from pilot_dry_runner import DryRunner
finally:sys.path.pop(0)


def expected(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}


@unittest.skipUnless(importlib.util.find_spec('pysam') is not None,'Pinned PySAM required for workflow')
class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'run'
        fixtures=REPO/'reports/unc13a-minigenome-20261102/fixtures'
        self.payloads={'r1':gzip.compress((fixtures/'r1.fq').read_bytes(),mtime=0),'r2':gzip.compress((fixtures/'r2.fq').read_bytes(),mtime=0),'sam':(fixtures/'wild.sam').read_bytes()}
        members=[];buffer=io.BytesIO()
        with tarfile.open(fileobj=buffer,mode='w',format=tarfile.USTAR_FORMAT) as tf:
            for i in range(1,9):
                name=f'toy/genome.{i}.ht2';data=f'SYNTHETIC PLACEHOLDER {i}\n'.encode();m=tarfile.TarInfo(name);m.size=len(data);tf.addfile(m,io.BytesIO(data));members.append({'name':name,**expected(data)})
        self.payloads['index']=gzip.compress(buffer.getvalue(),mtime=0);self.requests=[];outer=self
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_GET(self):
                outer.requests.append(self.path)
                if self.path=='/redirect':self.send_response(302);self.send_header('Location','/r1');self.end_headers();return
                data=outer.payloads[self.path.lstrip('/')];self.send_response(200);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        self.server=ThreadingHTTPServer(('127.0.0.1',0),Handler);self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start();self.addCleanup(self.shutdown)
        self.origin=f'http://127.0.0.1:{self.server.server_port}';MiB=1024**2
        self.limits={'wall_seconds':90,'transfer_bytes':MiB,'disk_bytes':8*MiB,'reserve_bytes':0,'threads':2,'process_caps':{'wall_seconds':90,'rss_bytes':384*MiB,'address_space_bytes':512*MiB}}
        def cap(kind,wall,**extra):return {'kind':kind,'wall_seconds':wall,'rss_bytes':384*MiB,'address_space_bytes':512*MiB,**extra}
        phases={n:cap('transfer',20) for n in self.payloads};phases.update(index_extract=cap('archive',10),prefix=cap('paired_fastq',10),calc=cap('compact',30,producer_seconds=20,reduce_seconds=10))
        policy={'schema':'pilot-b4-local-v1','production_enabled':False,'total_seconds':90,'transfer_seconds':20,'allocations':{'artifacts':2*MiB,'prefixes':MiB//2,'temporaries':2*MiB,'dependencies':MiB//2,'receipts':2*MiB},'phases':phases}
        steps=[{'kind':'http','name':n,'url':self.origin+'/'+n,'expected':expected(self.payloads[n])} for n in ('index','r1','r2','sam')]+[{'kind':'archive','name':'index_extract'},{'kind':'paired_fastq','name':'prefix'},{'kind':'stream_compute','name':'calc'}]
        self.manifest={'execution_policy':policy,'archives':{'index_extract':{'transfer':'index','identity':'synthetic-index-placeholder','expected':expected(self.payloads['index']),'members':members,'max_members':16,'max_expanded_bytes':4096,'max_tar_bytes':32768}},
                       'paired_fastq':{'prefix':{'mates':[{'transfer':n,'identity':'synthetic/'+n,'expected':{**expected(self.payloads[n]),'md5':hashlib.md5(self.payloads[n]).hexdigest()}} for n in ('r1','r2')],'prefix_pairs':9}},
                       'stream_compute':{'calc':{'scope':'synthetic-replay-only','paired_phase':'prefix','archive_phase':'index_extract','fixture_transfer':'sam','index_prefix':'toy/genome','library':'fixture','targets':[['mini',556,1844,'-'],['mini',556,1413,'-'],['mini',1541,1844,'-']],
                                                  'limits':{**DEFAULT_LIMITS,'max_temp_bytes':MiB,'max_result_bytes':65536,'chunk_bytes':4096,'max_row_bytes':4096},'decoder':decoder_identity(),'minimum_fragment_union':1,'behavior':'ok'}},
                       'sealed_workflow':{'schema':'b1-local-workflow-v1','mode':'synthetic-only','origins':[self.origin],'steps':steps,'producer':workflow.producer_identity()}}
    def shutdown(self):self.server.shutdown();self.server.server_close();self.thread.join()
    def run_job(self):return workflow.run_workflow(self.root,self.manifest,self.limits)
    def assert_unsealed(self):
        self.assertFalse((self.root/'workflow-seal.json').exists())
        if (self.root/'ledger.json').exists():self.assertRaises(ValueError,DryRunner,self.root,self.manifest,self.limits)
    def test_full_local_graph_seals_and_revalidates_without_transfer(self):
        seal=self.run_job();self.assertEqual(seal['technical_status'],'complete');before=(self.root/'ledger.json').read_bytes();result=workflow.verify_workflow(self.root)
        self.assertEqual(result['status'],'verified');self.assertEqual(before,(self.root/'ledger.json').read_bytes());self.assertEqual(len(self.requests),4)
        ledger=json.loads(before);self.assertEqual(len(ledger['phases']),7);self.assertEqual(ledger['phases']['calc']['coverage']['fragment_union'],6)
        self.assertFalse(any((self.root/'compact').rglob('*.sam')))
    def test_insufficient_coverage_is_sealed_as_blocked_not_success(self):
        self.manifest['stream_compute']['calc']['minimum_fragment_union']=20
        self.assertEqual(self.run_job()['technical_status'],'coverage_insufficient');self.assertEqual(len(self.requests),4)
    def test_parent_does_not_rehash_bulk_data(self):
        with patch.object(workflow,'file_digest',side_effect=AssertionError('Parent bulk hashing prohibited')):self.assertEqual(self.run_job()['status'],'sealed')
    def test_nonloopback_origin_or_mode_or_free_command_rejected_before_job(self):
        original=copy.deepcopy(self.manifest)
        for mode in ('origin','mode','argv'):
            self.manifest=copy.deepcopy(original)
            if mode=='origin':self.manifest['sealed_workflow']['origins']=['https://example.com']
            elif mode=='mode':self.manifest['sealed_workflow']['mode']='production'
            else:self.manifest['sealed_workflow']['steps'][-1]['argv']=['anything']
            self.assertRaises(ValueError,self.run_job);self.assertFalse((self.root/'workflow-job.json').exists())
    def test_redirect_rejected_without_seal(self):
        self.manifest['sealed_workflow']['steps'][0]['url']=self.origin+'/redirect';self.assertRaises(ValueError,self.run_job);self.assert_unsealed()
    def test_hash_mismatch_rejected_without_seal(self):
        self.manifest['sealed_workflow']['steps'][0]['expected']['sha256']='0'*64;self.assertRaises(ValueError,self.run_job);self.assert_unsealed()
    def test_producer_hash_rejected_before_network(self):
        self.manifest['sealed_workflow']['producer']['script_sha256']='0'*64;self.assertRaises(ValueError,self.run_job);self.assertEqual(self.requests,[]);self.assert_unsealed()
    def test_nonzero_producer_cannot_seal(self):
        self.manifest['stream_compute']['calc']['behavior']='exit7';self.assertRaises(ValueError,self.run_job);self.assert_unsealed()
        self.assertEqual(json.loads((self.root/'ledger.json').read_text())['phases']['calc']['status'],'failed')
    def test_prefix_identity_mismatch_cannot_seal(self):
        self.manifest['paired_fastq']['prefix']['prefix_pairs']=8;self.assertRaises(ValueError,self.run_job);self.assert_unsealed()
    def test_blocked_producer_is_killed_without_seal(self):
        self.manifest['stream_compute']['calc']['behavior']='stall';self.manifest['execution_policy']['phases']['calc'].update(producer_seconds=1,reduce_seconds=1,wall_seconds=4)
        self.assertRaises(RuntimeError,self.run_job);self.assert_unsealed()
        rec=json.loads((self.root/'workflow-receipts/run.json').read_text());self.assertEqual(rec['exit_code'],-9);self.assertEqual(rec['live_group_members_after_cleanup'],[])
    def test_phase_rss_is_enforced_below_global_rss_cap(self):
        self.manifest['execution_policy']['phases']['calc']['rss_bytes']=1024**2
        self.manifest['stream_compute']['calc']['behavior']='stall'
        self.assertRaises(RuntimeError,self.run_job);self.assert_unsealed()
        rec=json.loads((self.root/'workflow-receipts/run.json').read_text());self.assertIn('Workflow phase RSS cap',rec['supervisor_error']);self.assertEqual(rec['live_group_members_after_cleanup'],[])
    def test_external_failure_after_inner_complete_cannot_seal(self):
        actual=workflow.supervise
        def reject(*args,**kwargs):
            rec=actual(*args,**kwargs);injected={**rec,'exit_code':9,'synthetic_injection':'decision object only; real external receipt remains intact'}
            (self.root/'injected-decision.json').write_text(json.dumps(injected,indent=2)+'\n');return injected
        with patch.object(workflow,'supervise',side_effect=reject):self.assertRaises(ValueError,self.run_job)
        self.assertEqual(json.loads((self.root/'workflow-inner.json').read_text())['status'],'complete');self.assert_unsealed()
    def test_seal_missing_or_changed_external_metadata_blocks_open(self):
        self.run_job();seal=(self.root/'workflow-seal.json').read_bytes();(self.root/'workflow-seal.json').unlink();self.assertRaises(ValueError,DryRunner,self.root,self.manifest,self.limits)
        (self.root/'workflow-seal.json').write_bytes(seal);rec=self.root/'workflow-receipts/run.json';rec.write_text('{}');self.assertRaises(ValueError,DryRunner,self.root,self.manifest,self.limits)
    def test_bulk_output_tamper_is_detected_in_supervised_revalidation(self):
        self.run_job();(self.root/'paired-fastq/prefix/prefix-R1.fastq.gz').write_bytes(b'bad');self.assertRaises(ValueError,workflow.verify_workflow,self.root)
        self.assertEqual(len(self.requests),4)
    def test_descriptor_not_overwritten(self):
        self.run_job();before=(self.root/'workflow-job.json').read_bytes();self.assertRaises(FileExistsError,self.run_job);self.assertEqual(before,(self.root/'workflow-job.json').read_bytes())
    def test_fixed_real_argv_is_hash_pinned_plan_only(self):
        spec=copy.deepcopy(self.manifest['stream_compute']['calc']);spec['aligner']={'path':sys.executable,'sha256':hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),'version':'2.2.3'}
        plan=workflow.fixed_hisat2_plan(self.root,spec);self.assertFalse(plan['execution_enabled']);self.assertEqual(plan['argv'][0],sys.executable)
        self.assertIn('/dev/stdout',plan['argv']);self.assertNotIn('--rna-strandness',plan['argv']);self.assertNotIn('--tmo',plan['argv'])
        spec['aligner']['sha256']='0'*64;self.assertRaises(ValueError,workflow.fixed_hisat2_plan,self.root,spec)
        spec['aligner']['sha256']=hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest();spec['index_prefix']='../escape';self.assertRaises(ValueError,workflow.fixed_hisat2_plan,self.root,spec)
    def test_real_execution_rejected_before_any_binary_or_input_access(self):
        class Runner:
            manifest={'stream_compute':{'calc':{'scope':'fixed-hisat2-disabled'}}}
        self.assertRaises(ValueError,workflow.run_stream,Runner(),'calc');self.assertFalse(self.root.exists())


if __name__=='__main__':unittest.main()
