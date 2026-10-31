# Verificación de referencia STMN2 — 31/10/2026

## Resultado comprobado

Plan previo: research/plans/2026-10-31-stmn2-reference-gate.md. La predicción técnica GT en el donante y AG en ambos aceptores de las coordenadas fijadas se cumple. Se recuperaron tres ventanas16bp desde UCSC y las mismas tres desde Ensembl; cada pareja coincide por bytes de secuencia. Ensembl declara GRCh38.p14, accessionGCA_000001405.29, chr8 longitud145138636. Son proveedores del mismo ensamblaje, no replicación biológica independiente.

| Sitio STMN2, hebra+ | Ventana0-based semiabierta chr8 | Secuencia genómica | Motivo previsto/observado | Controles desplazados−1/+1 |
|---|---|---|---|---|
| Donante común | [79611206,79611222) | AGCAATGGGTAAGGCA | GT/GT | GG/TA |
| Aceptor críptico candidato | [79616813,79616829) | TATTGCAGGACTCGGC | AG/AG | CA/GG |
| Aceptor canónico | [79636793,79636809) | CATTTCAGCCTACAAG | AG/AG | CA/GC |

Motivos extraídos de intervalos0-based [79611214,79611216), [79616819,79616821) y [79636799,79636801). No se cambian coordenadas para mejorar el resultado. La presencia de motivos compatibles no acredita que una unión se use, ni identidad de transcrito completo/polyA, ni función. No FASTA íntegro validado: son48bases únicas de referencia.

## Índice y software: candidato, todavía no aceptado

La página oficial HISAT2 enlaza hg38_genome.tar.gz. Un HEAD real a S3 devuelve4.355.786.349bytes comprimidos, última modificación25/06/2020, versionId8z.MUbL_W4wij.Nmcia5c4mT7tlz0cU. El manifiesto fija ese versionId para evitar una descarga de objeto mutable. **ETag2b99c030ca493d30bd4b12bf8e42327b-520 es multipart y no se trata como MD5.** No se descargó el archivo, no se conocen su SHA256 propio, integridad, tamaño extraído o compatibilidad efectiva. No afirmar que encaja por conocer solo los bytes comprimidos.

Se fija como versión candidata HISAT2v2.2.3, tag en commit0d244324f98de541bce04d45c75e83bc3522f7f4. Manual primario inspeccionado por esa revisión; no binario instalado o ejecutado. La documentación distingue número de alineamientos reportadosNH de búsqueda exhaustiva. No usar-k1 para fabricar unicidad. XS es hebra transcrita; no forzar F/R sin documentación de biblioteca. Las opciones dta cambian requisitos de anclaje y no se activan por inercia para este objetivo. El manual incluye ejemplosMAPQ255; el extractor actual los excluye. Esa diferencia exige un control con la versión ejecutada antes de aplicar el contrato, sin rebajar filtros a partir de efectos biológicos. No se concluye del ejemplo antiguo qué MAPQ producirá la versión nueva.

Los campos exactos, fuentes/versiones y pendientes están en index_candidate.json y software_sources.json. La fecha del índice y una etiqueta hg38 no certifican identidad con GENCODEv47. Se debe inspeccionar la referencia reconstruida, nombres/longitudes y ventanas antes de aceptar; no sustituir un genoma por una ventana recortada para afirmar unicidad.

## Ejecución y límites

Python3.12.14; estándar de biblioteca, sin dependencias nuevas ni aleatoriedad. reference_inputs.json conserva los payloads mínimos reales, URL exactas, hashes, y proyección de la respuesta de ensamblaje con hash del original. El hash del conjunto se verifica antes del replay. El script comprueba estadoHTTP, SHA256, esquema, ensamblaje/cromosoma, longitud, bases ambiguas, identidad de solicitudes y concordancia entre proveedores. Dos ejecuciones producen results.json idéntico por bytes, con hashes en run.json.

**284 tests locales correctos** (275previos+9nuevos), compileall correcto. Los controles negativos rechazan respuestas alteradas, referencia equivocada, discrepancia entre proveedores y coordenadas erróneas. Pruebas de software, no experimentos. La CI nueva debe verificarse por su cabeza y no valida el índice humano ni ejecuta FASTQ.

Se conserva el timeout inicial de Ensembl para el aceptor críptico; un reintento obtuvo16bases idénticas a UCSC. Las aperturas web de API UCSC fallaron al codificar parámetros; las seis recuperaciones efectivas fueron solicitudes Python. No se presenta la apertura fallida como lectura de datos. No efectos biológicos, cuentas RNA-seq, PSI, inferencia o validación funcional. Solo secuencia de referencia pública, sin datos clínicos personales.

## Operación y siguiente prueba

PR32 fusionado con autorización de Luis: merge9c82795df2dfdb1be142169ee8733db70dbde92f; cabeza57771806 y CI275tests enPython3.11/3.12 comprobadas antes del merge. Rama30 a053ef70ce437cc637ec18278a2c07e3abd6bf58b sin cambios. Este avance se propone aparte, sin otro merge automático. No costes, comunicaciones, laboratorio o publicación externa.

Única continuación: descargar de forma controlada el índice fijado, calcular SHA256 y comprobar integridad/recursos y referencia con hisat2-inspect. Máximo6GiB RAM,2hilos,15GiB disco adicionales y reserva8GiB del plan previo. Si el objeto/versionId no responde, el tamaño extraído excede presupuesto o no concuerda la referencia, detener y registrar bloqueo. Después ejecutar controles de semántica NH/XS/MAPQ y comparación de extracción con una implementación independiente; solo con puertas resueltas iniciar el piloto técnico predefinido. Sin prometer viabilidad o inferencia.

```bash
python scripts/audit_stmn2_reference_gate.py --input reports/stmn2-reference-gate-20261031/reference_inputs.json --expected-sha256 HASH_EN_RUN_JSON --out reports/stmn2-reference-gate-20261031/results.json
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

## Fuentes primarias

- UCSC Genome Browser, API getData/sequence para hg38/chr8. URL de cada intervalo y respuesta íntegra mínima en reference_inputs.json. https://api.genome.ucsc.edu/getData/sequence y https://genome.ucsc.edu/goldenPath/help/api.html.
- Ensembl REST, sequence/region y info/assembly/homo_sapiens. Solicitudes1-based, hebra+; originales mínimos y metadatos en reference_inputs.json. https://rest.ensembl.org.
- HISAT2, documentación de autores: https://daehwankimlab.github.io/hisat2/download/ y https://github.com/DaehwanKimLab/hisat2/blob/0d244324f98de541bce04d45c75e83bc3522f7f4/MANUAL.markdown. SeccionesSAM output, reporting, spliced alignment, inspect. https://benlangmead.github.io/aws-indexes/hisat.
