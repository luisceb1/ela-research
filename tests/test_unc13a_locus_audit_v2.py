"""Timeout regression, worker guard I/O, immutable failure lineage and replay."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import unc13a_locus_audit_v2 as audit
import test_unc13a_locus_audit as first
from process_supervisor_v2 import atomic_json
HAS=importlib.util.find_spec('pysam') is not None

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.job={'root':str(self.root),'clock_policy':{'clock':'fixture'}};self.tick=100.
        for p in [patch.object(audit.base.clock,'tick',side_effect=lambda:self.tick),patch.object(audit.base.clock,'clock_policy',return_value=self.job['clock_policy']),patch.object(audit,'disk_guard')]:p.start();self.addCleanup(p.stop)
    def guard_at_reduce(self,local=True):
        g=audit.Guard(self.job,local_state=local)
        for phase in ('verify','stage','producer','reduce'):g.phase(phase)
        return g
    def test_reduction_survives_old_300s_cap_but_expires_at_720s(self):
        g=self.guard_at_reduce();self.tick=400.;g();self.tick=819.99;g();self.tick=820.
        with self.assertRaisesRegex(RuntimeError,'phase deadline') as c:g()
        self.assertIn('"phase": "reduce"',str(c.exception));self.assertIn('720.0',str(c.exception))
    def test_worker_hot_loop_does_not_read_metadata(self):
        g=self.guard_at_reduce()
        with patch.object(audit,'small',side_effect=AssertionError('No worker per-row metadata reads')),patch.object(audit.base.clock,'clock_policy',side_effect=AssertionError('Only sampled boot reads')):
            for _ in range(10000):g()
        self.tick=100.25
        with patch.object(audit.base.clock,'clock_policy',return_value=self.job['clock_policy']) as boot:g();self.assertEqual(boot.call_count,1)
    def test_parent_independently_reads_worker_state_and_catches_deadline(self):
        worker=self.guard_at_reduce();parent=audit.Guard(self.job,start=99)
        with patch.object(audit,'small',wraps=audit.small) as read:
            parent();parent();self.assertEqual(read.call_count,2)
        self.tick=820.
        with self.assertRaisesRegex(RuntimeError,'phase deadline'):parent()
    def test_parent_detects_forged_deadline_and_body_counter(self):
        self.guard_at_reduce();p=self.root/'audit-state.json';s=audit.small(p);parent=audit.Guard(self.job,start=99)
        for key,value in [('phase_deadline_tick',999999),('cumulative_body_bytes',0),('new_transfer_bytes',1)]:
            atomic_json(p,{**s,key:value});self.assertRaises(RuntimeError,parent)
    def test_wall_time_changes_do_not_change_deadlines(self):
        g=self.guard_at_reduce();self.tick=450.
        with patch.object(audit.time,'time',return_value=-1e20):g()
    def test_boot_and_clock_regression_and_total_expiry_still_rejected(self):
        g=self.guard_at_reduce();self.tick=101.
        with patch.object(audit.base.clock,'clock_policy',return_value={'changed':True}):self.assertRaisesRegex(RuntimeError,'boot identity',g)
        self.tick=99.;self.assertRaisesRegex(RuntimeError,'backwards',g)
        self.tick=2200.;self.assertRaisesRegex(RuntimeError,'total deadline',g)
    def test_fixed_phase_allocations_fit_same_total_window(self):
        self.assertEqual(audit.PHASES,{'verify':180,'stage':120,'producer':900,'reduce':720,'finalize':60})
        self.assertEqual(sum(audit.PHASES.values()),1980)
    def test_out_of_order_phase_refused(self):
        g=audit.Guard(self.job,local_state=True);g.phase('verify');self.assertRaises(ValueError,g.phase,'producer')

class FailureBindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.control={'root':str(Path(self.tmp.name)/'control')}
        self.root=audit.previous.output_root(self.control);self.root.mkdir()
        self.job={'root':str(self.root),'clock_policy':{'clock':'historical boot'},'fixed':'original descriptor'}
        self.state={'completed_phases':[
            {'phase':'verify','started_tick':7.,'finished_tick':27.,'deadline_tick':307.},
            {'phase':'stage','started_tick':27.,'finished_tick':33.,'deadline_tick':327.},
            {'phase':'producer','started_tick':33.,'finished_tick':576.,'deadline_tick':933.}],
            'clock_policy':self.job['clock_policy'],'started_tick':7.,'phase':'reduce','phase_started_tick':576.,'phase_deadline_tick':876.,'new_transfer_bytes':0,'cumulative_body_bytes':audit.base.CHARGED}
        self.record={'status':'finished','exit_code':-9,'live_group_members_after_cleanup':[],'supervisor_error':'RuntimeError: Audit phase elapsed cap','elapsed_seconds':869.893300581}
        atomic_json(self.root/'audit-plan.json',self.job);atomic_json(self.root/'audit-state.json',self.state)
        (self.root/'supervision').mkdir();atomic_json(self.root/'supervision/run.json',self.record)
        (self.root/'supervision/run.log').write_text('');(self.root/'producer.log').write_text('fixture complete alignment')
        atomic_json(self.root/'operator-acceptance.json',{'prepared_sha256':audit.sha(self.root/'audit-plan.json'),'accepted_local_audit_window':True})
        p=patch.object(audit.previous,'make_job',return_value={**self.job,'clock_policy':{'clock':'new boot'}});p.start();self.addCleanup(p.stop)
    def test_exact_failed_reduction_metadata_is_preserved_not_adopted(self):
        b=audit.failed_binding(self.control)
        self.assertEqual(b['prior_elapsed_seconds'],869.893300581);self.assertEqual(b['prior_phase_seconds']['reduce'],300)
        self.assertIn('no compact-run',b['disposition']);self.assertEqual(len(b['metadata_sha256']),6)
        (self.root/'compact').mkdir();(self.root/'compact/orphan').write_bytes(b'never opened')
        self.assertEqual(b,audit.failed_binding(self.control))
    def test_failed_metadata_pin_detects_later_change(self):
        b=audit.failed_binding(self.control);(self.root/'producer.log').write_text('changed')
        self.assertNotEqual(b,audit.failed_binding(self.control))
    def test_wrong_failure_live_group_or_success_refused(self):
        p=self.root/'supervision/run.json'
        for key,value in [('exit_code',0),('live_group_members_after_cleanup',[123]),('supervisor_error','other')]:
            atomic_json(p,{**self.record,key:value});self.assertRaises(ValueError,audit.failed_binding,self.control)
    def test_false_completed_phase_timing_or_counter_refused(self):
        p=self.root/'audit-state.json'
        for key,value in [('phase','producer'),('cumulative_body_bytes',0),('phase_deadline_tick',900)]:
            atomic_json(p,{**self.state,key:value});self.assertRaises(ValueError,audit.failed_binding,self.control)
    def test_no_adoption_of_inner_result_or_seal(self):
        for name in ('audit-inner.json','audit-seal.json'):
            p=self.root/name;atomic_json(p,{});self.assertRaises(ValueError,audit.failed_binding,self.control);p.unlink()
    def test_descriptor_or_acceptance_change_refused(self):
        p=self.root/'operator-acceptance.json';atomic_json(p,{'prepared_sha256':'0'*64,'accepted_local_audit_window':True})
        self.assertRaises(ValueError,audit.failed_binding,self.control)

class DiskPartitionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.base=Path(self.tmp.name)
        roots=[self.base/f'history{i}' for i in range(11)]
        for root in roots:root.mkdir()
        self.control=self.base/'control';self.control.mkdir();self.failed=self.base/'failed';self.failed.mkdir();self.current=self.base/'new'
        self.job={'root':str(self.current),'source':{'root':str(self.control),'read_binding':{'lineage_roots':list(map(str,roots))},'failed_audit':{'root':str(self.failed)}},'limits':{'disk_bytes':27*audit.GiB,'reserve_bytes':8*audit.GiB}}
        self.history=18*audit.GiB-1
        for p in [patch.object(audit.base,'history_bytes',side_effect=lambda b:self.history),patch.object(audit.base.real.shutil,'disk_usage',return_value=type('Usage',(),{'free':40*audit.GiB})())]:p.start();self.addCleanup(p.stop)
    def sparse(self,root,name,size):
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('wb') as f:f.truncate(size)
        return p
    def test_failed_temporaries_are_not_historical_artifacts_and_all_bytes_count(self):
        self.sparse(self.failed,'compact/work/old.jsonl',2*audit.GiB)
        self.sparse(self.current,'compact/work/new.jsonl',audit.GiB)
        self.sparse(self.failed,'alignment-inputs/CTRL_compute/R1.fastq',audit.GiB//4)
        self.sparse(self.current,'alignment-inputs/CTRL_compute/R1.fastq',audit.GiB//4)
        with patch.object(Path,'open',side_effect=AssertionError('No bulk reads or mutation while accounting')):
            usage=audit.disk_guard(self.job)
        self.assertEqual(usage,{'artifacts':self.history,'compact':3*audit.GiB,'plain':audit.GiB//2,'receipts':0})
        self.assertGreater(self.history+2*audit.GiB,18*audit.GiB)
        self.assertEqual(sum(usage.values()),self.history+3*audit.GiB+audit.GiB//2)
    def test_old_and_new_plaintext_share_same_2gib_cap(self):
        for root in (self.failed,self.current):self.sparse(root,'alignment-inputs/CTRL_compute/R1.fastq',audit.GiB+1)
        self.assertRaisesRegex(RuntimeError,'plain',audit.disk_guard,self.job)
    def test_old_and_new_compact_files_share_same_6gib_cap(self):
        self.sparse(self.failed,'compact/work/a',4*audit.GiB);self.sparse(self.current,'compact/work/b',3*audit.GiB)
        self.assertRaisesRegex(RuntimeError,'compact',audit.disk_guard,self.job)
    def test_old_and_new_receipts_share_same_quarter_gib_cap(self):
        for root in (self.failed,self.current):self.sparse(root,'producer.log',audit.GiB//8+1)
        self.assertRaisesRegex(RuntimeError,'receipts',audit.disk_guard,self.job)
    def test_original_artifact_and_total_caps_are_still_enforced(self):
        self.history=18*audit.GiB+1;self.assertRaisesRegex(RuntimeError,'artifacts',audit.disk_guard,self.job)
        self.history=18*audit.GiB-1;self.job['limits']['disk_bytes']=self.history-1
        self.assertRaisesRegex(RuntimeError,'total',audit.disk_guard,self.job)
    def test_reserve_is_not_relaxed(self):
        with patch.object(audit.base.real.shutil,'disk_usage',return_value=type('Usage',(),{'free':8*audit.GiB-1})()):
            self.assertRaisesRegex(RuntimeError,'reserve',audit.disk_guard,self.job)
    def test_fourteen_distinct_roots_required(self):
        self.job['source']['failed_audit']['root']=self.job['source']['root']
        self.assertRaisesRegex(ValueError,'Fourteen',audit.disk_guard,self.job)
    def test_symlink_in_failed_attempt_rejected(self):
        p=self.failed/'compact/work/link';p.parent.mkdir(parents=True);p.symlink_to(self.base/'absent')
        self.assertRaisesRegex(ValueError,'symlink',audit.disk_guard,self.job)


@unittest.skipUnless(HAS,'Pinned optional PySAM required; dedicated workflow installs it')
class WorkerReplayTests(unittest.TestCase):
    def setUp(self):
        p=patch.object(first,'audit',audit);p.start();self.addCleanup(p.stop)
        first.WorkerReplayTests.setUp(self)
        self.binding['failed_audit']={'root':str(self.oldroot)+'-locus-audit-01','disposition':'fixture failed metadata, no orphan adoption'}
        atomic_json(self.root/'audit-plan.json',self.job)
        atomic_json(self.root/'operator-acceptance.json',{'prepared_sha256':audit.sha(self.root/'audit-plan.json'),'accepted_local_audit_window':True})
    test_worker_replays_and_seals=first.WorkerReplayTests.test_worker_uses_exact_old_prefix_replays_all_targets_and_seals_inventory
    test_replay_changed_fails=first.WorkerReplayTests.test_replay_changed_fails_without_audit_seal
    test_corrupt_prefix_fails=first.WorkerReplayTests.test_prefix_corruption_refused_before_alignment
    test_nonzero_outer_fails=first.WorkerReplayTests.test_sealer_rejects_nonzero_outer_after_worker_success
    test_tampered_result_fails=first.WorkerReplayTests.test_sealer_rejects_tampered_result

if __name__=='__main__':unittest.main()
