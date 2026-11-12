# #37 reorientada: arbitrar la discrepancia de fracción críptica de UNC13A — plan prospectivo

Fecha: 2026-11-11. **Decisión de alcance de Luis el 11/11/2026: «reorienta #37 a resolver la discrepancia».** Base: main `b438ab9`, rama `claude/youthful-hypatia-v0ehce`.

**Este plan se fija ANTES de descargar o calcular nada de lo que describe.**

## Por qué #37 cambia de pregunta

#37 pedía una fuente con cuentas de uniones y cobertura ≥20 en una unión críptica de UNC13A. Tres candidatos examinados por la vía recount3 dejaron el bloqueo en otro sitio:

| Fuente | Ensayo | Fracción críptica en knockdown |
|---|---|---|
| SRP166282 (Klim 2019) | RNA-seq de transcriptoma completo | **0,000 – 0,145** |
| SRP334561 (Ma 2022) | amplicón dirigido | **0,390 – 0,690** |

Una fracción es **independiente de la profundidad**, de modo que la cobertura no explica una diferencia de 4–5×. Y el umbral de 20 solo es alcanzable según cuál sea la fracción real: con 0,10 haría falta ≈200 lecturas canónicas; con 0,50 bastarían ≈40.

Por tanto la pregunta previa ya no es «¿hay un dataset más profundo?» sino **«¿cuál es el nivel real de inclusión críptica, y por qué discrepan las dos mediciones?»**. El umbral de 20 **no se modifica**; se suspende su aplicación como criterio de aceptación de fuentes hasta que la discrepancia se arbitre.

## Pregunta

¿Cuánto de la discrepancia se explica por **eficacia del knockdown de TDP-43**, y qué explicaciones alternativas quedan en pie tras medirlo?

## Explicaciones candidatas y qué se puede comprobar con lo accesible

| # | Explicación | Comprobable aquí | Cómo |
|---|---|---|---|
| E1 | Eficacia del knockdown distinta | **Parcialmente** | TARDBP en `gene_sums` de Klim (knockdown vs control). Para Ma **no** por datos: su librería es amplicón y las cuentas génicas no representan el transcriptoma; se toma su eficacia **declarada en el artículo**, etiquetada como tal |
| E2 | Sesgo de detección por longitud de lectura y anclaje | **Parcialmente** | Longitud de lectura de ambos proyectos en `recount_qc`. El exón críptico mide 128/178 pb, de modo que un anclaje corto penalizaría las uniones crípticas frente a la canónica. Mecanismo plausible, **no demostrable** con estos archivos |
| E3 | Filtros de uniones o multimapeo de recount3 | **No** | Requeriría comparar `ALL` frente a `UNIQUE`, y **SRP166282 no tiene archivos UNIQUE**. Se registra como no comprobable |
| E4 | Sesgo de amplificación del ensayo de amplicón | **No** | Exigiría datos de control de amplificación que no se depositan |
| E5 | Línea o tipo celular | Débilmente | Ambos son motoneuronas derivadas de células madre; se documenta, no se cuantifica |

Se añade como contexto, **no como explicación de la fracción**: nivel de expresión de UNC13A en `gene_sums` de Klim. Explica cuentas absolutas bajas, **no** una diferencia de fracción. Se declara así para no confundir ambas cosas.

## Predicción refutable

Predicción: **la eficacia del knockdown de Klim será sustancialmente menor** que la declarada por Ma, y bastará para explicar parte de la diferencia de fracción, sin cerrarla por completo.

Refutación: si el knockdown de Klim resulta comparable al de Ma (reducción de TARDBP de magnitud similar), E1 queda descartada y **E2/E4 pasan a ser las explicaciones principales**, lo que se informará así en lugar de buscar otra variable que salve la predicción.

## Criterios de fracaso y parada

- Si `gene_sums` no permite identificar TARDBP sin ambigüedad, se informa y se para; no se sustituye por un gen proxy.
- Si la eficacia declarada por Ma no aparece en el texto accesible, se registra como no disponible; **no se estima**.
- No se calcula ningún PSI, efecto ni p-valor sobre la comparación entre proyectos: son ensayos y cohortes distintos.
- No se promedian las dos fracciones ni se elige una como «la verdadera» sin evidencia que lo sostenga.
- Un solo ciclo. Presupuesto de descarga: **≤50 MB**. No se descargan crudos, no se contacta a nadie, no se asumen costes.

## Entregables

`reports/unc13a-fraction-discrepancy-20261111/`: `REPORT.md` (Evidencia / Interpretación / Limitaciones / Siguiente), `results.json`, script con pruebas. Etiqueta de evidencia: **arbitraje parcial de una inconsistencia entre fuentes**. El resultado esperado es acotar explicaciones, no declarar una fracción verdadera.
