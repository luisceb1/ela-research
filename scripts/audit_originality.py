"""Validate a manually curated evidence register; never infer novelty from searches."""
import argparse
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path


def validate(register):
    errors = []
    cutoff = date.fromisoformat(register['cutoff'])
    studies = register['studies']
    ids = [s['id'] for s in studies]
    if len(ids) != len(set(ids)):
        errors.append('duplicate study id')
    versions = [v for s in studies for v in s['versions']]
    if len(versions) != len(set(versions)):
        errors.append('version assigned to multiple families')
    for s in studies:
        if date.fromisoformat(s['date']) > cutoff:
            errors.append(s['id'] + ': after cutoff')
        if not s.get('locator') or not s.get('evidence'):
            errors.append(s['id'] + ': missing evidence locator')
        if s['access'] == 'abstract' and s.get('methods_verified'):
            errors.append(s['id'] + ': abstract cannot verify methods')
        if s['after_measured_deficit'] == 'yes' and not s.get('baseline_locator'):
            errors.append(s['id'] + ': measured deficit needs baseline locator')
        if len(s.get('quote', '').split()) > 25:
            errors.append(s['id'] + ': quote exceeds source budget')
    allowed = {'prior_art', 'extension', 'open_not_original', 'technical', 'unresolved'}
    for c in register['claims']:
        if c['classification'] not in allowed:
            errors.append(c['id'] + ': invalid classification')
        if not set(c['studies']).issubset(ids):
            errors.append(c['id'] + ': unknown study')
        if c.get('novelty_proven'):
            errors.append(c['id'] + ': novelty not established by this audit')
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--register', type=Path, default=Path('research/references/originality_evidence_20261029.json'))
    ap.add_argument('--out', type=Path, default=Path('reports/originality-audit/qc.json'))
    args = ap.parse_args()
    raw = args.register.read_bytes()
    data = json.loads(raw)
    errors = validate(data)
    result = {'cutoff': data['cutoff'], 'register_sha256': hashlib.sha256(raw).hexdigest(),
              'studies': len(data['studies']), 'claims': len(data['claims']),
              'classification_counts': dict(Counter(c['classification'] for c in data['claims'])),
              'errors': errors, 'scope': 'Register consistency only; no automatic scientific validation'}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
