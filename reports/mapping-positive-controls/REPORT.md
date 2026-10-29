# Issue19: corrección existente reconciliada y controles de regresión efectivos

29/10/2026. Auditoría técnica sobre datos públicos procesados. No nueva cohorte, inferencia diferencial, réplica biológica ni validación funcional.

## Hallazgo de continuidad

El run40868865843 (commitd42fdac375ba71f5aaf01a952bc73b9796118bce) se marcó success con0transcritos STMN2/UNC13A porque seleccionaba por gene_name. En los GTF utilizados ese atributo falta para todos los TXNAME presentes en las matrices. El vínculo TXNAME/GTF sí existía; cero seleccionados no demostraba ausencia biológica.

La corrección **ya estaba en main** (snapshot13ccbc5c9f1c9744c57ed9abb822d169772e32a5): seleccionaba también por ENSG. Los logs del run posterior40870066862 confirman11objetivos en cultivo y10en cerebro, con hashes de las cuatro entradas idénticos a los de nuestras ramas. Por tanto, no corresponde volver a presentar la resolución por ENSG como arreglo nuevo ni afirmar que main todavía produce cero.

Sí quedaban dos defectos: el test sin gene_name estaba fuera de la clase de unittest, tras el bloque de ejecución, y contenía separadores literales; nunca lo descubría la suite. Además, el CLI solo rechazaba cero TXNAME coincidentes, permitiendo éxito con cero genes objetivo. La resolución por símbolo aún podía sobreponerse a IDs discordantes.

## Cambios de este PR directo a main

- Selección exclusivamente por panel ENSG versionado y contrastado con GENCODEv47/GRCh38, con hash del archivo original. gene_name es opcional; si existe, una contradicción con el ID se registra como conflicto y no se usa para reasignar un gen.
- Prueba sin gene_name colocada dentro de la clase y con tabuladores reales. Tests positivos/negativos para versiones de ID, símbolos discordantes, ausencia de cada control solicitado, objetivos desconocidos, duplicados, cuentas vacías/no finitas/negativas e identidad GTF conflictiva.
- Un guard de aceptación exige coincidencia de todos los TXNAME, ausencia de conflictos y al menos un modelo de cada gen solicitado. Ante fallo, el CLI termina con estado no cero y no publica un nuevo TSV parcial: el archivo temporal se renombra solo tras superar los controles.
- Los workflows existentes vigilan también cambios en el panel de referencia. No se añade un servicio de cómputo ni se fusiona la cadena de PR pendientes.

Estos requisitos son controles técnicos del panel de este proyecto. Fallar uno significa salida insuficiente para interpretar, no ausencia del gen ni un diagnóstico.

## Reproducción ejecutada

Se verificaron primero los cuatro SHA256 GEO y el SHA256 GENCODEv47. Los dos IDs, símbolos, cromosomas y hebras se contrastaron de nuevo con filas gene del GTF de referencia. Se analizaron las dos series con un índice GTF validado compartido entre las funciones de selección histórica, main anterior al endurecimiento y versión propuesta; la comparación de baselines se limita a esas funciones de selección, no reejecuta por completo los workflows antiguos.

| Serie | Filas/transcritos enlazados | gene_name ausente | Selección histórica | Selección main y propuesta | STMN2 / UNC13A |
|---|---:|---:|---:|---:|---|
| GSE310723 |392871/392871|392871|0|11|4/7|
| GSE315972 |401720/401720|401720|0|10|3/7|

Cero conflictos de ID y cero contradicciones de símbolo en ambas series. Los TSV propuestos son **idénticos por bytes** a los de la selección de main con estas entradas. Además coinciden IDs, símbolos, número de exones y sumas de cuentas con `reports/isoforms/transcripts.tsv` de las ramas previas (PR#4y siguientes). Así se explica la divergencia de estados: eran rutas y puntos de continuación distintos, no resultados biológicos incompatibles.

La reproducción se ejecutó dos veces con los mismos resultados estructurados. Suite de este snapshot de main:16tests(12de mapeo y4generales) pasan; es distinta de las85pruebas de la ramaMEA. No sumar ambas cifras como si fueran una sola suite ni asumir que todos sus cambios ya están en main.

## Diccionario y límites de salida

Los TSV contienen una fila por transcrito y **suma de cuentas a través de columnas**, sin exportar nombres/filas por donante. `gene_name` en la salida es el símbolo resuelto por panel, no un atributo observado en estos GTF. `counts_sum` conserva la escala depositada: no representa moléculas independientes verificadas ni compara grupos o series. Cero expresión de un modelo y cero modelos seleccionados no son la misma medida.

`reproduction.json` conserva fuentes, controles por serie, comparación de baselines y coincidencia con el mapeo de ramas anteriores. `remote_evidence.json` conserva solo hashes/sumarios y localizadores de logs, sin secretos ni volcado completo del runner. `run.json` y `errors.json` registran versiones, repetición e incidencias. Referencias pequeñas fijadas en research/references; originales fuera de git.

## Cómo repetir

`python scripts/reproduce_mapping_controls.py --cache RUTA_A_CACHE_PUBLICA` verifica las fuentes fijadas y produce los TSV y controles actuales. La caché debe contener los cuatro archivos GEO y `gencode.v47.annotation.gtf.gz`; no se descargan automáticamente ni se reconstruyen de memoria si faltan.

Para comparación histórica, recuperar del propio historial Git las versiones de `scripts/map_isoseq_gtf.py` en commitsd42fdac375ba71f5aaf01a952bc73b9796118bce y13ccbc5c9f1c9744c57ed9abb822d169772e32a5, leerlas y pasar sus rutas mediante `--baseline-historical`/`--baseline-current`. `--prior-transcripts` acepta la tabla del PR#4; esas ramas no se fusionan aquí. Los hashes de los scripts y de la tabla usados quedan registrados. Cambiar los argumentos cambia el alcance del resultado; la ausencia de baseline no se presenta como comparación realizada.

## Próxima tarea y estado de issues

La selección cero de#19 ya se había resuelto; este PR deja controles que realmente se ejecutan, referencia y evidencia reproducida. Issue#19 permanece abierta para revisión humana. #1/#2 y la cadena#3–#13/#22 tampoco se cierran ni fusionan automáticamente.

Siguiente prioridad segura: issue#20, reconstruir los filtros que distinguen21frente a1910uniones y cotejar el ZIP original antes de interpretar candidatos. Main ya corrigió la clasificación publicada ALS-CI a3/3/2en su otro flujo; no volver a usar solo etiquetas de columna como clasificación clínica. El paquete completo de21uniones no figura entre los11archivos adjuntos inventariados en este chat; localizar la copia persistente por nombre/hash o declarar el bloqueo. Los resultados de distintos filtros no se suman ni equivalen a replicaciones.
