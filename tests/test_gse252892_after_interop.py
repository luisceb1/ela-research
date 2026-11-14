"""Settled transfer evidence and full-input checks after interop failure."""
import gzip,hashlib,json
from pathlib import Path
import sys,tempfile,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import gse252892_after_interop as m
import gse252892_range_transport as t

class InteropEvidenceTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.root=Path(tmp.name);self.old=self.root/'old';self.old.mkdir();d=self.old/'GSM8009878';d.mkdir();self.d=d
        self.rows=[];self.infos=[]
        for name in ['first.gz','second.gz']:
            p=d/name;p.write_bytes(gzip.compress(name.encode(),mtime=0));info={'path':str(p),'status':'verified_complete','bytes':p.stat().st_size,'md5':hashlib.md5(p.read_bytes()).hexdigest(),'sha256':m.b.sha(p)}
            p.with_name(name+'.verified.json').write_text(json.dumps(info));self.infos.append(info)
            self.rows.append({'gsm':'GSM8009878','url':'https://ftp.sra.ebi.ac.uk/'+name,'compressed_bytes':str(info['bytes']),'md5':info['md5']})
        self.inherited={'prior_plan_path':'v3','prior_roots':['v1','v2','v3'],'prior_charge_bytes':10,'prior_observed_body_bytes':9}
        self.plan=self.root/'plan.json';self.plan.write_text(json.dumps({'schema':'gse252892-after-sampler-v4','transport':t.RECOVERY_SETTINGS,'base_sha256':'base','lineage':self.inherited,'run_root':str(self.old),'base':{'input_files':self.rows}}));sha=m.b.sha(self.plan)
        claim={'plan_sha256':sha,'transfer_bytes':14000000000};Path(str(self.plan)+'.claimed.json').write_text(json.dumps(claim));self.write('accepted.json',claim)
        self.write('supervision.json',{'status':'failed','cleanup_error':None,'plan_sha256':sha,'failure':'Cannot query real C: free space through fixture'})
        self.receipts=self.old/'transport-receipts';self.receipts.mkdir()
        for i in range(1,234):
            (self.receipts/f'{i:06d}.json').write_text(json.dumps({'id':i,'url':self.rows[1]['url'],'total':int(self.rows[1]['compressed_bytes']),'status':'complete','inflight_max_bytes':0,'uncertain_bytes':0,'charged_bytes':1,'observed_bytes':1,'start':0,'end':0}))
        self.ledger={'prior_charge_bytes':10,'prior_observed_body_bytes':9,'prior_unobserved_bytes_charged':1,'new_observed_body_bytes':233,'actual_body_bytes':242,'new_charged_upper_bytes':233,'body_upper_bound_bytes':243,'cap_bytes':14000000000,'request_attempts':233,'completed_attempts':233,'active_requests':[],'receipt_directory':str(self.receipts)}
        self.write('transfer-ledger.json',self.ledger)
        (d/'fastp.log').write_text('fixture completed');(d/'fastp.json').write_text('{}')
        for obj,name,val in [(m,'V4_SHA',sha),(m,'CHARGE',243),(m,'OBSERVED',242),(m,'NEW_OBSERVED',233),(m.a,'FIRST_SHA',self.infos[0]['sha256']),(m,'SECOND_SHA',self.infos[1]['sha256'])]:
            p=patch.object(obj,name,val);p.start();self.addCleanup(p.stop)
    def write(self,name,data):(self.old/name).write_text(json.dumps(data))
    def run_record(self):return m.record(self.plan,lambda p:json.loads(Path(p).read_text()),lambda *a,**k:self.inherited,t.RECOVERY_SETTINGS,'base',14000000000)
    def test_two_full_inputs_no_blocks_charge_and_observation_distinct(self):
        out=self.run_record();self.assertEqual(len(out['complete_inputs']),2);self.assertEqual(out['retained_blocks'],[])
        self.assertEqual(out['prior_charge_bytes'],243);self.assertEqual(out['prior_observed_body_bytes'],242)
        self.assertEqual(len(out['prior_roots']),4)
    def test_corrupt_second_full_input_refused(self):
        (self.d/'second.gz').write_bytes(b'bad')
        with self.assertRaisesRegex(ValueError,'digest'):self.run_record()
    def test_pending_reservation_or_requests_not_silently_reset(self):
        d=dict(self.ledger,active_requests=[{}]);self.write('transfer-ledger.json',d)
        with self.assertRaisesRegex(ValueError,'settled v4 ledger'):self.run_record()
    def test_missing_request_receipt_refused(self):
        (self.receipts/'000233.json').unlink()
        with self.assertRaisesRegex(ValueError,'233 settled'):self.run_record()
    def test_charge_change_refused(self):
        d=dict(self.ledger,body_upper_bound_bytes=242);self.write('transfer-ledger.json',d)
        with self.assertRaisesRegex(ValueError,'ledger'):self.run_record()
    def test_unexpected_completed_count_requires_review(self):
        (self.d/'junction-counts.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'inspect before continuation'):self.run_record()
    def test_changed_consumed_claim_refused(self):
        Path(str(self.plan)+'.claimed.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'claim/acceptance'):self.run_record()
    def test_changed_request_totals_refused(self):
        p=self.receipts/'000233.json';d=json.loads(p.read_text());d.update(charged_bytes=0,observed_bytes=0);p.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,'totals'):self.run_record()
