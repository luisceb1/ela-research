# Los datos depositados de Ikegami/Koike 2026 reproducen sus estadísticos publicados

**Fecha:** 2026-11-10. **Plan prefijado:** [`research/plans/2026-11-10-ikegami-source-data-replay.md`](../../research/plans/2026-11-10-ikegami-source-data-replay.md), commit `2dd8ba9`, **anterior a abrir el archivo**.
**Etiqueta de evidencia:** reproducción descriptiva interna. **No** es replicación independiente —son los mismos sujetos y las mismas medidas— **ni** validación biológica. **No aporta cuentas de uniones y no avanza #37.**

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

Esto reproduce exactamente la afirmación publicada: el Tipo 2b es significativamente más alto que los Tipos 1 y 2a en **ambas** medidas, mientras que Tipo 1 y 2a no se distinguen entre sí.

### R4 — Concordancia ddPCR ↔ qRT-PCR: cuantificada

El artículo afirma «strong correlations» sin dar coeficiente. Los datos depositados lo permiten calcular:

| Medida | n | Spearman ρ | p |
|---|---:|---|---|
| UNC13A críptico (Fig. S5e) | 26 | **0,859** | 1,9 × 10⁻⁸ |
| STMN2 truncado (Fig. S5f) | 26 | **0,870** | 7,7 × 10⁻⁹ |

El subconjunto con ddPCR es de 26 casos, no 35.

### Controles

- **Control negativo por permutación** (2.000 iteraciones, semilla 20261110): al barajar las etiquetas de subtipo, la diferencia se destruye. p de permutación 1,5 × 10⁻³ (UNC13A) y 5,0 × 10⁻⁴ (STMN2), concordantes con los p asintóticos. El resultado depende de las etiquetas reales, no de la estructura del reparto.
- **Explicación alternativa comprobada:** correlación con la duración de enfermedad **no significativa** en ninguna medida: ρ = −0,237 (p = 0,17) para UNC13A críptico y ρ = −0,258 (p = 0,13) para STMN2 truncado, n=35. Confirma de forma independiente la afirmación del artículo de que las diferencias por subtipo no se explican por la duración.

## Interpretación

Los datos fuente depositados **sostienen los estadísticos publicados**: tamaños de grupo exactos, ρ dentro de tolerancia, diferencias por subtipo idénticas en dirección y significación, y la explicación alternativa por duración descartada con los mismos datos. Es un ejercicio de reproducibilidad superado, y vale la pena decirlo: en este proyecto varios depósitos previos **no** reprodujeron sin fricción.

Qué añade a nuestra línea científica: la correlación ρ ≈ 0,57–0,58 entre el RNA críptico de UNC13A y el STMN2 truncado en **35 casos humanos revisados por pares** es el respaldo observacional más sólido que tenemos para la hipótesis **H2** de desregulación coordinada entre dianas de TDP-43. Coincide en dirección con el hallazgo experimental de Mallika: corregir una sola diana fue insuficiente para la enfermedad de motoneurona, mientras la restauración multidiana sí rescató fenotipos.

Qué **no** añade: correlación entre dos marcadores en el mismo tejido no demuestra mecanismo compartido, causalidad ni que corregir ambas dianas beneficie a un paciente. Una correlación de 0,57 deja más de dos tercios de la varianza sin explicar.

## Limitaciones

- **Reproducibilidad interna, no replicación.** Mismos sujetos, mismas medidas, mismo laboratorio. Que los números cuadren no los hace correctos: un error de medida o de asignación de subtipo se reproduciría igual de bien.
- **Sin cuentas de uniones.** qRT-PCR y ddPCR cuantifican abundancia de transcrito críptico, no PSI de uniones. **#37 sigue bloqueada** y esta fuente continúa **rechazada** para esa puerta.
- **Tejido post mortem heterogéneo**, no cultivo i3N. No se equipara ni se compara directamente con los modelos celulares de la matriz de cronología.
- **n=11 en el Tipo 2b**, el grupo que porta el efecto. Pequeño para estimaciones estables, aunque el leave-one-out sobre R1 no mostró dominancia de un caso.
- **El ajuste de multiplicidad puede diferir del de los autores:** usé Holm; Prism aplica su propia corrección y el artículo no nombra el método de familia. Las conclusiones de significación coinciden de todos modos.
- **Sin asignación caso→muestra entre hojas.** Las hojas comparten orden aparente dentro de cada subtipo, pero **no he enlazado un caso concreto entre paneles por posición de fila**, conforme al plan. Por eso R1 se calculó solo donde el propio archivo deposita los pares (Fig. 2c), no cruzando hojas.
- No se descargó el Additional file 2 (DOCX, 3,7 MB) ni se extrajo número alguno de imágenes.
- Correlación de marcadores ≠ mecanismo ≠ función ≠ beneficio clínico. **Nada aquí respalda ninguna indicación clínica.**

## Siguiente prueba discriminante

1. La pregunta que estos datos **no** pueden responder es si la coordinación UNC13A–STMN2 refleja una dependencia mecanística común o solo la intensidad de la pérdida nuclear de TDP-43. Discriminaría una fuente con **pérdida de TDP-43 cuantificada por caso** junto a ambos marcadores: si la correlación entre marcadores se anula al condicionar en la carga de TDP-43, es un efecto de dosis compartida; si persiste, apunta a algo más. El Additional file 1 (Table S1, 46×15) contiene metadatos por caso aún no inspeccionados y podría incluir esa variable.
2. No se amplía a otros artículos del grupo, no se contacta a los autores y no se abre un ciclo nuevo sin decisión de alcance.

**Criterio de abandono de H2:** si una fuente con medida directa de uniones y unidades biológicas independientes no reproduce la asociación entre dianas, H2 deja de sostenerse como hipótesis de trabajo.

Sin contactos, gastos, datos personales, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
