"""Local SAM fixtures and supervised guards; no new human alignment/download."""
import copy
from collections import Counter
import importlib.util
import io
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import unc13a_locus_audit as audit
import unc13a_locus_pipeline as pipeline
import compact_pe_pipeline as original
from process_supervisor_v2 import atomic_json

REPO=Path(__file__).resolve().parents[1]
FIXTURE=REPO/'reports/unc13a-minigenome-20261102/fixtures/wild.sam'
TARGETS=[['mini',556,1844,'-'],['mini',556,1413,'-'],['mini',1541,1844,'-']]
HAS=importlib.util.find_spec('pysam') is not None

class GeometryAndGuardTests(unittest.TestCase):
    def test_cached_reference_geometry_exact_and_old_candidates_differ(self):
        g=audit.geometry();self.assertEqual([(r['start0'],r['end0']) for r in g['accepted']],[(17641556,17642844),(17641556,17642413),(17642541,17642844)])
        self.assertTrue(all(r['minus_gt_ag'] for r in g['accepted']));self.assertEqual({r['model'] for r in g['accepted']},{'exonic1'})
        self.assertEqual(pipeline.REGION,('chr19',17600000,17690000))
    def test_original_control_pin_rejects_changed_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);atomic_json(root/'workflow-job.json',{})
            self.assertRaisesRegex(ValueError,'metadata changed',audit.source_binding,root)
    def test_no_acceptance_does_not_read_plan(self):
        with patch.object(audit,'sha',side_effect=AssertionError('No plan read')):self.assertRaises(ValueError,audit.execute,'absent',None,False)
    def test_metadata_symlink_and_oversize_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'p';p.write_bytes(b'x'*(1024**2+1));self.assertRaises(ValueError,audit.small,p)
            p.unlink();p.symlink_to(Path(d)/'missing');self.assertRaises(ValueError,audit.small,p)
    def test_elapsed_guard_ignores_wall_clock_and_preserves_phase_order(self):
        with tempfile.TemporaryDirectory() as d:
            job={'root':d,'clock_policy':{'fixed':True}}
            with patch.object(audit.base.clock,'tick',return_value=100),patch.object(audit.base.clock,'clock_policy',return_value=job['clock_policy']),patch.object(audit,'disk_guard'),patch.object(audit.time,'time',return_value=-1000000):
                guard=audit.Guard(job);guard.phase('verify');guard();self.assertRaises(ValueError,guard.phase,'producer');guard.phase('stage')
                self.assertEqual(audit.small(Path(d)/'audit-state.json')['completed_phases'][0]['phase'],'verify')
            with patch.object(audit.base.clock,'tick',return_value=2200),patch.object(audit.base.clock,'clock_policy',return_value=job['clock_policy']):self.assertRaises(RuntimeError,guard)
    def test_phase_expiry_counter_and_forged_deadline_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            job={'root':d,'clock_policy':{}}
            with patch.object(audit.base.clock,'tick',return_value=100),patch.object(audit.base.clock,'clock_policy',return_value={}),patch.object(audit,'disk_guard'):
                g=audit.Guard(job);g.phase('verify');p=Path(d)/'audit-state.json';s=audit.small(p)
                for key,value in [('cumulative_body_bytes',0),('phase_deadline_tick',999999),('phase','other')]:
                    atomic_json(p,{**s,key:value});self.assertRaises(RuntimeError,g)
                atomic_json(p,s)
                with patch.object(audit.base.clock,'tick',return_value=400):self.assertRaises(RuntimeError,g)
    def test_actual_supervised_cli_rejects_invalid_source_without_alignment(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'audit-plan.json';atomic_json(p,{'source':{'root':str(Path(d)/'missing')}})
            rec=audit.supervise('run',[sys.executable,str(Path(audit.__file__).resolve()),'--worker',str(p)],Path(d)/'supervision',timeout=10,rss_limit=512*audit.GiB//1024,address_space=audit.GiB)
            self.assertNotEqual(rec['exit_code'],0);self.assertEqual(rec['live_group_members_after_cleanup'],[])
            self.assertFalse((Path(d)/'producer.log').exists())
    def test_overlap_is_halfopen_and_accepts_both_strands(self):
        self.assertTrue(pipeline.overlaps(('chr19',17600000,17600001,'+')))
        self.assertFalse(pipeline.overlaps(('chr19',17599900,17600000,'-')))
        self.assertFalse(pipeline.overlaps(('chr19',17690000,17690010,'-')))
    def test_junction_cap_fails_instead_of_truncating(self):
        with patch.object(pipeline,'MAX_JUNCTIONS',1):
            j=Counter({('chr19',17641556,17642844,'-'):1})
            self.assertRaisesRegex(ValueError,'inventory cap',pipeline.inventory_group,[],{('lib','chr19',17641556,17642413,'-'):1},{},'lib',j,Counter())

@unittest.skipUnless(HAS,'Pinned optional PySAM required; dedicated workflow installs it')
class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.limits={**pipeline.DEFAULT_LIMITS,'max_row_bytes':4096,'chunk_bytes':4096,'merge_fan_in':2}
    def run_pipeline(self,data=None,finish=lambda:0):
        with patch.object(pipeline,'REGION',('mini',0,2500)):
            return pipeline.run(io.BytesIO(data if data is not None else FIXTURE.read_bytes()),self.root/'audit','fixture',TARGETS,self.limits,finish)
    def test_same_four_routes_qc_counts_and_full_inventory_at_both_anchors(self):
        r=self.run_pipeline();old=original.run(io.BytesIO(FIXTURE.read_bytes()),self.root/'old','fixture',TARGETS,self.limits,lambda:0)
        self.assertEqual(r['routes'],old['routes']);self.assertEqual(r['records'],old['records'])
        for anchor,expected in [(15,2),(8,3)]:
            a=r['regional_audit']['routes']['text'+str(anchor)];self.assertEqual(a,r['regional_audit']['routes']['hts'+str(anchor)])
            self.assertEqual([x['fragments'] for x in a['junctions']],[expected]*3)
            self.assertTrue(all(x['near_original_targets'][0]['start_delta']==0 for x in a['junctions']))
        self.assertFalse((self.root/'audit/work').exists());self.assertFalse(any(self.root.rglob('*.sam')))
    def test_one_base_neighbor_is_inventoried_without_changing_original_target(self):
        shifted=copy.deepcopy(TARGETS);shifted[0][2]+=1
        with patch.object(pipeline,'REGION',('mini',0,2500)):
            r=pipeline.run(io.BytesIO(FIXTURE.read_bytes()),self.root/'audit','fixture',shifted,self.limits,lambda:0)
        self.assertEqual(r['routes']['text15']['counts'][0]['fragments'],0)
        rows=r['regional_audit']['routes']['text15']['junctions'];match=next(row for row in rows if row['event']==TARGETS[0])
        self.assertEqual(match['near_original_targets'][0]['end_delta'],-1)
    def test_regional_qc_counts_excluded_groups_not_accepted_support(self):
        data=FIXTURE.read_bytes().replace(b'NH:i:1',b'NH:i:2');r=self.run_pipeline(data)
        route=r['regional_audit']['routes']['text15'];self.assertEqual(route['junctions'],[])
        self.assertEqual(route['qc']['excluded:mapping_quality'],9)
    def test_outside_window_retains_original_targets_but_no_inventory(self):
        r=pipeline.run(io.BytesIO(FIXTURE.read_bytes()),self.root/'audit','fixture',TARGETS,self.limits,lambda:0)
        self.assertEqual(r['routes']['text15']['target_fragment_union'],6);self.assertEqual(r['regional_audit']['routes']['text15']['junctions'],[])
    def test_failed_producer_not_certified(self):
        with self.assertRaises(ValueError):self.run_pipeline(finish=lambda:1)
        self.assertEqual(audit.small(self.root/'audit/result.json')['status'],'failed')
    def test_inventory_result_cap_fails_closed(self):
        self.limits['max_result_bytes']=4096
        with self.assertRaisesRegex(ValueError,'Result byte cap'):self.run_pipeline()

@unittest.skipUnless(HAS,'Pinned optional PySAM required; dedicated workflow installs it')
class WorkerReplayTests(unittest.TestCase):
    def setUp(self):
        from test_offline_control_pilot import ControlTests
        self.helper=ControlTests();self.helper.setUp();self.addCleanup(self.helper.doCleanups)
        self.oldroot,self.rec=self.helper.miniature();self.oldseal=audit.base.accept_outer(self.helper.job,self.rec)
        self.raw_source_binding=audit.source_binding
        self.root=Path(str(self.oldroot)+'-locus-audit-01');self.root.mkdir()
        pair=audit.small(self.oldroot/'paired-fastq/CTRL_prefix/result.json')
        self.binding={'root':str(self.oldroot),'read_binding':self.helper.b,'prefixes':[{'path':str(self.oldroot/f'paired-fastq/CTRL_prefix/prefix-R{i}.fastq.gz'),**expected} for i,expected in enumerate(pair['prefixes'],1)],'spec':self.helper.job['manifest']['real_compute']['CTRL_compute']}
        self.job={'root':str(self.root),'source':self.binding,'clock_policy':audit.base.clock.clock_policy(),'geometry':audit.geometry()}
        for p in [patch.object(audit,'validate',return_value=self.root),patch.object(audit,'source_binding',return_value=self.binding),patch.object(audit,'disk_guard'),patch.object(audit.base.real,'validate_aligner'),patch.object(pipeline,'REGION',('mini',0,2500))]:p.start();self.addCleanup(p.stop)
        atomic_json(self.root/'audit-plan.json',self.job);atomic_json(self.root/'operator-acceptance.json',{'prepared_sha256':audit.sha(self.root/'audit-plan.json'),'accepted_local_audit_window':True})
        (self.root/'supervision').mkdir();atomic_json(self.root/'supervision/run.json',self.rec)
    def test_full_prior_metadata_chain_binds_prefixes_and_detects_tampering(self):
        pins={name:audit.sha(self.oldroot/name) for name in audit.PINNED}
        expected_geometry={'accepted':[{'chrom':t[0],'start0':t[1],'end0':t[2]} for t in TARGETS]}
        with patch.object(audit,'PINNED',pins),patch.object(audit,'PREFIX_PAIRS',self.helper.pairs),patch.object(audit,'geometry',return_value=expected_geometry):
            result=self.raw_source_binding(self.oldroot)
            self.assertEqual(result['prefixes'],self.binding['prefixes'])
            self.assertEqual(result['spec'],self.binding['spec'])
            p=self.oldroot/'paired-fastq/CTRL_prefix/result.json';r=audit.small(p);r['prefixes'][0]['sha256']='0'*64;atomic_json(p,r)
            self.assertRaises(ValueError,self.raw_source_binding,self.oldroot)
    def test_worker_uses_exact_old_prefix_replays_all_targets_and_seals_inventory(self):
        audit.worker(self.job);s=audit.seal(self.job,self.rec)
        self.assertEqual(s['status'],'sealed_exploratory_locus_audit');self.assertFalse(s['gate_promoted'])
        self.assertEqual(s['new_transfer_bytes'],0);self.assertTrue(s['same_prefix_target_and_qc_replay_identical'])
        self.assertEqual(len(s['regional_audit']['routes']['text15']['junctions']),3)
        self.assertFalse((self.root/'alignment-inputs/CTRL_compute').exists())
    def test_replay_changed_fails_without_audit_seal(self):
        p=self.oldroot/'compact/CTRL_compute/result.json';r=audit.small(p);r['routes']['text15']['counts'][0]['fragments']+=1;atomic_json(p,r)
        with self.assertRaisesRegex(ValueError,'replay differs'):audit.worker(self.job)
        self.assertFalse((self.root/'audit-seal.json').exists())
    def test_prefix_corruption_refused_before_alignment(self):
        Path(self.binding['prefixes'][0]['path']).write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'prefix changed'):audit.worker(self.job)
        self.assertFalse((self.root/'producer.log').exists())
    def test_sealer_rejects_nonzero_outer_after_worker_success(self):
        audit.worker(self.job);bad={**self.rec,'exit_code':1}
        self.assertRaises(ValueError,audit.seal,self.job,bad);self.assertFalse((self.root/'audit-seal.json').exists())
    def test_sealer_rejects_tampered_result(self):
        audit.worker(self.job);p=self.root/'compact/result.json';r=audit.small(p);r['regional_audit']['window'][1]+=1;atomic_json(p,r)
        self.assertRaises(ValueError,audit.seal,self.job,self.rec)

if __name__=='__main__':unittest.main()
