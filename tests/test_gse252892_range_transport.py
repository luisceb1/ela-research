"""All transport bodies, prefixes and HTTP responses in these controls are fixtures."""
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import threading
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import gse252892_range_transport as m

CFG={'chunk_bytes':32,'workers':4,'attempts':3,'socket_seconds':1,'overlap_bytes':16,'backoff_seconds':[0,0]}

class Response(io.BytesIO):
    def __init__(self,b,url,a,z,total,status=206,etag='"fixture"',length=None,content_range=None):
        super().__init__(b);self.status=status;self.url=url
        self.headers={'Content-Range':content_range or f'bytes {a}-{z}/{total}',
                      'Content-Length':str(z-a+1 if length is None else length),'ETag':etag}
    def geturl(self):return self.url

class Opener:
    def __init__(self,b,mode=None):self.b=b;self.mode=mode;self.calls=[];self.counts={};self.lock=threading.Lock()
    def open(self,req,timeout):
        a,z=map(int,re.fullmatch(r'bytes=(\d+)-(\d+)',req.get_header('Range')).groups())
        with self.lock:
            n=self.counts.get((a,z),0)+1;self.counts[(a,z)]=n;self.calls.append((a,z,req.get_header('If-range')))
        data=self.b[a:z+1];kw={}
        if self.mode=='short-first' and a==0 and n==1:data=data[:7]
        if self.mode=='short-always':data=data[:3]
        if self.mode=='ignored':kw['status']=200
        if self.mode=='wrong-range':kw['content_range']='bytes 1-2/3'
        if self.mode=='bad-length':kw['length']=999
        if self.mode=='overflow':data+=b'x'
        if self.mode=='changed-etag' and a>0:kw['etag']='"changed"'
        if self.mode=='bad-overlap':data=b'x'*len(data)
        return Response(data,req.full_url,a,z,len(self.b),**kw)

class TransferTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.b=gzip.compress(bytes(range(256))*2,mtime=0)
        self.item={'url':'https://ftp.sra.ebi.ac.uk/fixture.fastq.gz','compressed_bytes':str(len(self.b)),'md5':hashlib.md5(self.b).hexdigest()}
    def budget(self,prior=0,cap=100000):return m.Budget(self.root/'ledger.json',cap,prior)
    def run_file(self,mode=None,prefix=None,prior=0,cap=100000,settings=None):
        d=self.root/'new';d.mkdir();budget=self.budget(prior,cap);op=Opener(self.b,mode)
        result=m.download(self.item,d,budget,prefix=prefix,settings=settings or CFG,opener=op,sleep=lambda n:None)
        return result,budget,op
    def test_parallel_assembly_exact_and_final_MD5(self):
        result,budget,op=self.run_file()
        self.assertEqual(result.read_bytes(),self.b)
        self.assertEqual(budget.observed,len(self.b));self.assertEqual(budget.upper(),len(self.b))
        self.assertTrue(all(x[2]=='"fixture"' for x in op.calls[1:]))
        self.assertFalse(list(result.parent.rglob('*.ok')))
        verified=json.loads(result.with_name(result.name+'.verified.json').read_text())
        self.assertEqual(verified['status'],'verified_complete')
    def test_old_prefix_reused_unchanged_and_charge_carried(self):
        old=self.root/'old.partial';old.write_bytes(self.b[:91]);before=old.read_bytes()
        prefix={'path':str(old),'bytes':91,'sha256':m.digest_file(old)}
        result,budget,op=self.run_file(prefix=prefix,prior=91)
        self.assertEqual(result.read_bytes(),self.b);self.assertEqual(old.read_bytes(),before)
        self.assertEqual(op.calls[0][:2],(75,90))
        self.assertTrue(all(a>=91 for a,z,tag in op.calls[1:]))
        self.assertEqual(budget.observed,len(self.b)-91+16)
        self.assertEqual(budget.upper(),len(self.b)+16)
    def test_bad_overlap_stops_before_suffix(self):
        old=self.root/'old.partial';old.write_bytes(self.b[:91]);prefix={'path':str(old),'bytes':91,'sha256':m.digest_file(old)}
        with self.assertRaisesRegex(m.IntegrityError,'overlap'):self.run_file(mode='bad-overlap',prefix=prefix,prior=91)
        self.assertEqual(old.read_bytes(),self.b[:91]);self.assertFalse((self.root/'new/fixture.fastq.gz').exists())
    def test_mutated_prefix_refused_before_request(self):
        old=self.root/'old.partial';old.write_bytes(self.b[:91]);prefix={'path':str(old),'bytes':91,'sha256':'0'*64}
        with self.assertRaisesRegex(m.IntegrityError,'prefix integrity'):self.run_file(prefix=prefix)
        self.assertEqual(json.loads((self.root/'ledger.json').read_text())['request_attempts'],0)
    def test_range_200_not_fallback_or_retry(self):
        with self.assertRaisesRegex(m.IntegrityError,'206'):self.run_file(mode='ignored')
        self.assertEqual(json.loads((self.root/'ledger.json').read_text())['request_attempts'],1)
    def test_wrong_content_range_refused(self):
        with self.assertRaisesRegex(m.IntegrityError,'Content-Range'):self.run_file(mode='wrong-range')
    def test_wrong_content_length_refused(self):
        with self.assertRaisesRegex(m.IntegrityError,'Content-Length'):self.run_file(mode='bad-length')
    def test_partial_chunk_retried_only_within_bound_and_charged(self):
        result,budget,op=self.run_file(mode='short-first')
        self.assertEqual(result.read_bytes(),self.b);self.assertEqual(op.counts[(0,31)],2)
        self.assertEqual(budget.observed,len(self.b)+7)
        self.assertTrue(list((self.root/'new').rglob('*a1.partial')))
    def test_exhausted_chunk_retries_retained(self):
        with self.assertRaisesRegex(m.RetryableError,'Short range'):self.run_file(mode='short-always')
        receipts=list((self.root/'transport-receipts').glob('*.json'));self.assertEqual(len(receipts),3)
        self.assertEqual(sum(json.loads(p.read_text())['observed_bytes'] for p in receipts),9)
    def test_changed_validator_fails(self):
        with self.assertRaisesRegex(m.IntegrityError,'validator'):self.run_file(mode='changed-etag')
    def test_full_MD5_mismatch_never_promoted(self):
        self.item['md5']='0'*32
        with self.assertRaisesRegex(m.IntegrityError,'Complete-file'):self.run_file()
        self.assertFalse((self.root/'new/fixture.fastq.gz').exists());self.assertTrue(list((self.root/'new').glob('*.assembling')))
    def test_range_overflow_is_charged_and_refused(self):
        with self.assertRaisesRegex(m.IntegrityError,'overflow'):self.run_file(mode='overflow')
        self.assertEqual(json.loads((self.root/'ledger.json').read_text())['actual_body_bytes'],33)
    def test_prior_budget_is_not_reset(self):
        with self.assertRaises(m.IntegrityError):self.run_file(prior=50,cap=55)
        ledger=json.loads((self.root/'ledger.json').read_text())
        self.assertEqual(ledger['prior_charge_bytes'],50);self.assertLessEqual(ledger['body_upper_bound_bytes'],55)
    def test_no_final_overwrite(self):
        d=self.root/'new';d.mkdir();(d/'fixture.fastq.gz').write_text('keep');budget=self.budget()
        with self.assertRaisesRegex(m.IntegrityError,'overwrite'):m.download(self.item,d,budget,settings=CFG,opener=Opener(self.b))
        self.assertEqual((d/'fixture.fastq.gz').read_text(),'keep')
    def test_blocks_are_contiguous_not_overlapping(self):
        self.assertEqual(m.blocks(5,15,4),[(5,8),(9,12),(13,14)])
    def test_assembly_out_of_order_is_sorted(self):
        pieces=[]
        for a,z in [(4,7),(0,3),(8,len(self.b)-1)]:
            p=self.root/str(a);p.write_bytes(self.b[a:z+1]);pieces.append({'path':str(p),'start':a,'end':z,'bytes':z-a+1,'sha256':m.digest_file(p)})
        out=m.assemble(self.item,pieces,None,self.root/'final.gz');self.assertEqual(Path(out['path']).read_bytes(),self.b)
    def test_gap_refused(self):
        p=self.root/'part';p.write_bytes(self.b[1:])
        with self.assertRaisesRegex(m.IntegrityError,'Gap'):m.assemble(self.item,[{'path':str(p),'start':1,'bytes':len(self.b)-1,'sha256':m.digest_file(p)}],None,self.root/'final.gz')

class BudgetTests(unittest.TestCase):
    def test_concurrent_reservations_never_exceed_lineage_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            budget=m.Budget(Path(tmp)/'ledger.json',10,2);barrier=threading.Barrier(2)
            class Slow:
                def read(self,n):barrier.wait(timeout=5);return b'x'*n
            def job(n):
                r=budget.start('fixture',0,5,6,1);b=budget.read(r,Slow(),6);budget.finish(r,'complete');return len(b)
            with ThreadPoolExecutor(max_workers=2) as pool:counts=list(pool.map(job,[1,2]))
            self.assertEqual(sum(counts),8);self.assertEqual(budget.upper(),10)
    def test_unknown_read_tail_is_conservatively_charged(self):
        with tempfile.TemporaryDirectory() as tmp:
            budget=m.Budget(Path(tmp)/'ledger.json',20,5);r=budget.start('fixture',0,9,10,1)
            class Broken:
                def read(self,n):raise OSError('fixture reset')
            with self.assertRaises(OSError):budget.read(r,Broken(),8)
            budget.finish(r,'failed','fixture reset')
            self.assertEqual(budget.observed,0);self.assertEqual(budget.upper(),13)
            rec=json.loads(next(budget.receipts.glob('*.json')).read_text());self.assertEqual(rec['uncertain_bytes'],8)
    def test_redirect_never_followed(self):
        with self.assertRaises(m.IntegrityError):m.NoRedirect().redirect_request(None,None,None,None,None,None)
