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

## Ciclo Work — unión conocida y soporte full-length

- `reports/event-reference/` y `scripts/check_event_reference.py`: una coincidencia exacta de unión STMN2 con Figura 5 de Grima et al. 2025, DOI 10.1186/s13024-025-00820-5, GRCh38. Hebra + tomada por separado de GENCODE v47; el pie no especifica hebra.
- BambuTx9249 contiene una unión críptica **ya conocida**; no se presenta como descubrimiento de nueva unión. Extremo 3′/transcrito completo/poliadenilación sin validar.
- FullLengthCounts del candidato 0/0 en controles y 8/12 en KD, frente a uniqueCounts 4/0 y 10/24. Son estimaciones del mismo experimento, no lecturas independientes verificadas.
- Cuatro matrices por serie: IDs/columnas coinciden; cero violaciones unique<=counts o fullLength<=counts (tolerancia 1e-4). CPM real usa otro denominador; no revierte dirección STMN2 en cultivo.
- Código exacto bambu 3.2.6 fijado a commit 2fb886442096896807f44191ad2d1e00b43ceadd. Exportación sin factor2 explícito; paridad sigue sin causa establecida. R no ejecutado. Bloqueo e incidencias documentados, sin modificar escala original.
- 37 pruebas offline pasan. Siguiente tarea segura seleccionada: evidencia funcional publicada, con separación ARN/proteína/función, temporalidad y controles.

## Auditoría funcional — siguiente ciclo
- reports/functional-evidence: cinco unidades curadas, sin contarlas como estudios independientes. Código de validación ejecutado; 41 pruebas pasan.
- Keuss2024 neuronal: ASO inicia junto a PROTAC; no verifica rescate diferido tras basal deficitario. Otro preprint2025 inicia ASO antes de shRNA.
- Baughn2023: resumen respalda función celular; cronología completa bloqueada HTTP500. Keuss2026 aceptado: registro verificado, PDF HTTP403; no transferir calendario del preprint a la versión aceptada.
- Próxima tarea segura: recuperar manuscrito aceptado y auditar figuras/calendario; especificar contraste de rescate diferido sin iniciar laboratorio. Estado completo en rama research/functional-evidence-20261029, dependiente del PR6.

## Manuscrito aceptado Keuss: bloqueo de lectura resuelto con copia del usuario
- reports/accepted-keuss: portada peer-reviewed/registro institucional cotejados; no igualdad de bytes con endpoint público403. Lectura de métodos/resultados y Table6 con páginas explícitas.
- MEA: ASO desdeDIV14, KD tardíoDIV33. Tratamiento19días antes de la perturbación; no rescate diferido. Autapsis espinales: corrector y gapmer concurrentesDIV45.
- Recuperación de liberación en sinapsis restantes no restituye densidad sináptica. Conflicto de la fila de imagen Table6 conservado sin adjudicar calendario.
- 45 pruebas offline pasan; tabla manual y cálculo reproducible. Siguiente: localizar datos públicos de tratamiento diferido; en su ausencia ficha de colaboración sin envío. Rama research/accepted-keuss-timeline-20261029.

## Diseño discriminante de reversión
- PNAS2025 PMC12130871 Fig7: expresión3días antes de lesión en fondo STMN2 nulo; distinguir lesión de inicio de deficiencia genética. XML/hash y extracción en reports/reversal-design.
- EXPERIMENT_SPEC.md: contraste concurrente/diferido, control temporal, viabilidad, acción molecular/proteica y dependencia por diferenciación; sin cifras simuladas ni laboratorio.
- Misma unidad longitudinal preferible para MEA, no requisito universal: cohortes paralelas comparables pueden establecer rescate.
- 48 pruebas locales pasan. Próximo: inventario Zenodo15346391 y reanalizabilidad; si bloqueado modelo humano2026 DOI10.1038/s42003-026-10832-6. Rama research/reversal-design-20261029.
- Inventario Zenodo ejecutado:100archivos/15.009.420.706bytes;27imágenes Figure7 en9seriesnominales0/24/48h. No son9réplicas biológicas verificadas; artículo declara2diferenciaciones. Imágenes no descargadas. Próximo resolver unidad/escala/metadatos antes de medir efectos.

## TIFF y hoja de Figure7 auditados
- reports/image-metadata-qc:27cabeceras/1.769.472bytes por HTTP206; todas27740×7940/16bit. Solo4con escala0,325µm/píxel;23sin resolución física;0con fecha TIFF. No hay triplete completamente calibrado.
- RawData.xlsx verificado por MD5; Figure7 tiene conteos distintos de longitudes24/48 y carece de IDs para enlazar axón/imagen/diferenciación. Dos diferenciaciones según artículo; no transformar nueve etiquetas ni cientos de longitudes en réplicas.
- Calibración no transferida por igualdad de tamaño; sin efectos biológicos ni p-valores.59pruebas locales pasan. Originales fuera de git.
- Próximo: suplemento por otra fuente pública e inspección visual de par calibrado, verificar registro/orientación antes de segmentar. Inferencia grupal sigue bloqueada por correspondencia experimental. Rama research/image-metadata-qc-20261029.
