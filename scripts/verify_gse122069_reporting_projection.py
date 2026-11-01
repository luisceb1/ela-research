#!/usr/bin/env python3
"""Check cached public Reporting Summary hash/text without retaining unrelated sections."""
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys


def verify(pdf,receipt,rows):
    b=Path(pdf).read_bytes()
    if hashlib.sha256(b).hexdigest()!=receipt['sha256_original']:raise ValueError('Reporting Summary bytes changed')
    text=subprocess.run(['pdftotext','-layout',str(pdf),'-'],capture_output=True,text=True,check=True).stdout
    info=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True,check=True).stdout
    pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
    if pages!=3 or 'Reporting Summary' not in text:raise ValueError('Unexpected document')
    versions={}
    for name,version in [('STAR','2.5.3a'),('RSEM','1.3.0'),('DESeq2','1.14.1')]:
        if name not in text or version not in text:raise ValueError('Software projection not supported')
        versions[name]=version
    tokens=[r[k] for r in rows for k in ('gsm','experiment','run')]
    found=[token for token in tokens if token in text]
    if '531342' not in text or 'Minimum' not in text or 'Essential Medium' not in text:
        raise ValueError('Cell-medium projection not supported')
    return {'source_sha256':receipt['sha256_original'],'pages':pages,'accession_tokens_found':found,
            'author_software_versions_present':versions,'FBS_lot531342_present':True,
            'token_absence_alone_is_not_a_semantic_proof_of_missing_map':True,
            'visual_review_required_for_checkboxes_and_semantics':True,
            'no_full_text_clinical_or_contact_sections_retained':True}

if __name__=='__main__':
    out=Path('reports/gse122069-design-20261031')
    receipt=json.loads((out/'reporting-summary-retrieval.json').read_text())
    rows=json.loads(Path('reports/gse122069-resource-plan/input_manifest.json').read_text())['rows']
    result=verify(Path(sys.argv[1]),receipt,rows)
    result.update(python=platform.python_version(),pdftotext_version=subprocess.run(['pdftotext','-v'],capture_output=True,text=True).stderr.strip())
    (out/'reporting-summary-qc.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
