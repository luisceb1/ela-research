# Diccionario y alcance

- audit.json/supplements: medios deduplicados por href, alias XML, llamadas a tabla/localizador y política curada. No se asignan tablas por igualdad entre número de archivo y de tabla.
- legend_table_ids: identificadores de las42subtablas, sin contenido clínico o leyendas de muestras individuales.
- schemas: primera y segunda fila, nombres de hojas, ID del título, discordancia y cabeceras por letra. Se conservan posiciones repetidas para evitar pérdida por dict de nombres. Las fórmulas se marcan sin evaluación; no son resultados numéricos.
- culture_structure_qc: solo S7A–D y S8A–D. rows cuenta filas no vacías después de dos filas de cabecera, sin deduplicar ni exigir expresión positiva.
- valid_block_rows: longitudes/offsets enteros literales, cantidad igual a ExonNum, primer offset0, último extremo igual al span, longitudes positivas y bloques no solapantes. No significa validez biológica.
- invalid_block_rows/invalid_reasons: falla de reconstrucción estricta, no evidencia de ausencia del transcrito. noninteger incluye representaciones no admitidas; no se fuerzan ni separan dígitos para recuperar listas.
- valid_without_intron_rows: ningún intervalo intrónico entre los bloques reconstruidos; no asumir que todos sean eventos de splicing.
- listed_intron_labels: etiquetas separadas por punto y coma, solo en filas S8 con bloques válidos. La columna N se inspecciona por posición y contenido validado, no por las cabeceras erróneas B/C.
- labels_match_exon_boundaries: coincide exactamente con final exónico izquierdo/base inicial derecha, cromosoma y hebra; no coincide numéricamente con intervalo intrónico.
- labels_match_intronic_1based: coincide con primera/última base intrónica. Ausencia de la clave Counter en JSON significa contador0; no significa dato no evaluado para ese subtipo en S8.
- labels_unexplained_by_blocks: etiqueta válida sintácticamente que no encaja en ninguna de las dos convenciones probadas. No se corrige. Ejemplos inválidos solo contienen número de fila y motivo, no datos por persona.
- run.json: versión Python, controles, hash de salida repetida y agregados.115tests incluyen diez nuevos; no sumarlos con los históricos como evidencia experimental.
- author_catalog_matched=false: comparación de nuestras1901claves todavía no realizada; nunca interpretar como cero coincidencias.
