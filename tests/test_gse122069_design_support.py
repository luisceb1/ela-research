import json
from pathlib import Path
import unittest
from scripts.fetch_gse122069_growth_projection import project as growth
from scripts.plan_gse122069_remaining_resources import project as resources

ROOT=Path(__file__).resolve().parents[1]

class DesignSupportTests(unittest.TestCase):
    def body(self,gsm='GSM3454242'):
        return ('!Sample_geo_accession = '+gsm+'\n!Sample_source_name_ch1 = SH-SY5Y cell line\n!Sample_growth_protocol_ch1 = DMEM/F12 with 10% fetal-bovine serum and 1% penicillin-streptomycin at 37 °C and 5% CO2\n!Sample_contact_name = synthetic excluded value\n').encode()
    def test_growth_projection_is_technical_only(self):
        r=growth(self.body());self.assertEqual(r['growth_protocol_projection']['medium'],'DMEM/F12');self.assertEqual(r['growth_protocol_projection']['temperature_C'],37)
        self.assertNotIn('excluded',json.dumps(r));self.assertNotIn('!Sample_growth_protocol_ch1',r)
    def test_non_target_growth_record_rejected(self):
        with self.assertRaises(ValueError):growth(self.body('GSM9999999'))
    def test_partial_benchmark_cannot_generate_estimates(self):
        rows=json.loads((ROOT/'reports/gse122069-resource-plan/input_manifest.json').read_text())['rows']
        with self.assertRaises(ValueError):resources(rows,{'complete_library':False})
    def test_estimates_exclude_observed_control_and_never_claim_execution(self):
        rows=json.loads((ROOT/'reports/gse122069-resource-plan/input_manifest.json').read_text())['rows']
        observed={'complete_library':True,'reads':37518164,'run':'SRR8144907','watchdog_errors':[],'independent_parser_concordant':True,'elapsed_seconds':1000}
        estimates=resources(rows,observed);self.assertEqual(len(estimates),5)
        self.assertNotIn('SRR8144907',[r['run'] for r in estimates]);self.assertTrue(all(r['new_run_executed'] is False for r in estimates))
        self.assertGreater(estimates[-1]['linear_point_estimate_seconds_not_measured'],1000)

if __name__=='__main__':unittest.main()
