# STMN2: unión validada y mapa parcial de donantes recuperado

Fecha: 11/11/2026. Base de los conteos: `ad96ec5e3e5ebb40a12324c0802a4979916f5c4d`.
Alcance fijado antes de los nuevos cruces en el commit `7f9b04c613fc7ad80032ff0bc25fa0377392a6af`, [plan](../../research/plans/2026-11-11-stmn2-map-audit.md).
Los conteos y las afirmaciones originales ya eran conocidos: esto es una auditoría retrospectiva de medida y diseño, no una validación prospectiva ni un descubrimiento biológico.

## Evidencia

### La sonda mide la entrada al exón terminal 2a documentado

Se mantienen sin cambios las uniones selladas, intrónicas 0-based half-open, hebra positiva, GRCh38:

| Evento | Intervalo sellado | Intrón 1-based inclusivo |
|---|---|---|
| Canónico exón 1→2 | chr8:[79611214,79636801) | 79611215–79636801 |
| Críptico exón 1→2a | chr8:[79611214,79616821) | 79611215–79616821 |

El aceptor inicia el exón críptico en **79616822 (1-based)**. Melamed 2019 proporciona directamente ese inicio en hg38. La cadena UCSC hg19→hg38 confirma de forma única los ocho nucleótidos comprobados alrededor de los límites canónico y críptico, sin extrapolar un desplazamiento entre bloques. Resultados base a base en `results.json`.

Los dos anclajes RefSeq anteriores eran concordantes, pero por sí solos no demostraban la alineación de la región intermedia. Esta comprobación con cadena y la coordenada publicada directamente en hg38 cierran esa limitación.

**Una precisión de un nucleótido:** Melamed describe el transcrito terminal de 227 nt en 79616822–79617048. El intervalo de conteo de 228 nt usado por Quadros, trasladado mediante cadena, acaba en 79617049. Ambos comparten el inicio; no se demuestra que sus extremos de conteo y de corte sean intercambiables. Esta diferencia no altera la unión que contamos.

### Qué puede omitir la medida

Cribado limitado a las cuatro familias fijadas, texto principal y métodos pertinentes; no es un inventario exhaustivo de suplementos o de todas las isoformas humanas.

| Fuente primaria y localizador | Evento o alternativa documentada | Consecuencia para nuestra sonda |
|---|---|---|
| [Klim 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7153761/), Fig.3f–g y apartado de exones crípticos | Unión desde exón 1 al exón críptico, sin salida observada a los exones posteriores | Compatible con una unión de entrada terminal |
| [Melamed 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6348009/), Fig.3c–e y párrafo de las 227 bases | Exón 2a terminal con poliadenilación prematura; no detectaron unión 2a→2. Se menciona otra anotación alternativa entre exones 4 y 5, no detectada en sus células | La sonda no cuenta todas las isoformas aguas abajo ni verifica el corte terminal |
| [Baughn 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10148063/), Fig.1H–I y apartado de disrupción del sitio críptico | Tras inactivar experimentalmente el PAS proximal persisten RNAs 1→2a poliadenilados; los autores proponen sitios distales, sin resolver aquí su uso individual | Un mismo aceptor puede terminar en sitios diferentes; la sonda los agrupa. No convertir los 61 motivos candidatos del trabajo en 61 isoformas observadas |
| [Quadros 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10766724/), cuantificación RNA-seq de STMN2 | Intervalo exónico usado para cuantificar RNA truncado | Un conteo exónico publicado no equivale directamente a nuestro conteo de unión |

No se identificó un segundo aceptor críptico validado que debamos añadir dentro del texto y métodos cribados. Esto no prueba su inexistencia. Las cinco candidatas regionales `annotated=0` no adquieren identidad biológica por su bandera de anotación. La sonda tampoco mide retención intrónica sin empalme, estabilidad, proteína ni reparación axonal. **K/(C+K) es un cociente local de lecturas de unión**, no una fracción molecular calibrada; no necesita dividir K entre dos para este evento terminal.

### Mapa técnico: 293/313 muestras, con 128 donantes compartidos

Ruta exacta: **(región de proyecto recount3, rail_id) → external_id → clave original de biblioteca → donante declarado + región + proyecto**. `rail_id` se reutiliza entre regiones: no es una clave global. El primer cruce sin acotar región detectó 245 colisiones aparentes; se corrigió el ámbito de la clave y se añadió un control específico antes de aceptar el resultado. Dentro de una región, las claves conflictivas se rechazan. Se preservan todos los sufijos, incluido `-2`; no se deducen personas a partir de prefijos.

Fuentes: metadatos de autor de Fratta (`cryptic_biology`, commit `80fa3d70418a4665a85d414e33c7c470a9312086`) y tabla S1 de la curación GEO de [Jung 2026](https://www.mdpi.com/1422-0067/27/18/8011), repositorio `chaeyunjung/pd-als-transcriptomics`, commit `8e57756b7b875e0e4b326ecb900ee43d14e49c9b`. Los proyectos aceptados son, respectivamente, `Target ALS` y `Target ALS PM core`. Son dos rutas de metadatos de la misma cohorte; su concordancia **no** constituye replicación biológica independiente.

| Comprobación | Corteza motora lateral | Médula cervical |
|---|---:|---:|
| Muestras en conteos originales | 149 | 164 |
| Enlace exacto en metadatos Fratta | 140 | 153 |
| Donantes distintos declarados en ese enlace | 140 | 152 |
| Muestras sin enlace aceptado | 9 | 11 |
| Enlace por curación GEO de Jung | 117 | 129 |
| Muestras comunes a ambas rutas / claves de donante coincidentes | 117/117 | 129/129 |
| Donantes con >1 muestra en esa región | 0 | 1 (dos muestras) |
| ELA pura: muestras enlazadas / originales | 81/84 | 92/95 |
| Controles: muestras enlazadas / originales | 13/13 | 12/13 |

Fratta proporciona **128 donantes en ambas regiones**, de 164 donantes distintos en la unión de las regiones enlazadas. La ruta Jung confirma 104 donantes compartidos, en su subconjunto. Los 128 incluyen todos los grupos originales, no solo ELA/control ni solo bibliotecas con cobertura suficiente. No son todavía el tamaño de un contraste elegible.

Las cuatro muestras cervicales de ELA pura con K≥20 enlazan a **cuatro donantes diferentes**. Las ocho con K≥20 entre todos los grupos enlazan a ocho donantes; no confundir esos dos totales. El duplicado cervical está en el grupo mixto y no debe convertirse en dos réplicas independientes. No se ha determinado si son réplicas técnicas o dos extracciones: se registra multiplicidad y se exige una regla antes de analizarlas.

Se contrastaron además cuatro fichas originales GEO, primera GSM por estrato región/preparación dentro de los enlaces exactos, sin selección por señal. **4/4** contienen la misma clave de muestra, donante y región. Recibos en `geo_spotcheck.json`; es una comprobación acotada, no una relectura exhaustiva de GEO. Las 20 muestras no enlazadas quedan excluidas del mapa aceptado, sin inferir claves.

### Correcciones al informe STMN2

Los conteos originales no se alteran. La mediana cervical ELA con C+K≥20 sigue siendo 0,005684; el error previo era de etiquetado y población del resumen, no un cambio numérico de esa mediana.

| Tejido / grupo | n total | n con C+K>0 | n con C+K≥20 | Mediana / máximo, C+K≥20 | Máximo entre todos los denominadores >0 |
|---|---:|---:|---:|---|---:|
| Corteza / ELA pura | 84 | 84 | 82 | 0 / 0,029106 | 0,029106 |
| Corteza / control | 13 | 13 | 12 | 0 / 0,008547 | 0,008547 |
| Cervical / ELA pura | 95 | 92 | 58 | 0,005684 / 0,543860 | 1 |
| Cervical / control | 13 | 13 | 8 | 0 / 0,001027 | 0,001027 |

**P1 no se cumple:** normalizando primero cada biblioteca por `star.number_of_input_reads_both`, las medianas canónicas son 0,929460 STMN2 y 0,114960 UNC13A por millón; cociente **8,085**, menor que 10. Sensibilidades con lecturas únicas mapeadas y lecturas asignadas a exones: 7,782 y 7,769. El cociente de medianas brutas, 33/5=6,6, tampoco cumplía el criterio. La predicción original no se cambia a posteriori.

**P2 se observa:** cuatro muestras de ELA pura con K≥20. Esto demuestra capacidad de obtener lecturas del evento en algunas bibliotecas; no valida por completo el ensayo ni localiza la causa de la escasa cobertura de UNC13A.

**P3 solo describe frecuencias de muestra:** 48/95 frente a 1/13 en cervical y 31/84 frente a 1/13 en corteza. No se confirma diferencia inferencial mediante solapamiento de intervalos de Wilson. Los tejidos comparten donantes y la cobertura/composición difiere; no se excluye confusión por esas vías. Se retiran las frases que descartaban una explicación por cobertura o asignaban causalidad al locus.

## Interpretación y límites

El bloqueo de identidad de unidad queda **parcialmente resuelto** para un subconjunto explícito, y existe una vía concreta de comparación emparejada. No se han recuperado datos de carga pTDP-43 ni un resultado funcional; #37 UNC13A y #44 K26 conservan sus condiciones originales. La independencia entre personas no sustituye información sobre selección de tejidos, extracción, lote, calidad y composición celular.

No se ajustó ningún efecto, p-valor o contraste de enfermedad. Exigir K≥20 a los controles seleccionaría artificialmente controles positivos; un diseño futuro debe fijar elegibilidad por información total o precisión de medida, admitir K=0 cuando C aporta información y no redefinir la puerta UNC13A existente para declarar un éxito STMN2.

Solo se usaron claves técnicas, región, proyecto y preparación. No se usaron columnas de edad, sexo, mutación, inicio o evolución. Se exportan agregados y hashes; no se incorporan tablas mixtas ni filas individuales con donante y enfermedad. No hubo contactos, gastos, descarga de RNA ni nuevo tejido. La respuesta de serie GEO superó el límite de lectura de 7 MB y se descartó; Klim/Baughn XML fallaron o agotaron tiempo y se consultó su texto primario en PMC. No se insistió con descargas grandes.

## Siguiente experimento

Redactar un único protocolo de **comparación STMN2 entre corteza y médula del mismo donante**, condicionado a verificar preparación/lote, elegibilidad C+K y número de pares utilizables. Fijar antes del contraste la agregación de multiplicidades, exclusiones, endpoint y manejo de profundidad; detenerlo si quedan pocos pares o el diseño no separa tejido y preparación. La selección de esa pregunta está informada por los resultados actuales y necesita replicación externa para sostener novedad. No abrir otra búsqueda de cohortes por inercia.

## Reproducción y validación

Python estándar, sin dependencias adicionales. Desde la raíz del repositorio, con los archivos de fuente exactos del manifiesto descargados en una carpeta temporal:

```sh
python scripts/audit_stmn2_units.py --source-root /ruta/temporal/fuentes --cortex reports/stmn2-derivation-20261111/results_corteza.json --cervical reports/stmn2-derivation-20261111/results_cervical.json --unc13a-cervical reports/target-als-cervical-20261111/results.json --output /ruta/temporal/recheck.json
python -m unittest discover -s tests -p test_audit_stmn2_units.py -v
```

`sources.json` fija URL, versiones y SHA-256; el resultado registra también los hashes de los conteos históricos. Los tests cubren sufijos, colisiones entre/dentro de regiones, conflictos, donante ausente, tejido erróneo, duplicados, agregación sin exportar claves, huecos/hebra de cadena y normalización antes de la mediana. La comprobación de GEO tiene recibos separados. La suite completa se comprueba mediante CI en el PR; la prueba local acotada no se presenta como ejecución local de toda la suite.
