# Mapeabilidad del primer exón STMN2 — 31/10/2026

## Resultado y alcance

**Las 194 lecturas perfectas de 50/51 bases generadas en el primer exón se recuperan íntegras en su posición de origen**, en ambas orientaciones, con NH1 y MAPQ≥20 distinto de255. También pasan todos los controles de exones posteriores, los ocho positivos de unión y el negativo. No se han procesado nuevos FASTQ reales.

La predicción del plan previo se cumple: hay recuperación en el origen para ambas longitudes. Esto no respalda una imposibilidad general de mapear las secuencias perfectas del primer exón con esta versión/configuración. **No explica todavía por qué el piloto real no aporta cobertura aceptada de ese exón.** No demuestra igualdad de sensibilidad con errores, variantes, fragmentación u otras propiedades de las bibliotecas reales; no acredita expresión ni ausencia molecular.

| Región de referencia | Consultas de 50 nt exactas/total | Consultas de 51 nt exactas/total |
|---|---:|---:|
| Primer exón canónico, 98 nt | 98/98 | 96/96 |
| Tramo común de 63 nt, subgrupo del anterior | 28/28 | 26/26 |
| Exón2, 96 nt | 94/94 | 92/92 |
| Exón3, 173 nt | 248/248 | 246/246 |

Las cifras incluyen ambas orientaciones de cada ventana. Hay49 posiciones de inicio de50nt y48de51nt en el exón de98nt:194 consultas sintéticas, no194 posiciones independientes o réplicas biológicas. Las680 consultas posteriores tampoco son un experimento de eficacia. Las ocho lecturas de unión equilibradas recuperan exactamente los dos objetivos prefijados; N50 queda sin alinear. Total:883 consultas.

## Definición, método y controles

Plan fijado antes del alineamiento: research/plans/2026-10-31-stmn2-exon1-mappability.md. Se recorrieron todas las ventanas, sin seleccionar las que mejor alinean. Criterio de exactitud: primario, chr8 yposición/orientación de origen, CIGAR íntegro50M/51M, NM0, NH1, MAPQ≥20 yno255. No se requiere XS a lecturas exónicas continuas; sí se verifica la hebra de las uniones. NH es unicidad **reportada**, no exhaustividad genómica demostrada.

Se reutiliza la proyección GENCODEv47 ya auditada en reports/isoforms/exons.tsv, cotejada con el blob remoto y con SHA256 en definition.json. No se reconstruye independientemente el GTF ni se repite la auditoríaGEO/ENSG. ENST00000220876.12 tiene exon1 chr8:[79611116,79611214),98nt; ENST00000518111.5 tiene [79611151,79611214),63nt. Ambos comparten el donante79611214. La intersección se evaluó como subgrupo, sin suponer qué TSS se expresa ni cambiar numerador/denominador.

Los otros intervalos0-based semiabiertos son exon2 [79636801,79636897), exon3 [79641377,79641550), y un flanco del aceptor críptico para los positivos. Se obtuvieron desde el índice fijado, en flujo, sin FASTA completo en disco. Los controles equilibrados de las uniones se fijaron a25+25 o25+26bases, en ambas orientaciones, sin sitios inyectados.

HISAT2v2.2.3, ejecutable directo y mismo índice que el piloto:2hilos,-k5,--seed0,--no-temp-splicesite,--reorder; sin dta, anotación añadida o strandness impuesta. Límite virtual5GiB, timeout600s yafinidad2CPUs. No se cambian coordenadas/filtros tras observar la recuperación. No hay aleatoriedad en la generación de ventanas. Se conservan controles completos y observaciones por consulta sintética, sin datos de personas.

## Reproducibilidad y recuperación

La copia local disponible pertenecía a una rama antigua y se dejó intacta. Se trabajó en un directorio aislado, con226 archivos recuperados que coincidían exactamente con los blobsGit de la cabeza inicial del PR33; las309 pruebas de base pasaron. El índice y binarios anteriores seguían accesibles: se cotejaron los hashes de sus nueve ficheros y los ejecutables. No se descargaron otra vez ni se leyeron los FASTQ reales del control.

Los hashes de entradas, secuencias mínimas, código y salidas se preservan. Dos alineamientos generan SAM, results.json yobservations.tsv idénticos por bytes. El SAM yFASTQ sintéticos quedan como intermedios regenerables; los controles y tablas completas están en el informe. La copia de fuente y los datos se contrastan contra SHA antes de reutilizarse.

Python3.12.14; **317 pruebas locales correctas** (309previas+8nuevas) ycompileall. Las nuevas pruebas cubren exhaustividad de ventanas, coordenadas/orientación, subgrupo compartido, longitud inválida, mapeo alternativo, multimapeo, MAPQexcluido y alineamientos parciales. Son controles de software, no experimentos biológicos. La CI por verificar en la cabeza nueva no ejecuta el índice humano.

El alineamiento sintético inicial tardó6,48s. El máximo hijo acumulado en el proceso —incluye extracción del inspector y alineador, no un pico agregado— fue4.758.740KiB (~4,54GiB). No extrapolar este tiempo al control completo. La reconstrucción del referente fue en flujo y se conservan solo427bases únicas de los cuatro intervalos.

Errores técnicos conservados: una transferencia local excedió el límite de argumentos y se repitió con un inventario compacto; un test inicial avisó de un fichero sin cerrar, corregido con context manager antes de la suite final. Sin fallos en los controles del alineamiento. El informe no afirma que los408 caminos remotos no materializados falten del repositorio: solo se recuperó lo necesario para esta ejecución.

```bash
python scripts/audit_stmn2_exon1_mappability.py --inspect RUTA_HISAT2_INSPECT --aligner RUTA_HISAT2_ALIGN --prefix PREFIJO_INDICE_FIJADO --out reports/stmn2-exon1-mappability-20261031 --cache data/cache/stmn2-exon1-mappability-20261031
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

Los argumentos reales están en run.json, con índice ybinarios cotejados en recovered_inputs.json. El helper valida la definición del exón antes de generar las lecturas. No cambió ningún dato del piloto real ni su diagnóstico.

## Siguiente prueba discriminante

El piloto de1M sigue con0soporte para ambas uniones15/8 y0solapamientos aceptados del exon1, aunque existe cobertura posterior del locus. No se atribuye ese patrón a una imposibilidad general del referente para lecturas perfectas. Permanecen abiertas distribución de cobertura, orden del subconjunto, variantes/errores, isoforma y otras propiedades de los datos reales.

La propuesta research/plans/2026-10-31-full-control-coverage-proposal.md fija una **fase nueva de QC del control completo SRR8144907**,37.518.164lecturas publicadas, antes de los otros cinco runs. No es ampliar retrospectivamente el piloto hasta encontrar señal. Exige implementación de modo completo con controles, bins de orden prefijados, integridad/concordancia y recursos; no detenerse según cuentas. Si falla el límite temporal, solo hay ejecución parcial, no biblioteca validada. Si el control completo tampoco cubre el sitio, rechazar aptitud para este contraste sin declarar ausencia biológica.

Esa fase no se ha ejecutado aquí. El contraste sigue bloqueado por cobertura/adecuación del evento. Mismo PR33 revisable, sin merge o cierre automático. PR30 cabeza053ef70ce437cc637ec18278a2c07e3abd6bf58b ymain9c82795d intactos. Sin gastos, contactos, publicación externa, datos clínicos personales, laboratorio o resultados funcionales.

Fuentes técnicas: proyección versionada GENCODEv47 ymanifiestos del índice dentro del repositorio; HISAT2commit0d244324f98de541bce04d45c75e83bc3522f7f4, https://github.com/DaehwanKimLab/hisat2/tree/0d244324f98de541bce04d45c75e83bc3522f7f4. No nueva afirmación bibliográfica o clínica.
