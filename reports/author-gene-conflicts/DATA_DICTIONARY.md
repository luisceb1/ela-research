# Diccionario

Cada fila de conflicts.tsv es una clave candidata intrónica y un gen autor alternativo. En este subconjunto hay74pares/74claves; no asumir esa igualdad en otros datos. Las coordenadas son intrónicas1-based, extremo derecho incluido; hebra y cromosoma forman parte de la identidad.

`GENCODE_*_transcripts`: modelos v47 que contienen la unión exacta bajo el gen candidato/autor, respectivamente; `.`=no encontrado en esa fuente para ese ID, no ausencia molecular. `GSE310723_*` y `GSE315972_*`: igual regla para GTF publicados; no cuentas de lecturas. Testigos separados por punto y coma, sin versiones inventadas.

`reference_junction_category`: author_reference_only/candidate_reference_only/both_reference_genes/neither_reference_gene. No selecciona cuál es el gen verdadero. `reference_gene_spans_overlap_diagnostic_only` no se usa como filtro; `gene_assignment_resolved` permanece false.

`primary_rows.json`:56filas distintas verificadas y número de referencias a esas filas; no copiar ese número a n biológico. La comprobación usa originales XLSX fijados, no fórmulas evaluadas ni reparación de bloques.
