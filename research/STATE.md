# Estado vigente — 04/11/2026

Base remota comprobada: main `95bf05ecc1f991ec9843d48519d0764b29dc5dfb`, con mantenimiento hasta PR #45 fusionado. PR #46 y #47 siguen abiertas y separadas de main; esta síntesis pertenece a #47. El [historial íntegro](history/README.md) conserva las decisiones anteriores; sus próximos pasos no son tareas actuales.

## Líneas actuales

| Línea | Estado comprobado | Única condición de continuación |
|---|---|---|
| Fuente independiente UNC13A, issue #37 | Ciclo Seddighi/Irwin/Baughn cerrado sin fuente aceptada | Archivo/manifiesto nuevo concreto Seddighi–AD Workbench con cuentas de uniones por biblioteca o BAM/índices, condiciones, unidades independientes y lotes |
| Rescate funcional UNC13A, K26 Fig.4d, issue #44 | Auditoría y plan FR-K26-4d v1 preparados; reanálisis numérico bloqueado | Tabla original de eEPSC con valores/unidades y mapa célula→cultivo→diferenciación, procedencia y exclusiones verificables |

Para #37, conservar cobertura objetivo mínima 20 y al menos tres unidades biológicas independientes por condición antes de un contraste inferencial. No abrir un cuarto candidato ni repetir búsquedas cerradas. [Decisión y fuentes](../reports/source-gate-issue37-20261103/REPORT.md), [requisitos de acceso](../reports/source-gate-issue37-20261103/ACCESS_REQUIREMENTS.md).

Fig.4d informa 34/30/25 células de tres experimentos; las células no equivalen a réplicas biológicas. El contrato sigue deshabilitado y no estima efectos. Petición enviada con autorización expresa de Luis el 03/11/2026; envío confirmado, sin datos recibidos documentados en el repositorio. [Informe](../reports/functional-rescue-20261103/REPORT.md), [plan](../reports/functional-rescue-20261103/REPRODUCTION_PLAN.md), [comunicación](../reports/functional-rescue-20261103/COMMUNICATION_LOG.md). En la comprobación acotada del hilo del 03/11/2026 solo figura el mensaje enviado. No hay seguimiento automático autorizado.

## Auditoría adicional autorizada — Asadollahi2025 Fig.3s,04/11/2026

Sesión limitada aprobada expresamente por Luis, independiente de #37/#44. Archivo fuente editorial1185531bytes, SHA25642f9a2266bf8e7dc157350fe588f1d87deb8d0e4c5067bc2c780b9fc7851a49f. Hoja Figure3_R202H, carga eEPSC en pC:38 entradas WT y35 R202H. QC estructural correcto, sin claves de neurona/cultivo ni exclusiones verificadas. Disponibilidad parcial, NO-GO para inferencia jerárquica; sin efecto estimado ni validación funcional propia. [Informe](../reports/asadollahi-fig3s-audit-20261104/REPORT.md).

Auditoría inicial completada. En continuación dirigida expresamente autorizada por Luis, Supplementary Data3 (MOESM8,18581bytes; SHA2567ba494959360e824eb333eeadb2e0fd1bb431a32859da92cabdd5a958cf1c2e7) confirma n38/35 para Charge(pC),Fig.3s, sin mapa observación→cultivo. El depósito GOE-Seek260 enlazado devuelveHTTP403 y su contenido no pudo inspeccionarse. [Informe de continuación](../reports/asadollahi-fig3s-audit-20261104/CULTURE_MAP_REPORT.md). Se cierra la búsqueda dirigida sin inferencia, otro candidato o contacto. Solo reconsiderar ante un mapa técnico inequívoco observación→cultivo. La declaración publicada de al menos tres cultivos no reconstruye ese mapa. #37/#44 mantienen prioridades y bloqueos, y la automatización sigue pausada. PR#46 conserva por separado el estado administrativo/búsqueda actualizado del04/11 y sigue pendiente de incorporación a main.


Comprobación pública adicional autorizada por Luis: /studies/260.json devuelveHTTP403 con error de aplicación «You may not view study:260». La API anónima no proporciona el manifiesto; no se presume que crear una cuenta baste. [Recibo y alcance](../reports/asadollahi-fig3s-audit-20261104/PUBLIC_ACCESS_REPORT.md). Luis autorizó expresamente el envío de la versión final presentada en el chat: Gmail confirma mensaje enviado el04/11/2026 a las10:20:43 Europe/Madrid. [Texto final y recibo](../reports/asadollahi-fig3s-audit-20261104/COMMUNICATION_LOG.md). Sin adjuntos/CC/BCC; no se comprobaron respuestas ni se habilitó acceso o inferencia. No hay seguimiento automático autorizado. No nuevas consultas equivalentes hasta un enlace/cambio de acceso o respuesta institucional.

## Reproducción descriptiva autorizada — A25 Fig.3s, 04/11/2026

Completada con Python3.12.14: los73 valores depositados reproducen2/2 medias dentro del redondeo prospectivo: WT n38,24.209923pC frente a24.2 (tolerancia0.05); R202H n35,15.009117pC frente a15.01 (tolerancia0.005). Figura de los73 puntos, cotejo racional independiente y repetición numérica byte a byte correctos;24 controles de software sin fallos/errores/omisiones, no24 experimentos. [Informe, fuentes y límites](../reports/fig3s-descriptive-20261104/REPORT.md), [SVG](../reports/fig3s-descriptive-20261104/fig3s-descriptive.svg).

Reproducción aritmética del mismo experimento publicado, sin replicación biológica externa, efecto entre grupos o validación funcional propia. Mapa observación→cultivo/exclusiones pendiente: NO-GO inferencial. No sustituye K26 Fig.4d. Sesión completada; siguiente entrada discriminante: mapa técnico primario verificable. Sin nuevas consultas equivalentes o comunicaciones por defecto. [Revisión concreta de integración #46/#47](../reports/fig3s-descriptive-20261104/INTEGRATION_REVIEW.md); no se ha fusionado ninguna.

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

Seguimiento administrativo #37: la nota inicial del03/11 solo reflejaba recepción/revisión y era incompleta. [La comprobación del04/11 en PR #46](https://github.com/luisceb1/ela-research/blob/9a69cb8caec3281a35dd29cd8add7a36d07ec968/reports/continuity-20261104/REPORT.md) documenta aprobación del dataset seguida de revisión y workspace pendiente; no acredita acceso efectivo ni manifiesto. Es una referencia a la rama pendiente, no un informe incorporado a main. Es estado de acceso, no evidencia científica. #37 y #44 son las dos prioridades; los bloqueos históricos #1/#2/#14/#20 no se reactivan por continuidad automática.

## Operación y mantenimiento

Consultar [BACKLOG](BACKLOG.md), [protocolo](PROTOCOL.md) e [inventario de scripts](SCRIPT_LIFECYCLE.md). Conservar los ejecutores históricos: sus identidades y hashes forman parte de los sellos. No moverlos, reescribirlos o ejecutarlos como próximo piloto por defecto.

La CI debe leerse por commit y dependencias. Una matriz completa Python 3.11/3.12 instala PySAM/PyArrow fijados, compila scripts/tests y exige cero omisiones. Los checks históricos dependen del resultado de esa matriz sin repetir pruebas. Una CI correcta no reproduce automáticamente todos los análisis de datos reales.

Sin comunicaciones adicionales, costes, publicación externa, datos personales, laboratorio o indicaciones clínicas sin autorización expresa.

