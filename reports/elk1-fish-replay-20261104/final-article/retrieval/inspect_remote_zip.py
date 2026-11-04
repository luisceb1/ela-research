import urllib.request,struct,json,hashlib
from pathlib import Path

URL='https://zenodo.org/api/records/15538003/files/2025-05-28__tdp43-apa__data.zip/content'
SIZE=831190727
CAP=5*1024*1024
requests=[]
used=0

def get_range(start,end):
    global used
    n=end-start+1
    if n<=0 or used+n>CAP: raise ValueError('Byte budget exceeded')
    req=urllib.request.Request(URL,headers={'Range':f'bytes={start}-{end}'})
    with urllib.request.urlopen(req,timeout=20) as r:
        data=r.read(min(n+1,CAP-used+1))
        used+=len(data)
        entry=dict(start=start,end=end,status=r.status,content_range=r.headers.get('Content-Range'),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        requests.append(entry)
        if r.status!=206 or entry['content_range']!=f'bytes {start}-{end}/{SIZE}' or len(data)!=n:
            raise ValueError('Range not honored exactly; no full archive download')
        return data

def main():
    tail=get_range(SIZE-65557,SIZE-1)
    pos=tail.rfind(b'PK\x05\x06')
    if pos<0: raise ValueError('No ZIP end record')
    sig,disk,cd_disk,n_disk,n_total,cd_size,cd_offset,comment=struct.unpack_from('<4s4H2IH',tail,pos)
    if disk or cd_disk or n_total==65535 or cd_size==0xffffffff:
        raise ValueError('Unsupported multipart/ZIP64')
    cd=get_range(cd_offset,cd_offset+cd_size-1)
    entries=[];i=0
    while i<len(cd):
        v=struct.unpack_from('<4s6H3I5H2I',cd,i)
        if v[0]!=b'PK\x01\x02': raise ValueError('Invalid central directory')
        name=cd[i+46:i+46+v[10]].decode('utf-8')
        if '/wet/' in name or 'fish' in name.lower():
            entries.append(dict(name=name,flags=v[3],method=v[4],crc32=v[7],compressed=v[8],uncompressed=v[9],offset=v[16]))
        i+=46+v[10]+v[11]+v[12]
    Path('elk1-final-cache/selected-members.json').write_text(json.dumps(entries,indent=2)+'\n')
    print(json.dumps(dict(total_entries=n_total,central_directory_bytes=cd_size,selected=entries)))

if __name__=='__main__':
    try:main()
    except Exception as error:print(type(error).__name__,str(error))
    finally:Path('elk1-final-cache/range-receipt.json').write_text(json.dumps(dict(bytes_read=used,cap=CAP,requests=requests),indent=2)+'\n')
