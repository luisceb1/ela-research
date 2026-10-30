import unittest
from scripts.audit_shsy5y_junction_map import parse_sheet,integer,star_to_flanks,bam_alias,condition,exact_link

class SHSY5YMapTests(unittest.TestCase):
    def header(self):return ['chromosome','start','end','name','score_left_blank_for_bed_format','strand']
    def test_nbsp_and_blank_source_row(self):
        r=parse_sheet([self.header(),['chr8\xa0','10\xa0','20','test\xa0','0','+'],['']*6])
        self.assertEqual(r[0]['left_boundary'],10);self.assertEqual(r[0]['name'],'test');self.assertEqual(r[0]['sheet_row'],2)
    def test_duplicate_names_fail(self):
        r=['chr8','10','20','same','0','+']
        with self.assertRaises(ValueError):parse_sheet([self.header(),r,r])
    def test_integer_types_and_invalid_values(self):
        self.assertEqual(integer(10.0),10)
        for x in [1.5,float('nan'),'10.5','bad']:
            with self.assertRaises(ValueError):integer(x)
    def test_star_flanking_boundaries_not_standard_bed(self):
        self.assertEqual(star_to_flanks(101,199),(100,200))
        with self.assertRaises(ValueError):star_to_flanks(1,2)
    def test_exact_submitted_filename_rule(self):
        self.assertEqual(bam_alias('run/ERR0/CTR07.Aligned.sorted.out.bam'),'CTR07')
        with self.assertRaises(ValueError):bam_alias('CTR07.bam')
    def test_condition_requires_exact_public_alias(self):
        self.assertEqual(condition('SHSY5YControl1'),'control')
        self.assertEqual(condition('SHSY5YTDP43KD3'),'TDP-43 KD')
        with self.assertRaises(ValueError):condition('SKNDZControl1')
    def fixture(self):
        cs=[];es=[];m={}
        for group,c in [('Control','control'),('TDP43KD','TDP-43 KD')]:
            for i in range(1,4):
                alias=group+str(i);run='ERR'+alias
                cs.append(dict(sample=alias,condition=c));es.append(dict(run_accession=run,study_accession='PRJEB42763',sample_alias='SHSY5Y'+alias,sample_accession='S'+alias,experiment_accession='X'+alias));m[run]=alias
        return cs,es,m
    def test_order_does_not_map_and_unknown_alias_fails(self):
        c,e,m=self.fixture();self.assertEqual(exact_link(c,e,m),exact_link(c,list(reversed(e)),m))
        c[0]['sample']='similar_but_not_exact'
        with self.assertRaises(ValueError):exact_link(c,e,m)
    def test_duplicate_run_or_condition_conflict_rejected(self):
        c,e,m=self.fixture();e.append(e[0])
        with self.assertRaises(ValueError):exact_link(c,e,m)
        c,e,m=self.fixture();c[0]['condition']='TDP-43 KD'
        with self.assertRaises(ValueError):exact_link(c,e,m)
