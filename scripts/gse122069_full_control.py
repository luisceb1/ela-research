#!/usr/bin/env python3
"""Frozen GSE122069 culture stream: ordered technical bins, bounded resources, two parsers.

No identifiers, sequences or sample-level clinical variables are exported.
The historical first1M runner remains unchanged.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.gse122069_pilot import TARGETS, empty_counts, verify_file
from scripts.audit_stmn2_junction_contract import sam_junctions
from scripts.hisat2_synthetic_gate import accepted_pysam
from scripts.fetch_gse122069_pilot import disk_guard
from scripts.gse122069_run_config import load_rows, configure, validate_receipt, aligner_command, DEFAULT_RUN


def save(path, obj):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2) + '\n')
    os.replace(tmp, path)


class Bins:
    """Query groups in HISAT2 --reorder output; one primary required per group.

    Names are held only for the current group, never serialized. Non-contiguous
    repeated names are not independently detected; --reorder and expected total
    are part of the input contract. Secondary records may precede a primary.
    """
    def __init__(self, size, expected, checkpoint=None):
        if size <= 0 or expected <= 0:
            raise ValueError('Positive bin size and expected reads required')
        self.size, self.expected, self.checkpoint = size, expected, checkpoint
        self.name = None
        self.primary = self.n = 0
        self.bins = []
        self.current = None

    def start(self, name, primary):
        if name != self.name:
            if self.name is not None:
                self.validate_group()
                if self.n % self.size == 0:
                    self.flush()
            self.name, self.primary = name, 0
            self.n += 1
            if self.n > self.expected:
                raise ValueError('More SAM query groups than expected')
            if self.current is None:
                self.current = {'first_read': self.n, 'last_read': self.n,
                                'reads': 0, 'sam_records': 0, 'primary_records': 0,
                                'counts': empty_counts()}
            self.current['last_read'] = self.n
            self.current['reads'] += 1
        self.primary += int(primary)
        self.current['primary_records'] += int(primary)
        self.current['sam_records'] += 1
        if self.primary > 1:
            raise ValueError('Multiple primary records in a query group')

    def validate_group(self):
        if self.primary != 1:
            raise ValueError('Query group lacks exactly one primary')

    def add(self, anchor, key):
        c = self.current['counts'][str(anchor)]
        c['eligible_intron_observations'] += 1
        if key in TARGETS:
            c[TARGETS[key]] += 1

    def flush(self):
        if self.current is not None:
            self.bins.append(self.current)
            self.current = None
            if self.checkpoint:
                self.checkpoint(self.snapshot(False))

    def snapshot(self, complete):
        counts = empty_counts()
        for b in self.bins:
            for a in counts:
                for k in counts[a]:
                    counts[a][k] += b['counts'][a][k]
        return {'complete_library': complete, 'completed_bins': self.bins,
                'reads': sum(b['reads'] for b in self.bins),
                'sam_records': sum(b['sam_records'] for b in self.bins),
                'counts': counts}

    def finish(self):
        if self.name is not None:
            self.validate_group()
        if self.n != self.expected:
            raise ValueError('SAM query count differs from fixed expected reads')
        self.flush()
        return self.snapshot(True)


def feed_fastq(path, target, expected, complete_library, checkpoint=None):
    """Validate records while streaming; full mode requires gzip EOF/CRC and no extra record."""
    lengths = Counter()
    n = bases = nbase = qsum = scanned = 0
    qmin, qmax = 127, 0
    with gzip.open(path, 'rb') as inp:
        for _ in range(expected):
            lines = [inp.readline(20000) for __ in range(4)]
            if any(not x.endswith(b'\n') for x in lines) or not lines[0].startswith(b'@') or not lines[2].startswith(b'+'):
                raise ValueError('Invalid/truncated FASTQ record')
            seq, qual = lines[1].rstrip(b'\r\n').upper(), lines[3].rstrip(b'\r\n')
            if not seq or len(seq) != len(qual) or set(seq) - set(b'ACGTN') or min(qual) < 33 or max(qual) > 126:
                raise ValueError('FASTQ sequence/quality schema failure')
            target.write(b''.join(lines).decode('ascii'))
            n += 1
            bases += len(seq)
            nbase += seq.count(b'N')
            lengths[len(seq)] += 1
            qsum += sum(qual)
            qmin, qmax = min(qmin, min(qual)), max(qmax, max(qual))
            scanned += sum(map(len, lines))
            if checkpoint and n % 1000000 == 0:
                checkpoint({'reads_streamed': n, 'bases': bases, 'N_bases': nbase,
                            'length_histogram': dict(lengths), 'gzip_eof_crc_validated': False})
        if complete_library and inp.read(1):
            raise ValueError('FASTQ contains more records than fixed library count')
    return {'reads': n, 'bases': bases, 'N_bases': nbase, 'length_histogram': dict(lengths),
            'quality_ascii_min': qmin, 'quality_ascii_max': qmax,
            'mean_quality_if_phred33': qsum / bases - 33,
            'uncompressed_bytes_scanned': scanned, 'gzip_eof_crc_validated': complete_library,
            'selection': 'entire fixed library' if complete_library else 'first fixed records, not random'}


def count_text(lines, bins, forward=None, on_accepted_junction=None):
    qc = Counter()
    for line in lines:
        if forward:
            forward.write(line)
        if line.startswith('@'):
            continue
        f = line.split('\t')
        flag = int(f[1])
        bins.start(f[0], not flag & (256 | 2048))
        qc['sam_records'] += 1
        for label, bit in [('unmapped', 4), ('secondary', 256), ('supplementary', 2048), ('qcfail', 512)]:
            qc[label + '_records'] += bool(flag & bit)
        for anchor in (8, 15):
            for key in sam_junctions(line, min_anchor=anchor):
                bins.add(anchor, key)
                if on_accepted_junction is not None:
                    on_accepted_junction(line, anchor, key)
    return qc


def count_htslib(out, expected, bin_size, on_accepted_read=None):
    import pysam
    bins = Bins(bin_size, expected, lambda obj: save(out, obj))
    locus = Counter()
    locus_bins = []
    def checkpoint(obj):
        locus_bins.append(dict(locus))
        locus.clear()
        obj['locus_bins'] = locus_bins
        save(out, obj)
    bins.checkpoint = checkpoint
    with pysam.AlignmentFile('-', 'r') as file:
        for read in file:
            bins.start(read.query_name, not (read.is_secondary or read.is_supplementary))
            if not (read.is_unmapped or read.is_secondary or read.is_supplementary or read.is_qcfail) and read.reference_name == 'chr8':
                blocks = read.get_blocks()
                if any(a < 79666158 and b > 79611116 for a, b in blocks):
                    locus['primary_block_overlap'] += 1
                    unique = 20 <= read.mapping_quality < 255 and read.has_tag('NH') and read.get_tag('NH') == 1
                    if unique:
                        locus['unique_mapq_block_overlap'] += 1
                        for label, left, right in [('exon1', 79611116, 79611214), ('exon2', 79636801, 79636897)]:
                            if any(a < right and b > left for a, b in blocks):
                                locus[label + '_unique_overlap'] += 1
                        if any(op == 3 for op, n in (read.cigartuples or [])):
                            locus['unique_spliced_reads'] += 1
            if not accepted_pysam(read):
                continue
            if on_accepted_read is not None:
                on_accepted_read(read)
            cigar = read.cigartuples or []
            cursor = read.reference_start
            introns = file.find_introns([read]) if any(op == 3 for op, n in cigar) else {}
            for i, (op, n) in enumerate(cigar):
                if op == 3:
                    anchors = []
                    for ops in (reversed(cigar[:i]), iter(cigar[i+1:])):
                        anchor = 0
                        for op2, n2 in ops:
                            if op2 not in (0, 7, 8):
                                break
                            anchor += n2
                        anchors.append(anchor)
                    if introns.get((cursor, cursor+n), 0):
                        key = (read.reference_name, cursor, cursor+n+1, read.get_tag('XS'))
                        for a in (8, 15):
                            if min(anchors) >= a:
                                bins.add(a, key)
                if op in (0, 2, 3, 7, 8):
                    cursor += n
    result = bins.finish()
    result.update(locus_bins=locus_bins, pysam=pysam.__version__,
                  htslib=pysam.version.__htslib_version__,
                  self_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    save(out, result)


def concordance(own, other):
    for k in ('reads', 'sam_records', 'counts', 'completed_bins'):
        if own[k] != other[k]:
            raise ValueError('Independent parser mismatch: ' + k)


def run(a, fastq_feeder=feed_fastq, text_counter=count_text, worker_script=None):
    start = time.monotonic()
    out = Path(a.out)
    if out.exists() and any(out.iterdir()):
        raise ValueError('Refuse non-empty execution directory')
    out.mkdir(parents=True, exist_ok=True)
    result = {'complete_library': False, 'run': getattr(a, 'run_accession', DEFAULT_RUN), 'sam_disk_written': False,
              'expected_reads': a.max_reads, 'bin_size': a.bin_size, 'combined_rss_available': False}
    bins = Bins(a.bin_size, a.max_reads, lambda obj: (save(out/'text-checkpoint.json', obj),
                print('completed reads', obj['reads'], 'elapsed seconds', round(time.monotonic()-start), flush=True)))
    procs, failures = [], []
    stop = threading.Event()
    def terminate():
        for proc in procs:
            if proc.poll() is None:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
    def monitor():
        while not stop.wait(0.5):
            try:
                if time.monotonic()-start > config['phase_deadline_seconds']:
                    raise TimeoutError('Fixed library phase exceeds explicit deadline')
                disk_guard(out)
            except Exception as exc:
                failures.append(type(exc).__name__ + ': ' + str(exc))
                terminate()
                return
    try:
        config = configure(load_rows(a.manifest), result['run'], a.max_reads, a.complete_library,
                           a.bin_size, getattr(a, 'phase_deadline_seconds', 1800))
        result.update(gsm=config['gsm'], experiment=config['experiment'], published_group=config['published_group'],
                      phase_deadline_seconds=config['phase_deadline_seconds'], configuration=config)
        download = json.loads(Path(a.download_record).read_text())
        digest = validate_receipt(config, download)
        result['fastq_sha256'] = verify_file(Path(a.fastq), config['expected_fastq_bytes'], config['expected_md5'], digest)
        expected = json.loads(Path(a.index_record).read_text())
        for entry in expected['verified_files']:
            verify_file(Path(a.index_directory).parent/entry['name'], entry['bytes'], None, entry['sha256'])
        if time.monotonic()-start > config['phase_deadline_seconds']:
            raise TimeoutError('Identity prechecks exceeded fixed phase deadline')
        binary = Path(a.source)/'hisat2-align-s'
        info = json.loads(Path(a.binary_record).read_text())
        digest = hashlib.sha256(binary.read_bytes()).hexdigest()
        if digest != info['hisat2-align-s']['sha256']:
            raise ValueError('Binary hash mismatch')
        result['binary_sha256'] = digest
        affinity = sorted(os.sched_getaffinity(0))[:2]
        os.sched_setaffinity(0, affinity)
        disk_guard(out)
        _, hard = resource.getrlimit(resource.RLIMIT_AS)
        resource.setrlimit(resource.RLIMIT_AS, (512*1024**2, hard))
        cmd = aligner_command(binary, a.prefix, a.max_reads)
        worker = ['prlimit', '--as=268435456', '--', a.pysam_python, str(worker_script or Path(__file__)), 'htslib',
                  '--out', str(out/'htslib-checkpoint.json'), '--max-reads', str(a.max_reads), '--bin-size', str(a.bin_size)]
        result.update(command=cmd, worker_command=worker, cpu_affinity=affinity,
                      prealignment_seconds=time.monotonic()-start,
                      virtual_address_caps={'aligner': 5368709120, 'parent': 536870912, 'htslib': 268435456})
        with (out/'hisat2.log').open('w') as log, (out/'htslib.stderr.txt').open('w') as err:
            align = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log,
                                     text=True, bufsize=65536, start_new_session=True)
            procs.append(align)
            hts = subprocess.Popen(worker, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=err,
                                   text=True, bufsize=65536, start_new_session=True)
            procs.append(hts)
            def feed():
                try:
                    qc = fastq_feeder(Path(a.fastq), align.stdin, a.max_reads, a.complete_library,
                                   lambda obj: save(out/'fastq-input-checkpoint.json', obj))
                    save(out/'fastq_qc.json', qc)
                    align.stdin.close()
                except Exception as exc:
                    failures.append('FASTQ producer: ' + type(exc).__name__ + ': ' + str(exc))
                    terminate()
            producer = threading.Thread(target=feed, daemon=True)
            watcher = threading.Thread(target=monitor, daemon=True)
            producer.start()
            watcher.start()
            result['sam_qc'] = dict(text_counter(align.stdout, bins, hts.stdin))
            hts.stdin.close()
            codes = [align.wait(), hts.wait()]
            producer.join()
            if failures or any(codes):
                raise RuntimeError('Pipeline failure: ' + str(codes) + '; ' + '; '.join(failures))
        own = bins.finish()
        other = json.loads((out/'htslib-checkpoint.json').read_text())
        concordance(own, other)
        qc = json.loads((out/'fastq_qc.json').read_text())
        if qc['reads'] != a.max_reads or (a.complete_library and not qc['gzip_eof_crc_validated']):
            raise ValueError('FASTQ completion contract failed')
        denominator = own['counts']['15']['canonical'] + own['counts']['15']['cryptic']
        result.update(own, complete_library=a.complete_library, independent_parser_concordant=True,
                      coverage_rule={'minimum_denominator': 20, 'achieved': denominator >= 20,
                                     'scope': 'technical library only; no PSI, effect or biological absence'})
    except Exception as exc:
        result['error'] = type(exc).__name__ + ': ' + str(exc)
        # Preserve validated completed bins, including timeout prefix; never call full.
        result['partial'] = bins.snapshot(False)
        otherpath = out/'htslib-checkpoint.json'
        if otherpath.exists():
            other = json.loads(otherpath.read_text())
            common = min(len(bins.bins), len(other['completed_bins']))
            result['common_completed_bins'] = common
            result['common_bins_concordant'] = bins.bins[:common] == other['completed_bins'][:common]
        raise
    finally:
        stop.set()
        terminate()
        for proc in procs:
            proc.wait()
        result.update(elapsed_seconds=time.monotonic()-start, watchdog_errors=failures,
                      self_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      maxrss_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        save(out/'full-control-results.json', result)


if __name__ == '__main__':
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('mode', choices=['run', 'htslib', 'plan'])
    p.add_argument('--out', required=True)
    p.add_argument('--max-reads', type=int, default=1000000)
    p.add_argument('--bin-size', type=int, default=1000000)
    p.add_argument('--complete-library', action='store_true')
    p.add_argument('--run-accession', default=DEFAULT_RUN)
    p.add_argument('--phase-deadline-seconds', type=int, default=1800)
    for name in ['manifest', 'download-record', 'fastq', 'index-record', 'index-directory', 'binary-record', 'source', 'prefix', 'pysam-python']:
        p.add_argument('--'+name)
    a = p.parse_args()
    if a.mode == 'htslib':
        count_htslib(Path(a.out), a.max_reads, a.bin_size)
    elif a.mode == 'plan':
        config = configure(load_rows(a.manifest), a.run_accession, a.max_reads, a.complete_library, a.bin_size, a.phase_deadline_seconds)
        destination = Path(a.out)
        destination.mkdir(parents=True, exist_ok=True)
        config['mode'] = 'plan_only_no_fastq_or_alignment_opened'
        save(destination/'execution-config.json', config)
        print(json.dumps(config, indent=2))
    else:
        run(a)
