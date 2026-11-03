# Integridad paired FASTQ y límites explícitos — 02/11/2026

## Evidencia

Continuación del PR #36 desde22d285f8f1f2a7ee428e8dc4dbf523f795d8d426, sin modificar main. Se leyeron las issues #1/#2 y las cabeceras de ambas ramas antes de elegir la tarea: GEO/mapeo, QC STMN2 y reproducción PPAU ya estaban hechos. No se repitieron esos análisis. Plan previo en research/plans/2026-11-02-paired-fastq-local.md; predicción: tres pares artificiales producen exactamente el prefijo de dos, pero ambos gzip se recorren hasta EOF/CRC. Cada corrupción debe impedir un recibo verificado. Cambiar límites no permite reutilizar una fase.

Implementado scripts/paired_fastq_integrity.py: cuatro líneas por registro, DNA ACGTN, longitud secuencia/calidad concordante, nombres sincronizados, sufijos /1 y /2 y etiquetas CASAVA explícitas, identidad de línea+ cuando existe. No inferencia de codificación Phred a partir del rango ASCII. Escaneo completo, incluidos miembros gzip concatenados y errores posteriores al prefijo. Prefijos gzip deterministas (mtime0, sin nombre de fichero embebido), hashes SHA256 y tamaño, fsync de archivos y recibo JSON atómico. Directorio exclusivo: no sobreescribe intentos anteriores. Un fallo deja status=failed y los parciales no se certifican; solo result.json verificado acredita ambos prefijos.

En pilot_dry_runner.py los límites explícitos requieren caps ligados al fingerprint persistente. La firma de proceso incluye dichos límites, impidiendo reutilizar un recibo con otra configuración. Se conserva el comportamiento histórico5s/128MiB solo para pruebas sintéticas. plan_process permite representar900s/6GiB del plan sin ejecutar nada; process(production=True) se rechaza. La marca raw_execution_ready permanece false.

## Ejecución y controles

Python3.12.14 ejecutado realmente. 48 tests locales correctos: 29 nuevos (21 de FASTQ y8 de configuración) más19 existentes del runner/transporte. Compileall correcto. La suite completa del repositorio se comprueba por separado en CI de la nueva cabeza; no se presenta esta selección local como la suite completa.

Dos validaciones locales de cada fixture producen resultados y prefijos idénticos por bytes. En executed-final: tres pares escaneados, dos escritos. Cada prefijo comprimido ocupa53bytes. SHA256 deR1:8aebdaa57101006d6aee780b9ff97f069b6f8aead96d5c6399733eb7aa546fb5; deR2:fa1602869df30cdd17290808c94f41a33ca1941fd19bca185396b6a75b82f977. Los payloads se crean en temporales y se descartan; aquí se guardan metadatos agregados y código generador, sin identidades o secuencias de lecturas biológicas.

Se conserva el negativo ejecutado: CRC corrupto después de escribir el prefijo provoca failed/BadGzipFile y no certifica el prefijo. Las pruebas también rechazan gzip truncado, mate ausente/extra/desordenado, etiquetas contradictorias, longitudes incorrectas, línea+ de otra identidad, prefijo mayor que la fuente y límites incompletos/inválidos. Se prueban reutilización de fase con límites distintos y recorte por deadline global. executed conserva la demostración inicial; executed-final corresponde al código con fsync de prefijos añadido. No hubo fallo inesperado de pruebas en esta fase.

Reproducción sin red externa:

```bash
python -m unittest discover -s tests -p 'test_paired_fastq_integrity.py' -v
python -m unittest discover -s tests -p 'test_pilot_process_limits.py' -v
python scripts/run_paired_fastq_fixture_gate.py /tmp/paired-fixture-new-directory
```

La última carpeta debe ser nueva. Los tests existentes de HTTP usan únicamente loopback; la consulta bibliográfica no accedió a datos biológicos. Ningún FASTQ deGSE296714, índice humano o alineamiento se descargó/ejecutó.

## Interpretación y límites

Es validación de integridad y configuración de software sintético, no replicación externa, cobertura de UNC13A ni validación funcional. Tener un prefijo correcto no demuestra muestras independientes, unicidad global de QNAME, codificación de calidad o factibilidad de un millón de pares. La política de cuatro líneas no pretende admitir todas las variantes FASTQ; un formato fuera de la política se detiene, sin conversión automática. Los hashes de entrada deben enlazarse con el recibo publicado/descargado en la fase de integración siguiente.

Los900s/6GiB solo se validaron como configuración. No se ejecutó un proceso con el presupuesto previsto para el genoma humano ni se certificó un techo agregado kernel/RAM. El watchdog RSS sigue siendo muestreado. No se acredita aquí plazo de socket externo, tráfico TCP/TLS o resistencia adversarial a modificación concurrente de archivos. La integridad del par de salidas se decide por el recibo final, no por la mera presencia de un gzip final o parcial.

## Siguiente prueba discriminante

Integrar estos controles como una fase ligada al ledger/recibo de transferencia y al manifiesto, con archivos locales sintéticos y escenarios de interrupción/reanudación. Debe rechazar identidad/hash cambiado, recibo.started/failed, prefijos parciales y límites distintos, sin reiniciar deadline ni consumos. Solo después reevaluar el gate de ejecución real. No hay nueva descarga o permiso implícito para procesar bibliotecas completas. Sin merge/cierre automático, contactos, costes, clínica o laboratorio.

## Referencias y acceso

Cock et al. (2009, publicación en línea). *The Sanger FASTQ file format for sequences with quality scores, and the Solexa/Illumina FASTQ variants*. Nucleic Acids Research,38(6),1767–1771. https://doi.org/10.1093/nar/gkp1137.

Scite devolvió únicamente el resumen (contentDenied=true), no texto completo. Extracto breve: “existing in at least three incompatible variants”. Esto fundamenta la cautela de no inferir la variante/codificación; la política implementada es una restricción prospectiva comprobada con fixtures. editorialNotices no figuró en la respuesta: el estado editorial no se certifica. Acceso y límites en source-access.json; no se afirma revisión completa del artículo.
