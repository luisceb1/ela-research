"""Read allowlisted code/aggregate members only; never execute received scripts."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import zipfile

EXPRESSION_MAP = {
    'media_delta_log2_CPM_TN_menos_TP': 'mean_delta_log2_CPM',
    'razon_geometrica_TN_TP_CPM': 'CPM_geometric_ratio', 'cambio_porcentual_CPM': 'CPM_change_percent',
    'IC95_t_delta_log2_CPM_limite_inferior': 'CPM_CI_t_low', 'IC95_t_delta_log2_CPM_limite_superior': 'CPM_CI_t_high',
    'n_pares': 'pairs', 'pares_con_aumento_CPM': 'CPM_increasing_pairs', 'pares_con_descenso_CPM': 'CPM_decreasing_pairs',
    'p_exacta_inversion_signos_bilateral_CPM': 'CPM_exploratory_signflip_p',
    'media_delta_log2_median_ratio': 'mean_delta_log2_median_ratio',
    'razon_geometrica_median_ratio': 'median_ratio_geometric_ratio', 'cambio_porcentual_median_ratio': 'median_ratio_change_percent',
    'pares_con_aumento_median_ratio': 'median_ratio_increasing_pairs', 'pares_con_descenso_median_ratio': 'median_ratio_decreasing_pairs',
    'p_exacta_inversion_signos_median_ratio': 'median_ratio_exploratory_signflip_p'}


def unique_package(root, fragment):
    ps = list(root.glob('*' + fragment + '*.zip'))
    if len(ps) != 1:
        raise ValueError('Missing or ambiguous package: ' + fragment)
    return ps[0]


def member(z, suffix):
    names = [n for n in z.namelist() if n.endswith(suffix)]
    if len(names) != 1 or z.getinfo(names[0]).file_size > 2_000_000:
        raise ValueError('Ambiguous or oversized allowlisted member')
    return names[0], z.read(names[0])


def main(upload, report):
    provenance, comparisons = [], []
    received = Path('research/received_code/issue14');received.mkdir(parents=True, exist_ok=True)
    specs = [('reanalisis_real', 'ELA_analisis_v1.py'), ('reanalisis_02_splicing', 'analizar_splicing_y_expresion.py'),
             ('CIERRE_SPLICING', 'analizar_dexseq_ela.py')]
    for fragment, code in specs:
        p = unique_package(upload, fragment)
        with zipfile.ZipFile(p) as z:
            n, raw = member(z, code)
            (received / code).write_bytes(raw)
            rec = {'package': p.name, 'package_sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                   'code_member': n, 'code_sha256': hashlib.sha256(raw).hexdigest(),
                   'code_executed': False, 'attribution': 'User-provided prior project analysis; no separate license inferred'}
            if fragment == 'reanalisis_real':
                _, packed_counts = member(z, 'GSE126542_NeuronalNuclei_RNAseq_counts.txt.gz')
                rec['packed_counts_sha256'] = hashlib.sha256(packed_counts).hexdigest()
                if rec['packed_counts_sha256'] != 'c7a9ddae801f160e5ee6f02d4a6f127bde351a1ca85adaaba07228d4c24da0f8':
                    raise ValueError('Received counts differ from verified public input')
                n, expected_raw = member(z, 'resultados_resumen.csv')
                rec['aggregate_member'] = n;rec['aggregate_sha256'] = hashlib.sha256(expected_raw).hexdigest()
                expected = list(csv.DictReader(io.StringIO(expected_raw.decode())))
                with (report / 'expression_aggregate.tsv').open() as f:
                    observed = {r['gene']: r for r in csv.DictReader(f, delimiter='\t')}
                for r in expected:
                    for old, new in EXPRESSION_MAP.items():
                        x, y = float(r[old]), float(observed[r['gen']][new])
                        comparisons.append({'block': 'expression', 'gene': r['gen'], 'field': old,
                            'expected': x, 'observed': y, 'agrees': math.isclose(x, y, rel_tol=1e-8, abs_tol=1e-8)})
            if fragment == 'CIERRE_SPLICING':
                n, raw_audit = member(z, 'auditoria.json');rec['aggregate_member'] = n
                rec['aggregate_sha256'] = hashlib.sha256(raw_audit).hexdigest();old = json.loads(raw_audit)
                with (report / 'dexseq_aggregate.tsv').open() as f:
                    observed = {r['gene']: r for r in csv.DictReader(f, delimiter='\t')}
                mapping = {'fragments': 'fragments', 'padj_evaluable': 'provided_padj_evaluable', 'padj_NA': 'provided_padj_missing',
                           'fdr_0_05': 'provided_padj_below_0_05', 'fdr_0_10': 'provided_padj_below_0_10', 'min_padj': 'min_provided_padj'}
                for r in old['genes']:
                    for old_key, new_key in mapping.items():
                        x, y = float(r[old_key]), float(observed[r['gen']][new_key])
                        comparisons.append({'block': 'dexseq_extraction', 'gene': r['gen'], 'field': old_key,
                            'expected': x, 'observed': y, 'agrees': math.isclose(x, y, rel_tol=1e-12, abs_tol=1e-14)})
                qc = json.loads((report / 'qc.json').read_text())['dexseq']
                if (qc['rows'], qc['columns'], qc['target_fragments']) != (old['n_rows'], old['n_columns'], old['n_target_fragments']):
                    raise ValueError('DEXSeq dimensions differ')
            provenance.append(rec)
    (report / 'package_provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    with (report / 'comparison.tsv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(comparisons[0]), delimiter='\t', lineterminator='\n');w.writeheader();w.writerows(comparisons)
    result = {'numeric_fields_compared': len(comparisons), 'mismatches': sum(not r['agrees'] for r in comparisons),
              'received_code_executed': False, 'individual_output_members_read': False,
              'scope': 'Only received code, packaged count-file digest and aggregate expected results read; no case/clinical/genetic tables'}
    (report / 'comparison.json').write_text(json.dumps(result, indent=2) + '\n')
    if result['mismatches']:
        raise SystemExit('Aggregate reproduction mismatch')


if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('--upload', type=Path, required=True)
    p.add_argument('--report', type=Path, default=Path('reports/issue14-reproduction'))
    args = p.parse_args();main(args.upload, args.report)
