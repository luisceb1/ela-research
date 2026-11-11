# Cronología de intervenciones UNC13A: la laguna específica persiste bajo las dos lecturas del criterio

[English](REPORT.en.md)


**Fecha:** 2026-11-10. **Base:** main `3916b77ec0546e9d327e6d54e4dacd90d1a51ce4`, plan prefijado en `research/plans/2026-11-10-unc13a-intervention-timing-matrix.md` (commit `626c259`, **anterior** a la recuperación de los textos).
**Etiqueta de evidencia:** auditoría documental exploratoria. Primera pasada y curación ejecutadas **por el mismo agente**; no hay revisión independiente. Ver [CURATION](CURATION.md).

Autorización: Luis confirmó el 10/11/2026 que **no** ha llegado el archivo K26 y que AD Workbench **no** ha concedido acceso, e indicó continuar con el resto. #37 y #44 siguen bloqueadas e intactas. Luis aportó después los PDF de Mallika y Cao, que completaron la matriz a 6/6 fuentes.

## Pregunta y predicción prefijadas

¿Algún experimento primario accesible que corrija o impida el exón críptico de UNC13A/Unc13a bajo pérdida de TDP-43 inicia la intervención **después** de documentar, en el mismo sistema y endpoint, un déficit funcional basal?

Predicción prefijada: ninguno lo cumple para un endpoint funcional.

## Resultado

**14 experimentos sobre 6 fuentes.** Todas las citas verificadas literalmente contra el texto primario: 14/14 PASS con `scripts/verify_matrix_quotes.py`.

La suerte de la predicción depende de un juicio de criterio, así que la matriz registra **dos lecturas** en columnas separadas y contables:

| Lectura | Definición | Posdéficit | Predicción |
|---|---|---:|---|
| `strict_rule_verdict` | La letra del criterio prefijado, que **excluye** el brazo paralelo como prueba basal | **0 de 14** | **no refutada** |
| `classification` | Lectura sustantiva: síntomas documentados al dosificar, enmarcado por los autores como «after onset of symptoms» | **1 de 14** | refutada |

El único experimento en discrepancia es **Mallika M-a**: AAV-PHP.eB-CTR a las 6 semanas, «when fine tremors are already apparent», con rescate grande de fuerza de agarre y supervivencia de ~47 a **≥110 semanas** (n=20 por grupo). Bajo mi criterio estricto no basta, porque lo documentado antes de dosificar son temblores (cualitativo, y no es el endpoint medido) y el déficit de agarre se evidencia en el **brazo GFP paralelo**. Doy las dos lecturas en lugar de elegir una en silencio.

**El resultado central no depende de esa elección.** Por alcance de diana, verificado fila por fila:

| Alcance | Experimentos | Posdéficit (estricto) | Posdéficit (sustantivo) |
|---|---:|---:|---:|
| **`unc13a_only`** | **6** | **0** | **0** |
| `mixed` (ASO single/combinados) | 2 | 0 | 0 |
| `multi_target` | 5 | 0 | 1 |
| `stmn2_focused` | 1 | 0 | 0 |

**En ninguna de las 6 intervenciones específicas de UNC13A pudo establecerse que la dosis siguiera a un déficit funcional documentado, en ninguna de las dos lecturas.**

> **Corrección del 11/11/2026.** La versión original añadía «todas son preventivas por construcción». **Eso no se sigue.** Para las deleciones germinales del exón críptico sí: el diseño lo garantiza. Para el resto, y señaladamente para **K-c** (Keuss, SH-SY5Y), donde el knockdown llevaba **5 días** establecido al dosificar, **no**: que no se midiera un déficit previo no demuestra que no lo hubiera. Lo que la matriz acredita es la **ausencia de documentación**, no la ausencia de déficit. Invertir lo uno en lo otro es convertir ausencia de evidencia en evidencia de ausencia.

Matriz completa: [`matrix.tsv`](matrix.tsv), 14 filas, 16 campos. Procedencia y SHA256: [`sources.json`](sources.json). Fallos encontrados y corregidos en la curación: [`CURATION.md`](CURATION.md).

## Evidencia por fuente

| Fuente | Acceso | Experimentos | Lectura estricta / sustantiva |
|---|---|---:|---|
| S1 Keuss 2024 | texto completo (Europe PMC) | 3 | 3 prevention / igual |
| S2 Guo 2025 | texto completo (Europe PMC) | 2 | 2 prevention / igual |
| S3 Mallika 2026 | **PDF aportado por Luis** | 2 | 2 prevention / **1 post-deficit (M-a, multidiana)** + 1 prevention |
| S4 Cao 2026 | **PDF aportado por Luis** | 2 | 2 prevention / igual |
| S5 Mehta 2025 | texto completo (Europe PMC) | 2 | 2 prevention / igual |
| S6 Gomberg 2025 | texto completo (Europe PMC) | 3 | 3 prevention / igual |

Cronologías que fijan la clasificación, con cita literal:

- **Keuss, brazo ASO:** «ASO treatments were started **at the same time as** PROTAC treatment». Concurrente con la degradación de TDP-43.
- **Guo:** la primera dosis **precede** al knockdown en ambos diseños — ASO días 3 y 10 con shRNA el día 5, y ASO días 20 y 27 con shRNA el día **21**. Los autores sitúan su medida «prior to any cell loss».
- **Mehta:** tU7 expresado desde líneas estables seleccionadas antes de inducir doxiciclina.
- **Gomberg:** ASO anti-TDP-43 día 30, lentivirus día 32, axotomía día **42**; la intervención precede al reto funcional, y su endpoint funcional se atribuye a STMN2.
- **Mallika, brazo Unc13a-específico:** deleción germinal de ~44 pb del CE cruzada al modelo cKO. Resultado: «could not maintain the normal grip strength and body weight … **indistinguishable** from those observed in ChAT-Cre;Tardbpf/f mice», y la conclusión de los autores: «**preventing cryptic splicing of Unc13a is insufficient to attenuate motor neuron disease**».
- **Cao, brazo Unc13a-específico:** deleción germinal, tamoxifeno a los 2 meses; preserva reconocimiento de objeto novedoso. Título: «**Prevention** of Unc13a cryptic splicing is sufficient to preserve memory».
- **Cao, brazo CTR:** «Tamoxifen was administered at 5 months of age to deplete TDP-43, followed by ICV injection of AAV-PHP.eB-CTR … **2 weeks later**». No se reporta medición conductual previa a la dosis, luego no acredita posdéficit.

## Interpretación

Tres lecturas, en orden de solidez:

1. **La corrección aislada de UNC13A nunca se ha probado después de un déficit medido.** En las **6** intervenciones `unc13a_only` accesibles no consta que la dosis siguiera a un déficit documentado, en ninguna de las dos lecturas; **preventivas por construcción lo son solo las deleciones germinales** (ver corrección arriba). Lo que la literatura sostiene es que *impedir* el exón críptico preserva función si se actúa antes o a la vez que la pérdida de TDP-43; no que *corregirlo* recupere función ya perdida, que es el escenario del paciente diagnosticado. El molde más cercano que existe es **K-c** (Keuss, SH-SY5Y): dosis con el knockdown ya establecido tras 5 días de doxiciclina, aunque sin medición del defecto previa a la dosis.

2. **La restauración multidiana posdéficit rescata función en un modelo murino, bajo la lectura sustantiva.** Mallika M-a muestra un efecto grande sobre supervivencia. No es un dato contra la hipótesis UNC13A: sugiere que la ventana posdéficit **no es intrínsecamente intratable** en este modelo, lo que hace la pregunta específica de UNC13A más pertinente, no menos. Bajo la lectura estricta, ni siquiera eso queda acreditado, porque la prueba basal procede del brazo paralelo.

3. **UNC13A sola divide resultados por endpoint, no por calidad del estudio.** Preventiva, falla para enfermedad de motoneurona (Mallika) y preserva memoria (Cao). Coherente con la hipótesis H1 de dependencia del tipo neuronal, y con el dato observacional de Ikegami (abajo) de desregulación coordinada entre dianas. No es una contradicción: son endpoints y poblaciones distintos.

Esto refuerza el criterio ya aplicado a #44, donde la intervención seleccionada también es concurrente con la depleción de TDP-43.

## Limitaciones

- **Un solo lector, sin revisión independiente.** La primera pasada y la curación las hizo el mismo agente. La curación caza fallos de transcripción y de aplicación de reglas —cazó cuatro, incluido un bug del propio verificador y tres citas mías mal unidas con elipsis— pero **no puede detectar un sesgo sistemático mío ni un criterio mal concebido**. Ver [CURATION](CURATION.md). El script `extract_intervention_timing.py` solo localiza frases; `verify_matrix_quotes.py` solo comprueba transcripción. Ninguno clasifica.
- **M-a es la fila en discrepancia y la que más necesita ojos ajenos.** Mi criterio exige el déficit *del mismo endpoint* medido *en los mismos animales* antes de la dosis, y excluye explícitamente el brazo paralelo. En M-a lo documentado antes de dosificar son **temblores finos** (cualitativo, y no es el endpoint medido) y el déficit de agarre viene del brazo GFP. Si ese criterio es demasiado estricto para un modelo murino con progresión por edad bien caracterizada es un juicio que **no puedo evaluar con independencia, porque la regla la escribí yo**.
- **Recuento corregido durante la curación:** mi cifra inicial de «9 específicas / 5 multidiana» era un recuento a mano sin respaldo. El reparto verificado por fila es 6 `unc13a_only`, 2 `mixed`, 5 `multi_target`, 1 `stmn2_focused`.
- **S3 y S4 no son independientes entre sí:** mismo autor corresponsal (Philip C. Wong, Johns Hopkins) y **6 autores compartidos** entre los 10 de S3 y los 18 de S4. Pueden compartir animales, construcciones y cohortes. No se cuentan como réplicas independientes.
- **Las 6 fuentes son preprints**, sujetos a revisión y corrección. La versión Nature 2026 de Keuss **no** fue inspeccionada; su cronología se atribuye solo al preprint de 2024.
- **Extrapolación murina:** el exón críptico de *Unc13a* de ratón está en el **intrón 1**, mientras el humano está en el **intrón 20** (confirmado en la discusión de Mallika). Las dos intervenciones no se equiparan mecánicamente. El AAV-PHP.eB cruza la barrera hematoencefálica de ratón; no acredita aplicabilidad humana.
- El efecto de CTR **no permite adjudicar mejora a cada diana por separado**: no hay control factorial.
- No se cuantificó ningún efecto propio, no se ejecutó ningún modelo y no se compararon magnitudes entre sistemas. Corrección de splicing ≠ rescate molecular ≠ función neuronal ≠ beneficio clínico. Nada aquí respalda ninguna indicación clínica.
- Licencia de S4: «All rights reserved. No reuse allowed without permission». Solo se versionan hashes y citas cortas con fin de auditoría; no se redistribuye el PDF.

## Comprobación colateral de la puerta de fuentes (#37)

Se evaluó **PMID 42983891** (Ikegami/Koike 2026, *Acta Neuropathologica Communications* 14:229, revisado por pares, acceso abierto) como posible fuente nueva para #37.

**Decisión: RECHAZADA como fuente técnica para #37.** Motivos verificados en el texto completo (SHA256 en `sources.json` C1):

1. **No hay cuentas de uniones.** La cuantificación es qRT-PCR y ddPCR, no RNA-seq. En el texto completo: `RNA-seq` 0 apariciones, `sequencing` 0, `GEO` 0, `BAM` 0, `FASTQ` 0. No hay matriz de uniones ni alineamiento que someter al criterio de cobertura ≥20.
2. **Disponibilidad insuficiente:** «available from the corresponding author on reasonable request». Datos fuente en Additional file 3 (XLSX, 29 KB), no descargado.
3. **Tejido post mortem, no cultivo.** Corteza motora de ALS esporádica (Tipo 1 n=12, Tipo 2a n=12, Tipo 2b n=11). No sustituye el contraste en cultivo i3N ni se equipara a él.

Valor retenido como **contexto**: el subtipo 2b muestra niveles significativamente más altos de RNA críptico de UNC13A y de STMN2 truncado, con correlación positiva entre ambos (Spearman ρ = 0.58). Desregulación coordinada observacional, no rescate ni causalidad.

#37 sigue bloqueada por su única entrada: un manifiesto concreto Seddighi–AD Workbench. Esta revisión **no** abre un cuarto candidato.

## Siguiente experimento discriminante

1. La laguna documentada, ahora precisa, es: **ninguna corrección específica de UNC13A probada después de un déficit funcional medido** (0 de 6, en las dos lecturas). Eso justifica documentalmente el protocolo #18 en su forma específica, y **no** autoriza ningún ensayo: seguiría exigiendo déficit medido antes de la primera dosis, unidades independientes verificables y autorización concreta.
2. Antes de cualquier diseño, comprobar si la versión revisada por pares de Mallika o Cao modifica cronologías o tamaños de grupo.

### Revisión independiente: vías sin coste

La curación la he hecho yo, así que la independencia sigue pendiente. Rutas gratuitas, en orden de esfuerzo para Luis:

- **Esperar la versión revisada por pares.** Keuss ya tiene aceptación en Nature; Mallika y Cao están en revisión. Los revisores harán gratis, y con más autoridad, el juicio sobre la cronología de M-a. Coste: cero; plazo: meses.
- **Comentario público en bioRxiv.** Cualquiera puede comentar un preprint sin coste ni registro de pago. Una pregunta concreta y cortés sobre si hubo medida basal de fuerza de agarre antes de la inyección a las 6 semanas la resolvería. **Requiere tu autorización expresa**, porque `AGENTS.md` prohíbe comunicaciones externas sin ella, y la firmarías tú, no yo.
- **Comunidades de investigación en ELA.** Foros y listas académicas abiertas donde una pregunta metodológica suele recibir respuesta experta sin coste. Mismo requisito de autorización.
- **Servicios de revisión estadística/metodológica de pago.** Existen, pero no los recomiendo aquí: el juicio pendiente es de criterio de diseño, no de estadística, y los revisores de pares lo resolverán gratis. Si en algún momento consideras esta vía, te daría precios antes de cualquier gasto.

**Criterio de abandono:** si una revisión externa identifica una intervención *específica de UNC13A* posdéficit ya publicada, esta laguna se cierra y #18 pierde su justificación en la forma aquí descrita.

Sin contactos, gastos, datos personales, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
