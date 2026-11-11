import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from stmn2_within_region import ranks,pearson,spearman,residual_correlation,partial,require_vector

class WithinRegionTests(unittest.TestCase):
    def test_linkage_fails_closed_without_reference_key(self):
        with self.assertRaises(ValueError):require_vector({('S','Cortex'):{'A':1}},'S','Spinal Cord')

    def test_average_tie_ranks(self):
        np.testing.assert_array_equal(ranks([9,1,1,5]),[4,1.5,1.5,3])
        with self.assertRaises(ValueError):ranks([1,float('nan')])
    def test_constant_is_undefined(self):
        self.assertIsNone(pearson([1,1,1],[1,2,3]))
        self.assertIsNone(spearman([1]*10,list(range(10))))
    def test_minimum_n_and_distinct_guards(self):
        row=dict(neuronal=.1,ratio=0,rin=7,total=30,prep='Manual KAPA Total')
        self.assertEqual(partial([row]*19)[1],'insufficient_n')
        self.assertEqual(partial([row]*20)[1],'insufficient_distinct_values')
    def test_singular_design_is_rejected(self):
        x=np.arange(10,dtype=float);design=np.ones((10,2))
        self.assertEqual(residual_correlation(x,x,design)[1],'singular_design')
    def test_confounding_is_removed(self):
        # Centered orthogonal contrasts: large shared nuisance drives raw correlation.
        z=np.array([-1,-1,-1,-1,1,1,1,1.]);u=np.array([-1,-1,1,1,-1,-1,1,1.]);v=np.array([-1,1,-1,1,-1,1,-1,1.])
        x=100*z+u;y=100*z+v;design=np.column_stack([np.ones(8),z])
        corr,status=residual_correlation(x,y,design)
        self.assertGreater(pearson(x,y),.99);self.assertEqual(status,'ok');self.assertAlmostEqual(corr,0,places=8)
    def test_known_negative_residual_relationship(self):
        z=np.arange(8,dtype=float);u=np.array([1,-1,1,-1,1,-1,1,-1.]);design=np.column_stack([np.ones(8),z])
        corr,status=residual_correlation(10*z+u,20*z-u,design)
        self.assertEqual(status,'ok');self.assertAlmostEqual(corr,-1)
    def test_zero_residual_variance_is_undefined(self):
        x=np.arange(8,dtype=float);design=np.column_stack([np.ones(8),x])
        self.assertEqual(residual_correlation(x,x,design)[1],'zero_residual_variance')

if __name__=='__main__':unittest.main()
