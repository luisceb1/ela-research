#!/usr/bin/env python3
"""Bounded immutable-index download/extraction; no read alignment."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tarfile
import time
import urllib.request


def safe_name(name):
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name or not p.parts:
        raise ValueError('Unsafe archive path')
    return p


def check_space(free_bytes, reserve, projected_total, limit):
    if projected_total > limit or free_bytes < reserve:
        raise ValueError('Disk budget exceeded')


def download(manifest, archive, out, timeout=1800):
    size = manifest['size_bytes']
    limits = manifest['resource_limits']
    archive.parent.mkdir(parents=True, exist_ok=True)
    check_space(shutil.disk_usage(archive.parent).free - size,
                limits['reserve_disk_bytes'], size, limits['additional_disk_bytes'])
    if archive.exists():
        raise ValueError('Archive exists; require explicit verified reuse, not overwrite')
    start = time.monotonic()
    req = urllib.request.Request(manifest['pinned_url'])
    result = {'url': manifest['pinned_url'], 'expected_bytes': size, 'complete': False}
    digest = hashlib.sha256()
    n, last = 0, start
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            headers = dict(response.headers)
            if response.status != 200 or int(response.headers.get('Content-Length', '-1')) != size:
                raise ValueError('HTTP status/size mismatch')
            if response.headers.get('x-amz-version-id') != manifest['s3_version_id'] or response.headers.get('ETag') != manifest['etag']:
                raise ValueError('Immutable object identity mismatch')
            result['headers'] = headers
            with archive.open('xb') as target:
                while True:
                    if time.monotonic() - start > timeout:
                        raise TimeoutError('Download time budget exceeded')
                    chunk = response.read(8*1024**2)
                    if not chunk:
                        break
                    n += len(chunk)
                    if n > size:
                        raise ValueError('Download exceeds expected size')
                    check_space(shutil.disk_usage(archive.parent).free - len(chunk), limits['reserve_disk_bytes'], n, limits['additional_disk_bytes'])
                    digest.update(chunk)
                    target.write(chunk)
                    if time.monotonic() - last > 15:
                        print(f'downloaded {n}/{size} bytes', flush=True)
                        last = time.monotonic()
        if n != size:
            raise ValueError('Truncated download')
        result['complete'] = True
    except Exception as exc:
        result['error'] = type(exc).__name__ + ': ' + str(exc)
        raise
    finally:
        result.update(bytes=n, elapsed_seconds=time.monotonic()-start, sha256=digest.hexdigest(),
                      hash_is_independent_expected_checksum=False)
        out.write_text(json.dumps(result, indent=2)+'\n')
    return result


def extract(archive, destination, manifest, download_record, out):
    if not download_record.get('complete') or archive.stat().st_size != manifest['size_bytes']:
        raise ValueError('No complete verified download')
    digest = hashlib.sha256()
    with archive.open('rb') as source:
        for chunk in iter(lambda: source.read(8*1024**2), b''): digest.update(chunk)
    if digest.hexdigest() != download_record['sha256']:
        raise ValueError('Archive bytes changed since download')
    limits = manifest['resource_limits']
    destination.mkdir(parents=True, exist_ok=False)
    entries, extracted = [], 0
    start = time.monotonic()
    with gzip.open(archive, 'rb') as gz:
        with tarfile.open(fileobj=gz, mode='r|') as tar:
            for member in tar:
                rel = safe_name(member.name)
                if not (member.isdir() or member.isfile()):
                    raise ValueError('Links/special archive members forbidden')
                if member.size < 0:
                    raise ValueError('Invalid member size')
                projected = manifest['size_bytes'] + extracted + member.size
                check_space(shutil.disk_usage(destination).free-member.size,
                            limits['reserve_disk_bytes'], projected, limits['additional_disk_bytes'])
                path = destination.joinpath(*rel.parts)
                if member.isdir():
                    path.mkdir(parents=True, exist_ok=True)
                    continue
                path.parent.mkdir(parents=True, exist_ok=True)
                n, h = 0, hashlib.sha256()
                with tar.extractfile(member) as source, path.open('xb') as target:
                    for chunk in iter(lambda: source.read(8*1024**2), b''):
                        n += len(chunk); h.update(chunk); target.write(chunk)
                if n != member.size: raise ValueError('Truncated tar member')
                extracted += n
                entries.append({'name': member.name, 'bytes': n, 'sha256': h.hexdigest()})
                print(f'extracted {member.name}: {n} bytes', flush=True)
        # Drain the gzip stream so its trailing CRC/ISIZE are actually verified.
        while gz.read(8*1024**2): pass
    result = {'gzip_crc_validated': True, 'archive_sha256': digest.hexdigest(),
              'files': entries, 'extracted_bytes': extracted,
              'archive_plus_extracted_bytes': archive.stat().st_size+extracted,
              'elapsed_seconds': time.monotonic()-start, 'index_accepted': False}
    out.write_text(json.dumps(result, indent=2)+'\n')
    return result


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('mode', choices=['download', 'extract'])
    p.add_argument('--manifest', required=True)
    p.add_argument('--archive', required=True)
    p.add_argument('--report', required=True)
    p.add_argument('--download-record')
    p.add_argument('--destination')
    a = p.parse_args()
    m = json.loads(Path(a.manifest).read_text())
    out = Path(a.report); out.parent.mkdir(parents=True, exist_ok=True)
    if a.mode == 'download': download(m, Path(a.archive), out)
    else:
        if not a.destination or not a.download_record: p.error('extract requires destination and download-record')
        extract(Path(a.archive), Path(a.destination), m, json.loads(Path(a.download_record).read_text()), out)


if __name__ == '__main__': main()
