import importlib.util
from pathlib import Path
import tempfile
import unittest
import shutil

def load(name):
    s=importlib.util.spec_from_file_location(name,Path(__file__).resolve().parents[1]/'scripts'/f'{name}.py')
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

sorter=load('collate_pe_sam');pe=load('pe_fragment_contract')

@unittest.skipUnless(shutil.which('sort'),'GNU sort required')
class CollationTests(unittest.TestCase):
    def test_lexicographic_rg_qname_and_support_preserved(self):
        from test_pe_fragment_contract import pair
        lines=pair('q2',rg='B')+pair('q2',rg='A')+pair('q10',rg='A')
        # Interleave the mates to ensure adjacency is not assumed.
        shuffled=lines[::2]+lines[1::2]
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);source=root/'in.sam';out=root/'out.sam'
            source.write_text('@SQ\tSN:chr19\tLN:100000\n'+'\n'.join(shuffled)+'\n')
            sorter.collate(source,out,root/'sort')
            records=list(pe.text_records(out,15))
            self.assertEqual([(r['rg'],r['qname']) for r in records],[('A','q10')]*2+[('A','q2')]*2+[('B','q2')]*2)
            c,q=pe.count_fragments(iter(records),'synthetic');self.assertEqual(sum(c.values()),3)
            self.assertFalse((root/'sort/keyed.tsv').exists())
    def test_duplicate_rg_fails_closed(self):
        from test_pe_fragment_contract import pair
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);source=root/'in.sam';source.write_text(pair()[0]+'\tRG:Z:B\n')
            with self.assertRaises(ValueError):sorter.collate(source,root/'out.sam',root/'sort')

if __name__=='__main__':unittest.main()
