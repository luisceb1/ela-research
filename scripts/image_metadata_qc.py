"""Read bounded TIFF headers and published XLSX XML; no pixel effects or inference."""
import concurrent.futures,csv,hashlib,json,re,struct,urllib.request,zipfile
import xml.etree.ElementTree as E
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/image-metadata-qc';CACHE=ROOT/'data/cache/image_headers'
def parse_tiff(b):
 endian='>' if b[:2]==b'MM' else '<' if b[:2]==b'II' else None
 if endian is None or struct.unpack(endian+'H',b[2:4])[0]!=42:raise ValueError('Unsupported TIFF')
 off=struct.unpack(endian+'I',b[4:8])[0]
 if off+2>len(b):raise ValueError('IFD outside sampled bytes')
 n=struct.unpack(endian+'H',b[off:off+2])[0];tags={}
 for i in range(n):
  loc=off+2+i*12
  if loc+12>len(b):raise ValueError('Truncated IFD')
  tag,typ,count,value=struct.unpack(endian+'HHII',b[loc:loc+12])
  width={1:1,2:1,3:2,4:4,5:8,7:1,11:4,12:8}.get(typ)
  if width is None:tags[tag]='unparsed';continue
  start=loc+8 if width*count<=4 else value
  raw=b[start:start+width*count]
  if len(raw)!=width*count:tags[tag]='outside_sample';continue
  if typ==2:tags[tag]=raw.rstrip(b'\0').decode('utf-8',errors='replace')
  elif typ in (3,4):tags[tag]=list(struct.unpack(endian+str(count)+('H' if typ==3 else 'I'),raw));tags[tag]=tags[tag][0] if count==1 else tags[tag]
  elif typ==5:tags[tag]=list(struct.unpack(endian+str(count*2)+'I',raw))
  else:tags[tag]=raw.hex()
 nextloc=off+2+12*n
 if nextloc+4>len(b):raise ValueError('Next IFD pointer missing')
 return {'width':tags.get(256),'height':tags.get(257),'bits':tags.get(258),'compression':tags.get(259),
 'description':tags.get(270,''),'x_resolution':tags.get(282),'y_resolution':tags.get(283),'resolution_unit':tags.get(296),
 'datetime':tags.get(306),'next_ifd':struct.unpack(endian+'I',b[nextloc:nextloc+4])[0],'tag_ids':sorted(tags)}
def validate_range(status,content_range,start,end,size,body):
 if status!=206 or content_range!=f'bytes {start}-{end}/{size}' or len(body)!=end-start+1:raise ValueError('Unverified HTTP byte range')
def micron_scale(header):
 unit=re.search(r'^unit=(.+)$',header.get('description',''),re.M)
 if not unit or unit[1].strip().lower() not in {'micron','um','µm'}:return None
 x,y=header.get('x_resolution'),header.get('y_resolution')
 if not isinstance(x,list) or not isinstance(y,list) or len(x)!=2 or len(y)!=2 or min(*x,*y)<=0:return None
 return {'x_um_per_pixel':x[1]/x[0],'y_um_per_pixel':y[1]/y[0],'basis':'ImageJ micron unit plus TIFF rational resolution; no transfer to untagged images'}
def header(f):
 CACHE.mkdir(parents=True,exist_ok=True);p=CACHE/(hashlib.sha256(f['key'].encode()).hexdigest()+'.bin')
 expected=min(65536,f['size'])
 if p.exists():b=p.read_bytes();transport='cached_range'
 else:
  req=urllib.request.Request(f['url'],headers={'Range':f'bytes=0-{expected-1}'})
  with urllib.request.urlopen(req,timeout=30) as r:
   if r.status!=206:raise ValueError('Server ignored Range; full download refused')
   b=r.read(expected+1);validate_range(r.status,r.headers.get('Content-Range'),0,expected-1,f['size'],b)
  p.write_bytes(b);transport='verified_HTTP206_range'
 return {'file':f['key'],'source_url':f['url'],'source_size':f['size'],'source_md5_not_verified':f['checksum'],
 'range_start':0,'range_end':len(b)-1,'range_sha256':hashlib.sha256(b).hexdigest(),'transport':transport,**parse_tiff(b)}
def workbook_projection(path):
 ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};relsns='{http://schemas.openxmlformats.org/package/2006/relationships}'
 with zipfile.ZipFile(path) as z:
  wb=E.fromstring(z.read('xl/workbook.xml'));rels={r.get('Id'):r.get('Target') for r in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
  sheets=wb.find('s:sheets',ns);sheet=next(x for x in sheets if x.get('name')=='Figure7');rid=sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id');target=rels[rid];name=target.lstrip('/') if target.startswith('/') else 'xl/'+target
  shared=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml'))] if 'xl/sharedStrings.xml' in z.namelist() else []
  cells=[]
  for c in E.fromstring(z.read(name)).findall('.//s:sheetData/s:row/s:c',ns):
   v=c.find('s:v',ns);value=v.text if v is not None else ''
   if c.get('t')=='s':value=shared[int(value)]
   elif c.get('t')=='inlineStr':value=''.join(c.find('s:is',ns).itertext())
   form=c.find('s:f',ns)
   if value or form is not None:cells.append({'cell':c.get('r'),'value':value,'type':c.get('t','numeric'),'formula':form.text if form is not None else '','sheet':'Figure7'})
 return cells
if __name__=='__main__':
 OUT.mkdir(exist_ok=True);inventory=json.loads((ROOT/'reports/reversal-design/zenodo_inventory.json').read_text())
 selected=sorted([f for f in inventory['files'] if f['key'].startswith('Figure7_')],key=lambda f:f['key'])
 errors=[];rows=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  for f,future in [(f,pool.submit(header,f)) for f in selected]:
   try:rows.append(future.result())
   except Exception as e:errors.append({'file':f['key'],'error':type(e).__name__+': '+str(e)})
 for row in rows:row['physical_scale']=micron_scale(row)
 (OUT/'tiff_headers.json').write_text(json.dumps(rows,indent=2)+'\n')
 meta=json.loads((ROOT/'data/cache/zenodo15346391.json').read_text());source=next(f for f in meta['files'] if f['key'].endswith('.xlsx'));path=ROOT/'data/cache'/source['key']
 if hashlib.md5(path.read_bytes()).hexdigest()!=source['checksum'][4:]:raise ValueError('Workbook checksum mismatch')
 cells=workbook_projection(path)
 with (OUT/'figure7_workbook_cells.tsv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(cells[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(cells)
 counts={}
 for col in 'ABCDEFGH':
  vals=[c for c in cells if re.fullmatch(col+r'\d+',c['cell']) and int(re.search(r'\d+',c['cell'])[0])>=4 and c['type']=='numeric' and c['value']!='']
  counts[col]=len(vals)
 summary={'selected_files':len(selected),'parsed_headers':len(rows),'range_bytes_total':sum(r['range_end']+1 for r in rows),'all_pixel_sizes':sorted(set((r['width'],r['height']) for r in rows)),
 'headers_with_resolution_tags':sum(r['x_resolution'] is not None or r['y_resolution'] is not None for r in rows),'headers_with_datetime':sum(r['datetime'] is not None for r in rows),
 'full_file_md5_verified':False,'workbook_md5_verified':True,'workbook_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'length_observations_by_column_not_replicates':counts,'biological_replication_verified':False,'new_biological_effects_estimated':False}
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(OUT/'errors.json').write_text(json.dumps(errors,indent=2)+'\n')
 (OUT/'run.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'status':'partial' if errors else 'generated','original_workbook_edited':False,'header_bytes_per_file':65536,'max_workers':2},indent=2)+'\n');print(summary)
 if errors:print(errors);raise SystemExit(1)
