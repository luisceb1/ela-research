# Curación de la matriz: verificación de citas y re-derivación de criterios

**Fecha:** 2026-11-10 (segunda pasada, mismo día). **Ejecutada por:** el mismo agente que hizo la primera pasada.

## Qué es y qué no es esta curación

Luis indicó que la labor técnica me corresponde. Esta pasada hace dos cosas **verificables**:

1. **Comprobación mecánica de transcripción.** `scripts/verify_matrix_quotes.py` comprueba que cada fragmento entre comillas de la columna `locator` existe literalmente en el texto fuente, tras normalizar espacios, comillas tipográficas, guiones y μ→u. **Resultado: 14/14 filas PASS, 0 fragmentos ausentes.**
2. **Re-derivación de cada clasificación** contra las reglas del plan prefijado, releyendo el texto primario en vez de mis propias notas.

**Lo que esta pasada NO es:** una revisión independiente. La hice yo, el mismo lector que cometió los errores de la primera pasada. Caza fallos de transcripción y de aplicación de reglas —y cazó cuatro—, pero no puede caer en la cuenta de un sesgo sistemático mío ni de un criterio mal concebido desde el principio. La necesidad de revisión externa sigue abierta, y el informe propone vías sin coste.

## Fallos encontrados y corregidos

| # | Fallo | Naturaleza | Corrección |
|---|---|---|---|
| 1 | El verificador no veía ninguna cita (`NO_QUOTES` en 9 filas) | **Bug mío**: el módulo `csv` trata `"` como delimitador de campo y borraba las comillas | `quoting=csv.QUOTE_NONE` |
| 2 | Tres citas (K-c, M-b, H-a) no existían literalmente | **Error mío de transcripción**: uní con `...` fragmentos no contiguos, creando frases que ningún autor escribió | Divididas en fragmentos literales separados; las tres verifican ahora |
| 3 | Dos citas de Cao no coincidían | **Artefacto de extracción**, no error de transcripción: los números de línea y el aviso de copyright del preprint cortan las frases | Limpieza documentada de esa plantilla en el verificador |
| 4 | Recuento «9 específicas de UNC13A / 5 multidiana» | **Error mío de recuento a mano**, sin respaldo por fila | Columna `target_scope` por fila: **6** `unc13a_only`, 2 `mixed`, 5 `multi_target`, 1 `stmn2_focused` |

## Corrección de fondo: mi afirmación de «predicción refutada» era demasiado fuerte

En mi mensaje anterior declaré la predicción refutada por el brazo CTR de Mallika (M-a). Al re-derivarlo contra la **letra** de mi criterio prefijado, esa afirmación no se sostiene sin matiz.

Mi regla de *post-deficit recovery* dice: «el déficit del mismo endpoint se mide en el mismo sistema/cohorte **antes** de la primera dosis… Un control no tratado en paralelo que muestre déficit al final **no basta**.»

En M-a:
- Lo documentado en el momento de dosificar son **temblores finos** («when fine tremors are already apparent»): observación **cualitativa**, y **no es el endpoint medido** (fuerza de agarre, supervivencia).
- El déficit de fuerza de agarre «as early as 6 weeks» se evidencia en el **brazo GFP paralelo** — exactamente la situación que mi regla excluye de forma explícita.

Por tanto la matriz registra ahora **dos lecturas**, en columnas separadas y contables por máquina:

| Lectura | Definición | Posdéficit |
|---|---|---:|
| `strict_rule_verdict` | La letra del criterio prefijado | **0 de 14** |
| `classification` | Lectura sustantiva: los animales tenían síntomas documentados al dosificar y los autores lo enmarcan como «after onset of symptoms» | **1 de 14** (M-a) |

**Bajo la lectura estricta, la predicción NO queda refutada.** Bajo la sustantiva, sí, por un único experimento multidiana. Doy las dos en lugar de elegir una en silencio, porque la diferencia es un juicio sobre qué cuenta como déficit basal, no un dato.

**En ambas lecturas, el resultado central no cambia:** de las **6** intervenciones `unc13a_only`, en **0** consta que la dosis siguiera a un déficit medido. **Corrección del 11/11/2026:** eso acredita ausencia de documentación, no que todas sean «preventivas por construcción»; esto último solo se sostiene para las deleciones germinales. Ver la corrección en el informe.

## Reclasificación de K-c

De `indeterminate` a `prevention`. Motivo: el plan reserva *indeterminate* para «cronología o medición basal **no recuperable** del texto accesible». En K-c la cronología **sí** es recuperable —doxiciclina 5 días, después transfección del ASO— y la medición basal no es irrecuperable, simplemente **no se hizo**. La cláusula prefijada de *prevention* («…o antes de que el déficit del endpoint se haya medido») cubre ese caso. Es aplicación de la regla, no cambio de regla.

**Observación que merece destacarse:** K-c es la única fila `unc13a_only` donde la dosis llega con el knockdown de TDP-43 **ya establecido** (5 días de doxiciclina). No acredita rescate posdéficit —nadie midió el defecto en esos pozos antes de dosificar— pero es **el molde experimental más cercano** a un diseño posdéficit que existe hoy para UNC13A. Es el punto de partida natural para el protocolo #18.

## Veredicto fila por fila

Las 14 filas tienen sus citas verificadas literalmente. `strict` = letra del criterio; `subst` = lectura sustantiva.

| Fila | Alcance | strict | subst | Verdicto de curación |
|---|---|---|---|---|
| K-a | unc13a_only | prevention | prevention | Confirmada. Dosis concurrente con el PROTAC, cita inequívoca |
| K-b | unc13a_only | prevention | prevention | Confirmada. Deleción genómica, preventiva por construcción |
| K-c | unc13a_only | prevention | prevention | **Reclasificada** desde *indeterminate*; ver arriba. Molde más cercano a posdéficit |
| G-a | mixed | prevention | prevention | Confirmada. ASO día 3, shRNA día 5 |
| G-b | mixed | prevention | prevention | Confirmada. ASO día 20, shRNA día 21 |
| M-a | multi_target | prevention | **post-deficit** | **Discrepante entre lecturas.** La fila que más necesita revisión externa |
| M-b | unc13a_only | prevention | prevention | Confirmada. Germinal. Resultado negativo: insuficiente para enfermedad de motoneurona |
| C-a | unc13a_only | prevention | prevention | Confirmada. Germinal. Preserva memoria |
| C-b | multi_target | prevention | prevention | Confirmada. AAV 2 semanas tras tamoxifeno, sin medición conductual previa |
| H-a | unc13a_only | prevention | prevention | Confirmada. Línea estable anterior a la doxiciclina |
| H-b | multi_target | prevention | prevention | Confirmada. Inyección neonatal |
| B-a | multi_target | prevention | prevention | Confirmada. Lentivirus día 32, axotomía día 42 |
| B-b | multi_target | prevention | prevention | Confirmada. Doxiciclina concurrente con la transducción |
| B-c | stmn2_focused | prevention | prevention | Confirmada. Inyección en las primeras 24 h de vida |

## Lo que sigue necesitando ojos ajenos

1. **M-a**: si los temblores finos documentados al dosificar cuentan como déficit basal. Es un juicio de criterio, no de dato.
2. **Mi definición de «déficit basal»**: exigir el mismo endpoint en los mismos animales es estricto; puede ser demasiado estricto para modelos murinos bien caracterizados, donde la progresión por edad está establecida. No puedo evaluar con independencia una regla que escribí yo.
3. **El alcance de `target_scope` en G-a/G-b**: etiquetadas `mixed` porque las filas agregan varios ASO. Separarlas por diana exigiría releer los paneles por figura.

## Reproducir esta verificación

```
python -I scripts/verify_matrix_quotes.py \
  reports/unc13a-intervention-timing-20261110/matrix.tsv \
  --sources <mapa>.json --base <directorio de fuentes>
```

El mapa asocia `source_id` a su texto fuente. Los originales (XML de Europe PMC, y los dos PDF aportados por Luis) **no** se versionan: sus SHA256 están en `sources.json`. Salida distinta de 0 si falta algún fragmento, de modo que puede usarse como control en CI.
