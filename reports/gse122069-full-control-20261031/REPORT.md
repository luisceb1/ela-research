# QC del control completo SRR8144907 — 31/10/2026

## Evidencia

Pasada completa ejecutada, no proyección del piloto: **37.518.164 lecturas** públicas de SRR8144907 / GSM3454242 / SRX4965534, grupo publicado siControl 1, cultivo SH-SY5Y. No se procesaron las otras cinco bibliotecas. Esta biblioteca contiene el primer millón ya auditado: no se suman como lecturas únicas, estudios o réplicas independientes.

Plan anterior al análisis: [ejecución](../../research/plans/2026-10-31-full-control-execution.md), derivada de la [propuesta fijada](../../research/plans/2026-10-31-full-control-coverage-proposal.md). Código/preflight persistidos en c3bf1f757f0fe08f415a98a4d5a95923f439cf42; recuperación acotada en dc30c0bc3deb05ccfa5878b6e8ac910d321b7122; inicio en23426ef338ee509db8c802480d99ce6b3c0572b5. Checkpoints intermedios son estados parciales de esta misma pasada, reemplazados por el resultado final.

Pregunta: ¿persiste la falta de cobertura aceptada de exon1/donante observada en el primer1M cuando se procesa la biblioteca completa fijada? Resultado discriminante previo: detectar soporte o no; criterio de aptitud canónica+críptica≥20 a anclaje15. Fracaso técnico: hashes, esquema, número fijo, EOF/CRC, parsers o límites discordantes. No detener por señal, cambiar objetivos ni ampliar muestra.

| Métrica técnica | Primaria: anclaje≥15 | Sensibilidad: anclaje≥8 |
|---|---:|---:|
| Observaciones de intrón elegibles, genoma completo | 2.039.339 | 3.286.603 |
| STMN2 canónica79611214→79636802, chr8+ | **72** | 110 |
| STMN2 críptica79611214→79616822, chr8+ | **0** | 0 |

Uniones expresadas como límites exónicos1-based, referenciaGRCh38. Mismos filtros: primario, no unmapped/QCfail/secundario/suplementario, MAPQ20–254,NH1,XS+, anclajes contiguos a cada lado; duplicados no eliminados. Los intrones globales admiten ambas hebras XS. No son moléculas ni transcritos completos.

38 bloques técnicos en orden depositado:37×1.000.000+518.164. **Todos coinciden entre extractor de texto/CIGAR y PySAM/HTSlib**, en cuentas globales/objetivos y números de registros por bloque. [Tabla](bin-qc.tsv), [resumen](summary.json), [resultado](execution/full-control-results.json), [extractor independiente](execution/htslib-checkpoint.json). El primer bloque reproduce exactamente las cuentas del piloto y sus1.256.935registrosSAM. El segundo bloque ya tiene2observaciones canónicas a15; no se detuvo la pasada al recuperarlas. No atribuir al orden un sesgo causal ni inferir sesgo3prime a partir de esta distribución.

QC del locus por bloques, con PySAM:24.701primarios con bloque solapante;24.691únicos/MAPQ≥20;169solapan exon1,1.308exon2;1.901lecturas únicas con splicing dentro del locus. Un solapamiento no acredita por sí solo asignación génica. Cero exon1 en el primer1M no persistió en la biblioteca completa.

FASTQ: exactamente37.518.164registros,1.896.541.486bases,547.114N; longitudes35–51nt, histograma completo en[QC](execution/fastq_qc.json). Calidad ASCII35–74, media37,1399 siPhred33. Lectura hastaEOF conCRC/ISIZE gzip válido, sin registro extra. Alineamiento:37.518.164primarios y47.124.040registrosSAM;9.605.876secundarios,0suplementarios,0QCfail. [HISAT2](execution/hisat2.log) informa31.483.857lecturas alineadas exactamente una vez,4.611.370multialineadas y1.422.937no alineadas;96,21%alineamiento. Es QC, no inferencia biológica.

Controles anteriores a datos reales: ambos parsers concordantes enSAMsintéticos de26consultas y2consultas/3registros, incluyendo fronteras de7consultas por bloque. [Preflight](preflight.json). Se mantienen los controles históricos positivos, negativos y multicopia. La menor recuperación canónica sintética a ancla8 ya documentada no se borra:15es primaria,8sensibilidad; no certificar sensibilidad equivalente universal. Suite final335tests locales ycompileall correctos; CI por SHA se enlaza en el PR.

## Reproducción, recursos e incidencias

HISAT2v2.2.3, fuente0d244324f98de541bce04d45c75e83bc3522f7f4; PySAM0.23.3/HTSlib1.21. Binario recompilado, nuevoSHA256 **736b75476c6b0b041d7520821e16435c7e9afcdde5fe7863d20992e3fb044ee2**; no se presenta como el mismo binario previo. Fuente, compilador, wheel verificado contra registroPyPI, versión y construcción en[binaries](binaries.json),[build](build.json),[source](source-restore.json). Índice oficial fijado porS3versionId, archivoSHA2561848784403a0fb3ee7735b2f891d8be96fd2782e08aed3d8212d922666f077a5; nueve miembros extraídos coinciden con los hashes anteriores yCRC de restauración válido. No nueva certificación de igualdad externa del genoma completo.

FASTQ1.391.030.664bytes: MD5ENA90ad6a34a34e8262bf300d7bb35406e1 ySHA256propio previo **d3f57e023735d35261f9b0c2acb4d8034a859295ab12178375be352c7b7d6593**, ambos iguales tras restauración. [Origen y rangos](fastq-download.json). Ningún otro run descargado en esta fase.

Restauración necesaria por retirada de cachés del entorno. Primer intento detenido porguard de disco tras48/83rangos guardados; [registro del error](fastq-download-attempt1.json). Copias temporales redundantes de esta ejecución retiradas, cachés aisladas en/tmp conservando rutas mediante enlaces. Los48rangos guardados se verificaron porSHA256 antes de reusar; solo35faltantes recuperados. RestauraciónFASTQacumulada1.055,44s<1.800s, incluidos751,06s delprimer intento. No interpretar fragmentos descargados no conservados como nuevos datos analizados.

Fase completa **1.373,82s (22,90min)**, incluidos20,88s de verificación previa; salida0, sin errores delwatchdog. CPUafín0/1; caps de espacio virtual5GiB alineador+512MiB padre+256MiBHTSlib=5,75GiB. MaxRSS hijo4.649.224KiB, padre31.616KiB, worker31.616KiB, métricas separadas: no medición deRSScombinado. Guard de disco15GiBadicionales desde baseline63.427.059.712bytes, reserva8GiB; primerfallo explícito y pasado completo dentro de presupuesto tras limpieza. No se guardóSAM/BAMcompleto niFASTQdescomprimido.

Comando exacto en[command.json](command.json); ejecutar desde raíz tras restaurar las entradas verificadas y el entorno registrado. Runner:`scripts/gse122069_full_control.py`; resumen:`python scripts/summarize_gse122069_full_control.py reports/gse122069-full-control-20261031`. El modo histórico1M se conserva. [Tests](tests.txt) y logs de compilación forman parte del registro. Hashes de archivos finales en`artifact-hashes.json`.

## Interpretación y límites

El escenario de falta persistente de cobertura aceptada en todo el control **no se observa**. Denominador técnico72≥20: supera la regla de factibilidad fijada para este control. Esto no acepta automáticamente las otras bibliotecas, el diseño biológico ni la potencia. La unión críptica sin soporte aceptado es un resultado negativo técnico; no ausencia molecular demostrada. No se calculan fracciones, PSI, efectos, p-valores o intervalos. No se estimó expresión/proteína funcional ni rescate.

Es exploración/QC técnico de datos publicados, no replicación externa establecida ni validación funcional. Un control no proporciona contrasteTDP-43. Los38bins, el piloto, la expresión ysplicing reutilizados no son cohortes independientes. Solo accesiones, grupos de cultivo publicados yvariables técnicas; sin datos clínicos personales, identificadores de lecturas exportados o scripts de autores ejecutados.

## Siguiente prueba discriminante

Antes de descargar los otros cinco: enlazar las seisbibliotecas a experimentos/lotes mediante documentación pública técnica/agregada, sin suponer pareamiento por sufijos ni equiparar bibliotecas a diferenciaciones. Mantener bloqueada la inferencia si el enlace no se acredita. Con ese resultado, preparar plan prospectivo de recursos y ejecución secuencial con QC por biblioteca; este control no predice cobertura de otras. No repetir este control como nueva muestra.

Los otros runs tienen38,50–66,94Mlecturas publicadas:30min no garantiza completar el mayor. El benchmark de un control no autoriza ampliar automáticamente presupuestos. No se inicia aquí ninguna biblioteca adicional, contacto, gasto, laboratorio, publicación externa, merge o cierre de issue. PR30 permanece separado.
