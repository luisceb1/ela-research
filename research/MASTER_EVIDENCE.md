# Registro maestro de evidencia — 30/10/2026

Registro vigente de ambas líneas consolidadas. Una integración, una reproducción técnica y una validación funcional son cosas distintas. No hay nueva terapia, diana acreditada o beneficio clínico propio.

| ID | Línea | Evidencia ejecutada | Límite vigente |
|---|---|---|---|
| ELA-01 | GSE126542 expresión | 45 campos agregados reproducidos; STMN2 baja en 7/7 pares, UNC13A sube ARN nuclear total; TARDBP cambia de signo entre normalizaciones | No proteína funcional, tratamiento o nueva cohorte |
| ELA-02 | GSE126542 uniones | BED/Rmd auditados: 241→69 filas; 24 campos concordantes; 27 ausencias rellenadas con 0 por autor; fórmulas/deduplicación alteran índices | Índices de cuentas, no porcentaje molecular ni cohorte adicional |
| ELA-03 | GSE121569 | 102 bins/18 campos extraídos; 12 columnas en dos lotes; 7.030.428 cuentas concordantes; 4.034 duplicados solo anotativos | No refit inferencial; pozos/reactivos/modelo pendientes |
| ELA-04 | Genética | Material previo inventariado | Sin hallazgo validado; no clínica o genotipos personales nuevos |
| ELA-05 | CAMK2B | Resultado estructural agregado reproducido | Ausencia de modelo cerebral no prueba ausencia molecular |
| ELA-06 | Péptidos crípticos | Material inventariado | Sin proteómica independiente propia |
| ELA-07 | MEA | Auditoría del software sintético y contraejemplos | No ensayo funcional, potencia o eficacia medida |
| ELA-08 | GSE310723 | Inventario técnico y mapeo ENSG ejecutados | Una biblioteca por condición; sin inferencia diferencial |
| ELA-09 | GSE315972 | Estructura/mapeo y corrección agregada de grupos publicados | Tejido heterogéneo; QC/lecturas incompletos, sin análisis clínico nuevo |
| ELA-10 | Función/originalidad | Keuss/Chan y revisión dirigida; seis fichas funcionales no reconstruyen posdéficit; protocolo UNC13A v0.4 | Propuesta incremental; originalidad no certificada; sin experimento |
| ELA-11 | Catálogo compartido | Parser corregido; 1.910 uniones/1.901 con soporte asignado; 21 históricas no exhaustivas | Modelos/asignaciones no equivalen a lecturas directas o réplica externa |
| ELA-12 | GENCODE/autores | 354 coincidencias estrictas/355 solo sensibilidad; partición 1.901: 545 anotadas, 353 solo autores, 182 pendientes, 821 sin coincidencia limitada | No 821 descubrimientos ni origen molecular reasignado |
| ELA-13 | AGRN | Antecedentes y pregunta publicados | No nueva diana/propuesta original certificada |
| ELA-14 | DEXSeq y CE | Sensibilidad descriptiva, cuentas y denominadores; 72 bins STMN2/UNC13A sin solapar regiones CE publicadas bajo el mismo ensamblaje | No cuantificación directa de CE ni ausencia biológica; no PSI |
| ELA-15 | SH-SY5Y | Seis bibliotecas exactas a ENA; 16 uniones en S6; una etiqueta concordante, dos conflictos de hebra, cuatro alias sin resolver | Reanálisis conjunto bloqueado; unidades independientes no establecidas |

| ELA-16 | Selección local de fuentes | Tres candidatas; BW y TPM no aportan cuentas directas; Parquet E-MTAB-15653 real, 2.598.287 filas/22 bibliotecas, hashes y QC verificados | Ninguna aceptada para el contraste completo; unidad independiente y evento pendientes. No replicación externa conseguida |

## Localizadores

- ELA01–03: reports/issue14-reproduction, fratta-junction-audit, gse121569-design y dexseq-qc.
- ELA08–09/11: reports/geo-audit, isoforms, mapping-positive-controls y junction-filter-reconciliation.
- ELA12: reports/author-catalog-schema, author-junction-match, author-gene-ambiguity, author-gene-conflicts y global-junction-geometry.
- ELA10: reports/originality-audit, functional-data-inventory y research/UNC13A_POST_DEFICIT_PROTOCOL_v0.4.md.
- ELA14: reports/dexseq-batch-sensitivity, dexseq-magnitude, dexseq-coverage y ce-bin-coordinate-audit.
- ELA15: reports/junction-source-inventory, shsy5y-junction-map y junction-definition-search.

## Reglas

ARN total, procesamiento de una unión, isoforma funcional, proteína, recuperación neuronal y beneficio clínico son niveles diferentes. Compartir cohortes entre series/tablas/paquetes no añade replicación. Las no coincidencias y búsquedas negativas no prueban novedad o ausencia. Tests, commits y fuentes bibliográficas no son experimentos.

Se conservan los informes históricos con sus hashes/entornos/resultados, pero sus próximos pasos antiguos no son el planning vigente. El criterio de entrada para nueva evidencia está en NEXT_STUDY_GATE. Los registros maestros anteriores se archivan en reports/integration-20261030/history.

ELA16: reports/source-selection-20261030/REPORT.md, results.json y manifest research/references/independent_source_gate_20261030.json. Propuesta en PR separado de #30; sus resultados no se suman ni se presentan como incorporados a main antes de merge.
