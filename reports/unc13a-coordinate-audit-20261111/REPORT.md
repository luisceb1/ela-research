# Las coordenadas selladas de UNC13A quedan confirmadas: 88 de 88 límites concuerdan

**Fecha:** 2026-11-11. **Plan prefijado:** [`research/plans/2026-11-11-unc13a-coordinate-audit.md`](../../research/plans/2026-11-11-unc13a-coordinate-audit.md), commit `1f854c3`, **anterior a consultar UCSC**.
**Etiqueta de evidencia:** auditoría de coordenadas, superada. No modifica ninguna coordenada ni ninguna medición previa.

## Por qué se auditó

El ciclo STMN2 demostró que mi criterio estructural de `annotated=0` podía **excluir el evento publicado**, y que solo el cruce con ancla doble lo resolvía. Las coordenadas selladas de UNC13A venían de una derivación anterior del proyecto que **nunca pasó ese cruce**. Si estaban mal, toda la medición de esta semana apuntaba a uniones equivocadas.

## Resultado: coincidencia exacta

Desplazamiento calculado sobre `NM_001080421.3`, pista `ncbiRefSeq` de UCSC, en ambos ensamblajes:

| Comprobación | Resultado |
|---|---|
| Límites exónicos comparados | **88** (44 exones × 2) |
| Desplazamientos distintos observados | **uno solo: 110.809** |
| Excepciones | **ninguna** |

El plan pedía **dos** anclas independientes concordantes. Se obtuvieron **88**, unánimes, lo que indica que esta región se transfirió entre ensamblajes sin cambio estructural.

Aplicado al intervalo publicado del exón críptico:

| | Valor |
|---|---|
| Publicado (hg19), DOI `10.1007/s00401-023-02655-0` | `chr19:17.753.223–17.753.350`, ancho 128 |
| Derivado a hg38 (− 110.809) | **`17.642.414–17.642.541`** |
| Implicado por las uniones selladas | **`17.642.414–17.642.541`** |
| **Coincidencia** | **EXACTA** |

El desplazamiento de 110.809 se anotó **en el plan, antes de consultar UCSC**, de modo que esto fue una predicción comprobada y no un ajuste a posteriori.

Verificación adicional de la canónica: el intrón sellado `17.641.557–17.642.844` empieza una base después de un fin de exón real en hg38 y termina en un inicio de exón real. Ambos extremos son límites anotados genuinos.

**Las coordenadas no se han modificado. No hacía falta.** Verificación registrada en [`research/references/unc13a_targets_sealed.json`](../../research/references/unc13a_targets_sealed.json).

## Consecuencia: ninguna medición de esta semana queda afectada

Los informes de recount3, la discrepancia de fracción, corteza motora y médula cervical medían las uniones correctas. El cierre de la puerta de cobertura para UNC13A se sostiene por la razón que ya se dio —la cobertura del locus— y no por un error de coordenadas.

## Lección metodológica que sí cambia algo

| Gen | Uniones crípticas en recount3 |
|---|---|
| UNC13A | `annotated=0` |
| STMN2 | `annotated=1` |

**El indicador `annotated` de recount3 es inconsistente entre genes y no es un criterio fiable en ninguna dirección.** Usarlo para *incluir* habría fallado en UNC13A; usarlo para *excluir* falló en STMN2. El criterio que sí funcionó en ambos casos fue el cruce con un intervalo publicado mediante ancla doble.

Queda anotado en el archivo sellado para que ningún ciclo futuro vuelva a apoyarse en ese indicador.

## Limitaciones

- La auditoría valida la **correspondencia entre ensamblajes y con el intervalo publicado**. No valida que el intervalo publicado sea biológicamente correcto, ni que las dos uniones sean las únicas del evento.
- Se usó un transcrito (`NM_001080421.3`), el de mayor número de exones común a ambos ensamblajes. Otras anotaciones podrían diferir en algún límite.
- `ncbiRefSeq` de UCSC es una anotación entre varias; GENCODE podría asignar límites ligeramente distintos en exones alternativos, aunque no en los implicados aquí.
- No se midió nada nuevo y no se reclama ningún hallazgo biológico.

## Siguiente paso

Ninguno derivado de esta auditoría: cierra en verde. Las continuaciones pendientes siguen siendo el contraste de STMN2 en médula cervical, que exige resolver unidades biológicas independientes, y las vías humanas.

Sin contactos, gastos, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
