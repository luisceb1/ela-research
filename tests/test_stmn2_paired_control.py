"""Fixture-only chr8/plus splice response and offline-source integrity controls."""
import ast,gzip,hashlib,json,os
from pathlib import Path
import socket,sys,tempfile,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import pysam
import stmn2_paired_control_counts as c
import run_gse252892_stmn2_control as r
import run_gse252892_local as old
HEADER=pysam.AlignmentHeader.from_dict({'SQ':[{'SN':'chr8','LN':145138636},{'SN':'chr19','LN':58617616}]})
def read(name='q',first=True,event='cryptic',anchor=15,strand='+',chrom=0):
    a,b=r.EXPECTED_TARGETS[event];x=pysam.AlignedSegment(HEADER);x.query_name=name;x.flag=99 if first else 147;x.reference_id=chrom;x.reference_start=a-anchor;x.mapping_quality=60
    x.cigartuples=[(0,anchor),(3,b-a),(0,anchor)];x.query_sequence='A'*(anchor*2);x.query_qualities=pysam.qualitystring_to_array('I'*(anchor*2))
    x.next_reference_id=chrom;x.next_reference_start=a-anchor;x.set_tag('NH',1);x.set_tag('XS',strand);return x
def pair(**kw):return [read(first=True,**kw),read(first=False,**kw)]
class CountTests(unittest.TestCase):
    def test_plus_chr8_exact_sealed_cryptic_union_once(self):self.assertEqual(c.count_records(pair(),r.EXPECTED_TARGETS)['counts'],{'canonical':0,'cryptic':1})
    def test_canonical_measured(self):self.assertEqual(c.count_records(pair(event='canonical'),r.EXPECTED_TARGETS)['counts'],{'canonical':1,'cryptic':0})
    def test_minus_or_wrong_chrom_cannot_support(self):
        for kw in [{'strand':'-'},{'chrom':1}]:self.assertEqual(c.count_records(pair(**kw),r.EXPECTED_TARGETS)['counts']['cryptic'],0)
    def test_14_anchor_fails_15_passes(self):
        for n,want in [(14,0),(15,1)]:self.assertEqual(c.count_records(pair(anchor=n),r.EXPECTED_TARGETS)['counts']['cryptic'],want)
    def test_off_by_one_not_counted(self):
        xs=pair()
        for x in xs:x.reference_start+=1;x.next_reference_start+=1
        self.assertEqual(c.count_records(xs,r.EXPECTED_TARGETS)['counts']['cryptic'],0)
    def test_multimapping_pair_rejected(self):
        xs=pair();xs[0].set_tag('NH',2)
        self.assertEqual(c.count_records(xs,r.EXPECTED_TARGETS)['qc']['rejected_groups'],1)
    def test_more_than_two_alignments_rejected(self):self.assertEqual(c.count_records(pair()+[read()],r.EXPECTED_TARGETS)['qc']['rejected_groups'],1)
    def test_mate_reciprocity_required(self):
        xs=pair();xs[0].next_reference_start+=1
        self.assertEqual(c.count_records(xs,r.EXPECTED_TARGETS)['qc']['rejected_groups'],1)
    def test_20_flag_is_descriptive_not_psI_or_effect(self):
        xs=[x for i in range(20) for x in pair(name=str(i))];out=c.count_records(xs,r.EXPECTED_TARGETS)
        self.assertTrue(out['support_at_least_20_groups']['cryptic']);self.assertNotIn('psi',out);self.assertNotIn('effect',out)
    def test_new_filter_source_identical_except_gene_and_event_label(self):
        text=(ROOT/'scripts/run_gse252892_local.py').read_text();oldf={n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)}
        text=(ROOT/'scripts/stmn2_paired_control_counts.py').read_text();newf={n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)}
        self.assertEqual(newf['pair_hits'],oldf['pair_hits'])
        self.assertEqual(newf['events'],oldf['events'].replace("'chr19'","'chr8'").replace("read.get_tag('XS')!='-'","read.get_tag('XS')!='+'"))
        self.assertEqual(newf['count_records'],oldf['count_records'].replace("('cryptic_left','cryptic_right')","('cryptic',)"))
class SourceTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name);self.run=self.root/'run06';self.run.mkdir();self.source=self.root/'source.json';inputs=[];self.expected=[]
        for gsm in ['GSM8009878','GSM8009881']:
            d=self.run/gsm;d.mkdir()
            for mate in [1,2]:
                p=d/f'{gsm}_{mate}.fastq.gz';p.write_bytes(gzip.compress((gsm+str(mate)).encode(),mtime=0));h=r.raw_digest(p)
                inputs.append({'gsm':gsm,'url':'https://ftp.sra.ebi.ac.uk/'+p.name,'compressed_bytes':str(h['bytes']),'md5':h['md5']})
                self.expected.append({'gsm':gsm,'file':p.name,'recorded_sha256':h['sha256']})
                p.with_name(p.name+'.verified.json').write_text(json.dumps(dict(status='verified_complete',**h)))
        self.source.write_text(json.dumps({'run_root':str(self.run),'base':{'input_files':inputs},'lineage':{'prior_roots':[str(self.root/f'old{i}') for i in range(5)]}}))
        for n in ['result.json','supervision.json','transfer-ledger.json']:
            (self.run/n).write_bytes((ROOT/'reports/gse252892-audit-verification-20261114/original'/n).read_bytes())
        p=patch.object(r,'SOURCE_SHA',r.prep.sha256(self.source));p.start();self.addCleanup(p.stop)
        original=r.read
        def reader(p):
            if Path(p)==ROOT/'reports/gse252892-audit-verification-20261114/verification.json':return {'zip_sha256':'c8751b9610512791ba40a613449ad332833ff557e8c371f96e118636361e4617','recorded_complete_inputs':self.expected}
            return original(p)
        p=patch.object(r,'read',reader);p.start();self.addCleanup(p.stop)
    def test_local_inputs_rehashed_without_network(self):
        with patch.object(socket,'create_connection',side_effect=AssertionError('network forbidden')):
            source,record=r.source_record(self.source)
        self.assertEqual(len(record['inputs']),4);self.assertEqual(len(record['prior_roots']),6)
    def test_corrupt_raw_refused(self):
        (self.run/'GSM8009878'/'GSM8009878_1.fastq.gz').write_bytes(b'bad')
        with self.assertRaisesRegex(ValueError,'digest'):r.source_record(self.source)
    def test_changed_source_metadata_refused(self):
        (self.run/'result.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'metadata changed'):r.source_record(self.source)
    def test_wrong_source_proposal_refused(self):
        self.source.write_text('{}')
        with self.assertRaisesRegex(ValueError,'source proposal'):r.source_record(self.source)
    def test_raw_source_symlink_refused(self):
        p=self.run/'GSM8009878'/'GSM8009878_1.fastq.gz';p.unlink();p.symlink_to(self.source)
        with self.assertRaisesRegex(ValueError,'nonsymlink'):r.source_record(self.source)
    def test_network_acceptance_nonzero_refused_before_execution(self):
        with self.assertRaisesRegex(ValueError,'zero network'):r.execute(self.source,'wrong',1)
    def test_wrong_accepted_hash_refused(self):
        with self.assertRaisesRegex(ValueError,'proposal SHA'):r.execute(self.source,'wrong',0)
    def test_cli_options_unchanged_only_source_paths_replaced(self):
        plan={'run_root':'/new','fastp':{'path':'/fastp'},'source':{'base':{'tools':{'aligner':{'path':'/hisat'}},'index_directory':'/index'}},'inputs':[{'gsm':'GSM8009878','path':'/old/r1.gz'},{'gsm':'GSM8009878','path':'/old/r2.gz'}]}
        cmd=r.commands(plan,'GSM8009878');before=old.commands({'run_root':'/new','fastp':plan['fastp'],'base':plan['source']['base']},'GSM8009878')
        for flag,want in [('-i','/old/r1.gz'),('-I','/old/r2.gz')]:before['fastp'][before['fastp'].index(flag)+1]=want
        self.assertEqual(cmd,before)
    def test_worker_without_supervisor_refused(self):
        root=self.root/'new';root.mkdir();plan=self.root/'plan.json';plan.write_text(json.dumps({'run_root':str(root)}));(root/'accepted.json').write_text(json.dumps({'supervisor_pid':-1,'plan_sha256':'wrong','network_bytes':0}))
        with self.assertRaisesRegex(ValueError,'supervisor'):r.worker(plan)
    def test_claim_prevents_second_execute(self):
        plan=self.root/'plan.json';run=self.root/'out';plan.write_text(json.dumps({'run_root':str(run)}));Path(str(plan)+'.claimed.json').write_text('consumed')
        with patch.object(r,'validate'),patch.object(r.old,'physical_free',return_value=10**12):
            with self.assertRaises(FileExistsError):r.execute(plan,r.prep.sha256(plan),0)
        self.assertFalse(run.exists())
