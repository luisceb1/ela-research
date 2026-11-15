"""Verify bounded original STMN2 metadata; never replay or fetch raw inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_SHA = '7cbfa8d652ab35178717813e47fd2c66c6c71ff5612b359ff29da05b693756db'
PRIOR_SHA = 'c8751b9610512791ba40a613449ad332833ff557e8c371f96e118636361e4617'
PLAN = 'ela-gse252892-stmn2-control-20261114.json'
RUNTIME = 'acff06335ca1283b079c35ab0830a284e6d23258'
PLAN_SHA = '8379c7e56c0546623fac80c732935f29113f17e048b8625d85e1163e3f61b557'
GSMS = ('GSM8009878', 'GSM8009881')


def digest(b):
    return hashlib.sha256(b).hexdigest()


def verify(archive, prior_archive):
    raw = Path(archive).read_bytes()
    assert digest(raw) == ARCHIVE_SHA, 'Archive SHA256 mismatch'
    expected = {PLAN, PLAN+'.claimed.json', 'accepted.json', 'result.json',
                'supervision.json', 'worker.log'}
    expected.update(g+'/'+n for g in GSMS for n in
                    ('stmn2-counts.json', 'fastp.json', 'fastp.log',
                     'hisat2.log', 'hisat2-summary.txt'))
    with tarfile.open(archive, 'r:gz') as t:
        members = t.getmembers()
        assert len(members) == len(expected)
        assert {m.name for m in members} == expected
        assert all(m.isfile() and 0 < m.size < 2**20 for m in members)
        data = {m.name: t.extractfile(m).read() for m in members}
    j = lambda n: json.loads(data[n])
    plan, result, sup = j(PLAN), j('result.json'), j('supervision.json')
    assert digest(data[PLAN]) == PLAN_SHA
    assert plan['repository_commit'] == RUNTIME
    for name in (PLAN+'.claimed.json', 'accepted.json', 'supervision.json'):
        assert j(name)['plan_sha256'] == PLAN_SHA
        assert j(name)['network_bytes'] == 0
    assert result == json.loads((ROOT/'reports/gse252892-stmn2-result-20261115/user-reported-result.json').read_bytes())
    assert sup == json.loads((ROOT/'reports/gse252892-stmn2-result-20261115/user-reported-supervision.json').read_bytes())
    assert result['status'] == sup['status'] == 'completed'
    assert sup['failure'] is None and sup['cleanup_error'] is None
    assert j('worker.log') == {'status': 'worker_finished'}
    assert result['network_bytes'] == plan['caps']['network_bytes'] == 0
    assert sup['caps'] == plan['caps']
    for measured, limit in [('elapsed_seconds', 'wall_seconds'),
                            ('peak_sampled_group_rss_bytes', 'group_rss_bytes'),
                            ('peak_sampled_combined_root_bytes', 'root_bytes')]:
        assert 0 <= sup[measured] < plan['caps'][limit]
    for path, want in plan['code_sha256'].items():
        b = subprocess.check_output(['git', 'show', RUNTIME+':'+path], cwd=ROOT)
        assert digest(b) == want, path
    seal = subprocess.check_output(['git', 'show', RUNTIME+':research/references/stmn2_targets_sealed.json'], cwd=ROOT)
    assert digest(seal) == plan['targets_sha256']
    assert json.loads(seal)['junctions'] == {'canonical': [79611214,79636801], 'cryptic': [79611214,79616821]}
    prior_raw = Path(prior_archive).read_bytes()
    assert digest(prior_raw) == PRIOR_SHA
    with zipfile.ZipFile(prior_archive) as z:
        source = z.read('plans/ela-gse252892-interrupt-execution-20261113.json')
        assert digest(source) == plan['source_record']['sha256']
        assert json.loads(source) == plan['source']
        for name, want in plan['source_record']['metadata_sha256'].items():
            assert digest(z.read('runs/06/'+name)) == want
        assert plan['inputs'] == plan['source_record']['inputs']
        for row in plan['inputs']:
            path = row['gsm']+'/'+Path(row['path']).name+'.verified.json'
            receipt = z.read('runs/06/'+path)
            assert digest(receipt) == row['receipt_sha256']
            receipt = json.loads(receipt)
            for k in ('bytes', 'md5', 'sha256'):
                assert receipt[k] == row[k]
        prior_result = json.loads(z.read('runs/06/result.json'))
        for lib, previous in zip(result['libraries'], prior_result['libraries']):
            gsm = lib['gsm']
            assert gsm == previous['gsm']
            assert lib['qc'] == previous['qc']
            assert lib == j(gsm+'/stmn2-counts.json')
            assert lib['positive_control_measured'] == (lib['counts']['canonical'] > 0)
            assert lib['support_at_least_20_groups']['cryptic'] == (lib['counts']['cryptic'] >= 20)
            fastp = j(gsm+'/fastp.json')
            assert fastp['summary']['fastp_version'] == '0.23.4'
            text = data[gsm+'/hisat2-summary.txt'].decode()
            assert data[gsm+'/hisat2.log'] == data[gsm+'/hisat2-summary.txt']
            pairs = int(re.search(r'^(\d+) reads;', text)[1])
            unique = int(re.search(r'^\s*(\d+) .*aligned concordantly exactly 1 time', text, re.M)[1])
            multi = int(re.search(r'^\s*(\d+) .*aligned concordantly >1 times', text, re.M)[1])
            zero = int(re.search(r'^\s*(\d+) .*aligned concordantly 0 times', text, re.M)[1])
            assert zero+unique+multi == pairs
            assert fastp['summary']['after_filtering']['total_reads'] == 2*pairs
            assert unique == lib['qc']['eligible_groups']
            assert multi == lib['qc']['rejected_groups']
            assert unique+multi == lib['qc']['alignment_groups']
            assert 2*unique+4*multi == lib['qc']['sam_records']
            expected_command = plan['commands'][gsm]['fastp']
            assert fastp['command'].split() == expected_command
            assert ' '.join(expected_command) in data[gsm+'/fastp.log'].decode()
            # Compare deterministic QC across runs, excluding path-specific command.
            old_fastp = json.loads(z.read('runs/06/'+gsm+'/fastp.json'))
            assert {k:v for k,v in fastp.items() if k!='command'} == {k:v for k,v in old_fastp.items() if k!='command'}
    import sys
    sys.path.insert(0, str(ROOT/'scripts'))
    import run_gse252892_stmn2_control as runner
    assert plan['caps'] == runner.CAPS
    assert plan['commands'] == {g:runner.commands(plan,g) for g in GSMS}
    assert len(set(plan['source_record']['prior_roots']+[plan['run_root']])) == 7
    return {'status':'passed', 'archive_sha256':digest(raw), 'archive_bytes':len(raw),
            'metadata_members':len(data), 'metadata_bytes':sum(map(len,data.values())),
            'plan_sha256':PLAN_SHA, 'runtime_commit':RUNTIME,
            'runtime_file_hashes_checked':len(plan['code_sha256']),
            'prior_archive_sha256':PRIOR_SHA, 'source_input_receipts_checked':len(plan['inputs']),
            'checks':['exact original aggregate result/supervision match terminal transcriptions',
                      'proposal/claim/acceptance/supervision identity',
                      'runtime hashes, sealed targets, commands and fixed envelope',
                      'embedded source proposal and original run06 metadata/input receipts',
                      'per-library results, support flags, fastp QC/command and HISAT2 group totals',
                      'fastp non-command fields and count QC equal original prior run06',
                      'completed worker, reported zero network and sampled resources below caps'],
            'limitations':['No raw FASTQ, binary or index replay/rehash by this verifier.',
                           'Network and resource evidence is recorded metadata, not independent system telemetry.',
                           'No independent biological replication or protein efficacy inference.'],
            'members':{n:{'bytes':len(b),'sha256':digest(b)} for n,b in sorted(data.items())}}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive',required=True,type=Path)
    p.add_argument('--prior-archive',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    report=verify(a.archive,a.prior_archive)
    a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='members'},indent=2))
