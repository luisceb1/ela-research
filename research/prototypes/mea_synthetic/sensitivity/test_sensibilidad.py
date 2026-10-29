import unittest
import numpy as np
from analisis_sensibilidad import Config,simulate_once,plan,SCENARIOS

class SensitivityTests(unittest.TestCase):
    def test_seed_reproducibility(self):
        a=simulate_once(Config(),'clear_recovery',57)
        b=simulate_once(Config(),'clear_recovery',57)
        self.assertEqual(a,b)
    def test_biological_units(self):
        for config in plan():
            z=simulate_once(config,'none',13)
            self.assertLessEqual(z['n_analyzable_blocks'],config.n_diffs)
            self.assertLessEqual(z['randomized_wells'],config.n_diffs*config.n_candidate)
            self.assertEqual(z['randomized_wells']%2,0)
            self.assertGreaterEqual(z['eligible_wells'],z['randomized_wells'])
    def test_strong_effect_not_weaker_than_null_in_same_seed(self):
        cfg=Config()
        # diagnostic, not a formal proof of the classification algorithm
        for seed in range(15):
            none=simulate_once(cfg,'none',seed)
            strong=simulate_once(cfg,'clear_recovery',seed)
            self.assertGreater(strong['mean_effect_3'],none['mean_effect_3'])
    def test_scenarios_have_clear_labelling(self):
        self.assertEqual(len(SCENARIOS),4)
        self.assertEqual(len(plan()),9)
        self.assertEqual(SCENARIOS['none'],(0,0))
    def test_composites_mortality_not_technical_failure(self):
        c=Config(mortality_hazard=.15,technical_missing=0)
        z=simulate_once(c,'clear_recovery',23)
        self.assertGreater(z['death_observations'],0)
        self.assertEqual(z['technical_missing'],0)

if __name__=='__main__':unittest.main()
