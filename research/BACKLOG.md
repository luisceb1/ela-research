# Backlog vigente — 31/10/2026

Solo la primera fila es la próxima tarea científica. Los bloqueos requieren evidencia nueva, no más ejecuciones de los mismos insumos. Consultar STATE y MASTER_EVIDENCE.

| Prioridad | Trabajo | Estado / criterio de cierre |
|---|---|---|
| P0 | Inspeccionar índice HISAT2 fijado antes del piloto GSE122069 | Ventanas STMN2 UCSC/Ensembl y motivos comprobados; candidato hg38 de4.355.786.349bytes/versionId fijado. Pendiente descarga controlada, SHA256, integridad, secuencia/nombres/longitudes, tamaño extraído y ejecución NH/XS/MAPQ. Sin índice/FASTQ descargado; piloto bloqueado |
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
