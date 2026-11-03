"""Extract preselected cell-culture metadata/count/annotation members by HTTP ranges.

Requires the saved central directory and inventory. Does not download the full ZIP,
sequence reads, or any postmortem table. No archive members are executed.
"""
import hashlib
import argparse
import json
import struct
import urllib.request
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'reports/gse296714-design-20261101'
URL = 'https://zenodo.org/api/records/15538003/files/2025-05-28__tdp43-apa__data.zip/content'
TOTAL = 831190727
MEMBER = 'tdp43-apa/preprocessing/data/PAPA/sample_tables/humphrey_i3_cortical/humphrey_i3_cortical_underscore_sample_tbl.csv'
COUNTS = 'tdp43-apa/preprocessing/data/PAPA/i3_cortical_upf1_zanovello_novel/humphrey_i3_cortical/differential_apa/summarised_pas_quantification.counts.tsv'
ANNOTATION = 'tdp43-apa/misc/processed/cleaned.cryptics.all.novel_ref_combined.quant.gtf'


def extract_member(block, entry, max_uncompressed=100_000):
    if len(block) < 30 or block[:4] != b'PK\x03\x04':
        raise ValueError('Invalid local header')
    fields = struct.unpack_from('<4s5H3L2H', block)
    if fields[2] & 1 or fields[3] != entry['method']:
        raise ValueError('Encrypted member or method mismatch')
    name_len, extra_len = fields[-2:]
    name = block[30:30 + name_len].decode('utf-8')
    if name != entry['name']:
        raise ValueError('Member name mismatch')
    start = 30 + name_len + extra_len
    payload = block[start:start + entry['compressed']]
    if len(payload) != entry['compressed'] or entry['uncompressed'] > max_uncompressed:
        raise ValueError('Size limit or truncation')
    if entry['method'] != 8:
        raise ValueError('Expected deflate')
    decoder = zlib.decompressobj(-15)
    data = decoder.decompress(payload, entry['uncompressed'] + 1)
    if not decoder.eof or decoder.unused_data or len(data) != entry['uncompressed']:
        raise ValueError('Decompressed size/EOF mismatch')
    if zlib.crc32(data) != entry['crc']:
        raise ValueError('CRC mismatch')
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--counts', action='store_true', help='Fetch the preselected PAPA count member instead of metadata')
    selection.add_argument('--annotation', action='store_true', help='Fetch the processed cryptic annotation to identify target events')
    args = parser.parse_args()
    selected = ANNOTATION if args.annotation else COUNTS if args.counts else MEMBER
    output = 'cryptic_annotation.gtf' if args.annotation else 'papa_counts.tsv' if args.counts else 'humphrey_sample_table.csv'
    entries = json.loads((ROOT / 'archive_inventory.json').read_text())
    entry, = [row for row in entries if row['name'] == selected]
    # Local header: 30 bytes + at most 65535-byte filename + 65535-byte extra.
    start = entry['offset']
    end = min(TOTAL - 1, start + 30 + 65535 + 65535 + entry['compressed'] - 1)
    expected = f'bytes {start}-{end}/{TOTAL}'
    receipt = {'url': URL, 'member': selected, 'range': f'bytes={start}-{end}',
               'at_utc': datetime.now(timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(URL, headers={'Range': receipt['range']})
        with urllib.request.urlopen(request, timeout=25) as response:
            receipt.update(status=response.status, content_range=response.headers.get('Content-Range'))
            if response.status != 206 or response.headers.get('Content-Range') != expected:
                raise ValueError('Range mismatch; refusing full ZIP')
            block = response.read(end - start + 2)
        if len(block) != end - start + 1:
            raise ValueError('Range length mismatch')
        data = extract_member(block, entry, max_uncompressed=10_000_000 if args.counts or args.annotation else 100_000)
        (ROOT / 'sources' / output).write_bytes(data)
        receipt.update(saved=True, transferred_bytes=len(block), member_bytes=len(data),
                       range_sha256=hashlib.sha256(block).hexdigest(),
                       member_sha256=hashlib.sha256(data).hexdigest(), crc_verified=True)
    except Exception as exc:
        receipt.update(saved=False, error=f'{type(exc).__name__}: {exc}')
    receipt_name = 'retrievals-zip-annotation.json' if args.annotation else 'retrievals-zip-counts.json' if args.counts else 'retrievals-zip-member.json'
    (ROOT / receipt_name).write_text(json.dumps([receipt], indent=2) + '\n')
    print(json.dumps(receipt, indent=2))
