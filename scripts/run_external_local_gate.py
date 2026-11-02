"""Run local supervision controls and retain only JSON/log evidence, no reads."""
import argparse
import json
from pathlib import Path
import platform
import shutil
import sys
import unittest


def run(report):
    report=Path(report);report.mkdir(parents=True,exist_ok=False)
    repo=Path(__file__).resolve().parents[1]
    sys.path.insert(0,str(repo/'tests'))
    import test_external_local_stage as ext
    original=ext.ExternalTests.tearDown
    def capture(self):
        out=report/'cases'/self._testMethodName;out.mkdir(parents=True,exist_ok=True)
        for p in self.root.rglob('*'):
            if p.is_file() and p.suffix in ('.json','.log'):
                dest=out/p.relative_to(self.root);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        original(self)
    ext.ExternalTests.tearDown=capture
    patterns=['test_external_local_stage.py','test_http_read_reservation.py','test_paired_fastq_phase.py','test_paired_fastq_integrity.py','test_pilot_dry_runner.py','test_pilot_process_limits.py','test_bounded_http_transport.py']
    try:
        suite=unittest.TestSuite(unittest.defaultTestLoader.discover(str(repo/'tests'),pattern=p) for p in patterns)
        with (report/'tests.txt').open('w') as out:result=unittest.TextTestRunner(stream=out,verbosity=2).run(suite)
    finally:ext.ExternalTests.tearDown=original
    summary={'python':platform.python_version(),'patterns':patterns,'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'success':result.wasSuccessful(),'raw_execution_ready':False}
    (report/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
    records=[]
    for case in sorted((report/'cases').iterdir()):
        entry={'case':case.name}
        receipts=list(case.glob('external-receipts/*.outcome.json'))
        if receipts:
            outcome=json.loads(receipts[0].read_text());entry['outcome']=outcome
            rec=json.loads((receipts[0].parent/outcome['external_receipt']).read_text())
            entry.update({k:rec.get(k) for k in ['exit_code','violation','elapsed_seconds','max_group_members','live_group_members_after_cleanup']})
        if (case/'ledger.json').exists():
            ledger=json.loads((case/'ledger.json').read_text());entry.update({k:ledger[k] for k in ['deadline_epoch','transfer_bytes_consumed']})
        records.append(entry)
    (report/'case-summary.json').write_text(json.dumps(records,indent=2)+'\n')
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True)
    result=run(p.parse_args().report);print(json.dumps(result,indent=2));raise SystemExit(not result['success'])
