# Diccionario de datos

- `candidate_identity.tsv`: 36 claves originales con identidad pendiente; estados por ENSG/locus, símbolo de origen, símbolo v47 y todos los IDs asociados globalmente a ese símbolo. No contiene 36 genes distintos.
- `author_ambiguous_candidates.tsv`: 278 claves originales; número de referencias por categoría y distribución de estados de identidad. Cero filas condicionales concordantes no implica ausencia molecular.
- `all_candidates.tsv`: sensibilidad en las 1901 claves; conserva estado anterior. Los contadores son referencias a filas, no observaciones biológicas independientes.
- `evidence_diagnostics.tsv`: 4008 referencias originales más resolución por token/ID. La clave primaria de trazabilidad incluye candidato, categoría, hoja, fila y transcripto. Una fila puede referirse a varios candidatos; no sumar como lecturas.
- `tokens_json`: token literal, método de reconocimiento y conjunto completo de IDs; `compatible_ids`: filtro exclusivo por cromosoma/hebra; `excluded_locus_ids`: descartados por esa discordancia, no por distancia; `unresolved_tokens_json`: tokens que impiden resolución conservadora.
- `conditional_same_gene`: todos los tokens conocidos y un solo ID compatible, igual al candidato. Es sensibilidad dependiente de anotación, no validación molecular ni una nueva coincidencia estricta.
- `conditional_other_gene`: un solo ID compatible distinto; `multiple_ids_at_chrom_strand`: más de uno; `unresolved_token`: incluye None/vacíos/no encontrados; `no_id_at_chrom_strand`: ninguno compatible.
- `conditional_primary_rows.json`: verificación directa de tres filas S8 del candidato GTPBP6; mismas coordenadas intrónicas 1-based, sin análisis de lecturas X/Y.
- `missing_gene_provenance.json`: ejemplos de GTF originales para ENSG ausente en v47; número de líneas no es abundancia.

El resultado estricto original354 se conserva. La sensibilidad355 no lo reemplaza. No significación, funcionalidad, replicación o novedad inferidas.
