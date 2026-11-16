"""Read-only local capacity snapshot; no preparation, download or execution."""
import json
import shutil
from pathlib import Path
import run_gse252892_local as old


def main():
    names = ['ela-gse252892-run-01', 'ela-gse252892-range-run-02',
             'ela-gse252892-retained-run-03', 'ela-gse252892-after-sampler-run-04',
             'ela-gse252892-drvfs-run-05', 'ela-gse252892-interrupt-run-06',
             'ela-gse252892-stmn2-control-01']
    home = Path.home()
    roots = []
    for name in names:
        p = home/name
        roots.append({'path': str(p), 'exists': p.exists(),
                      'sampled_bytes': old.root_bytes(p) if p.exists() else None})
    windows = old.physical_free()
    output = {'status': 'capacity_snapshot_only_execution_disabled',
              'physical_c_available_bytes': windows,
              'required_physical_c_reserve_bytes': 50*1024**3,
              'new_advertised_compressed_bytes': 27762593667,
              'retained_roots': roots,
              'retained_total_sampled_bytes': sum(x['sampled_bytes'] or 0 for x in roots),
              'linux_filesystem_available_bytes': shutil.disk_usage(home).free,
              'meminfo': Path('/proc/meminfo').read_text().splitlines()[:5],
              'sources_deleted': 0, 'network_bytes': 0,
              'limitations': 'Snapshot, not peak prediction or execution approval. Linux virtual capacity does not replace physical C: space.'}
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
