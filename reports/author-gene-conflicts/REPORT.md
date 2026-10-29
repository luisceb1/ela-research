# Conflictos de gen: explicación alternativa de 73 uniones — 29/10/2026

## Evidencia ejecutada

**73 de los 74 conflictos contienen una unión exacta anotada en GENCODE v47 bajo el gen señalado por los autores.** La misma unión aparece en modelos de ambos genes en los dos GTF GEO. Esto limita el reclamo de novedad de esas geometrías y aporta una explicación alternativa de atribución. No demuestra cuál es el gen de origen de las lecturas ni justifica reasignarlas automáticamente.

Se auditaron 74 claves de 23 genes candidatos, con 298 referencias a filas autoras; esas referencias corresponden a 56 filas originales distintas. Se verificaron directamente las 56 en los XLSX fijados por hash: bloques/etiqueta elegibles, transcripto y gen concordantes con la proyección anterior. No son 298 lecturas ni 56 réplicas. Plan previo: `research/plans/2026-10-29-gene-conflicts.md`.

| Comprobación | Resultado |
|---|---:|
| Unión exacta en transcripto v47 del gen autor, sin coincidencia en transcripto v47 del candidato | 73 |
| Unión no encontrada en transcritos v47 de ninguno de los dos genes | 1 |
| Unión en modelos de ambos genes en GTF cultivo | 73 |
| Unión en modelos de ambos genes en GTF cerebro | 73 |
| Unión solo en modelos del candidato en ambos GTF GEO | 1 |
| Solapamiento de spans de los dos genes en v47, diagnóstico geométrico | 16 |
| Conflictos cuyo verdadero gen de origen queda demostrado por este QC | 0 |

## Método y controles

Entradas `matches.tsv` y `evidence.tsv` del cruce anterior, con SHA256 verificado. Se selecciona exactamente `coordinate_match_different_gene`, sin modificar el universo ni sus 354 coincidencias estrictas. Cada símbolo autor debe corresponder globalmente a un único ENSG diferente y concordar en cromosoma/hebra; se verifica de nuevo con el índice completo v47.

Se leen todos los exones de los genes pertinentes en GENCODE y en cada GTF GEO. Se agrupan por gen, transcripto, cromosoma y hebra **antes** de formar uniones; no se presupone que las líneas de un transcripto sean consecutivas. Coordenadas intrónicas 1-based: fin del exón izquierdo+1, inicio del derecho−1. Se rechazan exones superpuestos dentro del mismo modelo, se distinguen hebras y se conservan modelos de genes distintos aun cuando tengan la misma geometría. Exones idénticos repetidos no crean una unión nueva.

`conflicts.tsv` exporta por cada clave los dos IDs, símbolos, categoría de referencia y todos los transcriptos testigos en las tres fuentes. Se procesaron 634 grupos de transcripto pertinentes en v47, 666 en cultivo y 680 en cerebro. Son grupos de anotación, no abundancia ni replicación. El solapamiento de spans se informa solo como contexto: no se usa para elegir un gen o descartar extensiones no canónicas.

## Ejemplo y conflicto residual

Ejemplo de atribución alternativa: `AURKC / ENSG00000105146`, chr19:57194002–57205396, hebra+. En v47 la unión aparece en `ZNF264 / ENSG00000083844`, transcripto `ENST00000263095.10`. En los GTF GEO también está en modelos atribuidos a AURKC: `BambuTx6996` en cultivo y `BambuTx18477` en cerebro, además del modelo ENST de ZNF264. No se elige entre ambos por nombre, cercanía o condición experimental. Es una unión ya anotada en otro gen; su presencia en un modelo extendido no crea una geometría nueva.

El caso restante es `ENSG00000278915`, chr5:140871438–140875240, hebra−, frente a autor `ENSG00000278946`. No se encontró esa unión exacta bajo ninguno de los dos IDs en v47. Sí aparece en modelos del candidato `BambuTx4510` y `BambuTx12945` en cultivo/cerebro, sin modelo testigo del gen autor en esos GTF. La discrepancia de atribución persiste; no inventamos alias, cambio de versión o causa de error. La comprobación de filas XLSX confirma la etiqueta autora, no su verdad molecular. No llamarlo nuevo o ausente biológicamente.

## Interpretación y límites

El filtro previo «no encontrado para el mismo gen» es insuficiente para hablar de novedad de una unión. En este subconjunto, 73 geometrías ya están en otro gen de la referencia. Esto no invalida automáticamente un posible transcripto extendido o compartido; valida una explicación alternativa que debe examinarse antes de priorizar.

Tampoco se establece que la asignación de los autores sea correcta solo por concordar con v47: las tres fuentes contienen modelos, no una auditoría de alineamientos o moléculas. No se ha probado expresión diferencial, empalme aberrante inducido, proteína o función. Cultivo y cerebro pertenecen al mismo estudio, sin nueva replicación. El resultado no se extrapola a las 1901 claves; quedan geometrías no examinadas aquí bajo otros genes.

## Reproducción y siguiente acción

`python scripts/audit_gene_conflicts.py --cache /ruta/cache_GEO_GENCODE --author-cache /ruta/author-supplements` reproduce tablas y verificación de filas originales. Los tres GTF y ambos XLSX están fijados por hash; manifiestos/URLs en sources.json y run.json. Sin `--author-cache` se reproduce solo el contraste de modelos; `primary_rows.json` conserva la comprobación primaria efectuada con esa opción.

Siete pruebas nuevas: exones intercalados, mismo nombre de transcripto entre genes, hebras, exones superpuestos, adyacentes/duplicados, categoría de referencia y exclusión de genes ajenos. Suite **156 tests OK**. No se calcularon efectos/p-valores ni se importó clínica. No hubo contactos, gastos o laboratorio.

Siguiente tarea segura: extender el control de geometría exacta a **todos los genes de v47** para las 1901 claves, conservando IDs y hebras; no limitarse al gen candidato o al gen que figura en el catálogo autor. Separar «geometría ya anotada en otro gen» de «no encontrada en referencia» antes de revisar cobertura/priorización. Mantener conflictos como tales; ausencia de coincidencia tampoco certificará novedad. Esta es continuación del QC de anotación, no una nueva línea experimental.
