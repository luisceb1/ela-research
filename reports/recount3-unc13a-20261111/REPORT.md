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

## Limitaciones

- **Rechazo por cobertura**, igual que el piloto cerrado. La diferencia es que ahora la causa está aislada: profundidad en el locus, no acceso.
- **Una sola línea celular**: sin independencia genética.
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
