# Cronología de intervenciones sobre UNC13A: ninguna acreditada como rescate posdéficit

**Fecha:** 2026-11-10. **Base:** main `3916b77ec0546e9d327e6d54e4dacd90d1a51ce4`, plan prefijado en `research/plans/2026-11-10-unc13a-intervention-timing-matrix.md` (commit `626c259`, **anterior** a la recuperación de los textos).
**Etiqueta de evidencia:** auditoría documental exploratoria de un solo lector. **Requiere segunda revisión humana** antes de considerarse curada. No es un experimento propio ni una estimación de efecto.

Autorización: Luis confirmó el 10/11/2026 que **no** ha llegado el archivo K26 y que AD Workbench **no** ha concedido acceso, e indicó continuar con el resto. #37 y #44 siguen bloqueadas e intactas.

## Pregunta y predicción prefijadas

¿Algún experimento primario accesible que corrija o impida el exón críptico de UNC13A/Unc13a bajo pérdida de TDP-43 inicia la intervención **después** de documentar, en el mismo sistema y endpoint, un déficit funcional basal?

Predicción prefijada: ninguno lo cumple para un endpoint funcional. Se refutaría con un solo experimento que lo cumpliese con localizador textual verificable.

## Evidencia

Matriz completa y citable: [`matrix.tsv`](matrix.tsv) — 12 experimentos extraídos de 6 fuentes, 14 campos, cada fila con cita literal y sección de origen. Procedencia, versiones, bytes y SHA256: [`sources.json`](sources.json).

**Resultado: 12 experimentos; 0 clasificados como *post-deficit recovery*; 10 *prevention*; 2 *indeterminate*. La predicción no queda refutada.**

| Fuente | Acceso | Experimentos | Clasificación |
|---|---|---:|---|
| S1 Keuss 2024 (PMC11230273) | texto completo | 3 | 2 prevention, 1 indeterminate |
| S2 Guo 2025 (PMC12424808) | texto completo | 2 | 2 prevention |
| S3 Mallika 2026 (PMC13596259) | **solo abstract** (registro restringido en PMC) | 1 | 1 indeterminate |
| S4 Cao 2026 (sin PMCID) | **solo abstract** | 1 | 1 prevention |
| S5 Mehta 2025 (PMC12697360) | texto completo | 2 | 2 prevention |
| S6 Gomberg 2025 (PMC12822690) | texto completo | 3 | 3 prevention |

Hallazgos de cronología que fijan la clasificación, con cita literal:

- **Keuss, brazo ASO:** «ASO treatments were started **at the same time as** PROTAC treatment and were included in each media change for two weeks until cells were harvested.» La dosis es concurrente con el inicio de la degradación de TDP-43. El brazo de deleción genómica del exón críptico es constitutivo, luego preventivo por construcción.
- **Guo:** la primera dosis **precede** a la pérdida de TDP-43 en los dos diseños: ASO días 3 y 10 con shRNA el día 5, y ASO días 20 y 27 con shRNA el día **21**. Esto confirma y precisa lo que el informe de la PR #51 anotaba solo para el primer diseño. Los propios autores sitúan su medida funcional «prior to any cell loss».
- **Mehta:** el tU7 anti-UNC13A se expresa desde líneas estables seleccionadas **antes** de inducir el knockdown con doxiciclina; el rescate de frecuencia de mEPSC se mide en células que nunca estuvieron sin la intervención.
- **Gomberg:** ASO anti-TDP-43 el día 30, lentivirus SURF el día **32**, axotomía el día **42**. La intervención precede al reto funcional; no hay medida de regeneración basal antes del día 32. Además, el endpoint funcional (regeneración axonal) se atribuye a **STMN2**, no a UNC13A.
- **Cao:** clasificado *prevention* desde el abstract por ser ablación genética constitutiva; el propio título dice «**Prevention** of Unc13a cryptic splicing is sufficient to preserve memory».

## Interpretación

La bibliografía accesible sostiene que impedir el exón críptico de UNC13A preserva función cuando se actúa **antes o a la vez** que la pérdida de TDP-43. **No** sostiene todavía que corregir UNC13A recupere función ya perdida, que es el escenario relevante para un paciente diagnosticado. Esto no es un defecto de los estudios: ninguno declara probar un rescate posdéficit. Es una laguna de diseño en el conjunto del campo, y es exactamente la laguna que el protocolo diferido #18 («UNC13A posdéficit v0.4») apunta en el BACKLOG.

Un hallazgo negativo con valor operativo: refuerza el criterio ya aplicado a #44, donde la intervención ASO seleccionada también es concurrente con la depleción de TDP-43 y por tanto no acredita recuperación posterior a un déficit previo.

## Limitaciones

- **Un solo lector automatizado.** Las 12 clasificaciones necesitan segunda curación humana. El script `scripts/extract_intervention_timing.py` solo **localiza** frases; no clasifica.
- **2 de 6 fuentes sin métodos accesibles.** Mallika y Cao quedan sin cronología verificable; Mallika es precisamente el estudio que reporta que impedir solo Unc13a **no** mitigó la enfermedad motora. Con 4/6 textos completos, la matriz queda **en el mínimo** prefijado: es utilizable, no concluyente.
- **Las 6 fuentes son preprints**, sujetos a revisión y corrección. La versión Nature 2026 de Keuss **no** fue inspeccionada; la cronología citada se atribuye solo al preprint de 2024.
- Ausencia de un diseño en los textos accesibles **no** demuestra que no exista en datos no publicados, en versiones posteriores o en material suplementario no descargado.
- No se cuantificó ningún efecto, no se ejecutó ningún modelo y no se compararon magnitudes entre sistemas. Modelos murinos y cultivos humanos no se equiparan; el exón críptico de *Unc13a* de ratón no es homólogo posicional del humano (intrón 1 frente a intrón 20), según lo ya registrado.
- Corrección de splicing ≠ rescate molecular ≠ función neuronal ≠ beneficio clínico. Nada aquí respalda ninguna indicación clínica.

## Comprobación colateral de la puerta de fuentes (#37)

Se evaluó **PMID 42983891** (Ikegami/Koike 2026, *Acta Neuropathologica Communications* 14:229, revisado por pares, acceso abierto), detectado por el vigilante automático el 09/11, como posible fuente nueva para #37.

**Decisión: RECHAZADA como fuente técnica para #37.** Motivos verificados en el texto completo (SHA256 en `sources.json` C1):

1. **No hay cuentas de uniones.** La cuantificación es qRT-PCR y ddPCR, no RNA-seq. Búsquedas en el texto completo: `RNA-seq` 0 apariciones, `sequencing` 0, `GEO` 0, `BAM` 0, `FASTQ` 0. No existe matriz de uniones ni alineamiento que someter al criterio de cobertura ≥20.
2. **Disponibilidad de datos insuficiente para nuestro contraste:** «The datasets generated and/or analyzed during the current study are available from the corresponding author on reasonable request.» Los datos fuente numéricos están en el Additional file 3 (XLSX, 29 KB), no descargado en este ciclo.
3. **Tejido post mortem, no cultivo.** Corteza motora de ALS esporádica (Tipo 1 n=12, Tipo 2a n=12, Tipo 2b n=11). Por `AGENTS.md` y el estado vigente, no sustituye el contraste en cultivo i3N ni se equipara a él.

Valor retenido como **contexto**, no como fuente aceptada: reporta que el subtipo patológico 2b muestra niveles significativamente más altos de RNA críptico de UNC13A y de STMN2 truncado, y una correlación positiva entre ambos (Spearman ρ = 0.58). Es evidencia observacional de desregulación coordinada entre dianas, coherente con la hipótesis H2 del informe de la PR #51, y no un rescate ni una causalidad.

#37 sigue bloqueada por su única entrada: un manifiesto concreto Seddighi–AD Workbench. Esta revisión **no** abre un cuarto candidato ni reactiva búsquedas.

## Siguiente experimento discriminante

1. **Segunda curación humana** de las 12 filas de `matrix.tsv`, con atención a las 2 *indeterminate*.
2. Resolver el acceso a los métodos de Mallika y Cao por vía pública (bioRxiv directo), ya que son las dos fuentes que más pesan para la hipótesis de dependencia del tipo neuronal. No está hecho: requiere permitir `biorxiv.org` en la red de la sesión.
3. Solo entonces, y solo si la segunda curación confirma 0 experimentos posdéficit, el protocolo #18 queda justificado documentalmente como laguna real. Eso **no** autoriza ningún ensayo: seguiría requiriendo datos con déficit funcional medido antes de la primera dosis y autorización específica.

**Criterio de abandono:** si la curación humana identifica un experimento posdéficit ya publicado, esta laguna se cierra y #18 pierde su justificación en la forma aquí descrita.

Sin contactos, gastos, datos personales, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
