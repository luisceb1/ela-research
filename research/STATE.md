# Estado vigente — 04/11/2026

Base comprobada para esta continuidad: main `95bf05ecc1f991ec9843d48519d0764b29dc5dfb`, con PR #36, #38, #39 y mantenimiento posterior hasta #45 fusionados. El [historial íntegro](history/README.md) conserva las decisiones anteriores; sus próximos pasos no son tareas actuales.

## Comprobación de continuidad — 04/11/2026

No hay PR abiertas ni archivo científico nuevo en las fuentes concretas revisadas. Fig.4d: el hilo conocido contiene solo la petición enviada y la búsqueda acotada de respuestas no devuelve nuevos mensajes. #37: Outlook contiene un aviso de aprobación del acceso al dataset (03/11 a17:35:13 Madrid) y otro de revisión del mismo acceso un segundo después. Los avisos de workspace dicen solicitud recibida/revisión. Esa combinación no acredita acceso efectivo, workspace operativo o disponibilidad del manifiesto; no se resuelve por suposición. El registro anterior que solo mencionaba recepción/revisión era incompleto.

Cotejo reproducible en Python3.12.14 sobre metadatos administrativos reducidos: reports/continuity-20261104. Sin datos clínicos, tablas numéricas, adjuntos, nuevas búsquedas científicas o mensajes enviados. Se excluyen de la PR los cuerpos íntegros y enlaces de autenticación. No hay reanálisis científico ni nuevas pruebas unitarias.

Ambas prioridades siguen bloqueadas por sus archivos concretos. Conforme a BACKLOG, este ciclo se detiene: no otra auditoría equivalente, simulación o candidato para eludir el bloqueo. La continuidad automática se pausa hasta nueva entrada y decisión de reanudación; las issues permanecen abiertas. Las condiciones de continuación de la tabla siguen vigentes.

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

Seguimiento administrativo anterior #37, 03/11/2026: el registro inicial solo reflejaba recepción/revisión. La comprobación del04/11 de arriba añade el aviso de aprobación y el de revisión posterior, sin acreditar acceso efectivo ni manifiesto. Es estado administrativo, no evidencia científica. #37 y #44 son las dos prioridades; los bloqueos históricos #1/#2/#14/#20 no se reactivan por continuidad automática.

## Operación y mantenimiento

Consultar [BACKLOG](BACKLOG.md), [protocolo](PROTOCOL.md) e [inventario de scripts](SCRIPT_LIFECYCLE.md). Conservar los ejecutores históricos: sus identidades y hashes forman parte de los sellos. No moverlos, reescribirlos o ejecutarlos como próximo piloto por defecto.

La CI debe leerse por commit y dependencias. Una matriz completa Python 3.11/3.12 instala PySAM/PyArrow fijados, compila scripts/tests y exige cero omisiones. Los checks históricos dependen del resultado de esa matriz sin repetir pruebas. Una CI correcta no reproduce automáticamente todos los análisis de datos reales.

Sin comunicaciones adicionales, costes, publicación externa, datos personales, laboratorio o indicaciones clínicas sin autorización expresa.

## Búsqueda manual ampliada de Fig.4d — 04/11/2026

A petición expresa de Luis se amplió la búsqueda pública, sin reactivar la automatización. DataCite:77 registros DOI (incluyen versiones), Zenodo:15 entradas, Figshare:42; también Crossref, Europe PMC/BioStudies, bioRxiv, GitHub y páginas de grupos. No se localizó una tabla original identificable K26 Fig.4d. BioStudies lista solo media-1.pdf del preprint2024; descarga HTTP503, sin inspección de bytes. XML K24 identifica Fig.4d como intensidad UNC13A, no eEPSC espinal. Errores y recuperación incompleta de índices documentados; no se demuestra inexistencia de datos. [Informe y registro](../reports/fig4d-source-search-20261104/REPORT.md).

#44 sigue bloqueada; contrato deshabilitado, sin estimación funcional ni nuevas réplicas. No repetir esta ampliación por defecto: continuar con enlace/archivo original nuevo y revisión del mapa de independencia. #37 y las condiciones previas no cambian. La continuidad automática permanece pausada; sin nuevos contactos, costes, merge o cierre de issues.
