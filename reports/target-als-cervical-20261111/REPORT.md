# Médula cervical frente a corteza motora: 22× menos cobertura de UNC13A

**Fecha:** 2026-11-11. **Plan prefijado:** [`research/plans/2026-11-11-target-als-cervical-cord.md`](../../research/plans/2026-11-11-target-als-cervical-cord.md), commit `9816f9d`, **anterior a descargar las uniones de médula**. El diseño incorpora las cinco correcciones de la revisión externa del ciclo anterior.
**Etiqueta de evidencia:** descriptivo exploratorio en tejido post mortem, **comparación no emparejada entre tejidos**. Sin p-valores entre tejidos, sin efectos, sin interpretación clínica.

> ## Historial de correcciones de la cifra central
>
> Esta cifra se ha publicado tres veces y **las dos primeras no eran defendibles**. Queda constancia porque el lector tiene derecho a saber cuántas veces se corrigió y por qué.
>
> | Versión | Cifra | Qué estaba mal |
> |---|---|---|
> | 1 (mañana) | **20,9×**; «canónica por millón» 2,30 y 0,11 | Dividía la **mediana del grupo** por una **única** mediana de profundidad de 44,4 M aplicada a los dos tejidos. Es una **razón de medianas**, no una normalización por biblioteca. Además el informe llamaba a ese campo «lecturas asignadas a exones»: **no lo es.** Es `exon_fc_count_all.total`, las lecturas *entregadas* a featureCounts. Las realmente asignadas difieren entre tejidos (20,3 M frente a 23,9 M), de modo que la afirmación de que la profundidad «es idéntica» solo se sostenía para el campo que no se nombraba. El informe también decía que eso «elimina el confusor»: coincidir en una mediana no elimina nada |
> | 2 (tarde) | **22,3×**; 2,530 y 0,113 | **La aritmética era correcta, el procedimiento no existía.** Se anunció sin código depositado y con el denominador mal nombrado, así que un lector externo no pudo reproducirlo: probando `.assigned` sale 0,2055 y con lecturas de entrada 0,1150, y ninguna es 0,113. Una cifra correcta e irreproducible no es un estado aceptable para un informe publicado |
> | **3 (esta)** | **22,33×** | Calculada por [`scripts/normalize_tissue_coverage.py`](../../scripts/normalize_tissue_coverage.py), con el campo QC nombrado, hashes de entrada, rangos por biblioteca, los **cinco** denominadores candidatos y seis pruebas, una de ellas dedicada a que mediana-de-razones no vuelva a confundirse con razón-de-medianas. Salida completa: [`depth_normalisation.json`](depth_normalisation.json) |
>
> La dirección y el orden de magnitud se mantuvieron en las tres. El método no.

## Lo que hace esta comparación inusualmente limpia, y lo que no

**A favor:** mismo consorcio, misma tubería de cuantificación, mismos criterios de grupo, mismas coordenadas selladas.

**Sobre la profundidad, con precisión esta vez:** la mediana de `exon_fc_count_all.total` del conjunto de cada tejido coincide (44,387 M y 44,389 M), pero **por grupo no coincide**: los controles están más profundos que la ELA en los dos tejidos (50,4 M frente a 42,7 M en corteza; 49,5 M frente a 43,2 M en médula). Por eso cada biblioteca se normaliza por la suya, y por eso la coincidencia de medianas no era un control.

**En contra, declarado:** la comparación es **entre conjuntos de muestras distintos y no emparejada**. El proyecto dispone de un mapa de donante que establece **45 pares corteza–médula** (recuperado en la PR #57 a partir de la tabla ST7, no de los metadatos de recount3, que no exponen identidad de sujeto). **Ese emparejamiento no se usa aquí**: este contraste se diseñó y prefijó sin él. Un contraste emparejado sobre los 45 pares es una continuación legítima y pendiente, no algo que este informe pueda reclamar.

Controles de montaje superados en médula: no parece dirigido (2.695.965 uniones, 4,8 % en chr19, 119 cromosomas); las tres uniones selladas coinciden exactamente; patrón de anotación correcto. Descargado 213 MB frente al presupuesto de 400 MB.

## Tabla por tejido: el entregable

Tabla completa en [`tissue_comparison.tsv`](tissue_comparison.tsv), con rangos por biblioteca, el denominador alternativo y la razón de medianas retirada, para que la columna publicada se pueda auditar contra las dos que no se eligieron.

| Tejido | Grupo | n | Profundidad mediana | Canónica (mediana) | **Canónica por millón** (mediana de razones por biblioteca) | Rango por biblioteca | Detección [Wilson 95 %] | ≥20 |
|---|---|---:|---:|---:|---:|---|---|---:|
| Corteza motora | ALS Spectrum MND | 84 | 42,7 M | 102 | **2,530** | 0,139–4,240 | 0,190 [0,121–0,287] | 0 |
| Corteza motora | Control no neurológico | 13 | 50,4 M | 148 | **2,845** | 0,750–5,819 | 0,000 [0,000–0,228] | 0 |
| Médula cervical | ALS Spectrum MND | 95 | 43,2 M | 5 | **0,113** | 0,000–0,763 | 0,053 [0,023–0,117] | 0 |
| Médula cervical | Control no neurológico | 13 | 49,5 M | 8 | **0,174** | 0,000–0,442 | 0,000 [0,000–0,228] | 0 |

Denominador: `exon_fc_count_all.total`. **La elección de denominador mueve la cifra**, y por eso se publican todas: 22,33× con este campo, 25,55× con `exon_fc_count_all.assigned`, 23,56× con lecturas de entrada, 22,86× con lecturas mapeadas, 22,16× con lecturas mapeadas de forma única. **El hallazgo no depende de la elección**; el intervalo de 22× a 26× sí.

## Las tres predicciones prefijadas

| | Predicción | Resultado |
|---|---|---|
| **P1** | Cobertura canónica normalizada **menor** en médula cervical | **CONFIRMADA. 22,33× menor** (2,530 frente a 0,113 por millón en ELA), y entre 22,2× y 25,6× bajo los cinco denominadores |
| **P2** | Menor proporción de muestras ELA con alguna lectura críptica en médula | **CONFIRMADA en la proporción:** 0,053 frente a 0,190. Los intervalos de Wilson no se solapan, pero **por 0,004** (0,117 frente a 0,121), lo que **no constituye una separación interpretable**; y la propia predicción es poco informativa, porque con 22× menos cobertura una detección menor es lo esperado sin necesidad de biología distinta |
| **P3** | Ninguna muestra de médula alcanzará 20 lecturas en una unión críptica | **CONFIRMADA.** Máximo 2 |

## Interpretación

### El hallazgo principal: la diferencia tisular es grande y ahora es reproducible

Normalizando cada biblioteca por su propia profundidad, **UNC13A está unas 22 veces menos cubierto en médula cervical que en corteza motora**. No se afirma que la profundidad quede «controlada»: se normaliza, la comparación sigue siendo **no emparejada** y hay confusores no medidos, la composición celular entre otros. Esto comprueba, dentro de una sola cohorte y tubería, la observación que Ikegami 2026 y el panel GTEx de Mallika 2026 hacían entre estudios.

Y ofrece una explicación plausible de los fracasos del proyecto: **el piloto cerrado y el dataset de Klim eran de motoneuronas espinales**, donde este locus está mucho peor cubierto. Es una explicación retrospectiva de la cobertura, **no una demostración de que la cobertura fuese la única causa** de aquellos fracasos; no se afirma que fuera «el tejido equivocado», porque eso presupone que la cobertura explica todo lo que falló.

### La menor detección en médula NO requiere una biología distinta

La detección es menor en médula (5,3 % frente a 19,0 %), pero **eso es lo que se espera de 22× menos cobertura por sí sola**. Donde no hay lecturas no puede haber lecturas crípticas. Esta comparación **no** aporta evidencia de que la inclusión críptica difiera entre tejidos, y no se presenta como tal.

### En médula, ninguna razón es interpretable

Con cobertura canónica mediana de **5** lecturas en ELA cervical, los cocientes carecen de sentido: el «PSI máximo» de 0,33 que aparece en el grupo mixto es **una lectura críptica sobre dos canónicas**. Es ruido de muestreo, no señal. La columna `ratio_interpretable` lo marca como `no` para médula.

Esto es, en sí mismo, una lección metodológica: **una razón sin denominador mínimo no es una medida**, y publicar PSI de loci con cobertura de un dígito produce cifras que parecen informativas y no lo son.

### Un dato colateral que no se explota

En los dos tejidos la cobertura canónica normalizada es **menor en ELA que en los controles** (2,530 frente a 2,845; 0,113 frente a 0,174). Es la dirección que cabría esperar si la pérdida de TDP-43 redujera el empalme canónico, pero con **13 controles**, sin emparejar y sin contraste prefijado, **no se somete a prueba ni se interpreta**. Queda anotado como observación, con el emparejamiento de 45 pares como vía para examinarlo en serio.

### La pregunta se formuló sobre tejidos, y así se responde

El tejido contiene varios tipos celulares. Este contraste **no identifica una dependencia del tipo neuronal** y no se usa para sostener H1. Solo dice que estas uniones se cubren mucho peor en médula cervical que en corteza motora.

## Conclusión acotada, como se fijó de antemano

De los cinco datasets examinados, **ninguno alcanza el umbral de 20 lecturas en una unión críptica**. **Esta búsqueda se cierra por falta de precisión con los datos examinados.**

No se concluye que el umbral sea inalcanzable en todo el RNA-seq público. Lo que sí queda establecido, con evidencia, es **dónde la cobertura es peor** —médula espinal, unas 22 veces— y por qué más muestras no bastarían, si la explicación por dilución es correcta.

La vía que la evidencia señala para superar el umbral no es más n ni más profundidad, sino **enriquecimiento celular** —núcleos neuronales clasificados por presencia o ausencia de TDP-43, como GSE126543— o un ensayo dirigido. Ese dataset no tiene registros SRA alcanzables, de modo que exigiría otra ruta de acceso.

## Limitaciones

- **Comparación no emparejada.** Existen 45 pares de donante en el proyecto, **no usados aquí**.
- **Tejido bulk**; composición celular no medida y confusora de toda magnitud.
- **13 controles por tejido.** Su 0/13 es compatible con tasas de hasta 22,8 %, de modo que **no se puede distinguir a los controles de la ELA cortical** solo por proporción de detección. La separación limpia del ciclo anterior se sostiene como patrón, no como contraste estadístico.
- **La no superposición de los intervalos de Wilson en P2 es de 0,004** y no se usa para sostener ninguna afirmación.
- **La cifra central depende del denominador** entre 22,2× y 25,6×. Se publica el intervalo completo.
- **Sin p-valores entre tejidos**: conjuntos de muestras distintos, sin emparejamiento, con confusores no medidos.
- **STMN2 no se analizó en este ciclo**: sin coordenadas selladas en hg38 en su momento. Ya las tiene.
- **No se reclama novedad**: el consorcio ha publicado sobre estos datos.
- **Lumbar y torácica no se descargaron**, conforme al plan.
- **Datos personales:** se leyó **únicamente** la columna de grupo y, para la normalización, `rail_id` y columnas QC numéricas; sexo, etnia, edades y sitio de inicio **no se leyeron**; ninguna fila clínica individual aparece en la salida; el archivo de metadatos no se versiona.

## Reproducir la cifra central

```
python -I scripts/normalize_tissue_coverage.py \
  --tissue 'Cortex_Motor_Lateral:reports/target-als-cortex-20261111/results.json:<qc.MD.gz>' \
  --tissue 'Spinal_Cord_Cervical:reports/target-als-cervical-20261111/results.json:<qc_cerv.MD.gz>' \
  --json reports/target-als-cervical-20261111/depth_normalisation.json
```

Los dos `qc*.MD.gz` provienen de `recount3`, proyecto TARGET_ALS; sus SHA256 están en `depth_normalisation.json`. No se versionan porque contienen la tabla QC completa del consorcio.

## Siguiente paso

No proponer otro dataset de transcriptoma completo para esta pregunta. Las continuaciones con sentido son:

1. **El contraste emparejado sobre los 45 pares**, con un único contraste prefijado, que es lo que este informe no hizo.
2. **Enriquecimiento celular**, que exige una ruta de acceso a datos de núcleos clasificados.
3. Llevar el hallazgo tisular y el de cronología a quien tenga laboratorio.

Sin contactos, gastos, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
