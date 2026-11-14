"""Fixture-only reconciliation and complete-file reuse after sampler termination."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import random
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import gse252892_after_sampler as m
import gse252892_range_transport as t
from test_gse252892_range_transport import CFG,Opener

class SnapshotTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name);self.old=self.root/'v3';self.old.mkdir()
        self.control=self.old/'GSM8009878';self.control.mkdir();self.settings=dict(t.RECOVERY_SETTINGS,chunk_bytes=8,overlap_bytes=1)
        self.body=gzip.compress(random.Random(1).randbytes(600),mtime=0);self.full=self.control/'first.gz';self.full.write_bytes(self.body)
        self.rows=[{'gsm':'GSM8009878','url':'https://ftp.sra.ebi.ac.uk/first.gz','compressed_bytes':str(len(self.body)),'md5':hashlib.md5(self.body).hexdigest()},
                   {'gsm':'GSM8009878','url':'https://ftp.sra.ebi.ac.uk/second.gz','compressed_bytes':'1600','md5':'fixture'}]
        self.parts=self.control/'second.gz.ranges';self.parts.mkdir();self.receipts=self.old/'transport-receipts';self.receipts.mkdir();self.records=[]
        for i in range(1,233):
            second=i>=110;a=(i-110)*8 if second else (i-1)*4;n=8 if second else 4;complete=i<=94 or second;source=self.rows[1 if second else 0]
            r={'id':i,'url':source['url'],'total':int(source['compressed_bytes']),'start':a,'end':a+n-1,'attempt':1,'observed_bytes':n if complete else 0,'charged_bytes':n if complete else 0,'uncertain_bytes':0,'inflight_max_bytes':0,'status':'complete' if complete else 'failed'}
            if second:
                p=self.parts/f'range-{a:012d}-{a+n-1:012d}-a1.ok';p.write_bytes(b'x'*n);r.update(path=str(p),sha256=m.oldblocks.sha(p))
            self.records.append(r);self.write_receipt(i,r)
        complete_bytes=sum(r['observed_bytes'] for r in self.records);new_observed=complete_bytes+4;self.prior=100;self.upper=self.prior+new_observed+1
        active232=dict(self.records[-1],status='started');active233=dict(active232,id=233,start=984,end=991,observed_bytes=4,charged_bytes=4,inflight_max_bytes=1)
        self.ledger={'prior_charge_bytes':self.prior,'new_observed_body_bytes':new_observed,'actual_body_bytes':self.prior+new_observed,'new_charged_upper_bytes':new_observed,'body_upper_bound_bytes':self.upper,'cap_bytes':14000000000,'request_attempts':233,'completed_attempts':231,'active_requests':[active232,active233],'receipt_directory':str(self.receipts)}
        self.inherited={'prior_plan_path':'v2.json','prior_roots':['v1','v2'],'prior_charge_bytes':self.prior}
        self.plan=self.root/'v3-plan.json';self.plan.write_text(json.dumps({'schema':'gse252892-retained-v3','base_sha256':'base','transport':self.settings,'lineage':self.inherited,'run_root':str(self.old),'base':{'input_files':self.rows}}))
        plan_sha=m.oldblocks.sha(self.plan);claim={'plan_sha256':plan_sha,'transfer_bytes':14000000000}
        Path(str(self.plan)+'.claimed.json').write_text(json.dumps(claim));self.write('accepted.json',claim)
        self.write('supervision.json',{'plan_sha256':plan_sha,'status':'failed','cleanup_error':None,'failure':f"[Errno 2] No such file or directory: '{self.old}/transport-receipts/000232.json.tmp'"})
        self.write('transfer-ledger.json',self.ledger)
        self.full_info={'path':str(self.full),'bytes':len(self.body),'md5':self.rows[0]['md5'],'sha256':m.oldblocks.sha(self.full),'status':'verified_complete'}
        self.full.with_name(self.full.name+'.verified.json').write_text(json.dumps(self.full_info))
        for name,value in [('V3_SHA',plan_sha),('V3_UPPER',self.upper),('V3_OBSERVED',new_observed),('V3_COMPLETE_BYTES',complete_bytes),('FIRST_SHA',self.full_info['sha256'])]:
            p=patch.object(m,name,value);p.start();self.addCleanup(p.stop)
    def write(self,name,data):(self.old/name).write_text(json.dumps(data))
    def write_receipt(self,i,data):(self.receipts/f'{i:06d}.json').write_text(json.dumps(data))
    def run_record(self,current=True):return m.record(self.plan,lambda p:json.loads(Path(p).read_text()),lambda *a,**kw:self.inherited,self.settings,'base',14000000000,current)
    def test_durable_active_deduplicated_and_reserved_tail_carried(self):
        out=self.run_record();self.assertEqual(out['prior_charge_bytes'],self.upper)
        self.assertEqual(len(out['retained_blocks']),123);self.assertEqual(len(out['complete_inputs']),1)
        self.assertEqual(out['prior_roots'],['v1','v2',str(self.old)])
        self.assertEqual(m.reconcile(self.ledger,self.records),self.upper)
    def test_new_ledger_distinguishes_observed_from_prior_reservation(self):
        import io
        budget=t.Budget(self.root/'new-ledger.json',1000,100,prior_observed=99)
        r=budget.start('fixture',0,2,3,1);budget.read(r,io.BytesIO(b'abc'),3);budget.finish(r,'complete')
        info=json.loads((self.root/'new-ledger.json').read_text())
        self.assertEqual(info['actual_body_bytes'],102);self.assertEqual(info['body_upper_bound_bytes'],103)
        self.assertEqual(info['prior_unobserved_bytes_charged'],1)
    def test_reservation_cannot_be_reset_to_actual(self):
        ledger=copy.deepcopy(self.ledger);ledger['body_upper_bound_bytes']-=1
        with self.assertRaisesRegex(ValueError,'Conservative'):m.reconcile(ledger,self.records)
    def test_disagreeing_durable_active_snapshot_rejected(self):
        ledger=copy.deepcopy(self.ledger);ledger['active_requests'][0]['observed_bytes']-=1
        with self.assertRaisesRegex(ValueError,'snapshot disagrees'):m.reconcile(ledger,self.records)
    def test_missing_or_duplicate_request_identity_rejected(self):
        for records in [self.records[:-2],self.records+[self.records[0]]]:
            with self.assertRaises(ValueError):m.reconcile(self.ledger,records)
    def test_changed_first_full_file_rejected(self):
        self.full.write_bytes(b'x'*len(self.body))
        with self.assertRaisesRegex(ValueError,'complete-file digest'):self.run_record()
    def test_changed_retained_second_file_block_rejected(self):
        Path(self.records[-1]['path']).write_bytes(b'z'*8)
        with self.assertRaisesRegex(ValueError,'block size/hash'):self.run_record()
    def test_new_worker_failure_receipt_rejected(self):
        self.write('worker-failure.json',{})
        with self.assertRaisesRegex(ValueError,'worker failure'):self.run_record()
    def test_missing_final_receipt_rejected(self):
        (self.receipts/'000232.json').unlink()
        with self.assertRaisesRegex(ValueError,'232 durable'):self.run_record()
    def test_recorded_complete_file_source_identity_rejected(self):
        info=dict(self.full_info,md5='wrong');self.full.with_name(self.full.name+'.verified.json').write_text(json.dumps(info))
        with self.assertRaisesRegex(ValueError,'identity changed'):self.run_record()
    def test_copy_complete_preserves_source_and_published_md5(self):
        out=self.run_record();d=self.root/'new';d.mkdir();before=self.full.read_bytes()
        copied=m.copy_complete(self.rows[0],out['complete_inputs'][0],d,t.save)
        self.assertEqual(copied.read_bytes(),before);self.assertEqual(self.full.read_bytes(),before)
        self.assertNotEqual(copied.stat().st_ino,self.full.stat().st_ino)
        info=json.loads(copied.with_name(copied.name+'.verified.json').read_text());self.assertEqual(info['raw_body_bytes'],0)
    def test_changed_source_during_copy_no_promotion(self):
        out=self.run_record();self.full.write_bytes(b'bad');d=self.root/'new';d.mkdir()
        with self.assertRaisesRegex(ValueError,'digest mismatch'):m.copy_complete(self.rows[0],out['complete_inputs'][0],d,t.save)
        self.assertFalse((d/'first.gz').exists());self.assertTrue((d/'first.gz.copying').exists())

class RetainedWithoutPrefixTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)
        self.body=gzip.compress(bytes(range(256))*8,mtime=0);self.item={'url':'https://ftp.sra.ebi.ac.uk/fixture.gz','compressed_bytes':str(len(self.body)),'md5':hashlib.md5(self.body).hexdigest()}
        self.old=self.root/'old';self.old.mkdir();self.pieces=[]
        for a,z in [(0,31),(32,63),(96,127)]:
            p=self.old/f'{a}.ok';p.write_bytes(self.body[a:z+1]);self.pieces.append({'path':str(p),'start':a,'end':z,'bytes':32,'sha256':t.digest_file(p),'url':self.item['url']})
    def run_file(self,mode=None):
        d=self.root/'new';d.mkdir();b=t.Budget(self.root/'ledger.json',10000,100);op=Opener(self.body,mode)
        p=t.download(self.item,d,b,settings=CFG,opener=op,sleep=lambda n:None,retained=self.pieces);return p,b,op
    def test_probe_first_block_then_only_gaps_and_preserve_old(self):
        before={str(p):p.read_bytes() for p in self.old.iterdir()};p,b,op=self.run_file()
        self.assertEqual(p.read_bytes(),self.body);self.assertEqual(op.calls[0][:2],(0,15))
        self.assertEqual(b.observed,len(self.body)-96+16)
        self.assertEqual(before,{str(p):p.read_bytes() for p in self.old.iterdir()})
    def test_wrong_probe_prevents_further_transfer_and_promotion(self):
        with self.assertRaisesRegex(t.IntegrityError,'Remote probe'):self.run_file('bad-overlap')
        self.assertFalse((self.root/'new'/'fixture.gz').exists())
    def test_missing_first_retained_context_rejected(self):
        self.pieces=self.pieces[1:]
        with self.assertRaisesRegex(t.IntegrityError,'first block'):self.run_file()
