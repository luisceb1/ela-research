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

## Ciclo Work — 2026-10-29: auditoría #1 (pendiente revisión)

- Auditoría técnica completa de 12 bibliotecas GSM y 6 archivos de datos, con manifiesto SHA256, diccionario y QC en `reports/geo-audit/`.
- Enlace exacto de los 392.871 / 401.720 TXNAME al GTF de cada serie: cero ausentes, cero genes discordantes, cero IDs duplicados. `uniqueCounts <= counts` en todas las celdas; counts contiene valores fraccionarios.
- La serie cerebral informa ocho muestras de donante; las etiquetas ALS-C9 mezclan clasificación cognitiva. No tratar los cuatro grupos como estratos homogéneos ni los cultivos sin réplicas como replicados.
- Estado: listo para revisión técnica en PR, sin validación funcional ni inferencia clínica. Límites biológicos y de metadatos en `reports/geo-audit/REPORT.md`.
- Siguiente tarea segura: #2, mapeo por serie y verificación externa GENCODE v47 según `research/plans/2026-10-29-isoforms.md` (el plan y los resultados de #2 se entregarán en PR dependiente).
- Work: tarea diaria creada, mañana ~08:00 Europe/Madrid; incluye resumen de siete días cuando sea viernes. No se pudo crear una segunda tarea por límite de cinco activas. La ejecución futura debe comprobar herramientas/acceso cada vez; no hay garantía de cómputo continuo entre ejecuciones.

## Ciclo Work — mapeo #2 (pendiente revisión)

- Informe y tablas: `reports/isoforms/`; plan previo: `research/plans/2026-10-29-isoforms.md`. Referencia oficial GENCODE v47 descargada y fijada por hash; símbolos STMN2/UNC13A y controles ACTB/GAPDH verificados.
- STMN2: 4 transcritos en cultivo (3 ENST + BambuTx9249), 3 ENST en cerebro. UNC13A: 7 ENST en cada catálogo; solo 3 con cuenta única positiva por serie.
- BambuTx9249: cadena de dos exones y unión no anotada en GENCODE v47; etiqueta críptica NO validada. No aparece en el GTF cerebral asignada a STMN2. Cero otros transcritos de distinta asignación en la misma hebra que solapen los loci diana, según control del catálogo.
- Diez cadenas ENST compartidas reflejan anotación común y no validación de expresión independiente. No hay demostración de rescate funcional.
- PR #3 de auditoría: CI offline de GitHub completada con éxito. Mapeo: 25 pruebas offline pasan.
- Siguiente tarea segura seleccionada: P1 descriptivo de GSE310723 y sensibilidad de GSE315972, según plan `research/plans/2026-10-29-descriptive.md` (entrega en PR posterior).

## Ciclo Work — P1 descriptivo y sensibilidad (pendiente revisión)

- `reports/descriptive/` contiene 132 contrastes de cultivo y 180 filas de sensibilidad cerebral. Son cálculos, no réplicas. `scripts/describe_targets.py` ejecutado dos veces; tablas idénticas por SHA256; 30 pruebas offline pasan.
- Patrón STMN2 candidato/ENST principal de dirección consistente bajo medidas y denominadores examinados en cultivo; sin p-valores ni replicación independiente. BambuTx9249 sigue sin atribución críptica validada.
- UNC13A ENST principal cambia de dirección con counts/uniqueCounts en cultivo sin 5Aza y en cerebro ALS/CTL; en este último, los rangos al retirar bibliotecas cruzan 1. Resultado negativo de robustez registrado.
- GCD=2 en cada columna de uniqueCounts de ambas series. Causa no verificada; conservar unidades y no interpretar como moléculas independientes.
- PR #4 de mapeo: CI offline exitosa; depende del PR #3. Ningún PR fusionado ni issue cerrada.
- Siguiente tarea segura: coordenadas independientes del candidato STMN2 y semántica/escala de uniqueCounts; si bloqueada, evidencia funcional publicada. Mantener PR pendientes como parte del estado al reanudar la tarea Work diaria.

## Punto de continuación persistente

- PR abiertos y encadenados: #3 → #4 → #5. CI `unit-tests` completada con éxito en los tres. Revisar en ese orden; sin fusión ni publicación pública de hallazgos.
- Los 49 archivos nuevos/modificados de la entrega se verificaron contra los blobs almacenados en GitHub. Tres documentos iniciales de la instantánea local diferían solo por salto de línea final respecto a sus originales remotos; AGENTS.md y PROTOCOL.md se conservaron intactos en GitHub.
- Para reanudar sin perder estado, usar la rama `research/descriptive-sensitivity-20261029` hasta que sus PR se integren; main todavía no incluye estos análisis.
