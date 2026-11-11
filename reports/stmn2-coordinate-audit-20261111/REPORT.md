# Las coordenadas de STMN2 quedan confirmadas, y el exón críptico es terminal según los datos

**Fecha:** 2026-11-11. **Plan prefijado:** [`research/plans/2026-11-11-stmn2-coordinate-audit.md`](../../research/plans/2026-11-11-stmn2-coordinate-audit.md), commit `12b509e`, **anterior a mirar cuentas o consultar literatura**.
**Etiqueta de evidencia:** auditoría de coordenadas, superada. No modifica ninguna coordenada ni ninguna medición previa.

## Por qué se auditó

Las coordenadas de STMN2 se derivaron hoy y pasaron el cruce con ancla doble. Lo que **no** se había comprobado es si el evento medido es el **único** evento críptico del locus, o si hay otros que no estamos midiendo. La auditoría de UNC13A confirmó sus coordenadas pero no se hizo esa pregunta.

## Resultado de las cinco comprobaciones

| # | Comprobación | Resultado |
|---|---|---|
| **A1** | Mismas coordenadas en los dos tejidos | **PASA.** `79.611.215–79.616.821` idéntica en corteza (fila 2.389.629) y médula cervical (fila 2.415.963) |
| **A2** | El exón críptico es terminal: ninguna unión con donante en su extremo 3′ | **PASA de forma contundente.** En **313 muestras** de los dos tejidos **no existe ninguna** unión con donante en ≈79.617.049 |
| **A3** | Las cinco candidatas `annotated=0` rechazadas tienen soporte despreciable | **PASA.** 1–2 lecturas totales cada una en 149 muestras, frente a **215** (corteza) y **484** (cervical) de la sellada. En médula cervical ni aparecen |
| **A4** | ¿Hay otro evento críptico que no midamos? | **PASA por los datos.** Ver abajo |
| **A5** | Qué fuente de anotación marca la sellada como `annotated=1` (código `cH38`) | **NO RESUELTA.** Informativo, no bloqueante |

### A2: el supuesto del denominador queda validado empíricamente

El PSI de STMN2 se construyó sobre el supuesto de que el exón críptico es **terminal** (poliadenilación prematura), de modo que hay **una sola** unión críptica y no hace falta la corrección ×2 que sí requería UNC13A.

Si ese supuesto fuera falso existiría una unión saliendo del extremo 3′ del exón críptico. **No existe, en ninguna de las 313 muestras.** El denominador es correcto.

### A4: el evento sellado domina el locus por un factor de ~50

Todas las uniones del locus STMN2 en médula cervical, ordenadas por lecturas totales:

| Unión | Anotada | Lecturas | Muestras | Qué es |
|---|---|---:|---:|---|
| 79.641.551–79.654.870 | 1 | 21.372 | 161 | exón-exón canónico |
| 79.636.898–79.641.377 | 1 | 16.892 | 160 | exón-exón canónico |
| **79.611.215–79.636.801** | 1 | **15.004** | 158 | **canónica sellada** (exón 1→2) |
| 79.655.063–79.664.814 | 1 | 10.839 | 161 | exón-exón canónico |
| **79.611.215–79.616.821** | 1 | **484** | **72** | **críptica sellada** |
| 79.611.434–79.636.801 | 1 | 108 | 49 | donante alternativo menor |
| 79.611.792–79.636.801 | 1 | 89 | 46 | donante alternativo menor |

De las **50** uniones del locus, **34 no están anotadas y ninguna pasa de 9 lecturas**. La unión críptica sellada es, por un factor de unas 50 veces, el **evento no canónico dominante**.

Confirmación adicional no buscada: el aceptor críptico 79.616.821 lo usan **tres** donantes distintos — el canónico del exón 1 (484 lecturas), 79.613.938 (4) y 79.612.283 (3). Es un aceptor de splicing real, y el donante dominante es el canónico, como describe la literatura.

La búsqueda bibliográfica acotada (Europe PMC, título y resumen) **no encontró un segundo evento críptico documentado** de STMN2, pero esa es evidencia débil: un segundo evento podría estar descrito en métodos o material suplementario sin aparecer en título ni resumen. **La evidencia fuerte aquí es la de los datos.**

### A5: no resuelta, y no se adivina

La unión sellada aparece con `right_annotated = cH38` en recount3. **No dispongo de documentación de qué fuente de anotación designa ese código**, y no lo infiero. Queda registrado sin interpretar. No afecta a la aceptación: la derivación se sostiene sobre el cruce con ancla doble y sobre las comprobaciones empíricas de arriba.

## Consecuencia

**Las coordenadas no se han modificado. Ninguna medición de STMN2 queda afectada.** El PSI reportado está bien denominado, el evento medido es el dominante del locus, y las cinco candidatas que rechacé eran efectivamente ruido.

## Limitaciones

- A4 se resuelve **con estos datos y estos dos tejidos**. Un evento raro o específico de otro tejido no quedaría excluido.
- La búsqueda bibliográfica fue de título y resumen; no se leyeron métodos ni suplementos de las fuentes primarias.
- `cH38` sin resolver: no sabemos qué anotación incluye esta unión, de modo que no podemos decir *por qué* está marcada como anotada.
- Las cuentas son de la tubería de recount3; otra herramienta podría llamar uniones distintas.
- La auditoría valida coordenadas y dominancia, **no** biología: no dice nada sobre función, rescate ni beneficio clínico.

## Siguiente paso

Ninguno derivado de esta auditoría: cierra en verde, igual que la de UNC13A. Las dos dianas del proyecto tienen ahora coordenadas selladas y auditadas por el mismo procedimiento.

Sin contactos, gastos, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
