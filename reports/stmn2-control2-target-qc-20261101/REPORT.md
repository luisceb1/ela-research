# QC técnico del soporte STMN2 en SRR8144908 — 01/11/2026

## Evidencia

Plan previo: `research/plans/2026-11-01-stmn2-selected-replay.md`, guardado antes del análisis real en commit 920414df9a8ea96ab580447f31502b1557575282. Pregunta: ¿los cinco bloques fijados reproducen las cuentas previas y qué atributos técnicos agregados tienen sus candidatos? Predicción refutable: canónica/críptica 13/3 con anclas ≥15 y 15/4 con anclas ≥8. Fracaso ante discrepancia de identidad, selección, finalización, cuentas, parsers/histogramas o recursos. No se fijó un umbral posterior para calificar las observaciones como biológicamente verdaderas.

Fuente publicada de cultivo SRR8144908, GSM3454243, grupo publicado siControl2. Archivo ya procesado, restaurado con MD5 0cd29fe9f8bdf1a6f3596891b783990d  y SHA256 ed2f2f4a30b7f448c246029b0407e20e142493b2d74345e674c4e7b3c3e5527f. Índice restaurado idéntico en sus nueve miembros; archivo comprimido SHA256 1848784403a0fb3ee7735b2f891d8be96fd2782e08aed3d8212d922666f077a5. Las restauraciones son operaciones sobre los mismos insumos, sin añadir muestras.

Se escanearon las 54.292.655 lecturas para seleccionar ordinales y verificar EOF/CRC; solo 4.292.655 lecturas fueron enviadas de nuevo al alineador. Intervalos originales (1-based inclusivos): 1–1000000;17000001–18000000;37000001–38000000;42000001–43000000;54000001–54292655. Incluyen el primer bloque como contexto negativo y todos los bloques previamente crípticos a8. Selección post hoc para QC; no muestreo aleatorio. Los bins del nuevo flujo corresponden a estas ventanas, no a una nueva biblioteca.

Reproducción exacta 13/3 a15 y15/4 a8, cuentas e histogramas concordantes entre el contador texto/CIGAR y PySAM 0.23.3/HTSlib 1.21 numérico. Mismo HISAT2 v2.2.3, fuente 0d244324, binario SHA256 736b75476c6b0b041d7520821e16435c7e9afcdde5fe7863d20992e3fb044ee2, índice/semilla 0 y filtros. `--no-temp-splicesite` y `--reorder` conservados. Identificadores/secuencias solo en flujo transitorio; sin QNAME, SAM/BAM o variables clínicas exportados. Comandos completos en `replay-command.json` y `execution/full-control-results.json`.

Histogramas: cada entrada expresa valor: número de observaciones aceptadas, sin identificadores. Anclas izquierda/derecha completas en `target-qc-histograms.tsv`.

| Ancla mínima | Objetivo | Observaciones | MAPQ | NM | AS | Bases softclip | Flag duplicado |
|---|---|---|---|---|---|---|---|
| 15 | canonical | 13 | 60: 13 | 0: 13 | -2: 12, -4: 1 | 0: 12, 1: 1 | 0: 13 |
| 15 | cryptic | 3 | 60: 3 | 0: 3 | 0: 3 | 0: 3 | 0: 3 |
| 8 | canonical | 15 | 60: 15 | 0: 15 | -2: 13, -4: 2 | 0: 13, 1: 2 | 0: 15 |
| 8 | cryptic | 4 | 60: 4 | 0: 4 | 0: 4 | 0: 4 | 0: 4 |

## Interpretación

El replay aporta reproducibilidad técnica sobre la selección fijada. En las cuatro observaciones crípticas se registran MAPQ 60, NM 0, AS 0 y cero bases de softclip. La observación adicional con política8 tiene ancla derecha13; la política15 la excluye sin cambiar filtros. Entre las tres primarias, las anclas izquierdas son21 (dos observaciones) y22 (una), y las derechas30 (dos) y29 (una); son marginales, no pares reconstruidos. Estos atributos no muestran un problema de mismatches o softclip en los alineamientos aceptados; no agotan las explicaciones técnicas o biológicas del soporte bajo. Las cuatro observaciones con anclas ≥8 incluyen las tres con anclas ≥15; no sumarlas como siete. Las cuentas del control completo permanecen en 111/3 y 154/4, y su JSON original conserva SHA256 cb26604160e43cdc04d2eab0a2525fc02f296059d70f5e0d9d731a32d9f6b4a7. El contexto canónico no es otra réplica y esta fase no es replicación externa ni validación funcional.

## Limitaciones y resultados negativos

No se estiman tasas, efecto, PSI molecular, enfermedad o rescate funcional. Los marginales agregados no reconstruyen moléculas ni combinaciones de atributos por lectura. Ausencia de flag de duplicación no acredita moléculas independientes; no hay UMI. Las etiquetas ausentes permanecen como `missing`, nunca 0. La selección está enriquecida por el resultado previo y no permite comparar tasas con el control completo.

La regla de cobertura 20 no se reaplica a la selección: su denominador 16<20 aparece como False en la salida del motor genérico, sin revertir el denominador 114≥20 del control completo. `replay_complete=true` solo cubre la selección; `complete_library=false` en ambos contadores impide confundirla con un nuevo alineamiento completo. El mapa biblioteca→cultivo/lote/pareamiento sigue pendiente; se conserva la declaración publicada de 3 réplicas por condición sin convertir bibliotecas, bloques o lecturas en réplicas. No inferencia.

Error de desarrollo conservado: la primera prueba artificial de múltiples intrones tenía el inicio cinco bases desplazado; se corrigió antes de cualquier replay real. La prueba corregida y el preflight con PySAM pasaron. La restauración registró un payload HTTP de rango truncado: el descargador preexistente reintentó ese tramo una vez y obtuvo 98 rangos, MD5/SHA válidos en 801,646 s<1800 s. Este reintento de transporte no fue un segundo replay. Recibo en `restore-fastq-download.json`; errores de ejecución en JSON/logs, sin reintento de fase. Un intento auxiliar de inspeccionar procesos con `ps` no estuvo disponible (`fatal library error, lookup self`); no se utilizó como medición de recursos.

## Pruebas, recursos y trazabilidad

392 pruebas de software locales antes del replay, 14 nuevas; dos pasadas sintéticas con proyección estable idéntica y parsers concordantes. CI 3.11/3.12 del código previo 920414d: workflow 41254002525, 392 tests en cada versión. Las pruebas no son experimentos. Reexportación y seis rechazos de copias alteradas se verifican por separado con `verify_stmn2_selected_qc_artifacts.py`; acta en `artifact-verification.json`. Solo se modifican copias en memoria para esos controles negativos. Nueve módulos ejecutados cotejados por Git blob remoto y SHA256 en `execution-code-manifest.json`.

Tiempo observado de fase, incluidas comprobaciones de identidad: 371.380s≤600s; prealineamiento 18.878s. Afinidad CPU [0, 1]; caps virtuales 5 GiB+512 MiB+256 MiB, presupuesto de disco 15 GiB y reserva 8 GiB. MáximoRSS padre 31148KiB, máximo observado hijos 4642400KiB: no representan RSS simultáneo combinado. Watchdog: []. Restauración separada del reloj de fase, sin nueva biblioteca ni aumento de recursos. `launch-result.json` registra salida y cero reintentos.

Reproducción offline de los artefactos agregados, sin FASTQ ni alineamiento nuevo:

```bash
python -m unittest discover -s tests
python scripts/verify_stmn2_selected_qc_artifacts.py reports/stmn2-control2-target-qc-20261101
```

## Siguiente prueba discriminante

La siguiente puerta es revisión del PR #33 y de estos artefactos frente al plan fijado. Una afirmación biológica necesitaría una medición ortogonal publicada y unidades experimentales independientes identificadas; este replay no resuelve esa dependencia. Conservar el bloqueo de inferencia y decidir el siguiente contraste en un plan separado antes de más bibliotecas. Sin merge/cierre automático; PR #30 separado.
