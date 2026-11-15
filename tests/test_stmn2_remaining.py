"""Offline remaining-library scope and fixed-method regression controls."""
import ast
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import run_stmn2_remaining as r
import run_gse252892_stmn2_control as prior


class RemainingTests(unittest.TestCase):
    def test_exact_four_libraries_eight_inputs(self):
        rows = r.inputs()
        self.assertEqual(len(rows), 8)
        self.assertEqual(tuple(dict.fromkeys(x['gsm'] for x in rows)), r.SELECTED)
        self.assertEqual(sum(int(x['compressed_bytes']) for x in rows), 27762593667)

    def test_no_discovery_libraries_acquired(self):
        self.assertFalse({'GSM8009878', 'GSM8009881'} & set(r.SELECTED))

    def test_options_same_only_library_and_run_paths_change(self):
        plan = {'run_root': '/new', 'fastp': {'path': '/fastp'},
                'source': {'base': {'tools': {'aligner': {'path': '/hisat'}}, 'index_directory': '/index'}}}
        template = r.old.commands({'run_root': '/new', 'fastp': plan['fastp'], 'base': plan['source']['base']}, 'GSM8009878')
        for gsm in r.SELECTED:
            run = next(x['run'] for x in r.inputs() if x['gsm'] == gsm)
            expected = {k: [x.replace('GSM8009878', gsm).replace('SRR27477544', run) for x in v]
                        for k, v in template.items()}
            self.assertEqual(r.commands(plan, gsm), expected)

    def test_measurement_source_identical_except_existing_directory(self):
        def function(path, name):
            text = path.read_text()
            return next(ast.get_source_segment(text,n) for n in ast.parse(text).body
                        if isinstance(n, ast.FunctionDef) and n.name == name)
        previous = function(ROOT/'scripts/run_gse252892_stmn2_control.py', 'stage')
        expected = previous.replace('def stage(', 'def measure(').replace("d=root/gsm;d.mkdir();cmd=plan['commands'][gsm]", "d=root/gsm;cmd=plan['commands'][gsm]").replace('counter.count_records','stmn.counter.count_records').replace('EXPECTED_TARGETS','stmn.EXPECTED_TARGETS')
        self.assertEqual(function(ROOT/'scripts/run_stmn2_remaining.py', 'measure'), expected)

    def test_fixed_seal_and_resources(self):
        self.assertEqual(prior.EXPECTED_TARGETS, {'canonical':[79611214,79636801], 'cryptic':[79611214,79616821]})
        self.assertEqual(r.CAPS['cpus'],2)
        self.assertEqual(r.CAPS['transfer_bytes'],40000000000)
        self.assertEqual(r.CAPS['root_bytes'],200*1024**3)
        self.assertEqual(r.CAPS['wall_seconds'],96*3600)

    def test_history_not_reset_by_new_budget(self):
        self.assertEqual(r.HISTORY, {'charged_bytes':13007068985, 'observed_bytes':13006020409})
        self.assertEqual(r.HISTORY['charged_bytes']+r.CAPS['transfer_bytes'],53007068985)

    def test_wrong_budget_refused_before_execution(self):
        with self.assertRaisesRegex(ValueError, 'fixed transfer'):
            r.execute(Path('/missing'), 'wrong', 0)

    def test_wrong_hash_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'plan.json';p.write_text('{}')
            with self.assertRaisesRegex(ValueError, 'proposal SHA'):
                r.execute(p,'wrong',r.CAPS['transfer_bytes'])

    def test_consumed_claim_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'plan.json';p.write_text(json.dumps({'run_root':str(Path(d)/'out')}))
            Path(str(p)+'.claimed.json').write_text('consumed')
            with patch.object(r,'validate'),patch.object(r.old,'physical_free',return_value=10**12):
                with self.assertRaises(FileExistsError):
                    r.execute(p,r.prep.sha256(p),r.CAPS['transfer_bytes'])

    def test_existing_root_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'plan.json';p.write_text(json.dumps({'run_root':d}))
            with patch.object(r,'validate'),patch.object(r.old,'physical_free',return_value=10**12):
                with self.assertRaisesRegex(ValueError,'New root'):
                    r.execute(p,r.prep.sha256(p),r.CAPS['transfer_bytes'])
