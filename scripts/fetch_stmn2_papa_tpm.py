"""Retrieve only the preselected Humphrey TPM archive member."""
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from fetch_gse296714_zip_metadata import extract_member, URL, TOTAL

OUT = Path(__file__).resolve().parents[1] / 'reports/stmn2-papa-tpm-reproduction-20261101'

if __name__ == '__main__':
    entry = json.loads((OUT / 'execution_plan.json').read_text())['tpm_member']
    start = entry['offset']
    end = start + 30 + 65535 + 65535 + entry['compressed'] - 1
    expected_range = f'bytes {start}-{end}/{TOTAL}'
    cache = OUT / 'sources/tpm.tsv'
    cache.parent.mkdir(parents=True, exist_ok=True)
    if cache.exists():
        raise SystemExit('TPM cache exists; verify its receipt and reuse it')
    receipt = {'url': URL, 'member': entry['name'], 'range': f'bytes={start}-{end}',
               'at_utc': datetime.now(timezone.utc).isoformat(), 'full_zip_downloaded': False}
    try:
        req = urllib.request.Request(URL, headers={'Range': receipt['range']})
        with urllib.request.urlopen(req, timeout=25) as response:
            receipt.update(status=response.status, content_range=response.headers.get('Content-Range'))
            if response.status != 206 or receipt['content_range'] != expected_range:
                raise ValueError('Range mismatch; full ZIP refused')
            block = response.read(end - start + 2)
        if len(block) != end - start + 1:
            raise ValueError('Range length mismatch')
        data = extract_member(block, entry, max_uncompressed=10_000_000)
        cache.write_bytes(data)
        receipt.update(saved=True, transferred_bytes=len(block), member_bytes=len(data),
                       range_sha256=hashlib.sha256(block).hexdigest(),
                       member_sha256=hashlib.sha256(data).hexdigest(), crc_verified=True)
    except Exception as exc:
        receipt.update(saved=False, error=f'{type(exc).__name__}: {exc}')
    (OUT / 'retrieval.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))
    if not receipt.get('saved'):
        raise SystemExit(1)
