"""Metadata comparisons only; no human alignment or inferred missing rows."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import compare_unc13a_inventory_annotation as mod
ROOT=Path(__file__).resolve().parents[1]

class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.input=json.loads((ROOT/'reports/unc13a-control-annotation-20261103/operator-console-summary.json').read_text())
        self.annotation=json.loads((ROOT/'reports/unc13a-reference-strand-20261102/sources/annotation.json').read_text())
    def test_observed_partial_inventory_matches_exactly_but_keeps_missing_rows(self):
        r=mod.compare(self.input,self.annotation)
        self.assertFalse(r['all_inventory_rows_available']);self.assertEqual(r['reference_distinct_junctions'],47)
        for route,missing in [('text15',10),('text8',12)]:
            self.assertEqual(r['routes'][route]['exact_cached_annotation_matches'],21)
            self.assertEqual(r['routes'][route]['unavailable_distinct_junctions'],missing)
        self.assertTrue(r['missing_rows_are_not_zero']);self.assertFalse(r['gate_promoted'])
    def test_duplicate_same_event_is_not_double_counted(self):
        data=self.input['routes']['text15'];data['top20_by_support'].append(copy.deepcopy(data['all_target_neighbors_within_2bp'][0]))
        r=mod.compare(self.input,self.annotation);self.assertEqual(r['routes']['text15']['available_distinct_junctions'],21)
        self.assertEqual(r['routes']['text15']['available_event_support_sum_not_unique_groups'],66)
    def test_conflicting_duplicate_support_is_rejected(self):
        data=self.input['routes']['text15'];row=copy.deepcopy(data['top20_by_support'][0]);row['fragments']+=1;data['top20_by_support'].append(row)
        self.assertRaises(ValueError,mod.compare,self.input,self.annotation)
    def test_one_base_shift_and_wrong_strand_are_not_annotated_exact_matches(self):
        for mutation in ('coordinate','strand'):
            j=copy.deepcopy(self.input);event=j['routes']['text15']['top20_by_support'][0]['event']
            if mutation=='coordinate':event[2]+=1
            else:event[3]='+'
            with self.subTest(mutation=mutation):self.assertEqual(mod.compare(j,self.annotation)['routes']['text15']['not_in_cached_annotation'],1)
    def test_invalid_count_inventory_size_or_window_rejected(self):
        for mutation in ('negative','bool','size','window','promote'):
            j=copy.deepcopy(self.input)
            if mutation in ('negative','bool'):j['routes']['text15']['top20_by_support'][0]['fragments']=-1 if mutation=='negative' else True
            elif mutation=='size':j['routes']['text15']['distinct_junctions']=1
            elif mutation=='window':j['window'][1]+=1
            else:j['gate_promoted']=True
            with self.subTest(mutation=mutation):self.assertRaises(ValueError,mod.compare,j,self.annotation)
    def test_wrong_reference_identity_rejected(self):
        self.annotation['genome']='hg19';self.assertRaises(ValueError,mod.compare,self.input,self.annotation)
    def test_full_fixture_shape_is_reported_complete_without_fabricating_junctions(self):
        j=copy.deepcopy(self.input);j.pop('console_inventory_is_summary');routes={}
        for route,data in j.pop('routes').items():routes[route]={'junctions':data['top20_by_support']+data['all_target_neighbors_within_2bp']}
        j['regional_audit']={'window':j.pop('window'),'routes':routes}
        r=mod.compare(j,self.annotation);self.assertTrue(r['all_inventory_rows_available'])
        self.assertEqual(r['routes']['text15']['reported_distinct_junctions'],21)
        self.assertEqual(r['routes']['text15']['unavailable_distinct_junctions'],0)
    def test_console_extraction_is_json_data_only(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'console.txt';p.write_text('PS> irrelevant commands\n'+json.dumps(self.input)+'\nPS>')
            self.assertEqual(mod.load_inventory(p),self.input)

if __name__=='__main__':unittest.main()
