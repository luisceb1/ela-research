"""Bounded public metadata/count retrieval. Does not fetch sequence reads."""
import concurrent.futures
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1] / 'reports/gse296714-design-20261101'
SOURCES = {
    'series.soft': 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE296714&targ=self&form=text&view=full',
    'family.soft': 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE296714&targ=all&form=text&view=full',
    'gene_counts.csv.gz': 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE296nnn/GSE296714/suppl/GSE296714_gene_counts.humphrey_i3_cortical.csv.gz',
    'article.xml': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12586162/fullTextXML',
    'zenodo.json': 'https://zenodo.org/api/records/15538002',
    'gene_counts_geo.csv.gz': 'https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE296714&format=file&file=GSE296714%5Fgene%5Fcounts%2Ehumphrey%5Fi3%5Fcortical%2Ecsv%2Egz',
    'ena.tsv': 'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA1256902&result=read_run&fields=run_accession,experiment_accession,sample_accession,secondary_sample_accession,sample_alias,experiment_alias,library_layout,read_count,base_count,fastq_bytes,fastq_md5&format=tsv',
}

def retrieve(item):
    name, url = item
    receipt = {'name': name, 'url': url, 'retrieved_at_utc': datetime.now(timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ELA-research-public-data-audit/1.0'})
        with urllib.request.urlopen(req, timeout=25) as response:
            data = response.read(20_000_001)
            if len(data) > 20_000_000:
                raise ValueError('20 MB response limit exceeded')
            receipt.update(status=response.status, final_url=response.url,
                           content_type=response.headers.get('Content-Type'),
                           bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        (ROOT / 'sources' / name).write_bytes(data)
        receipt['saved'] = True
    except Exception as exc:
        receipt.update(saved=False, error=f'{type(exc).__name__}: {exc}')
    return receipt

if __name__ == '__main__':
    (ROOT / 'sources').mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        receipts = list(pool.map(retrieve, SOURCES.items()))
    output = ROOT / 'retrievals.json'
    if output.exists():
        output = ROOT / ('retrievals-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.json')
    output.write_text(json.dumps(receipts, indent=2) + '\n')
    print(json.dumps(receipts, indent=2))
