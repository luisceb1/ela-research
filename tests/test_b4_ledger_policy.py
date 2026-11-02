import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO=Path(__file__).resolve().parents[1];SCRIPTS=REPO/'scripts';sys.path.insert(0,str(SCRIPTS))
try:
    from pilot_dry_runner import DryRunner
    from compact_ledger_phase import decoder_identity
    import compact_pe_pipeline as pipeline
    from external_local_stage import run_local_stage
    from plan_b4_execution_policy import proposal
    import pilot_execution_policy as policy_module
finally:sys.path.pop(0)


def fixture_policy():
    MiB=1024**2
    limits={'wall_seconds':60,'transfer_bytes':MiB,'disk_bytes':8*MiB,'reserve_bytes':0,'process_caps':{'wall_seconds':60,'rss_bytes':256*MiB,'address_space_bytes':384*MiB}}
    def caps(kind,wall,**extra):return {'kind':kind,'wall_seconds':wall,'rss_bytes':256*MiB,'address_space_bytes':384*MiB,**extra}
    policy={'schema':'pilot-b4-local-v1','production_enabled':False,'total_seconds':60,'transfer_seconds':10,
            'allocations':{'artifacts':2*MiB,'prefixes':MiB//2,'temporaries':2*MiB,'dependencies':MiB//2,'receipts':2*MiB},
            'phases':{'source':caps('transfer',10),'second':caps('transfer',10),'calc':caps('compact',30,producer_seconds=20,reduce_seconds=10),'exec':caps('process',5)}}
    return {'execution_policy':policy},limits


def expected(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}


class Clock:
    def __init__(self):self.now=100
    def __call__(self):return self.now


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.manifest,self.limits=fixture_policy();self.clock=Clock();self.r=None;self.addCleanup(self.close)
    def close(self):
        if self.r:self.r.close();self.r=None
    def open(self):self.r=DryRunner(self.root,self.manifest,self.limits,clock=self.clock);return self.r
    def test_total_deadline_and_finished_transfer_clock_survive_resume(self):
        r=self.open()
        def chunks():self.clock.now+=3;yield b'abc'
        r.transfer('source',chunks(),expected(b'abc'));before=copy.deepcopy(r.state);self.close();self.clock.now+=20
        b=self.open();self.assertEqual(b.state,before);self.assertEqual(b.state['transfer_elapsed_seconds'],3)
    def test_phase_deadline_stops_and_records_failed(self):
        self.manifest['execution_policy']['phases']['source']['wall_seconds']=2;r=self.open()
        def chunks():self.clock.now+=3;yield b'abc'
        self.assertRaises(RuntimeError,r.transfer,'source',chunks(),expected(b'abc'));self.assertEqual(r.state['phases']['source']['status'],'failed')
    def test_cumulative_transfer_time_does_not_reset_per_phase(self):
        r=self.open()
        def first():self.clock.now+=6;yield b'a'
        r.transfer('source',first(),expected(b'a'))
        def second():self.clock.now+=5;yield b'b'
        self.assertRaises(RuntimeError,r.transfer,'second',second(),expected(b'b'));self.assertEqual(r.state['transfer_elapsed_seconds'],11)
    def test_backward_clock_rejected_on_reopen(self):
        r=self.open();self.clock.now+=5;r.guard();self.clock.now-=1;self.assertRaises(RuntimeError,r.guard)
        self.close();self.clock.now=99;self.assertRaises(RuntimeError,self.open)
    def test_unknown_or_wrong_kind_and_overlapping_phase_rejected(self):
        r=self.open();self.assertRaises(ValueError,r.begin,'unknown','transfer','sig')
        self.assertRaises(ValueError,r.begin,'source','compact','sig');r.begin('source','transfer','sig')
        self.assertRaises(RuntimeError,r.begin,'second','transfer','sig')
    def test_invalid_clock_memory_and_disk_policies_rejected(self):
        original=copy.deepcopy(self.manifest)
        for change in ('total','disk','memory','subphase','envelope','production'):
            self.manifest=copy.deepcopy(original);p=self.manifest['execution_policy']
            if change=='total':p['total_seconds']=61
            elif change=='disk':p['allocations']['artifacts']=self.limits['disk_bytes']
            elif change=='memory':p['phases']['calc']['address_space_bytes']=1
            elif change=='subphase':p['phases']['calc']['reduce_seconds']=20
            elif change=='envelope':p['phases']['calc']['wall_seconds']=60
            else:p['production_enabled']=True
            with self.subTest(change=change):self.assertRaises(ValueError,self.open)
    def test_partition_fill_rejected(self):
        r=self.open();d=self.root/'dependencies';d.mkdir();(d/'oversized').write_bytes(b'x'*(self.manifest['execution_policy']['allocations']['dependencies']+1));self.assertRaises(RuntimeError,r.guard)
    def test_producer_and_reduce_subclocks(self):
        r=self.open();r.begin('calc','compact','sig');self.clock.now+=4;r.compact_reduction('calc');p=r.state['phases']['calc'];self.assertEqual(p['substage'],'reduce');self.clock.now+=10;self.assertRaises(RuntimeError,r.guard)
    def test_expired_pending_commit_cannot_be_verified(self):
        r=self.open();r.begin('source','transfer','sig');r.state['phases']['source']['status']='verified';self.clock.now+=11
        self.assertRaises(RuntimeError,r.save);self.assertEqual(r.state['phases']['source']['status'],'failed')
    def test_proposal_envelope_and_allocations(self):
        p=proposal();self.assertEqual(p['clock_envelope_seconds'],8520);self.assertLess(p['disk_allocated_bytes'],p['limits']['disk_bytes']);self.assertFalse(p['execution_enabled'])
    def test_changed_policy_cannot_reopen(self):
        self.open();self.close();self.manifest['execution_policy']['phases']['source']['wall_seconds']=9;self.assertRaises(ValueError,self.open)
    def test_exact_finished_transfer_budget_allows_nontransfer_inspection(self):
        state={'last_epoch':100,'phases':{'x':{'kind':'transfer','status':'verified','started_epoch':90,'finished_epoch':100,'deadline_epoch':200}}}
        policy_module.guard_clocks(state,{'transfer_seconds':10},101)


@unittest.skipUnless(importlib.util.find_spec('pysam') is not None,'Pinned optional PySAM required')
class CompactLedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.manifest,self.limits=fixture_policy();self.r=None;self.addCleanup(self.close)
        self.data=(REPO/'reports/unc13a-minigenome-20261102/fixtures/wild.sam').read_bytes()
        self.manifest['compact']={'calc':{'source_scope':'existing-synthetic-sam-only','transfer':'source','library':'fixture','targets':[['mini',556,1844,'-'],['mini',556,1413,'-'],['mini',1541,1844,'-']],
                                         'limits':{**pipeline.DEFAULT_LIMITS,'max_temp_bytes':1024**2,'max_result_bytes':65536,'chunk_bytes':4096,'max_row_bytes':4096},'decoder':decoder_identity(),'minimum_fragment_union':20}}
    def close(self):
        if self.r:self.r.close();self.r=None
    def ready(self):
        self.r=DryRunner(self.root,self.manifest,self.limits);self.r.transfer('source',[self.data],expected(self.data));return self.r
    def verified(self):r=self.ready();r.compact('calc');return r
    def test_success_reuse_preserves_state_and_insufficient_coverage_stops_next_phase(self):
        r=self.verified();before=copy.deepcopy(r.state);self.assertEqual(r.state['phases']['calc']['coverage']['fragment_union'],6)
        self.assertFalse(r.state['phases']['calc']['coverage']['adequate']);self.close();self.r=DryRunner(self.root,self.manifest,self.limits);self.r.compact('calc');self.assertEqual(before,self.r.state)
        self.assertRaises(RuntimeError,self.r.transfer,'second',[b'x'],expected(b'x'))
    def test_coverage_union_counts_group_once_for_two_targets(self):
        from test_pe_fragment_contract import pair
        self.data=('@SQ\tSN:chr19\tLN:100000\n'+'\n'.join(pair(cigars=('20M100N20M','25M100N15M')))+'\n').encode()
        self.manifest['compact']['calc']['targets']=[['chr19',120,220,'+'],['chr19',125,225,'+']]
        r=self.verified();c=r.state['phases']['calc']['coverage'];self.assertEqual((c['fragment_union'],c['event_support_sum']),(1,2))
    def test_result_receipt_source_and_coverage_tamper_rejected(self):
        original_root=self.root
        for mode in ('result','receipt','source','coverage'):
            with tempfile.TemporaryDirectory() as sub:
                self.root=Path(sub);r=self.verified()
                if mode=='source':(self.root/'source').write_bytes(b'bad')
                elif mode=='coverage':r.state['phases']['calc']['coverage']['adequate']=True;r.save()
                else:(self.root/'compact/calc'/('result.json' if mode=='result' else 'receipt.json')).write_text('{}')
                self.close();self.assertRaises((ValueError,KeyError),DryRunner,self.root,self.manifest,self.limits)
        self.root=original_root
    def test_wrong_decoder_or_temp_caps_rejected_before_phase(self):
        for mode in ('decoder','temp'):
            with tempfile.TemporaryDirectory() as sub:
                self.root=Path(sub)
                if mode=='decoder':self.manifest['compact']['calc']['decoder']['pysam_version']='wrong'
                else:self.manifest['compact']['calc']['decoder']=decoder_identity();self.manifest['compact']['calc']['limits']['max_temp_bytes']=4*1024**2
                r=self.ready();self.assertRaises(ValueError,r.compact,'calc');self.assertNotIn('calc',r.state['phases']);self.close()
    def test_failed_pipeline_blocks_reopen_even_if_output_directory_exists(self):
        r=self.ready()
        with patch.object(pipeline,'run',side_effect=KeyboardInterrupt):self.assertRaises(KeyboardInterrupt,r.compact,'calc')
        self.close();self.assertRaises(ValueError,DryRunner,self.root,self.manifest,self.limits)
    def test_http_source_receipt_changes_block_reuse(self):
        r=self.ready();p=r.state['phases']['source'];p['attempts_used']=1
        path=self.root/'source.attempt-0.json';rec={'status':'verified','body_bytes':p['bytes'],'md5':p['md5'],'sha256':p['sha256']};path.write_text(json.dumps(rec));r.save();r.compact('calc')
        rec['status']='started';path.write_text(json.dumps(rec));self.close();self.assertRaises(ValueError,DryRunner,self.root,self.manifest,self.limits)
    def test_supervised_local_worker_records_policy_resources(self):
        self.ready();self.close();rec=run_local_stage(self.root,self.manifest,self.limits,{'kind':'compact','name':'calc'},timeout=5)
        self.assertEqual(rec['exit_code'],0);self.assertEqual(rec['live_group_members_after_cleanup'],[])
        job=json.loads((self.root/'external-receipts/calc.job.json').read_text());self.assertEqual(job['supervision']['rss_bytes'],256*1024**2);self.assertEqual(job['supervision']['address_space_bytes'],384*1024**2)
    def test_parent_enforces_subphase_when_child_is_blocked(self):
        p=self.manifest['execution_policy']['phases']['calc'];p.update(producer_seconds=1,reduce_seconds=1,wall_seconds=4)
        self.ready();self.close()
        with self.assertRaises(RuntimeError):run_local_stage(self.root,self.manifest,self.limits,{'kind':'compact','name':'calc'},timeout=4,synthetic_fault='stall_compact')
        rec=json.loads((self.root/'external-receipts/calc.json').read_text());self.assertIn('supervisor_error',rec);self.assertEqual(rec['live_group_members_after_cleanup'],[])
        self.assertRaises(ValueError,DryRunner,self.root,self.manifest,self.limits)


if __name__=='__main__':unittest.main()
