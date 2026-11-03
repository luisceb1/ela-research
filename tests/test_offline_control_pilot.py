"""Local fixtures only. Adapter integration uses 9/36 miniature pairs and a
fixture-emitting producer, never HISAT2 or human reads. Production prefix is 1M.
"""
import copy
import gzip
import hashlib
import io
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'scripts'))
import offline_control_pilot as mod
from process_supervisor_v2 import atomic_json, supervise


def read_json(p):return json.loads(Path(p).read_text())


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);base=Path(self.tmp.name)
        prior=base/'prior';prior.mkdir();self.root=mod.clock.recovery_root(prior);self.root.mkdir()
        r1=base/'r1';r1.mkdir();self.b={'root':str(r1),'file':'CTRL_R1.fastq.gz','bytes':960856963,
            'md5':'ed58daa011d6508a3e8d1f05bc39fc29','sha256':mod.recovered.READ_SHA,'index':{'fixture':True}}
        for path,size in ((r1/'CTRL_R1.fastq.gz',960856963),(self.root/'CTRL_R2.fastq.gz',997549457)):
            with path.open('wb') as f:f.truncate(size)
        self.policy={'clock':'CLOCK_BOOTTIME','boot_id':'00000000-0000-0000-0000-000000000000','wall_time':'diagnostic only'}
        audit={'resume_audit':{'previous_audit':{'ipv4_audit':{'pilot_audit':{'read_binding':self.b}}}},
            'prior_transfer_elapsed_seconds':16300.072928190231,'prior_global_deadline_epoch':1793709745.7293887}
        p={'schema':'ctrl-r2-elapsed-clock-v1','execution_enabled':False,'root':str(self.root),'original_root':str(prior),
           'source':mod.clock.SOURCE,'limits':mod.clock.LIMITS,'identity':{},'scope':mod.clock.SCOPE,
           'range_start':mod.clock.PARTIAL_BYTES,'range_end':997549456,'clock_policy':self.policy,'original_audit':audit}
        atomic_json(self.root/'recovery-plan.json',p);self.sha=mod.sha(self.root/'recovery-plan.json')
        atomic_json(self.root/'operator-acceptance.json',{'prepared_sha256':self.sha,'accepted_elapsed_clock_window':True})
        state={'status':'verified','limits':mod.clock.LIMITS,'clock_policy':self.policy,'prior_transfer_elapsed_seconds':audit['prior_transfer_elapsed_seconds'],
            'original_deadline_epoch':audit['prior_global_deadline_epoch'],'transfer_bytes_consumed':mod.CHARGED,
            'started_tick':100,'last_tick':107,'deadline_tick':2500,
            'phases':{n:{'status':'verified','started_tick':101+2*i,'finished_tick':102+2*i,'deadline_tick':500+2*i} for i,n in enumerate(('copy','range','verify'))}}
        atomic_json(self.root/'recovery-state.json',state)
        atomic_json(self.root/'range-attempt.json',{'status':'tail_received_not_source_verified','address_family':'IPv4',
            'body_bytes':96550743,'charged_body_bytes':mod.CHARGED,'range_start':900998714,'range_end':997549456})
        atomic_json(self.root/'recovery-result.json',{'status':'verified_ctrl_r2_elapsed_pending_outer_seal','source_verified':True,
            'state_sha256':mod.sha(self.root/'recovery-state.json'),'file':'CTRL_R2.fastq.gz','bytes':997549457,
            'md5':mod.clock.SOURCE['md5'],'sha256':mod.R2_SHA,'clock_policy':self.policy,'cumulative_body_bytes':mod.CHARGED,
            'prior_transfer_elapsed_seconds':audit['prior_transfer_elapsed_seconds'],'additional_transfer_elapsed_seconds':1,'additional_body_bytes':96550743})
        (self.root/'supervision').mkdir();atomic_json(self.root/'supervision/run.json',{'status':'finished','exit_code':0,'violation':None,'live_group_members_after_cleanup':[]})
        self.seal()
    def seal(self):
        atomic_json(self.root/'recovery-seal.json',{'status':'sealed_verified_ctrl_r2_elapsed','sha256':{n:mod.sha(self.root/n) for n in mod.clock.SEALED},
            'clock_policy':self.policy,'file':'CTRL_R2.fastq.gz','file_bytes':997549457,'file_md5':mod.clock.SOURCE['md5'],
            'file_sha256':mod.R2_SHA,'cumulative_body_bytes':mod.CHARGED,'remaining_body_budget_bytes':12_000_000_000-mod.CHARGED,
            'manual_browser_reserved_body_bytes':mod.clock.MANUAL_BROWSER_RESERVE,'manual_browser_exact_body_known':False})
    def binding(self):
        with patch.object(mod,'R2_PLAN_SHA',self.sha),patch.object(mod.clock,'identity',return_value={}),patch.object(mod.recovered,'read_binding',return_value=self.b),patch.object(mod.clock,'roots_for',return_value=['/fixture/'+str(i) for i in range(11)]):return mod.read_binding(self.root)
    def test_historical_boot_validated_without_matching_current_boot_or_reading_bulk(self):
        with patch.object(mod.clock,'clock_policy',side_effect=AssertionError('No current boot check for historical seal')),patch.object(mod.clock.transport,'whole_hash',side_effect=AssertionError('No bulk read')):
            b=self.binding()
        self.assertEqual(b['files'][1]['sha256'],mod.R2_SHA);self.assertEqual(b['cumulative_body_bytes'],mod.CHARGED)
    def test_metadata_changed_after_seal_refused(self):
        atomic_json(self.root/'recovery-result.json',{'changed':True});self.assertRaises(ValueError,self.binding)
    def test_resealed_wrong_md5_or_charge_or_elapsed_refused(self):
        path=self.root/'recovery-result.json';before=path.read_bytes()
        for key,value in [('md5','0'*32),('cumulative_body_bytes',0),('additional_transfer_elapsed_seconds',2)]:
            r=json.loads(before);r[key]=value;atomic_json(path,r);self.seal()
            with self.subTest(key=key),self.assertRaises(ValueError):self.binding()
            path.write_bytes(before);self.seal()
    def test_metadata_chain_changed_or_oversized_refused(self):
        (self.root/'small.json').write_text('{}');v={'root':str(self.root),'metadata_sha256':{'small.json':mod.sha(self.root/'small.json')}}
        mod.metadata_chain(v);(self.root/'small.json').write_text('changed');self.assertRaises(ValueError,mod.metadata_chain,v)
    def test_original_symlink_refused(self):
        p=self.root/'CTRL_R2.fastq.gz';p.unlink();p.symlink_to(self.root/'missing');self.assertRaises(ValueError,self.binding)


@unittest.skipUnless(importlib.util.find_spec('pysam'), 'Pinned PySAM required')
class ControlTests(unittest.TestCase):
    def setUp(self):
        from test_cached_index_pilot import CachedPilotTests
        CachedPilotTests.setUp(self)
        self.index=self.binding
        self.source=self.root/'sealed-r2';self.source.mkdir();r1=self.root/'sealed-r1';r1.mkdir()
        fixture=REPO/'reports/unc13a-minigenome-20261102/fixtures'
        self.data=[(fixture/f'r{i}.fq').read_bytes() for i in (1,2)]
        self.sam=(fixture/'wild.sam').read_bytes();self.pairs=len(self.data[0].splitlines())//4
        self.files=[]
        for i,(base,data) in enumerate(zip((r1,self.source),self.data),1):
            p=base/f'CTRL_R{i}.fastq.gz';b=gzip.compress(data,mtime=0);p.write_bytes(b)
            self.files.append({'name':f'CTRL_R{i}','path':str(p),'bytes':len(b),'md5':hashlib.md5(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest()})
        roots=[self.root/f'history{i}' for i in range(11)]
        for r in roots:r.mkdir()
        self.b={'root':str(self.source),'seal_sha256':'e'*64,'files':self.files,'index':self.index,'lineage_roots':list(map(str,roots)),
            'cumulative_body_bytes':mod.CHARGED,'prior_transfer_elapsed_seconds':16400.0,
            'manual_browser_reserved_body_bytes':997549457,'manual_browser_exact_body_known':False}
        p=patch.object(mod,'read_binding',return_value=self.b);p.start();self.addCleanup(p.stop)
        with patch.object(mod.real,'check_host',return_value={}),patch.object(mod,'disk_guard'):self.job=mod.prepare(self.source)
    def runner(self):
        with patch.object(mod,'disk_guard'):r=mod.Runner(self.job)
        self.addCleanup(r.close);return r
    def mark_preflight(self,r):
        r.begin('preflight','process','fixture');r.state['phases']['preflight'].update(status='verified');r.save()
    def test_fixed_control_only_no_network_steps_and_original_prefix(self):
        m=self.job['manifest'];self.assertEqual([s['name'] for s in m['sealed_workflow']['steps']],[n for n,_ in mod.STEPS])
        self.assertEqual(m['sealed_workflow']['origins'],[])
        self.assertEqual(set(m['real_compute']),{'CTRL_compute'});self.assertEqual(set(m['paired_fastq']),{'CTRL_prefix'})
        self.assertEqual(m['paired_fastq']['CTRL_prefix']['prefix_pairs'],1_000_000)
        self.assertEqual(m['real_compute']['CTRL_compute']['minimum_fragment_union'],20)
        self.assertEqual(self.job['limits']['wall_seconds'],3000)
    def test_prepare_no_process_or_data_copy(self):
        with patch.object(mod,'supervise',side_effect=AssertionError('No process')),patch.object(mod,'adopt_read',side_effect=AssertionError('No copying')),patch.object(mod.real,'check_host',return_value={}),patch.object(mod,'disk_guard'):
            j=mod.prepare(self.source)
        self.assertFalse(j['execution_enabled']);self.assertFalse(Path(j['root']).exists())
    def test_mutations_samples_clock_limits_and_identity_refused(self):
        for key,value in [('execution_enabled',True),('scope','other'),('identity',{}),('clock_policy',{})]:
            j=copy.deepcopy(self.job);j[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):mod.validate_job(j)
        for mutate in ('prefix','threshold','TDP','origins'):
            j=copy.deepcopy(self.job);m=j['manifest']
            if mutate=='prefix':m['paired_fastq']['CTRL_prefix']['prefix_pairs']=2_000_000
            elif mutate=='threshold':m['real_compute']['CTRL_compute']['minimum_fragment_union']=1
            elif mutate=='TDP':m['sealed_workflow']['steps'].append({'name':'TDP_R1','kind':'http'})
            else:m['sealed_workflow']['origins']=['https://example.invalid']
            with self.subTest(mutate=mutate),self.assertRaises(ValueError):mod.validate_job(j)
    def test_local_copies_preserve_counter_and_provenance(self):
        r=self.runner()
        with patch.object(mod,'disk_guard'):
            self.mark_preflight(r);mod.adopt_read(r,'CTRL_R1');mod.adopt_read(r,'CTRL_R2')
        self.assertEqual(r.state['transfer_bytes_consumed'],mod.CHARGED);self.assertEqual(r.state['new_transfer_bytes'],0)
        for item in self.files:
            self.assertEqual((r.root/item['name']).read_bytes(),Path(item['path']).read_bytes())
            self.assertEqual(r.state['phases'][item['name']]['new_body_bytes'],0)
    def test_corrupt_local_read_refused_without_promotion(self):
        r=self.runner();Path(self.files[0]['path']).write_bytes(b'changed')
        with patch.object(mod,'disk_guard'):
            self.mark_preflight(r);self.assertRaises(ValueError,mod.adopt_read,r,'CTRL_R1')
        self.assertFalse((r.root/'CTRL_R1').exists())
    def test_no_reopen_or_out_of_order_phase(self):
        r=self.runner()
        with patch.object(mod,'disk_guard'):self.assertRaises(ValueError,r.begin,'CTRL_R2','transfer','bad')
        r.close();self.assertRaises(ValueError,mod.Runner,self.job)
    def test_body_counter_cannot_change_at_all(self):
        r=self.runner();r.state['transfer_bytes_consumed']+=1
        self.assertRaisesRegex(RuntimeError,'counter',r.guard)
    def test_wall_clock_changes_do_not_affect_limits_and_subphase_expiry_does(self):
        clocks={'tick':100.0,'wall':1000.0}
        with patch.object(mod,'disk_guard'):
            r=mod.Runner(self.job,elapsed_clock=lambda:clocks['tick'],wall_clock=lambda:clocks['wall']);self.addCleanup(r.close)
            self.mark_preflight(r);clocks.update(tick=101.0,wall=1.0);r.guard();r.save()
            self.assertTrue(r.state.get('wall_clock_adjustments'))
            r.state['phases']['preflight'].update(status='started',subdeadline_tick=102.0)
            clocks['tick']=102.0;self.assertRaisesRegex(RuntimeError,'subphase',r.guard)
    def test_phase_rss_parent_guard(self):
        r=self.runner()
        with patch.object(mod,'disk_guard'):r.begin('preflight','process','fixture')
        _,memory=mod.monitor(self.job,mod.clock.tick())
        self.assertRaisesRegex(RuntimeError,'RSS',memory,513*1024**2,[1],{})
    def test_deny_network_hook_in_real_subprocess(self):
        code="import sys,socket;sys.path.insert(0,'scripts');import offline_control_pilot as m;sys.addaudithook(m.deny_network);socket.create_connection(('127.0.0.1',1))"
        r=subprocess.run([sys.executable,'-c',code],cwd=REPO,text=True,capture_output=True,timeout=10)
        self.assertNotEqual(r.returncode,0);self.assertIn('cannot connect',r.stderr)
    def test_lineage_artifact_partition_includes_all_old_roots(self):
        r=self.runner();(Path(self.b['lineage_roots'][0])/'large').write_bytes(b'123')
        with patch.object(mod.execution,'disk_usage',return_value={**{k:0 for k in mod.execution.ALLOCATIONS},'artifacts':18*mod.GiB}):
            self.assertRaises(RuntimeError,mod.disk_guard,self.job,r.state)
    def test_missing_acceptance_before_read(self):
        with patch.object(mod,'sha',side_effect=AssertionError('No filesystem')):self.assertRaises(ValueError,mod.execute,'absent',None,False)
    def miniature(self,repeats=1):
        originals=self.data[:];sam=self.sam
        if repeats>1:
            data=[]
            for mate in originals:
                lines=mate.splitlines(keepends=True);chunks=[]
                for rep in range(repeats):
                    for i,line in enumerate(lines):chunks.append(b'@rep'+str(rep).encode()+b'_'+line[1:] if i%4==0 else line)
                data.append(b''.join(chunks))
            bodies=[l for l in sam.splitlines(keepends=True) if not l.startswith(b'@')]
            headers=[l for l in sam.splitlines(keepends=True) if l.startswith(b'@')]
            sam=b''.join(headers)+b''.join(b'rep'+str(rep).encode()+b'_'+line for rep in range(repeats) for line in bodies)
            for item,plain in zip(self.files,data):
                compressed=gzip.compress(plain,mtime=0);Path(item['path']).write_bytes(compressed)
                item.update(bytes=len(compressed),md5=hashlib.md5(compressed).hexdigest(),sha256=hashlib.sha256(compressed).hexdigest())
        pairs=self.pairs*repeats
        baseline,caps=mod.cached.make_manifest(self.index['aligner'],self.index)
        baseline=copy.deepcopy(baseline);baseline['paired_fastq']['CTRL_prefix']['prefix_pairs']=pairs
        for mate,item in zip(baseline['paired_fastq']['CTRL_prefix']['mates'],self.files):mate['expected']={k:item[k] for k in ('bytes','md5')}
        baseline['real_compute']['CTRL_compute']['targets']=[['mini',556,1844,'-'],['mini',556,1413,'-'],['mini',1541,1844,'-']]
        stack=[]
        def start(p):p.start();stack.append(p)
        start(patch.object(mod,'PREFIX_PAIRS',pairs));start(patch.object(mod.cached,'make_manifest',return_value=(baseline,caps)))
        start(patch.object(mod.real,'check_host',return_value={}))
        start(patch.object(mod.cached,'verify_index_data'))
        start(patch.object(mod.real,'version_probe',return_value={'sha256':self.index['aligner']['sha256'],'fixture':'not HISAT2'}))
        start(patch.object(mod.resource,'setrlimit'))
        self.addCleanup(lambda:[p.stop() for p in reversed(stack)])
        self.job=mod.prepare(self.source)
        outer=self
        class Producer:
            def __init__(self,argv,**kwargs):
                outer.assertEqual(argv[0],outer.index['aligner']['path']);self.stdout=io.BytesIO(sam)
            def wait(self,**kwargs):return 0
            def poll(self):return 0
        start(patch.object(mod.real.subprocess,'Popen',Producer))
        root=Path(self.job['root']);root.mkdir();atomic_json(root/'workflow-job.json',self.job)
        atomic_json(root/'operator-acceptance.json',{'prepared_sha256':mod.sha(root/'workflow-job.json'),'accepted_offline_control_window':True})
        mod.worker(self.job)
        (root/'workflow-receipts').mkdir();rec={'status':'finished','exit_code':0,'violation':None,'live_group_members_after_cleanup':[]}
        atomic_json(root/'workflow-receipts/run.json',rec)
        return root,rec
    def test_miniature_real_pair_validator_and_two_decoders_insufficient_seal(self):
        root,rec=self.miniature();seal=mod.accept_outer(self.job,rec)
        self.assertEqual(seal['technical_status'],'coverage_insufficient');self.assertEqual(seal['coverage']['fragment_union'],6)
        self.assertEqual(seal['new_transfer_bytes'],0);self.assertEqual(seal['pairs_scanned'],self.pairs)
        self.assertFalse((root/'alignment-inputs/CTRL_compute').exists());self.assertFalse(any(root.rglob('*.sam')))
    def test_miniature_adequate_control_still_has_no_tdp_or_http(self):
        root,rec=self.miniature(4);seal=mod.accept_outer(self.job,rec)
        self.assertEqual(seal['technical_status'],'coverage_adequate');self.assertEqual(seal['coverage']['fragment_union'],24)
        self.assertEqual(list(read_json(root/'ledger.json')['phases']),[n for n,_ in mod.STEPS])
    def test_parent_rejects_tampered_pair_receipt(self):
        root,rec=self.miniature();p=root/'paired-fastq/CTRL_prefix/result.json';r=read_json(p);r['pairs_scanned']+=1;atomic_json(p,r)
        self.assertRaises(ValueError,mod.accept_outer,self.job,rec)
    def test_projected_copies_refused_before_root_creation(self):
        with patch.object(mod,'history_bytes',return_value=18*mod.GiB),self.assertRaisesRegex(ValueError,'planned local copies'):
            mod.projected_disk_check(self.job)
        self.assertFalse(Path(self.job['root']).exists())
    def test_parent_rejects_failed_outer_even_after_inner_result(self):
        root,rec=self.miniature();bad={**rec,'exit_code':1};atomic_json(root/'workflow-receipts/run.json',bad)
        self.assertRaises(ValueError,mod.accept_outer,self.job,bad)
        self.assertFalse((root/'workflow-seal.json').exists())
    def test_parent_rejects_compute_receipt_provenance_changed(self):
        root,rec=self.miniature();p=root/'compact/CTRL_compute/receipt.json';r=read_json(p);r['binding']['argv'][0]='other';atomic_json(p,r)
        self.assertRaises(ValueError,mod.accept_outer,self.job,rec)
    def test_elapsed_producer_and_reduce_limits_preserved(self):
        r=self.runner()
        # Test the declared caps/transition while preserving the fixed phase order.
        times={'t':100.0};r.elapsed_clock=lambda:times['t'];r.observed_tick=100.0
        r.state.update(started_tick=100.0,last_tick=100.0,deadline_tick=3100.0)
        r.state['phases']={n:{'kind':k,'status':'verified','finished_tick':99.0} for n,k in mod.STEPS[:-1]}
        with patch.object(mod,'disk_guard'):
            r.begin('CTRL_compute','compact','fixture');self.assertEqual(r.state['phases']['CTRL_compute']['subdeadline_tick'],1000.0)
            times['t']=200.0;r.compact_reduction('CTRL_compute');self.assertEqual(r.state['phases']['CTRL_compute']['subdeadline_tick'],500.0)
            times['t']=500.0;self.assertRaisesRegex(RuntimeError,'subphase',r.guard)
    def test_actual_supervised_worker_rejects_missing_source_before_compute(self):
        root=self.root/'bad-worker';root.mkdir();job=copy.deepcopy(self.job);job['root']=str(root);job['manifest']['offline_control']['root']=str(root/'missing')
        atomic_json(root/'workflow-job.json',job)
        rec=supervise('run',[sys.executable,str(Path(mod.__file__).resolve()),'--worker',str(root/'workflow-job.json')],root/'workflow-receipts',timeout=10,rss_limit=512*1024**2,address_space=mod.GiB)
        self.assertEqual(rec['exit_code'],1);self.assertEqual(rec['live_group_members_after_cleanup'],[]);self.assertFalse((root/'ledger.json').exists())


if __name__=='__main__':unittest.main()
