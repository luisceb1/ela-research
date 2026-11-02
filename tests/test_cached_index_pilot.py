"""Cached-index contracts use synthetic metadata/stand-ins, no human data."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import cached_index_pilot as cached
from pilot_dry_runner import DryRunner
from process_supervisor_v2 import atomic_json


@unittest.skipUnless(importlib.util.find_spec('pysam'),'Pinned PySAM required')
class CachedPilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        binary=self.root/'hisat2-align-s';inspector=self.root/'hisat2-inspect-s'
        for p in (binary,inspector):shutil.copyfile(sys.executable,p);p.chmod(0o755)
        self.aligner={'path':str(binary),'sha256':cached.file_digest(binary)['sha256'],'inspect_path':str(inspector),'inspect_sha256':cached.file_digest(inspector)['sha256'],'version':'2.2.3','source_commit':'0d244324f98de541bce04d45c75e83bc3522f7f4'}
        for n in ('original','recovery','index'):(self.root/n).mkdir()
        self.binding={'schema':'sealed-extracted-index-v1','index_root':str(self.root/'index'),'index_prefix':str(self.root/'index/index/files/hg38/genome'),
            'index_seal_sha256':'1'*64,'recovery_root':str(self.root/'recovery'),'original_root':str(self.root/'original'),
            'cumulative_body_bytes':4355802733,'remaining_body_budget_bytes':7644197267,
            'prior_transfer_elapsed_seconds':3748.5157940387726,'prior_global_deadline_epoch':1793658000.877632,'aligner':self.aligner,'members':cached.offline.make_spec()['members']}
        self.binding_patch=patch.object(cached,'index_binding',return_value=self.binding);self.binding_patch.start();self.addCleanup(self.binding_patch.stop)
        self.manifest,self.limits=cached.make_manifest(self.aligner,self.binding)
    def test_only_four_fixed_fastq_transfers_and_no_index_phases(self):
        spec=cached.validate_manifest(self.manifest,self.limits)
        steps=spec['steps'];transfers=[s for s in steps if s['kind']=='http'];names=[s['name'] for s in steps]
        self.assertEqual(len(transfers),4);self.assertEqual(sum(s['expected']['bytes'] for s in transfers),6349703881)
        self.assertEqual(spec['origins'],['https://ftp.sra.ebi.ac.uk'])
        self.assertFalse(any(n in names for n in ('index_archive','index_extract','index_probe')))
        self.assertLess(names.index('CTRL_compute'),names.index('TDP_R1'))
        self.assertEqual(self.limits['wall_seconds'],7200);self.assertEqual(self.manifest['execution_policy']['transfer_seconds'],1800)
        for p in self.manifest['paired_fastq'].values():self.assertEqual(p['prefix_pairs'],1_000_000)
        for p in self.manifest['real_compute'].values():self.assertEqual(p['minimum_fragment_union'],20)
    def test_guards_reject_caps_origins_samples_baseline_and_code_changes(self):
        for mode in ('origin','cap','reads','baseline','code'):
            with self.subTest(mode=mode):
                m=copy.deepcopy(self.manifest);limits=copy.deepcopy(self.limits)
                if mode=='origin':m['sealed_workflow']['origins']=['https://example.com']
                elif mode=='cap':limits['transfer_bytes']+=1
                elif mode=='reads':m['paired_fastq']['CTRL_prefix']['prefix_pairs']=2_000_000
                elif mode=='baseline':m['cached_index']['cumulative_body_bytes']-=16384
                else:m['sealed_workflow']['producer']['python_sha256']='0'*64
                self.assertRaises(ValueError,cached.validate_manifest,m,limits)
    def test_runner_starts_with_prior_charge_and_spent_time(self):
        runner=DryRunner(self.root/'run',self.manifest,self.limits,real_pilot=True);self.addCleanup(runner.close)
        self.assertEqual(runner.state['transfer_bytes_consumed'],4355802733)
        self.assertEqual(runner.state['prior_transfer_elapsed_seconds'],self.binding['prior_transfer_elapsed_seconds'])
        self.assertEqual(runner.state['cumulative_transfer_elapsed_seconds'],self.binding['prior_transfer_elapsed_seconds'])
        self.assertEqual(runner.state['transfer_elapsed_seconds'],0)
    def test_prior_charge_cannot_be_refunded_or_reopened_without_seal(self):
        root=self.root/'run';runner=DryRunner(root,self.manifest,self.limits,real_pilot=True)
        runner.state['transfer_bytes_consumed']-=1;self.assertRaises(RuntimeError,runner.guard);runner.close()
        self.assertRaises(ValueError,DryRunner,root,self.manifest,self.limits,real_pilot=True)
    def test_synthetic_runner_cannot_opt_into_cache(self):
        self.assertRaises(ValueError,DryRunner,self.root/'run',self.manifest,self.limits)
        self.assertFalse((self.root/'run/ledger.json').exists())
    def test_combined_lineage_disk_is_charged_to_artifact_partition(self):
        runner=DryRunner(self.root/'run',self.manifest,self.limits,real_pilot=True);self.addCleanup(runner.close)
        with patch.object(cached,'lineage_usage',return_value=self.manifest['execution_policy']['allocations']['artifacts']+1):
            self.assertRaises(RuntimeError,cached.combined_disk_guard,runner.root,runner.state,self.manifest,self.limits)
    def test_child_disk_sampling_does_not_sample_clocks_or_budget_floor(self):
        runner=DryRunner(self.root/'run',self.manifest,self.limits,real_pilot=True);self.addCleanup(runner.close)
        runner.cached_last_disk_check=float('-inf')
        with patch.object(cached,'combined_disk_guard') as disk:
            for _ in range(10):runner.guard()
            self.assertEqual(disk.call_count,1)
            runner.state['transfer_bytes_consumed']=0;self.assertRaises(RuntimeError,runner.guard)
    def test_prepare_is_disabled_and_emits_no_commands_or_network(self):
        with patch.object(cached.real,'check_host',return_value={'scope':'synthetic host observation'}),patch.object(cached.real.subprocess,'Popen',side_effect=AssertionError('No execution in prepare')):
            job=cached.prepare(self.root/'index')
        self.assertFalse(job['execution_enabled']);self.assertEqual(job['root'],str(cached.output_root(self.binding)))
        cached.real.validate_job(job)
        self.assertFalse(Path(job['root']).exists())
    def test_new_time_window_acceptance_required_before_output_creation(self):
        plan=self.root/'plan.json';atomic_json(plan,{'manifest':{'cached_index':self.binding}})
        self.assertRaises(ValueError,cached.real.execute,plan,cached.meta_sha(plan))
        self.assertFalse(cached.output_root(self.binding).exists())
    def test_fixed_output_lineage_cannot_be_changed(self):
        with patch.object(cached.real,'check_host',return_value={}):job=cached.prepare(self.root/'index')
        job['root']+='-another-attempt';self.assertRaises(ValueError,cached.real.validate_job,job)
    def test_stream_requires_cached_preflight_before_touching_pairs(self):
        class Runner:pass
        runner=Runner();runner.manifest=self.manifest;runner.state={'phases':{}}
        self.assertRaises(ValueError,cached.stream_binding,runner,'CTRL_compute')
    def test_decoder_input_provenance_and_fixed_external_index_path(self):
        class Runner:
            def guard(self):pass
        runner=Runner();runner.root=self.root/'run';runner.manifest=self.manifest
        runner.state={'fingerprint':'fixture-only','phases':{'preflight':{'kind':'process','status':'verified'},'CTRL_prefix':{'kind':'paired_fastq','status':'verified'}}}
        with patch.object(cached,'verify_preflight') as pre,patch.object(cached,'verify_phase') as pair:
            binding,_=cached.stream_binding(runner,'CTRL_compute')
        self.assertEqual(binding['argv'][binding['argv'].index('-x')+1],self.binding['index_prefix'])
        pre.assert_called_once();pair.assert_called_once();self.assertNotIn('--rna-strandness',binding['argv'])
    def test_cache_data_rehash_rejects_member_change(self):
        with patch.object(cached.offline,'verify_members',side_effect=ValueError('changed member')):
            self.assertRaises(ValueError,cached.verify_index_data,self.binding,lambda:None)


class IndexMetadataTests(unittest.TestCase):
    def make_index_fixture(self):
        from test_prepare_verified_index import RecoveryBindingTests
        fixture=RecoveryBindingTests();fixture.setUp();self.addCleanup(fixture.doCleanups)
        root=fixture.base/'index-ready';root.mkdir()
        plan=cached.read(fixture.root/'recovery-plan.json');plan['original_audit']['prior_global_deadline_epoch']=1793658000.877632
        fixture.write('recovery-plan.json',plan)
        fixture.write('operator-acceptance.json',{'prepared_sha256':cached.meta_sha(fixture.root/'recovery-plan.json'),'accepted_additional_time_window':True})
        result=cached.read(fixture.root/'recovery-result.json')
        result.update(prior_transfer_elapsed_seconds=3600.0012652873993,additional_transfer_elapsed_seconds=148.5145287513733)
        fixture.write('recovery-result.json',result);fixture.reseal()
        recovered=cached.offline.recovery_binding(fixture.root)
        aligner={'path':str(fixture.binary),'sha256':cached.file_digest(fixture.binary)['sha256'],'inspect_path':str(fixture.inspector),'inspect_sha256':cached.file_digest(fixture.inspector)['sha256'],'version':'2.2.3','source_commit':'0d244324f98de541bce04d45c75e83bc3522f7f4'}
        job={'schema':'offline-verified-index-v1','root':str(root),'recovery':recovered,'aligner':aligner,'archive_spec':cached.offline.make_spec()}
        atomic_json(root/'index-job.json',job)
        state={'status':'verified','phases':{n:{'status':'verified'} for n in cached.offline.PHASES},'new_transfer_bytes':0,'cumulative_body_bytes':4355802733}
        atomic_json(root/'index-state.json',state)
        prefix=str(root/'index/files/hg38/genome')
        result={'status':'verified_index_pending_outer_seal','state_sha256':cached.meta_sha(root/'index-state.json'),'members':job['archive_spec']['members'],'index_prefix':prefix,'source_archive_sha256':recovered['expected']['sha256'],'new_transfer_bytes':0,'cumulative_body_bytes':4355802733,'remaining_body_budget_bytes':7644197267}
        atomic_json(root/'index-result.json',result)
        for name in ('preflight.json','index/extraction.json','index-summary.json','supervision/run.json'):
            path=root/name;path.parent.mkdir(parents=True,exist_ok=True)
            rec={'scope':'synthetic metadata fixture; no index data'} if name!='supervision/run.json' else {'status':'finished','exit_code':0,'violation':None,'supervisor_error':None,'live_group_members_after_cleanup':[]}
            atomic_json(path,rec)
        atomic_json(root/'index-seal.json',{'status':'sealed_verified_extracted_index','sha256':{n:cached.meta_sha(root/n) for n in cached.INDEX_FILES},'index_prefix':prefix,'member_count':9,'new_transfer_bytes':0,'cumulative_body_bytes':4355802733,'remaining_body_budget_bytes':7644197267})
        return root
    def test_positive_sealed_metadata_chain_without_bulk_hash_or_index_files(self):
        root=self.make_index_fixture()
        with patch.object(cached,'file_digest',side_effect=AssertionError('Parent must not hash index files')):
            binding=cached.index_binding(root)
        self.assertEqual(binding['cumulative_body_bytes'],4355802733)
        self.assertEqual(binding['prior_transfer_elapsed_seconds'],3600.0012652873993+148.5145287513733)
        (root/'index-summary.json').write_text('{}')
        self.assertRaises(ValueError,cached.index_binding,root)
    @unittest.skipUnless(importlib.util.find_spec('pysam'),'Pinned PySAM required')
    def test_actual_cached_worker_preserves_charge_and_rejects_before_http(self):
        root=self.make_index_fixture();free=shutil.disk_usage(root);enough=type(free)(free.total,free.used,40*cached.GiB)
        with patch.object(cached.real,'check_host',return_value={'scope':'synthetic parent host'}):job=cached.prepare(root)
        plan=root.parent/'cached-plan.json';atomic_json(plan,job)
        with patch.object(cached.real,'check_host',return_value={'scope':'synthetic parent host'}),patch.object(cached.shutil,'disk_usage',return_value=enough):
            self.assertRaises(ValueError,cached.real.execute,plan,cached.meta_sha(plan),accept_cached_window=True)
        out=Path(job['root']);ledger=cached.read(out/'ledger.json');outer=cached.read(out/'workflow-receipts/run.json')
        self.assertEqual(set(ledger['phases']),{'preflight'});self.assertEqual(ledger['transfer_bytes_consumed'],4355802733)
        self.assertEqual(ledger['phases']['preflight']['status'],'failed');self.assertFalse((out/'workflow-seal.json').exists())
        self.assertEqual(outer['exit_code'],1);self.assertEqual(outer['live_group_members_after_cleanup'],[])
    def test_missing_seal_rejected_before_any_bulk_read(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(cached,'file_digest',side_effect=AssertionError('No bulk read')):
                self.assertRaises(FileNotFoundError,cached.index_binding,d)


if __name__=='__main__':unittest.main()
