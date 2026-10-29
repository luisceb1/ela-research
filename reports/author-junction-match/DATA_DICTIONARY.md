# Diccionario del cruce

## matches.tsv

Una fila por clave de entrada gene_id/cromosoma/primer y último nucleótido intrónico1-based/hebra. Son1901 uniones de catálogo, no1901 muestras o eventos nuevos.

- reference_symbol/identity: símbolo GENCODEv47 y validación única global símbolo→ENSG; no asignación por proximidad. Ausencia o ambigüedad no se cambia a no coincidencia.
- gencode_status: anotación externa previa por mismo gen, conservada sin nueva inferencia.
- match_status: categorías mutuamente excluyentes; exact_nonTE_label_match tiene prioridad sobre contextoS7 cuando hay ambas. not_found_in_eligible_culture_subset solo describe el subconjunto de filas reconstruibles, no ausencia de ARN.
- s8_sheets/s7_context_sheets: hojas donde coincide con gen exacto. No equivalen a expresión positiva ni efecto KD; punto significa sin evidencia estricta en esa clase.
- strict_evidence_rows/other_geometry_evidence_rows: referencias de filas autoras, no cuentas de lecturas, moléculas o replicados.

## evidence.tsv

Clave de candidato, categoría, hoja/fila, identificador molecular de transcrito autor, símbolo(s), clase declarada y estado de resolución de gen. Incluye evidencia ambigua/otro gen para auditoría, no solo aciertos. No contienen sujetos ni variables clínicas. El nombre transcript/... no se equipara al BambuTx del repositorio o a identidad de transcrito completo.

## summary.json

Denominadores, categorías, fuente por hash, QC por hoja y controles. s7_context_unique_junctions incluye las compartidas conS8; both_s7_and_s8 permite deduplicar. Los campos false sobre comparación completa/tejido/validación independiente son límites, no resultados negativos.

control_STMN2/status describe el resultado en el subconjunto elegible; cryptic_control_source_eligibility explica por qué no debe leerse como ausencia. invalid_block_partial_anchor_rows son anclajes incompletos que no entran en matches. canonical_geometry_control es una unión canónica del GTF y debe recuperarse; no es prueba de evento críptico o función. Los diagnósticos contienen únicamente estructura molecular de cultivo.

Locus significa cromosoma/hebra concordantes con el gen GENCODE, no pertenencia forzada a su span de anotación. Las extensiones terminales no se descartan por salirse del span canónico. PAR_Y se conserva al retirar versión numérica de IDs; evita colapsar copias distintas en la resolución global.
