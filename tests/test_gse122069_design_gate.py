import copy
import json
from pathlib import Path
import unittest
from scripts.gse122069_design_gate import project_xml, audit, validate_manifest

ROOT=Path(__file__).resolve().parents[1]

class DesignGateTests(unittest.TestCase):
    def setup_data(self):
        rows=json.loads((ROOT/'reports/gse122069-resource-plan/input_manifest.json').read_text())['rows'];sources=[]
        for i,r in enumerate(rows):
            sample='SRS'+str(100+i)
            sources += [{'accession':r['experiment'],'projection':{'title':r['gsm']+': '+r['published_group']+'; Homo sapiens; RNA-Seq','sample':sample,'layout':'SINGLE','technical_attributes':{}}},
                        {'accession':sample,'projection':{'sample_alias':r['gsm'],'primary_accession':'SAMN'+str(100+i),'technical_attributes':{'source name':'SH-SY5Y cell line','treatment':r['published_group'].rsplit(' ',1)[0]}}}]
        return rows,sources
    def test_secondary_accession_requires_explicit_identity(self):
        body=b'<SAMPLE_SET><SAMPLE accession="SAMN1" alias="GSM1"><IDENTIFIERS><PRIMARY_ID>SAMN1</PRIMARY_ID><SECONDARY_ID>SRS1</SECONDARY_ID></IDENTIFIERS></SAMPLE></SAMPLE_SET>'
        self.assertEqual(project_xml(body,'SAMPLE','SRS1')['primary_accession'],'SAMN1')
        with self.assertRaises(ValueError):project_xml(body,'SAMPLE','SRS2')
    def test_aliases_and_unique_accessions_never_establish_units(self):
        rows,sources=self.setup_data();r=audit(rows,sources,{'author_declared_n_per_condition':3})
        self.assertFalse(r['full_design_gate_pass']);self.assertFalse(r['explicit_all_library_units_documented'])
        self.assertFalse(r['independent_units_inferred_from_accessions_or_suffixes']);self.assertTrue(r['author_claim_three_biological_replicates_per_condition'])
        self.assertEqual(r['metadata_errors'],[])
    def test_assignment_without_real_evidence_reference_rejected(self):
        rows,sources=self.setup_data()
        with self.assertRaises(ValueError):audit(rows,sources,{'library_map':{rows[0]['gsm']:{'unit':'unit1','unit_evidence_source':'unknown'}}})
    def test_group_conflict_rejected(self):
        rows,sources=self.setup_data();sources[1]['projection']['technical_attributes']['treatment']='siTDP-43'
        with self.assertRaises(ValueError):audit(rows,sources,{})
    def test_duplicate_sources_rejected(self):
        rows,sources=self.setup_data()
        with self.assertRaises(ValueError):audit(rows,sources+[sources[0]],{})
    def test_duplicate_manifest_rejected(self):
        rows,sources=self.setup_data();rows[1]['run']=rows[0]['run']
        with self.assertRaises(ValueError):validate_manifest(rows)
    def test_allowlist_omits_non_technical_values(self):
        body=b'<SAMPLE_SET><SAMPLE accession="SAMN1" alias="GSM1"><SAMPLE_ATTRIBUTES><SAMPLE_ATTRIBUTE><TAG>source_name</TAG><VALUE>SH-SY5Y cell line</VALUE></SAMPLE_ATTRIBUTE><SAMPLE_ATTRIBUTE><TAG>contact</TAG><VALUE>synthetic excluded value</VALUE></SAMPLE_ATTRIBUTE><SAMPLE_ATTRIBUTE><TAG>diagnosis</TAG><VALUE>synthetic excluded value</VALUE></SAMPLE_ATTRIBUTE></SAMPLE_ATTRIBUTES></SAMPLE></SAMPLE_SET>'
        r=project_xml(body,'SAMPLE','SAMN1');self.assertEqual(r['technical_attributes'],{'source name':'SH-SY5Y cell line'});self.assertNotIn('excluded',json.dumps(r))
    def test_missing_metadata_keeps_gate_closed(self):
        rows,sources=self.setup_data();sources[1]={'accession':sources[1]['accession'],'error':'synthetic unavailable response'}
        r=audit(rows,sources,{});self.assertEqual(len(r['metadata_errors']),1);self.assertFalse(r['full_design_gate_pass'])
    def test_explicit_synthetic_map_can_pass_but_reagent_lot_cannot(self):
        rows,sources=self.setup_data();curated={'evidence_sources':{'synthetic_map':{'scope':'test fixture only'}},'library_map':{},'batch_structure_documented':True,'pairing_structure_documented':True,'batch_structure_evidence_source':'synthetic_map','pairing_structure_evidence_source':'synthetic_map'}
        for i,r in enumerate(rows):curated['library_map'][r['gsm']]={'unit':'unit'+str(i),'unit_evidence_source':'synthetic_map'}
        self.assertTrue(audit(rows,sources,curated)['full_design_gate_pass'])
        curated['library_map']={};curated['reagent_lot']='synthetic reagent lot'
        self.assertFalse(audit(rows,sources,curated)['full_design_gate_pass'])
    def test_layout_mismatch_rejected(self):
        rows,sources=self.setup_data();sources[0]['projection']['layout']='PAIRED'
        with self.assertRaises(ValueError):audit(rows,sources,{})

if __name__=='__main__':unittest.main()
