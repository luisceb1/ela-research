import hashlib
from pathlib import Path
import tempfile
import unittest
from scripts.resume_gse122069_ranges import validate_saved


class RangeResumeTests(unittest.TestCase):
    def test_verifies_reused_bytes_and_returns_only_missing_ranges(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'partial';p.write_bytes(b'abcdefgh')
            e={'start':0,'end':3,'sha256':hashlib.sha256(b'abcd').hexdigest()}
            self.assertEqual(validate_saved(p,[e],10,4),[(4,7),(8,9)])
            p.write_bytes(b'Xbcdefgh')
            with self.assertRaises(ValueError):validate_saved(p,[e],10,4)
    def test_duplicate_or_nonpartition_range_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'partial';p.write_bytes(b'abcdefgh')
            e={'start':0,'end':3,'sha256':hashlib.sha256(b'abcd').hexdigest()}
            with self.assertRaises(ValueError):validate_saved(p,[e,e],8,4)
            with self.assertRaises(ValueError):validate_saved(p,[dict(e,start=1)],8,4)

if __name__=='__main__':unittest.main()
