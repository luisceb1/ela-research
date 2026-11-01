# STMN2: la proporción de cuentas no reproduce PPAU — 01/11/2026

## Evidencia

La comparación preregistrada **falla en las doce bibliotecas**: cero aceptadas, doce rechazadas, ninguna indeterminada. La diferencia absoluta máxima es0,17013297835212804 en unidades de proporción (17,013297835212804 puntos porcentuales). El umbral se conservó en1e-6; no se cambiaron grupos, denominador, escala o selección de bibliotecas para lograr concordancia.

Se detiene la aceptación según la regla prospectiva, conservada en execution_plan.json y en el plan del commit b968b7a8aa7878e41c7da297702c525d6056f260. La salida correcta del programa indica que pudo realizar la comparación; **accepted=false** indica que la hipótesis técnica no pasó. Un test de software correcto no convierte ese resultado científico/metodológico en positivo.

Entradas: las dos matrices completas del mismo directorio Humphrey/Zenodo15538003, cada una con43.630filas. Hay exactamente dos grupos para ENSG00000104435.14 en ambas tablas. Se usó como numerador ENSG00000104435.14_1 y como denominador la suma de todos los grupos del gen de la matriz de cuentas, no la matriz génica GEO. Las doce columnas enlazan con la tabla técnica de la auditoría anterior. No se imputaron denominadores cero ni se omitió ninguna biblioteca.

La tabla per_library_comparison.tsv contiene GSM, etiqueta de biblioteca, condición, numerador, denominador, proporción desde cuentas, PPAUoriginal, diferencia y decisión. comparison_table.md muestra los mismos resultados con nueve decimales. Para ilustrar la discrepancia sin promediar grupos:

| Biblioteca | Proporción desde cuentas | PPAU autores | Diferencia absoluta |
|---|---:|---:|---:|
| CTRL-1 | 0,000259062 | 0,000111349 | 0,000147714 |
| TDP-2 | 0,794718650 | 0,624585672 | 0,170132978 |

Son proporciones de abundancia estimada, no fracciones de células enfermas, moléculas independientes, PSI de unión ni medidas de función.

## Interpretación

La expectativa propuesta en la fase anterior era incorrecta: **cuentas/suma(cuentas) no es la PPAU que define el método de autores**. El script primario scripts/tx_to_polya_quant.R de frattalab/PAPA calcula PPAU a partir de TPMporgrupo/suma(TPMdelgen). Su exportación de cuentas, en cambio, aplica el modo lengthScaledTPM de tximport. Compartir etiquetas de exones finales no convierte ambas mediciones en equivalentes.

Antes de calcular los resultados se leyó el código, se fijó que la PPAUestá en proporciones y se guardó measurement_definition.json. A pesar de esa advertencia, se ejecutó sin cambios el contraste prospectivo ya comprometido, para preservar su resultado negativo. No se buscó una escala que minimizase diferencias ni se sustituyeron las cuentas por TPM después de observar los fallos.

La definición metodológica explica por qué no debía suponerse la igualdad. No se ha repetido el pipeline histórico R/Salmon ni se ha cuantificado la contribución exacta de longitudes u otros pasos. Por tanto, no se atribuye un error a la tabla de autores, ni se afirma haber reproducido todavía la PPAU mediante sus insumos adecuados.

## Recuperación, trazabilidad y límites

Se reutilizaron la matriz de cuentas y el mapa de bibliotecas ya verificados: sin nueva auditoría de las mismas muestras. Solo se recuperó el miembro PPAU identificado en el índice guardado de Zenodo15538003 mediante HTTP206, Content-Range exacto, longitud, descompresión limitada y CRCcorrecto. Tráfico2.835.188bytes; miembro7.607.537bytes. SHA256c4828ee5edd25a8c6c29719366735df268a669d8d5ba8d075dd015bdccd5ac42. Recibo en retrieval.json.

La matriz de cuentas conserva SHA2565b25fdea528e99ba647fd20b0d5f4ca5aab401d0e373df131bdc2145ded1a296 y el mapa de muestras818b8f6553a3ea1b44e0c1cf511c5dec1fcc35f7ccd68e2d8b45af6c46087573. Ambos se verificaron antes de calcular. Los originales permanecen en caché temporal; Git contiene solo proyecciones, hashes, código propio y síntesis. No se añade el script completo de terceros.

Código de definición inspeccionado en frattalab/PAPA, commit d2ed20d217d9e3e397fa92dbcf9dc72a000f37b8, blob8e0319b6a18ab6fdeb6fe91a1314cb02dd480b36. Es una revisión fijada del código disponible; no se ha reconstruido el entorno histórico exacto del artículo.

Se mantienen las limitaciones experimentales: bibliotecas de una línea WTC11, intervención antes de diferenciar, mapa de lotes/diferenciaciones no reconstruido, ausencia de ensayo de rescate. No se ejecutaron medias de grupos, contrastes inferenciales, p-valores, alineamientos, análisis de UNC13A, laboratorio o contactos. Este resultado no cambia por sí solo la evidencia biológica publicada sobre STMN2.

## Verificación y errores

Dos ejecuciones offline del código final produjeron result.json y per_library_comparison.tsv idénticos por bytes. Nueve controles nuevos comprueban, entre otros, discrepancias entre mediciones, conservación de tolerancia, inclusión de todos los grupos del gen, rechazo de duplicados y manejo de denominadores cero. Pasan20tests locales de los dos módulos añadidos en esta PR y compileall. La suite histórica no se materializó completa localmente.

La cabeza anterior de PR36,b968b7a, ya pasó CI en Python3.11/3.12; se observaron415tests en el log3.12. Esa CI no acredita esta nueva cabeza: el estado final se verificará por SHA después del push. El contraste aritmético no concordante es un resultado previsto por el diseño, no una excepción ocultada del programa.

Comandos:

```bash
python scripts/fetch_stmn2_papa_ppau.py
python scripts/reproduce_stmn2_papa.py
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

El fetcher rechaza sobrescribir una caché existente; en ese caso se verifica el recibo y se reutiliza. No se redescarga para forzar un resultado diferente.

## Único siguiente experimento computacional

Plan nuevo y no ejecutado: research/plans/2026-11-01-stmn2-papa-tpm-reproduction.md. Usar la tabla TPM del mismo directorio, numerador idéntico, todos los grupos STMN2 en el denominador, mismas doce bibliotecas y tolerancia absoluta1e-6 frente a PPAUoriginal. Si falla, detener sin adaptar el umbral. No descargar FASTQ para sustituir una comparación aritmética pendiente ni repetir esta prueba con las mismas cuentas.

El contraste con cuentas queda cerrado como **no concordante**. El plan nuevo es una hipótesis distinta, no un rescate retrospectivo del resultado anterior. Incluso si la siguiente reproducción es correcta, será reproducción aritmética de datos publicados, sin nueva validación biológica independiente.

## Fuentes primarias

- Zenodo versión15538003:https://doi.org/10.5281/zenodo.15538003; miembro PPAU, ruta exacta y rango en retrieval.json.
- Definición de PPAU y preparación de cuentas:https://github.com/frattalab/PAPA/blob/d2ed20d217d9e3e397fa92dbcf9dc72a000f37b8/scripts/tx_to_polya_quant.R.
- Matrices y mapa previos:reports/gse296714-design-20261101, fijados en b968b7a8aa7878e41c7da297702c525d6056f260.
