"""Offline software controls; all reads, responses and processes here are fixtures."""
import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.error
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import run_gse252892_local as m
import pysam
TARGETS=json.loads((ROOT/'research/references/unc13a_targets_sealed.json').read_text())['junctions']
HEADER=pysam.AlignmentHeader.from_dict({'SQ':[{'SN':'chr19','LN':58617616}]})


def read(name='q',first=True,label='canonical',anchor=15):
    a,b=TARGETS[label]
    r=pysam.AlignedSegment(HEADER);r.query_name=name;r.flag=99 if first else 147
    r.reference_id=0;r.reference_start=a-anchor;r.mapping_quality=60
    r.cigartuples=[(0,anchor),(3,b-a),(0,anchor)]
    r.query_sequence='A'*(anchor*2);r.query_qualities=pysam.qualitystring_to_array('I'*(anchor*2))
    r.next_reference_id=0;r.next_reference_start=a-anchor;r.set_tag('NH',1);r.set_tag('XS','-')
    return r


def pair(**kwargs):return [read(first=True,**kwargs),read(first=False,**kwargs)]


class Response(io.BytesIO):
    def __init__(self,b,url,status=200,length=None):
        super().__init__(b);self.status=status;self.url=url
        self.headers={'Content-Length':str(len(b) if length is None else length)}
    def geturl(self):return self.url


class Opener:
    def __init__(self,b,url,**kw):self.b=b;self.url=url;self.kw=kw;self.calls=0
    def open(self,req,timeout):self.calls+=1;return Response(self.b,self.url,**self.kw)


class DownloadTests(unittest.TestCase):
    def run_download(self,mutate=None,**response):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);d=Path(tmp.name)
        body=gzip.compress(b'fixture paired data')
        item={'url':'https://ftp.sra.ebi.ac.uk/fixture.fastq.gz','compressed_bytes':str(len(body)),'md5':hashlib.md5(body).hexdigest()}
        if mutate:mutate(item)
        ledger={'actual_body_bytes':0,'requests':[]};op=Opener(body,item['url'],**response)
        return d,body,item,ledger,op

    def test_verified_download_and_charge(self):
        d,b,item,ledger,op=self.run_download();p=m.download(item,d,ledger,d/'ledger.json',op)
        self.assertEqual(p.read_bytes(),b);self.assertEqual(ledger['actual_body_bytes'],len(b));self.assertEqual(op.calls,1)
        self.assertEqual(ledger['requests'][0]['status'],'verified')
        self.assertEqual(ledger['requests'][0]['sha256'],hashlib.sha256(b).hexdigest())

    def test_md5_failure_retains_partial_and_charge(self):
        d,b,item,ledger,op=self.run_download(lambda x:x.update(md5='0'*32))
        with self.assertRaisesRegex(ValueError,'MD5'):m.download(item,d,ledger,d/'ledger.json',op)
        self.assertEqual(ledger['actual_body_bytes'],len(b));self.assertEqual(op.calls,1)
        self.assertTrue(list(d.glob('*.partial')));self.assertEqual(ledger['requests'][0]['status'],'failed')

    def test_wrong_length_header_stops_without_reading_payload(self):
        d,b,item,ledger,op=self.run_download(length=999)
        with self.assertRaisesRegex(ValueError,'Content-Length'):m.download(item,d,ledger,d/'ledger.json',op)
        self.assertEqual(ledger['actual_body_bytes'],0)

    def test_body_overflow_is_charged_and_refused(self):
        d,b,item,ledger,op=self.run_download();item['compressed_bytes']=str(len(b)-1);op.kw['length']=len(b)-1
        with self.assertRaisesRegex(ValueError,'larger'):m.download(item,d,ledger,d/'ledger.json',op)
        self.assertEqual(ledger['actual_body_bytes'],len(b))

    def test_budget_refused_before_request(self):
        d,b,item,ledger,op=self.run_download();ledger['actual_body_bytes']=m.CAPS['transfer_bytes']-1
        with self.assertRaisesRegex(ValueError,'budget'):m.download(item,d,ledger,d/'ledger.json',op)
        self.assertEqual(op.calls,0)

    def test_existing_file_not_overwritten(self):
        d,b,item,ledger,op=self.run_download();(d/'fixture.fastq.gz').write_text('keep')
        with self.assertRaisesRegex(ValueError,'overwrite'):m.download(item,d,ledger,d/'ledger.json',op)
        self.assertEqual(op.calls,0);self.assertEqual((d/'fixture.fastq.gz').read_text(),'keep')

    def test_redirect_handler_has_no_fallback(self):
        with self.assertRaisesRegex(ValueError,'Redirect'):m.NoRedirect().redirect_request(None,None,302,'',{},'https://elsewhere/')

    def test_HTTP_error_body_is_charged_without_retry(self):
        d,b,item,ledger,op=self.run_download()
        error=urllib.error.HTTPError(item['url'],500,'fixture error',{},io.BytesIO(b'error body'))
        with patch.object(op,'open',side_effect=error) as call:
            with self.assertRaises(urllib.error.HTTPError):m.download(item,d,ledger,d/'ledger.json',op)
        self.assertEqual(call.call_count,1)
        self.assertEqual(ledger['actual_body_bytes'],10)
        self.assertEqual(json.loads((d/'ledger.json').read_text())['requests'][0]['status'],'failed')

    def test_partial_read_failure_keeps_observed_charge(self):
        d,b,item,ledger,op=self.run_download()
        response=Response(b,item['url'])
        with patch.object(response,'read',side_effect=[b[:10],OSError('fixture interrupted')]), patch.object(op,'open',return_value=response):
            with self.assertRaises(OSError):m.download(item,d,ledger,d/'ledger.json',op)
        self.assertEqual(ledger['actual_body_bytes'],10)
        self.assertEqual(next(d.glob('*.partial')).read_bytes(),b[:10])


class CountTests(unittest.TestCase):
    def test_both_mates_count_once(self):
        out=m.count_records(pair(),TARGETS);self.assertEqual(out['counts']['canonical'],1)
        self.assertTrue(out['positive_control_measured']);self.assertFalse(out['support_at_least_20_groups']['cryptic_left'])

    def test_separate_events_and_libraries(self):
        a=m.count_records(pair(label='cryptic_left'),TARGETS);b=m.count_records(pair(label='cryptic_right'),TARGETS)
        self.assertEqual(a['counts'],{'canonical':0,'cryptic_left':1,'cryptic_right':0})
        self.assertEqual(b['counts'],{'canonical':0,'cryptic_left':0,'cryptic_right':1})

    def test_cryptic_can_exceed_canonical(self):
        records=[]
        for i in range(21):records+=pair(name=str(i),label='cryptic_left')
        out=m.count_records(records,TARGETS)
        self.assertEqual(out['counts']['canonical'],0);self.assertEqual(out['counts']['cryptic_left'],21)

    def test_insufficient_anchor_excluded(self):
        self.assertEqual(m.count_records(pair(anchor=14),TARGETS)['counts']['canonical'],0)

    def test_wrong_XS_excluded(self):
        reads=pair()
        for r in reads:r.set_tag('XS','+')
        self.assertEqual(m.count_records(reads,TARGETS)['counts']['canonical'],0)

    def test_multimapping_excluded(self):
        reads=pair();reads[0].set_tag('NH',2)
        self.assertEqual(m.count_records(reads,TARGETS)['counts']['canonical'],0)

    def test_MAPQ_255_not_unique(self):
        reads=pair();reads[0].mapping_quality=255
        self.assertEqual(m.count_records(reads,TARGETS)['counts']['canonical'],0)

    def test_bad_mate_links_excluded(self):
        reads=pair();reads[0].next_reference_start+=1
        self.assertEqual(m.count_records(reads,TARGETS)['counts']['canonical'],0)

    def test_supplementary_not_primary_pair(self):
        reads=pair();reads[0].flag|=2048
        self.assertEqual(m.count_records(reads,TARGETS)['counts']['canonical'],0)

    def test_duplicate_flag_not_molecular_dedup(self):
        reads=pair()
        for r in reads:r.flag|=1024
        out=m.count_records(reads,TARGETS);self.assertEqual(out['counts']['canonical'],1)
        self.assertEqual(out['qc']['marked_duplicate_records'],2)

    def test_pysam_introns_agree_with_sealed_half_open_interval(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'toy.sam'
            with pysam.AlignmentFile(p,'w',header=HEADER) as f:
                for r in pair():f.write(r)
            with pysam.AlignmentFile(p,'r') as f:
                introns=f.find_introns(f)
            self.assertEqual(introns[tuple(TARGETS['canonical'])],2)
            with pysam.AlignmentFile(p,'r') as f:out=m.count_records(f,TARGETS)
            self.assertEqual(out['counts']['canonical'],1)

    def test_ambiguous_extra_record_excluded(self):
        out=m.count_records(pair()+[read()],TARGETS)
        self.assertEqual(out['counts']['canonical'],0);self.assertEqual(out['qc']['rejected_groups'],1)


class StopTests(unittest.TestCase):
    def test_windows_probe_uses_existing_PATH_entry(self):
        with patch.object(m.shutil,'which',return_value='/fixture/powershell.exe'),patch.object(m.Path,'is_file',return_value=True):
            self.assertEqual(m.windows_powershell(),'/fixture/powershell.exe')

    def test_windows_probe_falls_back_when_PATH_has_no_Windows_entries(self):
        with patch.object(m.shutil,'which',return_value=None),patch.object(m.Path,'is_file',return_value=True):
            self.assertEqual(m.windows_powershell(),'/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe')

    def test_missing_both_windows_locations_still_blocks(self):
        with patch.object(m.shutil,'which',return_value=None),patch.object(m.Path,'is_file',return_value=False):
            with self.assertRaisesRegex(ValueError,'real C: free space is still required'):m.windows_free()

    def test_real_space_query_uses_resolved_executable(self):
        path='/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe'
        with patch.object(m,'windows_powershell',return_value=path),patch.object(m.subprocess,'check_output',return_value='\ufeff123456789012\r\n') as call:
            self.assertEqual(m.windows_free(),123456789012)
            self.assertEqual(call.call_args.args[0][0],path)
            self.assertEqual(call.call_args.args[0][-1],'(Get-PSDrive -Name C).Free')

    def test_invalid_space_output_cannot_fall_back_to_virtual_disk(self):
        with patch.object(m,'windows_powershell',return_value='fixture'),patch.object(m.subprocess,'check_output',return_value='not a byte count'):
            with self.assertRaisesRegex(ValueError,'Cannot parse'):m.windows_free()

    def test_disabled_Windows_executable_interop_still_blocks(self):
        with patch.object(m,'windows_powershell',return_value='fixture'),patch.object(m.subprocess,'check_output',side_effect=OSError('Exec format error')):
            with self.assertRaisesRegex(ValueError,'verify Windows executable interop'):m.windows_free()

    def test_timeout_does_not_weaken_physical_space_guard(self):
        with patch.object(m,'windows_powershell',return_value='fixture'),patch.object(m.subprocess,'check_output',side_effect=subprocess.TimeoutExpired('fixture',15)):
            with self.assertRaisesRegex(ValueError,'Cannot query real C: free space'):m.windows_free()

    def test_unsupported_tool_option_stops_preparation(self):
        with patch.object(m.subprocess,'run',return_value=SimpleNamespace(stdout='fixture help',stderr='')):
            with self.assertRaisesRegex(ValueError,'CLI options'):m.check_options('fixture',['--detect_adapter_for_pe'])

    def test_physical_space_guard(self):
        with self.assertRaisesRegex(ValueError,'reserve'):m.check_free(1)

    def test_symlink_in_runroot_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'link').symlink_to('/tmp')
            with self.assertRaisesRegex(ValueError,'Symlink'):m.root_bytes(p)

    def test_process_group_stopped(self):
        proc=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'],start_new_session=True)
        self.addCleanup(lambda:proc.kill() if proc.poll() is None else None)
        m.stop_group(proc);self.assertIsNotNone(proc.poll())

    def test_changed_cap_refused(self):
        with self.assertRaisesRegex(ValueError,'caps'):m.validate_plan({'schema':'gse252892-bounded-v1','caps':{}},False)

    def test_no_execution_without_explicit_matching_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'plan.json';p.write_text('{}')
            with self.assertRaisesRegex(ValueError,'acceptance'):m.execute(p,'0'*64,m.CAPS['transfer_bytes'])

    def test_internal_worker_cannot_start_without_supervisor_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'plan.json';p.write_text(json.dumps({'run_root':tmp}))
            with self.assertRaises(FileNotFoundError):m.worker(p)

    def test_supervisor_wall_stop_records_failure_and_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'plan.json';root=Path(tmp)/'new-root';p.write_text(json.dumps({'run_root':str(root)}))
            limits=dict(m.CAPS);limits['wall_seconds']=0
            with patch.object(m,'validate_plan'),patch.object(m,'windows_free',return_value=1000*1024**3),patch.object(m,'CAPS',limits):
                with self.assertRaisesRegex(ValueError,'Wall time'):m.execute(p,m.prep.sha256(p),limits['transfer_bytes'])
            receipt=json.loads((root/'supervision.json').read_text())
            self.assertEqual(receipt['status'],'failed');self.assertIsNone(receipt['cleanup_error'])
            self.assertTrue(Path(str(p)+'.claimed.json').exists())

    def test_control_failure_does_not_call_KD_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'plan.json'
            p.write_text(json.dumps({'run_root':str(root),'base':{'tools':{'inspector':{'path':'fixture'}},'index_directory':'fixture'}}))
            (root/'accepted.json').write_text(json.dumps({'supervisor_pid':os.getppid(),'plan_sha256':m.prep.sha256(p),'transfer_bytes':m.CAPS['transfer_bytes']}))
            def fake_inspect(argv,stdout,**kw):stdout.write(b'Sequence-19 chr19 58617616\n')
            with patch.object(m.os,'getpgrp',return_value=os.getpid()),patch.object(m,'validate_plan'),patch.object(m.subprocess,'run',side_effect=fake_inspect),patch.object(m,'stage',return_value={'positive_control_measured':False}) as call:
                m.worker(p)
            self.assertEqual(call.call_count,1)
            self.assertEqual(call.call_args.args[1],'GSM8009878')
            self.assertEqual(json.loads((root/'result.json').read_text())['status'],'control_failed_KD_not_downloaded')
