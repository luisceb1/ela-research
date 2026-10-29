# Anotación externa GENCODEv47 de1901uniones

29/10/2026. Auditoría de anotación, sin inferencia de novedad, función o eficacia.

Se verificaron SHA256 de la tabla estructural del PR24 y de GENCODEv47/GRCh38 completo. Se agruparon todos los exones por transcrito, sin asumir contigüidad; comparación exacta de gen estable, cromosoma, hebra y límites intrónicos1-based inclusivos.

| Clasificación | Uniones |
|---|---:|
| Coincidencia exacta para el mismo gen en GENCODEv47 |17|
| Gen reconocido, unión no encontrada para ese gen |1881|
| Gen ausente de esta versión de referencia |3|
| Discordancia de cromosoma/hebra del gen |0|

Total1901uniones/1250genes;1249genes reconocidos. Las tres uniones sin gen corresponden a un único ID, detallado en run.json. No convertirlas en evidencia de transcrito nuevo. Las17coincidencias demuestran que ausencia en ENST internos no equivale a ausencia de anotación externa. Las1881sin coincidencia requieren más evaluación; no son1881eventos crípticos nuevos.

La tabla exporta clave estructural, símbolo/tipo anotados, categoría y transcritos de referencia coincidentes. Es una búsqueda para el mismo gene_id; no se auditó reasignación a genes solapantes, otras versiones de GENCODE, variantes de ensamblaje, traducción o TE. Los IDs de transcritos son de referencia, no muestras. No se exportan datos individuales ni se recalculan efectos/pvalores.

## Catálogo del estudio de origen: pendiente

Se localizó el preprint Bolger DOI10.64898/2026.01.09.698641/PMC12803201. La página PMC devolvió recaptcha; EuropePMC entregó XML completo, fijado por hash. Se identifican17medios suplementarios distintos (1DOCX y16XLSX); las referencias se repiten en el XML y se deduplicaron por href. Inventario en author_supplement_inventory.json. Las tablas no se han descargado ni comparado: no se declara un cotejo con el catálogo crypTE.

Siguiente tarea segura: recuperar primero la descripción de tablas y verificar ensamblaje, coordenadas, gen/transcrito y tipo de evento. Un intervalo TE/exón no es automáticamente una unión intrónica. Solo después comparar las1881no encontradas y resolver el gen ausente. No priorizar una diana por este resultado de anotación aislado.

## Reproducción y controles

`python scripts/annotate_gencode_junctions.py --reference RUTA/gencode.v47.annotation.gtf.gz`

Original público: https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_47/gencode.v47.annotation.gtf.gz ; fuente editorial: https://doi.org/10.64898/2026.01.09.698641 ; XML: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12803201/fullTextXML . Hashes/alcance en summary.json e inventario. Entradas públicas originales fuera de git; tabla estructural por hash en el repositorio.

24tests locales pasan, cuatro nuevos: límites intrónicos/hebra negativa/deduplicación, categorías de gen/locus, exones intercalados y rechazo de solapamiento/no intrón adyacente. No son pruebas experimentales. Resultado exploratorio de anotación externa; no validación biológica ni comparación completa con los autores.
