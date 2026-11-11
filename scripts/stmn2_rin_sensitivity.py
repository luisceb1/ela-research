"""Fixed RIN restriction of original paired STMN2 results. Aggregate output only."""
import argparse
from collections import defaultdict, Counter
import hashlib
import json
import math
from pathlib import Path
import statistics
import xml.etree.ElementTree as E
import zipfile
from audit_stmn2_units import read_table, build_index, join_samples
from paired_stmn2 import select_pairs, summarize

HASH='c1bf21493c4a2773e27ff787e60267fc2e1304ce11e84e644c03c700cc68f048'
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def read_qc(path):
    if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=HASH:
        raise ValueError('metadata hash differs from fixed input')
    with zipfile.ZipFile(path) as z:
        strings=[''.join(el.itertext()) for el in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS)]
        relationships={r.attrib['Id']:r.attrib['Target'] for r in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        sheet=next(s for s in E.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet',NS) if s.attrib['name']=='ST3')
        target=relationships[sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
        target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
        rows=E.fromstring(z.read(target)).findall('m:sheetData/m:row',NS)
        def value(c):
            v=c.find('m:v',NS);text=v.text if v is not None else ''
            return strings[int(text)] if c.attrib.get('t')=='s' and text else text
        header={''.join(x for x in c.attrib['r'] if x.isalpha()):value(c) for c in rows[1].findall('m:c',NS)}
        allowed={'rna_id','donor_id','tissue_full','rin','rna_prep'}
        out=[]
        for row in rows[2:]:
            d={header[col]:value(c) for c in row.findall('m:c',NS) if (col:=''.join(x for x in c.attrib['r'] if x.isalpha())) in header and header[col] in allowed}
            out.append(d)
        return out


def compatibility(record, candidates, region):
    if len(candidates)!=1:return None,'missing_or_duplicate_metadata'
    q=candidates[0]
    if q.get('donor_id')!=record['donor']:return None,'donor_mismatch'
    if q.get('tissue_full')!=region:return None,'region_mismatch'
    # No fuzzy recoding of preparation labels.
    if q.get('rna_prep')!=record['prep']:return None,'preparation_mismatch'
    try:r=float(q.get('rin',''))
    except (ValueError,TypeError):return None,'invalid_rin'
    if not math.isfinite(r) or not 1<=r<=10:return None,'invalid_rin'
    return r,None


def qc_pass(pair, minimum):
    a,b=pair
    return min(a['rin'],b['rin'])>=minimum and abs(a['rin']-b['rin'])<=1


def interpretation(n, median):
    if n<10:return 'insufficient_pairs'
    return 'positive_median_persists_descriptively' if median>0 else 'directional_prediction_not_supported'


def guard_baseline(pairs):
    if len(pairs)!=45:raise ValueError('baseline is not the original 45 pairs')


def describe(pairs):
    s=summarize(pairs)
    for name,idx in [('cortex',0),('cervical',1)]:
        s['coverage'][name]['rin_median']=statistics.median(p[idx]['rin'] for p in pairs) if pairs else None
    s['rin_abs_difference_median']=statistics.median(abs(x['rin']-y['rin']) for x,y in pairs) if pairs else None
    return s


def run(root):
    root=Path(root);qcpath=root/'source-gate/nygc-metadata.xlsx'
    qc=defaultdict(list)
    for row in read_qc(qcpath):qc[row['rna_id']].append(row)
    projects=read_table(root/'project_global.source','\t')
    author=build_index(read_table(root/'author_map.source',','),('sample_id_rna','sample'),'external_subject_id','rna_tissue_source',('project',))
    jung=build_index(read_table(root/'jung_table.source','\t'),('sample_id_alt',),'subject_id','tissue',('project','libprep'))
    records=[];failure=Counter();labels=Counter()
    for tissue,region in [('corteza','Cortex_Motor_Lateral'),('cervical','Spinal_Cord_Cervical')]:
        samples=json.loads((root/f'repo/reports/stmn2-derivation-20261111/results_{tissue}.json').read_text())['samples']
        first,_=join_samples(samples,projects,*author,region,'Target ALS');second,_=join_samples(samples,projects,*jung,region,'Target ALS PM core')
        rows=[]
        for sample in samples:
            rail=str(sample['rail_id'])
            if rail not in first or rail not in second or first[rail]['donor']!=second[rail]['donor']:continue
            rec={'donor':first[rail]['donor'],'group':sample['group'],'prep':second[rail]['extra'][1],'c':sample['counts']['canonical'],'k':sample['counts']['cryptic']}
            candidates=qc[first[rail]['external']]
            labels.update(q.get('rna_prep','') for q in candidates)
            rin,reason=compatibility(rec,candidates,region)
            rec['rin']=rin;rec['qc_failure']=reason;rows.append(rec)
        records.append(rows)
    baseline,selection=select_pairs(*records,'ALS Spectrum MND',20);guard_baseline(baseline)
    compatible=[]
    for pair in baseline:
        reasons=[r['qc_failure'] for r in pair if r['qc_failure']]
        if reasons:failure.update(set(reasons))
        else:compatible.append(pair)
    out={'evidence':'exploratory RIN restriction of original cohort, no additional p-values',
         'metadata_sha256':HASH,'input_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'project_global.source',root/'author_map.source',root/'jung_table.source',root/'repo/reports/stmn2-derivation-20261111/results_corteza.json',root/'repo/reports/stmn2-derivation-20261111/results_cervical.json']},'baseline_n_pairs':len(baseline),'baseline_selection':selection,
         'metadata_compatible_pairs':len(compatible),'baseline_pair_failures':dict(failure),
         'observed_qc_preparation_labels':dict(labels),'subsets':{}}
    for minimum in [6,7]:
        kept=[p for p in compatible if qc_pass(p,minimum)]
        rejected=[p for p in compatible if not qc_pass(p,minimum)]
        summary=describe(kept)
        out['subsets'][str(minimum)]={'rule':f'RIN>={minimum} both, absolute RIN difference<=1',
              'retained':summary,'excluded_compatible_pairs':describe(rejected),
              'exclusion_reasons_nonexclusive':{'either_RIN_below_minimum':sum(min(x['rin'],y['rin'])<minimum for x,y in compatible),'paired_RIN_difference_over_1':sum(abs(x['rin']-y['rin'])>1 for x,y in compatible)},
              'interpretation':interpretation(len(kept),summary['median_paired_difference'])}
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-root',required=True);p.add_argument('--output',required=True)
    args=p.parse_args();result=run(args.source_root);path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result,indent=2))
