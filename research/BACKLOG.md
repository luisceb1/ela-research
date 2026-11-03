# Backlog vigente — 03/11/2026

Este archivo contiene tareas actuales y condiciones de reapertura. [STATE](STATE.md) resume resultados; el [backlog anterior íntegro](history/README.md) conserva la cronología.

## Continuaciones científicas bloqueadas

| Prioridad | Tarea | Entrada necesaria | Criterio de finalización |
|---|---|---|---|
| 1 | #37: inspeccionar un manifiesto concreto Seddighi–AD Workbench | Fuente nueva con cuentas de uniones o BAM/índices y mapa biblioteca→condición→unidad→lote | Tabla trazable de aceptación/rechazo; solo si cumple cobertura/diseño, redactar prospectivamente un único contraste |
| 1 | K26 Fig.4d: inspeccionar datos originales de eEPSC | Archivo nuevo con valores/unidades, grupos, claves de cultivo/diferenciación y procedencia | Adaptador trazable y revisión del diseño real; habilitar contrato solo tras comprobar independencia, exclusiones y agrupación |

La petición Fig.4d ya fue enviada autorizadamente: [recibo](../reports/functional-rescue-20261103/COMMUNICATION_LOG.md). No se ha documentado respuesta con datos ni se autoriza seguimiento automático. #37 conserva el [ciclo de búsqueda cerrado](../reports/source-gate-issue37-20261103/REPORT.md); no añadir un cuarto candidato.

Si no hay entrada nueva, registrar que ambas líneas siguen bloqueadas y detener ese ciclo. No crear otra auditoría equivalente, sustituir datos por simulación o cambiar de endpoint para evitar el bloqueo.

## Mantenimiento técnico

- [x] Separar estado/backlog actuales del historial íntegro.
- [x] Documentar scripts históricos y puntos de entrada acotados.
- [x] Hacer visibles pruebas ejecutadas/omitidas y exigir cero omisiones en el contrato paired-end. Verificar CI sobre el commit de la PR de mantenimiento antes de integrarla.
- [ ] Cuando una nueva tarea aceptada necesite transporte/ejecución: extraer módulos comunes de transporte, presupuesto, reloj y supervisión; definir configuración explícita y conservar ejecutores históricos sin cambiar sus hashes. Comparar recibos/salidas en fixtures antes de adoptar el nuevo ejecutor.
- [ ] Evaluar consolidación de trabajos CI redundantes después de documentar dependencias y cobertura efectivamente ejecutada.

## Líneas diferidas y reglas de parada

AGRN, CAMK2B, MEA sintético, protocolo UNC13A posdéficit v0.4, refit GSE121569, alias/hebras SH-SY5Y y soporte/cobertura Iso-Seq permanecen diferidos o bloqueados. Sus issues históricas no se cierran por esta limpieza. Una fuente primaria nueva y una pregunta definida son requisitos para reabrirlas.

No repetir STMN2/PPAU 12/12, el piloto UNC13A cerrado, Humphrey procesado o búsquedas agotadas como trabajo nuevo. No relajar cobertura 20, promover bibliotecas técnicas a réplicas ni sumar uniones ajenas al objetivo.

No nuevas descargas masivas, control completo/TDP, contactos, gastos, datos personales, laboratorio o publicación externa por continuidad automática. [AGENTS](../AGENTS.md) y [PROTOCOL](PROTOCOL.md) siguen aplicando.
