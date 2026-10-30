"""Compare published molecular counting regions to culture DEXSeq bins."""
import argparse
import csv
import gzip
import hashlib
import itertools
import json
import platform
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCE_HASH='daaf355a7cbd48b617d30201ba289d8f0c4efc9fbc2a23ca2f991c84e1d814f4'
FOCAL={'ENSG00000104435:E009','ENSG00000130477:E026','ENSG00000130477:E030','ENSG00000130477:E054'}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def interval(chrom,start,end,assembly,strand=None):
    if not chrom.startswith('chr') or not isinstance(start,int) or not isinstance(end,int) or start<1 or end<start:
        raise ValueError('Invalid closed interval')
    if strand not in (None,'+','-'):raise ValueError('Invalid strand')
    return dict(chrom=chrom,start=start,end=end,assembly=assembly,strand=strand)

def relation(a,b):
    if a['assembly']!=b['assembly']:raise ValueError('Assembly mismatch: no silent liftover')
    if a['chrom']!=b['chrom'] or (a['strand'] is not None and b['strand'] is not None and a['strand']!=b['strand']):
        return None
    overlap=max(0,min(a['end'],b['end'])-max(a['start'],b['start'])+1)
    distance=max(a['start']-b['end'],b['start']-a['end'],0)
    return dict(overlap_bp=overlap,boundary_distance_bp=distance,intervening_bases=max(0,distance-1))

def verify_assembly(soft,xml):
    with gzip.open(soft,'rt') as f:
        builds={l.split('Genome_build:',1)[1].strip() for l in f if l.startswith('!Sample_data_processing') and 'Genome_build:' in l}
    if builds!={'hg19'}:raise ValueError('Unexpected GEO genome build')
    root=ET.parse(xml).getroot()
    dois={e.text for e in root.findall('.//article-id') if e.get('pub-id-type')=='doi'}
    if '10.1038/s41593-018-0300-4' not in dois:raise ValueError('Unexpected dataset article')
    matches=[' '.join(p.itertext()) for p in root.findall('.//body//p') if 'FASTQ files were aligned to the GRCh37/hg19 reference genome' in ' '.join(p.itertext())]
    if len(matches)!=1:raise ValueError('Article assembly not uniquely verified')
    return dict(GEO_builds=sorted(builds),article_doi='10.1038/s41593-018-0300-4',assembly='GRCh37/hg19',
                short_excerpt='aligned to the GRCh37/hg19 reference genome',scope='Technical methods only; no individual observations exported')

def run(source,manifest,soft,xml,out):
    if sha(source)!=SOURCE_HASH:raise ValueError('DEXSeq original hash mismatch')
    cfg=json.loads(manifest.read_text()); assembly=verify_assembly(soft,xml)
    if cfg['assembly']!=assembly['assembly']:raise ValueError('Manifest assembly mismatch')
    evs={e['groupID']:e for e in cfg['events']};bins={g:[] for g in evs}
    with gzip.open(source,'rt') as f:
        for r in csv.DictReader(f):
            if r['groupID'] in bins:bins[r['groupID']].append(r)
    output=[];summary=[]
    for gid,rs in bins.items():
        e=evs[gid];ce=interval(e['chrom'],e['start'],e['end'],cfg['assembly'],e['strand'])
        if e['end']-e['start']+1!=e['expected_inclusive_width']:raise ValueError('Event width mismatch')
        if len(rs)!={'STMN2':10,'UNC13A':62}[e['gene']] or len({r['fragment'] for r in rs})!=len(rs):raise ValueError('Invalid target catalogue')
        these=[]
        for r in rs:
            start,end,width=(int(r['genomicData.'+x]) for x in ['start','end','width'])
            if end-start+1!=width:raise ValueError('DEXSeq width violates inclusive coordinates')
            b=interval(r['genomicData.seqnames'],start,end,cfg['assembly'],r['genomicData.strand'])
            rel=relation(b,ce)
            if rel is None:raise ValueError('Target bin chromosome/strand incompatible')
            overlaps=[]
            for ds,de in itertools.product([-1,0,1],repeat=2):
                moved=interval(e['chrom'],e['start']+ds,e['end']+de,cfg['assembly'],e['strand'])
                overlaps.append(relation(b,moved)['overlap_bp'])
            row=dict(gene=e['gene'],fragment=r['fragment'],focal_previous_discordance=r['fragment'] in FOCAL,assembly=cfg['assembly'],
                     chrom=b['chrom'],bin_start=start,bin_end=end,bin_width=width,bin_strand=b['strand'],
                     published_CE_start=e['start'],published_CE_end=e['end'],source_strand='unspecified',
                     **rel,maximum_overlap_under_endpoint_shifts=max(overlaps),source_doi=e['source_doi'])
            these.append(row);output.append(row)
        closest=min(these,key=lambda x:(x['boundary_distance_bp'],x['fragment']))
        summary.append(dict(gene=e['gene'],bins=len(rs),overlapping_bins=sum(r['overlap_bp']>0 for r in these),
                            endpoint_sensitivity_overlapping_bins=sum(r['maximum_overlap_under_endpoint_shifts']>0 for r in these),
                            nearest_bin=closest['fragment'],boundary_distance_bp=closest['boundary_distance_bp'],intervening_bases=closest['intervening_bases']))
    out.mkdir(parents=True,exist_ok=True)
    with (out/'bin_coordinate_comparison.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(output[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(output)
    (out/'summary.json').write_text(json.dumps(dict(events=summary,focal=[r for r in output if r['focal_previous_discordance']],
        prediction='No overlapping target bins for these two published hg19 counting regions',
        inference='Catalogue does not measure these CE intervals directly; no biological absence inferred',
        source_interval_formal_coordinate_base='Not expressly specified; inclusive interpretation and endpoint sensitivity reported'),indent=2)+'\n')
    (out/'assembly_projection.json').write_text(json.dumps(assembly,indent=2)+'\n')
    (out/'run.json').write_text(json.dumps(dict(python=platform.python_version(),dependencies='stdlib',date='2026-10-30',
        deterministic=True,parent_commit='c47afbe03818152f846cf8a4e9a6efdbcb80e319',endpoint_shifts=[-1,0,1],
        hashes={str(p):sha(p) for p in [source,manifest,soft,xml,Path(__file__)]},new_download=False,biological_replication=False,
        full_article_bytes_for_new_interval_sources_saved=False),indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for x in ['source','manifest','soft','xml','out']:p.add_argument('--'+x,type=Path,required=True)
    a=p.parse_args();run(a.source,a.manifest,a.soft,a.xml,a.out)
