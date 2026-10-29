# Estado actual del proyecto ELA

Actualizado: 29/10/2026. Sustituye los puntos de continuación históricos de las ramas. Consolidación integrada mediante PR #26, merge 2c0ef89207e81194f6d167f4ef3b01929a672f82. Ambas cadenas están incorporadas a main y sus 15 PR originales están cerrados; los dependientes documentan su incorporación mediante #26.

## Pregunta y nivel de evidencia

¿Qué alteraciones de splicing asociadas a pérdida nuclear de TDP-43 resisten controles técnicos y contraste publicado, y qué experimento distinguiría restauración de ARN de recuperación funcional neuronal?

Tenemos auditorías técnicas, observaciones descriptivas y propuestas. No una nueva diana validada, intervención experimental propia o evidencia clínica. Repetir cálculos o cruzar dos series del mismo estudio no crea replicación independiente.

## Resultados ejecutados

| Línea | Evidencia y localización | Límite vigente |
|---|---|---|
| GEO, #1 | reports/geo-audit: 12 bibliotecas, 392871/401720 TXNAME enlazados, cero discordancias de gen | QC técnico; RIN, composición y lecturas crudas no auditados completamente |
| STMN2/UNC13A, #2/#17/#19 | reports/isoforms y reports/mapping-positive-controls: STMN2 4/3 modelos y UNC13A 7/7 cultivo/cerebro; selector ENSG con controles positivos | Modelos asignados, no validación del transcrito completo ni lecturas de cada unión |
| Descriptivos | reports/descriptive y reports/event-reference: sensibilidad a medidas/denominadores y unión conocida STMN2 contrastada | Una biblioteca por condición en cultivo. Etiquetas cerebrales ALS/ALS-ci/ALS-C9 no son estratos cognitivos |
| Metadatos cerebrales | reports/ALS_CI_metadata_correction_2026-10-29.md: corrección agregada 3 CI / 3 no CI / 2 controles | No ampliar datos clínicos personales |
| 21 frente a 1910, #20 | reports/junction-filter-reconciliation: ZIP recuperado; parser consecutivo perdía exones y referencias. 1910 uniones agrupadas; 1901 con soporte asignado positivo en ambas series | Las 21 no forman cribado exhaustivo válido; 3 eran referencia ENST interna |
| GENCODE | reports/gencode-junction-annotation: 17 coincidencias exactas, 1881 no encontradas para el mismo gen y 3 de un gen ausente de v47 | Ausencia no prueba novedad, crypticidad, traducción o función |
| CAMK2B, #15 parcial | reports/camk2b-reproduction: resultado estructural previo reproducido | Ausencia de modelo cerebral no prueba ausencia biológica o de lecturas |
| MEA, #16 parcial | reports/mea-software-audit: 11 tests recibidos y seis contraejemplos; control separado solo sintético | Simulación; validadores/denominadores históricos no habilitados para datos reales |
| Función | reports/functional-evidence, accepted-keuss, chan-timing y reversal-design | Keuss: ASO anterior al KD tardío; Chan incluye ASO inmediatamente poslesión. No certificar originalidad del rescate diferido |
| Imágenes | reports/image-metadata-qc: 27 cabeceras, 4 con escala física; falta mapa de unidades | Sin inferencia grupal o transferencia de calibración por tamaño |
| Otros chats | reports/prior-work-reconciliation: 8 ZIP y 3 PDF inventariados; reproducciones posteriores arriba | GSE126542/GSE121569 y péptidos pendientes de reproducción completa; no sumar cohortes reutilizadas |

## Próximas tareas

1. Base operativa consolidada: partir de main y comprobar su cabeza actual. Las ramas originales son referencias históricas incorporadas, no tareas activas; no reabrir sus PR para repetir trabajo.
2. Suplementos Bolger/crypTE: XML primario y 17 medios inventariados; tablas aún no descargadas/cotejadas. Verificar esquema, ensamblaje, coordenadas, gen/transcrito y evento antes del cruce; un intervalo TE no equivale a un intrón.
3. Revaluar filtros y prioridades sobre catálogo corregido. El cero histórico de intersección estricta no valida el parser defectuoso ni descarta un mecanismo.
4. Reproducir GSE126542/GSE121569 (#14), diferenciando cohortes reutilizadas, diferenciaciones y lecturas de unión. Solo fuentes/proyecciones permitidas, sin filas clínicas personales.
5. Evaluar AGRN (#21) y elegir propuesta funcional (#18) tras contraste estructural y de antecedentes. UNC13A_POST_DEFICIT_PROTOCOL_v0.3.md es propuesta; actualizar su brecha histórica con auditorías Keuss/Chan.

## Bloqueos y restricciones

- Escala par de uniqueCounts sin causa establecida. No dividir por dos ni llamar moléculas a cuentas asignadas. counts, uniqueCounts, fullLengthCounts y CPM no son intercambiables.
- BAM/FASTQ y extremos completos no auditados; un cero o modelo ausente no demuestra ausencia molecular.
- Cultivo y cerebro se analizan por separado, sin p-valores artificiales o función inferida de ARN.
- Sin autorización aplicable: no contactos, publicaciones de resultados, gastos, laboratorio ni datos clínicos personales.

## Operación

Suite conjunta: 105 tests técnicos existentes (85 + 24 menos cuatro compartidos). CI unificada Python 3.11/3.12. Los 11 tests originales MEA son una ejecución histórica separada; no experimentos.

Main es el punto de partida. Usar ramas breves, revisión y pruebas antes de merge. Esta consolidación está autorizada por Luis; no concede autorización general para merges futuros. Las issues no se cierran automáticamente.

Work diario a las 08:00 Europe/Madrid y resumen los viernes. Releer fuentes remotas y comprobar acceso/herramientas en cada ejecución; no hay cómputo continuo garantizado. Informes antiguos conservan contexto/hashes; este estado y MASTER_EVIDENCE.md indican pendientes actuales.


## Fase #14 — reproducción agregada, rama independiente desde main

29/10/2026: reports/issue14-reproduction reproduce63campos agregados (45expresión/18extracciónDEXSeq) sin discrepancias. Fuentes GEO descargadas y fijadas; código recibido conservado sin ejecutar, sin tablas por caso/clínicas/genéticas importadas. STMN2/UNC13A mantienen dirección entre CPM/MR; TARDBP cambia de signo. DEXSeq102fragmentos, no refit niPSI; doce columnas de contraste no son doce diferenciaciones. Nueve tests nuevos sobre105de main:114OK. PR28con166tests sigue separado y no fusionado: contiene originalidad/crypTE/QCglobal posteriores al estado base de main. Leer ambos PR y reconciliar estados al integrar; no declarar esos informes ya incorporados. Issue14no se cierra: próximos BED/RdeFratta, deduplicación/denominadores y mapa de diferenciación121569. Sin nuevas cohortes, hallazgos clínicos, contactos, gasto, laboratorio o merge automático.

## Uniones Fratta auditadas — 29/10/2026, ampliación PR29

reports/fratta-junction-audit: BED/Rmd públicos fijados por SHA256 y Gitblob.241filas→69únicas/172repetidas,16muestras/7pares+2unsorted;27combinaciones ausentes rellenadas con0por método autor, no ceros observados.24campos agregados del paquete concordantes. Rmd2694incluye3clasesUNC13A;2766usa2clases. Cambio medio principal72.67puntos, dosclases72.00, sumar duplicados63.81; no porcentaje molecular, sensibilidad biológica ni nueva cohorte. No se leyeron archivos alélicos/clinica ni exportaron filas por muestra.124tests de esta rama (105base+19nuevos), PR28con166sigue separado. Próximo: mapa técnico biblioteca/experimento-diferenciación deGSE121569 antes de cualquier refit; issue14sigue abierta, sin contactos/laboratorio/gasto/merge.
