# Current backlog — 2026-11-04

Este archivo contiene tareas actuales y condiciones de reapertura. [STATE](STATE.md) resume resultados; el [backlog anterior íntegro](history/README.md) conserva la cronología.

## Continuaciones científicas bloqueadas

| Prioridad | Tarea | Entrada necesaria | Criterio de finalización |
|---|---|---|---|
| 1 | #37: inspeccionar un manifiesto concreto Seddighi–AD Workbench | Fuente nueva con cuentas de uniones o BAM/índices y mapa biblioteca→condición→unidad→lote | Tabla trazable de aceptación/rechazo; solo si cumple cobertura/diseño, redactar prospectivamente un único contraste |
| 1 | #44: K26 Fig.4d: inspeccionar datos originales de eEPSC | Archivo nuevo con valores/unidades, grupos, claves de cultivo/diferenciación y procedencia | Adaptador trazable y revisión del diseño real; habilitar contrato solo tras comprobar independencia, exclusiones y agrupación |

The K26 request and separate A25 support message have already been sent with authorization; no new follow-up is authorized. The administrative audit records mixed approval/review notices and a pending workspace, not effective data access. [Current state](STATE.md), [administrative evidence](../reports/continuity-20261104/REPORT.md), [K26 search](../reports/fig4d-source-search-20261104/REPORT.md).

Si no hay entrada nueva, registrar que ambas líneas siguen bloqueadas y detener ese ciclo. No crear otra auditoría equivalente, sustituir datos por simulación o cambiar de endpoint para evitar el bloqueo.

## Entradas del 10/11/2026

Confirmado por Luis: sin archivo K26 y sin acceso AD Workbench. Las dos líneas prioritarias (#37, #44) siguen bloqueadas por sus entradas ya registradas; sin seguimiento automático.

- [x] **Curación de las 14 filas** ejecutada por el agente (Luis lleva el proyecto por interés personal, no como técnico). Citas verificadas literalmente 14/14 con `scripts/verify_matrix_quotes.py`; cuatro fallos encontrados y corregidos, incluido un bug del propio verificador y tres citas unidas con elipsis. Ver [CURATION](../reports/unc13a-intervention-timing-20261110/CURATION.md).
- [ ] **Revisión independiente** (la curación no lo es: mismo lector). Pendiente solo para la fila **M-a** y para mi definición de «déficit basal». Vías sin coste: esperar la revisión por pares de Mallika/Cao; o un comentario público en bioRxiv, que **requiere autorización expresa de Luis** y lo firmaría él. No hay gasto propuesto.
- [x] Métodos de Mallika (PMID 42779622) y Cao (PMID 42779638): **resueltos el 10/11** con los PDF aportados por Luis, tras agotar las dos vías públicas (Europe PMC `PPR1322482`/`PPR1319997` con `inEPMC N`; bioRxiv con error 1015 de Cloudflare, sin falsear el cliente). Matriz completa a 6/6 fuentes. Verificado: ambos preprints son del mismo laboratorio (Wong, Johns Hopkins; 6 autores compartidos), luego no son replicaciones independientes entre sí. El PDF de Cao es `cc_no`: no se versiona ni se redistribuye.
- [ ] Comprobar si la versión revisada por pares de Mallika o Cao modifica cronologías o tamaños de grupo, antes de usar la matriz para cualquier diseño.
- [x] Revisar PMID 42983891 contra la puerta de #37: **rechazada** como fuente técnica (qRT-PCR/ddPCR post mortem, sin cuentas de uniones). Conservada como contexto. No abre un cuarto candidato.
- [x] Acotar a TITLE_ABS la consulta `long_reads` del vigilante diario, con pruebas de alcance de campo.

La laguna que motiva #18 queda documentada en su forma **precisa**: ninguna corrección *específica de UNC13A* probada tras un déficit funcional medido (0 de 9), mientras la restauración *multidiana* posdéficit sí rescata función en ratón (Mallika, CTR). Eso **no** autoriza ningún ensayo: seguiría exigiendo déficit medido antes de la primera dosis, unidades independientes verificables y autorización específica. No tratar el rescate multidiana como evidencia a favor de una diana aislada: no hay control factorial.

## Entradas del 10/11/2026 (tarde)

- [x] Replay descriptivo de los datos fuente de Ikegami/Koike 2026: R1–R4 reproducidos, con control de permutación y descarte de la duración de enfermedad como explicación. Ver [informe](../reports/ikegami-source-replay-20261110/REPORT.md). Reproducibilidad interna, **no** replicación; sigue sin aportar cuentas de uniones y **no reabre #37**.
- [x] Vigilante diario ampliado para detectar versiones revisadas por pares de los 6 preprints seguidos, con pruebas. Primer hallazgo real: Guo publicado en *Sci Transl Med* (PMID 42234776).
- [ ] **Métodos de Guo revisado por pares**: de pago y sin registro PMC. Las filas G-a/G-b de la matriz siguen atribuidas al preprint de 2025. Entrada necesaria: acceso legítimo al texto publicado. No reintentar por continuidad.
- [x] Table S1/S2 inspeccionadas: **no** contienen carga de pTDP-43 por caso, luego la prueba discriminante de H2 no es ejecutable con esta fuente. Cribado de confusores entre subtipos ejecutado: RIN, PMI y pérdida neuronal no difieren; la duración sí (32/19/11 meses); la edad de inicio solo nominalmente. Enlace por caso rechazado por clave no única en Tipos 2a y 2b.
- [ ] **Entrada necesaria para H2**: una fuente con carga de pTDP-43 cuantificada por caso junto a ambos marcadores, o una cohorte que desacople intensidad de patología y velocidad de progresión. No buscar por continuidad: requiere decisión de alcance.

## Entradas del 11/11/2026

- [x] Vía Snaptron/recount3 intentada para las uniones crípticas de UNC13A. **Bloqueada por TLS**: el túnel CONNECT se establece tras permitir el host, pero la cadena del certificado del servidor no verifica ni aportando el CA del proxy, y no se desactiva la verificación. **La pregunta de viabilidad queda sin responder, no refutada.** Ver [informe](../reports/snaptron-unc13a-feasibility-20261111/REPORT.md).
- [x] **Ciclo recount3 ejecutado.** La vía funciona: cuentas de uniones para depleción de TDP-43 en neuronas humanas, 24,5 MB, coste cero, condiciones declaradas. **SRP166282 (Klim 2019) rechazado por cobertura**: máximo 5 lecturas crípticas frente a ≥20, con control positivo canónico superado. Sonda reutilizable en `scripts/recount3_junction_probe.py` con 7 pruebas. Ver [informe](../reports/recount3-unc13a-20261111/REPORT.md).
- [x] **SRP334561 (Ma 2022) probado y NO elegible**: cobertura altísima (57.709) y el mejor diseño (3 líneas de donante), pero es **amplicón dirigido** de exón 19→21, etiquetado como `RNA-Seq` en SRA. Verificado contra el artículo, como exigía el plan. Reproduce el hallazgo cualitativo publicado; no habilita el contraste de #37. Detector `assay_shape()` añadido a la sonda con pruebas.
- [x] **Brown 2022 descartado desde su declaración de datos**: todo lo que depositó es dirigido u otro ensayo (Riboseq, RNA-seq dirigido, 2× iCLIP, nanopore dirigido); de lo reutilizado, GSE121569 = SRP166282 ya rechazado, y GSE126543 (cortical) no tiene registros SRA.
- [x] **#37 REORIENTADA** (autorizado 11/11): arbitrar la discrepancia. Resultado: **las dos cifras no son comparables** (Ma es amplicón confirmado por dos vías: un gen = 100 % de cuentas, fragmento 1.508 pb). Knockdown de Klim medido: **58,8 %** de reducción de TARDBP. El de Ma **no declarado** en el texto accesible y no estimable de un amplicón. Predicción prefijada **no comprobable**. Ver [informe](../reports/unc13a-fraction-discrepancy-20261111/REPORT.md).
- [ ] **Entrada necesaria para #37, criterios actualizados**: (1) RNA-seq de transcriptoma completo, (2) **eficacia de depleción documentada**, (3) profundidad suficiente en UNC13A (≈200 lecturas canónicas si la fracción ronda 0,10), (4) ≥3 unidades biológicas independientes por condición. El criterio 2 es **nuevo**: sin él, una fracción baja no se distingue de un knockdown débil.
- [ ] El umbral de 20 **no se ha modificado**; su aplicación como criterio de aceptación queda suspendida hasta disponer de una fracción fiable.
- [ ] ~~DECISIÓN DE ALCANCE PARA LUIS~~: la discrepancia de 4–5× en la fracción críptica entre Klim (RNA-seq, 0,000–0,145) y Ma (amplicón, 0,390–0,690) determina si el umbral de 20 es alcanzable en RNA-seq público. ¿Reorientar #37 a resolver esa discrepancia, o seguir buscando datasets más profundos? **El agente no cambia el umbral ni la pregunta por su cuenta.**
- [x] **Hipótesis cortical PROBADA en parte y apoyada**: en corteza motora de TARGET_ALS la cobertura canónica de UNC13A es 2–3× la de motoneuronas espinales (mediana 102–148 frente a 7–66). Separación cualitativa limpia: 23/109 ELA con lecturas crípticas, 0/17 no-ELA. **P1 refutada**: 0/149 alcanzan ≥20. Ver [informe](../reports/target-als-cortex-20261111/REPORT.md).
- [x] **Córtex frente a médula cervical ejecutado**, con el diseño corregido tras revisión externa. Profundidad **idéntica** (44,4 M en ambos), y **21× menos cobertura de UNC13A en médula**. P1/P2/P3 confirmadas. Explica por qué fallaron el piloto y Klim: eran médula espinal. Ver [informe](../reports/target-als-cervical-20261111/REPORT.md).
- [x] **Puerta de cobertura: búsqueda cerrada** por falta de precisión **con los datos examinados** (cinco datasets). No se afirma nada sobre todo el RNA-seq público. **No proponer otro dataset de transcriptoma completo para esta pregunta.**
- [x] **Ciclo STMN2 ejecutado: UMBRAL SUPERADO.** 4 muestras ELA en médula cervical con 21–52 lecturas crípticas (PSI 0,148–0,544). Detección 48/95 frente a 1/13 controles, Wilson sin solapar. El fracaso con UNC13A era **del locus**, no del método. Coordenadas derivadas con ancla doble (desplazamiento 912.235 concordante) y selladas. **Mi criterio `annotated=0` era erróneo**: la unión verdadera está `annotated=1`; cinco candidatas `annotated=0` pasaban todas las verificaciones estructurales y ninguna es el evento publicado. Ver [informe](../reports/stmn2-derivation-20261111/REPORT.md).
- [x] **Coordenadas de UNC13A auditadas y CONFIRMADAS** con ancla doble: 88/88 límites exónicos dan el mismo desplazamiento (110.809), y el intervalo publicado derivado coincide **exactamente** con el exón críptico implicado. Sin cambios; **ninguna medición de la semana queda afectada**. Ver [informe](../reports/unc13a-coordinate-audit-20261111/REPORT.md).
- [x] **Lección registrada en ambos archivos sellados:** el indicador `annotated` de recount3 es **inconsistente entre genes** (UNC13A `0`, STMN2 `1`) y no sirve como criterio en ninguna dirección. El criterio válido es el cruce con intervalo publicado vía ancla doble.
- [ ] ~~Revisar las coordenadas selladas de UNC13A~~ Su derivación es anterior y su supuesto de `annotated=0` pudo ser igualmente erróneo. Barato y podría cambiar lo que medimos.
- [x] **Coordenadas de STMN2 auditadas y CONFIRMADAS** en cinco comprobaciones: mismas coordenadas en ambos tejidos; **exón críptico terminal validado empíricamente** (ninguna unión desde su extremo 3′ en 313 muestras), lo que valida el denominador del PSI; candidatas rechazadas con 1–2 lecturas; y de 50 uniones del locus, **ninguna no anotada pasa de 9 lecturas**, así que la sellada domina por ~50×. El código de anotación `cH38` queda **sin resolver y sin adivinar**. Ver [informe](../reports/stmn2-coordinate-audit-20261111/REPORT.md).
- [ ] **Contraste STMN2 ELA frente a control en médula cervical**: ahora es planteable con cobertura suficiente, pero exige resolver unidades biológicas independientes (los metadatos no dan donante) y prefijar un único contraste. No calcular ningún efecto antes.
- [ ] Continuación para **UNC13A**: **enriquecimiento celular** (núcleos clasificados por TDP-43, tipo GSE126543, sin registros SRA alcanzables). Requiere otra ruta de acceso y decisión de alcance.
- [ ] ~~Ciclo siguiente: córtex frente a médula en la MISMA cohorte~~ (`TALS_Spinal_Cord_Cervical/Lumbar/Thoracic`). Es el contraste más limpio de H1 disponible, controlando cohorte y tubería. ~200 MB por tejido, plan propio.
- [ ] **Decisión pendiente sobre la puerta de cobertura de #37**: la aritmética de este ciclo indica que ≥20 exige **enriquecimiento celular** (núcleos clasificados por TDP-43, tipo GSE126543) o ensayo dirigido, no más n ni más profundidad. Si el ciclo de médula lo confirma, lo honesto es cerrar esa puerta como inalcanzable con RNA-seq público de transcriptoma completo.
- [ ] ~~Hipótesis cortical: SIGUE SIN PROBAR~~ Los dos datasets probados son de motoneuronas. Entrada necesaria: dataset de depleción de TDP-43 en neuronas corticales o i3Neurons con RNA-seq de transcriptoma completo (no amplicón). Candidatos no agotados: datos propios de Brown 2022 en ArrayExpress (`E-MTAB-11243`/`11244`), que habría que localizar en ENA/SRA.
- [ ] ~~Siguiente candidato recount3~~: dataset de depleción de TDP-43 en **neuronas corticales o i3Neurons**, donde UNC13A se expresa más que en médula espinal. Aplicar la sonda ya construida. Criterio de parada: si dos o tres datasets corticales profundos tampoco alcanzan ≥20, se cierra la vía recount3 para esta pregunta.
- [ ] `ANSWER_ALS` y `TARGET_ALS` están en recount3 pero son **cohortes de pacientes, no experimentos de depleción**. Usarlas responde otra pregunta y exige plan nuevo. No cambiar de endpoint para esquivar el rechazo por cobertura.
- [ ] ~~Decisión de alcance pendiente~~: abrir o no un ciclo sobre el almacén de archivos de recount3, distinto de la API de Snaptron. El plan prefijado prohibía perseguir rutas alternativas por continuidad, así que requiere autorización explícita y plan propio. Criterio de parada: si no se puede consultar por región sin descargas desproporcionadas, se cierra la vía recount3 completa.
- [ ] **Borrador de mensaje a laboratorio: redactado y NO enviado.** Requiere autorización expresa y lo firmaría Luis. Ver [borradores](drafts/2026-11-11-borradores-pendientes-de-autorizacion.md).
- [ ] **Estructura de comentario/preprint: redactada y NO publicada.** Espera revisión independiente de la fila M-a o la versión revisada por pares de Mallika/Cao. Publicar es irreversible.
- [ ] El repositorio es **privado**: la URL del borrador de contacto no funcionaría para un tercero sin cambiar eso. Decisión de Luis.

## Corrección del 11/11/2026 (tarde)

- [x] **P1 del ciclo STMN2 estaba mal etiquetada: era REFUTADA, no confirmada.** Umbral prefijado ≥10×; resultado 6,6×. Detectado por el segundo lector de la rama de la PR #57, verificado y corregido en el informe y en STATE. **P2 (umbral superado) y P3 no se ven afectadas**, ni las coordenadas ni la auditoría.
- [x] **Discrepancia informe/JSON documentada:** `results_cervical.json` contiene resúmenes `by_group` sin la restricción de denominador ≥20 que sí aplica el informe (n=92 frente a 58). Usar las cifras del informe.
- [ ] Revisar si otros informes propios declaran confirmada alguna predicción por debajo de su propio umbral. **No se ha hecho esa revisión sistemática.**

## Mantenimiento técnico

- [x] Separar estado/backlog actuales del historial íntegro.
- [x] Documentar scripts históricos y puntos de entrada acotados.
- [x] Hacer visibles pruebas ejecutadas/omitidas y exigir cero omisiones en la suite completa de CI.
- [x] Separar lectura, validación de células y diseño en el validador Fig.4d, conservando contrato, CLI y motivos de rechazo.
- [x] Validar el CSV de Fig.4d sobre los mismos bytes usados para SHA256 y rechazar cabeceras duplicadas, con controles de sustitución del archivo y compatibilidad de formato.
- [x] Revisar issues históricas: #19 cerrada como resuelta, #17 consolidada como duplicada de #2; #1/#2/#14/#20/#37 mantienen bloqueos explícitos. Las propuestas #15/#16/#18/#21 se conservan en la tabla de líneas futuras y se cierran como no planificadas actualmente; #44 sigue la reproducción Fig.4d ya aprobada.
- [ ] Cuando una nueva tarea aceptada necesite transporte/ejecución: extraer módulos comunes de transporte, presupuesto, reloj y supervisión; definir configuración explícita y conservar ejecutores históricos sin cambiar sus hashes. Comparar recibos/salidas en fixtures antes de adoptar el nuevo ejecutor.
- [x] Consolidar los trabajos CI redundantes en una matriz completa Python 3.11/3.12 con PySAM/PyArrow fijados, compilación e informes. Los nombres de checks anteriores dependen de esa matriz y propagan su resultado sin repetir pruebas.

## Líneas diferidas y reglas de parada

Las propuestas siguientes quedan aparcadas, con sus issues cerradas como `not_planned` por prioridad actual. El cierre no acredita validación científica ni descarta las hipótesis; se conserva toda la evidencia y el historial.

| Idea futura | Evidencia ya documentada | Condición para reconsiderarla |
|---|---|---|
| CAMK2B, #15 | Reproducción estructural; sin validación genética/proteómica independiente | Fuente primaria nueva con identidad de evento y soporte independiente verificables; pregunta y controles prospectivos |
| MEA, #16 | Auditoría del software sintético ejecutada; sin ensayo funcional propio | Registros funcionales reales, unidades independientes y cronología/basal verificables; no otro simulador como evidencia |
| UNC13A posdéficit v0.4, #18 | Protocolo conceptual y auditoría dirigida de antecedentes | Datos con déficit funcional medido antes de primera dosis, controles temporales y unidades verificables; ensayo nuevo solo con autorización específica |
| AGRN, #21 | Antecedente conocido y pregunta de isoforma, sin ensayo propio | Identidad exacta y soporte de lecturas, revisión de antecedentes y pregunta/controles definidos antes de cualquier ensayo autorizado |

Los bloqueos antiguos #1/#2/#14/#20 siguen abiertos por sus entradas concretas pendientes, sin tareas ejecutables por defecto. Las únicas continuaciones científicas priorizadas son #37 y #44. No reabrir propuestas o búsquedas cerradas sin una fuente nueva y una decisión de alcance.

No repetir STMN2/PPAU 12/12, el piloto UNC13A cerrado, Humphrey procesado o búsquedas agotadas como trabajo nuevo. No relajar cobertura 20, promover bibliotecas técnicas a réplicas ni sumar uniones ajenas al objetivo.

No nuevas descargas masivas, control completo/TDP, contactos, gastos, datos personales, laboratorio o publicación externa por continuidad automática. [AGENTS](../AGENTS.md) y [PROTOCOL](PROTOCOL.md) siguen aplicando.

## Completed user-authorized extensions

A25 Fig.3s descriptive replay and UNC13A Dox replay are complete; see STATE.md. Missing culture identities and molecular metadata do not become new searches by default. ELK1 final-paper archive reconciliation is complete and integrated with its molecular replay; see STATE.md. No further ELK1 intervention program is scheduled. No new equivalent audit is scheduled. A new source file and prospective design review are needed before inference. The scheduled one-time Fratta publication check does not reactivate broad research continuity.
