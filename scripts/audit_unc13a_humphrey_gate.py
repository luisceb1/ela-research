"""Project published event definitions without treating aggregates as samples."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'reports/unc13a-humphrey-processed-gate-20261101'

if __name__ == '__main__':
    path = ROOT / 'sources/compendium.csv'
    with path.open() as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames
        rows = list(reader)
    selected = [r for r in rows if r['gene_name'] == 'UNC13A' and r['comparison'] == 'Humphrey-i3Cortical']
    projected = [{k:r[k] for k in ['gene_name','paste_into_igv_junction','junc_cat','comparison','strand']} for r in selected]
    if projected:
        with (ROOT / 'event_definitions.tsv').open('w',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=list(projected[0]),delimiter='\t',lineterminator='\n')
            writer.writeheader();writer.writerows(projected)
    result={'source_commit':'80fa3d70418a4665a85d414e33c7c470a9312086','source_blob':'fa4bb9dfa5d9c6132524c7750c0304184a70552b','cached_projection_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'columns':columns,'humphrey_rows':sum(r['comparison']=='Humphrey-i3Cortical' for r in rows),'unc13a_humphrey_rows':len(selected),'per_library_identifiers_present':False,'read_support_counts_present':False,'matched_libraries':0,'accepted':False,'gate':'blocked: aggregate comparison table lacks per-library identity and junction support','psi_or_effects_computed':False,'coordinate_convention_validated':False}
    (ROOT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
