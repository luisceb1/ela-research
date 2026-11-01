# Backlog vigente — 01/11/2026

La primera fila marca la siguiente puerta de revisión. Los bloqueos requieren evidencia nueva, no más ejecuciones de los mismos insumos. Consultar STATE y MASTER_EVIDENCE.

| Prioridad | Trabajo | Estado / criterio de cierre |
|---|---|---|
| P0 revisión | Cierre del QC técnico y PR #33 | Replay completado:4292655lecturas,371,380s≤600,13/3a15 y15/4a8 exactos, cuentas/histogramas concordantes.392tests/compileall, exportadores idénticos y6rechazos negativos. Revisar informe nuevo antes de decidir integración o nuevo contraste; sin merge/cierre automático |
| Completado | QC del soporte críptico bajo SRR8144908 | reports/stmn2-control2-target-qc-20261101. MAPQ60/NM0/AS0/softclip0 en4observaciones a8 (incluyen3a15); no independencia molecular o efecto. Resultado original completo yhash intactos. No repetir ni usar selección para tasas; no otros4runs |
| Completado | Recuperación de artefactos delsegundo control | Resultado54.292.655lecturas,111/3a15,154/4a8 intacto. Paquete completo de resultados pequeños recuperado, verificado ypersistido porPR33. Historia parcial preservada; no reejecución delalineamiento |
| Bloqueado, búsqueda cerrada | Mapa biológico GSE122069 | reports/gse122069-design-20261031:12registros técnicos válidos yReportingSummary nuevo noaportan asignación explícita. Independencia3/3declarada, no refutada; no inferencia ni pares por sufijos. Reabrir solo con fuente concreta nueva; medio discrepante sin resolver |
| Bloqueado | E-MTAB-15653 | Auditoría documental terminada; independencia no certificada. No repetir búsqueda ni calcular efectos sin nueva fuente concreta |
| Completado en este PR | Ciclo de selección de tres fuentes | GSE182976: cobertura BW; GSE122069: TPM; E-MTAB-15653: cuentas de unión recuperadas, independencia no certificada. Ninguna lista para el contraste completo. No repetir |
| Revisión | PR #30 separado | Otros candidatos y trabajo posterior; no integrado ni reejecutado aquí. Reconciliar su planning al integrar, sin sumar resultados o ampliar a datos clínicos personales |
| Preparado | Plan de recursos GSE122069 | reports/gse122069-resource-plan: seis runs, 9,47 GB; entorno 8 GiB RAM. Presupuestos propuestos y puertas de parada, no benchmark o ejecución |
| Operación | Integración #28/#29/#31 | Incorporados en main f898b296. Este nuevo contrato queda en PR separado, sin merge/cierre automático. 275 pruebas locales; CI de nueva cabeza por verificar |
| Mantenimiento | #1/#2/#17/#19 | Entregables técnicos ejecutados; actualizar issues sin presentarlos como fallos activos ni cerrar automáticamente. Límites de QC/estructura completa permanecen |
| Mantenimiento | #20 | Parser y geometría global ejecutados. Separar esa resolución de cobertura/asignación y lecturas aún pendientes |
| Bloqueado | #14 refit | Pozo/reactivo/modelo original pendientes; reproducción agregada, deduplicación y QC completados. No repetir |
| Bloqueado | SH-SY5Y siete uniones | Nueva definición molecular explícita para cuatro alias y dos conflictos; seis enlaces ENA ya completados. Sin nueva fuente, detener |
| Bloqueado | Contraste funcional posdéficit | Necesita unidades, basal y primera dosis enlazados; inventario acotado cerrado. Protocolo v0.4 conceptual |
| Diferido | #15 CAMK2B/péptidos | Reproducción estructural realizada; proteómica independiente no validada. No anunciar nuevo candidato |
| Diferido | #16 MEA | Auditoría sintética realizada; no sustituye ensayo ni habilita datos reales sin requisitos |
| Diferido | #21 AGRN | Antecedentes ya existen; no iniciar otro ensayo/propuesta antes de escoger una pregunta única |
| Diferido | #18 colaboración | Propuesta incremental para revisión, sin contactos o laboratorio autorizados por esta integración |

Reglas de cierre: cada tarea termina en resultado reproducido, corregido o bloqueo documentado. Un bloqueo no se resuelve acumulando pruebas de software. Nuevas fuentes, costes, personas o cambios de alcance se evalúan antes de actuar.

No considerar como próximas tareas los párrafos históricos de los informes. Historial anterior del backlog de cada rama: reports/integration-20261030/history. Las issues abiertas se conservan hasta una decisión explícita sobre su cierre.

## Actualización: unidades de E-MTAB-15653

Auditoría acotada completada en reports/fractionation-units-20261030: XML primario y suplemento PDF nuevo verificados por hash. El PDF no aporta un mapa de cultivos independientes; seis enlaces técnicos basales correctos no certifican seis unidades biológicas. La vía inferencial sigue bloqueada y esta búsqueda se cierra sin repetirla. Siguiente trabajo seguro propuesto: redactar plan de recursos y controles de los seis runs GSE122069 ya identificados, sin descargar/alinear ni abrir un cuarto candidato. No efectos, PSI o inferencia en este ciclo. Mismo PR31 abierto; PR30 separado. Los próximos pasos anteriores sobre buscar documentación de unidades quedan reemplazados por este resultado.

## Continuidad 31/10/2026

La fila P0 sustituye los siguientes pasos históricos de abajo/anteriores informes. No repetir #1/#2, Fratta, DEXSeq ni búsquedas cerradas. Contrato positivo de software, sin resultado biológico. Un intento Ensembl falló por timeout; mantener referencia/índice como bloqueo de piloto y continuar con su verificación, sin instalar/alinear automáticamente. PR30 inspeccionado a 053ef70ce437cc637ec18278a2c07e3abd6bf58b, rama intacta. 22 pruebas nuevas no representan experimentos. Próxima prueba discriminante: FASTA e índice verificables con motivos/ensamblaje concordantes, después comparación del extractor con herramienta independiente en piloto condicionado al plan de recursos. El resumen semanal del viernes ya existe y no se duplica el sábado.

## Referencia completada, continuación posterior a #32

MotivosGT/AG/AG y tres ventanas16bp idénticas UCSC/Ensembl en reports/stmn2-reference-gate-20261031. No FASTA completo ni índice validados. #32 integrado en9c82795d con autorización específica; esta nueva entrega es PR revisable, sin fusión automática.284tests locales, no284experimentos. La única tarea siguiente es la filaP0; comprobar índice bajo presupuesto y semántica runtime del software antes del piloto. Evitar repetición de las verificaciones de motivos completadas y conservar rama30 intacta.

## Índice inspeccionado — continuación vigente en PR33

No volver a descargar/reinspeccionar como si faltara. Manifest real reports/hisat2-index-inspection-20261031/verified_index.json, hashes y comandos completos. Índice+archivo9,02GB; inspector~4,54GiB RAM, no coste de alineamiento medido.295tests locales,CI de cabeza nueva pendiente. Se continúa el mismoPR33 sin merge; PR30 intacto. La filaP0 sustituye pendientes históricos de descarga de índice/ventanas; piloto sigue condicionado a controles runtime/extracción antes de un primer millón de lecturas del control prefijado.

## Gate sintético completado — continuación vigente

Informe reports/hisat2-synthetic-gate-20261031. Positivos equilibrados/negativos/multicopia y dos parsers concordantes; no repetir como pendiente. Asimetría a8bases no eliminada retrospectivamente: futura primaria15y sensibilidad8, ambas fijadas antes de leer resultados reales. Requiere implementar política en ambos extractores para el piloto y mantener análisis solo técnico.301tests locales,CI de cabeza nueva por verificar. MismoPR33 abierto, sin merge/cierre automático; PR30 intacto.

## Piloto completado, contraste bloqueado por cobertura

reports/gse122069-pilot-20261031:1Mreal,96,58%alineamiento,conteospropio/HTSlib iguales. Umbral de cobertura noalcanzado, no ausencia biológica. Diagnóstico del mismo millón:0exon1,31exon2,48unionesposteriores; no nueva réplica. MetadataTruSeqRNAkit noacredita3prime-only. Siguiente filaP0 sustituye instrucciones históricas de ejecutar piloto.309tests locales;CI de nueva cabeza por verificar. Primer fallo de supervisión guardado y corregido conservadoramente; cachecomprimida del índice retirada para presupuesto,extraído verificado conservado. MismoPR33abierto sinmerge yPR30intacto.

## Mapeabilidad completada — continuación vigente

reports/stmn2-exon1-mappability-20261031:194/194 del exon1 (54en tramo común63nt),680 controles posteriores y8positivos correctos; negativo excluido. SinFASTQreales nuevos ni cambio del piloto. No imposibilidad general de mapeo perfecto bajo esta configuración; causa de cobertura5prime sigue abierta. Única próxima tarea: propuesta de controlcompleto fijado, no otros cinco ni nueva fase adaptativa.317tests locales,CI de cabeza nueva por verificar; mismoPR33 abierto yPR30 intacto.


## Control completo completado — estado vigente

reports/gse122069-full-control-20261031 reemplaza la instrucción anterior de preparar/ejecutar este mismo control.1373,82s,335tests locales/compileallOK,FASTQMD5/SHA yEOF/CRC válidos. El negativo del primer1M sigue intacto; la cobertura total recuperada no certifica ausencia críptica, efecto ni función. Checkpoints parciales y expresión/splicing de la misma fuente no son replicación externa. Error de restauración por disco yreanudación acotada documentados. No repetir el control como nueva fase. La únicaP0es el gate de diseño, sin iniciar otros5ni cambiar presupuestos automáticamente. PR30intacto; PR33abierto sinmerge/cierre.


## Diseño GSE122069 auditado — continuación vigente

349tests locales/compileallOK yreplay idéntico. Se conservan6errores iniciales de parser deaccesiones, reparación SRS/SAMN cotejada porhash,12proyecciones técnicas yReportingSummary porSHA coninspección visual. No nuevoFASTQ, alineamiento o réplica. La búsqueda del mapa queda cerrada conbloqueo concreto; no repetir comoP0. Siguiente únicaP0: código/configuración ycontroles sintéticos para accession, sin datos nuevos. Las estimaciones de recursos de5runs son proyecciones, no ejecuciones, yel límite futuro45min no es ampliación automática. PR30sin modificar, PR33revisable sinmerge/cierre.


## Parametrización completada — continuación vigente

reports/gse122069-parameterization-20261031: configuración/recibo/runner/resumen ligados aaccession; transporte con límite global supervisado.374tests locales, preflight concordante yrepetible; mismosargv yresumen delcontrolhistórico. CeroFASTQreales/alineamientosHISAT2nuevos;28consultas sintéticas únicas reusadas no sonreplicación externa. Propuesta concreta paraSRR8144908 en elnuevo plan, todavía pendiente decabeceras yrecursos antes deejecutar. No repetir elmapabiológico sinfuente nueva, ni reejecutar elprimercontrol. PR33sinmerge yPR30intacto.


## Cierre delsegundo control —01/11/2026

Queda sustituido elbloqueo de recuperación previo: JSONcompleto original coincide conSHA previo,55bins yambos extractores/TSV/logs disponibles yconsistentes.378tests locales/compileallOK; solo reexportación deJSON, sinFASTQ/HISAT2nuevos. El presente encargo termina en recuperación/persistencia completa de artefactos pequeños. La siguienteP0científica se conserva como propuesta noejecutada, sin otros4runs. PR33abierto para revisión, PR30intacto; sinmerge/cierre.
