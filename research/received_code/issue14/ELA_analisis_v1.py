#!/usr/bin/env python3
"""Reanálisis exploratorio reproducible de recuentos por gen GSE126542.

DATOS: 7 pares de núcleos neuronales corticales (FTD/ALS, C9orf72), TDP-43
nuclear positivo (TP) y negativo (TN); la matriz de recuentos por gen NO
permite medir inclusión de exones crípticos ni proteína ni función neuronal.

Uso:
  python ELA_analisis_v1.py --counts GSE126542_NeuronalNuclei_RNAseq_counts.txt.gz --out resultados

Requiere: pandas, numpy, scipy, matplotlib.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t as student_t, spearmanr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

GENES = ['STMN2', 'UNC13A', 'TARDBP']
CASES = [f'S{i}' for i in range(1, 8)]
SAMPLE_ORDER = [f'{s}_{t}' for s in CASES for t in ['TP', 'TN']]
FILENAME = 'GSE126542_NeuronalNuclei_RNAseq_counts.txt.gz'
SOURCE = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE126542'


def p_exacta_signflip(d):
    d = np.asarray(d, dtype=float)
    obs = abs(d.mean())
    vals = [abs(np.mean(d * np.array(signs)))
            for signs in itertools.product((-1, 1), repeat=len(d))]
    return np.mean(np.asarray(vals) >= obs - 1e-12).item()


def read_counts(path):
    # GEO omite etiqueta de cabecera para la primera columna. Es INDISPENSABLE
    # usar index_col=0 y no interpretar el literal 'NA' como valor ausente.
    df = pd.read_csv(path, sep='\t', index_col=0, keep_default_na=False,
                     compression='infer', low_memory=False)
    if set(df.columns) != set(SAMPLE_ORDER) or len(df.columns) != 14:
        raise ValueError(f'Columnas inesperadas: {df.columns.tolist()}')
    df = df[SAMPLE_ORDER]
    if any(not pd.api.types.is_integer_dtype(t) for t in df.dtypes):
        raise ValueError('Los datos no contienen únicamente recuentos enteros')
    if df.isna().any().any() or (df < 0).any().any():
        raise ValueError('Hay recuentos negativos o ausentes')
    # Este fichero incluye numerosas filas con identificador literal NA;
    # no sumarlas, reasignarlas ni interpretarlas como un gen válido.
    named = df.loc[df.index != 'NA']
    if not named.index.is_unique:
        raise ValueError('Duplicados de genes identificables: resolver antes de analizar')
    for g in GENES:
        if g not in named.index:
            raise ValueError(f'No aparece el gen esperado: {g}')
    return df


def calc_size_factors(df):
    # Cálculo de referencia análogo al median-of-ratios de DESeq2; NO es DESeq2.
    # Se excluyen las filas 'NA' ambiguas y filas con ceros para la media geométrica.
    named = df.loc[df.index != 'NA']
    positive = named.loc[(named > 0).all(axis=1)]
    if positive.shape[0] < 1000:
        raise ValueError('Insuficientes genes >0 para normalización robusta')
    gm = np.exp(np.log(positive).mean(axis=1))
    ratios = positive.div(gm, axis=0)
    factor = ratios.median(axis=0)
    factor = factor / np.exp(np.log(factor).mean())
    return factor, int(len(positive))


def graph_pairs(norm, gene, title, path, unit):
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    plt.rcParams.update({'font.size': 10})
    for k, case in enumerate(CASES):
        x = [0,1]
        y = [np.log2(norm[f'{case}_TP']), np.log2(norm[f'{case}_TN'])]
        ax.plot(x,y,alpha=0.8,linewidth=1.8, marker='o', markersize=5,label=case)
    ax.set_xticks([0,1],['Con TDP-43 nuclear (TP)','Sin TDP-43 nuclear (TN)'])
    ax.set_ylabel(f'log2({unit})')
    ax.set_title(title)
    ax.grid(axis='y',alpha=.2)
    ax.legend(title='Caso',ncol=7,fontsize=8, loc='best')
    fig.tight_layout()
    fig.savefig(path,dpi=175)
    plt.close(fig)


def run(path, out):
    out.mkdir(parents=True, exist_ok=True)
    df = read_counts(path)
    lib = df.sum(axis=0).astype(float)
    factors, ngenes = calc_size_factors(df)
    library_data = []
    for case in CASES:
        for cond in ['TP','TN']:
            sample=f'{case}_{cond}'
            library_data.append({'caso':case,'muestra':sample,
                'condicion':'TDP-43 nuclear presente' if cond=='TP' else 'TDP-43 nuclear ausente',
                'recuentos_totales':int(lib[sample]),
                'factor_normalizacion_median_ratio':float(factors[sample])})
    pd.DataFrame(library_data).to_csv(out/'muestras_y_bibliotecas.csv',index=False)
    rows=[]; records=[]; variants={}
    for gene in GENES:
        raw = df.loc[gene].astype(float)
        # CPM por recuentos sumados: lectura más transparente para presentación.
        cpm = raw / lib * 1e6
        # Pseudocuenta solo para estabilidad en log; no aporta datos aquí
        # pues las tres dianas tienen cobertura alta en las 14 muestras.
        log_cpm = np.log2(cpm + 0.5)
        med = raw / factors
        d_cpm=[]; d_mr=[]
        for case in CASES:
            p,n = f'{case}_TP',f'{case}_TN'
            dc = float(log_cpm[n]-log_cpm[p])
            dm = float(np.log2(med[n]/med[p]))
            d_cpm.append(dc);d_mr.append(dm)
            records.append({'gen':gene,'caso':case,
                'TP_raw':int(raw[p]),'TN_raw':int(raw[n]),
                'TP_CPM':float(cpm[p]),'TN_CPM':float(cpm[n]),
                'TP_log2_CPM_mas_0_5':float(log_cpm[p]),
                'TN_log2_CPM_mas_0_5':float(log_cpm[n]),
                'delta_log2_CPM_TN_menos_TP':dc,
                'delta_log2_median_ratio_TN_menos_TP':dm})
        ds=np.array(d_cpm)
        alt=np.array(d_mr)
        tcrit=student_t.ppf(0.975,len(ds)-1)
        se = ds.std(ddof=1)/np.sqrt(len(ds))
        ci=[float(ds.mean()-tcrit*se),float(ds.mean()+tcrit*se)]
        rows.append({'gen':gene,
            'media_delta_log2_CPM_TN_menos_TP':float(ds.mean()),
            'razon_geometrica_TN_TP_CPM':float(2**ds.mean()),
            'cambio_porcentual_CPM':float((2**ds.mean()-1)*100),
            'IC95_t_delta_log2_CPM_limite_inferior':ci[0],
            'IC95_t_delta_log2_CPM_limite_superior':ci[1],
            'n_pares':len(ds),'pares_con_aumento_CPM':int((ds>0).sum()),
            'pares_con_descenso_CPM':int((ds<0).sum()),
            'p_exacta_inversion_signos_bilateral_CPM':p_exacta_signflip(ds),
            'media_delta_log2_median_ratio':float(alt.mean()),
            'razon_geometrica_median_ratio':float(2**alt.mean()),
            'cambio_porcentual_median_ratio':float((2**alt.mean()-1)*100),
            'pares_con_aumento_median_ratio':int((alt>0).sum()),
            'pares_con_descenso_median_ratio':int((alt<0).sum()),
            'p_exacta_inversion_signos_median_ratio':p_exacta_signflip(alt)})
        variants[gene]={'CPM':ds,'median-ratio':alt}
        graph_pairs(cpm+0.5,gene,f'{gene}: comparación emparejada por caso (CPM+0,5)',
                    out/f'{gene}_expresion_pareada.png','CPM + 0,5')
    results=pd.DataFrame(rows)
    results.to_csv(out/'resultados_resumen.csv',index=False,float_format='%.9g')
    pd.DataFrame(records).to_csv(out/'resultados_por_caso.csv',index=False,float_format='%.9g')
    # QC: distribución de las diferencias por caso (evitar una media engañosa).
    fig,ax=plt.subplots(figsize=(7.1,4.5))
    xpos=np.arange(len(CASES))
    for gene,style in [('STMN2','o-'),('UNC13A','s-'),('TARDBP','^-')]:
        ax.plot(xpos,variants[gene]['CPM'],style,linewidth=1.7,markersize=6,label=gene)
    ax.axhline(0,linewidth=1,alpha=0.65)
    ax.set_xticks(xpos,CASES)
    ax.set_title('Cambio emparejado: ausencia frente a presencia de TDP-43 nuclear')
    ax.set_ylabel('Diferencia log2(CPM + 0,5), TN − TP')
    ax.set_xlabel('Caso')
    ax.grid(axis='y',alpha=.2)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out/'comparacion_tres_genes.png',dpi=175)
    plt.close(fig)
    rho,psp=spearmanr(variants['STMN2']['CPM'],variants['UNC13A']['CPM'])
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    audit={'fecha_analisis':'2026-10-28','dataset':'GSE126542',
           'fichero_original':path.name,'sha256_original':sha,
           'filas':len(df),'identificadores_unicos':int(df.index.nunique()),
           'filas_identificador_literal_NA':int((df.index=='NA').sum()),
           'muestras':len(df.columns),'pares':len(CASES),
           'recuentos_minimos_muestra':int(lib.min()),
           'recuentos_maximos_muestra':int(lib.max()),
           'genes_positivos_en_todas_muestras_para_median_ratio':ngenes,
           'spearman_rho_efectos_STMN2_UNC13A':float(rho),
           'spearman_p_exploratoria':float(psp),
           'advertencia':'Los datos son recuentos por gen de núcleos corticales post mortem; no miden splicing/proteína/función ni permiten inferencias terapéuticas.'}
    (out/'auditoria.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    def line(g):
        r=results.set_index('gen').loc[g]
        return (f"| {g} | {r['cambio_porcentual_CPM']:+.1f}% | "
            f"{int(r['pares_con_descenso_CPM'])}/7 descensos, {int(r['pares_con_aumento_CPM'])}/7 aumentos | "
            f"{r['p_exacta_inversion_signos_bilateral_CPM']:.5f} | "
            f"{r['cambio_porcentual_median_ratio']:+.1f}% |")
    report=f'''# ELA · Reanálisis GSE126542 · resultados reales

**Fecha del análisis:** 28 de octubre de 2026  
**Tipo de estudio:** análisis exploratorio secundario de datos públicos, no estudio experimental propio.

## Resumen ejecutivo

Hemos analizado {len(df):,} filas de recuentos de ARN en **14 muestras pareadas de 7 personas**, pertenecientes a núcleos neuronales corticales post mortem y clasificados según presencia (TP) o ausencia (TN) de TDP-43 nuclear. En el artículo original se describe que los siete casos tienen expansión C9orf72. Por tanto no deben confundirse con siete controles sanos frente a siete pacientes.

En las **siete comparaciones pareadas** STMN2 presenta menos recuentos normalizados cuando falta TDP-43 nuclear; UNC13A presenta **más recuentos totales** en esa misma condición. TARDBP no mantiene dirección uniforme. La segunda normalización de referencia (median-of-ratios) conserva la dirección de STMN2 y UNC13A; TARDBP cambia de signo y no muestra un patrón estable.

| Gen | Cambio TN respecto a TP (CPM) | Dirección dentro de los 7 pares | p exacta exploratoria bilateral | Cambio con median-of-ratios |
|---|---:|---|---:|---:|
{line('STMN2')}
{line('UNC13A')}
{line('TARDBP')}

Los porcentajes son razones geométricas de cambios **de ARN total por gen**, NO de ARNm funcional, proteína, sincronización o transporte axonal. Se emplea CPM con +0,5 antes de log2; el efecto relativo es el exponencial de la diferencia media en log2. Para median-of-ratios se usan genes con recuentos >0 en todas las bibliotecas.

## Interpretación y límites

1. **STMN2**: disminución consistente de recuentos totales normalizados, concordante con mecanismos conocidos de pérdida de función nuclear de TDP-43. Esto NO cuantifica el exón críptico ni prueba pérdida de transporte axonal en estas muestras.
2. **UNC13A**: el aumento de recuentos por gen en la fracción **nuclear** no permite inferir mayor producción de UNC13A funcional. Estos recuentos agregan diferentes variantes de ARN y se obtuvieron en núcleos, no en citoplasma o proteína. En otros trabajos se identifica splicing críptico de UNC13A en este mismo conjunto; hay que usar lecturas de empalme o datos procesados de isoformas para evaluar esa cuestión.
3. **TARDBP**: el ARN de TARDBP no es un marcador directo de localización subcelular de la proteína TDP-43. La clasificación experimental procede de inmunomarcaje/selección de núcleos, no del recuento de TARDBP.
4. **Pequeño n**: 7 sujetos emparejados, una medida RNA-seq por condición y sujeto. Una p exacta mínima posible de 0,015625 con 7 pares no es evidencia de una conclusión clínica ni de un descubrimiento nuevo. El IC t de las diferencias es descriptivo y depende de supuestos para n pequeño.
5. **Normalización**: las diferencias se resumen con CPM y con un método median-of-ratios similar al preprocesamiento de DESeq2; ninguno sustituye una prueba formal diferencial con dispersión RNA-seq y covariable del sujeto (DESeq2/edgeR).
6. **Identificadores ambigüos**: hay {audit['filas_identificador_literal_NA']} filas con el identificador literal `NA` en la fuente. Se conservaron para los totales por biblioteca pero se excluyeron de los cálculos de factores robustos. No deben asignarse a una proteína concreta.
7. **Estado de originalidad**: el conjunto y los eventos crípticos ya han sido analizados en publicaciones previas, como Brown et al. y Ma et al. (Nature, 2022). Nuestro resultado es una reproducción/descripción independiente de expresión génica.
8. **Generalización limitada**: tejido de corteza frontal post mortem de casos FTD/ALS C9orf72; no son experimentos longitudinales sobre neuronas motoras vivas, no son muestras de tratamiento y no predicen recuperación clínica.

**Análisis cruzado exploratorio**: correlación de Spearman entre los efectos emparejados de STMN2 y UNC13A = {rho:.2f} (p = {psp:.3f}). Con n=7, no hay evidencia suficiente para inferir asociación ni independencia.

## Siguientes pasos (ordenados)

1. **Auditar datos del mismo experimento a nivel de uniones de exones**: recuperar cuantificaciones validadas de STMN2/UNC13A o alinear datos de lecturas brutas; priorizar PSI/conteos de uniones y cobertura, evitando calcular PSI desde recuentos génicos.
2. **Contrastar con lo ya publicado** sobre exactamente GSE126542. La novedad no consiste en verificar de nuevo los mismos eventos.
3. **Estudiar sensibilidad técnica**: contrastar expresión con DESeq2/edgeR pareado, reconstrucción de isoformas y calidad de cobertura.
4. **Buscar una pregunta comprobable nueva** aplicable a las propuestas de rescate STMN2/UNC13A; después revisar la viabilidad con un equipo experimental.

## Procedencia y reproducibilidad

- GEO: {SOURCE}
- Estudio base: Liu et al. (2019), *Cell Reports*, “Loss of Nuclear TDP-43 Is Associated with Decondensation of LINE Retrotransposons”. https://pmc.ncbi.nlm.nih.gov/articles/PMC6508629/
- Reanálisis de UNC13A/STMN2: Brown et al. (2022), *Nature*. https://pmc.ncbi.nlm.nih.gov/articles/PMC8891020/
- Trabajo relacionado: Ma et al. (2022), *Nature*. https://www.nature.com/articles/s41586-022-04424-7
- SHA256 archivo de entrada: `{sha}`
- Reproducir: `python ELA_analisis_v1.py --counts {path.name} --out resultados`

## Archivos generados

- `resultados_resumen.csv`: tabla de efectos por gen y comprobación de normalización.
- `resultados_por_caso.csv`: comparación para cada gen y caso (incluye recuentos originales y CPM).
- `muestras_y_bibliotecas.csv`: tamaños de biblioteca y factores robustos.
- `comparacion_tres_genes.png`: diferencias emparejadas.
- `STMN2_expresion_pareada.png`, `UNC13A_expresion_pareada.png` y `TARDBP_expresion_pareada.png`: ilustraciones por gen.
- `auditoria.json`: estructura, recuentos y hash del archivo original.
'''
    (out/'INFORME_REANALISIS.md').write_text(report,encoding='utf-8')
    print('Auditoría:', json.dumps(audit,indent=2,ensure_ascii=False))
    print('\nResultados:')
    print(results.to_string(index=False))
    return results


def main():
    parser=argparse.ArgumentParser(description='GSE126542 reanálisis gen-level n=7 pares')
    parser.add_argument('--counts',type=Path,default=Path(FILENAME))
    parser.add_argument('--out',type=Path,default=Path('resultados'))
    args=parser.parse_args()
    if not args.counts.exists():
        parser.error(f'Falta fichero: {args.counts}')
    run(args.counts,args.out)


if __name__=='__main__':
    main()
