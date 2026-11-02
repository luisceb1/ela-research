"""Reproduce only local artificial FASTQ validation and process-limit planning."""
import gzip
import hashlib
import json
from pathlib import Path
import platform
import sys
import tempfile
from paired_fastq_integrity import validate_pair
from pilot_dry_runner import DryRunner


def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    def data(mate):return b''.join(f'@artificial-{i}/{mate}\nACGTN\n+\nIIIII\n'.encode() for i in range(3))
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp);r1=root/'one.gz';r2=root/'two.gz'
        r1.write_bytes(gzip.compress(data(1),mtime=0));r2.write_bytes(gzip.compress(data(2),mtime=0))
        results=[]
        for n in (1,2):
            result=validate_pair(r1,r2,root/f'pass{n}',2);results.append(result)
            (out/f'positive-{n}.json').write_text(json.dumps(result,indent=2)+'\n')
        if results[0]!=results[1]:raise ValueError('Repeated synthetic projection differs')
        broken=bytearray(r2.read_bytes());broken[-8]^=1;r2.write_bytes(broken)
        try:validate_pair(r1,r2,root/'bad-crc',2)
        except gzip.BadGzipFile:pass
        else:raise ValueError('Synthetic CRC corruption accepted')
        negative=json.loads((root/'bad-crc/result.json').read_bytes())
        (out/'negative-after-prefix.json').write_text(json.dumps(negative,indent=2)+'\n')
        caps={'wall_seconds':900,'rss_bytes':6*1024**3,'address_space_bytes':6*1024**3}
        limits={'wall_seconds':3600,'transfer_bytes':12000000000,'disk_bytes':25*1024**3,'reserve_bytes':0,'process_caps':caps}
        runner=DryRunner(root/'plan',{'fixture_only':True},limits)
        try:
            plan=runner.plan_process(['placeholder-no-execution'],caps)
            try:runner.process('disabled',['placeholder-no-execution'],process_limits=caps,production=True)
            except ValueError:disabled=True
            else:raise ValueError('Production unexpectedly executed')
        finally:runner.close()
        (out/'process-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
        summary={'python':platform.python_version(),'synthetic_source_pairs':3,'prefix_pairs':2,'full_scan_eof_crc_validated':True,
          'two_runs_byte_identical':True,'crc_corruption_after_prefix_rejected':negative['status']=='failed',
          'prefix_compressed':results[0]['prefixes'],'production_execution_rejected':disabled,
          'plan_values_only_not_resource_benchmark':True,'biological_data_opened':False,'external_data_connections':0,'raw_execution_ready':False,
          'global_read_identity_uniqueness_certified':False,'quality_encoding_inferred':False}
        (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':run(sys.argv[1])
