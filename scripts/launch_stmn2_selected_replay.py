#!/usr/bin/env python3
"""One launch after same-source restoration; no retries or budget changes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/stmn2-control2-target-qc-20261101'


def launch():
    os.chdir(ROOT);start=time.monotonic()
    receipt=OUT/'restore-fastq-download.json';ready=OUT/'restore-fastq-verified.json'
    while not ready.exists():
        if receipt.exists() and not json.loads(receipt.read_text()).get('verified'):raise RuntimeError('Restoration failed; replay not started')
        if time.monotonic()-start>1900:raise TimeoutError('Restoration wait ended; no replay or retry')
        print('Waiting for frozen FASTQ restoration; replay not started',flush=True);time.sleep(30)
    assert json.loads(ready.read_text())['same_previously_processed_file_sha256']
    assert json.loads((OUT/'restore-index-verified.json').read_text())['all9_members_identical']
    assert json.loads((OUT/'preflight/preflight.json').read_text())['status']=='passed'
    manifest=json.loads((OUT/'execution-code-manifest.json').read_text())
    for path,item in manifest['files'].items():
        if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Frozen execution module changed: '+path)
    command=json.loads((OUT/'replay-command.json').read_text())
    print('Launching ONE fixed selected replay, 600s budget including identity checks',flush=True)
    with (OUT/'replay-progress.txt').open('w') as log,(OUT/'replay-stderr.txt').open('w') as err:
        done=subprocess.run(command,stdout=log,stderr=err)
    (OUT/'launch-result.json').write_text(json.dumps({'returncode':done.returncode,'automatic_retries':0,
      'command_record':'replay-command.json','execution_code_commit':manifest['code_commit'],
      'restoration_wait_included_in_replay_clock':False,'phase_limit_seconds':600},indent=2)+'\n')
    if done.returncode:raise RuntimeError('Selected replay failed; preserve error, no retry')
    print('Selected replay exited0; result still requires artifact verification',flush=True)


if __name__=='__main__':launch()
