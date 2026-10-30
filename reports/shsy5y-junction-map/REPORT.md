# SH-SY5Y: enlace a ENA y coordenadas de uniones — 30/10/2026

## Resultado

**Se enlazan exactamente las seis filas SH-SY5Y del CSV de cuentas con seis runs públicos de PRJEB42763.** La prueba decisiva es el nombre del BAM en el XML de cada run. No se asignan registros por orden o parecido de alias.

| Alias técnico en CSV | Grupo publicado | Run ENA |
|---|---|---|
| CTR07 |control|ERR5300363|
| CTR08 |control|ERR5296849|
| CTR09 |control|ERR5296899|
| TDP10 |TDP-43 KD|ERR5296853|
| TDP11 |TDP-43 KD|ERR5301820|
| TDP12 |TDP-43 KD|ERR5296827|

Por ejemplo, ENA usa el alias `SHSY5YControl1`, pero su XML deposita `CTR07.Aligned.sorted.out.bam`. Se retira solo el sufijo fijo documentado y se exige identidad exacta con el CSV. Se comprueban estudio, run, experimento, unicidad y condición. Las accesiones de muestra/experimento quedan en la tabla técnica. **Esto verifica procedencia de bibliotecas, no independencia biológica ni número de cultivos independientes.** No se descargó ningún BAM/FASTQ.

## Coordenadas: resultado parcial y conflictos

Se recuperó Supplementary Table 6 de Brown et al. (2022) desde el archivo público PMC AWS, tras recibir HTML de recaptcha en la URL habitual. Es un XLS OLE válido de 29.184 bytes, SHA-256 `54d91b96f58b0cb85234f10c11451ca86211e183e1d2d6076dab3fcd87b83a41`. Contiene una hoja, 18 filas contando cabecera y una fila vacía: **16 uniones moleculares**. Solo se normalizan espacios y NBSP y se convierten números enteros, sin modificar el original.

El artículo identifica esta tabla como coordenadas hg38 de las uniones. Al comparar los siete nombres del CSV:

| Campo del CSV | Resultado de enlace literal a S6 |
|---|---|
| UNC13A_annotated |Nombre idéntico, cromosoma/hebra concordantes con referencia|
| STMN2_annotated |Nombre idéntico; S6 informa hebra−, referencia GENCODE v47 informa+|
| STMN2_cryptic |Nombre idéntico; mismo conflicto de hebra|
| UNC13A_3prime |Sin nombre idéntico en S6|
| UNC13A_5prime |Sin nombre idéntico en S6|
| UNC13A_5prime_2 |Sin nombre idéntico en S6|
| UNC13A_5prime_3 |Sin nombre idéntico en S6|

S6 utiliza nombres como NovelDonor, ShortNovelAcceptor y LongNovelAcceptor. No se asignan por el número de filas, por proximidad o suponiendo el significado de un sufijo. Los dos registros STMN2 tienen límites numéricos que se conservan tal como se publicaron, junto con la discrepancia de hebra. **No se corrige silenciosamente la tabla ni se da por plenamente validado el enlace.** La referencia es una proyección molecular de dos genes del GENCODE v47 ya auditado, incluida en esta rama; no depende de fusionar PR28 ni afirma revalidación nueva del GTF completo.

La predicción previa se cumple para los seis enlaces técnicos a ENA, pero **falla para siete correspondencias moleculares completas**: tres nombres exactos, solo uno con hebra concordante, dos conflictos y cuatro alias sin resolver. No se han calculado efectos, PSI, p-valores o rescates funcionales.

## Convención del pipeline

Se inspeccionaron, sin ejecutar, `splicejunction2bed.py` y `parse_star_junctions.smk` del commit `987893efd84a5c5c20ddac9bf33e137c1c6b33ae`. El código ejecutable transforma un intrón STAR inclusivo `(primera, última)` en `(primera−1, última+1)`: son límites flanqueantes, no se asumen intervalos intrónicos BED estándar. Un ejemplo comentado del extremo final difiere del código; se conserva esa diferencia y prevalece la operación ejecutable para describir el software. Eso **no demuestra que el CSV se generara con esa versión exacta**.

La regla de anotación usa intersección con cobertura recíproca completa; no contiene aquí una tabla inequívoca entre los cuatro nombres de UNC13A del CSV y S6. El fichero de definiciones configurado en la máquina del autor no queda recuperado por leer las reglas. Por eso no se interpreta el puente de nombres como resuelto.

## Fuentes, QC y reproducción

Plan previo: `research/plans/2026-10-30-shsy5y-junction-map.md`. Código: `scripts/audit_shsy5y_junction_map.py`. Análisis con el Python del runtime y xlrd2.0.1, sin modificar el XLS. La suite offline usa fixtures stdlib y no necesita xlrd. **183 tests correctos (175 previos + 8 nuevos), compileall correcto.** Pruebas de NBSP/fila vacía, nombres duplicados, enteros inválidos, transformación STAR, sufijo exacto de BAM, condición, permutación de ENA, alias ambiguo y conflicto de condición. Los tests no validan por sí solos los resultados biológicos.

Salidas completas: `S6_molecular_projection.tsv`, `SHSY5Y_library_links.tsv`, `count_field_coordinate_links.tsv`, summary/run JSON y log de pruebas. Solo coordenadas moleculares y metadatos públicos de bibliotecas de cultivo. No tablas clínicas, genotipos, cuentas por paciente ni comunicación externa.

```bash
"$CODEX_PRIMARY_RUNTIME_PYTHON" -m scripts.audit_shsy5y_junction_map \
 --cache data/cache/shsy5y-map \
 --culture data/cache/junction-source-inventory/kd_experiments_relative_rna_and_unc13a_cryptic_junction_counts.csv \
 --reference research/references/target_gene_geometry_v47.json \
 --out reports/shsy5y-junction-map
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

Los hashes de cada XML ENA, TSV de metadatos, XLS, CSV, referencia y scripts inspeccionados están en run.json. Las URLs técnicas y el fallo HTML inicial quedan en sources/errors JSON. La primera respuesta con extensión XLS era HTML, no un libro; se rechazó por sus bytes antes de leer. El original válido se recuperó mediante la clave exacta de un listado público PMC, sin adivinar archivos.

## Siguiente prueba discriminante

Buscar una definición molecular explícita que enlace los cuatro alias UNC13A del CSV con los extremos de las uniones y contraste el conflicto de hebra STMN2. Debe ser un fichero de definiciones o un paso de generación verificable; no otra suposición geométrica. Si no existe en los materiales públicos, conservar esos campos sin enlace completo y no calcular un contraste externo de CE bajo identidad no resuelta. La independencia de las unidades de SH-SY5Y sigue pendiente aunque sus seis runs estén identificados. Sin refit, merge/cierre automático, coste, laboratorio o publicación externa. PR28 permanece separado.

## Referencias

- Brown, A.-L., Wilkins, O. G., Keuss, M. J., et al. (2022). *TDP-43 loss and ALS-risk SNPs drive mis-splicing and depletion of UNC13A*. Nature,603,131–137. https://doi.org/10.1038/s41586-022-04436-3 . Supplementary Table6, métodos y disponibilidad. Fuente XLS: https://pmc-oa-opendata.s3.amazonaws.com/PMC8891020.1/41586_2022_4436_MOESM9_ESM.xls .
- Brown, A.-L., Wilkins, O. G., Keuss, M. J., et al. (2024). *Author Correction*. Nature,631,E7. https://doi.org/10.1038/s41586-024-07577-9 . Corrección de identidad de otra línea conservada en el inventario previo; no se transfieren sus etiquetas a SH-SY5Y.
- ENA PRJEB42763: metadatos de read_run y XML públicos de los seis runs indicados. Se consultaron alias y ficheros depositados, no datos crudos.
