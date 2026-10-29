import gzip,tempfile,unittest
from pathlib import Path
from scripts.annotate_gencode_junctions import junction_keys,reference_lookup,classify

class GencodeJunctionTests(unittest.TestCase):
    def test_intronic_coordinates_minus_strand_and_dedup(self):
        self.assertEqual(junction_keys('G','chr1','-',[(21,30),(1,10),(1,10)]),{('G','chr1',11,20,'-')})
    def test_gene_locus_and_missing_are_separate(self):
        genes={'G':{'chrom':'chr1','strand':'+'}};key=('G','chr1',11,20,'+')
        self.assertEqual(classify(key,genes,{key:[]}), 'exact_same_gene_junction')
        self.assertEqual(classify(('G','chr1',11,20,'-'),genes,{key:[]}), 'gene_locus_discordant')
        self.assertEqual(classify(('H','chr1',11,20,'+'),genes,{key:[]}), 'gene_not_in_v47')
        self.assertEqual(classify(key,genes,{}),'junction_not_found_same_gene')
    def test_interleaved_reference_exons_are_grouped(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'r.gz'
            with gzip.open(p,'wt') as f:
                for tx,start,end in [('T1',1,10),('T2',2,10),('T1',21,30),('T2',21,35)]:f.write(f'chr1\ts\texon\t{start}\t{end}\t.\t+\t.\tgene_id "G"; transcript_id "{tx}";\n')
            _,lookup=reference_lookup(p,{'G'});self.assertEqual(set(lookup[('G','chr1',11,20,'+')]),{'T1','T2'})
    def test_overlap_rejected_and_adjacent_not_an_intron(self):
        with self.assertRaises(ValueError):junction_keys('G','chr1','+',[(1,10),(9,20)])
        self.assertEqual(junction_keys('G','chr1','+',[(1,10),(11,20)]),set())
