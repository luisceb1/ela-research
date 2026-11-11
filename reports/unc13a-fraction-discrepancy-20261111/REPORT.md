# La discrepancia de fracción críptica NO se resuelve, pero queda acotada: las dos cifras no son comparables

**Fecha:** 2026-11-11. **Plan prefijado:** [`research/plans/2026-11-11-unc13a-fraction-discrepancy.md`](../../research/plans/2026-11-11-unc13a-fraction-discrepancy.md), commit `7bb94bf`, **anterior a descargar o calcular nada**.
**Etiqueta de evidencia:** arbitraje **parcial** de una inconsistencia entre fuentes. **No se declara una fracción verdadera.** Sin PSI propio, sin efectos, sin p-valores.

Reorientación de #37 autorizada por Luis el 11/11/2026. El umbral de 20 **no se modifica**; se suspende su aplicación como criterio de aceptación de fuentes hasta que la discrepancia se arbitre.

## La discrepancia que se investiga

| Fuente | Ensayo | Fracción críptica en depleción |
|---|---|---|
| SRP166282 (Klim 2019) | RNA-seq de transcriptoma completo | 0,000 – 0,145 |
| SRP334561 (Ma 2022) | amplicón dirigido | 0,390 – 0,690 |

Una fracción es independiente de la profundidad, así que la cobertura **no** puede explicar 4–5× de diferencia.

## Resultado principal: las dos mediciones no son comparables como estimaciones de PSI

### La naturaleza de amplicón queda confirmada por segunda vía, independiente

El ciclo anterior la detectó por la distribución de uniones (43 uniones, 77 % en chr19). Ahora, a nivel de gen y de fragmento:

| Proyecto | Genes detectados | Mayor gen como fracción del total | Longitud modal de fragmento |
|---|---|---|---|
| SRP166282 (RNA-seq) | **29.646 – 36.965** | 1,6 % | 126 – 147 pb |
| SRP334561 (amplicón) | **8 – 17** | **100,0 %** | **1.508 pb** |

En las 12 muestras de Ma, **un solo gen concentra el 100 % de las cuentas** y el fragmento modal mide 1.508 pb, el tamaño del producto de PCR de exón 19 a 21. Una librería así no estima expresión ni PSI de transcriptoma: cuantifica la proporción de productos **dentro de su propio amplicón**.

**Conclusión:** las dos cifras miden cosas distintas. La de Klim es una fracción de uniones sobre transcriptoma completo; la de Ma es una proporción de productos de amplificación de un locus. Compararlas directamente **no es válido**, y por tanto la «discrepancia» no es necesariamente un conflicto empírico: es en buena parte un artefacto de comparar dos ensayos no equivalentes.

### Eficacia del knockdown: medida en uno, no declarada en el otro

Lo que sí se puede medir, sobre las cuentas génicas de Klim (18/18 muestras de transcriptoma completo):

| Gen | CPM mediana control | CPM mediana depleción | Reducción |
|---|---:|---:|---:|
| **TARDBP** | 132,0 | 54,4 | **58,8 %** |
| STMN2 | 2.145,6 | 1.033,9 | 51,8 % |
| UNC13A | 178,5 | 169,3 | 5,1 % |

**El knockdown de Klim es parcial: queda ≈41 % de TARDBP.** Eso es compatible con una inclusión críptica baja, porque la represión del exón críptico por TDP-43 es dependiente de dosis — pero compatible no es demostrado.

Para Ma **no se puede medir**: el script **se niega** a leer un nivel de knockdown de una librería de amplicón, como fijaba el plan, porque el número no mediría expresión. Y la eficacia **no aparece declarada** en el texto accesible del artículo; el plan obligaba a registrarla como no disponible y **no estimarla**.

**Por tanto la comparación que habría arbitrado E1 está bloqueada por falta de información, no resuelta.** La predicción prefijada —que el knockdown de Klim sería sustancialmente menor que el de Ma— **no es comprobable** con lo accesible. No se confirma ni se refuta.

### Verificación de propina

La reducción de STMN2 del 51,8 % en las cuentas depositadas **reproduce de forma independiente el hallazgo central de Klim 2019** («TDP-43 sustains levels of STMN2»), que no era el objetivo de este ciclo.

## Estado de las explicaciones candidatas

| # | Explicación | Estado tras este ciclo |
|---|---|---|
| E1 | Eficacia del knockdown | **Viva, no cuantificable**. Klim: 58,8 %. Ma: no declarada |
| E2 | Sesgo de detección por longitud de lectura y anclaje | **Viva, no comprobable**. Klim usa lecturas cortas estándar; el exón críptico mide 128/178 pb, de modo que un anclaje corto penalizaría las uniones crípticas. Mecanismo plausible, sin prueba con estos archivos |
| E3 | Filtros de uniones o multimapeo de recount3 | **No comprobable**: SRP166282 no tiene archivos `UNIQUE` |
| E4 | Sesgo del ensayo de amplicón | **Reforzada**: una librería donde un gen es el 100 % de la señal no da un PSI comparable |
| E5 | Línea o tipo celular | Documentada, no cuantificada. Ambos son motoneuronas derivadas de células madre |

**Ninguna queda descartada y ninguna queda demostrada.** Lo que sí queda establecido es que E4 hace la comparación inválida de partida.

## Interpretación

La pregunta «¿cuál es la fracción críptica real de UNC13A?» **sigue sin respuesta**, y este ciclo explica por qué: una de las dos mediciones disponibles proviene de un ensayo que no puede dar esa cifra, y la otra se tomó bajo un knockdown parcial del 58,8 %.

Para #37 la consecuencia es concreta y más útil que «buscar un dataset más profundo». La entrada que haría falta ya no es solo cobertura, sino:

1. **RNA-seq de transcriptoma completo** (no amplicón, no dirigido, no nanopore dirigido),
2. con **eficacia de depleción de TDP-43 documentada** y preferiblemente alta,
3. con **profundidad suficiente en el locus UNC13A**, que con una fracción de 0,10 implicaría del orden de 200 lecturas en la unión canónica,
4. y con mapa condición→unidad biológica independiente, ≥3 por condición.

El criterio 2 es nuevo y nace de este ciclo: sin él, una fracción baja no se puede distinguir de un knockdown débil.

## Limitaciones

- **La discrepancia no está resuelta.** Este informe acota explicaciones; no elige una fracción verdadera ni promedia las dos.
- **La predicción prefijada no es comprobable** por falta de la eficacia declarada de Ma. Se registra como tal, sin sustituirla por otra predicción a posteriori.
- E2 y E3 quedan sin comprobar por limitaciones de los archivos, no por haberse descartado.
- Las cuentas génicas de recount3 usan su propia tubería (anotación G026). Otra tubería daría cifras distintas y habría que justificar la equivalencia.
- La reducción del 58,8 % es a nivel de **ARN**; la pérdida de proteína TDP-43 puede diferir y no se mide aquí.
- Comparar proyectos distintos no es un contraste: cohortes, ensayos y épocas son diferentes. **No se calcula ningún efecto entre proyectos.**
- Observación de splicing ≠ rescate molecular ≠ función neuronal ≠ beneficio clínico. **Nada aquí respalda ninguna indicación clínica.**

## Siguiente prueba discriminante

Un **único** dataset que cumpla los cuatro criterios de arriba zanjaría a la vez la fracción y la viabilidad del umbral. Mientras no aparezca:

- **No** se acepta ninguna fuente por cobertura sola.
- **No** se usa la fracción del amplicón como PSI de referencia.
- **No** se reabren las candidatas ya rechazadas.

**Criterio de abandono:** si tres datasets que cumplan los criterios 1, 2 y 4 muestran fracciones mutuamente consistentes pero por debajo de la cobertura necesaria, se concluirá que la medición de las uniones crípticas de UNC13A exige datos dirigidos, y #37 se cerrará como no alcanzable con depósitos públicos de transcriptoma completo.

Sin contactos, gastos, datos personales, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
