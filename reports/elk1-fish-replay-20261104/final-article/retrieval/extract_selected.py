import inspect_remote_zip as remote
import json,struct,zlib,hashlib
from pathlib import Path

p=Path('elk1-final-cache')
old=json.loads((p/'range-receipt.json').read_text())
remote.used=old['bytes_read'];remote.requests=old['requests']
selected=json.loads((p/'selected-members.json').read_text())
wanted=['wet/data/fish_counts_cleaned.tsv','wet/data/number_foci_ratio.csv',
        'wet/data/nuclear_cyto_ratio.csv','wet/processed/2023-10-13_fish_counts_processed.tsv',
        'wet/processed/2023-10-13_fish_counts_cleaned_longer.tsv','wet/fish_plot.R']
outputs=[]
try:
 for name in wanted:
    e=next(x for x in selected if x['name']=='tdp43-apa/'+name)
    h=remote.get_range(e['offset'],e['offset']+29)
    fields=struct.unpack('<4s5H3I2H',h)
    assert fields[0]==b'PK\x03\x04' and not fields[2]&1
    n,x=fields[-2:]
    data=remote.get_range(e['offset']+30,e['offset']+29+n+x+e['compressed'])
    assert data[:n].decode()==e['name']
    raw=zlib.decompress(data[n+x:],-15) if e['method']==8 else data[n+x:]
    assert len(raw)==e['uncompressed'] and zlib.crc32(raw)==e['crc32']
    dest=p/'members'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
    outputs.append(dict(**e,sha256=hashlib.sha256(raw).hexdigest(),crc_verified=True))
    print('Verified',name,len(raw),flush=True)
except Exception as error:
 print(type(error).__name__,str(error),flush=True)
 raise
finally:
 (p/'extracted-members.json').write_text(json.dumps(outputs,indent=2)+'\n')
 (p/'range-receipt.json').write_text(json.dumps(dict(bytes_read=remote.used,cap=remote.CAP,requests=remote.requests),indent=2)+'\n')
