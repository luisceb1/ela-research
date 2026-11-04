# Backlog vigente — 04/11/2026

Este archivo contiene tareas actuales y condiciones de reapertura. [STATE](STATE.md) resume resultados; el [backlog anterior íntegro](history/README.md) conserva la cronología.

## Continuaciones científicas bloqueadas

| Prioridad | Tarea | Entrada necesaria | Criterio de finalización |
|---|---|---|---|
| 1 | #37: inspeccionar un manifiesto concreto Seddighi–AD Workbench | Fuente nueva con cuentas de uniones o BAM/índices y mapa biblioteca→condición→unidad→lote | Tabla trazable de aceptación/rechazo; solo si cumple cobertura/diseño, redactar prospectivamente un único contraste |
| 1 | #44: K26 Fig.4d: inspeccionar datos originales de eEPSC | Archivo nuevo con valores/unidades, grupos, claves de cultivo/diferenciación y procedencia | Adaptador trazable y revisión del diseño real; habilitar contrato solo tras comprobar independencia, exclusiones y agrupación |

La petición Fig.4d ya fue enviada autorizadamente: [recibo](../reports/functional-rescue-20261103/COMMUNICATION_LOG.md). En la comprobación acotada del 03/11/2026 el hilo contiene solo la petición enviada; no se autoriza seguimiento automático. La nota inicial de AD Workbench era incompleta: [PR #46, comprobación del04/11](https://github.com/luisceb1/ela-research/blob/9a69cb8caec3281a35dd29cd8add7a36d07ec968/reports/continuity-20261104/REPORT.md) documenta aprobación del dataset seguida de revisión y workspace pendiente, sin acreditar acceso efectivo o manifiesto; informe aún separado de main. #37 conserva el [ciclo de búsqueda cerrado](../reports/source-gate-issue37-20261103/REPORT.md); no añadir un cuarto candidato.

Si no hay entrada nueva, registrar que ambas líneas siguen bloqueadas y detener ese ciclo. No crear otra auditoría equivalente, sustituir datos por simulación o cambiar de endpoint para evitar el bloqueo.

## Auditoría puntual autorizada y completada —04/11/2026

- [x] Asadollahi2025 Fig.3s: auditar el único archivo fuente experimental aprobado por Luis. Recuperadas38/35 entradas en pC, controles numéricos y de procedencia ejecutados. Falta mapa neurona→cultivo/exclusiones: disponibilidad parcial, sin reanálisis inferencial. [Decisión y reproducción](../reports/asadollahi-fig3s-audit-20261104/REPORT.md).
- [x] Continuación dirigida autorizada por Luis: Supplementary Data3 confirma n38/35 de Fig.3s sin asignaciones a cultivos; GOE-Seek260 devuelveHTTP403, contenido no inspeccionado. [Evidencia y límites](../reports/asadollahi-fig3s-audit-20261104/CULTURE_MAP_REPORT.md). Búsqueda acotada completada, sin inferencia.
- Condición de reconsideración: mapa técnico primario que vincule las entradas con cultivos independientes y aclare exclusiones. No repetir la consulta bloqueada o ampliar archivos/candidatos/modelos por defecto. Esta auditoría limitada no sustituye las prioridades #37/#44 ni reactiva automatización. PR#46 sigue pendiente y contiene la comprobación administrativa/búsqueda del04/11; reconciliar al integrar, sin declarar sus informes incorporados.


Comprobación pública adicional autorizada por Luis: /studies/260.json devuelveHTTP403 con error de aplicación «You may not view study:260». La API anónima no proporciona el manifiesto; no se presume que crear una cuenta baste. [Recibo y alcance](../reports/asadollahi-fig3s-audit-20261104/PUBLIC_ACCESS_REPORT.md). Luis autorizó expresamente el envío de la versión final presentada en el chat: Gmail confirma mensaje enviado el04/11/2026 a las10:20:43 Europe/Madrid. [Texto final y recibo](../reports/asadollahi-fig3s-audit-20261104/COMMUNICATION_LOG.md). Sin adjuntos/CC/BCC; no se comprobaron respuestas ni se habilitó acceso o inferencia. No hay seguimiento automático autorizado. No nuevas consultas equivalentes hasta un enlace/cambio de acceso o respuesta institucional.

## Reproducción descriptiva autorizada y completada — 04/11/2026

- [x] Reproducir A25 Fig.3s con los73 valores experimentales ya auditados: medias WT24.209923pC y R202H15.009117pC,2/2 concordantes con24.2/15.01 dentro de tolerancias prospectivas0.05/0.005pC; sin efecto entre grupos, SEM/IC o pruebas inferenciales. [Informe](../reports/fig3s-descriptive-20261104/REPORT.md).
- [x] Reconstruir los73 puntos, verificar conteos38/35, cotejar por fracciones racionales y repetir salidas numéricas byte a byte;24 controles de software correctos, sin omisiones. Mismo experimento publicado, no nueva replicación.
- [x] Preparar [revisión de integración #46/#47](../reports/fig3s-descriptive-20261104/INTEGRATION_REVIEW.md), manteniendo ambas PR abiertas.
- Entrada discriminante pendiente: mapa técnico inequívoco observación→cultivo y exclusiones. Mantener NO-GO inferencial si falta/ambigüedad. No repetir consultas bloqueadas, añadir otro endpoint/modelo o enviar seguimientos por defecto. Prioridades #37/#44 y automatización pausada se conservan.

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

