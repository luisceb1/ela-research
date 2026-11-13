"""Fixture-only lineage integrity and unchanged scientific function contracts."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import run_gse252892_local as m

class LineageTests(unittest.TestCase):
    def fixture(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);root=Path(temp.name)
        old=root/'old';old.mkdir();plan=root/'old-plan.json'
        plan.write_text(json.dumps({'schema':'gse252892-bounded-v1','base_sha256':m.BASE_SHA,'run_root':str(old)}))
        sha=m.prep.sha256(plan);(old/'GSM8009878').mkdir()
        row=m.prep.selected_inputs(ROOT/'reports/local-raw-feasibility-20261112/fastq-manifest.tsv')[0]
        prefix=old/'GSM8009878'/(Path(row['url']).name+'.partial');prefix.write_bytes(b'\x1f\x8bfixture-prefix')
        n=prefix.stat().st_size;h=m.prep.sha256(prefix)
        claim={'plan_sha256':sha,'transfer_bytes':m.CAPS['transfer_bytes']}
        Path(str(plan)+'.claimed.json').write_text(json.dumps(claim))
        (old/'accepted.json').write_text(json.dumps(claim))
        (old/'supervision.json').write_text(json.dumps({'plan_sha256':sha,'status':'failed','cleanup_error':None}))
        (old/'worker-failure.json').write_text(json.dumps({'error':'Raw length/MD5 mismatch'}))
        ledger={'actual_body_bytes':n,'body_upper_bound_bytes':n,'requests':[{'url':row['url'],'expected_bytes':int(row['compressed_bytes']),'actual_bytes':n,'status':'failed','inflight_max_bytes':0,'observed_body_prefix_sha256':h}]}
        (old/'transfer-ledger.json').write_text(json.dumps(ledger))
        return plan,old,prefix,n,h,sha
    def test_prefix_and_failed_charge_preserved(self):
        p,old,prefix,n,h,sha=self.fixture();before=prefix.read_bytes()
        with patch.object(m,'PRIOR_PLAN_SHA',sha),patch.object(m,'PRIOR_BYTES',n),patch.object(m,'PREFIX_SHA',h):out=m.prior_record(p)
        self.assertEqual(out['prior_charge_bytes'],n);self.assertEqual(prefix.read_bytes(),before)
        self.assertEqual(out['prefix']['sha256'],h)
    def test_changed_prefix_refused(self):
        p,old,prefix,n,h,sha=self.fixture();prefix.write_bytes(b'x'*n)
        with patch.object(m,'PRIOR_PLAN_SHA',sha),patch.object(m,'PRIOR_BYTES',n),patch.object(m,'PREFIX_SHA',h):
            with self.assertRaisesRegex(ValueError,'partial bytes/hash'):m.prior_record(p)
    def test_old_unknown_charge_cannot_be_reset(self):
        p,old,prefix,n,h,sha=self.fixture();q=old/'transfer-ledger.json';d=json.loads(q.read_text());d['body_upper_bound_bytes']+=1;q.write_text(json.dumps(d))
        with patch.object(m,'PRIOR_PLAN_SHA',sha),patch.object(m,'PRIOR_BYTES',n),patch.object(m,'PREFIX_SHA',h):
            with self.assertRaisesRegex(ValueError,'charge/prefix'):m.prior_record(p)
    def test_missing_or_changed_claim_refused(self):
        p,old,prefix,n,h,sha=self.fixture();Path(str(p)+'.claimed.json').write_text('{}')
        with patch.object(m,'PRIOR_PLAN_SHA',sha),patch.object(m,'PRIOR_BYTES',n),patch.object(m,'PREFIX_SHA',h):
            with self.assertRaisesRegex(ValueError,'remain consumed'):m.prior_record(p)
    def test_original_scientific_functions_byte_identical(self):
        expected=json.loads((ROOT/'reports/gse252892-range-recovery-20261113/scientific-functions-66eb858.json').read_text())['function_source_sha256']
        text=(ROOT/'scripts/run_gse252892_local.py').read_text()
        found={x.name:hashlib.sha256(ast.get_source_segment(text,x).encode()).hexdigest() for x in ast.parse(text).body if isinstance(x,ast.FunctionDef) and x.name in expected}
        self.assertEqual(found,expected)
    def test_original_14GB_cap_and_48h_new_window(self):
        self.assertEqual(m.CAPS['transfer_bytes'],14_000_000_000)
        self.assertEqual(m.CAPS['wall_seconds'],172800)
        self.assertEqual(m.ranged.SETTINGS['chunk_bytes'],33554432)
        self.assertEqual(m.ranged.SETTINGS['workers'],4)
        self.assertEqual(m.ranged.SETTINGS['attempts'],3)
