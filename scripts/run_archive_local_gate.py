"""Run synthetic archive/checksum controls, retaining selected JSON/log receipts."""
import argparse
import json
from pathlib import Path
import platform
import shutil
import sys
import unittest


def run(report):
    report=Path(report);report.mkdir(parents=True,exist_ok=False)
    repo=Path(__file__).resolve().parents[1];sys.path.insert(0,str(repo/'tests'))
    import test_archive_ledger_phase as archive_tests
    original=archive_tests.ArchiveTests.tearDown
    selected={'test_success_reopen_preserves_budget_deadline_and_files','test_sha_only_http_to_archive_and_cached_reuse','test_crc_corruption_after_complete_members_rejected','test_pax_header_rejected_without_loading_declared_payload','test_hard_external_timeout_keeps_started_and_partials'}
    def capture(self):
        if self._testMethodName in selected:
            out=report/'cases'/self._testMethodName;out.mkdir(parents=True,exist_ok=True)
            (out/'fixture-contract.json').write_text(json.dumps({'manifest':self.manifest,'limits':self.limits,'raw_tar_bytes':len(self.raw),'compressed_bytes':len(self.blob),'scope':'synthetic only; regenerate from test fixture'},indent=2)+'\n')
            for p in self.root.rglob('*'):
                if p.is_file() and p.suffix in ('.json','.log'):
                    dest=out/p.relative_to(self.root);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        original(self)
    archive_tests.ArchiveTests.tearDown=capture
    patterns=['test_archive_ledger_phase.py','test_artifact_checksum_transport.py','test_external_local_stage.py','test_http_read_reservation.py','test_paired_fastq_phase.py','test_paired_fastq_integrity.py','test_pilot_dry_runner.py','test_pilot_process_limits.py','test_bounded_http_transport.py']
    try:
        suite=unittest.TestSuite(unittest.defaultTestLoader.discover(str(repo/'tests'),pattern=p) for p in patterns)
        with (report/'tests.txt').open('w') as out:result=unittest.TextTestRunner(stream=out,verbosity=2).run(suite)
    finally:archive_tests.ArchiveTests.tearDown=original
    summary={'python':platform.python_version(),'patterns':patterns,'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'success':result.wasSuccessful(),'raw_execution_ready':False}
    (report/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);result=run(p.parse_args().report);print(json.dumps(result,indent=2));raise SystemExit(not result['success'])
