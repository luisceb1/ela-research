#!/usr/bin/env python3
"""Controlled synthetic SAM against actual installed HTSlib; no real source opened."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.gse122069_full_control import save
from tests.test_stmn2_selected_replay import synthetic_sam,projection


def run(out,python):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    sam=synthetic_sam();own,qc=projection(sam);projections=[]
    for i in range(2):
        dest=out/f'synthetic-htslib-{i+1}.json'
        cmd=[python,'scripts/replay_stmn2_control2_qc.py','htslib','--out',str(dest),'--max-reads','10','--bin-size','3']
        done=subprocess.run(cmd,input=sam,text=True,capture_output=True,timeout=30)
        (out/f'synthetic-worker-{i+1}.stderr.txt').write_text(done.stderr)
        if done.returncode:raise RuntimeError(done.stderr)
        other=json.loads(dest.read_text())
        for key in ('reads','sam_records','counts','completed_bins'):
            if own[key]!=other[key]:raise ValueError('Synthetic independent count mismatch: '+key)
        if qc!=other['target_qc_histograms']:raise ValueError('Synthetic independent histograms mismatch')
        if other['complete_library'] or not other['complete_query_stream']:raise ValueError('Wrong synthetic completion scope')
        projections.append({key:other[key] for key in ('reads','sam_records','counts','completed_bins','target_qc_histograms','pysam','htslib')})
    if projections[0]!=projections[1]:raise ValueError('Repeated synthetic projection differs')
    save(out/'preflight.json',{'status':'passed','synthetic_queries':10,'biological_replicates_added':0,'python':platform.python_version(),
         'sam_sha256':hashlib.sha256(sam.encode()).hexdigest(),'two_independent_parsers_concordant':True,'repeat_projection_identical':True,
         'expected_known_qc':qc,'pysam':other['pysam'],'htslib':other['htslib'],
         'development_error':'Initial multi-intron test fixture start was 5 bases too high; corrected synthetic position before real data. No real replay attempted on failing preflight.'})
    print('Synthetic independent QC preflight passed')


if __name__=='__main__':run(sys.argv[1],sys.argv[2])
