from pathlib import Path
import zipfile,xml.etree.ElementTree as E,json,sys,collections,hashlib,math
root=Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/'repo/scripts'));import audit_stmn2_units as a
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(root/'source-gate/nygc-metadata.xlsx') as z:
 ss=[''.join(el.itertext()) for el in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)]
 rows=E.fromstring(z.read('xl/worksheets/sheet6.xml')).findall('m:sheetData/m:row',ns)
 def values(row):
  out={}
  for c in row.findall('m:c',ns):
   v=c.find('m:v',ns);val=v.text if v is not None else '';out[''.join(x for x in c.attrib['r'] if x.isalpha())]=ss[int(val)] if c.attrib.get('t')=='s' and val else val
  return out
 headers=values(rows[1]);allowed={'rna_id','donor_id','tissue_full','tissue_clean','tissue_code','region','rin','rna_prep','rna_platform','sra_run'}
 cols={col:name for col,name in headers.items() if name in allowed}
 def valid_rin(v):
  try:return math.isfinite(float(v)) and 1<=float(v)<=10
  except (ValueError,TypeError):return False
 data=[]
 for row in rows[2:]:
  vals=values(row);data.append({name:vals.get(col,'') for col,name in cols.items()})
 idx=collections.defaultdict(list)
 for row in data:idx[row['rna_id']].append(row)
 pr=a.read_table(root/'project_global.source','\t');out={'source_sha256':hashlib.sha256((root/'source-gate/nygc-metadata.xlsx').read_bytes()).hexdigest(),'rows':len(data),'technical_columns_used':sorted(allowed),'regions':{}}
 for tissue,region in [('corteza','Cortex_Motor_Lateral'),('cervical','Spinal_Cord_Cervical')]:
  samples=json.loads((root/f'repo/reports/stmn2-derivation-20261111/results_{tissue}.json').read_text())['samples'];lookup,_=a.project_lookup(pr,region)
  matched=[idx[lookup[str(s['rail_id'])][0]][0] for s in samples if str(s['rail_id']) in lookup and len(idx[lookup[str(s['rail_id'])][0]])==1]
  out['regions'][region]={'original_samples':len(samples),'exact_rna_id_matches':len(matched),'rin_valid_1_to_10':sum(valid_rin(x['rin']) for x in matched),'preparation_nonmissing':sum(bool(x['rna_prep'].strip()) for x in matched),'source_tissue_labels':dict(collections.Counter(x['tissue_full'] for x in matched))}
 dest=root/'repo/reports/paired-stmn2-source-gate-20261111';dest.mkdir(parents=True,exist_ok=True);(dest/'qc_availability.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
