# Parametrización GSE122069 — 31/10/2026

## Evidencia

Preparación de software ejecutada en Python 3.12.14, sobre PR33 fecaeb5d3b66e2766afefaca13e25fab90a326b3. Pregunta, predicción refutable y controles anteriores al preflight en [plan](../../research/plans/2026-10-31-gse122069-parameterization.md). Sin nuevas búsquedas biológicas, FASTQ reales, ejecuciones HISAT2 o repetición del control completo. PR30 y main no modificados.

Se elimina la selección rígida del primer control en configuración, recibos de descarga, runner y resumen. La CLI valida los bytes exactos del manifiesto de seis cultivos (SHA256 b5ed1bcfaa32132ae3e05af183dcf16d9b1dc60639db1d4827934c944c40ccbd). Accession, GSM, tamaño, MD5, estado verificado y SHA propio del recibo deben corresponder a la biblioteca seleccionada; después el runner verifica el archivo antes de leerlo. Se rechazan identidades cruzadas, muestras desconocidas, conteos completos erróneos, presupuestos inválidos y salidas de ejecución no vacías. La configuración describe una solicitud, no una ejecución realizada.

El modo `plan` del runner y `--plan-only` del descargador generan metadatos sin abrir FASTQ, índice o binario. Se ejecutó realmente la planificación del segundo control usando como ruta de FASTQ `MUST_NOT_OPEN`, inexistente: [configuración](next-control/execution-config.json), [plan de descarga](next-control/download-plan.json). Un plan no es un recibo verificado y no habilita procesamiento. El ETag y el SHA propio del segundo archivo siguen pendientes.

| Comprobación ejecutada | Resultado |
|---|---|
| Comando HISAT2 histórico del primer millón | Lista argv idéntica |
| Comando HISAT2 histórico del control completo | Lista argv idéntica |
| Resumen histórico del control completo, sobre JSON archivados | Todos los campos iguales |
| Identidad del plan de descarga del primer control | URL/GSM/run/bytes/MD5 iguales al recibo histórico |
| Recibo histórico del primer control | Sigue siendo aceptado para su identidad |
| Mismo recibo asignado al segundo control | Rechazado antes de abrir FASTQ |
| Conteo completo del segundo control | 54×1.000.000 + 292.655, sin fabricar esas lecturas |
| Uso del piloto del primer control en resumen del segundo | Rechazado |

La primaria sigue siendo anclaje≥15, sensibilidad≥8, misma geometría chr8+, filtros MAPQ20–254/NH1/XS, seed0, k5, dos CPU, `--no-temp-splicesite --reorder`, sin strandness/sitios inyectados/deduplicación. Los extractores base y el runner histórico1M no se modificaron; sus blobs, dos fixtures SAM y manifiesto se cotejaron con la cabeza de partida. Los presupuestos por defecto siguen1800s. El valor2700s exige argumento explícito; no cambia por accession o fracaso. No se ha aplicado a un análisis real nuevo.

## Controles sintéticos y negativos

[Preflight ejecutable](../../scripts/preflight_gse122069_parameterization.py): se reutilizan dos SAM sintéticos fijados (26 consultas y2 consultas/3 registros), **28 consultas únicas**. Se comprueban en dos contextos de configuración, sin atribuirlos a lecturas observadas de ningún SRR. Texto/CIGAR y PySAM0.23.3/HTSlib1.21 concuerdan por bin7, total y objetivos. Matrices completas de ambos contextos repetidas dos veces: proyección científica estable idéntica por bytes. Métricas de memoria separadas, no exigidas iguales. No se suman consultas repetidas como muestras nuevas.

Con anclaje15, el fixture genómico conserva8 observaciones canónicas y8 crípticas; a8 conserva8/10. El fixture mini conserva1 intrón elegible y0 objetivos. Son controles de regresión, no una nueva calibración de sensibilidad. [Matriz1](synthetic-matrix-repeat1.json), [matriz2](synthetic-matrix-repeat2.json), [mediciones](measurements.json).

Cinco negativos explícitos se ejecutaron y rechazaron: recibo cruzado, número completo erróneo, accession desconocida, límite por encima del máximo y resumen de otra muestra. [Errores esperados](negative-controls.json). Las pruebas añaden controles de manifiesto alterado, duplicados, conteos inválidos, particiones, ausencia de QC del locus y preservación de salidas/recibos anteriores.

Hallazgo de revisión del transporte: comprobar30min antes de cada petición no imponía por sí solo un límite global a hilos/IO. La entrada normal del descargador ahora supervisa un subproceso completo con plazo1800s, mata su grupo al vencerlo y deja el recibo no verificado. No reinicia ni amplía presupuesto. Un proceso sintético sin red, configurado para dormir, fue terminado con plazo de prueba20ms; [registro](synthetic-transport-timeout.json). Esto es un negativo de software, no una descarga fallida del segundo control. JSON incompleto del subproceso, salida0 sin recibo verificado o identidad incorrecta fallan de forma conservadora; un recibo previo no se sobrescribe. La ruta interna `--transport-child` solo la utiliza el supervisor; los comandos propuestos usan la entrada supervisada.

**374 pruebas locales y compileall correctos** (349 anteriores +25 nuevas), no374 experimentos. [Log](tests.txt). Sin errores inesperados en esta fase; se conservan rechazos esperados y timeout sintético. La CI se verifica por SHA en el PR.

## Reproducción y límites

```bash
python -m unittest discover -s tests -v
python scripts/preflight_gse122069_parameterization.py
python scripts/gse122069_full_control.py plan --manifest reports/gse122069-resource-plan/input_manifest.json --out /tmp/control2-plan --run-accession SRR8144908 --max-reads 54292655 --complete-library --phase-deadline-seconds 2700 --fastq MUST_NOT_OPEN
```

El preflight usa el entorno PySAM registrado y los SAM sintéticos; no realinea ni abre archivos de lecturas públicas. El timeout sintético se registra por separado. Parámetros, Python, paths de caché y espacio observado en [entorno](environment.json); solo se comprobó existencia de índice/binario, no se revalidaron sus bytes aquí. Antes de una fase real, el runner volverá a verificar sus hashes. Los manifiestos anteriores se verifican en sus commits, incluidos167d370 para el control completo y fecaeb5 para diseño: no contra código o STATE posteriores.

Validación de software con controles sintéticos. No replicación externa biológica, PSI molecular, efecto de TDP-43, función o clínica. El diseño biológico sigue sin mapa explícito de cultivos/lotes/pares; la declaración previa de tres réplicas por condición no se contradice. No se reabre la búsqueda cerrada sin fuente nueva.

## Siguiente prueba discriminante

Preparada la propuesta de una única fase nueva para SRR8144908/GSM3454243/SRX4965535, siControl2:54.292.655lecturas. [Comandos prospectivos](next-control/commands.json) y [plan de ejecución](../../research/plans/2026-10-31-gse122069-control2-execution.md). Aún faltan cabeceras actuales/ETag fuerte y revisión de recursos antes de descargar. No reutilizar ETag del primer control ni inventar SHA del segundo.

Después de esa revisión, una pasada completa fijada, con límite45min explícito y sin otros cuatro runs, podrá comprobar cobertura técnica y concordancia; regla20 sin imputar ausencia, sin inferencia. El código no lanza automáticamente esa fase. Cualquier timeout conserva solo parciales no verificados/no completos según corresponda; recuperación requiere decisión separada. No contactos, costes, publicación externa, laboratorio, merge o cierre de issues.
