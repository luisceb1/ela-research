import json,urllib.parse,time
from transport import ROOT,get
j=json.loads((ROOT/'series_summaries.json').read_text())['result']
wanted=['GSE298758','GSE252892','GSE307054','GSE299341','GSE248847']
for acc in wanted:
 url='https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?'+urllib.parse.urlencode({'acc':acc,'targ':'self','form':'text','view':'full'})
 raw=get(url,acc+'_series')
 if raw is not None:
  t=raw.decode(errors='replace')
  print('\nSERIES',acc)
  for line in t.splitlines():
   if any(k in line for k in ['!Series_title','!Series_summary','!Series_overall_design','!Series_relation','!Series_type','!Series_pubmed_id']): print(line[:1500])
 time.sleep(.4)
