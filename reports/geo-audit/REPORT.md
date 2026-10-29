# Auditoría GSE310723 / GSE315972 — 2026-10-29

> Nota de consolidación (29/10/2026): inventario técnico histórico. group_label y libraries_in_group de samples.tsv describen etiquetas depositadas, no estratos cognitivos. La corrección agregada posterior 3 CI / 3 no CI / 2 CTL está en reports/ALS_CI_metadata_correction_2026-10-29.md. Las tareas de mapeo posteriores están ejecutadas; estado vigente en research/STATE.md. Integración de código no equivale a revisión científica externa.

Evidencia: **auditoría técnica reproducible; interpretación biológica exploratoria**. Relacionado con #1.

## Evidencia

| Serie | Bibliotecas GSM | Transcritos uniqueCounts y GTF | Exones GTF | Cuentas únicas asignadas/biblioteca | Transcritos detectados/biblioteca |
|---|---:|---:|---:|---:|---:|
| GSE310723 | 4 | 392,871 | 2,232,577 | 330,066–483,824 | 35,322–40,864 |
| GSE315972 | 8 | 401,720 | 2,266,926 | 230,530–433,750 | 30,316–47,291 |

Los 12 GSM se enlazan de forma biunívoca a las 12 columnas. No hubo TXNAME duplicados, cuentas negativas/no finitas, filas de ancho inválido, TXNAME ausentes del GTF ni discordancias exactas GENEID/gene_id. Tampoco hay transcritos del GTF ausentes de uniqueCounts. Cada uniqueCount es entero y no supera el valor correspondiente de counts. Hay 133.040 celdas fraccionarias en counts de GSE310723 y 258.417 en GSE315972; no se intercambian estas matrices.

Metadatos técnicos de los GSM: hg38; GENCODE v47; bambu 3.2.6; minimap2 2.24; IsoSeq 4.0.0. Los GTF extendidos contienen transcript/exon y gene_id/transcript_id/exon_number, sin gene_name ni una clasificación explícita de exones crípticos.

## Interpretación

- GSE310723: cuatro bibliotecas de cultivos i3N, un GSM por combinación Ctrl/TDP43KD × con/sin 5-Azacytidine. Los títulos dicen replicate 1. No hay replicación biológica independiente por condición demostrada aquí. No procede inferencia diferencial ni simular réplicas.
- GSE315972: ocho bibliotecas de corteza prefrontal BA46; la serie las describe como ocho muestras de donante. Dos bibliotecas por etiqueta ALS-C9 / ALS-ci / ALS / CTL. Los GSM verifican el tejido, grupos publicados y C9; no se usa el nombre de columna como única prueba. ALS-C9 mezcla clasificación cognitiva en los títulos/metadatos, por lo que no son cuatro estratos homogéneos para modelado factorial.
- Los controles de GSE315972 tienen más cuentas únicas asignadas que las bibliotecas ALS sin C9/CI. La suma de cuentas detectadas no mide por sí sola calidad biológica, carga patológica ni número de células. Las comparaciones deberán mostrar sensibilidad a profundidad y composición.

## Limitaciones y explicaciones alternativas

- Calidad de ARN (RIN), profundidad de reads crudos, lotes, proporciones celulares e independencia experimental no están auditados con estas tablas. No se afirma que no existan en otras fuentes.
- La ficha GSM9441959 incluye un protocolo de extracción que habla de cultured cells pese a que fuente y diseño dicen tejido cerebral. Inconsistencia de texto registrada durante consulta del SOFT; no demuestra intercambio de muestras. Se priorizan fuente tisular y diseño de serie, dejando la discrepancia abierta.
- La cuenta única es un subconjunto de la asignación de transcritos y puede penalizar isoformas ambiguas. Un cero no demuestra ausencia molecular; un transcrito anotado no implica expresión.
- Los archivos no demuestran origen causal, rescate molecular, función neuronal ni beneficio clínico. No se combinan estadísticamente cultivo y cerebro.

## Reproducción, incidencias y siguiente prueba

`python -m unittest discover -s tests -p test_geo_audit.py -v` y `python scripts/geo_audit.py`. Las pruebas previas de watchers también pasan. Manifiesto: `sources.json`; parámetros y entorno: `run.json`; tablas: `samples.tsv`, `depth.tsv`, `unmapped.tsv`, `gene_mismatches.tsv`; QC: `qc.json`. Véanse DATA_DICTIONARY.md y EXECUTION_NOTES.md.

Las fuentes originales son los endpoints oficiales GEO SOFT y suplementos HTTPS especificados en sources.json. Se descargaron seis archivos de datos (uniqueCounts, counts y GTF por serie), dos registros de serie y doce proyecciones técnicas GSM. Los binarios son recuperables por URL y SHA256, sin incorporarlos a git.

Criterio técnico alcanzado: inventario y controles estructurales ejecutados en ambas series; **pendiente revisión del PR**. La independencia biológica/covariables no se ha confirmado más allá del diseño depositado; este límite se conserva en la tabla.

Siguiente prueba discriminante (#2): enlazar STMN2/UNC13A por TXNAME/GENEID y verificar símbolos/estructuras contra GENCODE v47. Si los IDs no enlazan o cambian los hashes, rechazar el mapeo; si una estructura falta de referencia, etiquetarla no anotada sin llamarla críptica validada.
