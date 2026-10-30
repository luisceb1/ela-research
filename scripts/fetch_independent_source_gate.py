"""Fetch only the fixed processed/technical inputs in the source-gate manifest."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--cache', type=Path, required=True)
    a = p.parse_args()
    a.cache.mkdir(parents=True, exist_ok=True)
    logs = []
    for s in json.loads(a.manifest.read_text())['sources']:
        dst = a.cache/s['cache_file']
        try:
            if dst.exists() and hashlib.sha256(dst.read_bytes()).hexdigest() == s['sha256']:
                logs.append({'id': s['id'], 'status': 'verified_cache'})
                continue
            if s['bytes'] > 100_000_000:
                raise ValueError('processed input exceeds fixed 100 MB cap')
            with urllib.request.urlopen(s['url'], timeout=40) as r:
                b = r.read(s['bytes']+1)
            if len(b) != s['bytes'] or hashlib.sha256(b).hexdigest() != s['sha256']:
                raise ValueError('download size/hash differs from fixed manifest')
            tmp = dst.with_suffix(dst.suffix+'.partial')
            tmp.write_bytes(b)
            tmp.replace(dst)
            logs.append({'id': s['id'], 'status': 'downloaded_and_verified'})
        except Exception as e:
            logs.append({'id': s['id'], 'status': 'error', 'error': type(e).__name__+': '+str(e)})
            (a.cache/'fetch_log.json').write_text(json.dumps(logs, indent=2)+'\n')
            raise
    (a.cache/'fetch_log.json').write_text(json.dumps(logs, indent=2)+'\n')
    print(json.dumps({'verified_inputs': len(logs)}))


if __name__ == '__main__':
    main()
