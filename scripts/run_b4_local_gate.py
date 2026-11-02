"""Run B4 synthetic controls and retain bounded JSON/log receipts; no data fetch."""
import argparse
import json
from pathlib import Path
import platform
import shutil
import sys
import unittest


def run(report):
    import pysam
    if pysam.__version__!='0.23.3':raise ValueError('Pinned PySAM required')
    report=Path(report);report.mkdir(parents=True,exist_ok=False);repo=Path(__file__).resolve().parents[1];sys.path.insert(0,str(repo/'tests'))
    import test_b4_ledger_policy as tests
    original=tests.CompactLedgerTests.tearDown
    selected={'test_success_reuse_preserves_state_and_insufficient_coverage_stops_next_phase','test_coverage_union_counts_group_once_for_two_targets','test_supervised_local_worker_records_policy_resources','test_parent_enforces_subphase_when_child_is_blocked'}
    def capture(self):
        if self._testMethodName in selected:
            out=report/'cases'/self._testMethodName;out.mkdir(parents=True,exist_ok=True)
            (out/'fixture-contract.json').write_text(json.dumps({'manifest':self.manifest,'limits':self.limits},indent=2)+'\n')
            for p in self.root.rglob('*'):
                if p.is_file() and p.suffix in ('.json','.log'):
                    dest=out/p.relative_to(self.root);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        original(self)
    tests.CompactLedgerTests.tearDown=capture
    patterns=['test_b4_ledger_policy.py','test_compact_pe_pipeline.py','test_pe_fragment_contract.py','test_pe_external_collation.py','test_process_supervisor_v2.py','test_archive_ledger_phase.py','test_artifact_checksum_transport.py','test_external_local_stage.py','test_http_read_reservation.py','test_paired_fastq_phase.py','test_paired_fastq_integrity.py','test_pilot_dry_runner.py','test_pilot_process_limits.py','test_bounded_http_transport.py']
    try:
        suite=unittest.TestSuite(unittest.defaultTestLoader.discover(str(repo/'tests'),pattern=p) for p in patterns)
        with (report/'tests.txt').open('w') as out:result=unittest.TextTestRunner(stream=out,verbosity=2).run(suite)
    finally:tests.CompactLedgerTests.tearDown=original
    summary={'python':platform.python_version(),'pysam':pysam.__version__,'samtools_version':pysam.__samtools_version__,'patterns':patterns,'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'success':result.wasSuccessful(),'raw_execution_ready':False}
    (report/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);r=run(p.parse_args().report);print(json.dumps(r,indent=2));raise SystemExit(not r['success'])
