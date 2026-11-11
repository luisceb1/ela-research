# STMN2: lecturas crípticas suficientes en cuatro muestras cervicales de ELA

**Revisión:** auditoría posterior de [medida y unidades](../stmn2-map-audit-20261111/REPORT.md). Corrige P1, la interpretación de P3 y las limitaciones de donante; conserva los conteos originales.

**Fecha:** 2026-11-11. **Plan prefijado:** [`research/plans/2026-11-11-stmn2-junction-derivation.md`](../../research/plans/2026-11-11-stmn2-junction-derivation.md), commit `c378db1`, **anterior a derivar coordenadas o calcular nada**.
**Etiqueta de evidencia:** derivación de coordenadas verificada + medición descriptiva en tejido post mortem. Sin contraste inferencial, sin efectos, sin p-valores entre grupos.

**No se reclama ningún descubrimiento.** El splicing críptico de STMN2 en médula espinal de ELA es uno de los hallazgos más replicados del campo. Lo nuevo **para este proyecto** es que por primera vez puede medirlo con cobertura suficiente.

## Parte 1: derivación de coordenadas, y una corrección a mi propio criterio

El proyecto no tenía coordenadas de uniones de STMN2 en hg38. La derivación **no** usó ninguna conversión de ensamblaje improvisada.

### Ancla doble, independiente y concordante

Transcrito `NM_007029.4`, pista `ncbiRefSeq` de UCSC, consultada en **ambos** ensamblajes:

| Rasgo | hg19 | hg38 | Desplazamiento |
|---|---:|---:|---:|
| Fin del exón 1 | 80.523.449 | 79.611.214 | **912.235** |
| Inicio del exón 2 | 80.549.036 | 79.636.801 | **912.235** |

Dos rasgos distintos del mismo transcrito dan **el mismo desplazamiento**. Son anclas concordantes, pero por sí solas no prueban la alineación de la región intermedia. La auditoría posterior la comprobó con la cadena UCSC hg19→hg38 y contrastó el inicio con la coordenada hg38 de Melamed 2019. Los límites RefSeq de esta tabla son 0-based.

Aplicado al intervalo de conteo del exón críptico publicado (hg19 `chr8:80.529.057–80.529.284`, ancho 228, DOI `10.1007/s00401-023-02655-0`): **hg38 79.616.822–79.617.049**. Es un intervalo de conteo: Melamed describe el extremo de un transcrito de 227 nt en 79.617.048, una base antes; el inicio aceptor es el mismo.

### Verificación cruzada que resultó decisiva

La unión observada `chr8:79.611.215–79.616.821` (intrón, 1-based inclusivo) sitúa el inicio de su exón aceptor en **79.616.822**: **exactamente** el inicio derivado del exón críptico publicado.

Y la canónica `chr8:79.611.215–79.636.801` coincide **exactamente** con el fin del exón 1 y el inicio del exón 2 de `NM_007029.4` en hg38.

### Mi criterio prefijado era erróneo, y el cruce lo corrigió

El plan exigía `annotated=0` para la unión críptica. **La unión verdadera está marcada `annotated=1`** en el conjunto de referencia de recount3. Mi criterio la habría excluido.

En cambio sí pasaban todas las verificaciones estructurales **cinco** candidatas `annotated=0` con donante compartido, motivos GT/AG y aceptor en el intrón 1: aceptores en 79.613.669, 79.613.822, 79.615.701, 79.630.995 y 79.631.040. **Ninguna es el evento publicado.**

Por eso paré antes de medir, como el plan obligaba al haber más de una candidata. Si hubiera aplicado el criterio mecánicamente habría medido una unión arbitraria y la habría presentado como el exón críptico de STMN2.

Coordenadas selladas en [`research/references/stmn2_targets_sealed.json`](../../research/references/stmn2_targets_sealed.json), con el método y la corrección registrados.

### Una consecuencia sobre el denominador

El exón críptico de STMN2 es **terminal** (contiene una señal de poliadenilación prematura), de modo que hay **una sola unión críptica**, no dos como en UNC13A. Inclusión y exclusión aportan una unión cada una, así que `críptica/(críptica+canónica)` **no necesita** la corrección ×2 que sí requería UNC13A. Verificado con prueba unitaria.

## Parte 2: medición

Razones interpretadas **solo** cuando `(críptica + canónica) ≥ 20`, umbral declarado de antemano. En médula cervical, 25 de 95 muestras tienen canónica <10 y sus cocientes tienen poca precisión: el «PSI de 1,0» que aparece son **2 lecturas crípticas sobre 0 canónicas**.

Las detecciones y medianas canónicas de la tabla usan todas las muestras; las razones usan únicamente C+K≥20. Se retiran los intervalos de Wilson como criterio de confirmación de una diferencia.

| Tejido | Grupo | n total | n C+K≥20 | Canónica mediana, todas | Con K>0, todas | K≥20 | Cociente mediana / máximo, C+K≥20 |
|---|---|---:|---:|---:|---:|---:|---|
| Corteza motora | ELA pura | 84 | 82 | 632 | 31 | 0 | 0,000 / 0,029 |
| Corteza motora | Control | 13 | 12 | 883 | 1 | 0 | 0,000 / 0,009 |
| Médula cervical | ELA pura | 95 | 58 | 33 | 48 | 4 | 0,006 / 0,544 |
| Médula cervical | Control | 13 | 8 | 55 | 1 | 0 | 0,000 / 0,001 |

En cervical ELA, hay 92 denominadores no nulos y su máximo sin filtrar es 1,0; tras C+K≥20 quedan 58 y el máximo es 0,543860. La mediana coincide numéricamente (0,005684) en ambos subconjuntos. Las etiquetas de población se corrigen sin modificar ningún conteo.

Las cuatro muestras que superan el umbral, con denominadores sólidos:

| Crípticas | Canónicas | PSI |
|---:|---:|---:|
| 52 | 299 | 0,148 |
| 31 | 26 | 0,544 |
| 26 | 115 | 0,184 |
| 21 | 68 | 0,236 |

## Las tres predicciones prefijadas

| | Predicción | Resultado |
|---|---|---|
| **P1** | Cobertura canónica de STMN2 en médula ≥10× la de UNC13A (0,11 por millón) | **NO SE CUMPLE.** Medianas tras normalizar cada biblioteca por lecturas de entrada: 0,929460 frente a 0,114960 por millón, razón 8,085×. Sensibilidades 7,782× y 7,769×. La razón bruta 33/5=6,6 tampoco alcanza 10 |
| **P2** | Al menos una muestra alcanzará ≥20 lecturas crípticas | **CONFIRMADA. Cuatro muestras**, con 21–52 lecturas |
| **P3** | Detección mayor en espectro ELA que en controles | **DIRECCIÓN DESCRIPTIVA OBSERVADA** en ambas regiones (48/95 frente a 1/13 y 31/84 frente a 1/13). No es confirmación inferencial; el solapamiento de intervalos de Wilson no prueba esta hipótesis |

## Interpretación

### El evento puede medirse en algunas bibliotecas

Es la primera vez que este proyecto obtiene ≥20 lecturas en su unión críptica sellada a partir de datos públicos de transcriptoma completo. La literatura y la cadena respaldan la identidad de STMN2; cuatro bibliotecas de ELA cervical superan el umbral. Esto no valida todos los sesgos del ensayo ni establece la causa de la escasa cobertura de UNC13A.

### Diferencia descriptiva entre tejidos

La canónica STMN2 tiene mediana 632 en corteza frente a 33 en cervical entre las muestras de ELA pura, mientras que la detección críptica es 31/84 frente a 48/95. Es un patrón compatible con la literatura, pendiente de un contraste que respete donante, selección, calidad, profundidad y composición celular. No se excluye que esos factores expliquen parte de la diferencia. El cociente K/(C+K) es una medida local de lecturas, no una fracción molecular calibrada ni una medida de proteína o función.

### Lo que NO se hace aquí

No se calcula un efecto. La auditoría posterior recupera donante para 293/313 muestras y confirma cuatro donantes distintos en las cuatro bibliotecas cervicales de ELA pura con K≥20. Hay 128 donantes compartidos entre regiones contando todos los grupos, pero no son automáticamente pares con cobertura y diseño utilizables. La puerta original de #37 para UNC13A no se redefine: un análisis STMN2 necesita protocolo propio. Exigir K≥20 a controles seleccionaría controles positivos; deben admitirse ceros con denominador total adecuado bajo una regla fijada antes del contraste.

## Limitaciones

- **Tejido bulk**; composición celular no medida y confusora.
- **Comparación original no emparejada.** La auditoría posterior recupera un mapa parcial de donante, con 128 compartidos entre regiones; no se ha recalculado un efecto emparejado. Hay un donante con dos muestras cervicales y 20 bibliotecas sin enlace exacto.
- **13 controles originales por tejido.** El mapa posterior enlaza 13 en corteza y 12 en cervical. La muestra control pequeña limita precisión; no se usa el solapamiento de intervalos para confirmar ni descartar diferencias.
- **37 de 95 muestras cervicales no son interpretables** por denominador insuficiente; se excluyen de las razones, no se imputan.
- **No se reclama novedad.** El truncamiento de STMN2 en ELA está ampliamente replicado y el consorcio ha trabajado estos datos.
- La cadena y la coordenada hg38 publicada respaldan el aceptor; no se resuelven sitios alternativos de poliadenilación. El extremo del intervalo exónico de conteo difiere una base del extremo terminal descrito por Melamed.
- Cuantificaciones de la tubería de recount3.
- **Metadatos de la medición original:** solo grupo. La auditoría posterior usa claves técnicas de muestra/donante, región, proyecto y preparación, y exporta únicamente agregados.
- Observación de splicing ≠ rescate ≠ función ≠ beneficio clínico. **Nada aquí respalda ninguna indicación clínica.**

## Siguiente prueba discriminante

Fijar un protocolo único STMN2 corteza/cervical del mismo donante: compatibilidad de preparación/lote, exclusiones, agregación de multiplicidades y elegibilidad por denominador total. Contar los pares utilizables antes de ajustar el contraste y detenerlo si el diseño queda confundido o escaso. El mapa parcial y los límites del ensayo están en la [auditoría](../stmn2-map-audit-20261111/REPORT.md). No se amplía a lumbar/torácica ni se repite la auditoría de UNC13A ya completada.

Sin contactos, gastos, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
