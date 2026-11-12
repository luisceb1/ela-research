# STMN2: coordenadas conservadas y observaciones regionales acotadas

**Revisión de integración:** [REVIEW](../integration-20261111/REVIEW.md). Los totales de la unión sellada se verificaron contra los JSON existentes; los demás inventarios se conservan como observaciones reportadas por Claude, sin nuevo replay de matrices. No detectar una unión no demuestra su inexistencia ni valida por sí solo un denominador.

**Fecha:** 2026-11-11. **Plan prefijado:** [`research/plans/2026-11-11-stmn2-coordinate-audit.md`](../../research/plans/2026-11-11-stmn2-coordinate-audit.md), versión recuperada en commit `8fcb33c` (referencia original `12b509e`), **anterior a mirar cuentas o consultar literatura**.
**Etiqueta de evidencia:** auditoría de coordenadas, superada. No modifica ninguna coordenada ni ninguna medición previa.

## Por qué se auditó

Las coordenadas de STMN2 se derivaron hoy y pasaron el cruce con ancla doble. Lo que **no** se había comprobado es si el evento medido es el **único** evento críptico del locus, o si hay otros que no estamos midiendo. La auditoría de UNC13A confirmó sus coordenadas pero no se hizo esa pregunta.

## Resultado de las cinco comprobaciones

| # | Comprobación | Resultado |
|---|---|---|
| **A1** | Mismas coordenadas en los dos tejidos | **PASA.** `79.611.215–79.616.821` idéntica en corteza (fila 2.389.629) y médula cervical (fila 2.415.963) |
| **A2** | El exón críptico es terminal: ninguna unión con donante en su extremo 3′ | **OBSERVACIÓN COMPATIBLE, no demostración de terminalidad.** Claude reporta ninguna unión detectada desde el extremo examinado en estas 313 bibliotecas |
| **A3** | Las cinco candidatas `annotated=0` rechazadas tienen soporte despreciable | **PASA.** 1–2 lecturas totales cada una en 149 muestras, frente a **215** (corteza) y **484** (cervical) de la sellada. En médula cervical ni aparecen |
| **A4** | ¿Hay otro evento críptico que no midamos? | **PARCIAL.** Inventario observado y búsqueda acotada; no excluye eventos raros/no anotados de otra clase |
| **A5** | Qué fuente de anotación marca la sellada como `annotated=1` (código `cH38`) | **NO RESUELTA.** Informativo, no bloqueante |

### A2: ausencia observada de salida, no prueba de inexistencia

Claude reporta que no se detectó una unión con donante en el extremo 3′ examinado. Es compatible con un exón terminal, pero la sensibilidad, los filtros y el punto exacto explorado limitan esa observación. Tampoco excluye otros extremos de poliadenilación que comparten la misma unión de entrada. La interpretación terminal se apoya en la literatura primaria y la concordancia genómica documentadas en la [auditoría de #57](../stmn2-map-audit-20261111/REPORT.md), no en invertir la ausencia de detección en una demostración universal. K/(C+K) es un cociente local de lecturas, no una fracción molecular calibrada.

### A4: soporte sellado frente al subconjunto no anotado

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

De las **50** uniones del locus, **34 no están anotadas y ninguna pasa de 9 lecturas**. El cociente 484/9≈54 compara la sellada con el máximo de ese **subconjunto no anotado**. No demuestra que sea el mayor de todos los eventos no canónicos: la bandera de anotación no define identidad biológica y la propia tabla incluye donantes alternativos anotados con 108 y 89 lecturas.

Confirmación adicional no buscada: el aceptor críptico 79.616.821 lo usan **tres sitios donantes de empalme** distintos (no tres personas) — el canónico del exón 1 (484 lecturas), 79.613.938 (4) y 79.612.283 (3). Es un aceptor de splicing real, y el donante dominante es el canónico, como describe la literatura.

La búsqueda bibliográfica acotada (Europe PMC, título y resumen) **no encontró un segundo evento críptico documentado** de STMN2, pero esa es evidencia débil: un segundo evento podría estar descrito en métodos o material suplementario sin aparecer en título ni resumen. El inventario acota lo observado; no establece completitud del repertorio críptico.

### A5: no resuelta, y no se adivina

La unión sellada aparece con `right_annotated = cH38` en recount3. **No dispongo de documentación de qué fuente de anotación designa ese código**, y no lo infiero. Queda registrado sin interpretar. No afecta a la aceptación: la derivación se sostiene sobre el cruce con ancla doble y sobre las comprobaciones empíricas de arriba.

## Consecuencia

**Las coordenadas no se han modificado. Ninguna medición de STMN2 queda afectada.** Se conserva la medida de unión local sellada, con los límites de cobertura y anotación expuestos; poco soporte de las otras candidatas no prueba que sean ruido ni que no existan otros eventos.

## Limitaciones

- A4 queda parcial: un evento raro, filtrado o de otro tejido no queda excluido.
- La búsqueda bibliográfica fue de título y resumen; no se leyeron métodos ni suplementos de las fuentes primarias.
- `cH38` sin resolver: no sabemos qué anotación incluye esta unión, de modo que no podemos decir *por qué* está marcada como anotada.
- Las cuentas son de la tubería de recount3; otra herramienta podría llamar uniones distintas.
- La auditoría respalda coordenadas y describe soporte observado, **no** biología: no dice nada sobre función, rescate ni beneficio clínico.

## Siguiente paso

Ninguno derivado de esta auditoría: cierra en verde, igual que la de UNC13A. Las dos dianas del proyecto tienen ahora coordenadas selladas y auditadas por el mismo procedimiento.

Sin contactos, gastos, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
