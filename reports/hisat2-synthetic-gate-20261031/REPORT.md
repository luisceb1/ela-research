# HISAT2 y extracción: controles sintéticos — 31/10/2026

## Pregunta y resultado

Plan anterior a ejecutar: research/plans/2026-10-31-hisat2-synthetic-gate.md. ¿El alineador fijado recupera las dos uniones STMN2 con camposNH/XS/MAPQ compatibles y coinciden el parser propio yHTSlib/pysam? **Pasan los controles primarios prefijados**, con un límite de sensibilidad importante que no se oculta ni se corrige retrospectivamente.

Se compilaron y ejecutaron hisat2-align-s yhisat2-build-s2.2.3 desdecommit0d244324f98de541bce04d45c75e83bc3522f7f4. Se extrajeron tres flancos de60bases de la referencia indexada para construir controles artificiales. No son lecturas de un experimento ni datos clínicos. El índice completo se usa para competir contra otras regiones; no se alinea un recorte como si demostrara unicidad genómica.

26lecturas sintéticas se alinearon contra el índice humano; dos más contra una mini-referencia artificial de1500bases con dos copiasidénticas y un locusdistinto. Parámetros congelados:2hilos,-k5,--seed0,--no-temp-splicesite,--reorder; sin sitios inyectados, dta o strandness impuesta. Minirreferencia generada con semilla20261031. No se usa-k1 para fabricarNH1.

## Comprobaciones ejecutadas

| Control | Resultado bajo el filtro original de anclas≥8 |
|---|---|
| Críptica/canónica,50nt con25+25anclas, ambas orientaciones | 4/4 recuperadas exactamente |
| Críptica/canónica,100nt con50+50anclas, ambas orientaciones | 4/4 recuperadas exactamente |
| Lectura exónica continua yN50 | Sin soporte de las dos uniones |
| Misma unión artificial en dos copiasidénticas | Dos ubicaciones, NH2/MAPQ1; excluidas del soporte aceptado |
| Unión artificial única | NH1/MAPQ60/XS+, recuperada |
| Parsing/extracción propios vsHTSlib/pysam | Eventos filtrados idénticos en ambosSAM |
| Repetición completa | genome.sam, mini.sam yresults.json idénticos por bytes |

Los positivos equilibrados producenMAPQ60, NH1 yXS+ en ambas orientaciones de alineamiento; flag16 no se interpreta como hebra transcrita. El control multicopia produce un primarioflag0 y secundarioflag256 conNH2 yMAPQ1. Esto comprueba el comportamiento de esta versión/ejecución, no unicidad exhaustiva para cualquier lectura. El ejemploMAPQ255 del manual no describe estos positivos reales del ejecutable; se conserva su exclusión.

Pysam0.23.3, paquete que expone versiónsamtools1.21, usaHTSlib para parsearSAM yfind_introns para intervalos; el segundo filtro calcula anclas conCIGAR numérico. El parser propio opera sobre texto/regexCIGAR. Comparten la política de filtros, por lo que la concordancia verifica implementación/geometría, no constituye un alineador independiente o evidencia biológica. Wheel descargado envenv de tarea y SHA2564099393fc5097b5081c7efaf46b0109e4f0a8ed18f86d497219a8bf739c73992 cotejado contra metadatos primariosPyPI; sin instalación global.

## Resultado negativo que condiciona el piloto

Desafíos de50nt prefijados, dos orientaciones por caso:

| Ancla izquierda/derecha | Críptica aceptada | Canónica aceptada |
|---|---:|---:|
| 7/43 | 0/2 | 0/2 |
| 8/42 | 2/2 | 0/2 |
| 15/35 | 2/2 | 2/2 |
| 20/30 | 2/2 | 2/2 |
| 25/25 | 2/2 | 2/2 |

Las dos lecturas canónicas8/42 quedan sin alinear; las crípticas tienen8M5607N42M. **Exigir8bases en el extractor no garantiza igual recuperación del alineador para ambas uniones.** Esta asimetría puede sesgar una razón de cuentas. No se calcula esa razón y no se transforma un control perfecto en estimación de sensibilidad clínica o en corrección cuantitativa de sesgo.

Los resultados originales se conservan con≥8, conforme al plan. Para la **fase futura aún no ejecutada**, pilot_contract.json fija primaria≥15 y sensibilidad≥8, manteniendo los demás filtros, para que la política no se elija al ver cuentas reales. Es una decisión prospectiva de control técnico; no demuestra igual sensibilidad ante errores, calidad variable o todos los repartos de anclas. Antes del piloto debe implementarse esa parametrización en ambos extractores; no basta con modificar una etiqueta del informe. Los efectos, PSI y comparaciones biológicas siguen fuera de esta fase.

## Recursos y reproducibilidad

Compilación68,63s, máximo hijo504.072KiB. Primera ejecución de alineamiento humano sintético11,49s, máximo hijo observado4.633.708KiB (~4,42GiB), dentro del límite6GiB; minirreferencia y comandos limitados a2hilos y600s. El campo de memoria se registra como máximo de hijos acumulado, no medición separada de cada comando. No extrapolar28lecturas artificiales al coste de un millón de lecturas reales. Disco dentro del presupuesto previo, más50GB libres al verificarlo.

Python3.12.14. **301pruebas locales correctas** (295previas+6), compileall. Las pruebasoffline no instalanPySAM ni ejecutan el índice humano; la comparaciónHTSlib fue ejecutada realmente en elvenv y queda aparte enSAM/resultados/comandos. Las versiones del binario, hashes de fuentes/controles/salidas, ruedaPyPI y semillas están registradas. Dos alineamientos completos repetidos sin cambiar datos/parámetros producenSAM yresults.json idénticos. No fallos de ejecución; la asimetría de anclas se registra como resultado negativo técnico.

```bash
python scripts/hisat2_synthetic_gate.py prepare --binary data/cache/hisat2-source-20261031/hisat2-0d244324f98de541bce04d45c75e83bc3522f7f4/hisat2-inspect-s --prefix data/cache/hisat2-index-20261031/extracted/hg38/genome --out reports/hisat2-synthetic-gate-20261031
python scripts/run_hisat2_synthetic_controls.py --source data/cache/hisat2-source-20261031/hisat2-0d244324f98de541bce04d45c75e83bc3522f7f4 --genome data/cache/hisat2-index-20261031/extracted/hg38/genome --out reports/hisat2-synthetic-gate-20261031
data/tools/synthetic-gate-venv/bin/python scripts/hisat2_synthetic_gate.py compare --out reports/hisat2-synthetic-gate-20261031
python -m unittest discover -s tests -v
```

Controles.json conserva secuencias/expectativas; synthetic_reads.fastq ymini_reads.fastq contienen **solo lecturas artificiales**. Los índices pequeños de la minirreferencia se regeneran, no se incorporan aGit. Ningún FASTQ deGSE122069 descargado/procesado en esta fase.

## Continuación

Se amplía el mismoPR33, sin merge/cierre automático. Main9c82795d yPR30 cabeza053ef70ce437cc637ec18278a2c07e3abd6bf58b intactos. Sin contactos, gastos, clínica personal o laboratorio.

Siguiente prueba: preparar/ejecutar el piloto técnico del primer controlSRR8144907, con política15/8 ya prefijada y límites del plan previo. ComprobarMD5 del archivo completo y añadirSHA256 antes de procesar el primer millón en flujo; medir recursos yQC sinSAM/BAM completo ni contraste biológico. Cobertura escasa significa no evaluable, no ausencia molecular. No sustituir errores/calidades reales por el éxito de estas lecturas perfectas.

Fuentes técnicas primarias: HISAT2commit0d244324f98de541bce04d45c75e83bc3522f7f4 (fuente/manual en la copia fijada; https://github.com/DaehwanKimLab/hisat2/tree/0d244324f98de541bce04d45c75e83bc3522f7f4); PyPIpysam0.23.3 (https://pypi.org/pypi/pysam/0.23.3/json), metadatos/rueda registrados. No nueva afirmación bibliográfica o clínica.
