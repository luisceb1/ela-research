import unittest
from scripts.audit_gse121569_design import parse_soft, link_columns, audit, apply_published_batches


def sample(gsm='GSM1', alias='siScr_1', condition='scramble', date='2013-01-10'):
    return f'''^SAMPLE = {gsm}
!Sample_description = {alias}
!Sample_characteristics_ch1 = sirna type: {condition}
!Sample_characteristics_ch1 = cell type: differentiated HUES3 into hMNs
!Sample_characteristics_ch1 = date: {date}
!Sample_contact_name = excluded
'''


class DesignTests(unittest.TestCase):
    def test_exact_alias_not_order(self):
        rows = parse_soft(sample()+sample('GSM2','siTDP43_2','TDP43'))
        linked = link_columns(rows,['countData.siTDP43_2','countData.siScr_1'])
        self.assertEqual([r['gsm'] for r in linked], ['GSM2','GSM1'])
        self.assertNotIn('contact', str(linked))

    def test_duplicate_alias_rejected(self):
        with self.assertRaises(ValueError): parse_soft(sample()+sample('GSM2'))

    def test_condition_mismatch_rejected(self):
        with self.assertRaises(ValueError): parse_soft(sample(condition='TDP43'))

    def test_missing_date_rejected(self):
        with self.assertRaises(ValueError): parse_soft(sample(date=''))

    def test_unmatched_column_rejected(self):
        with self.assertRaises(ValueError): link_columns(parse_soft(sample()), ['countData.siScr_9'])

    def test_duplicate_column_rejected(self):
        with self.assertRaises(ValueError): link_columns(parse_soft(sample()), ['countData.siScr_1']*2)

    def test_crossed_date_does_not_authorize_refit(self):
        rows = parse_soft(sample()+sample('GSM2','siTDP43_1','TDP43'))
        result = audit(rows,link_columns(rows,['countData.siScr_1','countData.siTDP43_1']))
        self.assertTrue(result['condition_crossed_with_deposited_date'])
        self.assertFalse(result['inferential_refit_allowed'])
        self.assertEqual(result['published_batch_links'],0)

    def test_rep_number_does_not_assign_batch(self):
        rows = parse_soft(sample()+sample('GSM2','NoTx_1','none','2013-06-10'))
        self.assertTrue(all(r['experiment_id']=='unknown' for r in rows))

    def test_confounded_date_detected(self):
        rows = parse_soft(sample()+sample('GSM2','siTDP43_1','TDP43','2013-06-10'))
        self.assertFalse(audit(rows,link_columns(rows,['countData.siScr_1','countData.siTDP43_1']))['condition_crossed_with_deposited_date'])

    def test_incomplete_published_map_rejected(self):
        with self.assertRaises(ValueError):
            apply_published_batches(parse_soft(sample()), {'alias_to_published_batch':{}})

    def test_published_map_not_date_assignment(self):
        rows = parse_soft(sample()+sample('GSM2','siTDP43_1','TDP43'))
        mapped = apply_published_batches(rows, {'alias_to_published_batch':{'siScr_1':'Batch 2','siTDP43_1':'Batch 1'}})
        self.assertEqual([r['published_batch'] for r in mapped],['Batch 2','Batch 1'])
        self.assertEqual(mapped[0]['well_id'],'unknown')
