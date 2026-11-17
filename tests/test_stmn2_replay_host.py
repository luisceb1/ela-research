"""Mocked WSL admission controls; no real Windows host validation implied."""
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import stmn2_replay_host as host


class HostTests(unittest.TestCase):
    def setUp(self):
        self.row = dict(distribution='Ubuntu-24.04', version=2,
                        registry_key='{12345678-1234-1234-1234-123456789abc}',
                        base_path='C:\\WSL\\Ubuntu', vhd_name='ext4.vhdx')
        self.mount = dict(target='/', fstype='ext4', source='/dev/sde')
        self.patches = [patch.object(host, 'is_wsl', return_value=True),
                        patch.dict(host.os.environ, WSL_DISTRO_NAME='Ubuntu-24.04'),
                        patch.object(host.subprocess, 'check_output', side_effect=self.mount_json),
                        patch.object(host.subprocess, 'run', side_effect=self.registry),
                        patch.object(host.drvfs, 'free_bytes', return_value=200*1024**3)]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def mount_json(self, *args, **kwargs):
        return json.dumps({'filesystems': [self.mount]})

    def registry(self, *args, **kwargs):
        return subprocess.CompletedProcess([], 0, '\ufeff'+json.dumps(self.row)+'\n', '')

    def test_verified_identity_and_native_unchanged(self):
        self.assertEqual(host.placement('/home')['kind'], 'wsl2-c-vhd')
        with patch.object(host, 'is_wsl', return_value=False), \
                patch.object(host.subprocess, 'run', side_effect=AssertionError('no interop')):
            self.assertEqual(host.placement('/home'), {'kind': 'native-linux'})
            self.assertIsNone(host.check('/home', 1))

    def test_wrong_mount_refused(self):
        for field, value in [('target', '/mnt/c'), ('fstype', '9p'), ('source', '/dev/loop0')]:
            with self.subTest(field=field), patch.dict(self.mount, {field: value}), self.assertRaises(ValueError):
                host.placement('/home')

    def test_wrong_registration_refused(self):
        for field, value in [('distribution', 'Ubuntu'), ('version', 1), ('version', True),
                             ('base_path', 'D:\\WSL'), ('registry_key', 'other'),
                             ('vhd_name', '../ext4.vhdx')]:
            with self.subTest(field=field), patch.dict(self.row, {field: value}), self.assertRaises(ValueError):
                host.placement('/home')

    def test_interop_failures_and_malformed_json_fail_closed(self):
        for exc in (subprocess.TimeoutExpired('powershell', 15),
                    subprocess.CalledProcessError(1, 'powershell'), FileNotFoundError('powershell')):
            with self.subTest(exc=exc), patch.object(host.subprocess, 'run', side_effect=exc), self.assertRaises(type(exc)):
                host.placement('/home')
        with patch.object(host.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'bad', '')), self.assertRaises(ValueError):
            host.placement('/home')

    def test_missing_or_unsafe_distribution_refused(self):
        for name in ('', "Ubuntu';exit", 'x'*101):
            with patch.dict(host.os.environ, WSL_DISTRO_NAME=name), self.assertRaises(ValueError):
                host.placement('/home')

    def test_telemetry_absence_and_invalid_values_fail_closed(self):
        for value in (None, True, -1):
            with patch.object(host.drvfs, 'free_bytes', return_value=value), self.assertRaises(ValueError):
                host.physical_free()

    def test_low_host_space_refused_at_admission_and_runtime(self):
        for admission in (False, True):
            with patch.object(host.drvfs, 'free_bytes', return_value=49*1024**3), self.assertRaisesRegex(ValueError, 'physical C:'):
                host.check('/home', 50*1024**3, admission)

    def test_guest_ram_admission(self):
        for gib, passes in ((6, False), (7, True)):
            with patch.object(Path, 'read_text', return_value=f'MemAvailable: {gib*1024**2} kB\n'):
                if passes:
                    self.assertEqual(host.check('/home', 150*1024**3, True), 200*1024**3)
                else:
                    with self.assertRaisesRegex(ValueError, 'RAM'):
                        host.check('/home', 150*1024**3, True)

if __name__ == '__main__':
    unittest.main()
