#!/usr/bin/env python3
"""QC + descriptive post-eligibility analysis for normalized MEA exports.

Requires explicit arm, pre-established T0 and eligibility from laboratory protocol.
Input is NOT raw Axion export. This tool does NOT determine or assert treatment efficacy.
"""
import argparse
from pathlib import Path
import json
import pandas as pd
from mea_pipeline import add_baseline_adjustment,well_level_endpoints,summary_by_scenario

REQUIRED={"differentiation_id","well_id","arm","time_index","synchrony","viability","qc_ok","status","t0_index"}
ALLOWED={"sham","early_reference","late_ASO","damage_control","screen_fail","unpaired_not_randomized"}
STATUSES={"observed","technical_missing","dead"}


def validate(df):
    if "scenario" not in df: df=df.assign(scenario="external")
    missing=REQUIRED.difference(df.columns)
    if missing:raise ValueError(f"Missing required columns: {sorted(missing)}")
    if df[["differentiation_id","well_id","arm","time_index"]].isna().any().any():raise ValueError("Empty key values")
    if df.duplicated(["scenario","well_id","time_index"]).any():raise ValueError("Duplicated well_id,time_index: electrodes and repeated readings must be summarized to WELL x time first")
    if (~df.arm.isin(ALLOWED)).any():raise ValueError(f"Invalid arm: {df.loc[~df.arm.isin(ALLOWED),'arm'].unique()}")
    if (~df.status.isin(STATUSES)).any():raise ValueError("Invalid status value")
    if (df.status.eq("observed") & df.synchrony.isna()).any():raise ValueError("Observed rows have missing synchrony")
    if (df.status.ne("observed") & df.synchrony.notna()).any():raise ValueError("Non-observed rows must leave synchrony blank")
    if (df.status.eq("dead") & df.viability.ne(0)).any():raise ValueError("Dead rows must have viability 0")
    if (df.status.eq("observed") & df.qc_ok.ne(1)).any():raise ValueError("Observed rows must have qc_ok=1")
    if ((df.synchrony.dropna()<0) | (df.synchrony.dropna()>1)).any():raise ValueError("This prototype expects a normalized synchrony in [0,1], not raw arbitrary-scale MEA exports")
    bad=df.groupby(["scenario","well_id"]).agg(n_arm=("arm","nunique"),n_t0=("t0_index","nunique"),n_diff=("differentiation_id","nunique"))
    if (bad>1).any().any():raise ValueError("Well-level arm, T0 or differentiation changes across readings")
    r=df[df.arm.isin(["late_ASO","damage_control"])]
    if r.empty:raise ValueError("No randomized late-treatment wells")
    if r.t0_index.isna().any():raise ValueError("Each randomized well requires its prospectively recorded T0")
    if (r.groupby(["scenario","well_id"]).time_index.nunique()<5).any():raise ValueError("Some randomized wells have fewer than five timepoints")
    for (sc,did,arm),g in r.groupby(["scenario","differentiation_id","arm"]):
        if (df[(df.scenario==sc)&(df.differentiation_id==did)&df.arm.eq("sham")]).empty:
            raise ValueError(f"Missing same-differentiation healthy sham controls in {did}")
    for (sc,wid),g in r.groupby(["scenario","well_id"]):
        t0=int(g.t0_index.iloc[0]);times=set(g.time_index)
        if not set([0,1,2,t0,t0+3,t0+4]).issubset(times):
            raise ValueError(f"Missing baseline/T0/required follow-up readings for {wid}")
        if g.loc[g.time_index==t0,"status"].iloc[0]!="observed":
            raise ValueError(f"T0 must be an observed QC passing reading in {wid}")
    return {"n_wells":int(df.groupby(["scenario","well_id"]).ngroups),"n_randomized_wells":int(r.groupby(["scenario","well_id"]).ngroups),"n_differentiations":int(r.groupby(["scenario","differentiation_id"]).ngroups),"n_observation_rows":int(len(df))}


def main():
    p=argparse.ArgumentParser(description="Analyze standardized MEA data (not raw Axion exports)")
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--provenance",required=True,help="Origin of real dataset, or explicitly 'synthetic'")
    args=p.parse_args()
    df=pd.read_csv(args.input)
    if "scenario" not in df:df["scenario"]="external"
    info=validate(df)
    out=args.output;out.mkdir(parents=True,exist_ok=True)
    adjusted=add_baseline_adjustment(df)
    endpoints=well_level_endpoints(adjusted)
    summary=summary_by_scenario(endpoints)
    endpoints.to_csv(out/"desenlaces_por_pozo.csv",index=False)
    summary.to_csv(out/"resumen_descriptivo.csv",index=False)
    (out/"control_calidad.json").write_text(json.dumps({"provenance_user_reported":args.provenance,**info,"warning":"Análisis exploratorio sujeto a protocolo previamente registrado y validación científica. No demuestra causalidad ni eficacia clínica."},ensure_ascii=False,indent=2),encoding="utf-8")
    print("Validación de estructura: correcta. Resumen exploratorio:")
    print(summary.to_string(index=False))

if __name__=="__main__":main()
