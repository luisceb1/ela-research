#!/usr/bin/env python3
"""Retrospective STMN2 summaries and exact technical-unit joins; no inference.

Inputs may contain mixed metadata. Only the technical columns enumerated below
are used. Output contains aggregate counts and hashes, never sample/donor rows.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import statistics

REGIONS = {
    "TALS_Cortex_Motor_Lateral": "Cortex_Motor_Lateral",
    "TALS_Spinal_Cord_Cervical": "Spinal_Cord_Cervical",
    "Cortex Motor Lateral": "Cortex_Motor_Lateral",
    "Spinal Cord Cervical": "Spinal_Cord_Cervical",
}


def read_table(path, delimiter):
    data = Path(path).read_bytes()
    decoded = gzip.decompress(data) if data.startswith(b"\x1f\x8b") else data
    return list(csv.DictReader(io.StringIO(decoded.decode("utf-8-sig")), delimiter=delimiter))


def canonical_region(value):
    value = (value or "").strip()
    return REGIONS.get(value, value)


def build_index(rows, key_fields, donor_field, tissue_field, extras=()):
    """Preserve exact keys, including suffixes. Quarantine conflicting records."""
    buckets = defaultdict(set)
    for row in rows:
        donor = (row.get(donor_field) or "").strip()
        region = canonical_region(row.get(tissue_field))
        extra = tuple((row.get(field) or "").strip() for field in extras)
        for key_field in key_fields:
            key = (row.get(key_field) or "").strip()
            if key:
                buckets[key].add((donor, region, extra))
    lookup, ambiguous = {}, set()
    for key, values in buckets.items():
        if len(values) != 1:
            ambiguous.add(key)
        else:
            lookup[key] = next(iter(values))
    return lookup, ambiguous


def project_lookup(rows, expected_region):
    grouped = defaultdict(set)
    for row in rows:
        rail, external = (row.get("rail_id") or "").strip(), (row.get("external_id") or "").strip()
        region = canonical_region(row.get("project"))
        if rail and region == expected_region:
            grouped[rail].add((external, region))
    return {k: next(iter(v)) for k,v in grouped.items() if len(v)==1}, {k for k,v in grouped.items() if len(v)!=1}


def join_samples(samples, project_rows, index, ambiguous, expected_region, expected_project=None):
    rails = [str(s["rail_id"]) for s in samples]
    if len(rails) != len(set(rails)):
        raise ValueError("duplicate rail_id in a region")
    projects, conflicting_rails = project_lookup(project_rows, expected_region)
    joined, failures = {}, Counter()
    for sample in samples:
        rail = str(sample["rail_id"])
        if rail in conflicting_rails:
            failures["conflicting_project_rail"] += 1
            continue
        if rail not in projects:
            failures["missing_project_rail"] += 1
            continue
        key, project_region = projects[rail]
        if project_region != expected_region:
            failures["project_region_mismatch"] += 1
            continue
        if key in ambiguous:
            failures["ambiguous_external_key"] += 1
            continue
        if key not in index:
            failures["unmatched_external_key"] += 1
            continue
        donor, region, extra = index[key]
        if expected_project is not None and (not extra or extra[0] != expected_project):
            failures["metadata_project_mismatch"] += 1
            continue
        if not donor:
            failures["missing_donor"] += 1
            continue
        if region != expected_region:
            failures["metadata_region_mismatch"] += 1
            continue
        joined[rail] = {"donor": donor, "external": key, "region": region, "extra": extra}
    return joined, failures


def mapping_summary(samples, joined, failures):
    donors = [v["donor"] for v in joined.values()]
    multiplicity = Counter(donors)
    above = [s for s in samples if s["counts"]["cryptic"] >= 20]
    mapped_above = [joined[str(s["rail_id"])]["donor"] for s in above if str(s["rail_id"]) in joined]
    per_group = {}
    for group in sorted({s["group"] for s in samples}):
        subset = [s for s in samples if s["group"] == group]
        ds = [joined[str(s["rail_id"])]["donor"] for s in subset if str(s["rail_id"]) in joined]
        per_group[group] = {"samples": len(subset), "matched_samples":len(ds), "distinct_declared_donors":len(set(ds))}
    return {"samples":len(samples), "matched_samples":len(joined),
            "distinct_declared_donors":len(set(donors)),
            "donors_with_multiple_samples_in_this_region":sum(n>1 for n in multiplicity.values()),
            "max_samples_per_donor":max(multiplicity.values(), default=0),
            "failures":dict(failures), "by_group":per_group,
            "samples_with_cryptic_ge20":len(above), "matched_samples_with_cryptic_ge20":len(mapped_above),
            "distinct_declared_donors_with_cryptic_ge20":len(set(mapped_above))}


def descriptives(samples, denominator_min=20):
    result = {}
    for group in sorted({s["group"] for s in samples}):
        ss = [s for s in samples if s["group"]==group]
        qualified = [s for s in ss if sum(s["counts"].values()) >= denominator_min]
        def stats(records):
            values = [s["counts"]["cryptic"]/sum(s["counts"].values()) for s in records if sum(s["counts"].values())>0]
            return {"n":len(values), "median":statistics.median(values) if values else None,
                    "max":max(values) if values else None}
        result[group] = {"samples":len(ss), "nonzero_denominator":stats(ss),
                         "denominator_ge20":stats(qualified),
                         "observed_cryptic_ge20":sum(s["counts"]["cryptic"]>=20 for s in ss)}
    return result


def mapped_chain_positions(path, chrom, positions):
    """Map zero-based bases through UCSC chain alignment blocks, no interpolation."""
    result = {p:[] for p in positions}
    with gzip.open(path,"rt") as handle:
        active=False
        for line in handle:
            parts=line.split()
            if not parts:
                active=False
                continue
            if parts[0]=="chain":
                active=parts[2]==chrom and parts[4]=="+"
                if active:
                    tpos,qpos=int(parts[5]),int(parts[10]);qchrom,qsize,qstrand=parts[7],int(parts[8]),parts[9]
                continue
            if not active:continue
            size=int(parts[0])
            for p in positions:
                if tpos<=p<tpos+size:
                    q=qpos+p-tpos
                    if qstrand=="-":q=qsize-q-1
                    result[p].append({"chromosome":qchrom,"position0":q,"strand":qstrand})
            tpos+=size;qpos+=size
            if len(parts)==3:tpos+=int(parts[1]);qpos+=int(parts[2])
    return result


def coverage_recheck(stmn2_samples, unc13a_samples, qc_rows):
    """Compare medians after normalizing EACH library; fail on missing/zero QC."""
    qc = {str(r['rail_id']): r for r in qc_rows}
    groups = [[s for s in samples if s['group'] == 'ALS Spectrum MND']
              for samples in (stmn2_samples, unc13a_samples)]
    if {str(s['rail_id']) for s in groups[0]} != {str(s['rail_id']) for s in groups[1]}:
        raise ValueError('gene panels differ in pure-ALS library keys')
    result = {}
    for field in ['star.number_of_input_reads_both', 'star.uniquely_mapped_reads_number_both', 'exon_fc_count_all.assigned']:
        medians = []
        for samples in groups:
            values = []
            for sample in samples:
                denominator = float(qc[str(sample['rail_id'])][field])
                if denominator <= 0:
                    raise ValueError('nonpositive QC denominator')
                values.append(sample['counts']['canonical'] * 1e6 / denominator)
            medians.append(statistics.median(values))
        ratio = medians[0] / medians[1] if medians[1] else None
        result[field] = {'n_each_gene':len(groups[0]), 'STMN2_median_per_million':medians[0],
                         'UNC13A_median_per_million':medians[1], 'ratio_of_medians':ratio,
                         'P1_ge10_met':ratio is not None and ratio >= 10}
    return {'method':'per-library normalization followed by group medians; retrospective check of P1',
            'primary_denominator':'star.number_of_input_reads_both (matches prior UNC13A ~0.11/million)',
            'sensitivity_denominators':'unique mapped reads; assigned exonic reads', 'results':result}


def run(source_root, cortex_path, cervical_path, unc13a_path=None):
    root=Path(source_root)
    cortex=json.loads(Path(cortex_path).read_text())["samples"]
    cervical=json.loads(Path(cervical_path).read_text())["samples"]
    projects=read_table(root/"project_global.source","\t")
    author_rows=read_table(root/"author_map.source",",")
    geo_rows=read_table(root/"jung_table.source","\t")
    sources={
        "fratta_primary_metadata":build_index(author_rows,("sample_id_rna","sample"),"external_subject_id","rna_tissue_source",("project",)),
        "jung_GEO_curation":build_index(geo_rows,("sample_id_alt",),"subject_id","tissue",("project","libprep")),
    }
    results={};internals={}
    for tissue,samples,region in [("cortex",cortex,"Cortex_Motor_Lateral"),("cervical",cervical,"Spinal_Cord_Cervical")]:
        results[tissue]={"descriptive_recheck":descriptives(samples),"mapping":{}}
        internals[tissue]={}
        for name,(index,ambiguous) in sources.items():
            joined,failures=join_samples(samples,projects,index,ambiguous,region,
                "Target ALS" if name=="fratta_primary_metadata" else "Target ALS PM core")
            results[tissue]["mapping"][name]=mapping_summary(samples,joined,failures)
            internals[tissue][name]=joined
        a,b=internals[tissue].values()
        common=set(a)&set(b)
        results[tissue]["cross_source_check"]={"samples_mapped_in_both":len(common),
            "identical_donor_keys":sum(a[k]["donor"]==b[k]["donor"] for k in common),
            "different_donor_keys":sum(a[k]["donor"]!=b[k]["donor"] for k in common)}
    coverage = None
    if unc13a_path is not None:
        unc = json.loads(Path(unc13a_path).read_text())["samples"]
        coverage = coverage_recheck(cervical, unc, read_table(root/"qc_cervical.source", "\t"))
    overlap={}
    for name in sources:
        a={v["donor"] for v in internals["cortex"][name].values()};b={v["donor"] for v in internals["cervical"][name].values()}
        overlap[name]={"declared_donors_in_both_regions":len(a&b),"donors_in_either_region":len(a|b)}
    high_pure_als = [s for s in cervical if s['group']=='ALS Spectrum MND' and s['counts']['cryptic']>=20]
    source = internals['cervical']['fratta_primary_metadata']
    high_donors = [source[str(s['rail_id'])]['donor'] for s in high_pure_als if str(s['rail_id']) in source]
    high_summary = {'samples':len(high_pure_als), 'matched_samples':len(high_donors),
                    'distinct_declared_donors':len(set(high_donors))}
    positions=[80523448,80523449,80529055,80529056,80529283,80529284,80549035,80549036]
    return {"evidence":"retrospective descriptive and technical design audit; no biological test",
            "identifier_policy":"aggregate output only; no sample or donor keys exported",
            "input_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/"project_global.source",root/"author_map.source",root/"jung_table.source",root/"chain.source",Path(cortex_path),Path(cervical_path)] + ([Path(unc13a_path),root/"qc_cervical.source"] if unc13a_path else [])},
            "tissues":results,"cross_tissue_overlap":overlap,
            "pure_ALS_cervical_cryptic_ge20_units":high_summary,"coverage_recheck":coverage,
            "stmn2_chain_mapped_bases":mapped_chain_positions(root/"chain.source","chr8",positions)}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-root",type=Path,required=True)
    p.add_argument("--cortex",type=Path,required=True)
    p.add_argument("--cervical",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--unc13a-cervical",type=Path)
    a=p.parse_args();out=run(a.source_root,a.cortex,a.cervical,a.unc13a_cervical)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    print(json.dumps({t:{k:v for k,v in r.items() if k!="descriptive_recheck"} for t,r in out["tissues"].items()},indent=2))


if __name__=="__main__":main()
