"""Molecular supplement and culture library map. No effects or statistical tests."""
import argparse,csv,hashlib,json,math,platform,re
import xml.etree.ElementTree as ET
from pathlib import Path
from scripts.inventory_junction_sources import COUNTS,source_group

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def clean(v):return ' '.join(str(v).replace('\xa0',' ').split())

def integer(v):
    if isinstance(v,float):
        if not math.isfinite(v) or not v.is_integer():raise ValueError('Noninteger coordinate')
        return int(v)
    s=clean(v)
    if not re.fullmatch('[0-9]+',s):raise ValueError('Invalid coordinate literal')
    return int(s)

def parse_sheet(rows):
    if [clean(x) for x in rows[0]]!=['chromosome','start','end','name','score_left_blank_for_bed_format','strand']:
        raise ValueError('Unexpected S6 schema')
    out=[]
    for i,r in enumerate(rows[1:],2):
        if not any(clean(x) for x in r):continue
        if len(r)!=6:raise ValueError('Ragged S6 row')
        chrom,start,end,name,score,strand=r;start=integer(start);end=integer(end)
        if start<1 or end<=start or clean(strand) not in ['+','-']:raise ValueError('Invalid junction geometry')
        out.append(dict(sheet_row=i,chrom=clean(chrom),left_boundary=start,right_boundary=end,name=clean(name),strand=clean(strand)))
    if len({r['name'] for r in out})!=len(out):raise ValueError('Duplicate S6 name')
    return out

def star_to_flanks(first,last):
    if not isinstance(first,int) or not isinstance(last,int) or first<2 or last<first:raise ValueError('Invalid STAR intron')
    return first-1,last+1

def bam_alias(filename):
    suffix='.Aligned.sorted.out.bam';base=Path(filename).name
    if not base.endswith(suffix):raise ValueError('Unexpected submitted BAM suffix')
    return base[:-len(suffix)]

def condition(alias):
    m=re.fullmatch(r'SHSY5Y(Control|TDP43KD)[1-3]',alias)
    if not m:raise ValueError('Unrecognized ENA culture condition')
    return 'control' if m[1]=='Control' else 'TDP-43 KD'

def exact_link(count_rows,ena_rows,run_map):
    out=[]
    if len(count_rows)!=6 or len({r['sample'] for r in count_rows})!=6:raise ValueError('Expected six unique culture rows')
    for c in count_rows:
        hits=[r for r in ena_rows if run_map[r['run_accession']]==c['sample']]
        if len(hits)!=1:raise ValueError('Missing/ambiguous exact submitted-file alias')
        e=hits[0]
        if e['study_accession']!='PRJEB42763' or condition(e['sample_alias'])!=c['condition']:raise ValueError('Study/condition discordance')
        out.append(dict(count_alias=c['sample'],condition=c['condition'],run_accession=e['run_accession'],sample_accession=e['sample_accession'],
            experiment_accession=e['experiment_accession'],ENA_alias=e['sample_alias'],link_rule='Exact basename after removal of fixed submitted BAM suffix',
            biological_unit_independence='not established by accession map'))
    if len({r['run_accession'] for r in out})!=6:raise ValueError('Run reused by count rows')
    return out

def main(cache,culture,reference,out):
    import xlrd
    xls=cache/'Supplementary6.xls'
    if sha(xls)!='54d91b96f58b0cb85234f10c11451ca86211e183e1d2d6076dab3fcd87b83a41':raise ValueError('S6 hash mismatch')
    raw=culture.read_bytes()
    if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!='c8715e2b6452f0e32bf56bd315171213950d0dff':raise ValueError('Culture source blob mismatch')
    book=xlrd.open_workbook(xls)
    if book.sheet_names()!=['Sheet1']:raise ValueError('Unexpected sheets')
    sheet=book.sheet_by_index(0);junctions=parse_sheet([sheet.row_values(i) for i in range(sheet.nrows)])
    with culture.open() as f:cs=[r for r in csv.DictReader(f) if source_group(r['source'])=='SH-SY5Y']
    with (cache/'ENA_runs.tsv').open() as f:es=[r for r in csv.DictReader(f,delimiter='\t') if r['sample_alias'].startswith('SHSY5Y')]
    if len(es)!=6 or len({r['run_accession'] for r in es})!=6:raise ValueError('Unexpected ENA group size')
    run_map={};inputs=[xls,culture,reference,cache/'ENA_runs.tsv',Path(__file__)]
    for e in es:
        p=cache/(e['run_accession']+'.xml');inputs.append(p);r=ET.parse(p).getroot().find('RUN')
        if r is None or r.get('accession')!=e['run_accession']:raise ValueError('Run XML identity mismatch')
        refs=r.findall('EXPERIMENT_REF')
        if len(refs)!=1 or refs[0].get('accession')!=e['experiment_accession']:raise ValueError('Experiment reference mismatch')
        files=r.findall('.//FILE')
        if len(files)!=1 or files[0].get('filetype')!='bam':raise ValueError('Ambiguous submitted files')
        run_map[e['run_accession']]=bam_alias(files[0].get('filename'))
    links=exact_link(cs,es,run_map)
    ref=json.loads(reference.read_text())['by_id'];matches=[]
    for label in COUNTS:
        hits=[r for r in junctions if r['name']==label]
        if not hits:
            matches.append(dict(count_field=label,S6_name='',chrom='',left_boundary='',right_boundary='',S6_strand='',reference_strand='',status='unresolved_alias_no_automatic_mapping'));continue
        j=hits[0];gid='ENSG00000104435' if label.startswith('STMN2') else 'ENSG00000130477';g=ref[gid]
        if j['chrom']!=g['chrom']:raise ValueError('Reference chromosome mismatch')
        matches.append(dict(count_field=label,S6_name=j['name'],chrom=j['chrom'],left_boundary=j['left_boundary'],right_boundary=j['right_boundary'],
                            S6_strand=j['strand'],reference_strand=g['strand'],status='exact_label_strand_concordant' if j['strand']==g['strand'] else 'exact_label_strand_conflict'))
    inputs.extend([cache/'pipeline_converter.txt',cache/'pipeline_rules.txt'])
    converter=(cache/'pipeline_converter.txt').read_text()
    if 'int(linea_split[1]) - 1' not in converter or 'int(linea_split[2]) + 1' not in converter:raise ValueError('Converter transformation changed')
    summary=dict(supplement_rows=len(junctions),assembly='hg38 as described by article Supplementary Table6 legend',culture='SH-SY5Y',
        culture_count_rows=len(cs),exact_run_links=len(links),condition_counts={c:sum(r['condition']==c for r in links) for c in ['control','TDP-43 KD']},
        exact_coordinate_labels=sum(r['status'].startswith('exact_label') for r in matches),fully_strand_concordant_labels=sum(r['status']=='exact_label_strand_concordant' for r in matches),
        strand_conflict_labels=[r['count_field'] for r in matches if r['status']=='exact_label_strand_conflict'],
        unresolved_aliases=[r['count_field'] for r in matches if r['status'].startswith('unresolved')],
        library_mapping_prediction_met=True,seven_coordinate_links_prediction_met=False,
        ready_for_inference=False,effects_calculated=False,BAM_or_FASTQ_downloaded=False,
        source_comment_vs_code='Executable uses STAR first-1,last+1, unlike stale commented end example; outputs are flanking boundaries, not assumed standard BED intron intervals')
    out.mkdir(parents=True,exist_ok=True)
    for name,rows in [('S6_molecular_projection',junctions),('SHSY5Y_library_links',links),('count_field_coordinate_links',matches)]:
        with (out/(name+'.tsv')).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'run.json').write_text(json.dumps(dict(date='2026-10-30',python=platform.python_version(),dependencies={'xlrd':xlrd.__version__},
       parent_commit='04668868e1840b3f6600b9f2eb245339c656fe66',random_seed=None,
       hashes={str(p):sha(p) for p in inputs},reference_scope='Reused GENCODE v47 gene index from previous audited reference, not new whole-GTF revalidation'),indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for x in ['cache','culture','reference','out']:p.add_argument('--'+x,type=Path,required=True)
    a=p.parse_args();main(a.cache,a.culture,a.reference,a.out)
