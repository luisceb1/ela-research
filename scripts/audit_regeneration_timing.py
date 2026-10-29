"""Extract injury timing from primary Fig7; no new biological measurements."""
import re,json,hashlib,xml.etree.ElementTree as E
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def extract(caption):
 m=re.search(r'(\d+)\s+d\s+after transduction,\s*neurons were axotomized',caption)
 if not m:raise ValueError('Explicit interval missing')
 return {'intervention_minus_axotomy_days':-int(m[1]),'time_origin':'axotomy, not genetic deficiency','delayed_postinjury_intervention':False}
if __name__=='__main__':
 raw=(ROOT/'data/cache/PMC12130871.xml').read_bytes();r=E.fromstring(raw)
 assert any(x.text=='10.1073/pnas.2502294122' for x in r.findall('.//article-id'))
 captions=[' '.join(f.itertext()) for f in r.findall('.//fig') if '3 d after transduction' in ' '.join(f.itertext())]
 if len(captions)!=1:raise ValueError('Ambiguous caption')
 out={**extract(captions[0]),'source_sha256':hashlib.sha256(raw).hexdigest(),'locator':'Figure7 caption'}
 (ROOT/'reports/reversal-design/regeneration_timing.json').write_text(json.dumps(out,indent=2)+'\n')
