"""Offline controls for importing evidence from the fixed failed ranged attempt."""
import gzip
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import gse252892_retained_blocks as m
import gse252892_range_transport as t
from test_gse252892_range_transport import Opener,CFG

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.root=Path(tmp.name)
        self.old=self.root/'old';self.old.mkdir();self.receipts=self.old/'transport-receipts';self.receipts.mkdir()
        self.url='https://ftp.sra.ebi.ac.uk/fixture.fastq.gz';self.settings=dict(t.SETTINGS,chunk_bytes=32,overlap_bytes=16)
        self.inherited={'prior_plan_path':'v1.json','prior_root':str(self.root/'v1'),'prior_charge_bytes':91,'prefix':{'path':'prefix','bytes':91,'sha256':'prefix-sha','url':self.url}}
        self.parts=self.old/'GSM8009878'/'fixture.fastq.gz.ranges';self.parts.mkdir(parents=True)
        self.records=[]
        for i in range(1,61):
            a,z=(75,90) if i==1 else (91+(i-2)*32,91+(i-1)*32-1)
            complete=i<=50;n=z-a+1
            r={'id':i,'url':self.url,'start':a,'end':z,'total':3000,'attempt':1,'observed_bytes':n if complete else 0,
               'charged_bytes':n if complete else 0,'uncertain_bytes':0,'inflight_max_bytes':0,'status':'complete' if complete else 'failed'}
            if complete:
                p=self.parts/f'range-{a:012d}-{z:012d}-a1.ok';p.write_bytes(b'x'*n);r.update(path=str(p),sha256=m.sha(p))
            self.records.append(r);self.write_receipt(i,r)
        self.observed=sum(r['observed_bytes'] for r in self.records);self.charge=91+self.observed
        self.plan=self.root/'v2.json';self.plan.write_text(json.dumps({'schema':'gse252892-range-v2','base_sha256':'base','transport':self.settings,'lineage':self.inherited,'run_root':str(self.old),'base':{'input_files':[{'url':self.url,'compressed_bytes':'3000'}]}}))
        self.plan_sha=m.sha(self.plan);claim={'plan_sha256':self.plan_sha,'transfer_bytes':14000000000}
        Path(str(self.plan)+'.claimed.json').write_text(json.dumps(claim));self.write('accepted.json',claim)
        self.write('supervision.json',{'plan_sha256':self.plan_sha,'status':'failed','cleanup_error':None})
        self.write('worker-failure.json',{'error':'Short range body / premature EOF'})
        self.write('transfer-ledger.json',{'prior_charge_bytes':91,'new_observed_body_bytes':self.observed,'actual_body_bytes':self.charge,'new_charged_upper_bytes':self.observed,'body_upper_bound_bytes':self.charge,'cap_bytes':14000000000,'request_attempts':60,'completed_attempts':60,'active_requests':[],'receipt_directory':str(self.receipts)})
        for name,value in [('V2_SHA',self.plan_sha),('V2_CHARGE',self.charge),('V2_OBSERVED',self.observed),('V2_COMPLETE_BYTES',self.observed)]:
            p=patch.object(m,name,value);p.start();self.addCleanup(p.stop)
    def write(self,name,data): (self.old/name).write_text(json.dumps(data))
    def write_receipt(self,i,data): (self.receipts/f'{i:06d}.json').write_text(json.dumps(data))
    def run_record(self,current=True):return m.record(self.plan,lambda p:json.loads(Path(p).read_text()),lambda *a,**k:self.inherited,self.settings,'base',14000000000,current)
    def test_import_49_blocks_with_original_cumulative_charge(self):
        out=self.run_record();self.assertEqual(len(out['retained_blocks']),49);self.assertEqual(out['prior_charge_bytes'],self.charge)
        self.assertEqual(len(out['attempt_receipt_sha256']),60);self.assertEqual(len(out['prior_roots']),2)
    def test_changed_block_rejected(self):
        Path(self.records[1]['path']).write_bytes(b'z'*32)
        with self.assertRaisesRegex(ValueError,'size/hash'):self.run_record()
    def test_path_escape_rejected_even_without_hash_pass(self):
        r=self.records[1];r['path']=str(self.root/'other.ok');self.write_receipt(2,r)
        with self.assertRaisesRegex(ValueError,'path changed'):self.run_record(False)
    def test_block_symlink_rejected(self):
        p=Path(self.records[1]['path']);other=self.root/'other';other.write_bytes(p.read_bytes());p.unlink();p.symlink_to(other)
        with self.assertRaisesRegex(ValueError,'regular file'):self.run_record()
    def test_missing_receipt_rejected(self):
        (self.receipts/'000060.json').unlink()
        with self.assertRaisesRegex(ValueError,'all 60'):self.run_record()
    def test_duplicate_success_interval_rejected(self):
        r=dict(self.records[1],id=3);self.write_receipt(3,r)
        with self.assertRaisesRegex(ValueError,'Duplicate'):self.run_record()
    def test_changed_aggregate_charge_rejected(self):
        p=self.old/'transfer-ledger.json';d=json.loads(p.read_text());d['body_upper_bound_bytes']+=1;self.write('transfer-ledger.json',d)
        with self.assertRaisesRegex(ValueError,'cumulative'):self.run_record()
    def test_uncertain_old_read_not_silently_reset(self):
        r=self.records[-1];r['uncertain_bytes']=1;self.write_receipt(60,r)
        with self.assertRaisesRegex(ValueError,'Unsettled'):self.run_record()
    def test_changed_source_or_endpoint_rejected(self):
        r=self.records[1];r['end']-=1;self.write_receipt(2,r)
        with self.assertRaisesRegex(ValueError,'identity/range'):self.run_record()
    def test_missing_consumed_claim_rejected(self):
        Path(str(self.plan)+'.claimed.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'claim/acceptance'):self.run_record()

class ReuseTransportTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.root=Path(tmp.name)
        self.body=gzip.compress(bytes(range(256))*8,mtime=0)
        self.item={'url':'https://ftp.sra.ebi.ac.uk/fixture.fastq.gz','compressed_bytes':str(len(self.body)),'md5':hashlib.md5(self.body).hexdigest()}
        self.old=self.root/'old';self.old.mkdir();p=self.old/'prefix';p.write_bytes(self.body[:40])
        self.prefix={'path':str(p),'bytes':40,'sha256':t.digest_file(p)};self.pieces=[]
        for a,z in [(72,103),(136,167)]:
            p=self.old/f'{a}.ok';p.write_bytes(self.body[a:z+1]);self.pieces.append({'path':str(p),'start':a,'end':z,'bytes':z-a+1,'sha256':t.digest_file(p),'url':self.item['url']})
    def download(self):
        d=self.root/'new';d.mkdir();budget=t.Budget(self.root/'ledger.json',10000,999);op=Opener(self.body)
        result=t.download(self.item,d,budget,self.prefix,CFG,op,lambda n:None,retained=self.pieces)
        return result,budget,op
    def test_download_only_holes_preserve_old_files_full_MD5(self):
        before={str(p):p.read_bytes() for p in self.old.iterdir()};result,budget,op=self.download()
        self.assertEqual(result.read_bytes(),self.body);self.assertEqual(before,{str(p):p.read_bytes() for p in self.old.iterdir()})
        self.assertEqual(budget.observed,len(self.body)-40-64+16);self.assertEqual(budget.upper(),999+budget.observed)
        for a,z,_ in op.calls[1:]:
            self.assertTrue(all(z<p['start'] or a>p['end'] for p in self.pieces))
    def test_tampered_retained_bytes_no_promotion(self):
        Path(self.pieces[0]['path']).write_bytes(b'bad')
        with self.assertRaisesRegex(t.IntegrityError,'Retained block'):self.download()
        self.assertFalse((self.root/'new'/'fixture.fastq.gz').exists())
    def test_retained_wrong_source_no_promotion(self):
        self.pieces[0]['url']='https://other.invalid/file'
        with self.assertRaisesRegex(t.IntegrityError,'source URL'):self.download()
    def test_overlapping_or_out_of_bounds_pieces_refused(self):
        for piece in [{'start':39,'end':50,'bytes':12},{'start':49,'end':500,'bytes':452}]:
            with self.assertRaises(t.IntegrityError):t.missing_ranges(40,200,[piece],8)
    def test_holes_partitioned_at_new_block_size(self):
        out=t.missing_ranges(40,180,self.pieces,8)
        self.assertTrue(all(z-a+1<=8 for a,z in out))
        covered=[i for a,z in out for i in range(a,z+1)]+[i for p in self.pieces for i in range(p['start'],p['end']+1)]
        self.assertEqual(sorted(covered),list(range(40,180)))
    def test_recovery_transport_settings_and_original_cap(self):
        import run_gse252892_local as r
        self.assertEqual(t.RECOVERY_SETTINGS,{'chunk_bytes':8388608,'workers':2,'attempts':5,'socket_seconds':120,'overlap_bytes':1048576,'backoff_seconds':[2,10,30,60]})
        self.assertEqual(r.CAPS['transfer_bytes'],14000000000);self.assertEqual(r.CAPS['wall_seconds'],172800)
