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
- [ ] Table S1 del Additional file 1 (46×15, metadatos por caso) **no inspeccionada**. Solo merece abrirse si contiene pérdida de TDP-43 cuantificada por caso, que permitiría discriminar si la coordinación UNC13A–STMN2 es efecto de dosis compartida. Requiere decisión de alcance antes de abrirla.

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
