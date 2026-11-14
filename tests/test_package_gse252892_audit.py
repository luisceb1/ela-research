"""Audit packaging excludes sequencing/alignment bytes and preserves source metadata."""
from pathlib import Path
import json,sys,tempfile,unittest,zipfile
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import package_gse252892_audit as m

class AuditTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.root=Path(tmp.name)
        self.roots=[self.root/f'run{i}' for i in range(1,7)]
        for d in self.roots:
            d.mkdir()
            for name in ['accepted.json','supervision.json','transfer-ledger.json']:(d/name).write_text('{}')
        self.run=self.roots[-1];self.out=self.root/'audit.zip';self.plan=self.root/'final-plan.json';self.prev=self.root/'previous-plan.json';self.prev.write_text('{}');prev_sha=m.sha(self.prev.read_bytes())
        base=self.root/'base.json';base.write_text('{}')
        self.plan.write_text(json.dumps({'run_root':str(self.run),'base_path':str(base),'base_sha256':m.sha(base.read_bytes()),'lineage':{'prior_roots':[str(p) for p in self.roots[:-1]],'prior_plan_path':str(self.prev),'prior_plan_sha256':prev_sha}}));self.plan_sha=m.sha(self.plan.read_bytes())
        for p,sha in [(self.prev,prev_sha),(self.plan,self.plan_sha)]:Path(str(p)+'.claimed.json').write_text(json.dumps({'plan_sha256':sha,'transfer_bytes':14000000000}))
        pat=patch.object(m,'PLAN_SHA',self.plan_sha);pat.start();self.addCleanup(pat.stop)
        result=json.loads((ROOT/'reports/gse252892-local-result-20261114/user-reported-result.json').read_text());(self.run/'result.json').write_text(json.dumps(result))
        self.ledger={'active_requests':[],'actual_body_bytes':13000000000,'body_upper_bound_bytes':13000001000};(self.run/'transfer-ledger.json').write_text(json.dumps(self.ledger))
        self.sup={'status':'completed','failure':None,'cleanup_error':None,'plan_sha256':self.plan_sha};(self.run/'supervision.json').write_text(json.dumps(self.sup))
        for lib in result['libraries']:
            d=self.run/lib['gsm'];d.mkdir();(d/'junction-counts.json').write_text(json.dumps(lib));(d/'fastp.json').write_text('{}')
            (d/'raw.fastq.gz').write_bytes(b'RAW-MUST-NOT-ENTER');(d/'alignment.sam').write_bytes(b'SAM-MUST-NOT-ENTER');(d/'trimmed_1.fq').write_bytes(b'TRIMMED-MUST-NOT-ENTER')
            (d/'raw.fastq.gz.verified.json').write_text('{"recorded_hash":"fixture"}')
        (self.roots[0]/'worker-failure.json').write_text('{"error":"prior failed attempt"}')
    def run_package(self):return m.package(self.plan,self.out)
    def test_metadata_only_sources_unchanged_archive_hashes_verified(self):
        before={str(p):p.read_bytes() for d in self.roots for p in d.rglob('*') if p.is_file()}
        summary=self.run_package();manifest=m.verify_archive(self.out)
        self.assertEqual(summary['status'],'metadata_archive_verified');self.assertFalse(summary['raw_inputs_included']);self.assertEqual(summary['sources_deleted'],0)
        self.assertEqual(before,{str(p):p.read_bytes() for d in self.roots for p in d.rglob('*') if p.is_file()})
        names=[r['member'] for r in manifest['files']]
        self.assertIn('runs/01/worker-failure.json',names);self.assertTrue(any(n.endswith('.verified.json') for n in names))
        self.assertFalse(any(n.endswith(('.fastq.gz','.sam','.fq')) for n in names))
    def test_wrong_completed_proposal_refused(self):
        self.plan.write_text('{}')
        with self.assertRaisesRegex(ValueError,'exact completed'):self.run_package()
    def test_changed_result_requires_review(self):
        (self.run/'result.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'counts/QC differ'):self.run_package()
    def test_per_library_disagreement_refused(self):
        (self.run/'GSM8009878'/'junction-counts.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'Per-library'):self.run_package()
    def test_source_symlink_refused(self):
        p=self.run/'GSM8009878'/'fastp.json';p.unlink();p.symlink_to(self.plan)
        with self.assertRaisesRegex(ValueError,'Symlink'):self.run_package()
    def test_metadata_cap_enforced(self):
        with patch.object(m,'MAX_TOTAL',1):
            with self.assertRaisesRegex(ValueError,'budget'):self.run_package()
        self.assertFalse(self.out.exists())
    def test_existing_archive_never_overwritten(self):
        self.out.write_bytes(b'keep')
        with self.assertRaisesRegex(ValueError,'no overwrite'):self.run_package()
        self.assertEqual(self.out.read_bytes(),b'keep')
    def test_final_accounting_above_cap_refused(self):
        self.ledger['body_upper_bound_bytes']=14000000001;(self.run/'transfer-ledger.json').write_text(json.dumps(self.ledger))
        with self.assertRaisesRegex(ValueError,'accounting'):self.run_package()
    def test_bad_consumed_claim_refused(self):
        Path(str(self.prev)+'.claimed.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'claim'):self.run_package()
    def test_archive_corruption_detected(self):
        self.run_package()
        with zipfile.ZipFile(self.out) as z:members={n:z.read(n) for n in z.namelist()}
        name=next(n for n in members if n!='MANIFEST.json');members[name]=b'changed'
        bad=self.root/'bad.zip'
        with zipfile.ZipFile(bad,'w') as z:
            for n,b in members.items():z.writestr(n,b)
        with self.assertRaisesRegex(ValueError,'digest'):m.verify_archive(bad)
