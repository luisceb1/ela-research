"""Validate a manually curated evidence matrix, not automated paper interpretation."""
import csv,json,hashlib,platform
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def validate(rows):
    ids=set()
    for r in rows:
        if r['id'] in ids:raise ValueError('Duplicate evidence unit')
        ids.add(r['id'])
        if r['timing'] not in {'unverified','concurrent','prevention','delayed'}:raise ValueError('Unknown timing')
        if r['timing']=='delayed' and not r['baseline_same_units']:raise ValueError('Delayed reversal requires verified baseline in same units')
        if r['clinical_efficacy']:raise ValueError('No clinical efficacy established in this matrix')
        if not r['locator'] or not r['limit']:raise ValueError('Missing evidence provenance/limit')
    return rows
if __name__=='__main__':
    p=ROOT/'research/functional_evidence.json';raw=p.read_bytes();rows=validate(json.loads(raw))
    out=ROOT/'reports/functional-evidence';out.mkdir(exist_ok=True)
    with (out/'matrix.tsv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    (out/'validation.json').write_text(json.dumps({'units':len(rows),'input_sha256':hashlib.sha256(raw).hexdigest(),'python':platform.python_version(),'curation':'manual; source-level limits retained','delayed_reversal_verified':sum(r['timing']=='delayed' for r in rows),'clinical_efficacy_inferred':False},indent=2)+'\n')
