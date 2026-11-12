# Los datos depositados de Ikegami/Koike 2026 reproducen sus estadísticos publicados

**Corrección de integración del 11/11:** se conservan los estadísticos reproducidos, pero p>0,05 no establece equivalencia ni descarta confusión. La prueba de correlación de covariables prefijada no se ejecutó tal como se escribió. El cribado entre subtipos no la sustituye inferencialmente; duración, edad y otras covariables siguen sin quedar excluidas. Ver [revisión](../integration-20261111/REVIEW.md).

**Fecha:** 2026-11-10. **Plan prefijado:** [`research/plans/2026-11-10-ikegami-source-data-replay.md`](../../research/plans/2026-11-10-ikegami-source-data-replay.md), commit `2dd8ba9`, **anterior a abrir el archivo**.
**Etiqueta de evidencia:** reproducción descriptiva interna. **No** es replicación independiente —son los mismos sujetos y las mismas medidas— **ni** validación biológica. **No aporta cuentas de uniones y no avanza #37.**

## Corrección interpretativa — 10/11/2026

Se corrigen inferencias excesivas sobre confusión, independencia y varianza, conservando todos los estadísticos originales. El análisis condicionado por subtipo se documenta por separado en [el nuevo informe](../ikegami-subtype-conditioning-20261110/REPORT.md).

## Fuente

Ikegami I, Hongo S, Koyama A, Hayakawa-Yano Y, Yano M, Sugai A, Ishihara T, Tada M, Kakita A, Onodera O, Koike YM. *Acta Neuropathologica Communications* 14:229 (2026-08-08). DOI 10.1186/s40478-026-02400-0. PMID 42983891, PMC13737708. **Revisado por pares**, acceso abierto CC-BY-NC-ND 4.0.

Additional file 3 (Source Data), `40478_2026_2400_MOESM3_ESM.xlsx`, 29.237 bytes, SHA256 `d72b8ebc18c1b71be8bc4c26ffde1edd6f5da65541a7711c686073f4a36ad385`. 16 hojas, una por panel. Obtenido de `static-content.springer.com` tras fallar el endpoint `supplementaryFiles` de Europe PMC (cinco intentos: ZIP truncado a 2,8 MB o HTML) y la ruta `/bin/` de PMC (interstitial, no el archivo). **El libro no se versiona**; solo su hash y los estadísticos derivados.

Entorno fijado: **numpy 2.3.4, scipy 1.17.0, openpyxl 3.1.5** ([`research/requirements-ikegami-replay.txt`](../../research/requirements-ikegami-replay.txt), referenciado desde el manifiesto de CI). Los resultados se obtuvieron primero con numpy 2.5.3 / scipy 1.18.1 y se **reejecutaron bajo el stack fijado**: salida **byte a byte idéntica** salvo el campo de versiones. Se fijó 1.17.0 porque scipy 1.18.x y numpy 2.5.x exigen Python ≥3.12 y romperían el trabajo de Python 3.11 de la matriz de CI.

Resultados completos y legibles por máquina: [`results.json`](results.json). Script: [`scripts/replay_ikegami_source_data.py`](../../scripts/replay_ikegami_source_data.py), con 6 pruebas en `tests/test_replay_ikegami.py` que **se ejecutan en CI sin omisiones**.

## Evidencia

### R3 — Tamaños de grupo: coincidencia exacta

Tipo 1 **n=12**, Tipo 2a **n=12**, Tipo 2b **n=11**, total **35**, idéntico en ambas medidas y a lo publicado.

### R1 — Correlación UNC13A críptico ↔ STMN2 truncado: reproducida

| Cantidad | Valor |
|---|---|
| Pares (por caso, Fig. 2c) | **35** |
| Spearman ρ reproducido | **0,5737** |
| ρ publicado | 0,58 |
| Δ | **−0,0063** |
| p | 3,1 × 10⁻⁴ |
| Leave-one-out (rango de ρ) | 0,535 – 0,653 |

Dentro de la tolerancia prefijada (|Δ| ≤ 0,01), luego **la predicción se cumple**. Discrepancia menor digna de registro: 0,5737 redondea a **0,57**, no a 0,58. La diferencia es compatible con el tratamiento de empates de GraphPad Prism o con una convención de redondeo distinta, y **no** se ha ajustado el método para cuadrar. El leave-one-out muestra que ningún caso aislado domina el resultado.

### R2 — Diferencias por subtipo: reproducidas en dirección y significación

Kruskal–Wallis y Dunn (ajuste de Holm; Prism aplica su propia corrección de familia, que el artículo no nombra, así que lo comparable son z y la dirección).

**UNC13A críptico** — H = 12,99, p = 1,5 × 10⁻³. Medianas: Tipo 1 8,04 × 10⁻⁴, Tipo 2a 3,84 × 10⁻⁴, **Tipo 2b 2,98 × 10⁻³**.

| Comparación | z | p sin ajustar | p Holm |
|---|---|---|---|
| Tipo 1 vs 2a | +1,06 | 0,291 | 0,291 (ns) |
| Tipo 1 vs **2b** | −2,49 | 0,0128 | **0,0255** |
| Tipo 2a vs **2b** | −3,52 | 4,3 × 10⁻⁴ | **0,0013** |

**STMN2 truncado** — H = 16,30, p = 2,9 × 10⁻⁴. Medianas: Tipo 1 1,55 × 10⁻³, Tipo 2a 2,65 × 10⁻³, **Tipo 2b 2,49 × 10⁻²**.

| Comparación | z | p sin ajustar | p Holm |
|---|---|---|---|
| Tipo 1 vs 2a | −0,42 | 0,676 | 0,676 (ns) |
| Tipo 1 vs **2b** | −3,71 | 2,1 × 10⁻⁴ | **6,3 × 10⁻⁴** |
| Tipo 2a vs **2b** | −3,30 | 9,7 × 10⁻⁴ | **0,0019** |

Esto reproduce exactamente la afirmación publicada: el Tipo 2b es significativamente más alto que los Tipos 1 y 2a en **ambas** medidas, mientras que para Tipo 1 frente a 2a no se detectó una diferencia significativa; no es una prueba de equivalencia.

### R4 — Concordancia ddPCR ↔ qRT-PCR: cuantificada

El artículo afirma «strong correlations» sin dar coeficiente. Los datos depositados lo permiten calcular:

| Medida | n | Spearman ρ | p |
|---|---:|---|---|
| UNC13A críptico (Fig. S5e) | 26 | **0,859** | 1,9 × 10⁻⁸ |
| STMN2 truncado (Fig. S5f) | 26 | **0,870** | 7,7 × 10⁻⁹ |

El subconjunto con ddPCR es de 26 casos, no 35.

### Controles

- **Control negativo por permutación** (2.000 iteraciones, semilla 20261110): al barajar las etiquetas de subtipo, la diferencia se destruye. p de permutación 1,5 × 10⁻³ (UNC13A) y 5,0 × 10⁻⁴ (STMN2), concordantes con los p asintóticos. El resultado depende de las etiquetas reales, no de la estructura del reparto.
- **Explicación alternativa comprobada:** correlación con la duración de enfermedad **no significativa** en ninguna medida: ρ = −0,237 (p = 0,17) para UNC13A críptico y ρ = −0,258 (p = 0,13) para STMN2 truncado, n=35. Reproduce la ausencia de significación en esos mismos datos; no descarta un papel de la duración y no constituye validación independiente.

## Segundo ciclo: cribado de confusores con Table S1/S2

Addendum del plan, fijado **antes** de calcular (commit `9dce800`). Script: [`scripts/check_ikegami_covariates.py`](../../scripts/check_ikegami_covariates.py), 6 pruebas en `tests/test_ikegami_covariates.py`. Datos: Additional file 1, `40478_2026_2400_MOESM1_ESM.xlsx`, 17.845 bytes, SHA256 `aeacd9fdf134a8e0dbf02bf574e32338f22f38d55c542b8c4a4bf17424e7e1c9`. Resultados: [`covariates.json`](covariates.json).

### La prueba discriminante que quería hacer NO es ejecutable

El depósito **no contiene carga de pTDP-43 cuantificada por caso**, solo el subtipo categórico. Por tanto no puede comprobarse si la correlación UNC13A–STMN2 se anula al condicionar en la carga de TDP-43. Se registra como laguna; no se sustituye por un proxy.

### Enlace por caso: rechazado por mi propia regla

Las hojas de figura no llevan identificador de caso. La duración de enfermedad **sí** aparece en Table S1 (por caso) y en `Fig. S3a/b` (emparejada con la medida), y sus vectores coinciden posición por posición en los 35 casos. Pero mi regla prefijada exigía que la clave fuese **única dentro de cada subtipo**, y no lo es: Tipo 2a repite 18, 20 y 26 meses; Tipo 2b repite 10 y 12. Solo el Tipo 1 (n=12) tiene clave única.

Así que **no** calculo correlaciones por caso entre covariables y medidas. La coincidencia posicional es un dato de procedencia, no una licencia para enlazar por orden de fila, que el plan prohíbe. Se informa sin usarse para inferencia.

### Lo que sí se puede comprobar sin enlace

Se comprobó si se detectaban diferencias entre subtipos, sin estimar la relación individual con los marcadores. No detectar una diferencia no prueba igualdad ni excluye confusión. Kruskal–Wallis sobre los 35 casos, con corrección de Holm sobre las **seis** covariables cribadas:

| Covariable | H | p sin corregir | p Holm | Veredicto |
|---|---|---|---|---|
| **Duración de enfermedad (meses)** | 15,39 | 4,5 × 10⁻⁴ | **0,0027** | **Difiere** |
| Edad de inicio (años) | 6,25 | 0,0439 | 0,220 | solo nominal |
| Edad a la muerte (años) | 5,26 | 0,0720 | 0,288 | ns |
| Intervalo post mortem (horas) | 4,29 | 0,117 | 0,351 | ns |
| Pérdida neuronal (semicuantitativa) | 3,83 | 0,148 | 0,351 | ns |
| **RIN (calidad de RNA)** | 1,37 | 0,504 | 0,504 | ns |

No se detectaron diferencias significativas de RIN, pérdida neuronal semicuantitativa o PMI entre subtipos bajo este análisis. **No se demuestra equivalencia ni quedan descartadas como explicaciones del patrón.** Es reproducción interna, no confirmación independiente.

**Un matiz importante sobre la duración.** La duración **sí** difiere fuertemente entre subtipos, y en la dirección esperada: Tipo 1 mediana 32 meses, Tipo 2a 19, **Tipo 2b 11**. Es decir, el subtipo con más RNA críptico es el de curso más corto. El artículo afirma que las diferencias «no se explican fácilmente» por la duración, y su apoyo es la correlación no significativa entre duración y medidas, que reproduje en el primer ciclo (ρ = −0,24 y −0,26, ns). Las dos cosas son compatibles: la duración acompaña al subtipo y la correlación con el marcador no alcanzó significación; eso no demuestra ausencia de predicción o confusión. Conviene ser exacto sobre la fuerza de esa conclusión: con n=35 y ρ ≈ −0,25, la potencia para detectar un efecto moderado de la duración es limitada, de modo que esto es **ausencia de evidencia más que evidencia de ausencia**.

**Una discrepancia menor con el texto.** El artículo dice: «cases were selected to achieve comparable age distributions across ALS pathological subtypes». En los datos depositados, la **edad de inicio** difiere nominalmente (p = 0,044; medianas 64,5 / 67,5 / **74,0**) y la edad a la muerte muestra una diferencia nominal entre Tipo 1 y Tipo 2b (p = 0,034 por pares). Ninguna sobrevive a la corrección de Holm sobre las seis covariables, así que **la afirmación de comparabilidad no queda contradicha a nivel corregido**. Lo registro porque la dirección es consistente —los casos Tipo 2b son unos 10 años mayores al inicio— y porque la edad no figura entre los confusores que el resumen declara haber comprobado.

## Interpretación

Los datos fuente depositados **sostienen los estadísticos publicados**: tamaños de grupo exactos, ρ dentro de tolerancia, diferencias por subtipo idénticas en dirección y significación, sin poder descartar la explicación alternativa por duración con estos mismos datos. Es un ejercicio de reproducibilidad superado, y vale la pena decirlo: en este proyecto varios depósitos previos **no** reprodujeron sin fricción.

Update — 12 November 2026: the pooled association is internal observational evidence. The subsequently completed [subtype-conditioned cycle](../ikegami-subtype-conditioning-20261110/REPORT.md) gives adjusted rank rho 0.31669 and p=0.07825; its fixed prediction is not met. The association does not establish coordinated mechanism or benefit of multi-target correction, and is not independent validation of Mallika.

Qué **no** añade: correlación entre dos marcadores en el mismo tejido no demuestra mecanismo compartido, causalidad ni que corregir ambas dianas beneficie a un paciente. El coeficiente de Spearman describe asociación entre rangos; su cuadrado no cuantifica directamente la fracción de varianza biológica explicada.

## Limitaciones

- **Reproducibilidad interna, no replicación.** Mismos sujetos, mismas medidas, mismo laboratorio. Que los números cuadren no los hace correctos: un error de medida o de asignación de subtipo se reproduciría igual de bien.
- **Sin cuentas de uniones.** qRT-PCR y ddPCR cuantifican abundancia de transcrito críptico, no PSI de uniones. **#37 sigue bloqueada** y esta fuente continúa **rechazada** para esa puerta.
- **Tejido post mortem heterogéneo**, no cultivo i3N. No se equipara ni se compara directamente con los modelos celulares de la matriz de cronología.
- **n=11 en el Tipo 2b**, el grupo que porta el efecto. Pequeño para estimaciones estables, aunque el leave-one-out sobre R1 no mostró dominancia de un caso.
- **El ajuste de multiplicidad puede diferir del de los autores:** usé Holm; Prism aplica su propia corrección y el artículo no nombra el método de familia. Las conclusiones de significación coinciden de todos modos.
- **Sin asignación caso→muestra entre hojas.** Las hojas comparten orden aparente dentro de cada subtipo, pero **no he enlazado un caso concreto entre paneles por posición de fila**, conforme al plan. Por eso R1 se calculó solo donde el propio archivo deposita los pares (Fig. 2c), no cruzando hojas.
- No se descargó el Additional file 2 (DOCX, 3,7 MB) ni se extrajo número alguno de imágenes.
- **Sin carga de TDP-43 por caso**, luego la prueba discriminante central de H2 queda fuera del alcance de esta fuente.
- **Covariables no enlazables por caso** a las medidas: la duración no es clave única en Tipos 2a y 2b. El cribado de confusores es por tanto **entre subtipos**, que no permite descartar confusión ni cuantificar su efecto sobre el marcador.
- Las seis covariables se cribaron a la vez y se corrigieron por Holm. La duración sobrevive; la edad de inicio no. No se declara diferencia a partir de un p nominal aislado.
- Correlación de marcadores ≠ mecanismo ≠ función ≠ beneficio clínico. **Nada aquí respalda ninguna indicación clínica.**

## Siguiente prueba discriminante

1. La pregunta que estos datos **no** pueden responder sigue siendo si la coordinación UNC13A–STMN2 refleja una dependencia mecanística común o solo la intensidad de la pérdida nuclear de TDP-43. El segundo ciclo confirmó que **este depósito no la puede responder**: no hay carga de pTDP-43 cuantificada por caso. Haría falta una fuente con esa medida junto a ambos marcadores. La atenuación o persistencia tras ajustar por una medida de patología sería informativa, pero no identificaría por sí sola un mecanismo: persistirían error de medida y confusores no observados. La carga de agregados pTDP-43 no es intercambiable con pérdida de función nuclear de TDP-43.
2. Un confusor que esta fuente **sí** deja planteado: el Tipo 2b combina más RNA críptico, curso más corto y mayor edad de inicio. Separar «intensidad de patología» de «velocidad de progresión» exigiría una cohorte con esos ejes desacoplados. No lo tenemos.
3. No se amplía a otros artículos del grupo, no se contacta a los autores, no se abre el Additional file 2 y no se inicia un ciclo nuevo sin decisión de alcance.

**Criterio para revisar H2:** una fuente independiente y adecuadamente informativa que no reproduzca la asociación debilitaría la hipótesis. Un resultado no significativo por sí solo no la refuta: deben examinarse efecto, incertidumbre, cobertura y diseño.

Sin contactos, gastos, datos personales, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
