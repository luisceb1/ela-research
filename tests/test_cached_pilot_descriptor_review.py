"""Synthetic metadata only. Paths below are never followed; not a real WSL plan."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
scripts=Path(__file__).resolve().parents[1]/'scripts';sys.path.insert(0,str(scripts))
try:import audit_cached_pilot_descriptor as audit
finally:sys.path.pop(0)


def fixture(profile):
    p=profile['proposal'];aligner={'fixture_only':True};b={'schema':'sealed-extracted-index-v1','index_root':'/synthetic/index',
       'original_root':'/synthetic/original','recovery_root':'/synthetic/recovery','index_prefix':'/synthetic/index/index/files/hg38/genome',
       'cumulative_body_bytes':p['prior_charged_body_bytes'],'remaining_body_budget_bytes':p['original_body_cap']-p['prior_charged_body_bytes'],
       'prior_transfer_elapsed_seconds':p['prior_transfer_elapsed_seconds'],'prior_global_deadline_epoch':p['prior_global_deadline_epoch'],
       'members':copy.deepcopy(profile['index_members']),'aligner':aligner}
    m={'transport':{'read_chunk_bytes':65536,'reservation_block_bytes':4194304,'attempts':1},'execution_policy':copy.deepcopy(profile['execution_policy']),
       'aligner':aligner,'archives':{},'paired_fastq':copy.deepcopy(profile['paired_fastq']),
       'real_compute':{k:{**copy.deepcopy(v),'limits':{'max_temp_bytes':4*1024**3,'fixture_only':True}} for k,v in profile['compute_fields'].items()},
       'sealed_workflow':{'schema':'cached-index-pilot-v1','mode':'real-pilot','origins':['https://ftp.sra.ebi.ac.uk'],'steps':copy.deepcopy(profile['steps']),'producer':{'fixture_only':True}},
       'cached_index':b,'cached_guard_sample_seconds':.1}
    return {'schema':'b5-prepared-real-pilot-v1','execution_enabled':False,'root':'/synthetic/index-reads-01','manifest':m,'limits':copy.deepcopy(profile['limits']),
            'host_observed':{'fixture_only':True},'unverified':['all host facts; synthetic descriptor'],'scope':'SYNTHETIC METADATA ONLY; NOT A REAL PLAN'}


def negatives(job):
    cases=[]
    def add(name,mutator):
        j=copy.deepcopy(job);mutator(j);cases.append((name,j))
    add('execution_enabled',lambda j:j.update(execution_enabled=True))
    add('extra_byte_budget',lambda j:j['limits'].update(transfer_bytes=12000000001))
    add('new_total_window',lambda j:j['limits'].update(wall_seconds=7201))
    add('new_http_window',lambda j:j['manifest']['execution_policy'].update(transfer_seconds=1801))
    add('refunded_previous_charge',lambda j:j['manifest']['cached_index'].update(cumulative_body_bytes=0))
    add('changed_prior_deadline',lambda j:j['manifest']['cached_index'].update(prior_global_deadline_epoch=0.))
    add('lost_spent_time',lambda j:j['manifest']['cached_index'].update(prior_transfer_elapsed_seconds=0.))
    add('more_prefix_pairs',lambda j:j['manifest']['paired_fastq']['CTRL_prefix'].update(prefix_pairs=2000000))
    add('boolean_prefix',lambda j:j['manifest']['paired_fastq']['CTRL_prefix'].update(prefix_pairs=True))
    add('relaxed_coverage',lambda j:j['manifest']['real_compute']['CTRL_compute'].update(minimum_fragment_union=1))
    add('changed_target',lambda j:j['manifest']['real_compute']['CTRL_compute']['targets'][0].__setitem__(1,0))
    add('index_download_added',lambda j:j['manifest']['archives'].update(index_archive={}))
    add('retry_added',lambda j:j['manifest']['transport'].update(attempts=2))
    add('alternate_origin',lambda j:j['manifest']['sealed_workflow'].update(origins=['https://example.invalid']))
    add('changed_md5',lambda j:j['manifest']['sealed_workflow']['steps'][1]['expected'].update(md5='0'*32))
    add('changed_url',lambda j:j['manifest']['sealed_workflow']['steps'][1].update(url='https://example.invalid/read.gz'))
    add('tdp_before_ctrl_compute',lambda j:j['manifest']['sealed_workflow']['steps'].__setitem__(slice(4,6),list(reversed(j['manifest']['sealed_workflow']['steps'][4:6]))))
    add('extra_library',lambda j:j['manifest']['real_compute'].update(OTHER={}))
    add('reused_original_root',lambda j:j.update(root='/synthetic/original'))
    add('path_traversal',lambda j:j.update(root='/synthetic/../index-reads-01'))
    add('altered_index_member',lambda j:j['manifest']['cached_index']['members'][0].update(sha256='0'*64))
    add('relaxed_temporary_cap',lambda j:j['manifest']['real_compute']['CTRL_compute']['limits'].update(max_temp_bytes=5*1024**3))
    return cases


class OfflineReviewTests(unittest.TestCase):
    def setUp(self):self.p,_=audit.load(audit.PROFILE);self.j=fixture(self.p)
    def test_profile_hash_pinned(self):self.assertEqual(audit.load(audit.PROFILE)[1],audit.PROFILE_SHA256)
    def test_positive_is_explicitly_non_authorizing(self):
        r=audit.review(self.j,self.p)
        for key in ['execution_enabled','raw_execution_ready','host_files_verified','window_authorized','replaces_worker_validation']:self.assertFalse(r[key])
        self.assertTrue(r['descriptor_source_not_authenticated'])
    def test_declared_negative_mutations_all_rejected(self):
        for name,value in negatives(self.j):
            with self.subTest(case=name),self.assertRaises(ValueError):audit.review(value,self.p)
    def test_real_archived_proposal_arithmetic(self):
        r=audit.proposal_review(self.p['proposal'],self.p);self.assertEqual(r['cumulative_if_both_downloaded'],10705506614);self.assertEqual(r['margin_bytes'],1294493386)
    def test_proposal_changes_rejected(self):
        p=copy.deepcopy(self.p['proposal']);p['prior_charged_body_bytes']=0
        with self.assertRaises(ValueError):audit.proposal_review(p,self.p)
    def test_no_network_process_or_host_paths_followed(self):
        import socket,subprocess
        with patch.object(Path,'open',side_effect=AssertionError('No host files')),patch.object(socket,'socket',side_effect=AssertionError('No network')),patch.object(subprocess,'Popen',side_effect=AssertionError('No process')):
            self.assertFalse(audit.review(self.j,self.p)['host_files_verified'])
    def test_duplicate_keys_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.json';p.write_text('{"x":1,"x":2}')
            self.assertRaises(ValueError,audit.load,p)
    def test_nonfinite_json_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            for text in ['NaN','Infinity','-Infinity','1e999']:
                p=Path(d)/'x.json';p.write_text('{"x":'+text+'}')
                with self.subTest(value=text),self.assertRaises(ValueError):audit.load(p)
    def test_oversized_input_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.json';p.write_text(' '*(2*1024**2+1))
            self.assertRaises(ValueError,audit.load,p)
    def test_invalid_extra_schema_rejected(self):
        self.j['unknown']=True;self.assertRaises(ValueError,audit.review,self.j,self.p)
    def test_pure_review_does_not_mutate_input(self):
        before=copy.deepcopy(self.j);audit.review(self.j,self.p);self.assertEqual(before,self.j)
    def test_repeated_projection_identical(self):self.assertEqual(audit.review(self.j,self.p),audit.review(copy.deepcopy(self.j),self.p))
    def test_spent_clock_tolerance_does_not_allow_reset(self):
        self.j['manifest']['cached_index']['prior_transfer_elapsed_seconds']+=.0000001
        audit.review(self.j,self.p)
        self.j['manifest']['cached_index']['prior_transfer_elapsed_seconds']-=1
        self.assertRaises(ValueError,audit.review,self.j,self.p)

    def test_invalid_spent_clock_direct_call_rejected(self):
        for value in (float('inf'),10**500,True):
            self.j['manifest']['cached_index']['prior_transfer_elapsed_seconds']=value
            with self.subTest(value_type=type(value).__name__),self.assertRaises(ValueError):audit.review(self.j,self.p)
    def test_control_characters_in_paths_rejected(self):
        self.j['root']='/synthetic/index-reads-01\x00'
        self.assertRaises(ValueError,audit.review,self.j,self.p)

    def test_proposal_cross_checked_against_four_mates(self):
        changed=copy.deepcopy(self.p);changed['steps'][1]['expected']['bytes']+=1
        self.assertRaises(ValueError,audit.proposal_review,changed['proposal'],changed)
