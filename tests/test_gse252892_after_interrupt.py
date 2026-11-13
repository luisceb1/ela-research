"""Zero-transfer retry retains all prior resource/accounting evidence."""
from pathlib import Path
import json,sys,tempfile,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import gse252892_after_interrupt as m

class InterruptTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.root=Path(tmp.name);self.old=self.root/'old';self.old.mkdir();(self.old/'transport-receipts').mkdir()
        self.inherited={'prior_plan_path':'v4','prior_roots':['v1','v2','v3','v4'],'prior_charge_bytes':100,'prior_observed_body_bytes':99,'complete_inputs':[{'url':'fixture'}]}
        self.plan=self.root/'plan.json';self.plan.write_text(json.dumps({'schema':'gse252892-drvfs-v5','base_sha256':'base','transport':{},'lineage':self.inherited,'run_root':str(self.old)}));sha=m.b.sha(self.plan)
        p=patch.object(m,'PLAN_SHA',sha);p.start();self.addCleanup(p.stop)
        claim={'plan_sha256':sha,'transfer_bytes':14000000000};Path(str(self.plan)+'.claimed.json').write_text(json.dumps(claim));self.write('accepted.json',claim)
        self.write('supervision.json',{'status':'failed','failure':'KeyboardInterrupt','cleanup_error':None,'plan_sha256':sha})
        self.ledger={'prior_charge_bytes':100,'prior_observed_body_bytes':99,'prior_unobserved_bytes_charged':1,'new_observed_body_bytes':0,'actual_body_bytes':99,'new_charged_upper_bytes':0,'body_upper_bound_bytes':100,'cap_bytes':14000000000,'request_attempts':0,'completed_attempts':0,'active_requests':[],'last_completed':None,'receipt_directory':str(self.old/'transport-receipts')};self.write('transfer-ledger.json',self.ledger)
    def write(self,name,data):(self.old/name).write_text(json.dumps(data))
    def run_record(self):return m.record(self.plan,lambda p:json.loads(Path(p).read_text()),lambda *a,**k:self.inherited,{},'base',14000000000)
    def test_zero_transfer_preserves_root_inputs_and_charge(self):
        out=self.run_record();self.assertEqual(out['prior_roots'],self.inherited['prior_roots']+[str(self.old)])
        self.assertEqual(out['complete_inputs'],self.inherited['complete_inputs']);self.assertEqual(out['prior_charge_bytes'],100);self.assertEqual(out['prior_observed_body_bytes'],99)
    def test_nonzero_transfer_not_silently_discarded(self):
        self.write('transfer-ledger.json',dict(self.ledger,new_observed_body_bytes=1))
        with self.assertRaisesRegex(ValueError,'zero-transfer'):self.run_record()
    def test_active_request_prevents_zero_retry(self):
        self.write('transfer-ledger.json',dict(self.ledger,active_requests=[{}]))
        with self.assertRaisesRegex(ValueError,'zero-transfer'):self.run_record()
    def test_cleanup_error_prevents_retry(self):
        p=self.old/'supervision.json';d=json.loads(p.read_text());d['cleanup_error']='pending';self.write('supervision.json',d)
        with self.assertRaisesRegex(ValueError,'cleaned-up'):self.run_record()
    def test_consumed_claim_cannot_be_reset(self):
        Path(str(self.plan)+'.claimed.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'claim/acceptance'):self.run_record()
    def test_unexpected_request_evidence_prevents_retry(self):
        (self.old/'transport-receipts'/'unexpected.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'request evidence'):self.run_record()
    def test_unexpected_count_requires_review(self):
        d=self.old/'GSM8009878';d.mkdir();(d/'junction-counts.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'result/worker/count'):self.run_record()
