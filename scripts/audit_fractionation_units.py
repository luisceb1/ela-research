"""Project six baseline culture libraries; never infer biological units from labels."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import platform
import xml.etree.ElementTree as ET


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    names = ['fractionation_sdrf_resolved.source', 'unit_xml.source', 'units_supplement.pdf']
    hashes = {n: hashlib.sha256((a.cache/n).read_bytes()).hexdigest() for n in names}
    assert hashes[names[0]] == 'ff0772b7e85e51681edd2a3e85da248101160b09fd0001e63b9446e6c5a03449'
    assert hashes[names[1]] == '780feceea2f80509ef85062c01671b8f04657de466776913ad7f33ed5f9bb8ed'
    assert hashes[names[2]] == '55c515cd210590e02f7507e0adfe82ad6a059737f8313db877975888c5a48dfa'
    assert (a.cache/names[2]).read_bytes().startswith(b'%PDF-')
    root = ET.parse(a.cache/names[1])
    supplements = sorted({x.attrib['{http://www.w3.org/1999/xlink}href']
                          for x in root.iter('media') if '{http://www.w3.org/1999/xlink}href' in x.attrib})
    rows = list(csv.DictReader((a.cache/names[0]).read_text().splitlines(), delimiter='\t'))
    selected = {}
    for r in rows:
        if r['Factor Value[organism part]'] != 'cytosol':
            continue
        cond = r['Factor Value[stimulus]']
        if cond not in ['control cells baseline', 'TDP-43 knockdown baseline']:
            continue
        record = {'run': r['Comment[ENA_RUN]'], 'sample_accession': r['Comment[ENA_SAMPLE]'],
                  'assay': r['Assay Name'], 'derived_file': r['Derived Array Data File'],
                  'condition': cond, 'independent_culture_unit': None}
        assert r['Assay Name'] not in selected or selected[r['Assay Name']] == record
        selected[r['Assay Name']] = record
    out = sorted(selected.values(), key=lambda x: x['run'])
    assert len(out) == len({r['run'] for r in out}) == len({r['sample_accession'] for r in out}) == 6
    assert sorted(collections.Counter(r['condition'] for r in out).values()) == [3, 3]
    a.out.mkdir(parents=True, exist_ok=True)
    result = {'python': platform.python_version(), 'source_sha256': hashes,
              'libraries': out, 'supplement_inventory': supplements,
              'independent_units_certified': False, 'effect_analysis_executed': False,
              'scope': 'Six technical links, not six certified biological cultures. PDF reviewed separately.'}
    (a.out/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'technical_libraries': 6, 'independent_units_certified': False}))


if __name__ == '__main__':
    main()
