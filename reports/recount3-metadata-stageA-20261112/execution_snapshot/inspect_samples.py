import urllib.parse,time
from transport import get
samples=['GSM9022610','GSM9022614','GSM8009878','GSM8009881','GSM9214880','GSM9214882','GSM9037603','GSM9037613']
for acc in samples:
 url='https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?'+urllib.parse.urlencode({'acc':acc,'targ':'self','form':'text','view':'full'})
 raw=get(url,acc+'_sample')
 if raw is not None:
  print('\nSAMPLE',acc)
  for line in raw.decode(errors='replace').splitlines():
   if any(k in line for k in ['!Sample_title','!Sample_source_name','!Sample_characteristics','!Sample_treatment_protocol','!Sample_growth_protocol','!Sample_library','!Sample_data_processing','!Sample_relation','!Sample_extract_protocol']): print(line[:1400])
 time.sleep(.4)
