# CAMK2B: resultado previo reproducido técnicamente

29/10/2026. Reproducción técnica de una comparación con los mismos archivos públicos procesados; **no replicación biológica independiente**, identificación de péptido ni prueba de ausencia de un evento en personas.

## Pregunta y resultado

El paquete `ELA_06_CAMK2B_validacion_independiente_2026-10-29(1).zip` del otro chat declara que la unión de BambuTx9181, chr7 hebra− con límites exónicos44220901/44222117 (GRCh38), no está en los modelos CAMK2B de GSE315972. Se ha leído el código recibido sin ejecutarlo y se ha repetido la comparación con código del repositorio, usando únicamente GTF y uniqueCounts públicos ya cacheados y verificados en la auditoría GEO.

| Medida | GSE310723 | GSE315972 |
|---|---:|---:|
| Modelos CAMK2B |50|49|
| Modelos ENST |49|49|
| Modelos con unión objetivo exacta |1|0|
| Suma uniqueCounts de modelos con esa unión |32|No hay modelo cuantificable|
| Bibliotecas con suma CAMK2B positiva |4/4|8/8|

Los cuatro resultados previstos (1modelo celular, suma32, 49modelos cerebrales y0coincidencias cerebrales) coinciden. El cero de suma que aparece en JSON para el conjunto cerebral vacío es una **suma sobre cero modelos**, no una medición de cero lecturas de la unión ni una prueba de ausencia.

CAMK2B presenta señal génica agregada en las ocho bibliotecas cerebrales, de modo que la ausencia del modelo no procede de una ausencia total de cuantificación del gen. No comparar estas sumas entre series como expresión diferencial; no normalizamos ni estimamos un efecto biológico.

## Controles y calidad

- Coincidencia exige gen, cromosoma, hebra y ambos límites exónicos. En hebra negativa se conservan coordenadas en orden genómico; no confundir límites exónicos1-based con extremos intrónicos o BED0-based.
- Otras3uniones del mismo modelo CAMK2B sí aparecen entre modelos cerebrales. Esto controla que la comparación no retorna vacío para toda la cadena, sin demostrar sensibilidad de detección de la unión objetivo.
- La unión STMN2 de BambuTx9249 tampoco está en el catálogo cerebral, concordante con el mapeo previo. No se presenta como réplica nueva.
- De16uniones del candidato celular HDGFL2,14aparecen en algún modelo cerebral y2no. Que haya coincidencias parciales no establece la misma isoforma completa ni especificidad de ELA. No sumamos señales a través de uniones, pues repetiríamos transcritos.
- Cuatro hashes de fuentes cotejados con reports/geo-audit/sources.json y con el archivo de verificación del paquete anterior. Concordancia catálogo/cuentas para los3genes, exones no solapados, IDs únicos, valores finitos/no negativos y columnas válidas. No se repite la auditoría de todos los genes: esa comprobación global está en PR#3.
- No se exportaron filas por biblioteca/donante, información clínica ni lecturas alélicas. Las matrices originales no se incorporaron a git.

## Interpretación y límites

La evidencia se refiere a **estructuras de transcritos reconstruidos y cuentas asignadas a transcritos**. No observamos alineamientos que atraviesan la unión ni su cobertura regional. Una reconstrucción ausente puede reflejar baja abundancia, sensibilidad del algoritmo o composición celular. No usar la ausencia para descartar presencia en otro tejido o población neuronal.

32son unidades depositadas de uniqueCounts, no moléculas independientes verificadas. Se conserva la escala original: sigue pendiente la causa de cuentas pares documentada en PR#5/#6. Las cuatro condiciones celulares no son cuatro réplicas independientes por tratamiento, y cultivo y cerebro no son cohortes intercambiables. No calculamos significación ni inferimos toxicidad, traducción o beneficio terapéutico.

El título del paquete antiguo incluye «validación independiente», pero esta ejecución **reproduce sus cálculos sobre los mismos datos**, y el resultado cerebral es negativo a nivel de catálogo. Se actualiza la matriz de continuidad con ese alcance. La novedad bibliográfica de CAMK2B no se reaudita en este ciclo ni se reivindica como hallazgo propio.

## Reproducción y decisión

Plan previo: research/plans/2026-10-29-camk2b-reproduction.md. Ejecutar `python scripts/reproduce_camk2b.py`; escribe audit.json agregado. Emplea el lector GTF existente, ampliado para aceptar una lista explícita de genes sin cambiar su comportamiento por defecto. Dos ejecuciones producen bytes idénticos. Cinco pruebas nuevas controlan cromosoma/hebra/gen, orden de hebra negativa, ausencia de modelo, cuentas inválidas/duplicadas y ausencia de nombres individuales en salida. Suite completa en tests.txt.

No priorizar una nueva búsqueda de novedad CAMK2B ni inferencia cerebral de esta unión con el catálogo actual. Siguiente tarea segura seleccionada: auditar los dos pipelines MEA sintéticos del otro chat y reproducir sus pruebas por separado, tras leer código y verificar entradas. Deben seguir etiquetados como simulación y no proporcionar potencia o tamaños experimentales reales. Los cambios conceptuales Chan de PR#12 siguen vigentes; reanálisis numérico de esas curvas condicionado al mapa de unidades y tiempos.
