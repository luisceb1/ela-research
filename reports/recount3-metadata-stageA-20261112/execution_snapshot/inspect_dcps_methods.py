from transport import get,ROOT
import xml.etree.ElementTree as ET
raw=get('https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13058276/fullTextXML','DCPS_primary_fulltext')
if raw is not None:
 try:
  root=ET.fromstring(raw)
  out=[]
  for sec in root.findall('.//sec'):
   title=sec.findtext('title','')
   if any(x in title.lower() for x in ['cell culture','stem cell','neuron','model','resource','rna sequencing','rna-seq']):
    tx=' '.join(sec.itertext())
    if len(tx)<16000:out.append({'section':title,'text':tx})
  import json
  (ROOT/'DCPS_methods_projection.json').write_text(json.dumps(out,indent=2)+'\n')
  for x in out:
   if any(z in x['text'] for z in ['H1','WTC','WA01','KOLF','cell line']):print(x['section'],x['text'][:7000])
 except Exception as e:print('Full text not XML or parse failure:',e)
