#!/usr/bin/env python3
"""UNC13A/MEA: Monte Carlo sensitivity of a POST-deficit trial design.

All inputs, mechanisms and outcomes are synthetic. This is NOT a forecast of
real UNC13A effects, biological sample-size estimate or validated MEA workflow.
Scientific question: can a prospective design distinguish return of network
function from just slowing deterioration, under plausible *hypothetical* error?
Unit: well/culture, nested in independently differentiated batches.

Uses the prior prototype's structure (healthy same-age references; two screening
records; randomize only after eligibility; +3 and +4 follow-ups), while adding
cross-run evaluation and differentiation-level inferential bounds.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Literal
import numpy as np
import pandas as pd
from scipy.stats import t as t_dist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

MIN_CHANGE=0.06  # arbitrary synthetic meaningful change, not validated
ELIGIBILITY_DEFICIT=0.19  # arbitrary threshold, not validated
SCENARIOS={
    # Post-T0 benefit on SYNCHRONY after healthy-age adjustment compared to the
    # *same group's counterfactual without a corrector* at +3 and +4 indices.
    # Untreated additional deterioration: approximately -0.126 / -0.168.
    'none':(0.00,0.00),
    'protection_only':(0.09,0.11),
    'borderline_recovery':(0.19,0.23),
    'clear_recovery':(0.32,0.37),
}
SCENARIO_NAMES={
    'none':'Nulo', 'protection_only':'Solo protección',
    'borderline_recovery':'Recuperación límite', 'clear_recovery':'Recuperación clara'
}

@dataclass(frozen=True)
class Config:
    label:str='referencia'
    n_diffs:int=8
    n_candidate:int=12
    noise_sd:float=0.025
    response_sd:float=0.055
    technical_missing:float=0.03
    mortality_hazard:float=0.008
    batch_drift_sd:float=0.015
    missing_mode:Literal['MCAR','MNAR']='MCAR'
    # Missingness status is distinct from death. MNAR preferentially hides
    # relatively low function, and is intentionally an *adverse* mechanism.


def _lower_95_one_sided(x:np.ndarray) -> float:
    x=np.asarray(x,dtype=float)
    x=x[np.isfinite(x)]
    if len(x)<3:return -np.inf
    se=x.std(ddof=1)/np.sqrt(len(x))
    return float(x.mean()-t_dist.ppf(.95,len(x)-1)*se)


def simulate_once(config:Config,scenario:str,seed:int) -> dict:
    rng=np.random.default_rng(seed)
    tr3,tr4=SCENARIOS[scenario]
    records=[]; eligible_count=0; rand_count=0; deaths=0; missing=0
    for d in range(config.n_diffs):
        n=config.n_candidate
        # Entire pre-intervention history is generated before randomisation.
        # Index 0-6, damage starts at 3 and screening occurs at 5 and 6.
        batch=rng.normal(0,0.027)
        matur=rng.normal(0.008,0.003)
        normal_baselines=np.clip(0.70+batch+rng.normal(0,.038,n),.52,.86)
        susceptibility=np.maximum(.65,rng.normal(1,.12,n))
        T=np.arange(7)
        damage=np.where(T<3,0,np.minimum(.38,0.09+0.106*(T-3)))
        pre=(normal_baselines[:,None]+matur*T[None,:]
             -susceptibility[:,None]*damage[None,:]
             +rng.normal(0,config.noise_sd,(n,7)))
        sham_bases=0.70+batch+rng.normal(0,.025,(3,1))
        sham=sham_bases+matur*T[None,:]+rng.normal(0,config.noise_sd,(3,7))
        sham_mean=sham.mean(axis=0)
        baseline_mean=pre[:,:3].mean(axis=1)
        b_sham=sham_mean[:3].mean()
        expected=baseline_mean[:,None]+sham_mean[None,:]-b_sham
        delta=expected-pre
        eligible_at=np.full(n,-1,dtype=int)
        # Two consecutive prior observations, NOT post-treatment outcomes.
        for t0 in (5,6):
            good=(delta[:,t0]>=ELIGIBILITY_DEFICIT)&(delta[:,t0-1]>=ELIGIBILITY_DEFICIT)
            eligible_at[(eligible_at<0)&good]=t0
        eligible_count+=int((eligible_at>=0).sum())
        assignment=np.full(n,-1,dtype=int)
        # Block by differentiation and T0; sort by initial deficit and
        # randomise within adjacent pairs; orphan culture excluded.
        for t0 in (5,6):
            idx=np.where(eligible_at==t0)[0]
            idx=idx[np.argsort(delta[idx,t0])]
            for i in range(0,len(idx)-1,2):
                a,b=idx[i:i+2]
                if rng.random()<.5:assignment[a]=1;assignment[b]=0
                else:assignment[a]=0;assignment[b]=1
        assigned=np.where(assignment>=0)[0]
        rand_count+=len(assigned)
        if len(assigned)<4 or not np.any(assignment==0) or not np.any(assignment==1):
            continue
        post_drift=rng.normal(0,config.batch_drift_sd)
        responsivity=rng.normal(0,config.response_sd)
        slope_individual=rng.normal(0,.011,n)
        chosen_t0=eligible_at[assigned]
        chosen_arm=assignment[assigned]
        start=pre[assigned,chosen_t0]
        latent_t0=(normal_baselines[assigned]+matur*chosen_t0
                   -susceptibility[assigned]*damage[chosen_t0])
        sham_post={tt:float(sham_bases.mean()+matur*tt+rng.normal(0,config.noise_sd/np.sqrt(3)))
                   for tt in np.unique(np.r_[chosen_t0+3,chosen_t0+4])}
        dead=np.zeros(len(assigned),dtype=bool)
        row={'batch':d}
        for f in (3,4):
            event=(~dead)&(rng.random(len(assigned)) < (1-(1-config.mortality_hazard)**(f if f==3 else 1)))
            dead=dead|event
            deaths+=int(dead.sum())
            control_trajectory=-.042*f+post_drift*f/4+slope_individual[assigned]*f/4
            effect=(tr3 if f==3 else tr4)+responsivity
            latent=latent_t0+matur*f+control_trajectory+np.where(chosen_arm==1,effect,0.0)
            missing_rate=np.full(len(assigned),config.technical_missing)
            if config.missing_mode=='MNAR':
                missing_rate=np.clip(missing_rate*np.where(latent<.50,2.0,.40),0,.95)
            bad=(~dead)&(rng.random(len(assigned))<missing_rate)
            missing+=int(bad.sum())
            post=np.clip(latent+rng.normal(0,config.noise_sd,len(assigned)),0,1)
            post=np.where(dead,0,np.where(bad,np.nan,post))
            sham_change=np.array([sham_post[int(tt+f)]-sham_mean[int(tt)] for tt in chosen_t0])
            change=post-start-sham_change
            for arm,name in ((0,'control'),(1,'treated')):
                arr=change[chosen_arm==arm]
                row[f'{name}_{f}']=float(np.nanmean(arr)) if np.isfinite(arr).any() else np.nan
            row[f'effect_{f}']=row[f'treated_{f}']-row[f'control_{f}']
        records.append(row)
    block=pd.DataFrame(records)
    res=dict(config=config.label, scenario=scenario, n_diffs=config.n_diffs,
             eligible_wells=eligible_count,randomized_wells=rand_count,
             fraction_eligible=eligible_count/(config.n_diffs*config.n_candidate),
             n_analyzable_blocks=len(block),death_observations=deaths,
             technical_missing=missing,descriptive_recovery=False,
             evidence_recovery=False,descriptive_benefit=False,evidence_benefit=False,
             mean_treat_3=np.nan,mean_treat_4=np.nan,mean_effect_3=np.nan,mean_effect_4=np.nan)
    if len(block)<3:return res
    vals={col:block[col].dropna().to_numpy() for col in ('treated_3','treated_4','effect_3','effect_4')}
    if min(map(len,vals.values()))<3:return res
    means={k:float(np.mean(v)) for k,v in vals.items()}
    positive_treated=all(means[f'treated_{f}']>MIN_CHANGE for f in (3,4))
    relative_benefit=all(means[f'effect_{f}']>MIN_CHANGE for f in (3,4))
    res['descriptive_recovery']=positive_treated and relative_benefit
    res['descriptive_benefit']=relative_benefit
    # Evidence criterion: all four contrasts have lower one-sided 95% t
    # bounds > 0, and all observed mean contrasts > 0.06. A deliberately
    # stringent conjunction; no validated multiplicity or power claim.
    lo={key:_lower_95_one_sided(value) for key,value in vals.items()}
    res['evidence_recovery']=bool(res['descriptive_recovery'] and all(v>0 for v in lo.values()))
    res['evidence_benefit']=bool(res['descriptive_benefit'] and all(lo[f'effect_{f}']>0 for f in (3,4)))
    for f in (3,4):
        res[f'mean_treat_{f}']=means[f'treated_{f}']
        res[f'mean_effect_{f}']=means[f'effect_{f}']
    return res


def plan():
    base=Config()
    return [base,Config(label='4_diferenciaciones',n_diffs=4),
            Config(label='12_diferenciaciones',n_diffs=12),
            Config(label='ruido_alto',noise_sd=.070),
            Config(label='heterogeneidad_alta',response_sd=.130,batch_drift_sd=.055),
            Config(label='perdida_25porc',technical_missing=.25),
            Config(label='perdida_informativa',technical_missing=.24,missing_mode='MNAR'),
            Config(label='mortalidad_4pct_por_intervalo',mortality_hazard=.04),
            Config(label='estres_combinado',n_diffs=4,noise_sd=.070,response_sd=.130,batch_drift_sd=.055,
                   technical_missing=.25,missing_mode='MNAR',mortality_hazard=.025)]


def run(n_repeats:int,seed:int,out:Path):
    out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for cidx,c in enumerate(plan()):
        for sidx,sc in enumerate(SCENARIOS):
            for k in range(n_repeats):
                # Deterministic disjoint streams, no time-dependent randomness.
                rows.append(simulate_once(c,sc,seed+100000*cidx+20000*sidx+k))
    df=pd.DataFrame(rows)
    df.to_csv(out/'ejecuciones_montecarlo.csv.gz',index=False,compression='gzip')
    sums=(df.groupby(['config','scenario'],sort=False)
          .agg(repeticiones=('scenario','size'),
               recuperacion_descriptiva=('descriptive_recovery','mean'),
               recuperacion_con_evidencia=('evidence_recovery','mean'),
               beneficio_descriptivo=('descriptive_benefit','mean'),
               beneficio_con_evidencia=('evidence_benefit','mean'),
               diferenciaciones_analizables=('n_analyzable_blocks','mean'),
               pozos_aleatorizados=('randomized_wells','mean'),
               fraccion_elegible=('fraction_eligible','mean'),
               observaciones_muerte=('death_observations','mean'),
               perdidas_tecnicas=('technical_missing','mean'),
               efecto_estimado_3=('mean_effect_3','mean'),
               cambio_tratado_3=('mean_treat_3','mean'))
          .reset_index())
    sums.to_csv(out/'resumen_sensibilidad.csv',index=False)
    (out/'parametros.json').write_text(json.dumps({
      'seed':seed,'repetitions_per_cell':n_repeats,'scenario_effects_at_3_and_4':SCENARIOS,
      'configs':[asdict(c) for c in plan()],
      'units':'indices de registro inventados, NO días',
      'metric':'sincronía de red sintética [0,1] sin calibrar',
      'clinical_interpretation':'NINGUNA','input_data':'100% simulados',
      'minimum_meaningful_change_assumed':MIN_CHANGE,
      'prospective_eligibility_deficit_assumed':ELIGIBILITY_DEFICIT,
      'evidence_rule':'medias en +3,+4 >0.06 y límites inferiores unilaterales al 95% >0 en las 4 comparaciones por diferenciación'
    },indent=2,ensure_ascii=False),encoding='utf-8')
    return sums,df


def create_charts(sums,out):
    names=['none','protection_only','borderline_recovery','clear_recovery']
    for column,title,suffix in [
        ('recuperacion_descriptiva','Frecuencia de clasificación descriptiva de recuperación','clasificacion'),
        ('recuperacion_con_evidencia','Frecuencia con evidencia conservadora de recuperación','evidencia')]:
        fig,ax=plt.subplots(figsize=(11.5,5.2),dpi=150)
        configs=[x.label for x in plan()]
        x=np.arange(len(configs)); w=.19
        for j,sc in enumerate(names):
            vals=sums[sums.scenario==sc].set_index('config').reindex(configs)[column].values*100
            ax.bar(x+(j-1.5)*w,vals,w,label=SCENARIO_NAMES[sc])
        ax.set_xticks(x,[x.replace('_',' ') for x in configs],fontsize=8,rotation=22,ha='right')
        ax.set_ylim(0,105);ax.set_ylabel('Simulaciones clasificadas (%)')
        ax.set_title(title+' — DATOS SINTÉTICOS')
        ax.legend(loc='upper left',fontsize=8,ncol=2)
        ax.grid(axis='y',alpha=.2)
        fig.tight_layout();fig.savefig(out/f'{suffix}.png',dpi=170);plt.close(fig)
    fig,ax=plt.subplots(figsize=(11.5,5.2),dpi=160)
    configs=[x.label for x in plan()]
    s=sums[sums.scenario=='clear_recovery'].set_index('config').reindex(configs)
    x=np.arange(len(s));width=.34
    ax.bar(x-width/2,s.recuperacion_descriptiva*100,width,label='Regla descriptiva')
    ax.bar(x+width/2,s.recuperacion_con_evidencia*100,width,label='Regla con incertidumbre')
    ax.set_xticks(x,[k.replace('_',' ') for k in configs],fontsize=8,rotation=22,ha='right')
    ax.set_ylim(0,105);ax.set_ylabel('Clasificaciones de recuperación (%)')
    ax.set_title('Recuperación clara simulada: robustez de ambas reglas')
    ax.legend();ax.grid(axis='y',alpha=.2)
    fig.tight_layout();fig.savefig(out/'comparacion_reglas.png',dpi=170);plt.close(fig)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repeats',type=int,default=250)
    ap.add_argument('--seed',type=int,default=20261029)
    ap.add_argument('--output',type=Path,default=Path('resultados'))
    args=ap.parse_args()
    sums,_=run(args.repeats,args.seed,args.output)
    create_charts(sums,args.output)
    print(sums[sums.config.isin(['referencia','4_diferenciaciones','12_diferenciaciones'])][['config','scenario','recuperacion_descriptiva','recuperacion_con_evidencia','beneficio_con_evidencia','pozos_aleatorizados']].to_string(index=False))

if __name__=='__main__':main()
