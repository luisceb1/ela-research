# recount3 resuelve la medición de uniones de #37, pero este dataset no supera la cobertura

**Fecha:** 2026-11-11. **Plan prefijado:** [`research/plans/2026-11-11-recount3-unc13a-cycle.md`](../../research/plans/2026-11-11-recount3-unc13a-cycle.md), commit `27a56c9`, **anterior a cualquier consulta**.
**Etiqueta de evidencia:** auditoría de viabilidad de fuente, **ejecutada**. Rechazo documentado por cobertura. **Sin PSI, sin efectos, sin contraste inferencial.**

## Resultado en una línea

**La vía funciona y el bloqueo de medición de #37 queda resuelto como capacidad**, pero **este estudio concreto no supera el umbral de cobertura ≥20** en ninguna de las dos uniones crípticas. La causa está aislada: profundidad en el locus, no acceso ni diseño.

## Lo que se consiguió, y es nuevo para el proyecto

Las cuatro familias candidatas de #37 se rechazaron por **falta de cuentas de uniones accesibles**. recount3 las publica ya cuantificadas. Por primera vez el proyecto dispone de:

- **Cuentas de uniones exón-exón** para un experimento de depleción de TDP-43 en neuronas humanas, **sin descargar crudos ni alinear nada**.
- **24,5 MB** descargados en total, frente al presupuesto autoimpuesto de 200 MB. Coste económico: cero.
- **Condiciones declaradas por el depósito**, no inferidas.

Ruta y procedencia: el índice `https://duffel.rail.bio/recount3/human/homes_index` redirige a `recount-opendata.s3.amazonaws.com`. Fuentes disponibles en esa colección: `sra`, `gtex`, `tcga`, **`ANSWER_ALS`**, **`TARGET_ALS`**, `ega`, `LIBD`.

El host `duffel.rail.bio` estaba bloqueado por política de red (403 en CONNECT) y se permitió. `recount3.s3.amazonaws.com` respondió `NoSuchBucket`: no era una ruta real. La verificación TLS **no** se desactivó en ningún momento.

## Estudio inspeccionado

**SRP166282** = Klim et al. 2019, «ALS implicated protein TDP-43 sustains levels of STMN2 a mediator of motor neuron growth and repair». Identificado por `study_title` del propio depósito, no supuesto.

Es relevante que sea **este**: #37 rechazó a Irwin porque **reutilizaba** estos datos de Klim sin aportar cuentas de uniones enlazables. El plan prefijado contemplaba exactamente este caso — reevaluar una candidata rechazada **solo si recount3 aporta ahora esas cuentas**. Las aporta.

### Diseño reconstruido de metadatos declarados

18 muestras, RNA-seq de extremos emparejados, todas de `differentiated HUES3 into hMNs`:

| Condición | n | Tipos de siRNA | Lotes por fecha |
|---|---:|---|---|
| **TDP43 knockdown** (`genotype;;TDP43 knockdown`) | **6** | TDP43 | 2 en 2013-01-10, 4 en 2013-06-10 |
| **control** (`genotype;;control`) | **12** | scramble (6), fluorescent (3), none (3) | 4 en 2013-01-10, 8 en 2013-06-10 |

Ambos lotes contienen ambas condiciones, de modo que el lote no está completamente confundido con la condición.

**Límite de diseño que no se puede eludir:** una sola línea celular (HUES3). Las réplicas son diferenciaciones o cultivos independientes, **no donantes genéticamente independientes**. El criterio del proyecto de ≥3 unidades biológicas independientes se cumple a nivel de cultivo, pero **no** aporta independencia genética. No se promueven réplicas técnicas a unidades biológicas.

## Localización de las uniones: coincidencia exacta y control de convención superado

Objetivos: los **ya sellados** del proyecto (`research/references/unc13a_targets_sealed.json`), sin redefinir. recount3 almacena las uniones en 1-based inclusivo sobre el intrón, verificado por `length == end − start + 1`; el script **aborta** si esa identidad no se cumple, en vez de adivinar.

| Unión | Fila | Coincidencia | `annotated` | Hebra | Motivos |
|---|---:|---|---|---|---|
| canónica (exón 20–21) | 280856 | **exacta** | **1** | − | CT/AC |
| críptica izquierda | 280855 | **exacta** | **0** | − | CT/AC |
| críptica derecha | 280858 | **exacta** | **0** | − | CT/AC |

Las tres coinciden exactamente, sin desplazar ningún extremo. El patrón de anotación es el que predice la biología —canónica anotada, crípticas no— y los motivos CT/AC son GT/AG en la hebra negativa. **El control de convención de coordenadas queda superado.**

En la ventana del locus hay 5 uniones; las dos restantes (`17642506-17642844`, `17642592-17642844`) **no** se adoptan como objetivos.

## Cobertura: la puerta NO se supera

| Unión | máx. | muestras con alguna lectura | muestras ≥20 |
|---|---:|---:|---:|
| canónica (**control positivo**) | 66 | 18/18 | 10 |
| críptica izquierda | **4** | 3/18 | **0** |
| críptica derecha | **5** | 4/18 | **0** |

**El control positivo funciona** —la unión canónica se mide en las 18 muestras— de modo que el fallo no es de medición. La cobertura máxima en una unión críptica es **5 lecturas frente al mínimo prospectivo de 20**.

El veredicto se calcula **excluyendo el control positivo**, para que una canónica sana no pueda enmascarar objetivos sin cobertura: `gate_met: false`.

Mediana de la unión canónica: 25 lecturas en knockdown, 31 en control. El locus UNC13A está **poco cubierto en estas motoneuronas**, lo que es coherente con que este dataset de 2013 sea de un estudio de STMN2, no de UNC13A.

## Observación cualitativa, explícitamente por debajo del umbral

Separada del veredicto porque **no** cumple el criterio del proyecto y **no** sostiene ninguna inferencia:

| Condición | n | críptica izq. | críptica der. |
|---|---:|---|---|
| TDP43 knockdown | 6 | `[4, 4, 1, 0, 0, 0]` — 3/6 con lectura | `[5, 3, 2, 1, 0, 0]` — 4/6 con lectura |
| control | 12 | `[0 × 12]` — **0/12** | `[0 × 12]` — **0/12** |

Toda lectura críptica observada está en muestras de knockdown; ninguna en los 12 controles. La dirección coincide con la literatura publicada, en un dataset **que nunca se analizó para UNC13A**.

**Por qué esto NO es un resultado:** con un máximo de 5 lecturas, los ceros de los controles son **dato ausente a esta profundidad, no ceros biológicos**. No se calcula PSI, ni p-valor, ni efecto. No se promedia entre muestras para superar el umbral. El proyecto no relaja el mínimo de 20, y esta observación no es una excepción.

## Segundo candidato: SRP334561 (Ma 2022) — cobertura enorme, pero ensayo dirigido

Candidato **fijado antes de extraer cuentas** (addendum del plan, commit `b593cb0`), elegido por coincidencia exacta de `study_title` con el artículo de referencia del exón críptico de UNC13A, no por haber probado varios y quedarse con el que pasara.

**SRP334561** = GSE182976, «TDP-43 represses cryptic exon inclusion in FTD/ALS gene UNC13A», 12 muestras. Descarga total: **3 KB**.

### El diseño es superior al de Klim

Metadatos declarados: `treatment;;shTDP-43` frente a `treatment;;shScramble`, en **tres líneas de donante distintas** (`cell line;;NDS00262-NINDS`, `NDS00209-NINDS`, …), 2 réplicas por condición y línea. Eso aporta la **independencia genética** que a SRP166282 le faltaba (línea única HUES3): 3 unidades genéticamente independientes por condición.

### Las cuentas superan el umbral con enorme margen

| Unión | máx. | muestras ≥20 |
|---|---:|---:|
| canónica (control positivo) | 93.815 | 12/12 |
| críptica izquierda | **57.709** | **12/12** |
| críptica derecha | **49.314** | 11/12 |

Fracción críptica `(izq+der)/(izq+der+canónica)` por condición:

| Condición | n | Fracción críptica |
|---|---:|---|
| shScramble (control) | 6 | **0,000 – 0,002** |
| shTDP-43 (knockdown) | 6 | **0,390 – 0,690** |

Separación completa, consistente en las tres líneas de donante.

### Y sin embargo la puerta de #37 NO queda superada

El plan fijaba de antemano que superar el umbral en un ensayo dirigido **no acredita** la detectabilidad que el umbral pretendía garantizar, y exigía verificar la naturaleza del ensayo contra el artículo antes de declarar nada. Verificado:

> «The **amplicon sequencing** data has been deposited in the Gene Expression Omnibus (GEO) at GSE182976.» (Ma 2022, Data availability)

> «**Amplicon sequencing of the splice variants.** Splice variants in iPSC-MNs were established by **PCR amplification from UNC13A exon 19 to exon 21** … Resulting products were purified … and submitted for NGS (**Amplicon EZ**, Genewiz).» (Métodos)

**Es secuenciación de amplicón por RT-PCR de un solo locus, etiquetada como `library_strategy: RNA-Seq` en los metadatos de SRA.** Las 50.000–90.000 lecturas sobre tres uniones son profundidad de amplicón, no cobertura transcriptómica.

Por tanto: **cobertura obtenida en un ensayo de naturaleza dirigida, no comparable con el piloto cerrado ni con SRP166282**, y **no habilita el contraste inferencial de #37**. El denominador de la fracción críptica es específico del amplicón, está sujeto a sesgo de PCR y no equivale a PSI calculado sobre uniones de transcriptoma completo.

Lo que sí queda establecido: los datos depositados **reproducen de forma independiente el hallazgo cualitativo publicado** —la pérdida de TDP-43 induce inclusión del exón críptico de UNC13A— con separación limpia entre condiciones en tres líneas de donante.

### Detector añadido a la sonda

La trampa es reutilizable, así que la sonda ahora la detecta sola:

| Proyecto | Uniones totales | En chr19 | Cromosomas | ¿Parece dirigido? |
|---|---:|---:|---:|---|
| SRP166282 (RNA-seq real) | 599.768 | 34.031 (5,7 %) | 77 | **No** |
| SRP334561 (amplicón) | 43 | 33 (**76,7 %**) | 6 | **Sí** |

`assay_shape()` marca `looks_targeted_not_transcriptome_wide` y el veredicto queda `gate_qualified_by_assay_shape: true`. Es una heurística, no una prueba: obliga a verificar contra el artículo, no sustituye esa verificación.

## Tercer candidato: Brown 2022 — ninguno de sus depósitos es elegible

Decidido **desde la propia declaración de datos del artículo**, antes de tocar ningún dato. Brown 2022 enumera lo que depositó y lo que reutilizó:

| Accesión | Qué es | Elegible para #37 |
|---|---|---|
| E-MTAB-10235 | Riboseq | **No**: no es RNA-seq de uniones |
| E-MTAB-10237 | RNA-seq **dirigido** | **No**: dirigido |
| E-MTAB-10297 | iCLIP de minigén | **No**: otro ensayo |
| E-MTAB-11243 | iCLIP de TDP-43 en SH-SY5Y | **No**: otro ensayo |
| E-MTAB-11244 | nanopore **dirigido** a UNC13A | **No**: dirigido |
| GSE121569 (reutilizado) | «iPS cell MNs» | **= SRP166282**, ya probado y rechazado por cobertura |
| GSE126543 (reutilizado) | núcleos neuronales de córtex frontal por FACS | **Sin registros SRA** (`count=0`): no está en recount3 |
| GSE97262 (reutilizado) | SK-N-BE(2)b | Sin accesión SRA enlazada; línea de neuroblastoma, no neuronas corticales |

**Brown 2022 no puede probar la hipótesis cortical.** Su única fuente de transcriptoma completo reutilizada es el dataset de Klim que ya rechazamos, y su candidato cortical (GSE126543) no tiene depósito en SRA alcanzable por esta vía.

Dato relevante de paso: los dos artículos que **establecieron** el exón críptico de UNC13A depositaron **ensayos dirigidos** —amplicón, RNA-seq dirigido, nanopore dirigido—. Eso es coherente con que la unión críptica sea difícil de detectar en RNA-seq de transcriptoma completo a profundidad habitual.

## Discrepancia entre fuentes que NO se resuelve aquí

Las dos fuentes miden la misma cosa en condiciones de knockdown y **no concuerdan**:

| Fuente | Ensayo | Fracción críptica en knockdown |
|---|---|---|
| SRP166282 (Klim) | RNA-seq de transcriptoma completo | **0,000 – 0,145** |
| SRP334561 (Ma) | amplicón dirigido | **0,390 – 0,690** |

Una diferencia de **4 a 5 veces**. La fracción es independiente de la profundidad, de modo que **la discrepancia no se explica por cobertura**. Explicaciones alternativas posibles, ninguna comprobada aquí: eficacia distinta del knockdown (siRNA frente a shRNA), sesgo de amplificación del ensayo de amplicón, diferencias de línea o tipo celular, filtros de uniones de recount3 sobre el RNA-seq, o longitud de lectura y mapeabilidad de la unión críptica en los datos de 2013.

**No se resuelve y no se promedia.** Se registra como inconsistencia abierta entre fuentes, y refuerza la advertencia de no tratar la fracción del amplicón como PSI no sesgado.

### Por qué esta discrepancia decide el futuro de la puerta de #37

Con la fracción que muestra Klim (≈0,10) y su cobertura canónica (≈60 lecturas), alcanzar 20 lecturas crípticas exigiría unas **200 lecturas en la unión canónica**. Con la fracción de Ma (≈0,5) bastarían unas **40**.

Es decir: **si el umbral de 20 es alcanzable en RNA-seq público depende de cuál de las dos fracciones es la real**, y eso es precisamente lo que no sabemos. La pregunta previa a seguir buscando datasets ya no es «¿hay uno más profundo?» sino «¿cuál es el nivel real de inclusión críptica?».

**Esto es una decisión de alcance para Luis, no del agente:** reorientar #37 hacia resolver esa discrepancia, o seguir buscando datasets de transcriptoma completo más profundos. El agente **no** cambia el umbral de 20 ni la pregunta de #37 por su cuenta.

## Limitaciones

- **SRP166282: rechazo por cobertura**, igual que el piloto cerrado. La causa está aislada: profundidad en el locus, no acceso. **Una sola línea celular**, sin independencia genética.
- **SRP334561: no elegible** para la puerta de #37 por ser ensayo de amplicón dirigido, pese a tener el mejor diseño (3 líneas de donante) y cobertura altísima. Su fracción críptica no es PSI de transcriptoma completo.
- **La hipótesis cortical sigue SIN PROBAR**, y Brown 2022 no puede probarla: sus depósitos son dirigidos o de otro ensayo, y su candidato cortical no tiene SRA. Los tres candidatos examinados son de motoneuronas o inelegibles.
- **No se ha hecho una búsqueda exhaustiva de recount3.** Se comprobaron accesiones concretas derivadas de los dos artículos de referencia. **No se afirma que no exista** un dataset adecuado; se afirma que los de estos artículos no sirven.
- **Discrepancia abierta de 4–5× en la fracción críptica** entre las dos fuentes, sin resolver. Mientras siga abierta, no se puede saber si el umbral de 20 es alcanzable en RNA-seq público.
- **Los metadatos de SRA pueden mentir sobre la estrategia de librería.** Aquí un amplicón figura como `RNA-Seq`. No fiarse del campo sin comprobar la forma de la cuantificación y el artículo.
- Depleción por siRNA, no degradación controlada; el grado de knockdown por muestra **no** se ha verificado en estos datos.
- Las cuantificaciones de recount3 usan su propia tubería y filtros de uniones. Otra herramienta contaría distinto y habría que justificar la equivalencia.
- No se ha comprobado STMN2 en este ciclo; el plan fijaba UNC13A.
- Observación de splicing ≠ rescate molecular ≠ función neuronal ≠ beneficio clínico. **Nada aquí respalda ninguna indicación clínica.**

## Siguiente prueba discriminante, concreta

La hipótesis que explica el fallo es **de profundidad y de tipo neuronal**, y es comprobable:

1. Ikegami 2026 y el panel GTEx de Mallika 2026 coinciden en que **UNC13A se expresa menos en médula espinal que en córtex**. Estas son motoneuronas espinales. Un dataset de depleción de TDP-43 en **neuronas corticales o i3Neurons**, donde UNC13A está más expresado y la secuenciación suele ser más profunda, es el candidato natural para superar la cobertura ≥20.
2. La sonda ya está construida y probada: aplicar la misma ruta a otro proyecto cuesta **minutos y unos megabytes**, no un presupuesto. Eso es el activo real de este ciclo.
3. `ANSWER_ALS` y `TARGET_ALS` están en recount3. **Son cohortes de pacientes, no experimentos de depleción de TDP-43**, de modo que usarlas respondería una **pregunta distinta** (ALS frente a control) y exigiría un plan nuevo. No se cambia de endpoint para esquivar este rechazo.

**Criterio de parada:** si dos o tres datasets de depleción de TDP-43 con buena profundidad cortical tampoco alcanzan cobertura ≥20 en las uniones crípticas, la vía recount3 se cierra para esta pregunta y se registra que la detección exige datos dirigidos, no reanálisis de depósitos públicos.

Sin contactos, gastos, datos personales, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
