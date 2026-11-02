import copy
import gzip
import hashlib
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import threading
import unittest
from unittest.mock import patch

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts';sys.path.insert(0,str(SCRIPTS))
try:
    from pilot_dry_runner import DryRunner
    from bounded_http_transport import transfer_http
    from external_local_stage import run_local_stage
    import archive_ledger_phase as archive
finally:sys.path.pop(0)


def make_tar(entries):
    out=io.BytesIO()
    with tarfile.open(fileobj=out,mode='w',format=tarfile.USTAR_FORMAT) as tf:
        for name,data,kind in entries:
            info=tarfile.TarInfo(name);info.type=kind;info.size=len(data) if kind in (tarfile.REGTYPE,tarfile.AREGTYPE) else 0
            if kind in (tarfile.SYMTYPE,tarfile.LNKTYPE):info.linkname='../escape'
            tf.addfile(info,io.BytesIO(data) if info.isreg() else None)
    return out.getvalue()


def metadata(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.r=None;self.addCleanup(self.close)
        self.entries=[('index/a.ht2',b'a'*83,tarfile.REGTYPE),('index/b.ht2',b'bc'*57,tarfile.REGTYPE)]
        self.configure()
    def close(self):
        if self.r:self.r.close();self.r=None
    def configure(self,entries=None,tar_bytes=None):
        if entries is not None:self.entries=entries
        self.raw=make_tar(self.entries) if tar_bytes is None else tar_bytes;self.blob=gzip.compress(self.raw,mtime=0)
        members=[{'name':n,**metadata(b)} for n,b,k in self.entries if k in (tarfile.REGTYPE,tarfile.AREGTYPE)]
        spec={'transfer':'source','identity':'synthetic/index-v1','expected':metadata(self.blob),'members':members,'max_members':16,'max_expanded_bytes':4096,'max_tar_bytes':32768}
        self.manifest={'archives':{'unpack':spec}};self.limits={'wall_seconds':30,'transfer_bytes':1024**2,'disk_bytes':4*1024**2,'reserve_bytes':0}
    def open(self):self.r=DryRunner(self.root,self.manifest,self.limits);return self.r
    def ready(self):
        r=self.open();r.transfer('source',[self.blob],metadata(self.blob));return r
    def verified(self):r=self.ready();r.archive('unpack');return r
    @property
    def out(self):return self.root/'archives/unpack'
    @property
    def spec(self):return self.manifest['archives']['unpack']
    def rejected(self,exc=ValueError):
        r=self.ready()
        with self.assertRaises(exc):r.archive('unpack')
        self.assertEqual(r.state['phases']['unpack']['status'],'failed')
        if (self.out/'result.json').exists():self.assertEqual(json.loads((self.out/'result.json').read_text())['status'],'failed')
        self.close()
        with self.assertRaises(ValueError):self.open()
    def test_success_reopen_preserves_budget_deadline_and_files(self):
        r=self.verified();before=copy.deepcopy(r.state);mtime=(self.out/'result.json').stat().st_mtime_ns;self.close()
        b=self.open();b.archive('unpack');self.assertEqual(before,b.state);self.assertEqual(mtime,(self.out/'result.json').stat().st_mtime_ns)
        for n,data,_ in self.entries:self.assertEqual((self.out/'files'/n).read_bytes(),data)
        self.assertFalse((self.out/'partial').exists())
    def test_explicit_directories_and_zero_length_file(self):
        self.configure([('index',b'',tarfile.DIRTYPE),('index/empty',b'',tarfile.REGTYPE)]);self.verified();self.assertEqual((self.out/'files/index/empty').stat().st_size,0)
    def test_names_with_partial_suffix_do_not_collide(self):
        self.configure([('a.partial',b'first',tarfile.REGTYPE),('a',b'second',tarfile.REGTYPE)]);self.verified()
        self.assertEqual((self.out/'files/a.partial').read_bytes(),b'first');self.assertEqual((self.out/'files/a').read_bytes(),b'second')
    def test_sha_only_http_to_archive_and_cached_reuse(self):
        payload=self.blob;requests=[]
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_GET(self):requests.append(self.path);self.send_response(200);self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            r=self.open();origin=f'http://127.0.0.1:{server.server_port}'
            transfer_http(r,'source',origin+'/index',metadata(payload),[origin],reserve_reads=True)
            r.archive('unpack');before=copy.deepcopy(r.state);self.close();self.open().archive('unpack')
            self.assertEqual(before,self.r.state);self.assertEqual(requests,['/index'])
            receipt=json.loads((self.root/'source.attempt-0.json').read_text());self.assertEqual(set(receipt['expected_checksums']),{'sha256'})
        finally:server.shutdown();server.server_close();thread.join()
    def test_crc_corruption_after_complete_members_rejected(self):
        blob=bytearray(self.blob);blob[-8]^=1;self.blob=bytes(blob);self.spec['expected']=metadata(self.blob);self.rejected(gzip.BadGzipFile)
        self.assertFalse(any((self.out/'files').rglob('*.ht2')))
    def test_truncated_gzip_rejected(self):
        self.blob=self.blob[:-4];self.spec['expected']=metadata(self.blob);self.rejected(EOFError)
    def test_missing_member_rejected(self):
        self.spec['members'].append({'name':'index/missing',**metadata(b'z')});self.rejected()
    def test_unknown_member_rejected(self):self.spec['members']=self.spec['members'][:1];self.rejected()
    def test_duplicate_archive_member_rejected(self):
        self.configure(self.entries+[self.entries[0]]);self.spec['members']=self.spec['members'][:2];self.rejected()
    def test_symlink_and_hardlink_rejected(self):
        for kind in (tarfile.SYMTYPE,tarfile.LNKTYPE):
            with self.subTest(kind=kind):
                with tempfile.TemporaryDirectory() as sub:
                    self.root=Path(sub);self.configure(self.entries[:2]+[('link',b'',kind)]);self.rejected()
    def test_traversal_absolute_dot_and_noncanonical_names_rejected(self):
        for name in ('../outside','/outside','.', 'a/../outside','a//b','a\\b'):
            with self.subTest(name=name):self.assertRaises(ValueError,archive.safe_name,name)
        self.configure(self.entries+[('../outside',b'x',tarfile.REGTYPE)]);self.spec['members']=self.spec['members'][:2];self.rejected();self.assertFalse((self.root/'outside').exists())
    def test_member_size_mismatch_rejected(self):self.spec['members'][0]['bytes']+=1;self.rejected()
    def test_member_hash_mismatch_rejected(self):self.spec['members'][0]['sha256']='0'*64;self.rejected()
    def test_member_cap_rejected(self):
        self.configure([('index',b'',tarfile.DIRTYPE)]+self.entries);self.spec['max_members']=2;self.rejected()
    def test_expanded_cap_below_inventory_rejected_before_phase(self):
        self.spec['max_expanded_bytes']=1;r=self.ready()
        with self.assertRaises(ValueError):r.archive('unpack')
        self.assertNotIn('unpack',r.state['phases'])
    def test_tar_stream_cap_rejected(self):self.spec['max_tar_bytes']=4096;self.rejected()
    def test_bad_tar_header_rejected(self):
        data=bytearray(self.raw);data[0]^=1;self.configure(tar_bytes=bytes(data));self.rejected(tarfile.HeaderError)
    def test_pax_header_rejected_without_loading_declared_payload(self):
        info=tarfile.TarInfo('PaxHeader');info.type=tarfile.XHDTYPE;info.size=2**40
        data=info.tobuf(format=tarfile.GNU_FORMAT)+b'\0'*1024
        self.configure(tar_bytes=data);self.rejected()
    def test_nonzero_padding_rejected(self):
        data=bytearray(self.raw);data[512+len(self.entries[0][1])]=1;self.configure(tar_bytes=bytes(data));self.rejected()
    def test_nonzero_data_after_tar_end_rejected(self):self.configure(tar_bytes=self.raw+b'not-zero');self.rejected()
    def test_missing_second_zero_end_record_rejected(self):
        self.configure(tar_bytes=self.raw[:2048]+b'\0'*512+b'nonzero'+b'\0'*505);self.rejected()
    def test_truncated_tar_inside_valid_gzip_rejected(self):self.configure(tar_bytes=self.raw[:2500]);self.rejected()
    def test_concatenated_gzip_member_not_ignored(self):
        self.blob+=gzip.compress(b'not-zero',mtime=0);self.spec['expected']=metadata(self.blob);self.rejected()
    def test_mutated_source_outputs_receipt_and_transfer_receipt_block_reopen(self):
        for target in ('source','output','receipt','transfer'):
            with self.subTest(target=target),tempfile.TemporaryDirectory() as sub:
                self.root=Path(sub);self.configure();r=self.verified()
                if target=='source':(self.root/'source').write_bytes(b'bad')
                elif target=='output':(self.out/'files/index/a.ht2').write_bytes(b'bad')
                elif target=='receipt':(self.out/'result.json').write_text('{"status":"started"}')
                else:r.state['phases']['source']['signature']='changed';r.save()
                self.close()
                with self.assertRaises(ValueError):self.open()
    def test_same_instance_reuse_rechecks_outputs(self):
        r=self.verified();(self.out/'files/index/a.ht2').write_bytes(b'bad');self.assertRaises(ValueError,r.archive,'unpack')
    def test_http_receipt_tampering_blocks_reuse(self):
        r=self.ready();phase=r.state['phases']['source'];phase['attempts_used']=1
        receipt=self.root/'source.attempt-0.json';record={'status':'verified','body_bytes':phase['bytes'],'md5':phase['md5'],'sha256':phase['sha256']};receipt.write_text(json.dumps(record));r.save();r.archive('unpack')
        record['status']='started';receipt.write_text(json.dumps(record));self.close();self.assertRaises(ValueError,self.open)
    def test_extra_output_rejected(self):
        self.verified();(self.out/'files/extra').write_bytes(b'x');self.close();self.assertRaises(ValueError,self.open)
    def test_changed_identity_caps_or_limits_rejected(self):
        self.verified();self.close();original=copy.deepcopy(self.manifest)
        for change in ('identity','max_tar_bytes','limits'):
            self.manifest=copy.deepcopy(original)
            if change=='identity':self.spec['identity']='other'
            elif change=='max_tar_bytes':self.spec['max_tar_bytes']+=1
            else:self.limits['wall_seconds']+=1
            self.assertRaises(ValueError,self.open)
    def test_keyboard_interrupt_records_failed_and_blocks_resume(self):
        r=self.ready()
        with patch.object(archive,'extract',side_effect=KeyboardInterrupt):self.assertRaises(KeyboardInterrupt,r.archive,'unpack')
        self.assertEqual(r.state['phases']['unpack']['status'],'failed');self.close();self.assertRaises(ValueError,self.open)
    def test_hard_external_timeout_keeps_started_and_partials(self):
        r=self.ready();before=copy.deepcopy(r.state);self.close()
        rec=run_local_stage(self.root,self.manifest,self.limits,{'kind':'archive','name':'unpack'},timeout=1,synthetic_fault='stall_archive')
        self.assertEqual(rec['violation'],'timeout');self.assertEqual(rec['exit_code'],-9);self.assertEqual(rec['live_group_members_after_cleanup'],[])
        self.assertGreaterEqual(rec['max_group_members'],2)
        ledger=json.loads((self.root/'ledger.json').read_text());self.assertEqual(ledger['phases']['unpack']['status'],'started')
        for key in ('deadline_epoch','transfer_bytes_consumed'):self.assertEqual(before[key],ledger[key])
        self.assertTrue(any(p.is_file() for p in (self.out/'partial').rglob('*')));self.assertRaises(ValueError,self.open)
    def test_orphan_output_not_adopted(self):
        r=self.ready();self.out.mkdir(parents=True);self.assertRaises(FileExistsError,r.archive,'unpack');self.assertEqual(r.state['phases']['unpack']['status'],'failed')
    def test_duplicate_inventory_and_file_directory_collision_rejected(self):
        for member in ({**self.spec['members'][0]},{'name':'index',**metadata(b'x')}):
            with tempfile.TemporaryDirectory() as sub:
                self.root=Path(sub);self.configure();self.spec['members'].append(member);r=self.ready();self.assertRaises(ValueError,r.archive,'unpack');self.close()


if __name__=='__main__':unittest.main()
