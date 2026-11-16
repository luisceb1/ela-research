"""Offline source/command/scope controls, not biological simulations."""
import ast
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import run_unc13a_remaining as r


class OfflineTests(unittest.TestCase):
    def test_fixed_four_libraries(self):
        self.assertEqual(r.SELECTED,('GSM8009879','GSM8009880','GSM8009882','GSM8009883'))

    def test_zero_transfer_and_retained_history(self):
        self.assertEqual(r.CAPS['network_bytes'],0);self.assertEqual(r.CAPS['transfer_bytes'],0)
        self.assertEqual(r.HISTORY,{'observed_bytes':40772442278,'charged_bytes':40773490854})

    def test_fixed_resources(self):
        self.assertEqual([r.CAPS[k] for k in ['wall_seconds','cpus','process_as_bytes','group_rss_bytes','root_bytes','windows_reserve_bytes']],
                         [172800,2,8*1024**3,6*1024**3,200*1024**3,50*1024**3])

    def test_sealed_junctions_and_counter_not_reimplemented(self):
        seal=r.read(ROOT/r.TARGET)
        self.assertEqual(seal['junctions'],{'canonical':[17641556,17642844],'cryptic_left':[17641556,17642413],'cryptic_right':[17642541,17642844]})
        source=(ROOT/'scripts/run_unc13a_remaining.py').read_text()
        self.assertIn("old.count_records(sam,read(ROOT/TARGET)['junctions'])",source)
        self.assertNotIn('def count_records',source)

    def test_command_options_unchanged_except_input_paths(self):
        inputs=[{'gsm':g,'path':'/existing/'+g+'_'+str(m)+'.gz'} for g in r.SELECTED for m in (1,2)]
        plan={'inputs':inputs,'run_root':'/new','fastp':{'path':'/fastp'},'source':{'base':{'tools':{'aligner':{'path':'/hisat'}},'index_directory':'/index'}}}
        for g in r.SELECTED:
            old=r.remaining.commands(plan,g)
            paths=[x['path'] for x in inputs if x['gsm']==g]
            for flag,p in zip(['-i','-I'],paths):old['fastp'][old['fastp'].index(flag)+1]=p
            self.assertEqual(r.commands(plan,g),old)

    def test_nonzero_network_refused(self):
        with self.assertRaisesRegex(ValueError,'zero network'):r.execute('/missing','wrong',1)

    def test_wrong_accepted_hash_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'p.json';p.write_text('{}')
            with self.assertRaisesRegex(ValueError,'proposal SHA'):r.execute(p,'wrong',0)

    def test_wrong_source_hash_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'p.json';p.write_text('{}')
            with self.assertRaisesRegex(ValueError,'source proposal'):r.source_record(p)

    def test_existing_root_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'p.json';p.write_text(json.dumps({'run_root':d}))
            with patch.object(r,'validate'),patch.object(r.old,'physical_free',return_value=10**12):
                with self.assertRaisesRegex(ValueError,'New root'):r.execute(p,r.prep.sha256(p),0)

    def test_consumed_claim_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'p.json';p.write_text(json.dumps({'run_root':str(Path(d)/'run')}));Path(str(p)+'.claimed.json').write_text('consumed')
            with patch.object(r,'validate'),patch.object(r.old,'physical_free',return_value=10**12):
                with self.assertRaises(FileExistsError):r.execute(p,r.prep.sha256(p),0)

    def test_no_biological_gate_skips_a_library(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'run';root.mkdir();p=Path(d)/'p.json';p.write_text(json.dumps({'run_root':str(root)}))
            r.save(root/'accepted.json',{'supervisor_pid':os.getppid(),'plan_sha256':r.prep.sha256(p),'network_bytes':0})
            with patch.object(r,'validate'),patch.object(r.os,'getpgrp',return_value=os.getpid()),patch.object(r,'measure',return_value={'counts':{'canonical':0,'cryptic_left':0,'cryptic_right':0}}) as m:
                r.worker(p)
            self.assertEqual(m.call_count,4)
            result=r.read(root/'result.json');self.assertEqual(result['gene'],'UNC13A');self.assertEqual(result['network_bytes'],0)

    def test_measure_source_changes_only_target_counter_and_labels(self):
        def fun(file,name):
            text=(ROOT/file).read_text();return next(ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name==name)
        previous=fun('scripts/run_stmn2_remaining.py','measure')
        expected=previous.replace("'chr8'","'chr19'").replace('145138636','58617616').replace('chr8 header mismatch','chr19 header mismatch').replace('stmn.counter.count_records(sam,stmn.EXPECTED_TARGETS)',"old.count_records(sam,read(ROOT/TARGET)['junctions'])").replace("'STMN2'","'UNC13A'").replace('alignment_and_stmn2_count','alignment_and_unc13a_count').replace('stmn2-counts.json','unc13a-counts.json')
        self.assertEqual(fun('scripts/run_unc13a_remaining.py','measure'),expected)
