# Diccionario de datos y alcance

- `samples.tsv`: una fila por biblioteca GSM depositada y columna de uniqueCounts. `group_label` conserva la etiqueta publicada; no implica un estrato clínico homogéneo ni una réplica experimental independiente. `libraries_in_group` cuenta bibliotecas, no experimentos repetidos. `unit` y `verified_independent_biological_replicates` explicitan el límite de verificación.
- `depth.tsv`: suma de **uniqueCounts asignadas a transcritos** y número de transcritos con cuenta >0 por biblioteca. No son reads crudos, profundidad de bases, RIN, cobertura de exones ni estimación de número de células. `fractional_unique_cells` cuenta celdas numéricas no enteras.
- `qc.json`: filas, genes exactos (con versión), encabezados, cuentas asignadas, detección, inventario de features/atributos GTF, y comparación celda a celda uniqueCounts <= counts. No equipara ambas medidas. Los `counts` pueden ser fraccionarios por asignación/estimación; no se redondean a enteros.
- `unmapped.tsv`: TXNAME de uniqueCounts ausentes del GTF de **esa misma serie**; un fichero con solo encabezado significa cero casos, siempre que `run.json` indique ejecución completa de ambas series.
- `gene_mismatches.tsv`: TXNAME encontrados, pero GENEID de tabla distinto al `gene_id` de GTF; no se corrige quitando versiones.
- `sources.json`: URL exacta, fecha UTC, bytes y SHA256 del original descargado; hash adicional de la caché cuando solo se guarda una proyección técnica de SOFT. Los hashes de GSM son del texto SOFT recibido, no del HTML ni de un fichero clínico.
- `run.json` y `errors.json`: entorno, parámetros, fecha, alcance descriptivo y errores de la ejecución. Una salida parcial nunca acredita la auditoría de ambas series.

Tablas originales: `TXNAME` = identificador local de transcrito (ENST con versión o identificador Bambu); `GENEID` = identificador de gen informado por el depositante. Las otras columnas son bibliotecas; sus etiquetas se verifican con `samples.tsv`. BambuTx1 de dos series **no** es el mismo transcrito por compartir nombre.

GTF original (nueve campos separados por tabuladores): cromosoma; fuente (Bambu); feature; inicio; final; score; hebra; frame; atributos. Coordenadas **1-based, cerradas**; hebra `+`/`-`. Atributos observados: `gene_id`, `transcript_id` y, en exones, `exon_number`. No se supone que haya nombres de gen, CDS, evidencia de exón críptico, abundancia ni función codificante. `extended` no significa que cada transcrito nuevo sea críptico ni que esté validado.

Reproducción: `python -m unittest discover -s tests -v` y `python scripts/geo_audit.py`. Una primera ejecución descarga originales; las siguientes verifican la caché. `--refresh` vuelve a consultar, pero rechaza cambios respecto al SHA ya fijado. Para investigar una actualización de fuente se conserva el manifiesto anterior y se revisa una nueva versión por separado. No se incluyen datos binarios en git; se conservan URL y hashes para recuperarlos exactamente.
