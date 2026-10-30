import copy
import csv
import json
import unittest
from pathlib import Path
from scripts.inventory_junction_sources import source_group,ready,validate,inspect,COUNTS

class JunctionInventoryTests(unittest.TestCase):
    def row(self):return dict(file_inspected=True,junction_fields_verified=True,coordinate_link_verified=True,unit_map_verified=True,independent_units_verified=True,editorial_identity_verified=True,reused=False,clinical_data_used=False,ready_for_external_reanalysis=True)
    def test_complete_contract_positive(self):self.assertTrue(ready(validate(self.row())))
    def test_uninspected_or_unknown_units_not_ready(self):
        for k in ['file_inspected','coordinate_link_verified','unit_map_verified','independent_units_verified','editorial_identity_verified']:
            r=self.row();r[k]=False
            with self.assertRaises(ValueError):validate(r)
    def test_reuse_cannot_be_independence(self):
        r=self.row();r['reused']=True
        with self.assertRaises(ValueError):validate(r)
    def test_clinical_rejected(self):
        r=self.row();r['clinical_data_used']=True
        with self.assertRaises(ValueError):validate(r)
    def test_genotype_suffix_not_propagated(self):
        self.assertEqual(source_group('SH-SY5Y \\n C/C'),'SH-SY5Y')
        self.assertEqual(source_group('iPSC Neurons \n C/G'),'iPSC Neurons')
    def test_missing_flag_cannot_be_ready(self):
        r=self.row();r.pop('unit_map_verified')
        self.assertFalse(ready(r))
    def fixture(self):
        groups=[];rows=[]
        for label,c,k in [('A',3,3),('B',11,6),('C',3,3),('D',3,3),('E',4,3)]:
            groups.append(dict(source_label=label,control=c,KD=k,reused_units='not_verified',published_accession='PUBLIC',identity_status='culture_group_published'))
            for condition,n in [('control',c),('TDP-43 KD',k)]:
                for i in range(n):rows.append(dict(sample=f'{label}_{condition}_{i}',source=label,condition=condition,**{x:'0' for x in COUNTS}))
        return rows,groups
    def test_negative_fractional_counts_and_unknown_groups_rejected(self):
        for bad in ['-1','0.5','NaN']:
            rows,groups=self.fixture();rows[0][COUNTS[0]]=bad
            with self.assertRaises(ValueError):inspect(rows,groups)
        rows,groups=self.fixture();rows[0]['source']='UNKNOWN'
        with self.assertRaises(ValueError):inspect(rows,groups)
    def test_duplicate_alias_rejected_and_counts_are_not_bioreplicates(self):
        rows,groups=self.fixture();self.assertEqual(len(inspect(rows,groups)),5)
        rows[1]['sample']=rows[0]['sample']
        with self.assertRaises(ValueError):inspect(rows,groups)
