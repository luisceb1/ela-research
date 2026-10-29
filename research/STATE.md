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

## Prioridad expresa: originalidad antes de otras líneas

Auditoría dirigida completada en reports/originality-audit:12familias,8reivindicaciones y133tests técnicos. No tenemos una nueva diana/terapia/mecanismo demostrado. Baughn2023, combinaciónSTMN2/UNC13A2025, Chan2026y CTRsintomático2025limitan reclamos amplios. AGRNsecreción/función ya planteada por revisión2026. La comparación estrecha tras déficit funcional medido sigue no certificada; faltan métodos finales Guo y preprintmotor2026/solapamiento con2025. Próximo cerrar esos límites y reformular propuesta como extensión; antes de otra línea, no reclamar originalidad por búsqueda negativa. MismoPR28abierto, sin merge automático.

## Próximas tareas

1. Base operativa consolidada: partir de main y comprobar su cabeza actual. Las ramas originales son referencias históricas incorporadas, no tareas activas; no reabrir sus PR para repetir trabajo.
2. Suplementos Bolger/crypTE: fuentes recuperadas por PMC AWS, índice y cuatro XLSX verificados; auditoría en reports/author-catalog-schema.42subtablas mapeadas mediante leyendas/xrefs; S12 clínica excluida. S7/S8 auditadas completamente:26815/14525filas no reconstruibles bajo contrato estricto.103592/103599etiquetas S8 reconstruibles son límites exónicos,7excepciones. Cruce del subconjunto reconstruible ejecutado en reports/author-junction-match:284coincidencias S8y70solo contextoS7(354uniones estrictas);278coordenadas con gen ambiguo,74con otro gen,36identidad de referencia no resuelta y1159no encontradas en el subconjunto. No ausencia/novelty ni comparación exhaustiva. Próximo: cobertura excluida y conflictos con fuentes trazables, sin reparar filas por suposición.
3. Revaluar filtros y prioridades sobre catálogo corregido. El cero histórico de intersección estricta no valida el parser defectuoso ni descarta un mecanismo.
4. Reproducir GSE126542/GSE121569 (#14), diferenciando cohortes reutilizadas, diferenciaciones y lecturas de unión. Solo fuentes/proyecciones permitidas, sin filas clínicas personales.
5. Evaluar AGRN (#21) y elegir propuesta funcional (#18) tras contraste estructural y de antecedentes. UNC13A_POST_DEFICIT_PROTOCOL_v0.3.md es propuesta; actualizar su brecha histórica con auditorías Keuss/Chan.

## Bloqueos y restricciones

- Escala par de uniqueCounts sin causa establecida. No dividir por dos ni llamar moléculas a cuentas asignadas. counts, uniqueCounts, fullLengthCounts y CPM no son intercambiables.
- BAM/FASTQ y extremos completos no auditados; un cero o modelo ausente no demuestra ausencia molecular.
- Cultivo y cerebro se analizan por separado, sin p-valores artificiales o función inferida de ARN.
- Sin autorización aplicable: no contactos, publicaciones de resultados, gastos, laboratorio ni datos clínicos personales.

## Operación

Base consolidada:105tests técnicos (85+24menos cuatro compartidos). Las auditorías de suplementos y cruce añaden20tests y esta rama supera125; consultar CI del PR para estado remoto. CI unificada Python3.11/3.12. Los 11 tests originales MEA son una ejecución histórica separada; no experimentos.

Main es el punto de partida. Usar ramas breves, revisión y pruebas antes de merge. Esta consolidación está autorizada por Luis; no concede autorización general para merges futuros. Las issues no se cierran automáticamente.

Work diario a las 08:00 Europe/Madrid y resumen los viernes. Releer fuentes remotas y comprobar acceso/herramientas en cada ejecución; no hay cómputo continuo garantizado. Informes antiguos conservan contexto/hashes; este estado y MASTER_EVIDENCE.md indican pendientes actuales.

## Auditoría de suplementos — entrega para revisión

Acceso resuelto por objetos públicos PMC AWS con MD5/SHA256; no repetir recaptcha como bloqueo universal. Informe y manifiesto en reports/author-catalog-schema y research/references/bolger_author_catalog_v1.json. El método compartido de autores es gen+misma copiaTE, con colapso por categoría; S15 contiene extremos de transcritos, no uniones. S8B/C tiene cabeceras incorrectas y S7D título discordante. El cruce elegible de1901ya se ejecutó; el catálogo completo/tejido no. No inventar cero coincidencias ni interpretar no evaluables como negativos. Ramas nuevas breves desde main; PR de esta auditoría pendiente, sin merge automático.

## Cruce elegible de autores — ampliación del mismo PR28

354claves estrictas:284etiquetas noTE S8y70solo contexto de transcritoTE S7; S7total145incluye75también enS8.353de354no estaban en GENCODEpara mismo gen, pero sí representadas en estas tablas: no son descubrimientos por faltar en referencia. Gen resuelto por símbolo único globalGCv47, sin alias/proximidad. STMN2críptico no evaluable por diez filas S7con bloques inválidos; unión canónica de control recuperada en dos filas S8D. No reparar la lista de longitudes ni llamar ausencia al fallo.125tests locales; tablas idénticas en tres pasadas completas, hashes en reports/author-junction-match/run.json. Misma rama/PR28desde main, sin merge automático. Próximo revisar conflictos y cobertura con GTF/identificadores primarios; si bloqueado pasar a #14.

Actualización de prioridad: los siguientes pasos históricos de cobertura/#14 quedan después del cierre documental de originalidad solicitado por Luis. Informe, registro versionado y límites explícitos en reports/originality-audit;133tests locales.
