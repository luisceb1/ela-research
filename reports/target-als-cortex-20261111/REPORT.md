# Corteza motora de 149 pacientes: separación cualitativa limpia, pero el umbral de 20 es inalcanzable por dilución

**Fecha:** 2026-11-11. **Plan prefijado:** [`research/plans/2026-11-11-target-als-motor-cortex.md`](../../research/plans/2026-11-11-target-als-motor-cortex.md), commit `59f8394`, **anterior a descargar las uniones**.
**Etiqueta de evidencia:** descriptivo exploratorio en tejido post mortem. Sin PSI inferencial, sin p-valores, sin efectos. **Ni rescate, ni causalidad, ni beneficio clínico.**

Esta **no** es la pregunta original de #37, que pedía un contraste frente a depleción experimental. Es tejido de paciente, y se informa como tal.

## Procedencia y controles de montaje, todos superados

TARGET_ALS, tejido `TALS_Cortex_Motor_Lateral`, vía recount3. Descargado: **194 MB** frente al presupuesto de 400 MB. Matriz de **2.678.581 uniones × 149 muestras**, 42.269.332 valores no nulos.

| Control | Resultado |
|---|---|
| ¿Ensayo dirigido? | **No**: 2.678.581 uniones, 4,6 % en chr19, 127 cromosomas |
| Convención de coordenadas | **Superada** (el guardián aborta si `length ≠ end − start + 1`) |
| Coincidencia de las tres uniones selladas | **Exacta**, sin desplazar extremos |
| Patrón de anotación | canónica `annotated=1`; ambas crípticas `annotated=0` |

**Cobertura canónica: mediana 102–148 lecturas por muestra**, frente a 7–66 en las motoneuronas de Klim. La hipótesis de expresión cortical **queda apoyada**: el locus UNC13A está entre 2 y 3 veces mejor cubierto en corteza motora.

## Evidencia

Grupos **declarados por el depósito**. Las 23 muestras sin etiqueta se informan aparte y **no se imputan**; el grupo mixto no se fusiona con ELA pura.

| Grupo | n | Con alguna lectura críptica | Con ≥20 | Fracción críptica (mediana / máx.) | Canónica (mediana) |
|---|---:|---:|---:|---|---:|
| **ALS Spectrum MND** | 84 | **16** | **0** | 0,000 / 0,0796 | 102 |
| ALS Spectrum MND + Other Neuro | 25 | **7** | **0** | 0,000 / 0,0509 | 105 |
| (sin etiqueta) | 23 | 2 | 0 | 0,000 / 0,0291 | 101 |
| **Non-Neurological Control** | 13 | **0** | 0 | 0,000 / 0,000 | 148 |
| Other Neurological Disorders | 3 | **0** | 0 | 0,000 / 0,000 | 139 |
| Pre-fALS + Other Neuro | 1 | 0 | 0 | 0,000 / 0,000 | 26 |

**Separación cualitativa: 23 de 109 muestras del espectro ELA (21 %) presentan lecturas crípticas; 0 de 17 muestras no-ELA presentan ninguna** (13 controles no neurológicos, 3 otros trastornos neurológicos, 1 pre-fALS). Y eso con los controles teniendo **mejor** cobertura canónica (mediana 148) que los casos de ELA, de modo que el cero de los controles no se explica por menos profundidad.

## Las tres predicciones prefijadas

| | Predicción | Resultado |
|---|---|---|
| **P1** | Al menos una muestra de ELA alcanzará ≥20 lecturas crípticas | **REFUTADA.** 0 de 149 |
| **P2** | La mediana de fracción críptica en ELA quedará por debajo de 0,10 | **CONFIRMADA.** Mediana 0,000; máximo 0,0796 |
| **P3** | La fracción será mayor en ELA que en controles | **CONFIRMADA en dirección.** 21 % frente a 0 % con alguna lectura |

P1 se registra como refutada, sin reinterpretarla.

## Interpretación

### Por qué el umbral de 20 probablemente es inalcanzable aquí, y es aritmética

La cobertura canónica en esta cohorte ya es buena (mediana ~100, hasta 435). Lo que limita no es la profundidad, sino la **fracción**: como máximo 0,08, y normalmente 0.

Para obtener 20 lecturas crípticas con una fracción de 0,08 harían falta unas **250** lecturas canónicas; con 0,02, unas **1.000**. Es decir, entre 2 y 10 veces más profundidad en el locus de la que tiene **una de las cohortes de ELA más grandes que existen**.

La causa es biológica, no de disponibilidad de datos: el tejido bulk contiene mayoritariamente células **sin** pérdida nuclear de TDP-43, y esa dilución acota la fracción a unos pocos puntos porcentuales. Aumentar n no lo arregla; haría falta enriquecimiento celular (como los núcleos clasificados por FACS de GSE126543) o un ensayo dirigido.

### Tercer punto de datos para la discrepancia: el amplicón es el valor atípico

| Fuente | Ensayo | Sistema | Fracción críptica |
|---|---|---|---|
| SRP166282 (Klim) | RNA-seq completo | cultivo, knockdown 58,8 % | 0,000 – 0,145 |
| **TARGET_ALS (este ciclo)** | **RNA-seq completo** | **corteza de paciente** | **0,000 – 0,0796** |
| SRP334561 (Ma) | amplicón dirigido | cultivo, shRNA | 0,390 – 0,690 |

**Las dos mediciones de transcriptoma completo coinciden en orden de magnitud** —unidades a decenas por mil— pese a venir de laboratorios distintos, décadas distintas y sistemas distintos (cultivo frente a tejido humano). La única cifra entre 5 y 10 veces superior es la del amplicón.

Honestamente: esto **no demuestra** que el amplicón esté sesgado. Cada fuente de transcriptoma tiene su propia explicación de sesgo a la baja —knockdown parcial en Klim, dilución tisular aquí—, así que la coincidencia podría ser casual. Pero desplaza la carga de la prueba: **el amplicón pasa a ser el valor atípico solitario**, y quien quiera usar 0,39–0,69 como fracción de referencia debe justificar por qué dos mediciones independientes de transcriptoma dan un orden de magnitud menos.

### Lo que el 21 % sí y no dice

Que 23 de 109 muestras del espectro ELA muestren lecturas crípticas y ninguna de las 17 no-ELA lo haga es **consistente** con que el exón críptico de UNC13A sea un marcador de patología de TDP-43 presente en un subconjunto de casos. No lo demuestra, y **la ausencia en las otras 86 no es evidencia contra el mecanismo**: con una fracción esperada de pocos puntos porcentuales y ~100 lecturas canónicas, muchas muestras con patología real caerían en cero por simple muestreo. Es dato ausente, no cero biológico.

## Limitaciones

- **P1 refutada: cero muestras alcanzan el umbral.** Esta fuente **no** supera la puerta de cobertura.
- **Tejido bulk.** La composición celular confunde toda magnitud. La razón dentro del gen mitiga, no resuelve.
- **Solo 13 controles no neurológicos.** Suficiente para una comparación descriptiva, no para una estimación estable.
- **No todo caso de ELA tiene patología de TDP-43 en corteza motora** (SOD1, FUS). La heterogeneidad observada es esperable y no se interpreta.
- **No se ha comprobado antecedentes.** El consorcio ha publicado sobre estos datos y Ma 2022 incluye una tabla suplementaria de variantes de UNC13A y STMN2 en la cohorte NYGC. **No se reclama novedad.**
- **STMN2 no se analizó**: el proyecto carece de sus coordenadas de unión selladas en hg38, y no se improvisan.
- Las cuantificaciones son de la tubería de recount3; otra herramienta contaría distinto.
- No se ajustó ningún modelo ni se comprobaron intervalo post mortem ni RIN en este ciclo.
- **Datos personales:** se leyó **únicamente** la columna de grupo. Sexo, etnia, edades y sitio de inicio **no se leyeron**, ninguna fila clínica individual aparece en la salida, y el archivo de metadatos no se versiona.

## Siguiente prueba discriminante

1. **Córtex frente a médula en la misma cohorte.** TARGET_ALS incluye `Spinal_Cord_Cervical`, `Lumbar` y `Thoracic`. Comparar la cobertura canónica y la fracción críptica entre tejidos del mismo consorcio es el contraste más limpio disponible de la hipótesis de dependencia por tipo neuronal (H1), y controla cohorte y tubería. Ciclo propio, otros ~200 MB por tejido.
2. **La vía que la aritmética señala** para superar el umbral no es más n ni más profundidad, sino **enriquecimiento celular**: núcleos neuronales clasificados por presencia o ausencia de TDP-43, como GSE126543. Ese dataset no tiene registros SRA alcanzables, así que requeriría otra ruta de acceso.

**Criterio de cierre propuesto para la puerta de cobertura de #37:** con este ciclo, dos de las tres explicaciones posibles del fracaso repetido quedan descartadas —no es falta de acceso ni falta de tamaño de cohorte—. Si la comparación con médula confirma que la fracción en tejido se mantiene en pocos puntos porcentuales, lo honesto será concluir que **medir estas uniones con el criterio ≥20 exige datos enriquecidos o dirigidos**, y cerrar esa puerta como inalcanzable con RNA-seq público de transcriptoma completo, en vez de seguir probando datasets.

Sin contactos, gastos, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
