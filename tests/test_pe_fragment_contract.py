import importlib.util
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('pe_fragment_contract',Path(__file__).resolve().parents[1]/'scripts/pe_fragment_contract.py')
pe=importlib.util.module_from_spec(spec);spec.loader.exec_module(pe)

def pair(name='a',cigars=('20M100N20M','20M100N20M'),flags=(99,147),xs=('+','+'),mq=(60,60),nh=(1,1),rg='A',positions=(101,101)):
    lines=[]
    for i in range(2):
        import re
        n=sum(int(n) for n,op in re.findall(r'(\d+)([MIDNSHP=X])',cigars[i]) if op in 'MIS=X')
        tags=[f'NH:i:{nh[i]}',f'RG:Z:{rg}']
        if xs[i] is not None:tags.append('XS:A:'+xs[i])
        lines.append('\t'.join(map(str,[name,flags[i],'chr19',positions[i],mq[i],cigars[i],'=',positions[1-i],0,'A'*n,'I'*n]+tags)))
    return lines

def run(lines,anchor=15,backend='text',library='lib'):
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/'fixture.sam'
        path.write_text('@HD\tVN:1.6\tSO:unknown\n@SQ\tSN:chr19\tLN:100000\n@RG\tID:A\tSM:synthetic\n@RG\tID:B\tSM:synthetic\n'+'\n'.join(lines)+'\n')
        records=pe.text_records(path,anchor) if backend=='text' else pe.hts_records(path,anchor)
        return pe.count_fragments(records,library)

class PairedContractTests(unittest.TestCase):
    def test_both_mates_count_once(self):
        counts,qc=run(pair());self.assertEqual(counts,{('lib','chr19',120,220,'+'):1});self.assertEqual(qc['accepted_pairs'],1)
    def test_one_mate_and_negative_transcript(self):
        counts,_=run(pair(cigars=('20M100N20M','40M'),xs=('-',None)))
        self.assertEqual(counts,{('lib','chr19',120,220,'-'):1})
    def test_distinct_events_remain_distinct(self):
        counts,_=run(pair(cigars=('20M100N20M','25M100N15M')));self.assertEqual(len(counts),2)
    def test_anchor_primary_and_sensitivity(self):
        lines=pair(cigars=('14M100N26M','40M'))
        self.assertEqual(run(lines)[0],{});self.assertEqual(len(run(lines,8)[0]),1)
    def test_insertion_interrupts_anchor(self):
        self.assertEqual(run(pair(cigars=('20M1I100N20M','40M')))[0],{})
    def test_adjacent_match_blocks_form_contiguous_anchor(self):
        lines=pair(cigars=('10M10=100N10X10M','40M'))
        self.assertEqual(run(lines)[0],{('lib','chr19',120,220,'+'):1})
    def test_secondary_and_supplementary_not_extra_fragments(self):
        lines=pair()+pair(flags=(99|256,147|2048));c,q=run(lines)
        self.assertEqual(sum(c.values()),1);self.assertEqual(q['nonprimary_excluded'],2)
    def test_orphan_and_extra_primary(self):
        for lines in [pair()[:1],pair()+pair()[:1]]:self.assertEqual(run(lines)[0],{})
    def test_mapping_filters(self):
        for args in [{'mq':(19,60)},{'mq':(255,60)},{'nh':(2,1)},{'flags':(97,145)},{'flags':(99|512,147)}]:
            with self.subTest(args=args):self.assertEqual(run(pair(**args))[0],{})
    def test_strand_missing_or_conflicting(self):
        for xs in [(None,'+'),('+','-')]:self.assertEqual(run(pair(xs=xs))[0],{})
    def test_marked_duplicates_retained_and_labeled(self):
        c,q=run(pair(flags=(99|1024,147|1024)));self.assertEqual(sum(c.values()),1);self.assertEqual(q['accepted_marked_duplicate_pairs'],1)
    def test_rg_and_library_separation(self):
        self.assertEqual(sum(run(pair(rg='A')+pair(rg='B'))[0].values()),2)
        self.assertNotEqual(run(pair(),library='one')[0],run(pair(),library='two')[0])
    def test_wrong_order_and_group_cap_fail_closed(self):
        for lines in [pair('b')+pair('a'),pair()*9]:
            with self.assertRaises(ValueError):run(lines)
    def test_nonreciprocal_coordinates(self):
        lines=pair();f=lines[1].split('\t');f[7]='102';lines[1]='\t'.join(f)
        self.assertEqual(run(lines)[0],{})
    def test_wrong_orientation_and_read_roles(self):
        for args in [{'flags':(67,131)},{'flags':(99,99)},{'positions':(201,101)}]:
            self.assertEqual(run(pair(**args))[0],{})
    def test_explicit_library_required(self):
        with self.assertRaises(ValueError):run(pair(),library='')
    def test_htslib_independent_decode(self):
        try:import pysam
        except ImportError:self.skipTest('Pinned optional PySAM required for independent parsing')
        fixtures=[pair(),pair(cigars=('10M10=100N10X10M','40M')),pair(cigars=('20M100N20M','40M'),xs=('-',None)),pair(cigars=('14M100N26M','40M')),pair(cigars=('20M1I100N20M','40M')),pair(xs=('+','-')),pair(flags=(99|1024,147|1024)),pair()+pair(flags=(99|256,147|2048)),pair(rg='A')+pair(rg='B'),pair()[:1],pair(nh=(2,1))]
        for anchor in [15,8]:
            for lines in fixtures:
                with self.subTest(anchor=anchor,lines=lines):self.assertEqual(run(lines,anchor),run(lines,anchor,'hts'))

if __name__=='__main__':unittest.main()
