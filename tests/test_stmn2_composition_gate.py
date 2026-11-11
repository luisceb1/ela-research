import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from stmn2_composition_gate import validate_vectors

class CompositionGateTests(unittest.TestCase):
    def rows(self,values=(.2,.8),labels=('A','B'),sample='S',tissue='T'):
        return [dict(Sample=sample,tissue=tissue,estimate=str(v),**{'cell type':label}) for label,v in zip(labels,values)]
    def test_simplex_and_zero_accepted(self):
        accepted,bad,taxa=validate_vectors(self.rows((0,1)))
        self.assertEqual(accepted[('S','T')],{'A':0,'B':1})
        self.assertEqual(bad,{'incomplete_taxonomy':0})
    def test_duplicate_cell_type_rejected(self):
        accepted,bad,_=validate_vectors(self.rows(labels=('A','A')))
        self.assertFalse(accepted);self.assertEqual(bad['duplicate_cell_type_keys'],1)
    def test_nonfinite_negative_large_and_sum_fail(self):
        for values in [(float('nan'),1),(-.1,1.1),(2,0),(.2,.2)]:
            accepted,bad,_=validate_vectors(self.rows(values))
            self.assertFalse(accepted)
            self.assertTrue(any(v for v in bad.values()))
    def test_reference_taxonomies_remain_separate(self):
        accepted,bad,taxa=validate_vectors(self.rows()+self.rows(labels=('X','Y'),tissue='U'))
        self.assertEqual(len(accepted),2)
        self.assertNotEqual(taxa['T'],taxa['U'])
    def test_incomplete_vector_rejected_even_if_sum_one(self):
        rows=self.rows()+self.rows(values=(1,),labels=('A',),sample='OTHER')
        accepted,bad,_=validate_vectors(rows)
        self.assertNotIn(('OTHER','T'),accepted)
        self.assertEqual(bad['incomplete_taxonomy'],1)

if __name__=='__main__':unittest.main()
