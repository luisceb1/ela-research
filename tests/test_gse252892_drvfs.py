"""Only an exact physical C: drvfs mapping may replace the interop query."""
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock,patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import gse252892_drvfs as m
import run_gse252892_local as r

MOUNT=r'130 80 0:68 / /mnt/c rw,noatime - 9p C:\134 rw,aname=drvfs;path=C:\;uid=1000;gid=1000;cache=5,trans=fd'
class DriveTests(unittest.TestCase):
    def test_exact_user_mount_queries_only_c(self):
        stat=Mock(return_value=SimpleNamespace(f_bavail=10,f_blocks=20,f_frsize=4096))
        self.assertEqual(m.free_bytes(MOUNT,stat),40960);stat.assert_called_once_with('/mnt/c')
    def test_other_drive_source_or_options_refused(self):
        for line in [MOUNT.replace('C:\\134','D:\\134'),MOUNT.replace('path=C:', 'path=D:'),MOUNT.replace('aname=drvfs','aname=other')]:
            with self.assertRaises(ValueError):m.free_bytes(line,Mock())
    def test_linux_virtual_filesystem_refused(self):
        with self.assertRaises(ValueError):m.free_bytes(MOUNT.replace('9p C:\\134','ext4 /dev/sde'),Mock())
    def test_ambiguous_mount_refused(self):
        with self.assertRaisesRegex(ValueError,'Ambiguous'):m.free_bytes(MOUNT+'\n'+MOUNT,Mock())
    def test_no_c_mount_requests_original_method(self):self.assertIsNone(m.free_bytes(''))
    def test_invalid_availability_refused(self):
        for info in [SimpleNamespace(f_bavail=-1,f_blocks=20,f_frsize=4096),SimpleNamespace(f_bavail=21,f_blocks=20,f_frsize=4096),SimpleNamespace(f_bavail=10,f_blocks=20,f_frsize=0)]:
            with self.assertRaises(ValueError):m.free_bytes(MOUNT,lambda p:info)
    def test_valid_drvfs_does_not_spawn_windows_process(self):
        with patch.object(r.drvfs,'free_bytes',return_value=100),patch.object(r,'windows_free',side_effect=AssertionError('interop must not run')):
            self.assertEqual(r.physical_free(),100)
    def test_no_mount_preserves_original_windows_method(self):
        with patch.object(r.drvfs,'free_bytes',return_value=None),patch.object(r,'windows_free',return_value=100) as call:
            self.assertEqual(r.physical_free(),100);call.assert_called_once()
    def test_bad_mapping_does_not_bypass_guard(self):
        with patch.object(r.drvfs,'free_bytes',side_effect=ValueError('wrong drive')),patch.object(r,'windows_free') as call:
            with self.assertRaises(ValueError):r.physical_free()
            call.assert_not_called()
    def test_original_50gib_reserve_retained(self):
        with self.assertRaisesRegex(ValueError,'50 GiB'):r.check_free(50*1024**3-1)
        r.check_free(50*1024**3)
