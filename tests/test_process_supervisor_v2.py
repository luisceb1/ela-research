import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

s=importlib.util.spec_from_file_location('supervisor',Path(__file__).resolve().parents[1]/'scripts/process_supervisor_v2.py')
sup=importlib.util.module_from_spec(s);s.loader.exec_module(sup)

class SupervisorTests(unittest.TestCase):
    def run_child(self,code,**kwargs):
        with tempfile.TemporaryDirectory() as d:
            record=sup.supervise('test',[sys.executable,'-c',code],d,**kwargs)
            self.assertEqual(json.loads((Path(d)/'test.json').read_text()),record)
            return record
    def test_known_allocation_and_namespace_mapping(self):
        r=self.run_child('import time;x=bytearray(32*1024**2);time.sleep(.2)')
        self.assertGreaterEqual(r['peak_group_rss_bytes_sampled'],32*1024**2)
        self.assertEqual(r['exit_code'],0);self.assertIsNone(r['violation'])
    def test_descendant_allocation_included(self):
        code='import subprocess,sys,time;x=bytearray(24*1024**2);p=subprocess.Popen([sys.executable,"-c","import time;x=bytearray(24*1024**2);time.sleep(.3)"]);p.wait()'
        r=self.run_child(code)
        self.assertGreaterEqual(r['max_group_members'],2);self.assertGreaterEqual(r['peak_group_rss_bytes_sampled'],48*1024**2)
    def test_memory_kill_and_cleanup(self):
        r=self.run_child('import time;x=bytearray(32*1024**2);time.sleep(2)',rss_limit=20*1024**2)
        self.assertEqual(r['violation'],'memory');self.assertFalse(r['live_group_members_after_cleanup'])
    def test_timeout_kills_descendant(self):
        r=self.run_child('import subprocess,sys,time;p=subprocess.Popen([sys.executable,"-c","import time;time.sleep(3)"]);time.sleep(3)',timeout=.3)
        self.assertEqual(r['violation'],'timeout');self.assertFalse(r['live_group_members_after_cleanup'])
    def test_fast_failure_recorded(self):
        r=self.run_child('raise SystemExit(7)');self.assertEqual(r['exit_code'],7);self.assertEqual(r['status'],'finished')
    def test_distinct_receipts_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            for i in range(4):sup.supervise('r'+str(i),[sys.executable,'-c','pass'],d)
            self.assertEqual(len(list(Path(d).glob('r*.json'))),4)
            with self.assertRaises((FileExistsError,ValueError)):sup.supervise('r0',[sys.executable,'-c','pass'],d)
    def test_started_receipt_publishes_procfs_group_to_child(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'identity.json'
            code="import json,time,os;from pathlib import Path;p=Path("+repr(str(path))+");until=time.monotonic()+2\nwhile time.monotonic()<until:\n r=json.loads(p.read_text())\n if 'procfs_group' in r:break\n time.sleep(.01)\nassert r['status']=='started'\nassert r['procfs_group']==int(Path('/proc/self/stat').read_text().rsplit(')',1)[1].split()[2])"
            rec=sup.supervise('identity',[sys.executable,'-c',code],d)
            self.assertEqual(rec['exit_code'],0)
    def test_spawn_failure_has_terminal_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):sup.supervise('missing',['/definitely/not/a/program'],d)
            r=json.loads((Path(d)/'missing.json').read_text())
            self.assertEqual(r['status'],'finished');self.assertIn('supervisor_error',r)

if __name__=='__main__':unittest.main()
