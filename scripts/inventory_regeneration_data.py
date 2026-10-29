"""Inventory public file metadata; labels are not verified biological replicates."""
import json,re,csv
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/reversal-design'
if __name__=='__main__':
 d=json.loads((OUT/'zenodo_inventory.json').read_text());files=d['files']
 if len({f['key'] for f in files})!=len(files):raise ValueError('Duplicate file key')
 groups=defaultdict(dict)
 for f in files:
  if not f.get('checksum'):raise ValueError('Missing source checksum')
  m=re.fullmatch(r'Figure7_(WT|KO)_(WTmScarlet|TBNmScarlet|mScarlet)_(0|24|48)h_(\d+)\.tif',f['key'],re.I)
  if m:
   group,label=(m[1].upper()+'_'+m[2].lower(),m[4])
   if int(m[3]) in groups[(group,label)]:raise ValueError('Duplicate label/time')
   groups[(group,label)][int(m[3])]=f
 rows=[]
 for (condition,label),times in sorted(groups.items()):
  rows.append({'condition_from_filename':condition,'label_not_verified_replicate':label,'times_hours':','.join(map(str,sorted(times))),'complete_0_24_48':set(times)=={0,24,48},'bytes':sum(f['size'] for f in times.values())})
 with (OUT/'figure7_file_groups.tsv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
 summary={'metadata_files':len(files),'all_bytes':sum(f['size'] for f in files),'figure7_matched_files':sum(len(g) for g in groups.values()),'filename_groups':len(rows),'complete_triplets':sum(r['complete_0_24_48'] for r in rows),'biological_replication_verified':False,'images_downloaded_or_analyzed':False}
 (OUT/'inventory_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)
