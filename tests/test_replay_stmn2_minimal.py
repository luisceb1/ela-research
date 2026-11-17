"""Technical replay controls; fixture orchestration is not biological evidence."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import replay_stmn2_minimal as replay
import run_gse252892_local as historical

FIRST = replay.ROOT/'reports/gse252892-stmn2-result-20261115/original/result.json'
REST = replay.ROOT/'reports/stmn2-remaining-result-20261116/original/result.json'


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.rows = json.loads(FIRST.read_text())['libraries']+json.loads(REST.read_text())['libraries']

    def fixture(self, rows=None):
        path = self.root/'results.json'
        path.write_text(json.dumps(dict(status='completed', gene='STMN2',
                                        project='SRP482832', libraries=self.rows if rows is None else rows)))
        return path

    def test_exact_original_records_and_low_controls(self):
        report = replay.compare([FIRST, REST])
        self.assertEqual(report['status'], 'records_match')
        self.assertFalse(report['raw_replay_verified'])
        self.assertEqual([r['counts']['cryptic'] for r in report['libraries']], [3, 5, 0, 727, 551, 556])

    def test_missing_is_not_success(self):
        report = replay.compare([FIRST])
        self.assertEqual(report['status'], 'records_differ')
        self.assertEqual(len(report['missing_libraries']), 4)

    def test_count_change_preserved(self):
        self.rows[0]['counts']['cryptic'] = 4
        report = replay.compare([self.fixture()])
        self.assertEqual(report['differences'], [dict(gsm='GSM8009878', field='counts.cryptic', expected=3, observed=4)])

    def test_changed_qc_cannot_pass_with_matching_counts(self):
        self.rows[0]['qc']['sam_records'] += 2
        self.assertEqual(replay.compare([self.fixture()])['status'], 'records_differ')

    def test_duplicate_and_extra_refused(self):
        for rows in (self.rows+[self.rows[0]], [dict(self.rows[0], gsm='other')]):
            with self.assertRaises(ValueError):
                replay.compare([self.fixture(rows)])

    def test_invalid_identity_completion_units_and_flags_refused(self):
        for field, value in [('complete', False), ('project', 'TARGET_ALS'), ('gene', 'UNC13A'),
                             ('unit', 'reads'), ('positive_control_measured', 1),
                             ('support_at_least_20_groups', {'cryptic': 0})]:
            rows = copy.deepcopy(self.rows)
            rows[0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                replay.compare([self.fixture(rows)])

    def test_invalid_numbers_and_inconsistent_qc_refused(self):
        for field, key, value in [('counts', 'canonical', True), ('counts', 'cryptic', -1),
                                  ('counts', 'cryptic', 1.0), ('qc', 'eligible_groups', 1)]:
            rows = copy.deepcopy(self.rows)
            rows[0][field][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                replay.compare([self.fixture(rows)])

    def test_duplicate_json_keys_refused(self):
        path = self.root/'duplicate.json'
        path.write_text('{"x":1,"x":2}')
        with self.assertRaises(ValueError):
            replay.read(path)

    def test_cli_difference_is_nonzero_and_output_not_overwritten(self):
        output = self.root/'comparison.json'
        cmd = [sys.executable, str(Path(replay.__file__)), 'compare', '--results', str(FIRST), '--output', str(output)]
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)
        previous = output.read_bytes()
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 2)
        self.assertEqual(output.read_bytes(), previous)


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.ref = copy.deepcopy(replay.reference())
        self.inputs = {}
        for i, row in enumerate(self.ref['inputs']):
            p = self.root/row['filename']
            p.write_bytes(('software fixture '+str(i)).encode())
            row.update(replay.digest(p))
            self.inputs[row['filename']] = str(p)
        self.index = self.root/'index'
        self.index.mkdir()
        for row in self.ref['index_files']:
            p = self.index/row['name']
            p.write_bytes(b'index software fixture')
            row.update(bytes=p.stat().st_size, sha256=replay.sha(p))
        self.tools = {}
        for key, ver in [('fastp', 'fastp 0.23.4'), ('aligner', 'hisat2-align-s version 2.2.3')]:
            p = self.root/key
            p.write_text('#!/bin/sh\nprintf "%s\\n" "'+ver+'"\n')
            p.chmod(0o755)
            self.tools[key] = str(p)
        self.output = self.root/'run'
        self.patches = [patch.object(replay, 'reference', return_value=self.ref),
                        patch.object(replay, 'git', side_effect=lambda *a: '' if a[0] == 'status' else 'test-commit')]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def inspect(self, full=True):
        return replay.inspect(self.inputs, self.index, self.tools, self.output, full)

    def test_portable_plan_without_historical_roots(self):
        plan = self.inspect()
        self.assertEqual(len(plan['commands']), 6)
        self.assertEqual(len(plan['inputs']), 12)
        replay.validate(plan)
        self.assertFalse(self.output.exists())

    def test_missing_and_duplicate_source_refused(self):
        old = self.inputs.pop(next(iter(self.inputs)))
        with self.assertRaises(ValueError):
            self.inspect()
        self.inputs = {r['filename']: old for r in self.ref['inputs']}
        with self.assertRaises(ValueError):
            self.inspect()

    def test_same_size_corruption_and_index_corruption_refused(self):
        p = Path(next(iter(self.inputs.values())))
        original = p.read_bytes()
        p.write_bytes(b'x'*len(original))
        with self.assertRaisesRegex(ValueError, 'FASTQ digest'):
            self.inspect()
        p.write_bytes(original)
        p = self.index/self.ref['index_files'][0]['name']
        p.write_bytes(b'x'*p.stat().st_size)
        with self.assertRaisesRegex(ValueError, 'Index shard'):
            self.inspect()

    def test_altered_plan_commands_caps_and_inputs_refused(self):
        plan = self.inspect()
        for field in ('commands', 'caps', 'inputs'):
            changed = copy.deepcopy(plan)
            if field == 'commands':
                changed[field]['GSM8009878']['align'].append('--local')
            elif field == 'caps':
                changed[field]['cpus'] = 3
            else:
                changed[field][0]['sha256'] = 'wrong'
            with self.subTest(field=field), self.assertRaises(ValueError):
                replay.validate(changed)

    def test_exact_historical_command_options_all_six(self):
        plan = self.inspect()
        for lib in self.ref['libraries']:
            gsm = lib['gsm']
            cmd = plan['commands'][gsm]
            old = historical.commands(dict(run_root=plan['run_root'], fastp=dict(path=self.tools['fastp']),
                base=dict(index_directory=str(self.index), tools=dict(aligner=dict(path=self.tools['aligner'])))), 'GSM8009878')
            for key in ('fastp', 'align', 'plain_files'):
                expected = [s.replace('GSM8009878', gsm) for s in old[key]]
                if key == 'fastp':
                    raw = [r['path'] for r in plan['inputs'] if r['gsm'] == gsm]
                    for flag, path in zip(('-i', '-I'), raw):
                        expected[expected.index(flag)+1] = path
                self.assertEqual(cmd[key], expected)

    def test_prepare_has_no_alignment_and_is_single_use(self):
        mapping, out = self.root/'paths.json', self.root/'plan.json'
        mapping.write_text(json.dumps(self.inputs))
        with patch.object(replay, 'free_check'), patch.object(replay, 'measure', side_effect=AssertionError('no alignment')):
            report = replay.prepare(mapping, self.index, self.tools['fastp'], self.tools['aligner'], self.output, out)
            self.assertEqual(report['status'], 'prepared_not_executed')
            with self.assertRaises(ValueError):
                replay.prepare(mapping, self.index, self.tools['fastp'], self.tools['aligner'], self.output, out)
        self.assertFalse(self.output.exists())

    def test_wrong_version_and_wsl_refused(self):
        Path(self.tools['fastp']).write_text('#!/bin/sh\necho fastp 0.23.40\n')
        with self.assertRaises(ValueError):
            self.inspect()
        with patch.object(Path, 'read_text', return_value='6.6.87-microsoft-standard-WSL2'), self.assertRaises(ValueError):
            replay.native_linux()

    def test_worker_processes_all_six_despite_zero_canonical(self):
        plan = self.inspect()
        self.output.mkdir()
        plan_path = self.root/'plan.json'
        replay.write_new(plan_path, plan)
        replay.write_new(self.output/'accepted.json', dict(supervisor_pid=123, plan_sha256=replay.sha(plan_path)))
        observed = []
        def measure(p, gsm):
            observed.append(gsm)
            return dict(gsm=gsm, counts=dict(canonical=0, cryptic=0))
        with patch.object(replay, 'validate'), patch.object(replay, 'measure', side_effect=measure), \
                patch.object(replay.os, 'getpgrp', return_value=456), patch.object(replay.os, 'getpid', return_value=456), \
                patch.object(replay.os, 'getppid', return_value=123):
            replay.worker(plan_path)
        self.assertEqual(observed, [r['gsm'] for r in self.ref['libraries']])
        self.assertEqual(len(replay.read(self.output/'result.json')['libraries']), 6)

    def test_failed_worker_retains_failure_and_stops(self):
        plan = self.inspect()
        self.output.mkdir()
        path = self.root/'plan.json'
        replay.write_new(path, plan)
        replay.write_new(self.output/'accepted.json', dict(supervisor_pid=123, plan_sha256=replay.sha(path)))
        with patch.object(replay, 'validate'), patch.object(replay, 'measure', side_effect=ValueError('fixture failure')), \
                patch.object(replay.os, 'getpgrp', return_value=456), patch.object(replay.os, 'getpid', return_value=456), \
                patch.object(replay.os, 'getppid', return_value=123), self.assertRaises(ValueError):
            replay.worker(path)
        self.assertEqual(replay.read(self.output/'worker-failure.json')['status'], 'failed_partial')
        self.assertFalse((self.output/'result.json').exists())

    def test_exact_sha_and_consumed_plan_refusals(self):
        path = self.root/'plan.json'
        replay.write_new(path, self.inspect())
        with self.assertRaises(ValueError):
            replay.execute(path, 'incorrect')
        replay.write_new(str(path)+'.claimed.json', {})
        with patch.object(replay, 'free_check'), self.assertRaises(FileExistsError):
            replay.execute(path, replay.sha(path))
        self.assertFalse(self.output.exists())

    def test_real_subprocess_stream_through_original_counter(self):
        # Tiny synthetic SAM tests software plumbing, never biological support.
        fastp = Path(self.tools['fastp'])
        fastp.write_text('#!'+sys.executable+'\nimport sys\nfrom pathlib import Path\n'
                         'for flag in ("-o", "-O"):\n'
                         '    Path(sys.argv[sys.argv.index(flag)+1]).write_text("fixture")\n')
        sam = ('@HD\tVN:1.6\tSO:unsorted\n@SQ\tSN:chr8\tLN:145138636\n'
               'fixture\t99\tchr8\t79611195\t60\t20M5607N20M\t=\t79616900\t0\t'
               + 'A'*40+'\t'+'I'*40+'\tNH:i:1\tXS:A:+\n'
               'fixture\t147\tchr8\t79616900\t60\t40M\t=\t79611195\t0\t'
               + 'T'*40+'\t'+'I'*40+'\tNH:i:1\tXS:A:+\n')
        aligner = Path(self.tools['aligner'])
        aligner.write_text('#!'+sys.executable+'\nimport sys\nsys.stdout.write('+repr(sam)+')\n')
        self.output.mkdir()
        plan = dict(run_root=str(self.output), inputs=[dict(gsm=r['gsm'], path=self.inputs[r['filename']])
                    for r in self.ref['inputs']], index_dir=str(self.index),
                    tools={k: dict(path=v) for k, v in self.tools.items()})
        plan['commands'] = {'GSM8009878': replay.commands(plan, 'GSM8009878')}
        result = replay.measure(plan, 'GSM8009878')
        self.assertEqual(result['counts'], dict(canonical=0, cryptic=1))
        self.assertEqual(result['qc']['eligible_groups'], 1)
        self.assertFalse(result['positive_control_measured'])
        self.assertFalse((self.output/'GSM8009878/trimmed_1.fq').exists())
        self.assertEqual(replay.read(self.output/'GSM8009878/stmn2-counts.json'), result)

    def test_supervisor_cap_failure_preserves_metadata(self):
        path = self.root/'plan.json'
        replay.write_new(path, self.inspect())
        fake = unittest.mock.Mock(pid=99999999, returncode=None)
        fake.poll.return_value = None
        with patch.object(replay, 'validate'), patch.object(replay, 'free_check'), \
                patch.object(replay.subprocess, 'Popen', return_value=fake), \
                patch.object(replay, 'group_rss', return_value=replay.CAPS['group_rss_bytes']+1), \
                patch.object(replay, 'stop_group') as stop, self.assertRaisesRegex(ValueError, 'resource cap'):
            replay.execute(path, replay.sha(path))
        stop.assert_called_once_with(fake)
        record = replay.read(self.output/'supervision.json')
        self.assertEqual(record['status'], 'failed')
        self.assertFalse(record['raw_execution_reported'])
        self.assertTrue(Path(str(path)+'.claimed.json').exists())


if __name__ == '__main__':
    unittest.main()
