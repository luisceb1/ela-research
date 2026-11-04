"""Bounded public metadata search; no effect estimates or clinical data."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import platform
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 5_000_000
TIMEOUT = 25
TITLE = 'UNC13A splice correction rescues synaptic dysfunction induced by TDP-43 loss'
OLD_TITLE = 'Loss of TDP-43 induces synaptic dysfunction that is rescued by UNC13A splice-switching ASOs'


def query(base, params):
    return base + '?' + urllib.parse.urlencode(params)


JOBS = [
    ('crossref-new', query('https://api.crossref.org/works', {'query.title': TITLE, 'rows': 10}), None),
    ('crossref-old', query('https://api.crossref.org/works', {'query.title': OLD_TITLE, 'rows': 10}), None),
    ('datacite', query('https://api.datacite.org/dois', {'query': 'UNC13A', 'page[size]': 100}), None),
    ('zenodo', query('https://zenodo.org/api/records', {'q': 'UNC13A', 'size': 50}), None),
    ('figshare', 'https://api.figshare.com/v2/articles/search', {'search_for': 'UNC13A', 'limit': 100}),
    ('biostudies-index', query('https://www.ebi.ac.uk/biostudies/api/v1/search', {'query': 'UNC13A', 'pageSize': 100}), None),
    ('biostudies-k24', 'https://www.ebi.ac.uk/biostudies/api/v1/studies/S-EPMC11230273', None),
    ('epmc-title', query('https://www.ebi.ac.uk/europepmc/webservices/rest/search', {'query': 'TITLE:"UNC13A splice correction"', 'format': 'json', 'pageSize': 100, 'resultType': 'core'}), None),
    ('epmc-author', query('https://www.ebi.ac.uk/europepmc/webservices/rest/search', {'query': 'AUTH_LAST:Keuss AND UNC13A', 'format': 'json', 'pageSize': 100, 'resultType': 'core'}), None),
    ('epmc-k24-xml', 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11230273/fullTextXML', None),
    ('biorxiv-versions', 'https://api.biorxiv.org/details/biorxiv/10.1101/2024.06.20.599684', None),
]


def project(name, obj):
    if name.startswith('crossref'):
        return {'total': obj['message'].get('total-results'), 'items': [
            {k: v.get(k) for k in ('DOI', 'title', 'URL', 'relation', 'link', 'published', 'resource')}
            for v in obj['message']['items']]}
    if name == 'datacite':
        return {'total': obj.get('meta', {}).get('total'), 'items': [
            {k: v['attributes'].get(k) for k in ('doi', 'titles', 'url', 'relatedIdentifiers', 'types')}
            for v in obj.get('data', [])], 'next': obj.get('links', {}).get('next')}
    if name == 'figshare':
        return [{k: v.get(k) for k in ('id', 'title', 'doi', 'url', 'url_public_html')} for v in obj]
    if name == 'zenodo':
        return {'total': obj.get('hits', {}).get('total'), 'items': [
            {'id': v.get('id'), 'title': v.get('metadata', {}).get('title'),
             'doi': v.get('doi'), 'files': v.get('files', [])}
            for v in obj.get('hits', {}).get('hits', [])]}
    if name == 'biostudies-k24':
        def files(node):
            found = []
            if isinstance(node, dict):
                if 'path' in node:
                    found.append({k: node.get(k) for k in ('path', 'size', 'type')})
                for v in node.values(): found.extend(files(v))
            elif isinstance(node, list):
                for v in node: found.extend(files(v))
            return found
        return {'accno': obj.get('accno'), 'attributes': obj.get('attributes'), 'files': files(obj)}
    if name.startswith('epmc-'):
        return {'total': obj.get('hitCount'), 'next': obj.get('nextCursorMark'), 'items': [
            {k: v.get(k) for k in ('id', 'source', 'pmcid', 'doi', 'title', 'firstPublicationDate', 'fullTextUrlList', 'hasSuppl', 'commentCorrectionList')}
            for v in obj.get('resultList', {}).get('result', [])]}
    if name == 'biorxiv-versions':
        return {'messages': obj.get('messages'), 'items': [
            {k: v.get(k) for k in ('title', 'date', 'version', 'doi', 'published', 'jatsxml')}
            for v in obj.get('collection', [])]}
    return obj


def fetch(job):
    name, url, body = job
    rec = {'id': name, 'url': url, 'method': 'POST-search' if body else 'GET', 'query_body': body,
           'retrieved_at': datetime.now(ZoneInfo('Europe/Madrid')).isoformat()}
    start = time.monotonic()
    try:
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, headers={'User-Agent': 'ela-research-public-source-audit/1.0', 'Accept': 'application/json, application/xml, text/xml', **({'Content-Type': 'application/json'} if body else {})})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            raw = response.read(LIMIT + 1)
            rec.update(status=response.status, content_type=response.headers.get('Content-Type'), final_url=response.url, bytes=len(raw))
            if len(raw) > LIMIT: raise ValueError('response_size_limit_exceeded')
            rec['sha256_response'] = hashlib.sha256(raw).hexdigest()
            if name.endswith('-xml'):
                import xml.etree.ElementTree as ET
                tree = ET.fromstring(raw)
                rec['xml_root'] = tree.tag
                rec['title'] = ' '.join(tree.find('.//article-title').itertext())
                rec['supplement_links'] = [dict(el.attrib) for el in tree.iter() if el.tag.rsplit('}', 1)[-1] in ('supplementary-material', 'media', 'ext-link')]
                rec['availability_sections'] = [' '.join(el.itertext()) for el in tree.iter('sec') if any(t in ' '.join(el.itertext()).lower()[:150] for t in ('data availability', 'code availability'))]
            else:
                rec['result'] = project(name, json.loads(raw))
    except Exception as exc:
        rec.update(error_type=type(exc).__name__, error=str(exc))
        if isinstance(exc, urllib.error.HTTPError): rec['status'] = exc.code
    rec['elapsed_seconds'] = round(time.monotonic() - start, 3)
    return rec


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, JOBS))
    out = {'python': sys.version, 'platform': platform.platform(), 'parameters': {'timeout_seconds': TIMEOUT, 'max_response_bytes': LIMIT, 'max_workers': 4}, 'results': results}
    (ROOT / 'api-results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    for rec in results:
        r = rec.get('result', {})
        print(rec['id'], rec.get('status'), rec.get('error'), 'items=', len(r.get('items', [])) if isinstance(r, dict) else len(r))


if __name__ == '__main__': main()
