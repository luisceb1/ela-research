# Médula cervical frente a corteza motora: 21× menos cobertura de UNC13A con profundidad idéntica

**Fecha:** 2026-11-11. **Plan prefijado:** [`research/plans/2026-11-11-target-als-cervical-cord.md`](../../research/plans/2026-11-11-target-als-cervical-cord.md), commit `9816f9d`, **anterior a descargar las uniones de médula**. El diseño incorpora las cinco correcciones de la revisión externa del ciclo anterior.
**Etiqueta de evidencia:** descriptivo exploratorio en tejido post mortem, **comparación no emparejada entre tejidos**. Sin p-valores entre tejidos, sin efectos, sin interpretación clínica.

## Lo que hace esta comparación inusualmente limpia, y lo que no

**A favor:** mismo consorcio, misma tubería de cuantificación, mismos criterios de grupo, mismas coordenadas selladas. Y un dato comprobado, no supuesto: **la profundidad de secuenciación es idéntica** — mediana de **44,4 M** lecturas asignadas a exones en ambos tejidos, ratio **1,00**. Esto elimina el confusor que invalidó mi comparación anterior con Klim.

**En contra, declarado de antemano:** los metadatos **no exponen identidad de donante** (`CGND-HRA-…` identifica muestra, no sujeto; no hay columna de sujeto). El número de sujetos por tejido es **desconocido** y la comparación es **entre conjuntos de muestras distintos, no emparejada**.

Controles de montaje superados en médula: no parece dirigido (2.695.965 uniones, 4,8 % en chr19, 119 cromosomas); las tres uniones selladas coinciden exactamente; patrón de anotación correcto. Descargado 213 MB frente al presupuesto de 400 MB.

## Tabla por tejido: el entregable

Tabla completa en [`tissue_comparison.tsv`](tissue_comparison.tsv).

| Tejido | Grupo | n | Sujetos | Lecturas exón (mediana) | Canónica (mediana) | **Canónica por millón** | Con alguna lectura críptica | Detección [Wilson 95 %] | ≥20 |
|---|---|---:|---|---:|---:|---:|---:|---|---:|
| Corteza motora | ALS Spectrum MND | 84 | desconocido | 44,4 M | 102 | **2,30** | 16 | 0,190 [0,121–0,287] | 0 |
| Corteza motora | Control no neurológico | 13 | desconocido | 44,4 M | 148 | **3,33** | 0 | 0,000 [0,000–0,228] | 0 |
| Médula cervical | ALS Spectrum MND | 95 | desconocido | 44,4 M | 5 | **0,11** | 5 | 0,053 [0,023–0,117] | 0 |
| Médula cervical | Control no neurológico | 13 | desconocido | 44,4 M | 8 | **0,18** | 0 | 0,000 [0,000–0,228] | 0 |

## Las tres predicciones prefijadas

| | Predicción | Resultado |
|---|---|---|
| **P1** | Cobertura canónica normalizada **menor** en médula cervical | **CONFIRMADA, y con margen amplio: 21× menor** (2,30 frente a 0,11 por millón en ELA) |
| **P2** | Menor proporción de muestras ELA con alguna lectura críptica en médula | **CONFIRMADA.** 0,053 frente a 0,190; los intervalos de Wilson **no se solapan** (0,117 < 0,121), por poco |
| **P3** | Ninguna muestra de médula alcanzará 20 lecturas en una unión críptica | **CONFIRMADA.** Máximo 2 |

## Interpretación

### El hallazgo principal: la diferencia tisular es real, grande y ahora está medida con profundidad controlada

Con la profundidad igualada por diseño del propio consorcio, **UNC13A está unas 21 veces menos cubierto en médula cervical que en corteza motora**. Esto convierte en comprobada, dentro de una sola cohorte y tubería, la observación que Ikegami 2026 y el panel GTEx de Mallika 2026 hacían entre estudios.

Y explica retrospectivamente los fracasos del proyecto: **el piloto cerrado y el dataset de Klim eran de motoneuronas espinales**, es decir el tejido donde UNC13A está peor cubierto. No era mala suerte ni mala ejecución; era el tejido equivocado para este locus.

### La menor detección en médula NO requiere una biología distinta

La detección es menor en médula (5,3 % frente a 19,0 %), pero **eso es lo que se espera de 21× menos cobertura por sí sola**. Donde no hay lecturas no puede haber lecturas crípticas. Esta comparación **no** aporta evidencia de que la inclusión críptica difiera entre tejidos, y no se presenta como tal.

### En médula, ninguna razón es interpretable

Con cobertura canónica mediana de **5** lecturas en ELA cervical, los cocientes carecen de sentido: el «PSI máximo» de 0,33 que aparece en el grupo mixto es **una lectura críptica sobre dos canónicas**. Es ruido de muestreo, no señal. La columna `ratio_interpretable` de la tabla lo marca como `no` para médula.

Esto es, en sí mismo, una lección metodológica: **una razón sin denominador mínimo no es una medida**, y publicar PSI de loci con cobertura de un dígito produce cifras que parecen informativas y no lo son.

### La pregunta se formuló sobre tejidos, y así se responde

El tejido contiene varios tipos celulares. Este contraste **no identifica una dependencia del tipo neuronal** y no se usa para sostener H1. Solo dice que estas uniones se cubren mucho peor en médula cervical que en corteza motora.

## Conclusión acotada, como se fijó de antemano

De los cinco datasets examinados, **ninguno alcanza el umbral de 20 lecturas en una unión críptica**. **Esta búsqueda se cierra por falta de precisión con los datos examinados.**

No se concluye que el umbral sea inalcanzable en todo el RNA-seq público. Lo que sí queda establecido, con evidencia, es **dónde no buscar**: en médula espinal, donde el locus está 21× peor cubierto; y por qué más muestras no bastarían, si la explicación por dilución es correcta.

La vía que la evidencia señala para superar el umbral no es más n ni más profundidad, sino **enriquecimiento celular** —núcleos neuronales clasificados por presencia o ausencia de TDP-43, como GSE126543— o un ensayo dirigido. Ese dataset no tiene registros SRA alcanzables, de modo que exigiría otra ruta de acceso.

## Limitaciones

- **Comparación no emparejada**, sin identidad de donante y con número de sujetos desconocido por tejido.
- **Tejido bulk**; composición celular no medida y confusora de toda magnitud.
- **13 controles por tejido.** Su 0/13 es compatible con tasas de hasta 22,8 %, de modo que **no se puede distinguir a los controles de la ELA cortical** solo por proporción de detección. La separación limpia del ciclo anterior se sostiene como patrón, no como contraste estadístico.
- Los intervalos de Wilson de ELA no se solapan **por muy poco** (0,117 frente a 0,121); con 95 % de confianza y confusores no medidos, no se construye una afirmación fuerte sobre ello.
- **Sin p-valores entre tejidos**: conjuntos de muestras distintos, sin emparejamiento, con confusores no medidos.
- **STMN2 no se analizó**: sin coordenadas selladas en hg38.
- **No se reclama novedad**: el consorcio ha publicado sobre estos datos.
- **Lumbar y torácica no se descargaron**, conforme al plan.
- **Datos personales:** se leyó **únicamente** la columna de grupo; sexo, etnia, edades y sitio de inicio **no se leyeron**; ninguna fila clínica individual aparece en la salida; el archivo de metadatos no se versiona.

## Siguiente paso

No proponer otro dataset de transcriptoma completo para esta pregunta. Las dos continuaciones con sentido son:

1. **Enriquecimiento celular**, que exige una ruta de acceso a datos de núcleos clasificados.
2. Llevar el hallazgo tisular y el de cronología a quien tenga laboratorio, que es lo que este proyecto no puede hacer por sí mismo.

Sin contactos, gastos, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
