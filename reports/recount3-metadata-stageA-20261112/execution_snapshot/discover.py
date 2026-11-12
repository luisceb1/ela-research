import json,pathlib,time,urllib.parse
from transport import get,ROOT
LOCK=pathlib.Path('/workspace/scratch/9fdc55a9cfb9/ela-recount3-stageA/reports/recount3-metadata-stageA-20261112/QUERIES.json')
spec=json.loads(LOCK.read_text());ids=[];query_results=[]
for q in spec['queries']:
 params={'db':'gds','term':q['term'],**spec['parameters']}
 url=spec['endpoint']+'?'+urllib.parse.urlencode(params)
 raw=get(url,q['id'])
 if raw is None:
  query_results.append({'id':q['id'],'status':'access_failure','ids':[]})
  # This endpoint is required; preserve failure and stop, do not call it zero hits.
  break
 try:
  j=json.loads(raw)
  if 'error' in j or 'esearchresult' not in j:raise ValueError('not an esearch result')
  e=j['esearchresult']
  if e.get('errorlist'):raise ValueError(str(e['errorlist']))
  new=[x for x in e['idlist'] if x not in ids]
  slots=30-len(ids);ids.extend(new[:slots])
  query_results.append({'id':q['id'],'status':'ok','declared_hits':e['count'],'returned_ids':e['idlist'],'opened_ids':new[:slots],'unopened_ids':new[slots:],'translation':e.get('querytranslation'),'warninglist':e.get('warninglist')})
 except Exception as e:
  query_results.append({'id':q['id'],'status':'parse_failure','error':str(e)});break
 if len(ids)>=30:break
 time.sleep(.4)
(ROOT/'discovery.json').write_text(json.dumps({'query_lock':'3bbc9326a926a77e6224600a8250e189d5c679b3','queries':query_results,'inspected_ids':ids},indent=2)+'\n')
if ids:
 url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?'+urllib.parse.urlencode({'db':'gds','id':','.join(ids),'retmode':'json'})
 raw=get(url,'series_summaries')
 if raw is not None:
  j=json.loads(raw)
  (ROOT/'series_summaries.json').write_text(json.dumps(j,indent=2)+'\n')
  for uid in j.get('result',{}).get('uids',[]):
   s=j['result'][uid];print(json.dumps({k:s.get(k) for k in ['uid','accession','title','summary','gpl','gse','entrytype','taxon','samples','pubmedids']}),flush=True)
