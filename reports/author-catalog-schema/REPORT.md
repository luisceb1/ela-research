# Catálogo crypTE: fuentes recuperadas y comparación estructural todavía pendiente

29/10/2026. Auditoría de fuentes, esquema y reconstrucción; no nuevos hallazgos biológicos. Bolger et al., bioRxiv v1 DOI10.64898/2026.01.09.698641, PMC12803201. Preprint y licencia CC BY-NC; investigación no comercial. NCBI PMC Article Datasets on AWS, consultado el29/10/2026.

## Evidencia

Se recuperaron el índice DOCX y cuatro XLSX mediante el repositorio público oficial de PMC en AWS, después de fallos en PMC/EuropePMC/bioRxiv. No se requieren cuenta ni gastos. Listado S3 y metadatos JSON verifican identidad/versionado; cinco Office verificados por SHA256, MD5 publicado y tamaño. No se confunde ETag multipart con MD5: para archivos grandes se usa el MD5 explícito de los metadatos JSON. XML primario EuropePMC verificado con el hash anterior. Manifiesto: research/references/bolger_author_catalog_v1.json.

El XML contiene17medios distintos, duplicados en dos secciones; el DOCX enumera42subtablas. Los xref/rid y las leyendas permiten asignar tabla a archivo sin inferirlo del número media: S5=media-6, S7=media-8, S8=media-9 y S15=media-16. S12=media-13 contiene metadatos clínicos individuales y no se descargó. S13/S14 no se descargaron. El análisis no exporta filas por persona, cantidades por donante ni clínica.

## Qué contienen las tablas inspeccionadas

| Tabla | Uso comprobado | Límite para el siguiente cruce |
|---|---|---|
| S5 | Uniones publicadas y presencia nominal en condiciones de cultivo | No es catálogo exhaustivo ni prueba nueva independiente |
| S7A–D | Catálogo TE de cultivo con columnas tipo BED12 y gen/tipo TE | Reconstruir bloques antes de deduplicar uniones; filas no equivalen a transcritos/eventos únicos |
| S8A–D | Catálogo noTE de cultivo con etiquetas de uniones y bloques | Cabeceras N/O de B/C dicen TE/CryptTE type, aunque contienen uniones/clases noTE; no mapear por nombre sin validar contenido |
| S15 | Eventos compartidos, símbolos y extremos de transcritos; incluye columna Patient | Inspección reproducible solo de título/cabecera. No tiene pares de límites de unión. Encabezado K2 repite Transcript1Start en bloque de transcrito2; no corregir por suposición |

Además, el título de S7D dice S7C; la hoja y la leyenda identifican S7D. El script conserva ambas evidencias y marca el desacuerdo. Las fórmulas del resumen S5 se señalan sin ejecutarlas ni usar sus resultados cacheados.

## QC completo de las hojas de cultivo

| Catálogo | Filas de datos | Bloques reconstruibles con contrato estricto | Filas no reconstruibles |
|---|---:|---:|---:|
| S7A–D |448818|422003|26815|
| S8A–D |60471|45946|14525|

Son filas de las tablas, no individuos, lecturas independientes, transcritos únicos ni réplicas. Las fallas incluyen cantidad de longitudes/offsets incompatible con ExonNum, valores sin representación entera literal y bloques de longitud no positiva. No se insertan comas, convierten números en listas o imputan exones para hacerlas pasar. Este resultado no demuestra errores biológicos en los datos crudos o en toda la publicación.

De las filas reconstruibles S7,21022tienen al menos un intrón y400981no lo tienen bajo sus bloques. No interpretar todas las filas TE como uniones: esa tabla y nuestro universo de1901claves no tienen la misma unidad. El QC no exige expresión positiva ni convierte Score en cuenta molecular.

## Convención de coordenadas: comprobación geométrica

Los campos de bloques son compatibles con geometría BED: inicio0-based, final exclusivo, longitudes y offsets relativos; el contrato se contrasta con documentación primaria UCSC. Para dos bloques cuyo final izquierdo exclusivo esL y comienzo derecho0-based esR:

- límites en bases exónicas1-based: L y R+1;
- intrón1-based inclusivo usado en nuestras1901claves: L+1 y R.

En S8 reconstruible,103592de103599etiquetas listadas coinciden con el primer par; cero con el segundo y7no se explican por sus bloques. Se cuentan etiquetas, con posibles repeticiones entre filas, no103599eventos independientes. Es una inferencia geométrica respaldada por el contenido; no una declaración explícita de los autores sobre el formato. La transformación propuesta para etiquetas concordantes es inicio+1/final−1, después de validar cromosoma/hebra/bloques. No aplicarla ciegamente a las7excepciones o filas inválidas.

La distinción también existe en el repositorio: reports/isoforms/junctions.tsv y event-reference usan límites exónicos explícitos; junction-filter-reconciliation y gencode-junction-annotation usan intervalo intrónico. No comparar esas columnas como si fueran idénticas. La unión conocida STMN2 allí documentada como límites exónicos79611214/79616822 corresponde al intervalo intrónico79611215–79616821, no a los mismos números sin conversión.

## Interpretación

El método de los autores (XML P54) define compartir mediante gen y la misma copia TE, con colapso por gen/categoría. Esto no equivale a igualdad de una unión, de cadena completa ni a nuestros filtros de conteos asignados. También distingue TSS, ApA, exónTE y eventos sinTE. S15 no puede cotejarse directamente con1901intrones usando los extremos de sus transcritos.

Por tanto, **no se ha ejecutado una intersección de las1901claves con el catálogo de autores**; no se informa cero coincidencias ni novedad. Haber recuperado las fuentes elimina el bloqueo de acceso, pero deja decisiones de equivalencia y cobertura. El siguiente análisis debe contrastar solo estructuras reconstruibles con gen/cromosoma/hebra, resolver símbolos frente a IDs ENSG, excluir ambigüedades y publicar denominadores de elegibilidad. Los no evaluables deben quedar separados de las no coincidencias. Los GTF públicos pueden servir para contrastar incidencias sin reparar los XLSX de forma silenciosa.

## Reproducción, controles y límites

`python scripts/audit_author_catalog.py --cache data/cache/author-supplements --xml data/cache/author-supplements/primary.xml --fetch`

Descarga únicamente los cinco Office fijados y el XML, nunca S12 ni el paquete completo. Sin --fetch, todas las entradas deben existir y pasar hashes. Cabeceras de S5/S15 por posición; QC completo solo de S7/S8 permitidas. Office sin macros, expansión limitada, lectura de celdas sin ejecución de fórmulas ni enlaces. El byte hash del audit.json repetido coincide; los conteos de QC también permanecen iguales tras mejorar liberación de memoria.115tests locales pasan, diez nuevos; no son experimentos. Detalles en audit.json,run.json,tests.txt y errors.json.

Fuentes primarias: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12803201/fullTextXML ; https://pmc-oa-opendata.s3.amazonaws.com/PMC12803201.1/PMC12803201.1.json ; https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/ ; https://genome.ucsc.edu/FAQ/FAQformat . Los binarios permanecen fuera de git, recuperables por URL/hash. No publicar o redistribuir hallazgos fuera del repositorio privado ni contactar a autores sin autorización.
