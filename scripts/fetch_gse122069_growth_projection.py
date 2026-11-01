#!/usr/bin/env python3
"""Recheck one fixed culture growth protocol because newly read PDF differs.
No contacts or other sample attributes are retained.
"""
import hashlib
import json
import re
from datetime import datetime,timezone
from pathlib import Path
import urllib.request

URL='https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM3454242&targ=self&form=text&view=quick'

def project(body):
    text=body.decode('utf-8')
    fields={}
    for line in text.splitlines():
        if line.startswith('!Sample_') and ' = ' in line:
            key,value=line.split(' = ',1)
            if key in ('!Sample_geo_accession','!Sample_source_name_ch1','!Sample_growth_protocol_ch1'):
                if key in fields and fields[key]!=value:raise ValueError('Conflicting growth fields')
                fields[key]=value
    if fields.get('!Sample_geo_accession')!='GSM3454242' or fields.get('!Sample_source_name_ch1')!='SH-SY5Y cell line':
        raise ValueError('Non-target culture record')
    if not fields.get('!Sample_growth_protocol_ch1'):raise ValueError('No growth protocol')
    protocol=fields.pop('!Sample_growth_protocol_ch1')
    if 'DMEM/F12' not in protocol:raise ValueError('Unexpected medium; manual review required')
    def number(pattern):
        match=re.search(pattern,protocol)
        if not match:raise ValueError('Unparsed technical growth variable')
        return float(match.group(1))
    fields['growth_protocol_projection']={'medium':'DMEM/F12',
        'fetal_bovine_serum_percent':number(r'(\d+)% fetal-bovine serum'),
        'penicillin_streptomycin_percent':number(r'(\d+)% penicillin-streptomycin'),
        'temperature_C':number(r'(\d+) °C'),'CO2_percent':number(r'(\d+)% CO2')}
    return fields

if __name__=='__main__':
    r={'url':URL,'date_utc':datetime.now(timezone.utc).isoformat(),'reason':'new Reporting Summary medium formulation differs; focused reconciliation, not repeated discovery of protocol'}
    try:
        with urllib.request.urlopen(URL,timeout=30) as f:b=f.read(200001);r['http_status']=f.status
        if len(b)>200000:raise ValueError('Byte cap exceeded')
        r.update(bytes=len(b),sha256_original=hashlib.sha256(b).hexdigest(),projection=project(b))
    except Exception as exc:r['error']=type(exc).__name__+': '+str(exc)
    Path('reports/gse122069-design-20261031/growth-protocol-recheck.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
