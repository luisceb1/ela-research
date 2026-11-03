"""Technical resource plan only. Reads local metadata; never downloads FASTQ."""
import csv
import hashlib
import json
import os
import shutil
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'reports/gse296714-raw-pilot-plan-20261101'
SAMPLES=BASE/'reports/gse296714-design-20261101/samples.tsv'

def main():
    samples=list(csv.DictReader(SAMPLES.open(),delimiter='\t'))
    if len(samples)!=12 or len({s['run'] for s in samples})!=12: raise ValueError('Unexpected library set')
    metadata=list(csv.DictReader((OUT/'ena-metadata.tsv').open(),delimiter='\t'))
    selected=[]
    for group in ['control','TDP43_KD']:
        row=min((r for r in samples if r['group']==group),key=lambda r:(int(r['fastq_bytes_ena']),r['run']))
        ena,=[r for r in metadata if r['run_accession']==row['run']]
        if ena['experiment_accession']!=row['srx'] or ena['sample_accession']!=row['biosample'] or ena['sample_alias']!=row['library']:raise ValueError('Identity mismatch')
        sizes=[int(x) for x in ena['fastq_bytes'].split(';')]
        md5=ena['fastq_md5'].split(';');urls=ena['fastq_ftp'].split(';')
        if ena['library_layout']!='PAIRED' or len(sizes)!=2 or len(md5)!=2 or len(urls)!=2:raise ValueError('Expected exactly two mates')
        if sum(sizes)!=int(row['fastq_bytes_ena']) or md5!=[row['fastq_md5_r1'],row['fastq_md5_r2']]:raise ValueError('Metadata changed')
        selected.append({'library':row['library'],'gsm':row['gsm'],'srx':row['srx'],'biosample':row['biosample'],'run':row['run'],'group':group,'read_count_ena':int(ena['read_count']),'fastq_bytes':sum(sizes),'mates':[{'url':'https://'+u,'bytes':n,'md5':m} for u,n,m in zip(urls,sizes,md5)]})
    plan={'selection_rule':'minimum compressed FASTQ bytes per condition; tie-break run accession; no effect-based selection','selected':selected,'selected_fastq_bytes':sum(r['fastq_bytes'] for r in selected),'all12_fastq_bytes':sum(int(r['fastq_bytes_ena']) for r in samples),'samples_sha256':hashlib.sha256(SAMPLES.read_bytes()).hexdigest(),'ena_metadata_sha256':hashlib.sha256((OUT/'ena-metadata.tsv').read_bytes()).hexdigest(),'limits':{'threads':2,'memory_bytes':6*1024**3,'additional_disk_bytes':25*1024**3,'reserve_free_disk_bytes':8*1024**3,'raw_plus_reference_transfer_bytes':12_000_000_000,'all_transfer_elapsed_seconds':3600,'prefix_pairs_per_library':1_000_000,'alignment_seconds_per_library':900},'raw_execution_ready':False,'blockers':['PE fragment-count contract and independent parser check not implemented','aligner and index not restored/verified in current environment','library strand orientation and UNC13A coordinate contract not fixed'],'raw_downloaded_in_this_task':False,'biological_contrast_permitted':False}
    (OUT/'PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
    environment={'cpu_count_os':os.cpu_count(),'disk':shutil.disk_usage(BASE)._asdict(),'binaries':{n:shutil.which(n) for n in ['hisat2','STAR','samtools']}}
    for path in ['/sys/fs/cgroup/memory.max','/sys/fs/cgroup/cpu.max']:
        environment[path]=Path(path).read_text().strip()
    (OUT/'environment.json').write_text(json.dumps(environment,indent=2)+'\n')
    print(json.dumps(plan,indent=2))

if __name__=='__main__':main()
