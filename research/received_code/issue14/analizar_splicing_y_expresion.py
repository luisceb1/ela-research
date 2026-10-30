#!/usr/bin/env python3
"""ELA / GSE126542: reproduccion de indices de empalme y cruce con expresion genica.

Datos originales de uniones publicados por el laboratorio de Fratta:
https://github.com/frattalab/unc13a_cryptic_splicing/blob/main/data/liu_stmn2_and_unc13aaggregated.clean.annotated.bed
GitHub blob sha: 89de715d8640382800cef959be064b3af8e76eee
El csv local es una tabla DEDUPLICADA y pivotada del BED. Se eliminaron 172 lineas
identicas repetidas: 241 filas brutas, 69 registros unicos (ningun conflicto
para la misma combinacion muestra/region/tipo). No se sumaron repeticiones.

En este archivo se almacenan las 16 muestras; se excluyen 2 sin clasificar en
el analisis pareado. Formula exactamente como el codigo R de los autores.
Las 'PSI' de los autores son proporciones de uniones y NO fracciones absolutas
moleculares ni prueba de variacion de proteina.
"""
from pathlib import Path
import itertools
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, wilcoxon
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE=Path(__file__).resolve().parent
COUNTS=BASE/'union_counts_autores_deduplicados.csv'
EXPRESSION=BASE/'resultados_por_caso_v1.csv'
OUT=BASE/'resultados'
OUT.mkdir(exist_ok=True)
CASES=[f'S{i}' for i in range(1,8)]


def signflip_exact(d):
    d=np.asarray(d,dtype=float)
    obs=abs(float(d.mean()))
    return float(np.mean([abs(float((d*np.array(s)).mean()))>=obs-1e-12 for s in itertools.product([-1,1],repeat=len(d))]))

junctions=pd.read_csv(COUNTS)
expected={'STMN2_cryptic','STMN2_annotated','UNC13A_3prime','UNC13A_5prime','UNC13A_5prime_2','UNC13A_annotated','sample'}
assert set(junctions.columns)==expected
assert junctions.shape==(16,7)
assert not junctions['sample'].duplicated().any()
assert (junctions.drop(columns='sample')>=0).all().all()

junctions['caso']=junctions['sample'].str.extract(r'_(S[1-7])_')[0]
junctions['condicion']=np.select([
    junctions['sample'].str.contains('TDP_43_negative'),
    junctions['sample'].str.contains('TDP_43_positive')], ['TN','TP'],default='unsorted')
junctions['STMN2_total_junc']=junctions.STMN2_cryptic+junctions.STMN2_annotated
junctions['UNC13A_cryptic_junc']=junctions.UNC13A_3prime+junctions.UNC13A_5prime+junctions.UNC13A_5prime_2
junctions['UNC13A_total_junc']=junctions.UNC13A_cryptic_junc+junctions.UNC13A_annotated
junctions['STMN2_psi_junc']=junctions.STMN2_cryptic/junctions.STMN2_total_junc
junctions['UNC13A_psi_junc']=junctions.UNC13A_cryptic_junc/junctions.UNC13A_total_junc
junctions.to_csv(OUT/'muestras_con_indices.csv',index=False,float_format='%.9f')

pair=junctions[junctions.condicion.isin(['TP','TN'])].copy()
assert len(pair)==14 and all(pair.groupby('caso').condicion.nunique()==2)
wide=pair.set_index(['caso','condicion']).unstack('condicion')
summary=[]
pair_out=pd.DataFrame({'caso':CASES})
for gene in ['STMN2','UNC13A']:
    key=f'{gene}_psi_junc'
    tp=wide[(key,'TP')].reindex(CASES).to_numpy()
    tn=wide[(key,'TN')].reindex(CASES).to_numpy()
    d=tn-tp
    pair_out[f'{gene}_psi_TP']=tp
    pair_out[f'{gene}_psi_TN']=tn
    pair_out[f'{gene}_delta_psi_TN_TP']=d
    summary.append({'gen':gene,'n_pares':7,'psi_TP_media':np.mean(tp),'psi_TN_media':np.mean(tn),
       'diferencia_media_puntos_porcentuales':100*np.mean(d),'diferencia_mediana_puntos_porcentuales':100*np.median(d),
       'rango_psi_TN_min':min(tn),'rango_psi_TN_max':max(tn),'pares_TN_mayor':int((d>0).sum()),
       'p_exacta_perm_signos_bilateral':signflip_exact(d),
       'p_wilcoxon_exacto_bilateral':wilcoxon(d,alternative='two-sided',method='exact').pvalue,
       'cobertura_minima_uniones_TP':int(wide[(f'{gene}_total_junc','TP')].min()),
       'cobertura_minima_uniones_TN':int(wide[(f'{gene}_total_junc','TN')].min())})
    plt.figure(figsize=(7.7,5.3))
    for i, case in enumerate(CASES):
        plt.plot([0,1],[100*tp[i],100*tn[i]],marker='o',label=case)
    plt.xticks([0,1],['TDP-43 nuclear presente','TDP-43 nuclear ausente'])
    plt.ylim(-5,105)
    plt.ylabel('Índice de unión críptica (%)')
    plt.title(f'{gene} · Lecturas de unión críptica (7 pares)')
    plt.grid(axis='y',alpha=.25)
    plt.legend(title='Caso',loc='upper left',ncol=7,fontsize=8)
    plt.figtext(0.5,0.015,'Fuente: Brown/Fratta, datos republicados; no son medidas de proteína',ha='center',fontsize=8)
    plt.tight_layout(rect=[0,0.04,1,1])
    plt.savefig(OUT/f'{gene}_indices_pareados.png',dpi=175)
    plt.close()

p=pd.DataFrame(summary)
p.to_csv(OUT/'resumen_splicing.csv',index=False,float_format='%.9f')

expr=pd.read_csv(EXPRESSION)
assert set(expr.gen)=={'STMN2','UNC13A','TARDBP'}
assert set(expr.caso)==set(CASES)
for gene in ['STMN2','UNC13A']:
    v=expr[expr.gen==gene].set_index('caso').reindex(CASES)
    pair_out[f'{gene}_exp_delta_log2CPM_TN_TP']=v.delta_log2_CPM_TN_menos_TP.to_numpy()
    pair_out[f'{gene}_exp_cambio_CPM_pct']=100*(2**v.delta_log2_CPM_TN_menos_TP.to_numpy()-1)
    pair_out[f'{gene}_junction_canonica_TP']=wide[(f'{gene}_annotated','TP')].reindex(CASES).to_numpy()
    pair_out[f'{gene}_junction_canonica_TN']=wide[(f'{gene}_annotated','TN')].reindex(CASES).to_numpy()

pair_out.to_csv(OUT/'cruce_por_caso.csv',index=False,float_format='%.9f')

correlations=[]
for gene in ['STMN2','UNC13A']:
    x=pair_out[f'{gene}_delta_psi_TN_TP']
    y=pair_out[f'{gene}_exp_delta_log2CPM_TN_TP']
    rho, pval=spearmanr(x,y)
    correlations.append({'contraste':f'{gene} índice críptico vs cambio de expresión total', 'rho':rho, 'p_exploratoria':pval})
rho,pval=spearmanr(pair_out.STMN2_delta_psi_TN_TP,pair_out.UNC13A_delta_psi_TN_TP)
correlations.append({'contraste':'Diferencia de índice críptico entre genes', 'rho':rho,'p_exploratoria':pval})
pd.DataFrame(correlations).to_csv(OUT/'correlaciones_exploratorias.csv',index=False)

# Figura de doble eje EVITADA: distintas unidades y mediciones; panel separado
plt.figure(figsize=(7.9,5.3))
xs=np.arange(len(CASES))
plt.plot(xs,100*pair_out.UNC13A_delta_psi_TN_TP,marker='o',label='Cambio índice críptico UNC13A (p.p.)')
plt.plot(xs,100*pair_out.STMN2_delta_psi_TN_TP,marker='s',label='Cambio índice críptico STMN2 (p.p.)')
plt.xticks(xs,CASES)
plt.ylabel('Cambio índice de unión críptica (puntos porcentuales)')
plt.xlabel('Caso emparejado')
plt.title('Heterogeneidad de la respuesta de splicing por caso')
plt.grid(axis='y',alpha=.25)
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'heterogeneidad_entre_casos.png',dpi=175)
plt.close()

print('RESUMEN SPLICE:')
print(p.to_string(index=False))
print('\nCRUCE:')
print(pair_out[['caso','STMN2_delta_psi_TN_TP','UNC13A_delta_psi_TN_TP','STMN2_exp_cambio_CPM_pct','UNC13A_exp_cambio_CPM_pct','UNC13A_junction_canonica_TP','UNC13A_junction_canonica_TN']].to_string(index=False))
print('\nCORRELACIONES')
print(pd.DataFrame(correlations).to_string(index=False))
