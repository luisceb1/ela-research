"""Reproduce published arithmetic means, without tests or biological inference."""
import argparse
import csv
from datetime import datetime
from decimal import Decimal, localcontext
import json
from pathlib import Path
import platform
import re
import sys
from zoneinfo import ZoneInfo

from audit_asadollahi_fig3s import audit_bytes, digest, GROUPS, MAX_BYTES as MAX_MEASUREMENTS
from audit_asadollahi_culture_map import inspect_table, MAX_BYTES as MAX_SUMMARY

MEAN_TOKEN = re.compile(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?\Z')


def published_mean(summary):
    parts = summary.split('±')
    if len(parts) != 2 or not parts[1].strip():
        raise ValueError('published_summary_format_ambiguous')
    token = parts[0].strip()
    if not MEAN_TOKEN.fullmatch(token):
        raise ValueError('published_mean_not_unambiguous_decimal')
    value = Decimal(token)
    tolerance = Decimal(1).scaleb(value.as_tuple().exponent) / 2
    return token, value, tolerance


def arithmetic_mean(values):
    if not values:
        raise ValueError('empty_group')
    if not all(v.is_finite() for v in values):
        raise ValueError('nonfinite_observation')
    with localcontext() as context:
        context.prec = 50
        return sum(values, Decimal(0)) / Decimal(len(values))


def check_mean(values, summary):
    with localcontext() as context:
        context.prec = 50
        token, expected, tolerance = published_mean(summary)
        computed = arithmetic_mean(values)
        discrepancy = abs(computed - expected)
        return {'n': len(values), 'computed_mean_pC': str(computed),
                'published_mean_pC': token, 'rounding_tolerance_pC': str(tolerance),
                'absolute_arithmetic_discrepancy_pC': str(discrepancy),
                'within_published_rounding': discrepancy <= tolerance}


def reproduce(measurements, summaries, counts):
    if set(summaries) != set(GROUPS.values()) or set(counts) != set(summaries):
        raise ValueError('unexpected_group_set')
    if len({r['source_cell'] for r in measurements}) != len(measurements):
        raise ValueError('duplicate_source_coordinate')
    if set(r['published_group'] for r in measurements) != set(summaries):
        raise ValueError('unexpected_observation_group')
    result = {}
    for group in GROUPS.values():
        records = [r for r in measurements if r['published_group'] == group]
        if len(records) != counts[group]:
            raise ValueError('published_count_mismatch')
        values = [Decimal(r['initial_epsc_charge_pC']) for r in records]
        result[group] = check_mean(values, summaries[group])
        result[group]['source_cells'] = [r['source_cell'] for r in records]
    return result


def render(records, groups, svg_path, png_path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'A25-fig3s-descriptive-v1'})
    fig, ax = plt.subplots(figsize=(6.4, 4.8), layout='constrained')
    colors = ['#0072B2', '#009E73']
    labels = []
    plotted_counts = {}
    for x, (group, color) in enumerate(zip(GROUPS.values(), colors)):
        values = [float(r['initial_epsc_charge_pC']) for r in records if r['published_group'] == group]
        # Horizontal offsets only improve legibility, never define cultures/pairs.
        positions = [x + (((i * 7) % 17) - 8) * 0.014 for i in range(len(values))]
        artist = ax.scatter(positions, values, s=27, color=color, alpha=.72, edgecolors='white', linewidths=.3)
        plotted_counts[group] = len(artist.get_offsets())
        mean = float(groups[group]['computed_mean_pC'])
        ax.hlines(mean, x - .18, x + .18, color='black', linewidth=2)
        ax.annotate(f'{mean:.3f} pC', (x + .23, mean), fontsize=9, va='center')
        name = 'UNC13A WT' if x == 0 else 'UNC13A R202H'
        labels.append(f'{name}\nn={len(values)} observations')
    ax.set(xticks=[0, 1], xticklabels=labels, xlim=(-.5, 1.65),
           ylabel='Initial EPSC charge (pC)', title='A25 Fig. 3s: descriptive reconstruction')
    ax.set_ylim(bottom=0)
    ax.spines[['top', 'right']].set_visible(False)
    ax.legend(handles=[Line2D([0], [0], color='black', lw=2, label='Unweighted arithmetic mean')],
              loc='upper left', frameon=False, fontsize=8)
    fig.supxlabel('Deposited values from mouse autaptic neurons. Culture IDs unavailable.\n'
                  'No SEM, confidence intervals or inferential tests. DOI:10.1038/s41588-025-02361-5',
                  fontsize=8)
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(svg_path, metadata={'Date': None})
    if png_path:
        png_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(png_path, dpi=160)
    plt.close(fig)
    return {'matplotlib': matplotlib.__version__, 'backend': 'Agg', 'figure_inches': [6.4, 4.8],
            'plotted_observation_counts': plotted_counts,
            'svg_sha256': digest(svg_path.read_bytes()), 'png_dpi': 160 if png_path else None,
            'png_sha256': digest(png_path.read_bytes()) if png_path else None,
            'horizontal_offset': '(((row_index*7)%17)-8)*0.014; cosmetic only', 'random_seed': None}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--measurements', type=Path, required=True)
    p.add_argument('--summary', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--plot', action='store_true')
    p.add_argument('--preview-png', type=Path)
    args = p.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    execution = {'started_at': datetime.now(ZoneInfo('Europe/Madrid')).isoformat(),
                 'python': sys.version, 'platform': platform.platform(),
                 'script_sha256': digest(Path(__file__).read_bytes()),
                 'parameters': {'decimal_precision': 50, 'tolerance': 'inclusive half last published decimal unit',
                                'no_exclusions': True, 'no_imputation': True, 'plot': args.plot}}
    try:
        if args.measurements.stat().st_size > MAX_MEASUREMENTS or args.summary.stat().st_size > MAX_SUMMARY:
            raise ValueError('source_size_limit_exceeded')
        audit, records = audit_bytes(args.measurements.read_bytes())
        if any(v['invalid_cells'] for v in audit['numeric_qc'].values()):
            raise ValueError('invalid_source_measurement')
        table = inspect_table(args.summary.read_bytes(), include_published_means=True)
        summaries = {'UNC13AWT': table['selected_fields']['C35'],
                     'UNC13AR202H': table['selected_fields']['E35']}
        groups = reproduce(records, summaries, table['published_observation_counts'])
        result = {'question': 'Do deposited Fig3s observations reproduce published arithmetic means?',
                  'source_measurements_sha256': audit['source_sha256'],
                  'source_summary_sha256': table['source_sha256'],
                  'measure': 'Initial EPSC Charge', 'unit': 'pC',
                  'published_mean_cells': {'UNC13AWT': 'C35', 'UNC13AR202H': 'E35'},
                  'groups': groups,
                  'arithmetic_concordance': all(v['within_published_rounding'] for v in groups.values()),
                  'total_source_observations': len(records), 'group_means_calculated': True,
                  'between_group_effect_estimated': False, 'p_values_computed': False,
                  'sem_or_confidence_intervals_computed': False, 'culture_map_verified': False,
                  'inferential_decision': 'NO_GO_CULTURE_MAP_MISSING',
                  'evidence_level': 'descriptive arithmetic reproduction of the same published experiment'}
        (args.output_dir / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        fields = ['published_group', 'n', 'computed_mean_pC', 'published_mean_pC',
                  'rounding_tolerance_pC', 'absolute_arithmetic_discrepancy_pC', 'within_published_rounding']
        with (args.output_dir / 'mean-concordance.csv').open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
            w.writeheader()
            for group, values in groups.items():
                w.writerow({'published_group': group, **{k: v for k, v in values.items() if k in fields}})
        if args.plot:
            execution['render'] = render(records, groups, args.output_dir / 'fig3s-descriptive.svg', args.preview_png)
        execution.update(status='completed', arithmetic_concordance=result['arithmetic_concordance'])
    except Exception as exc:
        execution.update(status='error', error_type=type(exc).__name__, error=str(exc))
    execution['finished_at'] = datetime.now(ZoneInfo('Europe/Madrid')).isoformat()
    (args.output_dir / 'execution.json').write_text(json.dumps(execution, indent=2) + '\n')
    print(json.dumps({k: execution[k] for k in ['status', 'arithmetic_concordance', 'error'] if k in execution}))
    return 0 if execution['status'] == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
