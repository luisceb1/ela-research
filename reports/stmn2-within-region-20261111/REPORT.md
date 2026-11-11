# Cierre del ciclo STMN2: asociación tisular exploratoria y composición aún no resuelta

[English](REPORT.en.md)


11/11/2026. Análisis final dentro de cada región, sin nuevos p-valores ni corrección del efecto tisular. [Protocolo](../../research/plans/2026-11-11-stmn2-within-region.md) fijado en `3a43db16981ab7dd5d0d887fb46099db74ee45d1` antes de calcular estas asociaciones. Los resultados anteriores ya eran conocidos; no es confirmación prospectiva externa.

## Evidencia del análisis final

Se conservaron los **45 donantes de ELA pura** con una biblioteca por región, preparación compatible, C+K≥20 en ambos tejidos, RIN válido y enlaces técnicos exactos. Corteza y cervical se analizaron **por separado**, sin mezclar sus referencias MuSiC.

- Indicador neuronal cortical: suma Excitatory+Inhibitory de la referencia GSE140231.
- Indicador neuronal cervical: Neurons de GSE190442.
- Resultado: cociente local de lecturas STMN2 K/(C+K), no proteína ni fracción de neuronas enfermas.
- Spearman: correlación de rangos medios, admitiendo empates. Correlación parcial: rangos de resultado e indicador residualizados por separado frente a intercepto, rangos de RIN, rangos de log1p(C+K) y preparación binaria; correlación de ambos residuos.

Las dos matrices de covariables pasaron los controles de tamaño, valores distintos, rango completo, condición numérica y variación residual. Son controles computacionales, no una garantía de potencia o identificación causal.

| Región | Donantes | Spearman | Correlación parcial de rangos | Rango al retirar un donante cada vez |
|---|---:|---:|---:|---|
| Corteza | 45 | −0,229 | **−0,299** | −0,364 a −0,247 |
| Cervical | 45 | −0,093 | **−0,105** | −0,185 a −0,054 |

Hubo 45/45 estimaciones válidas al retirar un donante en cada región; todas conservaron signo negativo. Es una comprobación de influencia individual, **no un intervalo de confianza ni replicación**. No se comparan formalmente los coeficientes entre regiones, que comparten donantes y usan referencias distintas.

En el subconjunto RIN prefijado (RIN≥6 ambos y diferencia≤1, **19 pares**) se calcularon solo asociaciones sin ajuste multivariable: Spearman −0,285 en corteza y −0,117 en cervical. No se ampliaron cortes o variables tras ver los resultados.

### Un límite material del indicador cervical

En médula, **22/45 estimaciones neuronales son exactamente cero** (10/19 en el subconjunto RIN); solo hay 24 valores neuronales distintos. En corteza no hay ceros neuronales y hay 45 valores distintos. Un cero de deconvolución no demuestra ausencia histológica de neuronas: es una estimación del método y referencia. Este amontonamiento de ceros limita el sondeo de composición cervical.

El resultado STMN2 también tiene empates: cociente cero en 29/45 bibliotecas corticales y 21/45 cervicales. La correlación cercana a cero en cervical **no descarta confusión por composición**, errores de estimación o relaciones no monotónicas. La relación inversa cortical tampoco identifica mecanismo: pérdida neuronal ligada a patología, mezcla de tipos celulares, calidad o expresión compartida entre indicador y resultado pueden contribuir.

## Balance integrado del ciclo

| Pregunta | Resultado que podemos sostener | Lo que no establece |
|---|---|---|
| ¿Se mide el evento STMN2 documentado? | Unión sellada respaldada por literatura hg38 y cadena genómica; cuatro muestras cervicales de ELA con K≥20 corresponden a cuatro donantes | Validación completa del ensayo, función o causa del límite de UNC13A |
| ¿Se cumple P1, ≥10× cobertura frente a UNC13A? | **No**: 6,6× bruto; 8,085× tras normalizar por lecturas de entrada | No se cambia el umbral para declarar éxito |
| ¿Hay diferencia descriptiva entre tejidos del mismo donante? | En 45 pares, cervical mayor/empate/menor: 24/14/7; mediana +0,368 puntos porcentuales | Independencia de composición, calidad o lote; descubrimiento externo |
| ¿Resiste una restricción de RIN? | En 19 pares principales: 10/8/1; mediana +0,255 puntos porcentuales | Robustez uniforme: el filtro más estricto deja nueve pares y mediana cero |
| ¿Queda descartada la composición? | **No**. Hay asociaciones inversas dentro de región y un indicador cervical con muchos ceros | Corrección del efecto tisular o dependencia causal por tipo neuronal |
| ¿P3 quedó confirmada inferencialmente? | No; sus frecuencias originales son descriptivas | Confirmación por solapamiento/no solapamiento de intervalos de Wilson |

La normalización de cobertura, las medianas de razones y sus poblaciones se mantienen separadas. No se alteran los conteos originales. La predicción P2 de obtener lecturas suficientes se cumple en esas muestras, pero no demuestra que el problema previo con UNC13A fuese exclusivamente del locus.

## Interpretación y parada

**Resultado final: patrón tisular exploratorio reproducible dentro de esta cohorte, parcialmente resistente a restricciones de calidad, sin resolución de la explicación por composición.** No se ha demostrado causa, rescate funcional, novedad biológica ni utilidad clínica. Los análisis de la misma cohorte, aunque usen tablas nuevas, no son replicaciones independientes.

Este ciclo queda **cerrado**. No se propone otra correlación, otro umbral RIN ni otro ajuste sobre estos 45 donantes. El siguiente avance requiere una entrada discriminante: estimaciones de composición con procedencia/calibración verificadas y, para validación externa, una cohorte independiente con cuentas del evento y diseño/QC trazables. La colección EGA ya identificada sigue condicionada a acceso y comprobación de independencia; no se contactó a nadie ni se descargaron datos controlados.

El PR #57 reúne protocolos, derivación, mapas, controles de calidad, resultados positivos/negativos y límites para revisión humana. La revisión sistemática de afirmaciones históricas propuesta por Claude es una tarea distinta: no se duplica aquí ni se declara terminada. Las puertas UNC13A #37 y K26 #44 no cambian.

## Reproducción y verificación

```sh
python scripts/stmn2_within_region.py --source-root /ruta/temporal/stmn2-audit-work --output /ruta/temporal/within.json
python -m unittest discover -s tests -p test_stmn2_within_region.py -v
```

Se usan fuentes ya fijadas, sin descargas adicionales ni columnas clínicas. La estructura temporal es la de los pasos previos; `results.json` conserva hashes de conteos, mapas, ST3/ST7 y versiones Python/NumPy. Se exportan solo agregados, no filas o gráficos identificables de donantes. El algoritmo es determinista, sin semilla necesaria.

Ocho tests nuevos verifican rangos empatados, constantes, mínimos, diseño singular, eliminación de confusión sintética, correlación residual conocida, ausencia de variación residual y fallo ante enlace/referencia ausente. Las pruebas sintéticas validan el cálculo, **no son datos biológicos ni evidencia de la hipótesis**. La CI del PR ejecuta compilación y suite offline completa con dependencias fijadas.
