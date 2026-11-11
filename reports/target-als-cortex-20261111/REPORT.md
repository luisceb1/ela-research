# Corteza motora de 149 pacientes: separación por grupo limpia, con 1–4 lecturas por muestra positiva

**Fecha:** 2026-11-11, **corregido el mismo día** tras una revisión externa (ver «Correcciones»). **Plan prefijado:** [`research/plans/2026-11-11-target-als-motor-cortex.md`](../../research/plans/2026-11-11-target-als-motor-cortex.md), commit `59f8394`, **anterior a descargar las uniones**.
**Etiqueta de evidencia:** descriptivo exploratorio en tejido post mortem. Sin PSI inferencial, sin p-valores, sin efectos. **Ni rescate, ni causalidad, ni beneficio clínico.**

Esta **no** es la pregunta original de #37, que pedía un contraste frente a depleción experimental. Es tejido de paciente, y se informa como tal.

## Correcciones aplicadas tras revisión externa

Luis sometió la primera versión a un segundo lector (ChatGPT), que señaló cuatro sobreafirmaciones. **Verifiqué las cuatro y todas eran correctas.** Es la primera revisión independiente que recibe este proyecto, y encontró errores que yo no vi:

| # | Afirmación original | Comprobación | Corrección |
|---|---|---|---|
| 1 | «La hipótesis de expresión cortical queda apoyada», por cobertura canónica 102–148 frente a 7–66 | Las librerías de TARGET_ALS tienen **44,4 M** lecturas asignadas a exones (mediana) frente a **21,8 M** en Klim: **2× más profundas** | Casi toda la diferencia era profundidad de secuenciación. Normalizado queda ≈1,8×, evidencia **débil** entre estudios distintos, no demostración |
| 2 | Razón críptica = (cL+cR)/(cL+cR+canónica) | Una molécula **con** exón críptico ofrece **dos** uniones donde leer; una sin él, **una**. Sumarlas infla ≈2× a valores bajos | Se informan **ambas** razones y **cada unión por separado**. El máximo baja de 0,0796 a **0,0414** en estimación por unión |
| 3 | «La causa es biológica, no de disponibilidad de datos» | No se ha medido composición celular en estas muestras | Es una **explicación plausible**, no una causa demostrada |
| 4 | «Cerrar esa puerta como inalcanzable con RNA-seq público» | Se examinaron cuatro datasets, no todo el RNA-seq público | Alcance limitado a **los datos examinados** |

Se añade un hallazgo propio de la verificación: **los metadatos no exponen identidad de donante** (`CGND-HRA-…` es identificador de muestra y no hay columna de sujeto), de modo que el emparejamiento entre tejidos **no se puede establecer en ninguna dirección**.

## Procedencia y controles de montaje

TARGET_ALS, tejido `TALS_Cortex_Motor_Lateral`, vía recount3. Descargado **194 MB** frente al presupuesto de 400 MB. Matriz de **2.678.581 uniones × 149 muestras**.

| Control | Resultado |
|---|---|
| ¿Ensayo dirigido? | **No**: 2,68 M uniones, 4,6 % en chr19, 127 cromosomas |
| Convención de coordenadas | **Superada** (el guardián aborta si `length ≠ end − start + 1`) |
| Coincidencia de las tres uniones selladas | **Exacta**, sin desplazar extremos |
| Patrón de anotación | canónica `annotated=1`; ambas crípticas `annotated=0` |

## Evidencia

Grupos **declarados por el depósito**. Las 23 sin etiqueta se informan aparte y **no se imputan**; el grupo mixto no se fusiona con ELA pura.

| Grupo | n | cL: muestras con lectura (máx.) | cR: muestras con lectura (máx.) | Razón sumada (mediana/máx.) | PSI por unión (mediana/máx.) | Canónica (mediana) |
|---|---:|---|---|---|---|---:|
| **ALS Spectrum MND** | 84 | **7** (3) | **11** (4) | 0,000 / 0,0796 | 0,000 / **0,0414** | 102 |
| ALS + Other Neuro | 25 | 6 (3) | 2 (2) | 0,000 / 0,0509 | 0,000 / 0,0261 | 105 |
| (sin etiqueta) | 23 | 1 (2) | 2 (1) | 0,000 / 0,0291 | 0,000 / 0,0148 | 101 |
| **Non-Neurological Control** | 13 | **0** (0) | **0** (0) | 0,000 / 0,000 | 0,000 / 0,000 | 148 |
| Other Neurological Disorders | 3 | 0 (0) | 0 (0) | 0,000 / 0,000 | 0,000 / 0,000 | 139 |
| Pre-fALS + Other Neuro | 1 | 0 (0) | 0 (0) | 0,000 / 0,000 | 0,000 / 0,000 | 26 |

Dos lecturas de esta tabla, y la segunda modera la primera:

**Separación por grupo, limpia:** 23 de 109 muestras del espectro ELA (21 %) presentan alguna lectura críptica en alguna de las dos uniones; **0 de 17 muestras no-ELA presentan ninguna**. Y los controles tienen **mejor** cobertura canónica (mediana 148), así que su cero no se explica por menos profundidad.

**Precisión por muestra, muy baja:** el máximo en **una sola** unión críptica es de **4 lecturas**. Cada positivo individual se sostiene sobre 1–4 lecturas. El patrón es de grupo; ninguna muestra aislada constituye evidencia.

## Las tres predicciones prefijadas

| | Predicción | Resultado |
|---|---|---|
| **P1** | Al menos una muestra de ELA alcanzará ≥20 lecturas crípticas | **REFUTADA.** 0 de 149; máximo por unión 4 |
| **P2** | La mediana de razón críptica en ELA quedará por debajo de 0,10 | **CONFIRMADA.** Mediana 0,000 en ambas definiciones |
| **P3** | La razón será mayor en ELA que en controles | **CONFIRMADA en dirección.** 21 % frente a 0 % con alguna lectura |

P1 se registra como refutada, sin reinterpretarla.

## Interpretación

### Por qué el umbral de 20 no se alcanza aquí, con alcance limitado

La cobertura canónica de esta cohorte es buena (mediana ~100, hasta 435) y sus librerías son profundas (44,4 M lecturas de exón). Lo que limita no es la profundidad: es la **razón**, con máximo 0,04 por unión y normalmente 0.

Aritmética: para 20 lecturas en una unión críptica con razón 0,04 harían falta unas **500** lecturas canónicas; con 0,01, unas **2.000**. Es decir, entre 5 y 20 veces la profundidad en el locus que tiene esta cohorte, que es de las mayores que existen.

**Explicación más plausible, no demostrada:** el tejido bulk contiene mayoritariamente células **sin** pérdida nuclear de TDP-43, y esa dilución acotaría la razón a pocos puntos porcentuales. No se ha medido composición celular en estas muestras, así que es una hipótesis coherente con los datos, no una causa establecida. Si es correcta, aumentar n no ayudaría y sí ayudaría el **enriquecimiento celular** (núcleos clasificados por presencia o ausencia de TDP-43, como GSE126543) o un ensayo dirigido.

**Alcance:** esto concierne a los **cuatro datasets examinados**. No se afirma nada sobre todo el RNA-seq público.

### Tercer punto de datos para la discrepancia

Todas las cifras recalculadas con la **estimación por unión**, para que sean comparables entre sí:

| Fuente | Ensayo | Sistema | PSI por unión (aprox.) |
|---|---|---|---|
| SRP166282 (Klim) | RNA-seq completo | cultivo, knockdown 58,8 % | ~0,00 – 0,078 |
| **TARGET_ALS (este ciclo)** | **RNA-seq completo** | **corteza de paciente** | **0,00 – 0,041** |
| SRP334561 (Ma) | amplicón dirigido | cultivo, shRNA | ~0,24 – 0,53 |

Las dos mediciones de transcriptoma completo coinciden en orden de magnitud —unidades por cien— pese a venir de laboratorios, décadas y sistemas distintos. El amplicón sigue siendo entre **6 y 13 veces** superior.

Honestamente: **no demuestra** que el amplicón esté sesgado. Cada fuente de transcriptoma tiene su propia explicación de sesgo a la baja —knockdown parcial en Klim, posible dilución tisular aquí—, así que la coincidencia podría ser casual. Pero el amplicón queda como **el valor atípico solitario**, y quien quiera usarlo como referencia debe justificar por qué dos mediciones independientes dan un orden de magnitud menos.

### Lo que el 21 % no dice

La ausencia en las otras 86 muestras del espectro ELA **no es evidencia contra el mecanismo**: con razón esperada de pocos puntos y ~100 lecturas canónicas, muchas muestras con patología real caerían en cero por muestreo. Es dato ausente, no cero biológico. Además no todo caso de ELA tiene patología de TDP-43 en corteza motora (SOD1, FUS).

## Limitaciones

- **P1 refutada.** Esta fuente **no** supera la puerta de cobertura, y la precisión por muestra es de 1–4 lecturas.
- **Tejido bulk.** La composición celular confunde toda magnitud, y no se midió. La razón dentro del gen mitiga, no resuelve.
- **Solo 13 controles no neurológicos.** Descriptivo, no estimación estable.
- **Sin identidad de donante** en los metadatos: no se puede saber cuántos sujetos aportan más de una muestra ni emparejar entre tejidos.
- **La comparación con Klim cruza estudios**, protocolos y décadas; incluso normalizada por profundidad es evidencia débil.
- **No se ha comprobado antecedentes.** El consorcio ha publicado sobre estos datos y Ma 2022 incluye una tabla suplementaria de variantes de UNC13A y STMN2 en la cohorte NYGC. **No se reclama novedad.**
- **STMN2 no se analizó**: el proyecto carece de sus coordenadas selladas en hg38 y no se improvisan.
- Cuantificaciones de la tubería de recount3; otra herramienta contaría distinto. No se comprobaron intervalo post mortem ni RIN.
- **Datos personales:** se leyó **únicamente** la columna de grupo. Sexo, etnia, edades y sitio de inicio **no se leyeron**, ninguna fila clínica individual aparece en la salida, y el archivo de metadatos no se versiona.

## Siguiente prueba discriminante

**Médula cervical de la misma cohorte**, con su propio plan prefijado. Es el contraste disponible más limpio porque comparte consorcio, tubería y criterios de grupo — pero **no** comparte donantes comprobables, de modo que será una comparación **entre conjuntos de muestras distintos**, no emparejada.

Y la pregunta se formula sobre **tejidos**, no sobre tipos celulares: *¿difieren la cobertura y el uso relativo de estas uniones entre corteza motora y médula cervical?* El tejido contiene varios tipos celulares, así que ese contraste **no identifica por sí solo una dependencia del tipo neuronal**.

Lumbar y torácica quedan fuera salvo que aporten una comprobación necesaria.

Sin contactos, gastos, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
