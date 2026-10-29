"""Arithmetic on a manually reviewed timeline; not automated source extraction."""
import json,csv,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def classify(kd,aso):
 if min(kd,aso)<0:raise ValueError('Negative culture day')
 return 'before_perturbation' if aso<kd else 'concurrent' if aso==kd else 'after_perturbation_not_yet_proof_of_reversal'
if __name__=='__main__':
 p=ROOT/'research/keuss_accepted_timeline.json';raw=p.read_bytes();rows=json.loads(raw)
 for r in rows:r['aso_minus_kd_days']=r['aso_day']-r['kd_day'];r['timing']=classify(r['kd_day'],r['aso_day'])
 out=ROOT/'reports/accepted-keuss';out.mkdir(exist_ok=True)
 with (out/'timeline.tsv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
 (out/'validation.json').write_text(json.dumps({'curation':'manual; methods and table crosschecked','input_sha256':hashlib.sha256(raw).hexdigest(),'experiments_in_table':len(rows),'clinical_efficacy_inferred':False},indent=2)+'\n')
