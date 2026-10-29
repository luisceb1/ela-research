import unittest,json
from scripts.audit_functional_evidence import validate,ROOT
class EvidenceTests(unittest.TestCase):
 def rows(self):return json.loads((ROOT/'research/functional_evidence.json').read_text())
 def test_curated_matrix_consistent(self):self.assertEqual(len(validate(self.rows())),5)
 def test_concurrent_cannot_be_promoted_to_delayed(self):
  r=self.rows();r[2]['timing']='delayed'
  with self.assertRaises(ValueError):validate(r)
 def test_cells_cannot_be_promoted_to_clinical_efficacy(self):
  r=self.rows();r[0]['clinical_efficacy']=True
  with self.assertRaises(ValueError):validate(r)
 def test_duplicate_units_rejected(self):
  r=self.rows();r.append(r[0])
  with self.assertRaises(ValueError):validate(r)
