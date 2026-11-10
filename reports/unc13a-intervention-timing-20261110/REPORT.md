# Cronología de intervenciones UNC13A: predicción refutada por un experimento multidiana; la laguna específica de UNC13A persiste

**Fecha:** 2026-11-10. **Base:** main `3916b77ec0546e9d327e6d54e4dacd90d1a51ce4`, plan prefijado en `research/plans/2026-11-10-unc13a-intervention-timing-matrix.md` (commit `626c259`, **anterior** a la recuperación de los textos).
**Etiqueta de evidencia:** auditoría documental exploratoria de un solo lector. **Requiere segunda revisión humana** antes de considerarse curada. No es un experimento propio ni una estimación de efecto.

Autorización: Luis confirmó el 10/11/2026 que **no** ha llegado el archivo K26 y que AD Workbench **no** ha concedido acceso, e indicó continuar con el resto. #37 y #44 siguen bloqueadas e intactas. Luis aportó después los PDF de Mallika y Cao, que completaron la matriz a 6/6 fuentes.

## Pregunta y predicción prefijadas

¿Algún experimento primario accesible que corrija o impida el exón críptico de UNC13A/Unc13a bajo pérdida de TDP-43 inicia la intervención **después** de documentar, en el mismo sistema y endpoint, un déficit funcional basal?

Predicción prefijada: ninguno lo cumple para un endpoint funcional. Se refutaría con un solo experimento que lo cumpliese con localizador textual verificable.

## Resultado: la predicción queda REFUTADA

**14 experimentos sobre 6 fuentes: 1 *post-deficit recovery*, 12 *prevention*, 1 *indeterminate*.**

El experimento que la refuta es **Mallika M-a**: AAV-PHP.eB-CTR administrado por vena caudal **a las 6 semanas de edad, «when fine tremors are already apparent»**, en ratones ChAT-Cre;Tardbp^f/f^. Los autores lo describen explícitamente como tratamiento «at a symptomatic stage» y «after onset of symptoms». El rescate funcional es grande: fuerza de agarre mantenida, peso normal, y supervivencia de ~47 semanas (brazo GFP) a **≥110 semanas** sin parálisis, con n=20 por grupo.

Registro la refutación en los términos del plan, sin reescribir el criterio después de ver el resultado.

**Pero la laguna que motivaba la pregunta no desaparece, se vuelve más precisa.** CTR es un *Chimeric TDP-43 splicing Repressor* (dominio de reconocimiento de ARN de TDP-43 fusionado a RAVER1): restaura la represión de splicing de **muchas** dianas, **no es una intervención específica de UNC13A**. Separando por especificidad:

| Tipo de intervención | Experimentos | Posdéficit |
|---|---:|---:|
| **Específica de UNC13A** (deleción germinal del CE, ASO anti-CE, tU7 anti-CE) | 9 | **0** |
| **Multidiana** (CTR, ASO combinados, snRNA dual) | 5 | 1 |

**Para intervenciones específicas de UNC13A, la predicción se sostiene: ninguna de las 9 actúa después de un déficit medido.** Todas son preventivas por construcción —deleción germinal del exón críptico, o dosis que preceden o coinciden con la pérdida de TDP-43.

Matriz completa y citable: [`matrix.tsv`](matrix.tsv), 14 filas con cita literal y sección de origen. Procedencia, versiones, bytes y SHA256: [`sources.json`](sources.json).

## Evidencia por fuente

| Fuente | Acceso | Experimentos | Clasificación |
|---|---|---:|---|
| S1 Keuss 2024 | texto completo | 3 | 2 prevention, 1 indeterminate |
| S2 Guo 2025 | texto completo | 2 | 2 prevention |
| S3 Mallika 2026 | **PDF aportado por Luis** | 2 | **1 post-deficit (CTR, multidiana)**, 1 prevention (Unc13a-específica) |
| S4 Cao 2026 | **PDF aportado por Luis** | 2 | 2 prevention |
| S5 Mehta 2025 | texto completo | 2 | 2 prevention |
| S6 Gomberg 2025 | texto completo | 3 | 3 prevention |

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

1. **La corrección aislada de UNC13A nunca se ha probado después de un déficit medido.** Las 9 intervenciones específicas accesibles son preventivas. Lo que la literatura sostiene es que *impedir* el exón críptico preserva función si se actúa antes o a la vez que la pérdida de TDP-43; no que *corregirlo* recupere función ya perdida, que es el escenario del paciente diagnosticado.

2. **La restauración multidiana posdéficit sí rescata función en un modelo murino.** Mallika lo demuestra con un efecto grande sobre supervivencia. Esto no es un dato contra la hipótesis UNC13A: es la prueba de que la ventana posdéficit **no es intrínsecamente intratable** en este modelo, lo que hace la pregunta específica de UNC13A más pertinente, no menos.

3. **UNC13A sola divide resultados por endpoint, no por calidad del estudio.** Preventiva, falla para enfermedad de motoneurona (Mallika) y preserva memoria (Cao). Coherente con la hipótesis H1 de dependencia del tipo neuronal, y con el dato observacional de Ikegami (abajo) de desregulación coordinada entre dianas. No es una contradicción: son endpoints y poblaciones distintos.

Esto refuerza el criterio ya aplicado a #44, donde la intervención seleccionada también es concurrente con la depleción de TDP-43.

## Limitaciones

- **Un solo lector automatizado.** Las 14 clasificaciones necesitan segunda curación humana. El script `scripts/extract_intervention_timing.py` solo **localiza** frases; no clasifica.
- **La clasificación posdéficit de M-a cumple el criterio solo en parte.** Mi regla prefijada exige el déficit *del mismo endpoint* medido *en los mismos animales* antes de la dosis. Lo documentado antes de dosificar son **temblores finos** (cualitativo); el déficit de fuerza de agarre se evidencia en el brazo GFP **paralelo**, no pre-dosis en los mismos animales. Lo clasifico como posdéficit porque los autores documentan síntomas presentes en el momento de dosificar y lo enmarcan así, pero la base basal es más débil de lo que pedía mi criterio. Esta es la fila que más necesita tu revisión.
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

1. **Segunda curación humana** de las 14 filas de `matrix.tsv`, empezando por M-a (base basal cualitativa) y K-c (la única *indeterminate*).
2. La laguna documentada, ahora precisa, es: **ninguna corrección específica de UNC13A probada después de un déficit funcional medido**, mientras la restauración multidiana posdéficit sí rescata función en ratón. Eso justifica documentalmente el protocolo #18 en su forma específica, y **no** autoriza ningún ensayo: seguiría exigiendo déficit medido antes de la primera dosis, unidades independientes verificables y autorización concreta.
3. Antes de cualquier diseño, comprobar si la versión revisada por pares de Mallika o Cao modifica cronologías o n.

**Criterio de abandono:** si la curación humana identifica una intervención *específica de UNC13A* posdéficit ya publicada, esta laguna se cierra y #18 pierde su justificación en la forma aquí descrita.

Sin contactos, gastos, datos personales, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
