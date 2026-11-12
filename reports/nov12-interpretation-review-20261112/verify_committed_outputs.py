"""Check the reviewed committed outputs, without acquiring or reprocessing raw inputs."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = 'f6e66099103986507b9ad52c34fc5fc39c478fe3'

def read(path):
    return json.loads((ROOT / path).read_text())

gtex_path = 'reports/gtex-brain-negative-control-20261112/summary_BRAIN.json'
gtex = read(gtex_path)
old = json.loads(subprocess.check_output(['git', 'show', f'{BASE}:{gtex_path}'], cwd=ROOT))
old['comparability_window']['definition'] = gtex['comparability_window']['definition']
assert old == gtex, 'Only the window description may change'
assert gtex['n_samples'] == 2931
assert gtex['matrix_header']['rows'] == 9484210
assert gtex['window_totals'] == {'libraries': 26, 'cryptic_left_positive': 0, 'cryptic_right_positive': 0}
assert sum(v['libraries_in_window'] for v in gtex['by_tissue'].values()) == 26
# Resolve exact deposit labels, retaining all three named cortical categories.
cortical = [k for k in gtex['by_tissue'] if 'Cortex' in k or 'cortex' in k]
assert len(cortical) == 3
assert sum(gtex['by_tissue'][k]['libraries_in_window'] for k in cortical) == 15
assert len(gtex['libraries_with_any_cryptic_read']) == 7
assert gtex['per_junction']['canonical']['samples_with_any_read'] == 2655
assert gtex['per_junction']['cryptic_left']['max'] == 2
assert gtex['per_junction']['cryptic_right']['max'] == 1

kd_path = 'reports/questionA-detection-SRP069787-20261112/results_SRP069787.json'
kd = read(kd_path)
assert kd['n_samples'] == 16
assert {x['run']: x['counts']['canonical'] for x in kd['samples'] if x['sample_title'].startswith('TDP43 Knockdown')} == {'SRR3153259': 9, 'SRR3153260': 2}
assert all(x['counts'][j] == 0 for x in kd['samples'] for j in ['cryptic_left', 'cryptic_right'])
sp_path = 'reports/nonals-spinal-source-20261112/results_SRP097615.json'
sp = read(sp_path)
assert sp['n_samples'] == 39
assert sp['assay_shape']['total_junctions'] == 121078
assert all(x['counts']['canonical'] == 0 for x in sp['samples'])

cortex = (ROOT / 'reports/target-als-cortex-20261111/REPORT.md').read_text()
assert '| **ALS Spectrum MND** | 84 |' in cortex and '| 102 |' in cortex
assert '| **Non-Neurological Control** | 13 |' in cortex and '| 148 |' in cortex

preserved = [kd_path, sp_path, 'research/references/unc13a_targets_sealed.json', 'scripts/recount3_junction_probe.py']
preserved += [str(p.relative_to(ROOT)) for p in (ROOT / 'research/plans').glob('2026-11-12-*')]
for p in preserved:
    before = subprocess.check_output(['git', 'show', f'{BASE}:{p}'], cwd=ROOT)
    assert before == (ROOT / p).read_bytes(), p

paths = [gtex_path, kd_path, sp_path, 'reports/target-als-cortex-20261111/REPORT.md']
manifest = {p: {'base_sha256': hashlib.sha256(subprocess.check_output(['git', 'show', f'{BASE}:{p}'], cwd=ROOT)).hexdigest(), 'reviewed_sha256': hashlib.sha256((ROOT / p).read_bytes()).hexdigest()} for p in paths}
print(json.dumps({'status': 'PASS', 'scope': 'committed derived outputs only; no raw-input rerun', 'base_commit': BASE, 'checks': ['GTEx recorded totals and cortical window subset', 'KD recorded canonical and cryptic counts', 'SRP097615 recorded failed positive control', 'GTEx numerical fields unchanged', 'source group medians', 'plans, sealed targets, probe and two result files unchanged'], 'sources': manifest}, indent=2))
