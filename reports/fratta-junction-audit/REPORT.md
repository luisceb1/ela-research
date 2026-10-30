# Fratta: deduplicación y versiones del índice — 29/10/2026

## Evidencia y resultado

**El paquete anterior reproduce el bloque Rmd 2685–2694: los24 campos numéricos agregados cotejados coinciden.** No representa una cohorte nueva, replicación independiente o validación funcional. Se han auditado las transformaciones de un BED procesado de la misma cohorte GSE126542 usada en expresión; no alineamientos ni moléculas.

| QC del archivo fuente | Resultado |
|---|---:|
| Filas brutas |241|
| Filas completas únicas |69|
| Repeticiones exactas retiradas |172|
| Muestras técnicas en la tabla |16|
| Muestras clasificadas emparejadas |14:7 pares |
| No clasificadas excluidas del contraste |2|
| Celdas muestra×clase presentes |69 de 96 |
| Celdas ausentes rellenadas con0 por método autor |27|
| Filas fuente únicas con cuenta explícita0 |0|
| Colisiones entre filas distintas de misma muestra/clase |0|

El relleno de 0 está declarado en el código autor y se reproduce fielmente. **No implica haber observado experimentalmente cero lecturas en una combinación ausente**, ni ausencia molecular. No se confunde el nombre del archivo BEDcon una convención de coordenadas verificada: los campos se preservan para deduplicar, sin conversión/reanotación.

## Fórmulas: qué se reproduce y qué cambia

Rmd 2685–2694 aplica deduplicación completa y pivot por muestra, etiqueta y cuenta, con relleno de ausentes. STMN2 usa cuenta críptica dividida por críptica+anotada. UNC13A suma tres clases crípticas —3prime,5prime,5prime_2— y divide por esa suma+anotada. Este es el bloque que reproduce el paquete recibido.

Pero Rmd 2764–2766 contiene otra fórmula UNC13A, sin 5prime_2, en un gráfico posterior asociado a otro análisis. **No hay una fórmula única de UNC13A para todo el Rmd.** Se localiza esa diferencia sin leer el archivo alélico ni ejecutar el Rmd completo. No se decide que una versión sea la verdadera proporción molecular ni se atribuye al gráfico anterior la fórmula del posterior.

| Gen/método | Índice medio TP | Índice medio TN | Cambio medio TN−TP |
|---|---:|---:|---:|
| STMN2, deduplicado |0,89%|65,65%|+64,76 puntos |
| UNC13A, tres clases (principal) |1,20%|73,87%|+72,67 puntos |
| UNC13A, dos clases (sensibilidad) |1,13%|73,13%|+72,00 puntos |
| UNC13A, sumando duplicados (contraejemplo) |0,57%|64,38%|+63,81 puntos |

La sensibilidad de fórmula reduce el cambio medio de UNC13A en 0,6730 puntos; el contraejemplo de sumar duplicados lo reduce en 8,8675 puntos. Es una consecuencia matemática de estas entradas, no estimación de sesgo biológico o efecto clínico. Los siete pares mantienen dirección positiva con ambas fórmulas en esta fuente; no demuestra titulación, mayor sensibilidad de una diana ni recuperación tras tratamiento.

Las multiplicidades de duplicación no son uniformes entre clases: STMN2 aparece 3 veces por fila única en ambas clases y por eso sumar sus duplicados deja el cociente igual, aunque triplica sus cuentas. En UNC13A son 2 para 3prime, 4 para 5prime y 5prime_2, y 5 para anotada. Por eso sumar las241 filas en vez de retirar repeticiones altera el índice. Ninguna repetición es evidencia de una lectura adicional independiente.

## Trazabilidad y controles

Fuentes primarias públicas, bytes verificados por SHA256 **y** Gitblob:

- BED:blob89de715d8640382800cef959be064b3af8e76eee,18037bytes, SHA256b9a46c7e4f388d1e871a293b0b6da5c7ae5689ace7fc82d8ead38d3e41a6b447.
- Rmd:blob1534a7312bcee102fae9a60bb450ddd37da5c96c,148855bytes, SHA2563c46c164af6572bef28507b707f39d996d687abb06da00bf5468f89d0d491502.

Enlaces/localizadores en sources.json. Los originales permanecen en caché; no se republican matrices por muestra o el Rmd completo. La tabla esperada se lee solo de resultados/resumen_splicing.csv del ZIP recibido; no se accede a miembros por caso/genética ni a archivos alélicos enlazados en el Rmd.

Se deduplican filas completas exactas. Si dos filas distintas comparten muestra/clase, se rechaza el pivot en vez de sumarlas o seleccionar una. Las claves completas de muestra se tratan como identificadores opacos, sin usarlas como variable clínica; no se emparejan dos prefijos distintos por compartir S1. Solo entran siete pares completos y condiciones técnicas reconocidas. Un denominador cero es no estimable, no índice 0. Las pruebas exploran esos contraejemplos.

Las p de inversión de signos y Wilcoxon exacto del paquete también se reproducen como parte de los24 campos, bajo sus supuestos y sin nuevo ajuste por multiplicidad. No sustentan causalidad, proporción molecular, eficacia o novedad. Los índices suman clases de uniones, potencialmente de ambos extremos del mismo transcripto; no equivalen a fracciones absolutas de isoformas, células o proteínas.

## Reproducción, errores y estado

Plan previo: research/plans/2026-10-29-fratta-junction-audit.md. Código: scripts/audit_fratta_junctions.py. Comando: `python scripts/audit_fratta_junctions.py --cache /ruta/fratta --upload /ruta/paquetes`; `python -m unittest discover -s tests -v`. La reproducción completa usa SciPy ya fijado en requisitos de issue14; pruebas offline con biblioteca estándar.

Diez pruebas nuevas; esta rama PR29pasa **124 tests** (105 de base + 19 nuevos de las dos etapas). No incluye los166 de PR28como si estuvieran integrados. Resultados: aggregate_indices.tsv, sensitivity.tsv, comparison.tsv, summary.json, errores y hashes en run.json. No hay datos clínicos individuales exportados, archivos alélicos leídos ni ejecución del código recibido.

La primera validación rechazó el supuesto incorrecto de prefijo uniforme en nombres de muestra. Se corrigió conservando la clave opaca completa y se añadió un control contra emparejamiento entre prefijos distintos. Los hashes finales de fuentes quedaron verificados tras errores de transporte/decodificación, registrados aparte en errors.json; no se modificó el BEDpara hacerlo pasar.

## Siguiente tarea

La deduplicación/fórmula de este bloque queda auditada. Issue14sigue abierta: reconstruir metadatos técnicos biblioteca→experimento/diferenciación de GSE121569 y evaluar qué modelo puede reestimarse sin pseudorreplicación. Mantener separados los resúmenes publicados ya extraídos del ajuste estadístico aún no ejecutado. Si el mapa no es verificable, registrar bloqueo y no inventar seis diferenciaciones a partir de seis etiquetas de réplica. Sin contactos, gastos, laboratorio o merge automático.
