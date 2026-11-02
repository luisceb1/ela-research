"""Prepared real-route controls. No human downloads or HISAT2 alignment.

Adapter tests substitute a fixture-emitting producer; they exercise plaintext
staging, compact decoding, producer status and provenance, not actual alignment.
"""
import copy
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO=Path(__file__).resolve().parents[1];sys.path.insert(0,str(REPO/'scripts'))
import real_pilot_workflow as real
from pilot_dry_runner import DryRunner,digest
from compact_pe_pipeline import DEFAULT_LIMITS
import pilot_execution_policy as policy


@unittest.skipUnless(importlib.util.find_spec('pysam'),'Pinned PySAM required')
class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.binary=self.root/'hisat2-align-s';shutil.copyfile(sys.executable,self.binary);self.binary.chmod(0o755)
        self.inspector=self.root/'hisat2-inspect-s';shutil.copyfile(sys.executable,self.inspector);self.inspector.chmod(0o755)
        self.aligner={'path':str(self.binary),'sha256':real.file_digest(self.binary)['sha256'],'version':'2.2.3','source_commit':'0d244324f98de541bce04d45c75e83bc3522f7f4','inspect_path':str(self.inspector),'inspect_sha256':real.file_digest(self.inspector)['sha256']}
        self.manifest,self.limits=real.make_manifest(self.aligner)
    def test_canonical_two_library_manifest_and_budget(self):
        spec=real.validate_manifest(self.manifest,self.limits)
        transfers=[s for s in spec['steps'] if s['kind']=='http']
        self.assertEqual(sum(s['expected']['bytes'] for s in transfers),10_705_490_230)
        self.assertEqual(len(transfers),5)
        names=[s['name'] for s in spec['steps']]
        self.assertLess(names.index('index_extract'),names.index('index_probe'))
        self.assertLess(names.index('index_probe'),names.index('CTRL_R1'))
        self.assertLess(names.index('CTRL_compute'),names.index('TDP_R1'))
        for c in self.manifest['real_compute'].values():
            self.assertEqual(c['minimum_fragment_union'],20)
            self.assertEqual(c['max_plaintext_bytes']+c['limits']['max_temp_bytes'],6*real.GiB)
    def test_origin_sample_threshold_and_cap_mutations_rejected(self):
        for mutation in ('origin','url','threshold','pairs','cap','argv'):
            with self.subTest(mutation=mutation):
                m=copy.deepcopy(self.manifest);l=copy.deepcopy(self.limits)
                if mutation=='origin':m['sealed_workflow']['origins'][0]='https://example.com'
                elif mutation=='url':m['sealed_workflow']['steps'][1]['url']='https://genome-idx.s3.amazonaws.com/other'
                elif mutation=='threshold':m['real_compute']['CTRL_compute']['minimum_fragment_union']=1
                elif mutation=='pairs':m['paired_fastq']['CTRL_prefix']['prefix_pairs']=2_000_000
                elif mutation=='cap':l['transfer_bytes']+=1
                else:m['sealed_workflow']['steps'][-1]['argv']=['free-command']
                self.assertRaises(ValueError,real.validate_manifest,m,l)
    def test_synthetic_runner_cannot_accept_real_policy(self):
        self.assertRaises(ValueError,DryRunner,self.root/'run',self.manifest,self.limits)
        self.assertFalse((self.root/'run/ledger.json').exists())
        self.assertRaises(ValueError,policy.validate,self.manifest['execution_policy'],self.limits)
    def test_real_opt_in_cannot_accept_synthetic_policy(self):
        local=copy.deepcopy(self.manifest);local['execution_policy'].update(schema='pilot-b4-local-v1',production_enabled=False)
        self.assertRaises(ValueError,DryRunner,self.root/'run',local,self.limits,real_pilot=True)
    def test_real_ledger_labels_and_missing_seal_prevent_adoption(self):
        r=DryRunner(self.root/'run',self.manifest,self.limits,real_pilot=True)
        self.assertEqual(r.state['mode'],'real-pilot');r.close()
        self.assertRaises(ValueError,DryRunner,self.root/'run',self.manifest,self.limits,real_pilot=True)
    def test_hash_and_version_and_symlink_required(self):
        bad=copy.deepcopy(self.aligner);bad['sha256']='0'*64
        self.assertRaises(ValueError,real.validate_aligner,bad)
        bad=copy.deepcopy(self.aligner);bad['version']='2.2.1'
        self.assertRaises(ValueError,real.validate_aligner,bad)
        self.binary.unlink();self.binary.symlink_to(sys.executable)
        self.assertRaises(ValueError,real.validate_aligner,self.aligner)
    def test_native_binary_standin_not_certified_as_hisat(self):
        self.assertRaises(ValueError,real.version_probe,self.aligner)
    def test_prepare_never_starts_network_or_aligner(self):
        with patch.object(real,'source_commit_at',return_value=self.aligner['source_commit']),patch.object(real.subprocess,'Popen',side_effect=AssertionError('No network/aligner in prepare')):
            with patch.object(real,'check_host',return_value={'test':'host observation only'}):
                job=real.prepare(self.root/'output',self.binary)
        self.assertFalse(job['execution_enabled']);real.validate_job(job)
        self.assertFalse((self.root/'output').exists())
    def test_acceptance_required_before_descriptor_or_filesystem_access(self):
        self.assertRaises(ValueError,real.execute,self.root/'does-not-exist',None)
        self.assertFalse((self.root/'does-not-exist').exists())
    def test_wrong_acceptance_rejected_before_root_creation(self):
        plan=self.root/'plan.json';plan.write_text('{}')
        self.assertRaises(ValueError,real.execute,plan,'0'*64)
        self.assertEqual(set(self.root.iterdir()),{self.binary,self.inspector,plan})
    def test_index_summary_identity_and_failure(self):
        root=self.root
        class Runner:
            manifest={'aligner':self.aligner}
            state={'phases':{'index_extract':{'status':'verified'}}}
            def __init__(self):self.root=root
            def remaining(self,*args):return 5
        r=Runner()
        for output,accepted in [(b'Sequence-3\tchr19\t58617616\n',True),(b'Sequence-3\tchr19\t123\n',False),(b'Sequence-3\t19\t58617616\n',False)]:
            class Producer:
                def __init__(self,*a,**k):self.stdout=io.BytesIO(output)
                def wait(self,**k):return 0
                def poll(self):return 0
            with patch.object(real,'verify_archive'),patch.object(real.subprocess,'Popen',Producer):
                if accepted:self.assertIn('index summary only',real.index_probe(r)['scope'])
                else:self.assertRaises(ValueError,real.index_probe,r)
    def test_source_checkout_must_match_pin_and_be_clean(self):
        with patch.object(real.subprocess,'check_output',return_value='bad-commit'):
            self.assertRaises(ValueError,real.source_commit_at,self.root)
        with patch.object(real.subprocess,'check_output',return_value=self.aligner['source_commit']),patch.object(real.subprocess,'run') as run:
            self.assertEqual(real.source_commit_at(self.root),self.aligner['source_commit']);run.assert_called_once()
    def test_fixed_argv_uses_plaintext_not_gzip_or_wrapper_shell(self):
        spec=self.manifest['real_compute']['CTRL_compute'];argv=real.alignment_argv(self.root,spec,self.aligner)
        self.assertEqual(argv[0],str(self.binary));self.assertIn('/dev/stdout',argv)
        self.assertTrue(argv[argv.index('-1')+1].endswith('/alignment-inputs/CTRL_compute/R1.fastq'))
        self.assertNotIn('--rna-strandness',argv);self.assertNotIn('--tmo',argv)
        self.assertNotIn('shell',argv);self.assertNotIn('gzip',argv)
    def test_host_memory_and_disk_are_stop_gates(self):
        good={'architecture':'x86_64','python':'3.12.3','pysam_version':'0.23.3','cpu_affinity_count':2,'memory_ceiling_bytes':8*real.GiB,'memory_available_bytes':7*real.GiB,'disk_free_bytes':40*real.GiB}
        for key,value in [('memory_ceiling_bytes',6*real.GiB),('memory_available_bytes',5*real.GiB),('disk_free_bytes',32*real.GiB),('cpu_affinity_count',1)]:
            with self.subTest(key=key),patch.object(real,'host_report',return_value={**good,key:value}):
                self.assertRaises(ValueError,real.check_host,self.root/'new',self.limits)


@unittest.skipUnless(importlib.util.find_spec('pysam'),'Pinned PySAM required')
class PlainAndAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);root=Path(self.tmp.name)
        fixtures=REPO/'reports/unc13a-minigenome-20261102/fixtures';pair=root/'paired-fastq/prefix';pair.mkdir(parents=True)
        self.original=[]
        for i in (1,2):
            data=(fixtures/f'r{i}.fq').read_bytes();self.original.append(data);(pair/f'prefix-R{i}.fastq.gz').write_bytes(gzip.compress(data,mtime=0))
        self.spec={'paired_phase':'prefix','archive_phase':'index_extract','index_prefix':'hg38/genome','run':'SRR33425816','library':'fixture',
            'max_plaintext_bytes':1024**2,'minimum_fragment_union':20,'targets':[['mini',556,1844,'-'],['mini',556,1413,'-'],['mini',1541,1844,'-']],
            'limits':{**DEFAULT_LIMITS,'max_result_bytes':65536}}
        spec=self.spec
        class Runner:
            def __init__(self):self.root=root;self.manifest={'real_compute':{'CTRL_compute':spec}};self.state={'fingerprint':'fixture-only','phases':{}}
            def guard(self):pass
            def save(self):pass
            def begin(self,name,kind,signature):self.state['phases'][name]={'kind':kind,'status':'started','signature':signature};return True
            def remaining(self,*args):return 5
            def compact_reduction(self,name):self.reduced=True
        self.r=Runner();self.sam=(fixtures/'wild.sam').read_bytes()
    def test_plain_prefixes_exact_and_charged_to_temporaries(self):
        result=real.stage_plain_prefixes(self.r,'CTRL_compute',self.spec)
        for item,data in zip(result,self.original):
            self.assertEqual(Path(item['path']).read_bytes(),data)
            self.assertEqual(item['sha256'],hashlib.sha256(data).hexdigest())
        usage=policy.disk_usage(self.r.root,{'phases':{}})
        self.assertEqual(usage['temporaries'],sum(map(len,self.original)))
    def test_plain_cap_leaves_failed_partial_without_promotion(self):
        self.spec['max_plaintext_bytes']=10
        self.assertRaises(ValueError,real.stage_plain_prefixes,self.r,'CTRL_compute',self.spec)
        self.assertFalse((self.r.root/'alignment-inputs/CTRL_compute/R1.fastq').exists())
    def test_gzip_crc_failure_rejected(self):
        source=self.r.root/'paired-fastq/prefix/prefix-R1.fastq.gz';data=bytearray(source.read_bytes());data[-8]^=1;source.write_bytes(data)
        self.assertRaises(gzip.BadGzipFile,real.stage_plain_prefixes,self.r,'CTRL_compute',self.spec)
    def invoke_adapter(self,exit_code=0,tamper=False):
        argv=['standin-not-hisat'];binding={'policy':'real-stream-v1','spec':self.spec,'argv':argv}
        outer=self
        class Producer:
            def __init__(self,args,**kwargs):
                outer.assertEqual(args,argv)
                for i,data in enumerate(outer.original,1):outer.assertEqual((outer.r.root/f'alignment-inputs/CTRL_compute/R{i}.fastq').read_bytes(),data)
                self.stdout=io.BytesIO(outer.sam)
            def wait(self,**kwargs):
                if tamper:(outer.r.root/'alignment-inputs/CTRL_compute/R1.fastq').write_bytes(b'changed')
                return exit_code
            def poll(self):return exit_code
        with patch.object(real,'stream_binding',return_value=(binding,digest(binding))),patch.object(real.subprocess,'Popen',Producer):
            real.run_stream(self.r,'CTRL_compute')
        return binding
    def test_fixture_adapter_routes_and_insufficient_coverage_and_plaintext_cleanup(self):
        self.invoke_adapter();phase=self.r.state['phases']['CTRL_compute']
        self.assertEqual(phase['status'],'verified');self.assertEqual(phase['coverage']['fragment_union'],6)
        self.assertFalse(phase['coverage']['adequate']);self.assertFalse((self.r.root/'alignment-inputs/CTRL_compute').exists())
        self.assertFalse(any((self.r.root/'compact').rglob('*.sam')))
    def test_nonzero_producer_rejected_and_not_promoted(self):
        self.assertRaises(ValueError,self.invoke_adapter,7)
        self.assertEqual(self.r.state['phases']['CTRL_compute']['status'],'failed')
        self.assertFalse((self.r.root/'compact/CTRL_compute/receipt.json').exists())
    def test_plain_input_tamper_during_producer_rejected(self):
        self.assertRaises(ValueError,self.invoke_adapter,tamper=True)
        self.assertEqual(self.r.state['phases']['CTRL_compute']['status'],'failed')


if __name__=='__main__':unittest.main()
