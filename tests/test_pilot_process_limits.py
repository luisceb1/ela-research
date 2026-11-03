from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
scripts=Path(__file__).resolve().parents[1]/'scripts';sys.path.insert(0,str(scripts))
try:import pilot_dry_runner as runner
finally:sys.path.pop(0)

class ProcessLimitTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.caps={'wall_seconds':900,'rss_bytes':6*1024**3,'address_space_bytes':6*1024**3}
        limits={'wall_seconds':3600,'transfer_bytes':100,'disk_bytes':2*1024**2,'reserve_bytes':0,'process_caps':self.caps}
        self.r=runner.DryRunner(self.tmp.name,{'synthetic':True},limits);self.addCleanup(self.r.close)
    def test_real_plan_limits_configured_without_execution(self):
        with patch.object(runner,'supervise',side_effect=AssertionError('must not execute')):
            plan=self.r.plan_process(['not-executed'],self.caps)
        self.assertEqual(plan['process_limits'],self.caps);self.assertFalse(plan['execution_enabled']);self.assertFalse(plan['raw_execution_ready'])
    def test_production_has_no_default_fallback(self):self.assertRaises(ValueError,self.r.plan_process,['unused'])
    def test_production_execution_stays_disabled(self):self.assertRaises(ValueError,self.r.process,'blocked',['unused'],production=True,process_limits=self.caps)
    def test_invalid_limits(self):
        for policy in ({},{**self.caps,'wall_seconds':True},{**self.caps,'rss_bytes':0},{**self.caps,'wall_seconds':901},{**self.caps,'unknown':1}):
            with self.subTest(policy=policy),self.assertRaises(ValueError):self.r.plan_process(['unused'],policy)
    def test_caps_missing_fails_closed(self):
        del self.r.state['limits']['process_caps'];self.assertRaises(ValueError,self.r.plan_process,['unused'],self.caps)
    def test_limit_change_cannot_reuse_phase(self):
        policy={'wall_seconds':1,'rss_bytes':128*1024**2,'address_space_bytes':128*1024**2}
        self.r.process('local',[sys.executable,'-c','pass'],process_limits=policy)
        with self.assertRaises(RuntimeError):self.r.process('local',[sys.executable,'-c','pass'],process_limits={**policy,'wall_seconds':2})
    def test_explicit_synthetic_limits_recorded(self):
        policy={'wall_seconds':2,'rss_bytes':128*1024**2,'address_space_bytes':128*1024**2}
        r=self.r.process('local',[sys.executable,'-c','pass'],process_limits=policy)
        self.assertEqual(r['process_limits'],policy);self.assertEqual(r['status'],'verified')
    def test_global_deadline_clips_plan(self):
        self.r.clock=lambda:self.r.state['deadline_epoch']-3
        self.assertEqual(self.r.plan_process(['unused'],self.caps)['effective_wall_seconds'],3)
