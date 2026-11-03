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
