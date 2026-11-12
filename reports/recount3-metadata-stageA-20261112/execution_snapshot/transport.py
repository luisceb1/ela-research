import urllib.request,urllib.error,json,hashlib,pathlib,time,datetime
ROOT=pathlib.Path('/workspace/scratch/9fdc55a9cfb9/stageA-cache')
LOG=ROOT/'retrievals.json'
CAP=10_000_000
PER=700_000

def get(url,key):
 rows=json.loads(LOG.read_text()) if LOG.exists() else []
 used=sum(x.get('bytes',0) for x in rows)
 if used>=CAP:raise RuntimeError('Stage A total body byte cap reached')
 for attempt in range(2):
  row={'id':key,'url':url,'attempt':attempt+1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':0}
  data=b'';limit=min(PER,CAP-used)
  try:
   req=urllib.request.Request(url,headers={'Accept':'application/json,application/xml,text/plain,text/html','User-Agent':'ela-research-metadata-review/1.0'})
   try:resp=urllib.request.urlopen(req,timeout=25)
   except urllib.error.HTTPError as e:resp=e
   with resp:
    row.update(status=resp.status,final_url=resp.url,content_type=resp.headers.get('Content-Type',''),declared_bytes=resp.headers.get('Content-Length'))
    while len(data)<limit:
     chunk=resp.read(min(65536,limit-len(data)))
     if not chunk:break
     data+=chunk
    row['bytes']=len(data);row['sha256']=hashlib.sha256(data).hexdigest()
    row['truncated_or_limit']=len(data)==limit and row['declared_bytes']!=str(limit)
   used+=len(data)
   (ROOT/(key+f'.attempt{attempt+1}.body')).write_bytes(data)
   if row['status']!=200:row['error']='HTTP '+str(row['status'])
   if row['truncated_or_limit']:row['error']='response capped;not complete evidence'
  except Exception as e:row['error']=type(e).__name__+': '+str(e)
  rows.append(row);LOG.write_text(json.dumps(rows,indent=2)+'\n')
  print(json.dumps({k:row.get(k) for k in ['id','attempt','status','bytes','error']}),flush=True)
  if 'error' not in row:return data
  if row.get('status') not in [429,500,502,503,504] or attempt==1:return None
  time.sleep(2)
 return None
