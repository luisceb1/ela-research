"""Prepare a disabled local measurement descriptor; no network or alignment path exists."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports/local-raw-feasibility-20261112'
SELECTED = ('GSM8009878', 'GSM8009881')
EXPECTED_INPUT_BYTES = 12_826_593_031


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def selected_inputs(path):
    with Path(path).open(newline='') as f:
        rows = [r for r in csv.DictReader(f, delimiter='\t') if r['gsm'] in SELECTED]
    if len(rows) != 4 or {r['gsm'] for r in rows} != set(SELECTED):
        raise ValueError('Expected exactly two files for each fixed library')
    if any(sum(r['gsm'] == g for r in rows) != 2 for g in SELECTED):
        raise ValueError('Each selected library must have two FASTQs')
    if len({r['url'] for r in rows}) != 4:
        raise ValueError('Duplicate FASTQ URL')
    if any(r['geo_series'] != 'GSE252892' or r['strategy'] != 'RNA-Seq' or r['layout'] != 'PAIRED' or not r['url'].startswith('https://ftp.sra.ebi.ac.uk/') for r in rows):
        raise ValueError('Unexpected source or assay metadata')
    if sum(int(r['compressed_bytes']) for r in rows) != EXPECTED_INPUT_BYTES:
        raise ValueError('Fixed input-byte total changed')
    return rows


def verify_index(directory, expected):
    entries = expected['verified_files']
    names = {Path(x['name']).name for x in entries}
    if names != {f'genome.{i}.ht2' for i in range(1,9)} | {'make_hg38.sh'}:
        raise ValueError('Unexpected index inventory')
    out = []
    for item in entries:
        path = Path(directory) / Path(item['name']).name
        if not path.is_file() or path.stat().st_size != item['bytes']:
            raise ValueError(f'Index missing or size mismatch: {path.name}')
        digest = sha256(path)
        if digest != item['sha256']:
            raise ValueError(f'Index hash mismatch: {path.name}')
        out.append({'name': path.name, 'bytes': path.stat().st_size, 'sha256': digest})
    return out


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True, timeout=10).strip()


def prepare(index_dir, aligner, inspector, output):
    output = Path(output).expanduser().resolve()
    if output.exists():
        raise ValueError('Output already exists; no overwrite')
    if output == ROOT or ROOT in output.parents:
        raise ValueError('Descriptor must be outside the checkout')
    if git('status', '--porcelain', '--untracked-files=all'):
        raise ValueError('Checkout must be clean')
    manifest = REPORT / 'fastq-manifest.tsv'
    rows = selected_inputs(manifest)
    expected_path = ROOT / 'reports/hisat2-index-inspection-20261031/verified_index.json'
    verified = verify_index(Path(index_dir), json.loads(expected_path.read_text()))
    tools = {}
    for name, candidate in [('aligner', aligner), ('inspector', inspector)]:
        candidate = Path(candidate).resolve(strict=True)
        result = subprocess.run([str(candidate), '--version'], capture_output=True, text=True, timeout=10, check=True)
        if 'version 2.2.3' not in result.stdout:
            raise ValueError(f'Unexpected {name} version')
        tools[name] = {'path': str(candidate), 'sha256': sha256(candidate), 'version_output': result.stdout}
    import pysam
    if pysam.__version__ != '0.23.3':
        raise ValueError('Expected existing PySAM 0.23.3 environment')
    targets = ROOT / 'research/references/unc13a_targets_sealed.json'
    target_sha = sha256(targets)
    if target_sha != 'e35f6e05016b30eab89f8d3aacc2d4ec101840e24e2b6f07159e6c5235d0bc3a':
        raise ValueError('Sealed targets changed')
    descriptor = {
        'status': 'prepared_disabled', 'execution_enabled': False,
        'scope': 'two fixed libraries for technical measurement only; no matched-culture claim, effect, PSI or inference',
        'repository_commit': git('rev-parse', 'HEAD'),
        'repository_root': str(ROOT), 'preparer_sha256': sha256(__file__),
        'python': {'executable': sys.executable, 'version': sys.version, 'pysam': pysam.__version__},
        'tools': tools, 'index_directory': str(Path(index_dir).resolve()),
        'index_files': verified, 'expected_index_record_sha256': sha256(expected_path),
        'targets_sha256': target_sha, 'manifest_sha256': sha256(manifest),
        'input_files': rows, 'advertised_raw_input_bytes': EXPECTED_INPUT_BYTES,
        'raw_bytes_downloaded_by_preparation': 0,
        'unresolved_before_execution': [
            'Runner implementation and tests for complete FASTQ processing and junction counts',
            'Explicit transfer/disk/time limits and stop/cleanup policy',
            'Verified reference/coordinate and assay/strand/adapter compatibility',
            'Measured local resource behaviour; virtual disk capacity is not physical free space',
            'Review of the concrete execution/budget before raw transfer',
        ],
        'warning': 'This descriptor has no execution command. Do not edit it to enable the old pilot.',
    }
    encoded = (json.dumps(descriptor, indent=2, ensure_ascii=False) + '\n').encode()
    with output.open('xb') as f:
        f.write(encoded)
    return {'status': 'prepared_disabled', 'output': str(output), 'descriptor_sha256': hashlib.sha256(encoded).hexdigest(), 'index_members_verified': len(verified), 'input_files': len(rows), 'advertised_raw_input_bytes': EXPECTED_INPUT_BYTES, 'raw_bytes_downloaded': 0}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--index-dir', type=Path, required=True)
    p.add_argument('--aligner', type=Path, required=True)
    p.add_argument('--inspector', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(prepare(args.index_dir, args.aligner, args.inspector, args.output), indent=2))


if __name__ == '__main__':
    main()
