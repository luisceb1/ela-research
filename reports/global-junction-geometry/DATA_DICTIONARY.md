# Diccionario de geometría global

Unidad: clave candidata=(gene_id,chrom,intron_start,intron_end,strand). Geometría elimina gene_id y conserva los otros cuatro componentes. Intrones1-based inclusivos; no intervalos exónicos ni BED0-based.

`global_status`:same_gene_exact,other_gene_only_exact,not_found_in_v47_any_gene. La primera tiene prioridad si hay testigos del mismo gen; otros testigos se conservan en columnas separadas. No son clases de verdad molecular o novedad.

`same_gene_transcripts`:ENSTexactos del gen candidato; `other_gene_ids`:todos los ENSGdiferentes con esa geometría; `reference_genes_with_geometry` y `reference_transcripts_with_geometry`:cuentas de anotación por clave, no lecturas/replicados. `.`=sin testigo en ese campo y snapshot.

`coverage_group`:partición conjunta con los estados históricos de autores; no redefine354 estrictas ni355 condicionales. not_found_in_two_inspected_resources solo incluye ausencia de coincidencia en dos recursos limitados. author_catalog_representation_only incluye contextoS7, que no valida que la propia unión sea derivadaTEo funcional.

reference_witnesses.tsv repite la clave candidata para cada ENSG/ENSTtestigo. Si varias claves comparten geometría, los testigos pueden repetirse; no sumar como moléculas. Los nombres/IDs son anotaciones públicas, no identificadores clínicos.
