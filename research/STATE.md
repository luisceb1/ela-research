# Estado vigente — 03/11/2026

Base de esta síntesis: main `867e1478d4eaa5f31d078001785eed246783a27d`, con PR #36, #38 y #39 fusionadas. El [historial íntegro](history/README.md) conserva las decisiones anteriores; sus próximos pasos no son tareas actuales.

## Líneas actuales

| Línea | Estado comprobado | Única condición de continuación |
|---|---|---|
| Fuente independiente UNC13A, issue #37 | Ciclo Seddighi/Irwin/Baughn cerrado sin fuente aceptada | Archivo/manifiesto nuevo concreto Seddighi–AD Workbench con cuentas de uniones por biblioteca o BAM/índices, condiciones, unidades independientes y lotes |
| Rescate funcional UNC13A, K26 Fig.4d, issue #44 | Auditoría y plan FR-K26-4d v1 preparados; reanálisis numérico bloqueado | Tabla original de eEPSC con valores/unidades y mapa célula→cultivo→diferenciación, procedencia y exclusiones verificables |

Para #37, conservar cobertura objetivo mínima 20 y al menos tres unidades biológicas independientes por condición antes de un contraste inferencial. No abrir un cuarto candidato ni repetir búsquedas cerradas. [Decisión y fuentes](../reports/source-gate-issue37-20261103/REPORT.md), [requisitos de acceso](../reports/source-gate-issue37-20261103/ACCESS_REQUIREMENTS.md).

Fig.4d informa 34/30/25 células de tres experimentos; las células no equivalen a réplicas biológicas. El contrato sigue deshabilitado y no estima efectos. Petición enviada con autorización expresa de Luis el 03/11/2026; envío confirmado, sin datos recibidos documentados en el repositorio. [Informe](../reports/functional-rescue-20261103/REPORT.md), [plan](../reports/functional-rescue-20261103/REPRODUCTION_PLAN.md), [comunicación](../reports/functional-rescue-20261103/COMMUNICATION_LOG.md). En la comprobación acotada del hilo del 03/11/2026 solo figura el mensaje enviado. No hay seguimiento automático autorizado.

## Resultados cerrados que no se repiten como trabajo nuevo

- Piloto CTRL-4 / SRR33425816: técnicamente completado, cobertura UNC13A [1,0,0] frente a mínimo 20 en anclajes 15/8. Piloto cerrado; no ampliar al control completo ni iniciar TDP por defecto. Conservar datos, intentos, sellos y cargos. [Cierre](../reports/unc13a-control-annotation-20261103/CLOSURE.md).
- Inventario regional: 31/33 uniones. RefSeq coincide con 30/31 y 32/33; una unión unitaria antes no anotada en la caché coincide con NM_001387022.1/XM_017026502.2. Aclaración de referencia, sin cobertura nueva o validación biológica. [Comparación](../reports/source-gate-issue37-20261103/refseq-comparison/comparison.json).
- STMN2/PAPA: reproducción descriptiva de TPM a PPAU completada en 12/12 bibliotecas; no medición directa de uniones, PSI o función.
- GEO/mapeo ENSG y parser histórico corregidos. Catálogo de 1.901 claves con soporte asignado: 545 anotadas, 353 solo autores, 182 pendientes, 821 sin coincidencia en recursos limitados. No equivalen a descubrimientos.
- GSE126542/GSE121569: reproducción agregada y QC ejecutados. Los bins DEXSeq auditados no miden directamente las regiones CE contrastadas. Refit bloqueado por diseño/dependencias incompletos.
- GSE122069: dos controles procesados y QC seleccionado completados; mapa biblioteca→cultivo/lote/pareamiento pendiente. No procesar los cuatro runs restantes por continuidad automática.

El [registro de evidencia](MASTER_EVIDENCE.md) y el [historial](history/README.md) enlazan informes, hashes y resultados negativos.

## Límites y líneas diferidas

GSE310723 tiene una biblioteca por condición: no simular réplicas. GSE315972 es tejido heterogéneo y no se combina con i3N como replicación. Paridad/escala de uniqueCounts y soporte molecular siguen sin explicación completa; no dividir cuentas por dos por suposición.

SH-SY5Y conserva cuatro alias UNC13A y dos conflictos de hebra STMN2 pendientes; solo reabrir con fichero fuente nuevo. AGRN, CAMK2B, simulador MEA y protocolo posdéficit UNC13A v0.4 permanecen aparcados/conceptuales; #15/#16/#18/#21 se cierran como no planificadas actualmente y conservan condiciones de reconsideración en BACKLOG. No hay rescate funcional propio ni beneficio clínico demostrado.

Seguimiento administrativo #37, 03/11/2026: los correos localizados de la solicitud AD Workbench confirman recepción y revisión en curso; no incluyen aprobación ni manifiesto. Es estado de acceso, no evidencia científica. #37 y #44 son las dos prioridades; los bloqueos históricos #1/#2/#14/#20 no se reactivan por continuidad automática.

## Operación y mantenimiento

Consultar [BACKLOG](BACKLOG.md), [protocolo](PROTOCOL.md) e [inventario de scripts](SCRIPT_LIFECYCLE.md). Conservar los ejecutores históricos: sus identidades y hashes forman parte de los sellos. No moverlos, reescribirlos o ejecutarlos como próximo piloto por defecto.

La CI debe leerse por commit y dependencias. Una matriz completa Python 3.11/3.12 instala PySAM/PyArrow fijados, compila scripts/tests y exige cero omisiones. Los checks históricos dependen del resultado de esa matriz sin repetir pruebas. Una CI correcta no reproduce automáticamente todos los análisis de datos reales.

Sin comunicaciones adicionales, costes, publicación externa, datos personales, laboratorio o indicaciones clínicas sin autorización expresa.

## User-authorized bounded extension — 04/11/2026

ELK1 RNA-FISH image-count replay: [report](../reports/elk1-fish-replay-20261104/REPORT.md). Sixty image rows, three source replicate labels; seven of nine deposited ratios reproduced, two unresolved. Molecular/descriptive only; no functional rescue or independent experimental validation. This completed extension does not replace #37/#44 or reopen their searches. No further ELK1 program is scheduled.

Final-paper-linked ELK1 archive reconciliation completed: [comparison](../reports/elk1-fish-replay-20261104/FINAL_ARTICLE_COMPARISON.md). Inputs identical, 240 long rows and 84 aggregate fields match; two old ratio discrepancies persist. Fig.3g-style extranuclear counts reconstructed without P values or editorial point-identity certification. Bounded task closed; no new ELK1 study scheduled.
