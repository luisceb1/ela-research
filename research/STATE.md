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
Inventario estructural GEO completado por primera ejecución de GitHub Actions. Aún no se ha auditado la calidad biológica, ni realizado análisis diferencial ni validación independiente.

## Actualización de auditoría (29-10-2026)
- Se identificó un análisis Iso-Seq externo al repositorio, en `INFORME_CIENTIFICO.md`, que comunica 21 uniones compartidas entre GSE310723/GSE315972, 20 genes y **cero eventos** que superen simultáneamente los filtros preespecificados celular y tejido; **no reejecutado en el repositorio**.
- MAP6D1 y ZNF317 no son candidatos de alta prioridad con la evidencia actual. El primer conjunto presenta un problema de ausencia de cobertura en controles; el segundo no reproduce inducción en i3N tras reducción de TDP-43.
- Informes previos sobre péptidos crípticos, CAMK2B, MEA y auditoría Keuss/Chan están sintetizados en `research/AUDIT_2026-10-29.md`.
- Pruebas unitarias del script `scripts/map_isoseq_gtf.py` superadas en GitHub Actions (run 40868184532); **no se ha ejecutado el mapeo con GTF reales**.
- Bloqueo comprobado: los archivos antiguos de la biblioteca no pudieron materializarse como bytes para reejecución local; tampoco hubo resolución DNS para el FTP público GEO en el entorno de ejecución.
- Prioridad de investigación: verificar y reproducir el cribado negativo existente, en lugar de repetirlo como investigación nueva. Se mantiene propuesta condicional de estudio UNC13A posterior a déficit funcional documentado, pendiente de laboratorio.

## Actualización científica: 29-10-2026 — AGRN/CAMK2B y control de calidad
- Auditoría de grupos clínicos GSE315972 corregida y reejecutada (GitHub Actions 40872016985): 1910 uniones compartidas bajo filtro amplio, 9 filtro celular, 100 filtro cerebral, **0 intersección estricta**, no validación de ausencia de mecanismo ni reconstrucción exacta del cribado original de 21.
- Nuevo informe: `reports/ALS_CI_metadata_correction_2026-10-29.md`; clasificación ALS-CI n=3, ALS-nonCI n=3 y controles n=2 por GSM/donante.
- Revisión de literatura dirigida: `research/AGRN_CAMK2B_EVIDENCE_2026-10-29.md`. AGRN y CAMK2B tienen antecedentes de eventos crípticos y péptidos; no candidatos nuevos descubiertos aquí.
- AGRN priorizada solo como **pregunta funcional de la unión neuromuscular** por testar; CAMK2B requiere auditoría isoforma-específica. UNC13A conserva la propuesta funcional posdéficit.
- Bloqueo pendiente: acceso al ZIP original del cribado de 21 uniones y reproducción exacta de filtros; no fusionar 21 y 1910 como si provinieran del mismo algoritmo.
