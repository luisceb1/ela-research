import gzip
from pathlib import Path
import tempfile
import unittest

from scripts.audit_shared_junctions import junction_index
from scripts.reconcile_shared_junctions import blocks, expressed_keys
from research.prototypes import junction_streaming_legacy as legacy


def exon(tx, start, end):
    return f'chr1\tsynthetic\texon\t{start}\t{end}\t.\t+\t.\tgene_id "ENSG1"; transcript_id "{tx}";\n'


class SharedJunctionReconciliationTests(unittest.TestCase):
    def test_interleaving_loses_legacy_structure_not_grouped_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'fixture.gtf.gz'
            with gzip.open(path,'wt') as f:
                f.write(exon('BambuTx1',1,10)+exon('BambuTx2',2,10)+exon('BambuTx1',21,30)+exon('BambuTx2',21,35))
            rows={'BambuTx1':('ENSG1',(1,)), 'BambuTx2':('ENSG1',(1,))}
            old,_=legacy.parse_bambu(path,rows);new,_=junction_index(path,rows)
            self.assertTrue(all(not v[1] for v in old.values()))
            self.assertEqual(set(new),{('ENSG1','chr1',11,20,'+')})
            self.assertEqual(set(new[('ENSG1','chr1',11,20,'+')]),set(rows))
            self.assertEqual(blocks(path,rows),{'BambuTx1':2,'BambuTx2':2})

    def test_grouped_parser_invariant_to_exon_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths=[Path(tmp)/f'order{i}.gtf.gz' for i in range(2)]
            lines=[exon('BambuTx1',1,10),exon('BambuTx1',21,30),exon('BambuTx2',2,10),exon('BambuTx2',21,35)]
            for p,order in zip(paths,[lines,[lines[i] for i in (0,2,1,3)]]):
                with gzip.open(p,'wt') as f:f.writelines(order)
            rows={'BambuTx1':('ENSG1',(1,)), 'BambuTx2':('ENSG1',(1,))}
            self.assertEqual(junction_index(paths[0],rows),junction_index(paths[1],rows))

    def test_zero_support_is_separate_from_catalog_membership(self):
        key=('ENSG1','chr1',11,20,'+')
        novel={key:['BambuTx1','BambuTx2']}
        self.assertEqual(expressed_keys(novel,{'BambuTx1':('ENSG1',(0,)),'BambuTx2':('ENSG1',(0,))}),set())
        self.assertEqual(expressed_keys(novel,{'BambuTx1':('ENSG1',(0,)),'BambuTx2':('ENSG1',(2,))}),{key})

    def test_internal_reference_also_requires_grouping(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'reference.gtf.gz'
            with gzip.open(path,'wt') as f:
                f.write(exon('ENST1',1,10)+exon('ENST2',2,10)+exon('ENST1',21,30)+exon('ENST2',21,35))
            _,reference=junction_index(path,{})
            old=legacy.internal_ref(path,{'ENSG1':{('chr1',11,20,'+')}})
            self.assertEqual(old,set())
            self.assertIn(('ENSG1','chr1',11,20,'+'),reference)
