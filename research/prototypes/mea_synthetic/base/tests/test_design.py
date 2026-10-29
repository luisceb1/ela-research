import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import pandas as pd
from mea_pipeline import simulate_pre,detect_eligibility,randomize_by_block,complete_simulation,add_baseline_adjustment,well_level_endpoints,summary_by_scenario
from analizar_csv_estandarizado import validate

class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results={}
        for k,sc in enumerate(['recovery','protection_only','null_effect']):
            pre,rng=simulate_pre(sc,20261029+k*1000,n_diffs=8,n_candidate=12)
            d=randomize_by_block(detect_eligibility(pre),rng)
            full=add_baseline_adjustment(complete_simulation(pre,d,rng,sc))
            e=well_level_endpoints(full)
            summ=summary_by_scenario(e,B=400)
            cls.results[sc]=(pre,d,full,e,summ)

    def test_eligibility_precedes_treatment(self):
        for pre,d,full,e,summary in self.results.values():
            assigned=d[d.arm.isin(['late_ASO','damage_control'])]
            self.assertTrue((assigned.t0_index>=5).all())
            self.assertTrue((assigned.t0_index<=6).all())
            self.assertTrue((assigned.eligible==1).all())
            self.assertTrue((assigned.deficit_t0>=0.19).all())
            self.assertTrue((full[(full.arm=='late_ASO')&(full.relative_to_t0<=0)].status=='observed').all())

    def test_randomization_balance_by_stratum(self):
        for pre,d,full,e,summary in self.results.values():
            arms=d[d.arm.isin(['late_ASO','damage_control'])]
            counts=arms.groupby(['differentiation_id','t0_index','arm']).size().unstack(fill_value=0)
            self.assertTrue((counts.late_ASO==counts.damage_control).all())

    def test_well_not_electrode_is_analysis_unit(self):
        for pre,d,full,e,summary in self.results.values():
            randomized=d[d.arm.isin(['late_ASO','damage_control'])]
            self.assertEqual(len(e),len(randomized))
            self.assertEqual(e.well_id.nunique(),len(e))
            self.assertTrue((e.groupby('well_id').size()==1).all())

    def test_scenarios_separated(self):
        self.assertIn('recuperación',self.results['recovery'][-1].classification.iloc[0])
        self.assertIn('sin recuperación',self.results['protection_only'][-1].classification.iloc[0])
        self.assertIn('sin evidencia',self.results['null_effect'][-1].classification.iloc[0])

    def test_mortality_not_excluded(self):
        for pre,d,full,e,summary in self.results.values():
            died=e[e.death_f3]
            self.assertTrue(len(died)>0)
            self.assertTrue(died.change_f3.notna().all())

    def test_duplication_not_allowed(self):
        full=self.results['recovery'][2].drop(columns=['scenario','composite_synchrony','adjusted_composite','adjusted_observed','relative_to_t0','age_expected'])
        validate(full)
        bad=pd.concat([full,full.iloc[[0]]],ignore_index=True)
        with self.assertRaisesRegex(ValueError,'Duplicated'):validate(bad)

if __name__=='__main__':unittest.main()
