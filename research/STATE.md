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
