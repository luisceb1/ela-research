"""Bounded ENA metadata acquisition and fixed-library manifest; never downloads FASTQ."""
import csv
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import urlencode
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCES = {'GSE252892': ('PRJNA1063175', [f'GSM{x}' for x in range(8009878,8009884)]), 'GSE299341': ('PRJNA1273942', [f'GSM{x}' for x in list(range(9037603,9037608))+list(range(9037613,9037618))])}
FIELDS = 'study_accession,secondary_study_accession,experiment_accession,run_accession,sample_accession,library_strategy,library_layout,read_count,base_count,fastq_ftp,fastq_bytes,fastq_md5'

def acquire():
    if (OUT / "retrievals.json").exists():
        raise RuntimeError("Receipt exists; acquisition is not resumed or repeated")
    ledger=[]
    used=0
    for geo,(project,_) in SOURCES.items():
        url='https://www.ebi.ac.uk/ena/portal/api/filereport?'+urlencode({'accession':project,'result':'read_run','fields':FIELDS,'format':'tsv'})
        receipt={'source':geo,'url':url,'body_bytes':0,'body_sha256':None,'status':None}
        body=bytearray()
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'ela-research/metadata-feasibility'})
            with urllib.request.urlopen(req,timeout=45) as resp:
                receipt['status']=resp.status
                while True:
                    chunk=resp.read(min(65536,1_000_001-len(body),2_000_001-used))
                    if not chunk: break
                    body.extend(chunk);used+=len(chunk)
                    if len(body)>1_000_000 or used>2_000_000:raise RuntimeError('metadata body cap exceeded; stop')
            if receipt['status']!=200:raise RuntimeError('metadata response not successful')
        except Exception as exc:
            receipt['error']=str(exc)
        finally:
            receipt['body_bytes']=len(body)
            receipt['body_sha256']=hashlib.sha256(body).hexdigest()
            (OUT/(geo+'-ENA.tsv')).write_bytes(body)
            ledger.append(receipt)
            (OUT/'retrievals.json').write_text(json.dumps(ledger,indent=2)+'\n')
        if 'error' in receipt:raise RuntimeError(receipt['error'])


def derive():
    """Use an explicit prior GEO->SRX map exported with the source accession/hash."""
    mapping=json.loads((OUT/'selected-library-map.json').read_text())
    rows=[];summary={}
    for geo,(project,gsms) in SOURCES.items():
        records=list(csv.DictReader(io.StringIO((OUT/(geo+'-ENA.tsv')).read_text()),delimiter='\t'))
        by_srx={}
        for item in records:by_srx.setdefault(item['experiment_accession'],[]).append(item)
        for gsm in gsms:
            m=mapping[geo][gsm]
            assert m['srx'] in by_srx,(gsm,m)
            for item in by_srx[m['srx']]:
                urls=item['fastq_ftp'].split(';') if item['fastq_ftp'] else []
                sizes=item['fastq_bytes'].split(';') if item['fastq_bytes'] else []
                md5s=item['fastq_md5'].split(';') if item['fastq_md5'] else []
                assert len(urls)==len(sizes)==len(md5s),(gsm,item)
                for url,size,md5 in zip(urls,sizes,md5s):
                    rows.append({'geo_series':geo,'gsm':gsm,'declared_title':m['declared_title'],'srx':m['srx'],'run':item['run_accession'],'strategy':item['library_strategy'],'layout':item['library_layout'],'compressed_bytes':int(size),'md5':md5,'url':'https://'+url})
        selected=[x for x in rows if x['geo_series']==geo]
        summary[geo]={'project':project,'selected_libraries':len(gsms),'mapped_libraries_with_fastq':len({x['gsm'] for x in selected}),'run_records_with_fastq':len({x['run'] for x in selected}),'files':len(selected),'compressed_bytes':sum(x['compressed_bytes'] for x in selected),'per_library_bytes':{g:sum(x['compressed_bytes'] for x in selected if x['gsm']==g) for g in gsms}}
    fields=list(rows[0])
    with (OUT/'fastq-manifest.tsv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--acquire-metadata',action='store_true');args=ap.parse_args()
    if args.acquire_metadata:acquire()
    derive()
