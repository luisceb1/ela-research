"""ST7 schema and exact sample compatibility, aggregate export only."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as E
import zipfile
from audit_stmn2_units import read_table, build_index, join_samples
from paired_stmn2 import select_pairs

SHA='6b24edc4279eebb0d8560ef277573745fa0110e1e8d1a07009621d020cd2abfc'
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def read_st7(path):
    if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=SHA:raise ValueError('source hash mismatch')
    with zipfile.ZipFile(path) as z:
        strings=[''.join(el.itertext()) for el in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS)]
        rel={r.attrib['Id']:r.attrib['Target'] for r in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        sheet=next(s for s in E.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet',NS) if s.attrib['name']=='ST7')
        target=rel[sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
        target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
        rows=E.fromstring(z.read(target)).findall('m:sheetData/m:row',NS)
        def values(row):
            out={}
            for c in row.findall('m:c',NS):
                v=c.find('m:v',NS);val=v.text if v is not None else ''
                out[''.join(x for x in c.attrib['r'] if x.isalpha())]=strings[int(val)] if c.attrib.get('t')=='s' and val else val
            return out
        header=values(rows[0]);required={'Sample','cell type','estimate','tissue'}
        if set(header.values())!=required:raise ValueError('unexpected ST7 schema')
        return [{name:values(row).get(col,'') for col,name in header.items()} for row in rows[1:]]


def validate_vectors(rows):
    grouped=defaultdict(list)
    for row in rows:grouped[(row['Sample'],row['tissue'])].append(row)
    accepted={};bad=Counter();taxa=defaultdict(set)
    for (sample,tissue),ss in grouped.items():
        labels=[r['cell type'] for r in ss];taxa[tissue].update(labels)
        if len(labels)!=len(set(labels)):bad['duplicate_cell_type_keys']+=1;continue
        try:values={r['cell type']:float(r['estimate']) for r in ss}
        except (ValueError,TypeError):bad['nonnumeric_estimate']+=1;continue
        if any(not math.isfinite(v) or not 0<=v<=1 for v in values.values()):bad['invalid_fraction_range']+=1;continue
        if abs(sum(values.values())-1)>1e-6:bad['sum_not_one']+=1;continue
        accepted[(sample,tissue)]=values
    # A locally summing vector need not contain the full tissue reference taxonomy.
    complete={k:v for k,v in accepted.items() if set(v)==taxa[k[1]]}
    bad['incomplete_taxonomy']=len(accepted)-len(complete)
    return complete,dict(bad),{t:sorted(v) for t,v in taxa.items()}


def baseline(root):
    root=Path(root);projects=read_table(root/'project_global.source','\t')
    author=build_index(read_table(root/'author_map.source',','),('sample_id_rna','sample'),'external_subject_id','rna_tissue_source',('project',))
    jung=build_index(read_table(root/'jung_table.source','\t'),('sample_id_alt',),'subject_id','tissue',('project','libprep'))
    records=[]
    for tissue,region in [('corteza','Cortex_Motor_Lateral'),('cervical','Spinal_Cord_Cervical')]:
        ss=json.loads((root/f'repo/reports/stmn2-derivation-20261111/results_{tissue}.json').read_text())['samples']
        a,_=join_samples(ss,projects,*author,region,'Target ALS');b,_=join_samples(ss,projects,*jung,region,'Target ALS PM core')
        rr=[]
        for s in ss:
            key=str(s['rail_id'])
            if key not in a or key not in b or a[key]['donor']!=b[key]['donor']:continue
            rr.append({'donor':a[key]['donor'],'sample':a[key]['external'],'group':s['group'],'prep':b[key]['extra'][1],'c':s['counts']['canonical'],'k':s['counts']['cryptic']})
        records.append(rr)
    pairs,_=select_pairs(*records,'ALS Spectrum MND',20)
    if len(pairs)!=45:raise ValueError('baseline changed')
    return pairs


def run(root):
    root=Path(root);rows=read_st7(root/'source-gate/nygc-expression-tables.xlsx')
    vectors,failures,taxa=validate_vectors(rows);pairs=baseline(root)
    match=Counter();regions={};keys_per_sample=defaultdict(list)
    for sample,tissue in vectors:keys_per_sample[sample].append(tissue)
    both=0
    for x,y in pairs:
        found=[]
        for name,rec in [('cortex',x),('cervical',y)]:
            tissuekeys=keys_per_sample[rec['sample']]
            if len(tissuekeys)==1:
                match[name]+=1;regions.setdefault(name,Counter())[tissuekeys[0]]+=1;found.append(True)
            else:found.append(False)
        both+=all(found)
    return {'source_sha256':SHA,'schema':['Sample','cell type','estimate','tissue'],'data_rows':len(rows),
            'validated_sample_reference_vectors':len(vectors),'vector_validation_failures':failures,
            'reference_taxonomies':taxa,'baseline_pairs':len(pairs),'exact_unique_vectors_for_baseline_libraries':dict(match),
            'source_reference_labels_by_baseline_region':{k:dict(v) for k,v in regions.items()},'pairs_with_two_exact_vectors':both,
            'decision':'technical sample join assessed only; do not assume cross-reference fractions are calibrated'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-root',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();out=run(a.source_root);dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps(out,indent=2))
