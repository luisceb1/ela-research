# STMN2 emparejado: 45 donantes utilizables y mayor cociente cervical

[English](REPORT.en.md)


11/11/2026. **Evidencia exploratoria**, misma cohorte previamente inspeccionada; no replicación independiente. [Protocolo](../../research/plans/2026-11-11-paired-stmn2.md), commit `60b1246c44b0ff1f8e7cb7a6579a2a0ee0340fb0`, fijado antes de contar pares elegibles o calcular diferencias. Los resultados marginales previos ya eran conocidos y motivaron la pregunta.

## Evidencia

Se usaron únicamente los conteos existentes y las fuentes técnicas fijadas en la [auditoría](../stmn2-map-audit-20261111/REPORT.md). Se exigieron enlaces exactos concordantes en las dos rutas de metadatos, donante declarado, región y proyecto compatibles, una sola biblioteca por región y método de preparación conocido e idéntico. Los grupos proceden del JSON original. No se usaron nuevas columnas clínicas ni se exportaron filas de donantes.

La ruta conjunta tiene 104 donantes compartidos entre tejidos, subconjunto de los 128 enlazados por la fuente primaria. Entre esos 104, 29 no son ELA pura en ambas regiones, uno tiene preparación discordante y 29 no alcanzan C+K≥20 en ambos tejidos: quedan **45 pares**. Hay 25 pares Manual KAPA Total y 20 Automated KAPA Total. No hay multiplicidades entre estos 104; el duplicado cervical detectado anteriormente no aporta un par aceptado en este subconjunto. No se infiere su independencia por escoger una biblioteca de mejor cobertura.

Endpoint: diferencia dentro del donante, cervical menos corteza, del cociente local K/(C+K). C=unión canónica, K=entrada al exón críptico terminal 2a. Se incluyen ceros de K si el denominador es adecuado.

| Umbral C+K en ambos tejidos | Pares ELA | Cervical mayor | Empates | Cervical menor | Mediana de la diferencia |
|---|---:|---:|---:|---:|---:|
| ≥20, principal | 45 | 24 | 14 | 7 | +0,003676 (0,368 puntos porcentuales) |
| ≥50, sensibilidad descriptiva | 32 | 20 | 8 | 4 | +0,010665 (1,066 puntos porcentuales) |
| ≥100, sensibilidad descriptiva | 22 | 14 | 7 | 1 | +0,010007 (1,001 puntos porcentuales) |

La puerta prefijada (≥10 pares y ≥5 diferencias no nulas) pasa: 45 pares, 31 diferencias no nulas. El único contraste principal, prueba bilateral exacta de signos, da **p nominal=0,0033268929** (24 frente a 7). No se hicieron pruebas adicionales sobre las sensibilidades. La predicción direccional de mediana positiva se observa en este subconjunto; no se presenta como confirmación externa.

Los totales medianos de lecturas de unión son **845 en corteza y 89 en cervical** entre los 45 pares; las canónicas medianas son 844 y 80. El emparejamiento no iguala profundidad ni precisión. Las sensibilidades conservan la dirección, pero retienen subconjuntos distintos y no sustituyen un ajuste de sesgos del ensayo.

El control descriptivo deja **4 pares control** con umbral 20 (uno cervical mayor y tres empates, mediana cero). Con umbrales 50 y 100 quedan tres y dos pares. No se compara ELA frente a control ni se declara especificidad de enfermedad con esos tamaños.

## Interpretación

El patrón marginal previo no desaparece al usar donantes emparejados y preparación compatible: en este subconjunto, el cociente local de STMN2 es habitualmente mayor en médula cervical. El análisis reduce la confusión por diferencias entre personas y por el método de preparación registrado. La mediana del efecto local principal es pequeña y no representa porcentaje de neuronas afectadas ni cantidad de proteína funcional.

## Limitaciones y alternativas

- **No se conocen lotes de extracción o secuenciación**, RIN, carga pTDP-43 ni composición celular en este análisis. Igual método de preparación no significa mismo lote. No se ha demostrado ausencia de confusión técnica.
- Diferencias de cobertura, estabilidad del RNA, pérdida neuronal y proporción glial pueden afectar detección y cociente. El umbral C+K selecciona por una variable dependiente de expresión/calidad y puede inducir sesgo.
- La prueba exacta de signos supone probabilidad 1/2 para cada dirección bajo su nulo y donantes independientes. La diferente profundidad y los ceros discretos pueden afectar esa simetría aun sin diferencias en una fracción molecular latente. Su p es **nominal para las diferencias observadas**, no evidencia de que se hayan eliminado sesgos de medida o todos los factores de confusión.
- No hay una cohorte nueva: seleccionar esta pregunta tras ver la diferencia marginal limita cualquier interpretación confirmatoria. Las dos rutas de metadatos son de la misma cohorte.
- Las uniones no distinguen extremos alternativos de poliadenilación ni miden rescate molecular, función neuronal o beneficio clínico. No se ha probado dependencia por tipo neuronal.
- Los 45 pares no equivalen a 90 réplicas biológicas ni son los 128 pares potenciales del mapa más amplio. Los 20 enlaces faltantes de la auditoría no se completaron por inferencia.

## Siguiente prueba discriminante y parada

Este ciclo termina con el contraste único fijado. La pregunta siguiente es si el patrón se mantiene con **composición celular y calidad de RNA caracterizadas**, idealmente en una cohorte independiente emparejada. Antes de nuevos análisis, inspeccionar un manifiesto concreto que aporte esos campos y cobertura; no abrir una búsqueda masiva ni repetir filtros hasta obtener otro p-valor. Sin ese dato, el resultado permanece como asociación tisular exploratoria. No modifica las puertas UNC13A #37 ni funcional K26 #44, y no requiere reinterpretar esta señal como descubrimiento.

## Reproducción

```sh
python scripts/paired_stmn2.py --source-root /ruta/temporal/stmn2-audit-work --output /ruta/temporal/paired.json
python -m unittest discover -s tests -p test_paired_stmn2.py -v
```

La carpeta de fuentes contiene los archivos exactos de `reports/stmn2-map-audit-20261111/sources.json` y un subdirectorio `repo` con los JSON históricos en sus rutas originales. `results.json` registra SHA-256 de todos los insumos y versión Python. Seis pruebas nuevas verifican colas exactas, empates, ceros, multiplicidad antes del filtro, compatibilidad de preparación y ambas condiciones de parada. Se ejecutan también en la suite completa de CI. Exportación solo de agregados.
