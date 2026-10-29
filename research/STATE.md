# Estado del proyecto ELA

Fecha de arranque del repositorio: 2026-10-29.

## Pregunta central
¿Qué cambios de splicing asociados a pérdida nuclear de TDP-43 se observan de manera consistente en datasets publicados, y qué experimento distinguiría restauración de ARN de recuperación funcional neuronal?

## Datasets prioritarios
- **GSE310723:** modelos neuronales i3N; secuenciación Iso-Seq.
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310723
- **GSE315972:** tejido cerebral humano Iso-Seq.
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE315972

## Primer inventario técnico realizado (2026-10-29)
- GSE310723: archivo uniqueCounts de 2.568.038 bytes comprimidos; 392.871 filas de transcritos y 4 columnas de condiciones, más TXNAME y GENEID.
- Condiciones etiquetadas: Ctrl ± 5Aza y TDP43KD ± 5Aza; una columna por condición.
- GSE315972: archivo uniqueCounts de 2.862.110 bytes comprimidos; 401.720 filas, 8 columnas de muestras y TXNAME / GENEID.
- Etiquetas de muestras: 2 ALS-C9, 2 ALS-ci, 2 ALS, 2 CTL. **Esto refleja nombres de columna, no verificación de la categorización clínica.**
- Inventario y nombres exactos: `reports/geo-inventory.md`.

## Restricciones
- Una columna por condición en GSE310723; no estimar significación estadística como si hubiera réplicas biológicas.
- No asumir equivalencia entre neuronas i3N cultivadas y tejido cerebral humano.
- Auditar identificadores TXNAME y GENEID contra GTF antes de atribuir isoformas a STMN2/UNC13A.
- `uniqueCounts`, `counts`, `CPM` y otros conteos no son intercambiables.
- No extrapolar observaciones moleculares a efectos clínicos.

## Estado operativo
Inventario estructural y mapeo por IDs de genes ejecutados en GitHub Actions. El run40870066862 recupera11objetivos en cultivo y10en cerebro; la reproducción y controles actuales están en reports/mapping-positive-controls. No confundir selección de transcritos con validación biológica, diferencial o funcional. Las auditorías adicionales de PR3–13y22siguen pendientes de revisión e integración.

## Actualización de auditoría (29-10-2026)
- Se identificó un análisis Iso-Seq externo al repositorio, en `INFORME_CIENTIFICO.md`, que comunica 21 uniones compartidas entre GSE310723/GSE315972, 20 genes y **cero eventos** que superen simultáneamente los filtros preespecificados celular y tejido; **no reejecutado en el repositorio**.
- MAP6D1 y ZNF317 no son candidatos de alta prioridad con la evidencia actual. El primer conjunto presenta un problema de ausencia de cobertura en controles; el segundo no reproduce inducción en i3N tras reducción de TDP-43.
- Informes previos sobre péptidos crípticos, CAMK2B, MEA y auditoría Keuss/Chan están sintetizados en `research/AUDIT_2026-10-29.md`.
- El primer run de mapeo40868865843 produjo0objetivos por dependencia de gene_name; el posterior40870066862 ya recuperó11/10por ENSG con GTF reales. Este estado sustituye la nota histórica de que el mapeo real no se había ejecutado; issue19 documenta el incidente original.
- Bloqueo histórico de aquel entorno: no se pudieron materializar archivos antiguos ni resolver el FTP GEO. Ahora están verificados los cuatro GEO y GENCODEv47; también se recuperó el ZIP original de21uniones, identificado en reports/junction-filter-reconciliation/source_inventory.json.
- Prioridad de investigación: verificar y reproducir el cribado negativo existente, en lugar de repetirlo como investigación nueva. Se mantiene propuesta condicional de estudio UNC13A posterior a déficit funcional documentado, pendiente de laboratorio.

## Actualización científica: 29-10-2026 — AGRN/CAMK2B y control de calidad
- Auditoría de grupos clínicos GSE315972 corregida y reejecutada (GitHub Actions 40872016985): 1910 uniones compartidas bajo filtro amplio, 9 filtro celular, 100 filtro cerebral, **0 intersección estricta**, no validación de ausencia de mecanismo ni reconstrucción exacta del cribado original de 21.
- Nuevo informe: `reports/ALS_CI_metadata_correction_2026-10-29.md`; clasificación ALS-CI n=3, ALS-nonCI n=3 y controles n=2 por GSM/donante.
- Revisión de literatura dirigida: `research/AGRN_CAMK2B_EVIDENCE_2026-10-29.md`. AGRN y CAMK2B tienen antecedentes de eventos crípticos y péptidos; no candidatos nuevos descubiertos aquí.
- AGRN priorizada solo como **pregunta funcional de la unión neuromuscular** por testar; CAMK2B requiere auditoría isoforma-específica. UNC13A conserva la propuesta funcional posdéficit.
- Discrepancia21/1910resuelta en reports/junction-filter-reconciliation: parser consecutivo original pierde exones y referenciasENST. Su lista21no es cribado exhaustivo válido. El catálogo agrupado reproduce1910, con1901de soporte positivo; no equivale a novedad o validación biológica.

## Reconciliación técnica con ramas de investigación — issue19
- Corrección ENSG ya existente confirmada en logs y reproducción local:392871/401720TXNAME enlazados,11/10objetivos; STMN2=4/3yUNC13A=7/7. gene_name ausente en todos los TXNAME de ambas matrices; no ausencia biológica.
- Panel GENCODEv47 fijado por hash y recontrastado. Nuevos controles de selección positiva/identidad/valores; test sin gene_name ahora se descubre; fallo explícito y escritura atómica ante salida inválida.16tests de este main pasan; no son la suite85de la ramaMEA.
- TSV iguales a la selección de main anterior y concordantes con IDs/exones/sumas de PR4. No fusionar estados ni omitir informes de PR3–13/#22, que continúan pendientes.
- Siguiente: issue20, ZIP original y filtros21vs1910, con metadatos publicados ya corregidos en main. Sin nueva inferencia biológica, cierre automático de issues o merge.

## Issue20: fuente recuperada y causa estructural reproducida
- ZIP15185bytes/SHA25673edc0006287f355001f968ce12f54d38a148535c05f7195f2db83e636215393; siete miembros verificados. Se reproducen21claves exactas con funciones originales, sin exportar cuentas por persona.
-9403/16321modelos Bambu ENSG presentan varios bloques de exones; el parser original sobrescribe bloques y solo conserva278/682modelos con unión, frente a9527/16633agrupando todos sus exones. No es principalmente un filtro de expresión.
- Catálogo noENST compartido1910(1255genes); soporte positivo en ambas series1901(1250genes). De21antiguas,18permanecen y3sí están en referenciasENSTinternas. Excluir cuentas0solo elimina9del catálogo, no explica21.
- Proyección segura21claves y cuatro funciones por hash permiten repetir desde GitHub+GEO sin ZIPprivado; el JSON distingue verificación opcional del original.20tests en esta rama. No pvalores, traducción, novedad ni evidencia terapéutica.
- Siguiente: GENCODEv47completa/catálogo publicado de origen para1901claves, antes de priorizarAGRN(#21)u otras dianas. #19/#20pendientes de revisión, sin cierre/merge automático.
