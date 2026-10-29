# Registro maestro de evidencia — 29/10/2026

Este registro sustituye los estados históricos. Reproducción técnica no equivale a replicación independiente, descubrimiento o eficacia. Ninguna línea acredita beneficio clínico propio.

| ID | Línea | Estado verificable | Pendiente o limitación |
|---|---|---|---|
| ELA-01 | GSE126542 expresión | Reproducción agregada de 45 campos numéricos, sin discrepancias, en reports/issue14-reproduction | Misma cohorte publicada; no ARN canónico/proteína/función; sensibilidad de TARDBP a normalización |
| ELA-02 | GSE126542 uniones | reports/fratta-junction-audit: 241→69 filas, pivot auditado y 24 campos agregados concordantes | Dos fórmulas UNC13A según bloque; 27 ausencias rellenadas con0; índice no molecular, misma cohorte |
| ELA-03 | GSE121569 | Extracción DEXSeq reproducida: 102 fragmentos y 18 campos agregados; no refit | Dos experimentos declarados; mapa biblioteca/diferenciación pendiente. No PSI de CE |
| ELA-04 | Genética | Existencia de material previo registrada | Sin hallazgo validado; revisión permitida de fuentes y proyecciones no personales |
| ELA-05 | CAMK2B | reports/camk2b-reproduction: resultado estructural agregado reproducido | Evento no reconstruido en catálogo cerebral; no ausencia molecular ni validación independiente |
| ELA-06 | Péptidos crípticos | Material inventariado | Sin espectrometría independiente ni validación proteómica propia |
| ELA-07 | UNC13A MEA | reports/mea-software-audit: pruebas y contraejemplos del software sintético | Corregir denominadores/completitud antes de reutilizar; no potencia o eficacia experimental |
| ELA-08 | GSE310723 | reports/geo-audit, isoforms y mapping-positive-controls: estructura y mapeo ejecutados | Una biblioteca por condición; sin inferencia diferencial |
| ELA-09 | GSE315972 | Estructura/mapeo ejecutados; corrección agregada 3 CI / 3 no CI / 2 CTL en informe de metadatos | Tejido heterogéneo, covariables/QC biológico incompletos; etiquetas históricas no son grupos cognitivos |
| ELA-10 | Rescate STMN2/UNC13A | Auditorías Keuss/Chan y propuestas en reports/accepted-keuss, chan-timing y reversal-design | Propuesta funcional, no ensayo; originalidad no certificada |
| ELA-11 | Uniones compartidas | reports/junction-filter-reconciliation: 21 antiguas reproducidas; pérdida de exones explica discrepancia. 1910 agrupadas, 1901 con soporte asignado positivo | Antiguas 21 no son cribado exhaustivo; modelos/soporte asignado no son lecturas directas |
| ELA-12 | GENCODE externa | reports/gencode-junction-annotation: 17 exactas / 1881 no encontradas para mismo gen / 3 de gen ausente | Catálogo de autores pendiente. Ausencia en v47 no prueba novedad |
| ELA-13 | AGRN | Antecedentes publicados y pregunta funcional en research/AGRN_CAMK2B_EVIDENCE_2026-10-29.md | Verificar isoforma/soporte y ensayos previos antes de proponer experimento |

## Reglas de interpretación

- ARN total, isoforma funcional, proteína, recuperación neuronal y beneficio clínico son niveles distintos.
- Las dos series Iso-Seq del mismo estudio no constituyen validación independiente por su intersección.
- Datos repetidos en varios paquetes/ejecuciones no son nuevas muestras.
- Los números de tests documentan controles de software, no cantidad de evidencia experimental.
- Informes antiguos conservan resultados/versiones y pendientes de entonces. STATE.md y este registro contienen los pendientes actuales.
- Para promover evidencia: fuente verificable, hash, código ejecutado, controles, tablas, sensibilidad y revisión con el alcance explícito. Una integración no aporta revisión científica externa.


## Fase #14 — reproducción agregada, rama independiente desde main

29/10/2026: reports/issue14-reproduction reproduce63campos agregados (45expresión/18extracciónDEXSeq) sin discrepancias. Fuentes GEO descargadas y fijadas; código recibido conservado sin ejecutar, sin tablas por caso/clínicas/genéticas importadas. STMN2/UNC13A mantienen dirección entre CPM/MR; TARDBP cambia de signo. DEXSeq102fragmentos, no refit niPSI; doce columnas de contraste no son doce diferenciaciones. Nueve tests nuevos sobre105de main:114OK. PR28con166tests sigue separado y no fusionado: contiene originalidad/crypTE/QCglobal posteriores al estado base de main. Leer ambos PR y reconciliar estados al integrar; no declarar esos informes ya incorporados. Issue14no se cierra: próximos BED/RdeFratta, deduplicación/denominadores y mapa de diferenciación121569. Sin nuevas cohortes, hallazgos clínicos, contactos, gasto, laboratorio o merge automático.

## Uniones Fratta auditadas — 29/10/2026, ampliación PR29

reports/fratta-junction-audit: BED/Rmd públicos fijados por SHA256 y Gitblob.241filas→69únicas/172repetidas,16muestras/7pares+2unsorted;27combinaciones ausentes rellenadas con0por método autor, no ceros observados.24campos agregados del paquete concordantes. Rmd2694incluye3clasesUNC13A;2766usa2clases. Cambio medio principal72.67puntos, dosclases72.00, sumar duplicados63.81; no porcentaje molecular, sensibilidad biológica ni nueva cohorte. No se leyeron archivos alélicos/clinica ni exportaron filas por muestra.124tests de esta rama (105base+19nuevos), PR28con166sigue separado. Próximo: mapa técnico biblioteca/experimento-diferenciación deGSE121569 antes de cualquier refit; issue14sigue abierta, sin contactos/laboratorio/gasto/merge.
