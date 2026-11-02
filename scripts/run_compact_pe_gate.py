"""Reproduce compact local controls and replay existing synthetic alignments."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import sys
import unittest


def run(report):
    import pysam
    if pysam.__version__!='0.23.3':raise ValueError('Pinned PySAM0.23.3 required')
    from compact_pe_pipeline import run as pipeline,DEFAULT_LIMITS
    report=Path(report);report.mkdir(parents=True,exist_ok=False)
    repo=Path(__file__).resolve().parents[1];sys.path.insert(0,str(repo/'tests'))
    import test_compact_pe_pipeline as compact_tests
    original=compact_tests.CompactTests.tearDown
    selected={'test_supervised_actual_pipe_success_and_nonzero_producer','test_supervised_blocked_pipe_kills_producer_and_consumer','test_offtarget_splice_strand_still_affects_qc','test_chunk_initial_runs_and_disk_caps','test_decoder_disagreement_rejected'}
    def capture(self):
        if self._testMethodName in selected:
            out=report/'cases'/self._testMethodName;out.mkdir(parents=True,exist_ok=True)
            for p in self.root.rglob('*'):
                if p.is_file() and p.suffix in ('.json','.log'):
                    dest=out/p.relative_to(self.root);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
            for p in self.root.rglob('run-*.jsonl'):
                with p.open('rb') as h:line=h.readline(65537)
                if line:
                    (out/'derived-row-example.json').write_text(json.dumps(json.loads(line.split(b'\t',2)[2]),indent=2)+'\n');break
        original(self)
    compact_tests.CompactTests.tearDown=capture
    patterns=['test_compact_pe_pipeline.py','test_pe_fragment_contract.py','test_pe_external_collation.py','test_archive_ledger_phase.py','test_artifact_checksum_transport.py','test_external_local_stage.py','test_http_read_reservation.py','test_paired_fastq_phase.py','test_paired_fastq_integrity.py','test_pilot_dry_runner.py','test_pilot_process_limits.py','test_bounded_http_transport.py']
    try:
        suite=unittest.TestSuite(unittest.defaultTestLoader.discover(str(repo/'tests'),pattern=p) for p in patterns)
        with (report/'tests.txt').open('w') as out:result=unittest.TextTestRunner(stream=out,verbosity=2).run(suite)
    finally:compact_tests.CompactTests.tearDown=original
    summary={'python':platform.python_version(),'pysam':pysam.__version__,'htslib_samtools':pysam.__samtools_version__,'patterns':patterns,'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'success':result.wasSuccessful(),'raw_execution_ready':False}
    (report/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
    if not result.wasSuccessful():return summary
    replay=[];limits={**DEFAULT_LIMITS,'chunk_bytes':4096,'max_row_bytes':4096,'merge_fan_in':2}
    for name in ('wild','multicopy','wrongstrand','wrongmotif'):
        source=compact_tests.FIXTURES/(name+'.sam')
        with source.open('rb') as inp:first=pipeline(inp,report/'replay'/name,'fixture',compact_tests.TARGETS,limits,lambda:0)
        with source.open('rb') as inp:second=pipeline(inp,report/'repeat'/name,'fixture',compact_tests.TARGETS,limits,lambda:0)
        if first!=second:raise ValueError('Replay not deterministic')
        replay.append({'fixture':name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'input_bytes':first['input_bytes'],'records':first['records'],'initial_runs':first['initial_runs'],'merge_passes':first['merge_passes'],'peak_temp_bytes':first['peak_temp_bytes'],'routes':first['routes'],'repeat_identical':True})
    (report/'replay-summary.json').write_text(json.dumps(replay,indent=2)+'\n')
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);r=run(p.parse_args().report);print(json.dumps(r,indent=2));raise SystemExit(not r['success'])
