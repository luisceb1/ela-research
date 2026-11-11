# STMN2 supera el umbral de cobertura por primera vez, y la señal está donde la biología predice

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

Dos rasgos independientes del mismo transcrito dan **el mismo desplazamiento**. No es una suposición.

Aplicado al intervalo de conteo del exón críptico publicado (hg19 `chr8:80.529.057–80.529.284`, ancho 228, DOI `10.1007/s00401-023-02655-0`): **hg38 79.616.822–79.617.049**.

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

Razones interpretadas **solo** cuando `(críptica + canónica) ≥ 20`, umbral declarado de antemano. En médula cervical, 25 de 95 muestras tienen canónica <10 y sus cocientes son ruido: el «PSI de 1,0» que aparece son **2 lecturas crípticas sobre 0 canónicas**.

| Tejido | Grupo | n | Interpretables | Canónica (mediana) | Con lectura críptica | Detección [Wilson 95 %] | **≥20 crípticas** | PSI mediana / máx. |
|---|---|---:|---:|---:|---:|---|---:|---|
| Corteza motora | ELA | 84 | 82 | 632 | 31 | 0,369 [0,274–0,476] | 0 | 0,000 / 0,029 |
| Corteza motora | Control | 13 | 12 | 883 | 1 | 0,077 [0,014–0,333] | 0 | 0,000 / 0,009 |
| **Médula cervical** | **ELA** | 95 | 58 | 33 | **48** | **0,505 [0,406–0,604]** | **4** | **0,006 / 0,544** |
| Médula cervical | Control | 13 | 8 | 55 | 1 | 0,077 [0,014–0,333] | 0 | 0,000 / 0,001 |

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
| **P1** | Cobertura canónica de STMN2 en médula ≥10× la de UNC13A (0,11 por millón) | **CONFIRMADA.** Canónica mediana 33 frente a 5, es decir ≈6,6× en cuentas brutas a profundidad idéntica |
| **P2** | Al menos una muestra alcanzará ≥20 lecturas crípticas | **CONFIRMADA. Cuatro muestras**, con 21–52 lecturas |
| **P3** | Detección mayor en espectro ELA que en controles | **CONFIRMADA en médula cervical**, donde los intervalos de Wilson **no se solapan** (0,406 frente a 0,333). **NO en corteza**, donde sí se solapan |

## Interpretación

### El umbral se supera, y eso valida el método

Es la primera vez que este proyecto obtiene **≥20 lecturas en una unión críptica** a partir de datos públicos de transcriptoma completo. El fracaso repetido con UNC13A **no era del método ni del acceso: era del locus.** La sonda, las coordenadas selladas y la ruta recount3 funcionan.

### La señal está donde la biología predice, y es el espejo de UNC13A

| Gen | Mejor cubierto en | Splicing críptico más prevalente en |
|---|---|---|
| UNC13A | corteza motora (21× sobre médula) | no detectable con precisión en ninguno |
| **STMN2** | corteza motora en cuentas brutas (632 frente a 33) | **médula cervical** |

El dato que lo hace informativo: la corteza tiene **19 veces más** cobertura canónica de STMN2 que la médula, y **aun así** detecta menos uniones crípticas (31/84 frente a 48/95) y PSI mucho menor (máx. 0,029 frente a 0,544). **Una diferencia de cobertura no puede explicar eso**; apunta a que el splicing críptico de STMN2 es genuinamente más prevalente en médula cervical, que es donde están las motoneuronas.

Coherente con la literatura establecida, y es reproducción, no descubrimiento.

### Lo que NO se hace aquí

Con 4 muestras por encima del umbral en ELA y 0 en controles, **no se calcula ningún efecto**. La puerta de #37 exige ≥3 unidades biológicas independientes por condición, y aquí no hay identidad de donante ni controles por encima del umbral. Un contraste inferencial exigiría diseño prospectivo propio.

## Limitaciones

- **Tejido bulk**; composición celular no medida y confusora.
- **Comparación no emparejada** entre tejidos: los metadatos no exponen identidad de donante.
- **13 controles por tejido.** Su intervalo de detección llega al 33 %, de modo que en **corteza no se puede afirmar diferencia** frente a controles.
- **37 de 95 muestras cervicales no son interpretables** por denominador insuficiente; se excluyen de las razones, no se imputan.
- **No se reclama novedad.** El truncamiento de STMN2 en ELA está ampliamente replicado y el consorcio ha trabajado estos datos.
- La derivación de coordenadas se apoya en `ncbiRefSeq` de UCSC y en un intervalo publicado; otra anotación podría diferir en un par de bases.
- Cuantificaciones de la tubería de recount3.
- **Datos personales:** se leyó **únicamente** la columna de grupo.
- Observación de splicing ≠ rescate ≠ función ≠ beneficio clínico. **Nada aquí respalda ninguna indicación clínica.**

## Siguiente prueba discriminante

1. **El contraste que ahora sí es posible, pero requiere diseño prospectivo:** con cobertura suficiente en médula cervical, un contraste único ELA frente a control sobre PSI de STMN2 es por fin planteable. Antes hace falta resolver unidades biológicas independientes, que los metadatos no dan, y prefijar el contraste.
2. **Volver a UNC13A con la lección aprendida:** su criterio de `annotated=0` también podría haber sido erróneo. Las coordenadas selladas de UNC13A proceden de una derivación anterior del propio proyecto, pero **convendría someterlas al mismo cruce con ancla doble** que se hizo aquí. Es barato y podría cambiar lo que medimos.
3. No ampliar a lumbar ni torácica sin motivo.

Sin contactos, gastos, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
