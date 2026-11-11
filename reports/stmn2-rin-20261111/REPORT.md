# STMN2 y calidad de RNA: patrón positivo en 19 pares, límite en el filtro más estricto

11/11/2026. **Sensibilidad exploratoria en la misma cohorte**, sin replicación independiente ni nuevos p-valores. [Protocolo](../../research/plans/2026-11-11-paired-stmn2-rin.md) fijado en `c444b5443b671f0aa8436109eb05a600f1fb0b86` antes de cruzar calidad con las diferencias de STMN2. El resultado original y la disponibilidad general del RIN ya eran conocidos.

## Evidencia

Se reprodujeron los **45 pares originales** usando exactamente las reglas anteriores: ELA pura en ambos tejidos, una biblioteca por donante/región, preparación compatible y C+K≥20 en ambos. Las 90 bibliotecas enlazan con ST3 NYGC mediante clave RNA exacta y única; **los 45 pares concuerdan en donante, región y preparación y tienen RIN válido**. No hubo recodificación difusa ni exclusión por discrepancias de identidad. El libro mixto permanece temporal, sin incorporar filas de donantes al repositorio.

La regla principal fue **RIN≥6 en ambos tejidos y diferencia absoluta entre RIN≤1**. La secundaria descriptiva elevó el mínimo a 7. Son reglas operativas fijadas para esta sensibilidad, no umbrales universales validados del ensayo. No se buscaron más cortes ni se relajó el mínimo de diez pares para interpretar la predicción.

| Conjunto | Pares | Cervical mayor | Empates | Cervical menor | Mediana cervical−corteza |
|---|---:|---:|---:|---:|---:|
| Original, sin filtro RIN | 45 | 24 | 14 | 7 | +0,003676 (0,368 puntos porcentuales) |
| RIN≥6 ambos y diferencia≤1, principal | **19** | **10** | **8** | **1** | **+0,002551 (0,255 puntos porcentuales)** |
| RIN≥7 ambos y diferencia≤1, secundaria | **9** | **4** | **4** | **1** | **0** |

El filtro principal conserva la dirección positiva con 19 pares; el más estricto deja nueve, por debajo de la puerta fijada, y su mediana observada es cero. **No respalda afirmar robustez uniforme frente a calidad del RNA.** Tampoco demuestra que mejorar el RIN elimine el efecto: son subconjuntos pequeños y diferentes, no una intervención sobre la calidad.

En los 19 pares principales, los RIN medianos son 6,9 en corteza y 7,2 en cervical, con diferencia absoluta mediana 0,5. Los denominadores medianos C+K siguen siendo muy distintos: **1150 frente a 120**. En los nueve pares estrictos son 921 frente a 53. RIN comparable no iguala profundidad ni elimina sesgo discreto de detección.

### Exclusiones y selección

El filtro principal excluye 26 pares compatibles. Su dirección es 14 cervical mayor / 6 empates / 6 cervical menor, con diferencia mediana +0,011059. El filtro estricto excluye 36 pares, con 20/10/6 y mediana +0,010007. Los motivos no exclusivos (RIN bajo en al menos un tejido y diferencia RIN>1) se cuantifican en `results.json`; un par puede incumplir ambas reglas. Los excluidos no se imputan ni se añaden al conjunto seleccionado.

Los resultados originales no se alteran ni se sustituyen por la sensibilidad más favorable. No se ejecutó regresión ajustada, prueba adicional de significación, comparación con controles o cambio de endpoint. K=0 sigue admitido si el denominador es suficiente.

## Interpretación y limitaciones

La diferencia cervical/corteza **no desaparece descriptivamente** con la restricción principal de calidad; esto aporta un control concreto sobre una explicación alternativa. Su magnitud mediana es menor que en los 45 pares originales, pero comparar esas medianas entre subconjuntos no cuantifica un efecto causal del RIN.

La sensibilidad estricta aporta una limitación material: mediana cero y solo nueve pares. La afirmación adecuada es persistencia descriptiva bajo el filtro principal, con resultado inconcluso en el estricto, no una asociación completamente ajustada por calidad. Los umbrales se fijaron tras conocer el patrón marginal, por lo que tampoco son una confirmación prospectiva externa.

Persisten composición celular no medida, lote real de extracción/secuenciación desconocido, selección por cobertura/RIN, estabilidad del RNA y profundidad desigual. El RIN de tejido completo puede no reflejar igual la integridad de cada transcrito o célula. Ni este control ni el anterior establecen dependencia por tipo neuronal, carga de TDP-43, función o rescate. Las puertas UNC13A #37 y K26 #44 no cambian.

## Siguiente prueba discriminante

La tarea RIN queda terminada. La siguiente entrada concreta es la **tabla ST7 NYGC de estimaciones de composición celular**, ya localizada. Antes de usarla, fijar un protocolo de inspección/extracción y confirmar granularidad por biblioteca, claves exactas y método de estimación. Si es solo agregada o no enlaza con nuestros pares, no puede ajustar esta comparación. Si sirve, fijar después un único modelo/sensibilidad apropiado antes de calcular su efecto. No añadir cortes de RIN hasta obtener otra conclusión ni tratar los mismos donantes como replicación independiente.

## Reproducción y verificación

```sh
python scripts/stmn2_rin_sensitivity.py --source-root /ruta/temporal/stmn2-audit-work --output /ruta/temporal/rin.json
python -m unittest discover -s tests -p test_stmn2_rin_sensitivity.py -v
```

Fuente ST3: libro `NYGC_Flagship_ST_1_3_Metadata.xlsx`, [Zenodo 20090702](https://zenodo.org/records/20090702), SHA-256 `c1bf21493c4a2773e27ff787e60267fc2e1304ce11e84e644c03c700cc68f048`. El script exige ese hash y localiza ST3 por nombre y relaciones del libro. La carpeta de fuentes y conteos conserva la disposición del análisis anterior; no se usan otras hojas clínicas.

`results.json` registra hashes de todos los insumos y solo agregados. Cinco tests nuevos verifican límites inclusivos, RIN ausente/no finito/fuera de rango, donante/región/preparación incorrectos, claves duplicadas, ceros crípticos, guardia de 45 pares y mínimo de diez para interpretar dirección. Sin aleatoriedad ni descargas nuevas. La CI del PR ejecuta compilación y suite offline completa.
