"""Fetch only the ZIP central directory; enumerate files without full download."""
import hashlib
import io
import json
import struct
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'reports/gse296714-design-20261101'
URL = 'https://zenodo.org/api/records/15538003/files/2025-05-28__tdp43-apa__data.zip/content'
TOTAL = 831190727


def request_range(start, end):
    expected = f'bytes {start}-{end}/{TOTAL}'
    req = urllib.request.Request(URL, headers={'Range': f'bytes={start}-{end}'})
    with urllib.request.urlopen(req, timeout=25) as response:
        if response.status != 206 or response.headers.get('Content-Range') != expected:
            raise ValueError('Range mismatch; refusing full ZIP')
        data = response.read(end - start + 2)
    if len(data) != end - start + 1:
        raise ValueError('Range length mismatch')
    return data


def inventory(central, offset):
    archive = zipfile.ZipFile(io.BytesIO(central))
    return [{'name': i.filename, 'compressed': i.compress_size, 'uncompressed': i.file_size,
             'crc': i.CRC, 'offset': i.header_offset + offset, 'method': i.compress_type}
            for i in archive.infolist()]


if __name__ == '__main__':
    receipts = []
    try:
        tail_start = TOTAL - 262144
        tail = request_range(tail_start, TOTAL - 1)
        (ROOT / 'sources/archive-tail.bin').write_bytes(tail)
        position = tail.rfind(b'PK\x05\x06')
        if position < 0:
            raise ValueError('Missing EOCD')
        end = struct.unpack_from('<4s4H2LH', tail, position)
        size, offset = end[5:7]
        if end[1] or end[2] or size > 2_000_000 or offset + size != TOTAL - 22:
            raise ValueError('Unexpected ZIP layout')
        central = request_range(offset, TOTAL - 1)
        (ROOT / 'sources/archive-central.bin').write_bytes(central)
        rows = inventory(central, offset)
        (ROOT / 'archive_inventory.json').write_text(json.dumps(rows, indent=2) + '\n')
        for name, start, data in [('archive-tail.bin', tail_start, tail), ('archive-central.bin', offset, central)]:
            receipts.append({'url': URL, 'name': name, 'range': f'bytes={start}-{TOTAL-1}',
                             'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                             'saved': True, 'at_utc': datetime.now(timezone.utc).isoformat()})
        print(f'Indexed {len(rows)} entries using {len(tail) + len(central)} bytes')
    except Exception as exc:
        receipts.append({'url': URL, 'saved': False, 'error': f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        (ROOT / 'retrievals-index-replay.json').write_text(json.dumps(receipts, indent=2) + '\n')
