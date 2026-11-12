import json,urllib.parse,time
from transport import get,ROOT
j=json.loads((ROOT/'series_summaries.json').read_text())['result']
# Complete the relevant whole-transcriptome control/KD library maps; do not fetch count files.
wanted={
'GSE298758':lambda t:t.startswith('shCTRshCTR_rep') or t.startswith('shTDP-43shCTR_rep'),
'GSE252892':lambda t:', RNA-seq,' in t,
'GSE307054':lambda t:t.startswith('i3N: guide RNA control') or t.startswith('i3N: TDP-43 KD ') and '+' not in t,
'GSE299341':lambda t:t.startswith('TDP43 Experiment') and 'Soma Fraction' in t,
}
selected={}
for uid in j['uids']:
 s=j[uid];acc=s['accession']
 if acc not in wanted:continue
 selected[acc]=[x['accession'] for x in sorted(s['samples'],key=lambda z:z['accession']) if wanted[acc](x['title'])]
 for gsm in selected[acc]:
  key=gsm+'_sample'
  if (ROOT/(key+'.attempt1.body')).exists():continue
  raw=get('https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?'+urllib.parse.urlencode({'acc':gsm,'targ':'self','form':'text','view':'full'}),key)
  if raw is not None:
   out=[x for x in raw.decode(errors='replace').splitlines() if x.startswith('!Sample_characteristics_ch1 = cell line:') or x.startswith('!Sample_characteristics_ch1 = batch:')]
   print(gsm,out,flush=True)
  time.sleep(.4)
(ROOT/'selected_library_maps.json').write_text(json.dumps(selected,indent=2)+'\n')
# Linked paper metadata only, not another study discovery query.
raw=get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=41943580&retmode=xml','DCPS_paper_metadata')
if raw is not None:
 import xml.etree.ElementTree as ET
 root=ET.fromstring(raw)
 print('DCPS primary identifiers:',[(e.attrib.get('IdType'),e.text) for e in root.findall('.//ArticleId')])
