"""Disk sampling tolerates atomic promotions while retaining fail-closed checks."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import run_gse252892_local as m

class DiskSamplingTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.root=Path(tmp.name)
    def test_atomic_promotion_after_metadata_read_needs_no_second_stat(self):
        old=self.root/'receipt.json.tmp';old.write_bytes(b'fixture')
        target=self.root/'receipt.json';real=Path.lstat
        def promote(p):
            info=real(p)
            if p==old:os.replace(old,target)
            return info
        with patch.object(Path,'lstat',promote):self.assertEqual(m.root_bytes(self.root),7)
        self.assertEqual(target.read_bytes(),b'fixture');self.assertFalse(old.exists())
    def test_name_disappeared_after_walk_is_tolerated(self):
        p=self.root/'receipt.json.tmp';p.write_bytes(b'fixture');real=Path.lstat
        def vanished(path):
            if path==p:p.unlink()
            return real(path)
        with patch.object(Path,'lstat',vanished):self.assertEqual(m.root_bytes(self.root),0)
    def test_permission_failure_is_not_swallowed(self):
        p=self.root/'blocked';p.write_bytes(b'x');real=Path.lstat
        def denied(path):
            if path==p:raise PermissionError('fixture permission failure')
            return real(path)
        with patch.object(Path,'lstat',denied):
            with self.assertRaises(PermissionError):m.root_bytes(self.root)
    def test_missing_root_fails_instead_of_returning_zero(self):
        with self.assertRaises(FileNotFoundError):m.root_bytes(self.root/'missing')
    def test_root_symlink_refused(self):
        link=self.root/'link';link.symlink_to(self.root,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'Symlink'):m.root_bytes(link)
    def test_walk_errors_are_not_silently_ignored(self):
        def walker(root,followlinks,onerror):
            onerror(PermissionError('fixture denied subtree'));return iter([])
        with patch.object(m.os,'walk',walker):
            with self.assertRaises(PermissionError):m.root_bytes(self.root)
