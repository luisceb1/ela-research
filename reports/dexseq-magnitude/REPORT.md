# Magnitud de discordancias por lote — 30/10/2026

## Evidencia ejecutada

Se analizaron las 204 medias de fracciones de cuentas previamente auditadas (102 fragmentos, dos lotes) del commit `18abfa5477ec78e937590fcc929bd44157a22a39`. No se redescargó ni reanalizó la matriz original en esta ejecución. Los controles de dimensiones, unicidad, finitud, tamaños técnicos, diferencias y cierre composicional pasan. La predicción previa de al menos una discordancia con magnitud >=0.1 pp en ambos lotes no queda refutada: persisten cuatro.

| Gen | Signo opuesto sin umbral | Signo opuesto con >=0.01 pp en ambos | >=0.1 pp en ambos | >=0.5 pp en ambos |
|---|---:|---:|---:|---:|
| STMN2 | 2 | 1 | 1 | 0 |
| UNC13A | 26 | 23 | 3 | 0 |
| TARDBP | 10 | 10 | 0 | 0 |

De las 38 discordancias originales, 34 tienen magnitud menor de0.1 pp en al menos un lote. No implica que todos sus cambios sean menores de0.1 pp ni que sean ruido. Se exige el umbral en ambos lotes, inclusivo. Los cuatro fragmentos que lo superan son:

| Gen / fragmento | Batch1 KD-control (pp) | Batch2 KD-control (pp) |
|---|---:|---:|
| STMN2 E009 | +0.163639 | -0.148627 |
| UNC13A E026 | -0.199486 | +0.163852 |
| UNC13A E030 | -0.101957 | +0.154234 |
| UNC13A E054 | +0.131524 | -0.173032 |

Concordantes >=0.1 pp en ambos: STMN2 7, UNC13A8, TARDBP6. Los restantes2/51/24 quedan bajo umbral en al menos uno. Con0.5 pp persisten3/0/1 concordantes, ninguna discordancia. Se publican todos los umbrales y102fragmentos, no solo los cuatro resaltados. No hay umbral de significación, relevancia funcional o equivalencia.

## Interpretación y resultados negativos

La clasificación de signos exageraba visualmente cuántas discordancias tienen magnitud apreciable en ambos lotes bajo estos umbrales arbitrarios. El resultado no distingue ruido técnico, efecto composicional y heterogeneidad real. No permite declarar TARDBP estable o concordante: sus diez inversiones siguen presentes sin umbral. Tampoco identifica los cuatro fragmentos con exones crípticos; ese enlace estructural aún requiere coordenadas y fuente primaria independientes.

La distancia composicional mitad de suma absoluta de cambios por gen es5.520594/2.707268 pp para STMN2,2.588070/2.952294 para UNC13A,2.134332/2.573651 para TARDBP (Batch1/2). Describe redistribución de fracciones de cuentas, no cantidad de ARN cambiado ni moléculas. Las medias por condición suman1 por construcción; no son réplicas ni PSI.

## Limitaciones y bloqueos reales

- La descarga directa GEO falló: `curl --connect-timeout 10 --max-time 20 -I <GEO URL>` devolvió28, Proxy CONNECT timeout. El conector GitHub sí funcionó. No hay nueva cobertura/lecturas observadas ni nuevo acceso al comprimido. El hash original GEO en provenance.json del informe previo es procedencia heredada, no verificación actual del original.
- Las medias de fracciones no identifican cuentas, ceros por biblioteca, ponderación por profundidad, sensibilidad de normalización o denominadores alternativos. No reconstruir esas variables mediante supuestos; ni dividir medias para fingir promedio de cocientes por biblioteca.
- Pozo/reactivo y fórmula original siguen pendientes. Dos lotes del mismo estudio no son replicación externa. Sin refit inferencial, p nuevos, hipótesis clínica o función.
- scite devolvió métodos primarios de Klim, confirmando el marco previamente auditado de dos experimentos y15bibliotecas en el contraste de expresión, distinto del contraste12DEXSeq. Excerpt de evidencia (12palabras): “two independent experiments were performed (Exp 1 and Exp 2)”. No resuelve reactivos por biblioteca. Consulta al artículo DEXSeq solo dio metadatos, `contentDenied=true`, sin lectura integral. Los cuatro filtros editoriales no devolvieron coincidencias y emitieron un mensaje genérico contradictorio sobre indexación; estado editorial no certificado, no garantía de ausencia de correcciones.

## Reproducción y QC

Plan fijado antes del cálculo: `research/plans/2026-10-30-dexseq-magnitude.md`. Python3.12.14, biblioteca estándar; sin semilla porque no hay aleatoriedad. Hash de tabla agregada y código en run.json, hashes de salidas en output_hashes.json. Comando:

```bash
python -m scripts.audit_dexseq_magnitudes --source reports/dexseq-batch-sensitivity/fragment_batch_aggregates.tsv --out reports/dexseq-magnitude
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

153tests correctos (147previos+6nuevos) localmente; compileall correcto. Primera ejecución incompleta:136tests/3errores por faltar dos archivos del checkout recuperado mediante conector. Se conservó el log, se recuperaron ambos archivos del mismo commit y la suite completa pasó sin cambiar su código. No era fallo científico o regresión del repositorio. Pruebas nuevas cubren límites inclusivos, ceros/no finitos, permutación y cambio de lotes, duplicación/ausencia, fracciones/deltas/cierre y etiquetas técnicas incorrectas. CI del nuevo commit se consulta tras persistir, no se presume del checkpoint anterior.

## Siguiente prueba discriminante

Recuperar el comprimido con hash ya conocido y exportar solo agregados técnicos de cuentas/profundidad para los cuatro fragmentos discordantes y todos los comparadores, incluidos ceros y sensibilidad al denominador por biblioteca. Antes: fijar plan, controles positivos/negativos y denominadores sin selección retrospectiva. Si no hay matriz, no estimar cobertura; alternativa segura: auditoría documental independiente de coordenadas/ensamblaje CE de STMN2/UNC13A. El refit sigue bloqueado hasta resolver pozo/reactivo/fórmula. Issue14 parcial. PR28 independiente y no incorporado; sin merge automático.

## Referencias

Klim, J. R., Williams, L. A., Limone, F., et al. (2019). ALS-implicated protein TDP-43 sustains levels of STMN2, a mediator of motor neuron growth and repair. *Nature Neuroscience, 22*,167–179. https://doi.org/10.1038/s41593-018-0300-4 . Métodos indexados vía scite, consulta30/10/2026; no nueva cohorte.

Anders, S., Reyes, A., & Huber, W. (2012). Detecting differential usage of exons from RNA-seq data. *Genome Research, 22*,2008–2017. https://doi.org/10.1101/gr.133744.111 . Solo metadatos recuperados en esta ejecución; no se utiliza para atribuir un método original no inspeccionado.
