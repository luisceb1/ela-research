import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import inspect_interrupted_pilot as audit


class InterruptedAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.job={'root':str(self.root),'manifest':{'sealed_workflow':{'steps':[{'name':'index_archive','kind':'http','url':audit.INDEX_URL,'expected':{'bytes':audit.INDEX_BYTES,'sha256':audit.INDEX_SHA}}]}},'limits':{'wall_seconds':9000,'transfer_bytes':12_000_000_000}}
        self.write('workflow-job.json',self.job)
        self.write('operator-acceptance.json',{'prepared_file_sha256':self.sha('workflow-job.json')})
        self.write('preflight-result.json',{'status':'verified'})
        self.ledger={'fingerprint':audit.digest({'manifest':self.job['manifest'],'limits':self.job['limits']}),'limits':self.job['limits'],'transfer_bytes_consumed':256,'transfer_elapsed_seconds':3600.0,'deadline_epoch':1793658000.877632,
            'phases':{'preflight':{'status':'verified','receipt_sha256':self.sha('preflight-result.json')},'index_archive':{'status':'started'}}}
        self.write('ledger.json',self.ledger)
        self.write('workflow-receipts/run.json',{'status':'finished','exit_code':-9,'live_group_members_after_cleanup':[],'supervisor_error':'RuntimeError: Cumulative transfer time cap'})
        self.write('index_archive.attempt-0.json',{'status':'started','body_bytes':256})
        (self.root/'index_archive.attempt-0.partial').write_bytes(b'x'*256)
    def write(self,name,obj):
        path=self.root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj))
    def sha(self,name):return hashlib.sha256((self.root/name).read_bytes()).hexdigest()
    def snapshot(self):return {str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
    def test_exact_audit_without_writes_and_never_marks_verified(self):
        before=self.snapshot();result=audit.inspect(self.root)
        self.assertEqual(before,self.snapshot());self.assertFalse(result['source_verified'])
        self.assertEqual(result['partial_bytes'],256);self.assertEqual(result['partial_sha256'],hashlib.sha256(b'x'*256).hexdigest())
        self.assertEqual(result['minimum_remaining_body_if_range_is_later_validated'],audit.INDEX_BYTES-256+audit.RAW_BYTES)
        self.assertIn('NOT_RESUMABLE',result['status'])
    def test_does_not_refund_uncertain_extra_charge(self):
        self.ledger['transfer_bytes_consumed']=512;self.write('ledger.json',self.ledger)
        result=audit.inspect(self.root);self.assertEqual(result['charged_minus_partial_bytes'],256)
        self.assertEqual(result['charged_body_bytes'],512)
    def test_inconsistent_budget_or_fingerprint_or_preflight_rejected(self):
        for mutation in ('budget','fingerprint','preflight'):
            with self.subTest(mutation=mutation):
                ledger=copy.deepcopy(self.ledger)
                if mutation=='budget':ledger['transfer_bytes_consumed']=128
                elif mutation=='fingerprint':ledger['fingerprint']='bad'
                else:ledger['phases']['preflight']['receipt_sha256']='bad'
                self.write('ledger.json',ledger);self.assertRaises(ValueError,audit.inspect,self.root)
    def test_nonempty_group_or_successful_or_sealed_run_rejected(self):
        for mutation in ('group','success','seal'):
            with self.subTest(mutation=mutation):
                outer={'status':'finished','exit_code':-9,'live_group_members_after_cleanup':[]}
                if mutation=='group':outer['live_group_members_after_cleanup']=[123]
                elif mutation=='success':outer['exit_code']=0
                else:self.write('workflow-seal.json',{})
                self.write('workflow-receipts/run.json',outer);self.assertRaises(ValueError,audit.inspect,self.root)
    def test_partial_symlink_or_full_size_refused(self):
        path=self.root/'index_archive.attempt-0.partial';path.unlink();target=self.root/'other';target.write_bytes(b'x'*256);path.symlink_to(target)
        self.assertRaises(ValueError,audit.inspect,self.root)
        path.unlink()
        with path.open('wb') as f:f.truncate(audit.INDEX_BYTES)
        self.assertRaises(ValueError,audit.inspect,self.root)
    def test_metadata_cap_and_acceptance_rejected(self):
        self.write('operator-acceptance.json',{'prepared_file_sha256':'bad'})
        self.assertRaises(ValueError,audit.inspect,self.root)
        with patch.object(audit,'MAX_METADATA',4):self.assertRaises(ValueError,audit.inspect,self.root)


if __name__=='__main__':unittest.main()
