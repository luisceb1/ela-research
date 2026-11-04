# Backlog vigente — 04/11/2026

Este archivo contiene tareas actuales y condiciones de reapertura. [STATE](STATE.md) resume resultados; el [backlog anterior íntegro](history/README.md) conserva la cronología.

## Ciclo detenido — comprobación del04/11/2026

Ninguna de las dos entradas científicas se recibió en las fuentes acotadas revisadas. La comprobación administrativa distingue aviso de aprobación del dataset, revisión posterior y workspace pendiente; no confirma acceso efectivo o manifiesto. Fig.4d sigue sin respuesta con datos en el hilo/búsqueda revisados. Evidencia y límites: reports/continuity-20261104/REPORT.md.

Se pausa la continuidad automática mientras faltan los archivos concretos. Reanudar tras nueva entrada y decisión; no enviar seguimientos, abrir candidatos o añadir controles equivalentes por defecto. Esta nota no cierra issues ni sustituye sus condiciones de aceptación.

## Continuaciones científicas bloqueadas

| Prioridad | Tarea | Entrada necesaria | Criterio de finalización |
|---|---|---|---|
| 1 | #37: inspeccionar un manifiesto concreto Seddighi–AD Workbench | Fuente nueva con cuentas de uniones o BAM/índices y mapa biblioteca→condición→unidad→lote | Tabla trazable de aceptación/rechazo; solo si cumple cobertura/diseño, redactar prospectivamente un único contraste |
| 1 | #44: K26 Fig.4d: inspeccionar datos originales de eEPSC | Archivo nuevo con valores/unidades, grupos, claves de cultivo/diferenciación y procedencia | Adaptador trazable y revisión del diseño real; habilitar contrato solo tras comprobar independencia, exclusiones y agrupación |

La petición Fig.4d ya fue enviada autorizadamente: [recibo](../reports/functional-rescue-20261103/COMMUNICATION_LOG.md). En la comprobación acotada del 03/11/2026 el hilo contiene solo la petición enviada; no se autoriza seguimiento automático. En la revisión del04/11 aparecen tanto aviso de aprobación del dataset como revisión posterior; el workspace se declara en revisión. No se acredita acceso efectivo ni manifiesto. #37 conserva el [ciclo de búsqueda cerrado](../reports/source-gate-issue37-20261103/REPORT.md); no añadir un cuarto candidato.

Si no hay entrada nueva, registrar que ambas líneas siguen bloqueadas y detener ese ciclo. No crear otra auditoría equivalente, sustituir datos por simulación o cambiar de endpoint para evitar el bloqueo.

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

## Búsqueda manual ampliada de Fig.4d — 04/11/2026

A petición expresa de Luis se amplió la búsqueda pública, sin reactivar la automatización. DataCite:77 registros DOI (incluyen versiones), Zenodo:15 entradas, Figshare:42; también Crossref, Europe PMC/BioStudies, bioRxiv, GitHub y páginas de grupos. No se localizó una tabla original identificable K26 Fig.4d. BioStudies lista solo media-1.pdf del preprint2024; descarga HTTP503, sin inspección de bytes. XML K24 identifica Fig.4d como intensidad UNC13A, no eEPSC espinal. Errores y recuperación incompleta de índices documentados; no se demuestra inexistencia de datos. [Informe y registro](../reports/fig4d-source-search-20261104/REPORT.md).

#44 sigue bloqueada; contrato deshabilitado, sin estimación funcional ni nuevas réplicas. No repetir esta ampliación por defecto: continuar con enlace/archivo original nuevo y revisión del mapa de independencia. #37 y las condiciones previas no cambian. La continuidad automática permanece pausada; sin nuevos contactos, costes, merge o cierre de issues.
