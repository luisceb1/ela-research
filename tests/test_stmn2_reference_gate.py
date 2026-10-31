import hashlib
import json
import unittest
from pathlib import Path
from scripts.audit_stmn2_reference_gate import audit, slice_genomic


class ReferenceGateTests(unittest.TestCase):
    def setUp(self):
        p=Path(__file__).resolve().parents[1]/'reports/stmn2-reference-gate-20261031/reference_inputs.json'
        self.bundle=json.loads(p.read_text())

    def test_real_reference_replay(self):
        r=audit(self.bundle)
        self.assertEqual([s['motif'] for s in r['sites']], ['GT','AG','AG'])
        self.assertFalse(r['pilot_ready'])
        self.assertFalse(r['full_fasta_verified'])
        self.assertEqual(r['raw_reads_processed'],0)

    def test_tampered_raw_payload(self):
        self.bundle['records']['ucsc_donor']['body']+=' '
        with self.assertRaises(ValueError): audit(self.bundle)

    def test_assembly_rejected(self):
        self.bundle['assembly_projection']['default_coord_system_version']='GRCh37'
        with self.assertRaises(ValueError): audit(self.bundle)

    def test_chromosome_length_rejected(self):
        self.bundle['chromosome8']['length']-=1
        with self.assertRaises(ValueError): audit(self.bundle)

    def test_provider_disagreement_even_valid_hash(self):
        r=self.bundle['records']['ensembl_canonical'];r['body']='A'*16
        r['sha256']=hashlib.sha256(r['body'].encode()).hexdigest()
        with self.assertRaises(ValueError): audit(self.bundle)

    def test_coordinate_rejected_even_valid_hash(self):
        r=self.bundle['records']['ucsc_donor'];d=json.loads(r['body']);d['start']+=1
        r['body']=json.dumps(d);r['sha256']=hashlib.sha256(r['body'].encode()).hexdigest()
        with self.assertRaises(ValueError): audit(self.bundle)

    def test_request_coordinates_rejected(self):
        self.bundle['records']['ensembl_cryptic']['url']='https://rest.ensembl.org/sequence/region/human/8:1..16:1'
        with self.assertRaises(ValueError): audit(self.bundle)

    def test_shifted_controls_not_reoptimized(self):
        for r in audit(self.bundle)['sites']:
            self.assertEqual(r['offset_controls']['0'], r['motif'])
            self.assertNotEqual(r['offset_controls']['-1'], r['motif'])
            self.assertNotEqual(r['offset_controls']['1'], r['motif'])

    def test_window_range_guard(self):
        for start,end in [(-1,1),(0,5),(3,2)]:
            with self.subTest(start=start,end=end), self.assertRaises(ValueError):
                slice_genomic('ACGT',0,start,end)


if __name__=='__main__': unittest.main()
