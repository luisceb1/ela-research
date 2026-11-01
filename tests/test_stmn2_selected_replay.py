import gzip
import io
import json
from pathlib import Path
import tempfile
import unittest
from scripts.replay_stmn2_control2_qc import select_fastq,validate_intervals,INTERVALS,SELECTED_READS,SOURCE_READS
from scripts.stmn2_target_alignment_qc import empty_qc,text_observer,validate_histograms,text_stats
from scripts.gse122069_full_control import Bins,count_text


def synthetic_sam():
    header='@HD\tVN:1.6\tSO:unsorted\n@SQ\tSN:chr8\tLN:145138636\n'
    def row(name,right=79636802,left=15,r=20,flag=0,mapq=60,tags='NH:i:1\tXS:A:+\tNM:i:2\tAS:i:-4',clip=0):
        cigar=(str(clip)+'S' if clip else '')+f'{left}M{right-79611214-1}N{r}M'
        return f'{name}\t{flag}\tchr8\t{79611214-left+1}\t{mapq}\t{cigar}\t*\t0\t0\t*\t*\t{tags}\n'
    lines=[row('canonical-known',clip=3,flag=1024),row('cryptic-missing',right=79616822,tags='NH:i:1\tXS:A:+'),
           row('cryptic-sensitive',right=79616822,left=8,r=9,tags='NH:i:1\tXS:A:+\tNM:i:0\tAS:i:0'),
           row('low-mapq',mapq=19),row('unknown-mapq',mapq=255),row('multimap',tags='NH:i:2\tXS:A:+'),
           row('opposite-xs',tags='NH:i:1\tXS:A:-'),row('qcfail',flag=512),row('missing-xs',tags='NH:i:1'),
           row('missing-nh',tags='XS:A:+')]
    return header+''.join(lines)


def projection(sam):
    qc=empty_qc();bins=Bins(3,10);count_text(sam.splitlines(True),bins,on_accepted_junction=text_observer(qc))
    result=bins.finish();validate_histograms(qc,result['counts']);return result,qc


class SelectedReplayTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.path=Path(self.tmp.name)/'x.gz'
        self.records=[f'@original-{i}\nACGN\n+\nIIII\n'.encode() for i in range(1,9)]
        self.path.write_bytes(gzip.compress(b''.join(self.records)))
    def run_selector(self,expected=5,source=8,intervals=((1,2),(5,5),(7,8))):
        out=io.StringIO();qc=select_fastq(self.path,out,expected,source_reads=source,intervals=intervals);return out.getvalue(),qc
    def test_frozen_total(self):validate_intervals(SOURCE_READS,INTERVALS,SELECTED_READS)
    def test_boundaries_names_and_qc(self):
        text,qc=self.run_selector();self.assertEqual(text,b''.join(self.records[i] for i in (0,1,4,6,7)).decode())
        self.assertEqual(qc['reads'],5);self.assertEqual(qc['source_reads_scanned'],8);self.assertTrue(qc['gzip_eof_crc_validated'])
        self.assertEqual(qc['N_bases'],5);self.assertEqual(qc['mean_quality_if_phred33'],40)
    def test_extra_source_rejected(self):
        with self.assertRaisesRegex(ValueError,'Extra'):self.run_selector(source=7,intervals=((1,5),))
    def test_short_source_rejected(self):
        with self.assertRaisesRegex(ValueError,'truncated'):self.run_selector(source=9,intervals=((1,5),))
    def test_crc_rejected(self):
        raw=bytearray(self.path.read_bytes());raw[-8]^=1;self.path.write_bytes(raw)
        with self.assertRaises(gzip.BadGzipFile):self.run_selector()
    def test_truncated_record_rejected(self):
        self.path.write_bytes(gzip.compress(b''.join(self.records)[:-2]))
        with self.assertRaisesRegex(ValueError,'truncated'):self.run_selector()
    def test_invalid_selected_sequence_rejected(self):
        self.path.write_bytes(gzip.compress(b''.join(self.records).replace(b'ACGN',b'ACGX',1)))
        with self.assertRaisesRegex(ValueError,'schema'):self.run_selector()
    def test_invalid_quality_length_rejected(self):
        self.path.write_bytes(gzip.compress(b''.join(self.records).replace(b'IIII',b'III',1)))
        with self.assertRaisesRegex(ValueError,'schema'):self.run_selector()
    def test_interval_failures(self):
        for intervals,expected in [(((1,3),(3,4)),5),(((0,2),),3),(((1,9),),9),(((1,2),),3),(((True,2),),2)]:
            with self.subTest(intervals=intervals),self.assertRaises(ValueError):validate_intervals(8,intervals,expected)
    def test_no_false_full_library_flag(self):
        with self.assertRaisesRegex(ValueError,'complete library'):select_fastq(self.path,io.StringIO(),5,True)
    def test_known_qc_and_filters(self):
        result,qc=projection(synthetic_sam())
        self.assertEqual((result['counts']['15']['canonical'],result['counts']['15']['cryptic']),(1,1))
        self.assertEqual((result['counts']['8']['canonical'],result['counts']['8']['cryptic']),(1,2))
        hist=qc['15']['canonical']['histograms']
        for key,value in [('left_anchor','15'),('right_anchor','20'),('MAPQ','60'),('NM','2'),('AS','-4'),('softclip_bases','3'),('duplicate_flag','1')]:self.assertEqual(hist[key],{value:1})
        self.assertEqual(qc['8']['cryptic']['histograms']['NM'],{'missing':1,'0':1})
    def test_observer_does_not_change_counts(self):
        sam=synthetic_sam();base=Bins(3,10);count_text(sam.splitlines(True),base)
        self.assertEqual(base.finish(),projection(sam)[0])
    def test_histogram_missing_observation_fails(self):
        result,qc=projection(synthetic_sam());qc['8']['cryptic']['histograms']['NM'].clear()
        with self.assertRaises(ValueError):validate_histograms(qc,result['counts'])
    def test_multi_intron_contiguous_anchors(self):
        # A previous intron followed by =/X/M; an insertion stops the left anchor.
        from scripts.gse122069_pilot import TARGETS
        key=next(k for k,v in TARGETS.items() if v=='cryptic')
        line='x\t0\tchr8\t79611175\t60\t5M10N5M1I5=5X10M5607N15M2S\t*\t0\t0\t*\t*\tNH:i:1\tXS:A:+\n'
        stats=text_stats(line,key);self.assertEqual(stats['left_anchor'],20);self.assertEqual(stats['right_anchor'],15)
        self.assertEqual(stats['softclip_bases'],2)


class HistogramSchemaReviewTests(unittest.TestCase):
    def test_empty_metrics_rejected_even_if_both_parsers_agree(self):
        result,qc=projection(synthetic_sam());qc['15']['cryptic']['histograms']={}
        with self.assertRaises(ValueError):validate_histograms(qc,result['counts'])
    def test_missing_single_metric_rejected(self):
        result,qc=projection(synthetic_sam());del qc['15']['cryptic']['histograms']['AS']
        with self.assertRaises(ValueError):validate_histograms(qc,result['counts'])
    def test_extra_metric_rejected(self):
        result,qc=projection(synthetic_sam());qc['15']['cryptic']['histograms']['unknown']={'0':1}
        with self.assertRaises(ValueError):validate_histograms(qc,result['counts'])
    def test_negative_weights_cannot_cancel(self):
        result,qc=projection(synthetic_sam());qc['15']['cryptic']['histograms']['NM']={'0':2,'missing':-1}
        with self.assertRaises(ValueError):validate_histograms(qc,result['counts'])
    def test_boolean_weight_is_not_integer_count(self):
        result,qc=projection(synthetic_sam());qc['15']['cryptic']['histograms']['NM']={'0':True}
        with self.assertRaises(ValueError):validate_histograms(qc,result['counts'])
    def test_anchor_and_target_schema_rejected(self):
        result,qc=projection(synthetic_sam())
        for altered in (dict(qc,extra={}),dict(qc,**{'15':{'canonical':qc['15']['canonical']}})):
            with self.subTest(altered=tuple(altered)),self.assertRaises(ValueError):validate_histograms(altered,result['counts'])
    def test_empty_histograms_valid_only_for_zero_observations(self):
        from scripts.gse122069_pilot import empty_counts
        validate_histograms(empty_qc(),empty_counts())
