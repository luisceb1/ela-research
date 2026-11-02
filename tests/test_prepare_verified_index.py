"""Offline synthetic contracts; no human index extraction/inspection or network."""
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import prepare_verified_index as offline
from process_supervisor_v2 import atomic_json


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        buffer=io.BytesIO();self.members=[]
        with tarfile.open(fileobj=buffer,mode='w',format=tarfile.USTAR_FORMAT) as tf:
            for i in range(1,9):
                data=f'NOT A REAL INDEX {i}\n'.encode();name=f'hg38/genome.{i}.ht2';info=tarfile.TarInfo(name);info.size=len(data);tf.addfile(info,io.BytesIO(data))
                self.members.append({'name':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        self.source=self.root/'source.gz';self.source.write_bytes(gzip.compress(buffer.getvalue(),mtime=0))
        self.expected=offline.file_digest(self.source);self.spec={'members':self.members,'max_members':16,'max_expanded_bytes':4096,'max_tar_bytes':32768}
    def test_exact_extract_rehash_and_no_archive_modification(self):
        before=self.source.read_bytes();result=offline.extract_checked(self.source,self.root/'out',self.spec,self.expected,lambda:None)
        offline.verify_members(self.root/'out',self.spec,lambda:None)
        self.assertEqual(self.source.read_bytes(),before);self.assertEqual(len(result['files']),8)
        self.assertFalse((self.root/'out/partial').exists());self.assertTrue(result['gzip_eof_crc_validated'])
    def test_wrong_source_hash_never_promotes_members(self):
        bad={**self.expected,'sha256':'0'*64}
        self.assertRaises(ValueError,offline.extract_checked,self.source,self.root/'out',self.spec,bad,lambda:None)
        self.assertTrue((self.root/'out/partial').exists());self.assertFalse(any((self.root/'out/files').rglob('*.ht2')))
    def test_wrong_member_or_crc_rejected(self):
        bad=copy.deepcopy(self.spec);bad['members'][0]['sha256']='0'*64
        self.assertRaises(ValueError,offline.extract_checked,self.source,self.root/'badmember',bad,self.expected,lambda:None)
        content=bytearray(self.source.read_bytes());content[-8]^=1;self.source.write_bytes(content)
        self.assertRaises(gzip.BadGzipFile,offline.extract_checked,self.source,self.root/'badcrc',self.spec,self.expected,lambda:None)
    def test_post_extraction_tamper_or_extra_member_rejected(self):
        out=self.root/'out';offline.extract_checked(self.source,out,self.spec,self.expected,lambda:None)
        path=out/'files/hg38/genome.1.ht2';before=path.read_bytes();path.write_bytes(b'tampered')
        self.assertRaises(ValueError,offline.verify_members,out,self.spec,lambda:None)
        path.write_bytes(before);(out/'files/extra').write_bytes(b'extra')
        self.assertRaises(ValueError,offline.verify_members,out,self.spec,lambda:None)
    def test_output_not_overwritten(self):
        out=self.root/'out';offline.extract_checked(self.source,out,self.spec,self.expected,lambda:None)
        self.assertRaises(FileExistsError,offline.extract_checked,self.source,out,self.spec,self.expected,lambda:None)
    def test_clean_external_decision_seals_exact_index_prefix(self):
        out=self.root/'index';offline.extract_checked(self.source,out,self.spec,self.expected,lambda:None)
        binding={'root':'fixture-only','expected':self.expected,'cumulative_body_bytes':4355802733,'remaining_body_budget_bytes':7644197267}
        job={'root':str(self.root),'archive_spec':self.spec,'recovery':binding,'phases':offline.PHASES}
        atomic_json(self.root/'index-job.json',job)
        state={'status':'verified','phases':{n:{'status':'verified'} for n in offline.PHASES},'new_transfer_bytes':0,'cumulative_body_bytes':4355802733}
        atomic_json(self.root/'index-state.json',state)
        result={'status':'verified_index_pending_outer_seal','state_sha256':offline.meta_sha(self.root/'index-state.json'),'members':self.members,'source_archive_sha256':self.expected['sha256'],'new_transfer_bytes':0,'cumulative_body_bytes':4355802733,'remaining_body_budget_bytes':7644197267,'index_prefix':str(self.root/'index/files/hg38/genome')}
        atomic_json(self.root/'index-result.json',result)
        atomic_json(self.root/'preflight.json',{'scope':'synthetic stand-in, no HISAT2'})
        atomic_json(self.root/'index-summary.json',{'scope':'synthetic stand-in, no real index'})
        (self.root/'supervision').mkdir();record={'status':'finished','exit_code':0,'violation':None,'supervisor_error':None,'live_group_members_after_cleanup':[]}
        atomic_json(self.root/'supervision/run.json',record)
        with patch.object(offline,'recovery_binding',return_value=binding):
            seal=offline.accept_outer(job,record)
            self.assertEqual(seal['status'],'sealed_verified_extracted_index');self.assertEqual(seal['new_transfer_bytes'],0)
            self.assertRaises(FileExistsError,offline.accept_outer,job,record)
            (self.root/'index-seal.json').unlink();result['index_prefix']='/wrong/index';atomic_json(self.root/'index-result.json',result)
            self.assertRaises(ValueError,offline.accept_outer,job,record)
    def test_inspector_summary_version_and_exit_contract(self):
        for text,code,good in [('Sequence-1\tchr19\t58617616\n',0,True),('Sequence-1\tchr19\t123\n',0,False),('Sequence-1\tchr19\t58617616\n',7,False)]:
            class Process:
                def __init__(self,*a,**k):self.stdout=io.BytesIO(text.encode())
                def wait(self,**k):return code
                def poll(self):return code
            with patch.object(offline.real,'validate_aligner'),patch.object(offline.subprocess,'Popen',Process):
                if good:self.assertIn('chr19',offline.inspect_summary({'inspect_path':'fixture-only'},'/fixture',lambda:None)['output'])
                else:self.assertRaises(ValueError,offline.inspect_summary,{'inspect_path':'fixture-only'},'/fixture',lambda:None)


class RecoveryBindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.base=Path(self.tmp.name)
        self.original=self.base/'original';self.original.mkdir();self.root=self.base/'recovery';self.root.mkdir()
        self.fixture_plan={'root':str(self.root),'original_root':str(self.original),'source':dict(offline.recovery.SOURCE),'range_start':1632447284,'original_audit':{'charged_body_bytes':1632463668}}
        self.write('recovery-plan.json',self.fixture_plan)
        self.write('operator-acceptance.json',{'prepared_sha256':offline.meta_sha(self.root/'recovery-plan.json'),'accepted_additional_time_window':True})
        self.write('recovery-state.json',{'status':'verified','transfer_bytes_consumed':4355802733})
        self.write('recovery-result.json',{'status':'verified_archive_pending_outer_seal','state_sha256':offline.meta_sha(self.root/'recovery-state.json'),'bytes':offline.recovery.SOURCE['bytes'],'sha256':offline.recovery.SOURCE['sha256'],'cumulative_body_bytes':4355802733})
        self.write('range-attempt.json',{'fixture':'metadata only, no HTTP'})
        self.write('supervision/run.json',{'status':'finished','exit_code':0,'violation':None,'supervisor_error':None,'live_group_members_after_cleanup':[]})
        # Sparse size placeholder. It is NEVER read/hashed as a real index.
        with (self.root/'hg38_genome.tar.gz').open('wb') as f:f.truncate(offline.recovery.SOURCE['bytes'])
        self.reseal()
        self.binary=self.base/'hisat2-align-s';self.inspector=self.base/'hisat2-inspect-s'
        for p in (self.binary,self.inspector):shutil.copyfile(sys.executable,p);p.chmod(0o755)
    def write(self,name,value):
        p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);atomic_json(p,value)
    def reseal(self):
        self.write('recovery-seal.json',{'status':'sealed_verified_index_archive','sha256':{n:offline.meta_sha(self.root/n) for n in offline.recovery.SEALED},'archive_bytes':offline.recovery.SOURCE['bytes'],'archive_sha256':offline.recovery.SOURCE['sha256'],'cumulative_body_bytes':4355802733})
    def make_job(self):
        with patch.object(offline.real,'source_commit_at',return_value='0d244324f98de541bce04d45c75e83bc3522f7f4'):
            return offline.make_job(self.root,self.binary)
    def test_recovery_metadata_and_cumulative_accounting_without_bulk_hash(self):
        with patch.object(offline,'file_digest',side_effect=AssertionError('No bulk hashing in metadata binding')):
            binding=offline.recovery_binding(self.root)
        self.assertEqual(binding['cumulative_body_bytes'],4355802733);self.assertEqual(binding['remaining_body_budget_bytes'],7644197267)
    def test_changed_metadata_missing_seal_or_bad_outer_refused(self):
        before=(self.root/'recovery-seal.json').read_bytes();(self.root/'recovery-seal.json').unlink()
        self.assertRaises(FileNotFoundError,offline.recovery_binding,self.root);(self.root/'recovery-seal.json').write_bytes(before)
        self.write('supervision/run.json',{'status':'finished','exit_code':7,'live_group_members_after_cleanup':[]})
        self.assertRaises(ValueError,offline.recovery_binding,self.root)
        self.reseal();self.assertRaises(ValueError,offline.recovery_binding,self.root)
    def test_wrong_source_or_charge_refused_even_with_self_consistent_metadata_hashes(self):
        result=offline.read(self.root/'recovery-result.json');result['cumulative_body_bytes']-=16384;self.write('recovery-result.json',result);self.reseal()
        self.assertRaises(ValueError,offline.recovery_binding,self.root)
    def test_fixed_job_rejects_output_caps_inventory_or_network_fields(self):
        job=self.make_job();offline.validate_job(job)
        for field in ('root','cap','member','transfer','url'):
            bad=copy.deepcopy(job)
            if field=='root':bad['root']+='-retry'
            elif field=='cap':bad['limits']['wall_seconds']+=1
            elif field=='member':bad['archive_spec']['members'][0]['sha256']='0'*64
            elif field=='transfer':bad['new_transfer_bytes']=1
            else:bad['url']='https://example.com'
            self.assertRaises(ValueError,offline.validate_job,bad)
    def test_attempted_budget_never_reopens_or_resets_clock(self):
        job=self.make_job();Path(job['root']).mkdir()
        offline.Budget(job)
        before=(Path(job['root'])/'index-state.json').read_bytes()
        self.assertRaises(ValueError,offline.Budget,job)
        self.assertEqual((Path(job['root'])/'index-state.json').read_bytes(),before)
    def test_actual_worker_fails_standin_version_before_sparse_archive_read(self):
        output=self.root.with_name(self.root.name+'-extracted-01')
        free=shutil.disk_usage(self.base);enough=type(free)(free.total,free.used,40*offline.GiB)
        with patch.object(offline.real,'source_commit_at',return_value='0d244324f98de541bce04d45c75e83bc3522f7f4'),patch.object(offline.shutil,'disk_usage',return_value=enough):
            self.assertRaises(ValueError,offline.execute,self.root,self.binary)
        state=offline.read(output/'index-state.json');outer=offline.read(output/'supervision/run.json')
        self.assertEqual(set(state['phases']),{'preflight'});self.assertEqual(state['status'],'failed')
        self.assertEqual(outer['exit_code'],1);self.assertEqual(outer['live_group_members_after_cleanup'],[])
        self.assertFalse((output/'index').exists());self.assertFalse((output/'index-seal.json').exists())
        self.assertEqual(state['new_transfer_bytes'],0)
    def test_external_rejection_never_seals_an_inner_result(self):
        self.assertRaises(ValueError,offline.accept_outer,{'root':str(self.base/'nonexistent')},{'status':'finished','exit_code':7})
        self.assertFalse((self.base/'nonexistent').exists())


if __name__=='__main__':unittest.main()
