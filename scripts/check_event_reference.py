#!/usr/bin/env python3
"""Known-event coordinates and count semantics. No biological inference."""
import csv
import hashlib
import itertools
import json
import math
import platform
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
try:
    from scripts import geo_audit as a
except ModuleNotFoundError:
    import geo_audit as a

OUT = a.ROOT / 'reports/event-reference'
ARTICLE_URL = 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12023386/fullTextXML'
DOI = '10.1186/s13024-025-00820-5'
TOLERANCE = 1e-4  # independently rounded counts/fullLengthCounts


def project_article(raw):
    root = ET.fromstring(raw)
    dois = [e.text for e in root.findall('.//article-id') if e.get('pub-id-type') == 'doi']
    if DOI not in dois:
        raise ValueError('Unexpected article DOI')
    methods = root.find('.//body')
    if methods is None or 'GRCh38.primary_assembly' not in ' '.join(methods.itertext()):
        raise ValueError('Assembly not verified in primary article')
    matches = []
    for fig in root.iter('fig'):
        text = ' '.join(fig.itertext())
        if 'STMN2' not in text:
            continue
        coords = re.findall(r'\b(chr\w+):(\d+):(\d+)\b', text)
        for chrom, left, right in coords:
            matches.append((fig.get('id'), chrom, int(left), int(right)))
    if len(matches) != 1:
        raise ValueError(f'Unique STMN2 figure coordinate required: {matches}')
    fig, chrom, left, right = matches[0]
    if chrom != 'chr8' or left >= right:
        raise ValueError('Unexpected STMN2 coordinate context')
    obj = {'doi': DOI, 'pmid': '40275359', 'pmcid': 'PMC12023386', 'figure': fig,
           'symbol': 'STMN2', 'assembly': 'GRCh38', 'chrom': chrom,
           'left_exonic_boundary': left, 'right_exonic_boundary': right,
           'strand_in_caption': None, 'coordinate_convention': 'reported splice junction endpoints; exact comparison to GTF exonic boundaries',
           'claim_scope': 'junction_identity_only_not_full_transcript_or_polyA',
           'retention': 'molecular coordinate projection only; no individual clinical tables retained'}
    return (json.dumps(obj, indent=2, sort_keys=True) + '\n').encode()


def junction_matches(event, chrom, strand, left, right, gene_strand):
    if event['assembly'] != 'GRCh38':
        raise ValueError('Assembly must be GRCh38')
    return (chrom, strand, left, right) == (event['chrom'], gene_strand,
                                          event['left_exonic_boundary'], event['right_exonic_boundary'])


def gene_strand_from_gtf():
    # Independently derive orientation from the already pinned GENCODE reference.
    strands = set()
    with __import__('gzip').open(a.DATA / 'gencode.v47.annotation.gtf.gz', 'rt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            row = line.rstrip('\n').split('\t')
            if row[2] != 'gene' or 'gene_name "STMN2";' not in row[8]:
                continue
            attr = a.attrs(row[8])
            if attr['gene_id'].split('.')[0] == a.TARGETS['STMN2']:
                strands.add(row[6])
    if len(strands) != 1:
        raise ValueError(f'Unresolved STMN2 orientation: {strands}')
    return next(iter(strands))


def load_tsv(path):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter='\t'))


def quant_violations(unique, full, total, tolerance=TOLERANCE):
    problems = []
    if unique > total + tolerance:
        problems.append('unique_exceeds_total')
    if full > total + tolerance:
        problems.append('full_length_exceeds_total')
    return problems


def one_isoform_unique_witness(observed_read_classes):
    """Algebraic scalar witness to K*n.obs*A_unique in source; NOT R execution."""
    total = sum(observed_read_classes)
    if total == 0:
        return 0.
    return sum(total * (x / total) for x in observed_read_classes)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    mpath = OUT / 'sources.json'
    manifest = json.loads(mpath.read_text()) if mpath.exists() else {}
    errors, depths, target_support, problems = [], [], [], []
    try:
        # Fetch immutable code revision and verify package and Git blob identity.
        index = json.loads((a.ROOT / 'research/bambu326_source_index.json').read_text())
        for rec in index['files']:
            raw = a.fetch(rec['url'], a.DATA / 'bambu326' / rec['path'], manifest)
            blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
            if blob != rec['blob_sha']:
                raise ValueError(f'Git source mismatch: {rec["path"]}')
        if 'Version: 3.2.6\n' not in (a.DATA / 'bambu326/DESCRIPTION').read_text():
            raise ValueError('Wrong bambu version')
        raw = a.fetch(ARTICLE_URL, a.DATA / 'PMC12023386.event_projection.json', manifest, project=project_article)
        manifest['PMC12023386.event_projection.json']['projection'] = 'molecular_coordinate_projection'
        event = json.loads(raw)
        a.dump_json(OUT / 'paper_evidence.json', event)
        # Pinned reference/GEO inputs must still match previous audit manifests.
        old_manifest = json.loads((a.OUT / 'sources.json').read_text())
        ref = json.loads((a.ROOT / 'reports/isoforms/reference_source.json').read_text())
        refname = 'gencode.v47.annotation.gtf.gz'
        if a.sha256((a.DATA / refname).read_bytes()) != ref[refname]['source_sha256']:
            raise ValueError('GENCODE reference hash changed')
        gene_strand = gene_strand_from_gtf()
        matches = []
        for row in load_tsv(a.ROOT / 'reports/isoforms/junctions.tsv'):
            matched = junction_matches(event, row['chrom'], row['strand'], int(row['left_exon_end']), int(row['right_exon_start']), gene_strand)
            if matched:
                matches.append({'gse': row['gse'], 'txname': row['txname'], 'symbol': row['symbol'],
                                'chrom': row['chrom'], 'strand': row['strand'],
                                'left_exonic_boundary': row['left_exon_end'], 'right_exonic_boundary': row['right_exon_start'],
                                'evidence': 'exact_junction_match_to_independent_primary_paper', 'doi': DOI,
                                'full_transcript_identity': 'not_established', 'polyA_site': 'not_established'})
        a.tsv(OUT / 'event_matches.tsv', matches, ['gse','txname','symbol','chrom','strand','left_exonic_boundary','right_exonic_boundary','evidence','doi','full_transcript_identity','polyA_site'])
        for gse, label in a.SERIES.items():
            s = a.soft((a.DATA / f'{gse}.soft').read_text(), '!Series_')
            paths = {}
            for measure in ['counts', 'uniqueCounts', 'fullLengthCounts', 'CPM']:
                name = f'{gse}_{label}_isoseq_{measure}_transcript.txt.gz'
                path = a.DATA / name
                if measure in ['counts', 'uniqueCounts']:
                    if a.sha256(path.read_bytes()) != old_manifest[name]['source_sha256']:
                        raise ValueError(f'Input hash mismatch: {name}')
                else:
                    url = next(u.replace('ftp://','https://') for u in s['!Series_supplementary_file'] if u.endswith('/'+name))
                    a.fetch(url, path, manifest)
                paths[measure] = path
            sums, frac, gcd, mismatch_full_unique = {}, {}, {}, None
            order = ['counts', 'uniqueCounts', 'fullLengthCounts', 'CPM']
            n = 0
            for bundle in itertools.zip_longest(*(a.count_rows(paths[x]) for x in order)):
                if any(r is None for r in bundle) or any(r[:3] != bundle[0][:3] for r in bundle[1:]):
                    raise ValueError('Matrix IDs or columns are not identical')
                header, tx, gene, vals = bundle[0]
                if not sums:
                    sums = {x:[0.] * len(vals) for x in order}
                    frac = {x:[0] * len(vals) for x in order}
                    gcd = {x:[0] * len(vals) for x in order if x != 'CPM'}
                    mismatch_full_unique = [0] * len(vals)
                for measure, record in zip(order, bundle):
                    for i, v in enumerate(record[3]):
                        sums[measure][i] += v
                        frac[measure][i] += not v.is_integer()
                        if measure != 'CPM' and v.is_integer():
                            gcd[measure][i] = math.gcd(gcd[measure][i], int(v))
                for i, (ct, uq, fl, cpm) in enumerate(zip(*(r[3] for r in bundle))):
                    mismatch_full_unique[i] += abs(fl-uq) > TOLERANCE
                    for problem in quant_violations(uq, fl, ct):
                        problems.append({'gse':gse,'txname':tx,'column':header[i+2], 'problem':problem,'unique':uq,'full_length':fl,'total':ct})
                    if gene.split('.')[0] in a.TARGETS.values():
                        target_support.append({'gse':gse,'txname':tx,'geneid':gene,'column':header[i+2],
                            'counts':ct,'uniqueCounts':uq,'fullLengthCounts':fl,'deposited_CPM':cpm,
                            'full_to_total':fl/ct if ct else 'NA', 'unique_to_total':uq/ct if ct else 'NA'})
                n += 1
            for i, col in enumerate(header[2:]):
                total, cpm_sum = sums['counts'][i], sums['CPM'][i]
                denominator = total * 1e6 / cpm_sum if cpm_sum else None
                depths.append({'gse':gse,'column':col,'rows':n,'sum_counts':total,'sum_uniqueCounts':sums['uniqueCounts'][i],
                    'sum_fullLengthCounts':sums['fullLengthCounts'][i],'sum_deposited_CPM':cpm_sum,
                    'CPM_denominator_implied_by_sums':denominator,
                    'denominator_minus_assigned_counts':denominator-total if denominator else '',
                    'fractional_unique_cells':frac['uniqueCounts'][i], 'fractional_full_length_cells':frac['fullLengthCounts'][i],
                    'unique_integer_gcd':gcd['uniqueCounts'][i] if not frac['uniqueCounts'][i] else '',
                    'full_length_integer_gcd':gcd['fullLengthCounts'][i] if not frac['fullLengthCounts'][i] else '',
                    'cells_full_length_different_from_unique':mismatch_full_unique[i]})
        a.tsv(OUT / 'depth_and_cpm.tsv', depths, list(depths[0]))
        a.tsv(OUT / 'target_full_length_support.tsv', target_support, list(target_support[0]))
        cpm_contrasts = []
        cultures = {}
        for r in target_support:
            if r['gse'] == 'GSE310723':
                cultures.setdefault(r['txname'], {})[r['column']] = r
        for tx, samples in cultures.items():
            for arm in ['5Aza', 'noAza']:
                control = samples[f'i3N_Ctrl_{arm}_hg38_minimap2']['deposited_CPM']
                kd = samples[f'i3N_TDP43KD_{arm}_hg38_minimap2']['deposited_CPM']
                cpm_contrasts.append({'gse':'GSE310723','txname':tx,'arm':arm,'control_deposited_CPM':control,
                    'kd_deposited_CPM':kd,'kd_control_ratio':kd/control if control else '',
                    'direction':'higher' if kd>control else 'lower' if kd<control else 'equal'})
        a.tsv(OUT / 'deposited_cpm_contrasts.tsv', cpm_contrasts, list(cpm_contrasts[0]))
        a.tsv(OUT / 'quant_violations.tsv', problems, ['gse','txname','column','problem','unique','full_length','total'])
        a.dump_json(OUT / 'summary.json', {'event_matches':len(matches),'libraries':len(depths),'quant_violations':len(problems),
            'bambu_version':'3.2.6','bambu_commit':index['commit'],'gene_strand_from_gencode':gene_strand,
            'unique_count_scale_cause':'unresolved','full_transcript_or_polyA_validated':False,
            'algebraic_scalar_witness':{'observed_count':1,'unique_output_of_scalar_expression':one_isoform_unique_witness([1]),
                'scope':'algebra only; package R/C++ NOT executed; does not trace deposited pipeline'}})
        print(f'Event matches={len(matches)}; libraries={len(depths)}; quantification violations={len(problems)}')
    except Exception as exc:
        errors.append({'type':type(exc).__name__,'message':str(exc)})
    finally:
        a.dump_json(mpath,manifest)
        a.dump_json(OUT/'errors.json',errors)
        a.dump_json(OUT/'run.json',{'utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'argv':sys.argv,
            'tolerance':TOLERANCE,'randomness':'none','original_bambu_runtime_executed':False,
            'status':'failed' if errors else 'generated_with_quant_violations' if problems else 'generated'})
    if errors:
        print(errors,file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
