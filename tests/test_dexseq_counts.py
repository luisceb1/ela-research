import unittest
from scripts.audit_dexseq_counts import count,key,compare,unique_header

class CountAuditTests(unittest.TestCase):
    def test_invalid_counts(self):
        for s in ['-1','1.2','NA','NaN','inf','','1e3']:
            with self.subTest(s=s),self.assertRaises(ValueError):count(s)
    def test_zero_valid(self):self.assertEqual(count('0'),0)
    def test_namespace_conversion(self):self.assertEqual(key('ENSG00001:001',True),key('ENSG00001:E001'))
    def test_bad_namespace(self):
        with self.assertRaises(ValueError):key('ENSG00001:001')
    def test_mismatch_detected(self):self.assertEqual(compare((1,2,0),(1,3,0)),1)
    def test_header_collision(self):
        with self.assertRaises(ValueError):unique_header(['id','a','a'])

    def test_compound_group_preserved(self):
        self.assertEqual(key('ENSG01+ENSG02:001',True),key('ENSG01+ENSG02:E001'))
        self.assertNotEqual(key('ENSG01+ENSG02:E001'),key('ENSG02+ENSG01:E001'))
    def test_full_join_duplicate_annotation_and_conflict(self):
        import tempfile,gzip,json,contextlib,io
        from pathlib import Path
        from scripts.audit_dexseq_counts import run
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);a=p/'a.gz';b=p/'b.gz'
            with gzip.open(a,'wt') as f:f.write('id\tb\ta\nENSG01:001\t2\t1\n')
            with gzip.open(b,'wt') as f:f.write('fragment,groupID,featureID,countData.a,countData.b,entrez\nENSG01:E001,ENSG01,E001,1,2,10\nENSG01:E001,ENSG01,E001,1,2,20\nENSG01:E001,ENSG01,E001,9,2,20\n')
            with contextlib.redirect_stdout(io.StringIO()):run(a,b,p/'out')
            r=json.loads((p/'out/summary.json').read_text())
            self.assertEqual(r['discordant_cells'],0)
            self.assertEqual(r['duplicate_annotation_variant_rows'],1)
            self.assertEqual(r['duplicate_count_conflicts'],1)
            self.assertEqual(r['compared_cells'],2)
