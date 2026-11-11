# Auditoría de predicciones prefijadas frente a su veredicto declarado — plan

Fecha: 2026-11-11. Autorización de Luis; tarea asignada a este agente mientras la rama de la PR #57 ejecuta el análisis de composición. **No se repite la auditoría de esa rama.**

## Por qué

En el ciclo STMN2 declaré **CONFIRMADA** una predicción (P1, umbral ≥10×) cuyo resultado fue 6,6×. Lo detectó un segundo lector, no yo. Queda por saber **si es un caso aislado o un patrón** en mis informes de esta sesión.

**Sesgo declarado:** audito mi propio trabajo. Por eso el procedimiento es **mecánico** donde puede serlo: extraer el umbral del plan, extraer el valor y el veredicto del informe, y comprobar la aritmética, en vez de releer mi propia prosa y juzgarla.

## Alcance

Los **8 planes** con predicciones prefijadas de esta sesión (10–11/11) y sus informes correspondientes. No se auditan ciclos anteriores al 10/11 ni el trabajo de otras ramas.

## Criterio de fallo, fijado ahora

Para cada predicción con **umbral numérico explícito**:

- **FALLO** si el veredicto declarado es «confirmada» y el valor reportado **no** satisface el umbral, o si es «refutada» y sí lo satisface.
- **CORRECTO** si veredicto y aritmética concuerdan.
- **NO NUMÉRICA** si la predicción es cualitativa; se revisa a mano y se marca como tal, sin pretender rigor mecánico.
- **NO COMPROBABLE** si el informe declara que la predicción no pudo ponerse a prueba; se verifica que esa declaración sea coherente, no que el resultado sea uno u otro.

Cada fallo encontrado se corrige en su informe **con la corrección visible**, no en silencio, y se registra aquí.

## Lo que esta auditoría NO hace

No revisa si los análisis eran correctos, ni si las conclusiones se sostienen. **Solo comprueba la coherencia entre umbral prefijado y veredicto declarado.** Un veredicto coherente puede seguir apoyándose en un análisis equivocado.

## Entregable

`reports/prediction-audit-20261111/REPORT.md` con una tabla: plan, predicción, umbral, valor reportado, veredicto declarado, veredicto correcto, resultado de la comprobación. Y las correcciones aplicadas, si hay.
