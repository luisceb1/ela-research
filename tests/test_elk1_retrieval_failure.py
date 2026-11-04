"""Offline failure controls for the bounded archive acquisition receipts."""
import json
import os
from pathlib import Path
import runpy
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from urllib.error import URLError

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'reports/elk1-fish-replay-20261104/final-article/retrieval'


class RetrievalFailureTests(unittest.TestCase):
    def setUp(self):
        self.old=os.getcwd()
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(os.chdir,self.old)
        os.chdir(self.tmp.name)
        self.cache=Path('elk1-final-cache');self.cache.mkdir()

    def test_index_network_failure_propagates_and_preserves_receipt(self):
        with patch('urllib.request.urlopen',side_effect=URLError('offline control')):
            with self.assertRaises(URLError):
                runpy.run_path(str(SCRIPTS/'inspect_remote_zip.py'),run_name='__main__')
        self.assertEqual(json.loads((self.cache/'range-receipt.json').read_text())['bytes_read'],0)

    def test_partial_extraction_failure_propagates_and_preserves_receipt(self):
        (self.cache/'range-receipt.json').write_text(json.dumps({'bytes_read':10,'requests':[]}))
        (self.cache/'selected-members.json').write_text(json.dumps([
            {'name':'tdp43-apa/wet/data/fish_counts_cleaned.tsv','offset':0}]))
        def fail(*args): raise ValueError('range refused')
        remote=SimpleNamespace(get_range=fail,CAP=5242880)
        with patch.dict(sys.modules,{'inspect_remote_zip':remote}):
            with self.assertRaisesRegex(ValueError,'range refused'):
                runpy.run_path(str(SCRIPTS/'extract_selected.py'),run_name='__main__')
        self.assertEqual(json.loads((self.cache/'extracted-members.json').read_text()),[])
        self.assertEqual(json.loads((self.cache/'range-receipt.json').read_text())['bytes_read'],10)
