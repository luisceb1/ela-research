import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('unc_ref',Path(__file__).resolve().parents[1]/'scripts/unc13a_reference_contract.py')
ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)

class ReferenceGeometryTests(unittest.TestCase):
    def test_exonic_and_inclusive_labels_convert_to_same_span(self):
        self.assertEqual(ref.interval(17641556,17642414,'exonic1'),(17641556,17642413))
        self.assertEqual(ref.interval(17641557,17642413,'inclusive1'),(17641556,17642413))
    def test_off_by_one_breaks_motif(self):
        dna='AACTCCCCACGG'
        self.assertEqual(ref.motifs(dna,100,102,110),('CT','AC'))
        self.assertNotEqual(ref.motifs(dna,100,102,111),('CT','AC'))
    def test_outside_window_rejected(self):
        with self.assertRaises(ValueError):ref.motifs('ACGT',100,99,103)
    def test_sam_N_span_uses_contract_coordinates(self):
        import tempfile
        spec=importlib.util.spec_from_file_location('pe_for_ref',Path(__file__).resolve().parents[1]/'scripts/pe_fragment_contract.py')
        pe=importlib.util.module_from_spec(spec);spec.loader.exec_module(pe)
        a,b=ref.interval(17641556,17642845,'exonic1');pos=a-20+1
        sam='@SQ\tSN:chr19\tLN:60000000\n'
        for flag in (99,147):
            sam+='\t'.join(map(str,['q',flag,'chr19',pos,60,f'20M{b-a}N20M','=',pos,0,'A'*40,'I'*40,'NH:i:1','XS:A:-']))+'\n'
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'test.sam';p.write_text(sam)
            c,_=pe.count_fragments(pe.text_records(p,15),'synthetic')
        self.assertEqual(c,{('synthetic','chr19',a,b,'-'):1})

if __name__=='__main__':unittest.main()
