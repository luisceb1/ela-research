import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO=Path(__file__).resolve().parents[1];SCRIPTS=REPO/'scripts';sys.path.insert(0,str(SCRIPTS))
try:
    import compact_pe_pipeline as compact
    import pe_fragment_contract as pe
    from process_supervisor_v2 import supervise
finally:sys.path.pop(0)


HAS_PYSAM=importlib.util.find_spec('pysam') is not None
FIXTURES=REPO/'reports/unc13a-minigenome-20261102/fixtures'
TARGETS=[['mini',556,1844,'-'],['mini',556,1413,'-'],['mini',1541,1844,'-']]
HEADER=b'@HD\tVN:1.6\tSO:unknown\n@SQ\tSN:chr19\tLN:100000\n@RG\tID:A\tSM:synthetic\n@RG\tID:B\tSM:synthetic\n'


@unittest.skipUnless(HAS_PYSAM,'Pinned optional PySAM required; dedicated workflow installs it')
class CompactTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.out=self.root/'out'
        self.limits={**compact.DEFAULT_LIMITS,'chunk_bytes':4096,'max_row_bytes':4096,'merge_fan_in':2}
        self.data=(FIXTURES/'wild.sam').read_bytes();self.targets=copy.deepcopy(TARGETS)
    def run_pipeline(self,**kw):return compact.run(io.BytesIO(kw.pop('data',self.data)),self.out,'fixture',kw.pop('targets',self.targets),kw.pop('limits',self.limits),kw.pop('finish_source',lambda:0),**kw)
    def rejected(self,**kw):
        with self.assertRaises((ValueError,UnicodeError)):self.run_pipeline(**kw)
        self.assertEqual(json.loads((self.out/'result.json').read_text())['status'],'failed')
    def synthetic(self,lines):self.targets=[['chr19',120,220,'+']];self.data=HEADER+('\n'.join(lines)+'\n').encode()
    def test_four_existing_fixtures_equal_both_baselines_at_both_anchors(self):
        for name in ('wild','multicopy','wrongstrand','wrongmotif'):
            with self.subTest(name=name):
                out=self.root/name
                result=compact.run(io.BytesIO((FIXTURES/(name+'.sam')).read_bytes()),out,'fixture',TARGETS,self.limits,lambda:0)
                for anchor in (15,8):
                    for backend in ('text','hts'):
                        records=(pe.text_records if backend=='text' else pe.hts_records)(FIXTURES/(name+'.ordered.sam'),anchor)
                        counts,qc=pe.count_fragments(records,'fixture');route=result['routes'][backend+str(anchor)]
                        self.assertEqual(route['qc'],qc)
                        self.assertEqual(route['counts'],[{'event':t,'fragments':counts.get(('fixture',)+tuple(t),0)} for t in TARGETS])
                        expected=[2,2,2] if name=='wild' and anchor==15 else [3,3,3] if name=='wild' else [0,0,0]
                        self.assertEqual([row['fragments'] for row in route['counts']],expected)
                self.assertFalse((out/'work').exists());self.assertEqual(result['status'],'verified')
                self.assertEqual(result['source_sha256'],hashlib.sha256((FIXTURES/(name+'.sam')).read_bytes()).hexdigest())
    def test_nonseekable_stream_and_multiple_merge_passes(self):
        class Stream:
            def __init__(self,data):self.data=io.BytesIO(data)
            def readline(self,n):return self.data.readline(n)
        limits={**self.limits,'chunk_bytes':1024,'max_row_bytes':1024}
        result=compact.run(Stream(self.data),self.out,'fixture',TARGETS,limits,lambda:0)
        self.assertGreater(result['initial_runs'],2);self.assertGreaterEqual(result['merge_passes'],2)
        self.assertLessEqual(result['peak_temp_bytes'],limits['max_temp_bytes'])
    def test_unsorted_rg_double_support_and_secondaries_preserve_counts(self):
        from test_pe_fragment_contract import pair
        lines=pair('q2',rg='B')+pair('q10',rg='A')+pair('q2',rg='A')+pair('q2',rg='B',flags=(99|256,147|2048))
        self.synthetic(lines[::2]+lines[1::2]);r=self.run_pipeline()
        self.assertEqual(r['routes']['text15']['counts'][0]['fragments'],3);self.assertEqual(r['routes']['text15']['qc']['nonprimary_excluded'],2)
    def test_offtarget_splice_strand_still_affects_qc(self):
        from test_pe_fragment_contract import pair
        self.synthetic(pair(cigars=('20M100N20M','25M100N15M'),xs=('+','-')))
        r=self.run_pipeline();self.assertEqual(r['routes']['text15']['counts'][0]['fragments'],0)
        self.assertEqual(r['routes']['text15']['qc']['excluded:event_strand'],1)
    def test_temp_runs_contain_no_read_sequence_quality_or_cigar(self):
        def guard():
            for p in (self.out/'work').glob('*'):
                for row in p.read_bytes().splitlines():
                    obj=json.loads(row.split(b'\t',2)[2]);self.assertEqual(set(obj),{'meta','events'})
                    self.assertTrue(set(obj['meta']).isdisjoint({'seq','qual','cigar','SEQ','QUAL','CIGAR'}))
        self.run_pipeline(checkpoint=guard)
    def test_group_over_sixteen_fails_closed(self):
        from test_pe_fragment_contract import pair
        self.synthetic(pair()*9);self.rejected()
    def test_duplicate_tag_rejected(self):
        self.data=self.data.replace(b'NH:i:1',b'NH:i:1\tNH:i:1',1);self.rejected()
    def test_truncated_line_rejected(self):self.rejected(data=self.data.rstrip(b'\n'))
    def test_missing_or_wrong_reference_header_rejected(self):self.rejected(targets=[['absent',1,2,'-']])
    def test_header_after_records_rejected(self):self.rejected(data=self.data+b'@CO\tlate\n')
    def test_producer_nonzero_cannot_certify_eof(self):
        self.rejected(finish_source=lambda:7);self.assertEqual(json.loads((self.out/'result.json').read_text())['producer_exit_code'],7)
    def test_line_byte_header_record_and_row_caps(self):
        for field,value in [('max_line_bytes',64),('max_input_bytes',256),('max_header_bytes',16),('max_records',1),('max_row_bytes',16)]:
            with self.subTest(field=field):
                self.out=self.root/field;self.rejected(limits={**self.limits,field:value})
    def test_chunk_initial_runs_and_disk_caps(self):
        for change in ({'chunk_bytes':1024,'max_row_bytes':1024,'max_runs':1},{'max_temp_bytes':100}):
            with self.subTest(change=change):
                self.out=self.root/('case'+str(len(list(self.root.iterdir()))));self.rejected(limits={**self.limits,**change})
    def test_result_cap_after_reduction(self):
        targets=[['mini',i,i+1,'-'] for i in range(100,125)]
        self.rejected(targets=targets,limits={**self.limits,'max_result_bytes':4096})
    def test_decoder_disagreement_rejected(self):
        original=pe.hts_decoded
        def wrong(records,anchor):
            for r in original(records,anchor):r['events']=[];yield r
        with patch.object(pe,'hts_decoded',side_effect=wrong):self.rejected()
    def test_output_directory_not_overwritten(self):self.run_pipeline();self.assertRaises(FileExistsError,self.run_pipeline)
    def test_invalid_policy_rejected_before_destination(self):
        for targets,limits in [([],self.limits),(TARGETS+TARGETS,self.limits),(TARGETS,{**self.limits,'merge_fan_in':1})]:
            self.assertRaises(ValueError,self.run_pipeline,targets=targets,limits=limits)
        self.assertFalse(self.out.exists())
    def test_supervised_actual_pipe_success_and_nonzero_producer(self):
        for exit_code in (0,7):
            folder=self.root/('pipe'+str(exit_code));folder.mkdir()
            code="""import json,sys,subprocess
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from compact_pe_pipeline import run
policy=json.loads(sys.argv[4])
producer=subprocess.Popen([sys.executable,'-c','from pathlib import Path;import sys;sys.stdout.buffer.write(Path(sys.argv[1]).read_bytes());sys.exit(int(sys.argv[2]))',sys.argv[2],sys.argv[3]],stdout=subprocess.PIPE)
with producer.stdout as stream:run(stream,Path(sys.argv[5]),'fixture',policy['targets'],policy['limits'],producer.wait)
"""
            policy=json.dumps({'targets':TARGETS,'limits':self.limits})
            rec=supervise('pipe',[sys.executable,'-c',code,str(SCRIPTS),str(FIXTURES/'wild.sam'),str(exit_code),policy,str(folder/'out')],folder/'receipts',timeout=5,rss_limit=256*1024**2,address_space=256*1024**2)
            result=json.loads((folder/'out/result.json').read_text());self.assertEqual(result['status'],'verified' if exit_code==0 else 'failed')
            self.assertEqual(result['producer_exit_code'],exit_code);self.assertEqual(rec['live_group_members_after_cleanup'],[])
            self.assertEqual(rec['exit_code']==0,exit_code==0)
    def test_supervised_blocked_pipe_kills_producer_and_consumer(self):
        code="""import sys,json,subprocess
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from compact_pe_pipeline import run
policy=json.loads(sys.argv[3])
producer=subprocess.Popen([sys.executable,'-c','from pathlib import Path;import sys,time;sys.stdout.buffer.write(Path(sys.argv[1]).read_bytes());sys.stdout.flush();time.sleep(30)',sys.argv[2]],stdout=subprocess.PIPE)
with producer.stdout as stream:run(stream,Path(sys.argv[4]),'fixture',policy['targets'],policy['limits'],producer.wait)
"""
        rec=supervise('blocked',[sys.executable,'-c',code,str(SCRIPTS),str(FIXTURES/'wild.sam'),json.dumps({'targets':TARGETS,'limits':self.limits}),str(self.out)],self.root/'receipts',timeout=1,rss_limit=256*1024**2,address_space=256*1024**2)
        self.assertEqual(rec['violation'],'timeout');self.assertEqual(rec['live_group_members_after_cleanup'],[]);self.assertGreaterEqual(rec['max_group_members'],2)
        self.assertEqual(json.loads((self.out/'result.json').read_text())['status'],'started')
        self.assertRaises(FileExistsError,self.run_pipeline)


if __name__=='__main__':unittest.main()
