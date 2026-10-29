# Tablas de mapeo

- `transcripts.tsv`: una fila por TXNAME diana **y serie**. `n_exons` y `exon_chain_1based_closed` describen coordenadas genómicas en orden ascendente, incluso en hebra negativa. `full_chain_in_gencode_v47` exige identidad de cromosoma, hebra y cadena completa. `n_unannotated_*` es comparación con referencia, no patología. `samples_gt0` y `samples_ge2` cuentan bibliotecas, no réplicas independientes; no garantizan moléculas únicas.
- `exons.tsv`: exones 1-based cerrados, orden genómico y etiqueta terminal/interno/single. `exact_exon_in_gencode_v47` requiere inicio y final exactos; un pequeño cambio de extremo se marca distinto.
- `junctions.tsv`: `left_exon_end` y `right_exon_start` son bases exónicas en orden genómico, **no** inicio/final intrónico. Donante/aceptor siguen la hebra. No hay una etiqueta de evento críptico validado.
- `support.tsv`: cuentas únicas originales, suma de esas cuentas por gen, cuota transcriptómica dentro del gen y ajuste por millón de cuentas asignadas de biblioteca. Un denominador cero queda vacío/NA. No se usa pseudocuenta ni se llama PSI/CPM depositado a estas magnitudes.
- `shared_full_chains.tsv`: coincidencias de cadena completa entre catálogos, independientemente del soporte. Las cadenas ENST retenidas de referencia no equivalen a expresión compartida ni validación externa.
- `mapping_controls.tsv`: mismo mapeo para ACTB y GAPDH; controles técnicos de identificación, sin suposición de estabilidad biológica.
- `other_gene_locus_overlaps.tsv`: transcritos de otros genes que solapan el locus de la diana (unión de intervalos de referencia); separa hebras y **no reasigna** genes. Sumas/detección solo para orientar revisión, sin llamar a esos transcritos isoformas de la diana.
- `summary.json`, `run.json`, `errors.json`, `tests.txt`: recuentos del mapeo, estado/entorno, errores finales y pruebas ejecutadas. El fallo inicial está en REPORT.md. `reference_source.json` fija URL/hash de GENCODE v47.
