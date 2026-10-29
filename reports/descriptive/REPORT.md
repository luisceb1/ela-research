# Comparaciones descriptivas y sensibilidad — 2026-10-29

Evidencia: **exploratoria**. Continúa los P1 del backlog tras auditoría (#3) y mapeo (#4). Sin pruebas de hipótesis, p-valores, intervalos de confianza, pseudocuentas ni mezcla de cultivo y cerebro.

## Evidencia

Se ejecutaron 132 contrastes descriptivos de cultivo (11 transcritos × 2 medidas × 3 denominadores × 2 brazos) y 180 filas de sensibilidad cerebral (10 transcritos × 2 medidas × 3 denominadores × 3 etiquetas frente a CTL). Estos recuentos describen cálculos, **no réplicas**. Las cuentas totales fraccionarias se conservaron sin redondear. Dos ejecuciones produjeron tablas con hashes idénticos (`reproducibility.json`). Pasan las 30 pruebas offline; las CI de los PR #3 y #4 también terminaron con éxito.

Las 12 columnas de uniqueCounts tienen máximo común divisor **2** en sus valores no nulos. Es una propiedad de la escala depositada; su causa no se ha establecido. No se ha dividido por dos ni interpretado como número de moléculas/lecturas independientes. En particular, el filtro `>=2` no discrimina entre cuentas positivas de estas matrices.

### Cultivo GSE310723

La estructura STMN2 `BambuTx9249` tiene dirección mayor en TDP43KD en los 12 contrastes de su tabla (bruto, por millón asignado y cuota del gen; dos medidas y dos brazos). El ENST principal STMN2 `ENST00000220876.12` tiene dirección menor en los 12. Esta concordancia entre medidas del mismo experimento no es replicación independiente.

| Transcrito | Brazo | Cociente KD/Ctrl por millón, uniqueCounts | Cociente KD/Ctrl por millón, counts |
|---|---|---:|---:|
| STMN2 BambuTx9249 | +5Aza | 2,854 | 2,723 |
| STMN2 BambuTx9249 | sin 5Aza | NA: control 0 | NA: control 0 |
| STMN2 ENST00000220876.12 | +5Aza | 0,155 | 0,165 |
| STMN2 ENST00000220876.12 | sin 5Aza | 0,193 | 0,209 |
| UNC13A ENST00000519716.7 | +5Aza | 1,019 | 1,202 |
| UNC13A ENST00000519716.7 | sin 5Aza | 1,246 | 0,794 |

El cero del control del candidato sin 5Aza se mantiene como denominador indefinido, sin inventar un fold change infinito o estabilizado con pseudocuenta. Para UNC13A, incluso la dirección sin 5Aza cambia con la medida elegida. No hay base para afirmar reducción consistente de ese ENST en estas bibliotecas de cultivo.

### Cerebro GSE315972

Cada etiqueta dispone de dos bibliotecas de donante según el diseño depositado. Se retira una biblioteca del grupo o del control por turno; la amplitud resultante **no** es un intervalo de confianza ni una validación poblacional.

Para el ENST principal STMN2, el cociente de medias por millón asignado (uniqueCounts / counts) frente a CTL es 0,709 / 0,736 en ALS; 0,536 / 0,540 en ALS-ci; 0,812 / 0,769 en ALS-C9. El cociente queda por debajo de 1 bajo las retiradas examinadas en estas dos medidas. Esto no controla composición celular, RNA quality ni otros factores, y no reproduce la estructura BambuTx9249, que no está asignada en el catálogo cerebral.

Para UNC13A ENST00000519716.7 en ALS, el cociente de medias por millón es **0,872** en uniqueCounts y **1,058** en counts. El rango de sensibilidad abarca 1 en ambas medidas (0,623–1,121 y 0,852–1,264). Por tanto, ni la dirección del contraste ALS/CTL es estable frente a estas decisiones técnicas y bibliotecas. Las otras etiquetas se conservan separadas en la tabla; no se agregan para mejorar un resultado.

## Interpretación

La predicción exploratoria fijada antes de este contraste se cumple descriptivamente para la dirección del candidato STMN2 y del ENST principal dentro de las bibliotecas de cultivo. La comparación ya ha encontrado un resultado útil negativo: una afirmación genérica de caída de UNC13A no resistiría la elección de medida ni, en cerebro ALS/CTL, la retirada de una biblioteca.

El ajuste por suma de cuentas solo examina sensibilidad a un denominador de biblioteca; no demuestra control de diferencias globales de ARN, número de células, composición, degradación, sesgo de asignación o carga TDP-43. La cuota dentro del gen no es PSI y no equivale a tasa de uso de un exón críptico.

## Limitaciones y alternativas

- n=1 biblioteca/condición en cultivo; los dos brazos de 5Aza no son réplicas. Los contrastes se seleccionan tras un mapeo exploratorio de la misma fuente.
- n=2 por etiqueta cerebral, grupos heterogéneos y covariables no auditadas; no hay inferencia estadística ni atribución causal a TDP-43.
- No se verificó la causa de la escala de uniqueCounts ni soporte en BAM/FASTQ. Un alto contraste relativo de cuentas escasas no es validación de isoforma ni actividad neuronal.
- Las sumas de counts y uniqueCounts tienen distinto contenido de asignación. `per_million_assigned` es un ajuste calculado, no el CPM del depositante.
- Los rangos de retirada exploran influencias en estas bibliotecas, no incertidumbre poblacional. Un rango que no cruza 1 no implica significación ni replicación externa.
- No hay intervención, prueba de rescate molecular, recuperación funcional ni beneficio clínico.

## Siguiente prueba discriminante

Priorizar la identidad del candidato STMN2: contrastar su unión/terminación con coordenadas de fuentes primarias independientes y ensamblaje confirmado. La estructura no se llamará críptica validada si esas coordenadas no coinciden. Después, comprobar soporte de uniones y límites de descubrimiento usando únicamente datos públicos técnicamente accesibles, sin gastos ni nuevos datos clínicos personales.

Investigar en paralelo documental la semántica/escala de `uniqueCounts` en bambu 3.2.6 y en la exportación del estudio. Hasta resolverlo, conservar unidades originales y evitar umbrales interpretados como moléculas. Si la identidad del evento o la escala no se resuelve, registrar el bloqueo y avanzar a evidencia funcional independiente publicada.

Reproducción: `python scripts/geo_audit.py`; `python scripts/map_isoforms.py`; `python scripts/describe_targets.py`; `python -m unittest discover -s tests -v`. Métodos fijados en `research/plans/2026-10-29-descriptive.md`. Estado: ejecutado, pendiente revisión de PR; no validado clínicamente.
