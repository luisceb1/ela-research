#!/usr/bin/env python3
"""Exploratory longitudinal MEA analysis for UNC13A post-deficit intervention.

Purely synthetic demonstrations; not empirical ALS data and not a power calculation.
Columns used in standardized real data:
 scenario, differentiation_id, well_id, arm, time_index, synchrony, viability, qc_ok,
 t0_index (for randomized affected wells). Missing readings use NaN; death uses status='dead'.

Python >=3.10 | numpy, pandas, matplotlib; scipy optional (not used).
"""
from __future__ import annotations
import argparse
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TIME_MAX=12
BASELINE=(0,1,2)
DAMAGE_START=3
THRESHOLD=0.19                 # synthetic placeholder, not a calibrated biological threshold
ELIGIBILITY_QC_MIN=0.60        # synthetic placeholder for cell viability
FOLLOW_PRIMARY=3
FOLLOW_CONFIRM=4
MIN_MEANINGFUL=0.06             # hypothetical SYNCHRONY scale, not literature-derived
SCENARIOS=("recovery", "protection_only", "null_effect")
RNG_SEED=20261029


def simulate_pre(scenario: str, seed:int=RNG_SEED, n_diffs:int=8, n_candidate:int=12):
    """Generate basal/untreated history, plus healthy and early-prevention references.

    No potential outcomes depending on future late allocation are generated before eligibility.
    """
    rng=np.random.default_rng(seed)
    rows=[]
    assert n_candidate % 2 == 0
    for d in range(n_diffs):
        did=f"D{d+1:02d}"
        batch=rng.normal(0,0.026)
        batch_maturation=rng.normal(0.008,0.003)
        for group,n in [("sham",3),("early_reference",2),("candidate",n_candidate)]:
            for w in range(n):
                wid=f"{did}_{group}_{w+1:02d}"
                base=np.clip(0.70+batch+rng.normal(0,0.038),0.54,0.86)
                susceptibility=max(0.65, rng.normal(1,0.12))
                for t in range(TIME_MAX+1 if group!="candidate" else 7):
                    matur=batch_maturation*t
                    e=0 if t<DAMAGE_START else min(0.38, 0.09+0.106*(t-DAMAGE_START))
                    damage=e*susceptibility
                    if group=="sham": damage=0
                    if group=="early_reference": damage*=0.20
                    obs=float(np.clip(base+matur-damage+rng.normal(0,0.017),0.0,1.0))
                    # Observation-level QC. No pre-screening dropout in this toy generator.
                    rows.append(dict(scenario=scenario,differentiation_id=did,well_id=wid,
                                     arm=group,time_index=t,synchrony=obs,viability=0.94,
                                     qc_ok=1,status="observed",t0_index=np.nan))
    return pd.DataFrame(rows),rng


def sham_expectations(df:pd.DataFrame):
    """Age/differentiation-matched sham trajectory, centered at sham baseline."""
    sham=df[(df.arm=="sham") & (df.qc_ok==1)].copy()
    ref=sham.groupby(["scenario","differentiation_id","time_index"]).synchrony.mean()
    baseline=sham[sham.time_index.isin(BASELINE)].groupby(["scenario","differentiation_id"]).synchrony.mean()
    return ref, baseline


def detect_eligibility(pre:pd.DataFrame, threshold:float=THRESHOLD):
    """Screen by two consecutive deficits with healthy age matched comparison.

    For candidate well i, expected synchrony at t = personal baseline + (matched-sham(t) -
    matched-sham(baseline)). A deficit is expected - observed.
    Event-specific t0 is the second qualifying observation. This screening method and threshold
    would need to be frozen using a separate pilot before any actual outcome comparison.
    """
    ref,sham_baseline=sham_expectations(pre)
    candidates=pre.loc[pre.arm=="candidate"].copy()
    base=candidates[candidates.time_index.isin(BASELINE)].groupby(["scenario","differentiation_id","well_id"]).synchrony.mean()
    cand=candidates.sort_values(["differentiation_id","well_id","time_index"])
    decisions=[]
    for (sc,did,wid),g in cand.groupby(["scenario","differentiation_id","well_id"]):
        b=float(base.loc[sc,did,wid]); r0=float(sham_baseline.loc[sc,did]); found=None
        g=g.sort_values("time_index").copy()
        g["expected"]=[b+float(ref.loc[sc,did,int(t)])-r0 for t in g.time_index]
        g["deficit"]=g.expected-g.synchrony
        for t in range(DAMAGE_START+2,7):
            pair=g[g.time_index.isin([t-1,t])]
            if len(pair)==2 and pair.qc_ok.eq(1).all() and pair.viability.ge(ELIGIBILITY_QC_MIN).all() and pair.deficit.ge(threshold).all():
                found=t;break
        if found is not None:
            severity=float(g.loc[g.time_index==found,"deficit"].iloc[0])
            decisions.append(dict(scenario=sc,differentiation_id=did,well_id=wid,t0_index=found,
                                  deficit_t0=severity,baseline_synchrony=b,eligible=1))
        else:
            decisions.append(dict(scenario=sc,differentiation_id=did,well_id=wid,t0_index=np.nan,
                                  deficit_t0=np.nan,baseline_synchrony=b,eligible=0))
    return pd.DataFrame(decisions)


def randomize_by_block(decisions:pd.DataFrame,rng):
    """Randomize only eligible wells, balancing measured deficit within differentiation.

    Consecutive severity-ranked pairs within each T0 and differentiation stratum receive one late treatment and one control. Unpaired
    cultures are explicitly not used in the randomized comparison.
    """
    dec=decisions.copy()
    dec["arm"]="screen_fail"
    for (_,did,_t0),g in dec[dec.eligible==1].groupby(["scenario","differentiation_id","t0_index"]):
        sorted_idx=g.sort_values("deficit_t0").index.to_numpy()
        for k in range(0,len(sorted_idx)-1,2):
            pair=sorted_idx[k:k+2].copy()
            rng.shuffle(pair)
            dec.loc[pair[0],"arm"]="late_ASO"
            dec.loc[pair[1],"arm"]="damage_control"
        if len(sorted_idx)%2:dec.loc[sorted_idx[-1],"arm"]="unpaired_not_randomized"
    return dec


def complete_simulation(pre:pd.DataFrame,randomization:pd.DataFrame,rng,scenario:str):
    """Simulate post-randomization outcomes and explicit missingness/death."""
    assignments=randomization.set_index("well_id")[["arm","t0_index"]]
    c=pre[pre.arm=="candidate"].copy()
    c["arm"]=c.well_id.map(assignments.arm)
    c["t0_index"]=c.well_id.map(assignments.t0_index)
    kept=[];new=[]
    for wid,g in c.groupby("well_id"):
        arm=g.arm.iloc[0]; ti=g.t0_index.iloc[0]
        if pd.isna(ti):
            kept.append(g)  # unevaluable historical samples retained for audit, excluded from inference
            continue
        t0=int(ti)
        kept.append(g[g.time_index<=t0].copy())
        pre_y=float(g.loc[g.time_index==t0,"synchrony"].iloc[0])
        diff=g.differentiation_id.iloc[0]
        dead=False
        for t in range(t0+1,TIME_MAX+1):
            elapsed=t-t0
            # Recovery is positive w.r.t. pre-treatment; protection slows decline but does not reverse.
            if arm=="damage_control": intervention=-0.039*elapsed
            elif scenario=="recovery" and arm=="late_ASO":
                intervention={1:0.065,2:0.175,3:0.260}.get(elapsed,0.270+0.003*(elapsed-4))
            elif scenario=="protection_only" and arm=="late_ASO":intervention=-0.009*elapsed
            else:intervention=-0.039*elapsed
            maturation=0.007*elapsed
            viab=0 if dead else float(np.clip(0.93-0.023*elapsed+rng.normal(0,0.012),0,1))
            if not dead and rng.random()<0.014:
                dead=True;viab=0
            qc_bad=(not dead) and rng.random()<0.018
            status="dead" if dead else ("technical_missing" if qc_bad else "observed")
            y=(float(np.clip(pre_y+maturation+intervention+rng.normal(0,0.019),0,1)) if status=="observed" else np.nan)
            new.append(dict(scenario=scenario,differentiation_id=diff,well_id=wid,
                            arm=arm,time_index=t,synchrony=y,viability=viab,
                            qc_ok=int(status=="observed"),status=status,t0_index=t0))
    other=pre[pre.arm!="candidate"].copy()
    return pd.concat([other]+kept+[pd.DataFrame(new)],ignore_index=True).sort_values(["differentiation_id","well_id","time_index"]).reset_index(drop=True)


def add_baseline_adjustment(raw:pd.DataFrame):
    ref,sham_baseline=sham_expectations(raw)
    data=raw.copy()
    bases=(data.loc[(data.time_index.isin(BASELINE)) & data.qc_ok.eq(1)]
             .groupby(["scenario","differentiation_id","well_id"]).synchrony.mean())
    exp=[]
    for sc,did,wid,t in data[["scenario","differentiation_id","well_id","time_index"]].itertuples(index=False,name=None):
        exp.append(float(bases.loc[sc,did,wid]+ref.loc[sc,did,t]-sham_baseline.loc[sc,did]))
    data["age_expected"]=exp
    # Death contributes structural floor (0) to the composite; technical missing remains missing.
    data["composite_synchrony"]=np.where(data.status.eq("dead"),0,data.synchrony)
    data["adjusted_composite"]=data.composite_synchrony-data.age_expected
    data["adjusted_observed"]=data.synchrony-data.age_expected
    data["relative_to_t0"]=data.time_index-data.t0_index
    return data


def well_level_endpoints(data:pd.DataFrame):
    randomized=data[data.arm.isin(["late_ASO","damage_control"])].copy()
    results=[]
    for (sc,did,wid,arm),g in randomized.groupby(["scenario","differentiation_id","well_id","arm"]):
        t0=int(g.t0_index.iloc[0]); anchor=g[g.time_index==t0]
        if len(anchor)!=1:raise ValueError(f"Missing T0 for {wid}")
        pre=float(anchor.adjusted_observed.iloc[0]);row={"scenario":sc,"differentiation_id":did,"well_id":wid,"arm":arm,"t0_index":t0,"adjusted_t0":pre}
        for follow in [FOLLOW_PRIMARY,FOLLOW_CONFIRM]:
            f=g[g.time_index==t0+follow]
            if len(f)!=1:raise ValueError(f"Missing follow-up {follow} for {wid}")
            z=f.iloc[0]
            row[f"status_f{follow}"]=z.status
            row[f"change_f{follow}"]=(float(z.adjusted_composite-pre) if pd.notna(z.adjusted_composite) else np.nan)
            row[f"recovery_f{follow}"]=(pd.notna(row[f"change_f{follow}"]) and row[f"change_f{follow}"]>0)
            row[f"observed_f{follow}"]=z.status=="observed"
            row[f"death_f{follow}"]=z.status=="dead"
        results.append(row)
    return pd.DataFrame(results)


def summary_by_scenario(endpoints:pd.DataFrame,seed:int=42,B:int=1500):
    rng=np.random.default_rng(seed)
    rows=[]
    for sc,g in endpoints.groupby("scenario"):
        block=[]
        for did,h in g.groupby("differentiation_id"):
            aa=h[h.arm=="late_ASO"];bb=h[h.arm=="damage_control"]
            if len(aa)==0 or len(bb)==0:continue
            row={"differentiation_id":did}
            for f in [3,4]:
                c=f"change_f{f}"
                row[f"ASO_f{f}"]=float(aa[c].mean())
                row[f"CTRL_f{f}"]=float(bb[c].mean())
                row[f"effect_f{f}"]=row[f"ASO_f{f}"]-row[f"CTRL_f{f}"]
            block.append(row)
        b=pd.DataFrame(block)
        if b.empty:raise ValueError("No randomized differentiation blocks")
        entry={"scenario":sc,"n_differentiations":len(b),"n_wells_late_ASO":int((g.arm=="late_ASO").sum()),"n_wells_control":int((g.arm=="damage_control").sum()),
               "n_deaths_f3":int(g.death_f3.sum()),"n_technical_missing_f3":int((g.status_f3=="technical_missing").sum())}
        for f in [3,4]:
            eff=b[f"effect_f{f}"].to_numpy()
            draws=rng.choice(eff,size=(B,len(eff)),replace=True).mean(axis=1)
            entry.update({f"mean_ASO_change_f{f}":float(b[f"ASO_f{f}"].mean()),
                          f"mean_CTRL_change_f{f}":float(b[f"CTRL_f{f}"].mean()),
                          f"mean_arm_difference_f{f}":float(eff.mean()),
                          f"bootstrap95_lower_f{f}":float(np.quantile(draws,.025)),
                          f"bootstrap95_upper_f{f}":float(np.quantile(draws,.975))})
        # Purely demonstrative classification. The two dimensions must be kept separate.
        pos=entry["mean_ASO_change_f3"]>MIN_MEANINGFUL and entry["mean_ASO_change_f4"]>MIN_MEANINGFUL
        better=entry["mean_arm_difference_f3"]>MIN_MEANINGFUL and entry["mean_arm_difference_f4"]>MIN_MEANINGFUL
        if pos and better:label="recuperación funcional compatible (simulada)"
        elif better:label="beneficio relativo sin recuperación (simulado)"
        else:label="sin evidencia del beneficio exigido (simulado)"
        entry["classification"] = label
        rows.append(entry)
    return pd.DataFrame(rows)


def plot_trajectories(data:pd.DataFrame,out:Path,scenario:str):
    sc=data[data.scenario==scenario].copy()
    s=sc[sc.arm.isin(["late_ASO","damage_control"]) & sc.relative_to_t0.between(-3,4)]
    df=(s.groupby(["arm","relative_to_t0"]).adjusted_composite.agg(["mean","count"]).reset_index())
    fig,ax=plt.subplots(figsize=(8.0,4.6),dpi=160)
    colors={"late_ASO":"#178A76","damage_control":"#4D6076"}
    for arm,label in [("damage_control","Daño + ASO control"),("late_ASO","Daño + ASO corrector tardío")]:
        h=df[df.arm==arm]
        ax.plot(h.relative_to_t0,h["mean"],marker="o",linewidth=2,markersize=5,label=label,color=colors[arm])
    ax.axvline(0,linestyle="--",color="#9A6C21",linewidth=1.6)
    ax.text(0.13,ax.get_ylim()[1]-0.015,"T0 / tratamiento",fontsize=9,color="#9A6C21")
    ax.axhline(0,color="0.6",linewidth=.7,linestyle=":")
    ax.set(xlabel="Registros relativos a T0 (unidades de simulación)",ylabel="Sincronización menos referencia sana de la misma edad",title={"recovery":"ESCENARIO A: recuperación","protection_only":"ESCENARIO B: protección sin recuperación","null_effect":"ESCENARIO C: ausencia de efecto"}[scenario])
    ax.legend(fontsize=8,loc="lower right");ax.grid(alpha=.16);fig.tight_layout();fig.savefig(out,dpi=160);plt.close(fig)


def plot_effects(summary:pd.DataFrame,out:Path):
    ordered=["recovery","protection_only","null_effect"]
    df=summary.set_index("scenario").loc[ordered]
    fig,ax=plt.subplots(figsize=(8.6,4.2),dpi=160)
    x=np.arange(len(df)); width=.35
    ax.bar(x-width/2,df.mean_ASO_change_f3,width,label="Cambio del corrector frente a T0",color="#168C7B")
    ax.bar(x+width/2,df.mean_CTRL_change_f3,width,label="Cambio del control frente a T0",color="#6F7A87")
    ax.axhline(0,color="0.30",linewidth=.8)
    ax.set_xticks(x,["Recuperación","Solo protección","Efecto nulo"])
    ax.set_ylabel("Cambio medio ajustado en +3 (sintético)")
    ax.set_title("La diferencia frente al control NO equivale a reversión")
    ax.legend(fontsize=8);ax.grid(axis="y",alpha=.15)
    fig.tight_layout();fig.savefig(out,dpi=160);plt.close(fig)


def write_report(summary:pd.DataFrame,decisions:pd.DataFrame,directory:Path):
    table=summary[["scenario","n_differentiations","n_wells_late_ASO","n_wells_control","mean_ASO_change_f3","mean_CTRL_change_f3","mean_arm_difference_f3","mean_ASO_change_f4","mean_arm_difference_f4","n_deaths_f3","n_technical_missing_f3","classification"]].copy()
    for col in table.select_dtypes(include="number").columns:
        if col not in ("n_differentiations","n_wells_late_ASO","n_wells_control","n_deaths_f3","n_technical_missing_f3"):
            table[col]=table[col].round(3)
    txt="""# Resultados de simulación — ensayo MEA tardío UNC13A

**ATENCIÓN: DATOS COMPLETAMENTE SINTÉTICOS.** Ninguno de los números de esta carpeta procede de un cultivo, un paciente, un experimento de Keuss o un ensayo de tratamiento real. No predicen eficacia clínica ni sirven para calcular potencia o tamaño muestral.

## Diseño que se prueba

- Registros basales y controles sanos de edad equivalente en cada diferenciación.
- Deterioro de TDP-43 simulado antes de la elegibilidad y el tratamiento tardío.
- Elegibilidad definida por dos registros consecutivos por debajo de la trayectoria sana del mismo bloque.
- Aleatorización por **pozos** después de verificar elegibilidad, balanceada por diferenciación y déficit basal.
- Comparación principal en la unidad **cultivo/pozo**; diferenciaciones independientes para cuantificar la variación por bloques.
- Comparación en +3 y confirmación en +4 unidades de tiempo de simulación; no representan días reales.
- Muerte contabilizada con valor funcional 0 en un desenlace compuesto. Pérdidas técnicas permanecen sin imputar y se cuantifican.
- Reversión: mejoría relativa al propio T0 **y** respecto al grupo control en dos tiempos; protección: mejor resultado que control, pero sin superar T0.

## Resumen de escenarios

"""+table.to_markdown(index=False)+"""

Los intervalos bootstrap se calculan re-muestreando diferenciaciones (bloques); son **descriptivos de la simulación**. Un estudio real requerirá un análisis jerárquico especificado de antemano, cálculo de potencia con datos piloto, reglas de ausencia y observación ciega.

## Límites críticos

1. Los umbrales 0,19 (elegibilidad), 0,60 (viabilidad) y 0,06 (cambio mínimo) son **arbitrarios de demostración**, no calibraciones científicas.
2. La sincronización MEA es aquí una variable escalar inventada entre 0 y 1. En datos reales hay que fijar métrica exacta del fabricante/software, unidades, normalización y criterios QC.
3. Seleccionar cultivos por deterioro crea **regresión a la media**. La comparación aleatoria con control y las referencias sanas reducen, pero no eliminan todos los riesgos de interpretación.
4. Las pérdidas técnicas podrían ser informativas; la interpretación debe incluir análisis de sensibilidad. La muerte no es equivalente a la ausencia de registro por fallo de aparato.
5. El código no mide splicing, proteína UNC13A, ni la magnitud real de pérdida de TDP-43: esos ensayos molecular/viabilidad deben acompañar el MEA.
6. No se usa la simulación para sostener novedad, seguridad, utilidad clínica o financiamiento experimental.
7. El escenario 'early_reference' aparece como referencia descriptiva y no entra en la estimación primaria del efecto del tratamiento tardío.

## Archivos

- `datos_mea_sinteticos.csv` — series por pozo, incluidas muerte y pérdidas técnicas.
- `elegibilidad_aleatorizacion.csv` — decisión prospectiva por pozo antes de generar respuestas al tratamiento.
- `desenlaces_por_pozo.csv` — cambios por cultivo frente a T0 en registros +3 y +4.
- `resumen_simulaciones.csv` — contrastes y clasificación bajo las reglas anteriores.
- `trayectoria_*.png` y `comparacion_escenarios.png` — gráficos ilustrativos.

## Requisito antes de recibir datos reales

El laboratorio debe fijar con el piloto **sin conocer el tratamiento**: momento de inducción, calendario de MEA, definición de sincronía y viabilidad, criterios de dos registros consecutivos, tiempo máximo de elegibilidad, aleatorización, ausencia de datos, tiempo principal, tiempo de confirmación y modelo estadístico (diferenciación como clúster y pozo como unidad longitudinal).
"""
    (directory/"INFORME_SINTETICO.md").write_text(txt,encoding="utf-8")


def main():
    p=argparse.ArgumentParser(description="Simulación demostrativa de rescate funcional MEA/UNC13A")
    p.add_argument("--output",type=Path,default=Path("output"))
    p.add_argument("--seed",type=int,default=RNG_SEED)
    p.add_argument("--differentiations",type=int,default=8)
    p.add_argument("--candidates",type=int,default=12)
    args=p.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True)
    all_series=[];all_decisions=[]
    for i,sc in enumerate(SCENARIOS):
        pre,rng=simulate_pre(sc,args.seed+i*1000,args.differentiations,args.candidates)
        dec=detect_eligibility(pre)
        dec=randomize_by_block(dec,rng)
        series=complete_simulation(pre,dec,rng,sc)
        series=add_baseline_adjustment(series)
        all_series.append(series);all_decisions.append(dec)
        plot_trajectories(series,out/f"trayectoria_{sc}.png",sc)
    data=pd.concat(all_series,ignore_index=True)
    dec=pd.concat(all_decisions,ignore_index=True)
    endpoint=well_level_endpoints(data)
    summary=summary_by_scenario(endpoint)
    data.to_csv(out/"datos_mea_sinteticos.csv",index=False)
    dec.to_csv(out/"elegibilidad_aleatorizacion.csv",index=False)
    endpoint.to_csv(out/"desenlaces_por_pozo.csv",index=False)
    summary.to_csv(out/"resumen_simulaciones.csv",index=False)
    plot_effects(summary,out/"comparacion_escenarios.png")
    write_report(summary,dec,out)
    (out/"configuracion_simulacion.json").write_text(json.dumps({"seed":args.seed,"n_differentiations":args.differentiations,"n_candidates_per_differentiation":args.candidates,"baseline_indices":BASELINE,"damage_start_index":DAMAGE_START,"threshold_deficit":THRESHOLD,"min_viability":ELIGIBILITY_QC_MIN,"minimum_meaningful_change":MIN_MEANINGFUL,"primary_followup_units":FOLLOW_PRIMARY,"confirmation_followup_units":FOLLOW_CONFIRM,"data_type":"EXCLUSIVAMENTE SINTETICOS"},indent=2),encoding="utf-8")
    print(summary[["scenario","n_wells_late_ASO","n_wells_control","mean_ASO_change_f3","mean_CTRL_change_f3","mean_arm_difference_f3","mean_ASO_change_f4","mean_arm_difference_f4","classification"]].to_string(index=False))
    print("Generado en",out.resolve())

if __name__=="__main__":main()
