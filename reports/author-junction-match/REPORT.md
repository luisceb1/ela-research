# Cruce de1901 uniones con el subconjunto reconstruible de catálogos de cultivo

29/10/2026. Evidencia exploratoria de anotación estructural, no validación experimental independiente. Fuentes: Bolger et al., bioRxiv v1 DOI10.64898/2026.01.09.698641(PMC12803201), licencia CC BY-NC; GENCODEv47/GRCh38 y proyección GTF pública del proyecto, todos por hash. Continúa la auditoría de esquema del mismo PR28.

## Evidencia

Se compararon1901 claves intrónicas con S7A–D(TE) y S8A–D(noTE) de cultivo, solo tras validar sus bloques. La identidad exige símbolo autor único, un único ENSG para ese símbolo en toda GENCODEv47 y concordancia con el ENSG/cromosoma/hebra del candidato. No se infieren IDs por proximidad ni se usan alias históricos. La referencia completa contiene78724 genes y480 símbolos con más de un ID;36 claves de entrada no superan identidad(33 por símbolo no inequívoco y3 por gen ausente).

| Clasificación de cada clave | Uniones |
|---|---:|
| Etiqueta noTE de S8, unión y gen resuelto exactos |284|
| Solo contexto de transcrito con TE en S7, unión y gen exactos |70|
| Misma coordenada, asignación genética autora no resuelta |278|
| Misma coordenada, otro gen inequívoco asignado por autores |74|
| Identidad de referencia no resuelta |36|
| No encontrada en el subconjunto elegible de cultivo |1159|
| Total |1901|

Hay145 claves con coincidencia estricta en contexto S7;75 también coinciden con etiqueta S8, de modo que la unión de coincidencias estrictas es354(284+70), no429 ni284+145 sin restar solapamiento. De esas354,353 estaban en la categoría sin coincidencia para el mismo gen en GENCODEv47 y una ya coincidía con esa referencia. Esto ilustra por qué no encontrar en GENCODE no demuestra novedad; tampoco las restantes se vuelven nuevas por descarte.

matches.tsv conserva las1901 claves, identidad, anotación GENCODE, categoría y hojas. evidence.tsv contiene referencias de4008 filas estructurales de evidencia(incluye coincidencias ambiguas o con otro gen); no4008 uniones únicas, lecturas o réplicas. Los2157 registros con gen exacto son referencias repetidas a las354 claves, no observaciones independientes. Se deduplica una etiqueta repetida dentro de una fila; no se borran fuentes distintas que permiten revisar la clasificación.

## Método y controles

El intervalo de comparación es intrónico1-based inclusivo, con igualdad exacta de cromosoma/hebra y ambos límites. En S8 solo se convierten etiquetas que coinciden con límites exónicos reconstruidos(+1/−1); siete etiquetas incompatibles con sus bloques se excluyen. En S7 se reconstruyen intrones de transcritos con anotación TE. Una unión de ese transcrito puede ser canónica o no estar en la región TE: la coincidencia no localiza la inserción TE ni prueba que la unión específica sea críptica.

Los denominadores y las exclusiones por bloques se contrastan con el QC anterior por hoja: S7=448818 filas/26815 no reconstruibles; S8=60471/14525 no reconstruibles. No se reparan listas ni se aceptan etiquetas aisladas de bloques inválidos. No hay exigencia de expresión positiva en las hojas autoras; presencia en hoja, Score o número de filas no sustituyen cuentas moleculares ni un efecto de KD. No se compara S15 ni se analizan filas de pacientes.

### STMN2: control real y fallo informativo de elegibilidad

La búsqueda predefinida de la unión críptica conocida STMN2(límites exónicos79611214/79616822, intrón79611215–79616821) no produjo una coincidencia elegible. Se investigó antes de aceptar los resultados:

- Diez filas S7A/B del locus, asignadas a STMN2, tienen ExonNum2 pero no dos longitudes interpretables. Sus offsets permiten verificar el extremo exónico derecho79616822 como anclaje parcial. No reconstruyen ambos límites de forma válida ni se reparan sus longitudes; el control críptico queda **no evaluable por bloques inválidos**, no ausente biológicamente.
- Dos filas válidas S8D(12237/12238) reproducen la unión canónica de STMN2 del GTF, intervalo intrónico79636898–79641377. Este control real de geometría confirma la conversión de coordenadas, no rescate ni carácter críptico. El script exige recuperarlo antes de escribir resultados.
- S5 contiene la etiqueta exónica conocida, pero sus fórmulas de presencia no se ejecutan ni se emplean como medición nueva.

El control está separado del universo1901 porque esa estructura críptica no figura en el catálogo cerebral reconstruido anteriormente. No se cuenta como coincidencia adicional ni réplica. summary.json conserva filas moleculares diagnósticas, sin datos clínicos.

Diez tests nuevos cubren conversión/deduplicación, bloques inválidos, hebra, locus, gen incorrecto, símbolos múltiples/ausentes/ambiguos, PAR_Y, categorías no evaluables y distinción entre control canónico y anclaje parcial. Suite conjunta125 tests. Se corrigió además una comparación de tupla/lista del control diagnóstico; no alteró los conteos del cruce. Ver errores y registro de repetición.

## Interpretación y límites

El resultado acredita representación estructural en un subconjunto de tablas del mismo estudio, no replicación independiente, novedad, traducción, causalidad o recuperación funcional. Las284 coincidencias S8 se refieren a etiquetas de los autores, no a un diagnóstico biológico nuevo. Las70 soloS7 se mantienen como contextoTE, no eventosTE validados. Los74 conflictos de gen no se reasignan automáticamente.

Los1159 no encontrados no son negativos biológicos: excluimos filas inválidas, símbolos ambiguos, otras categorías/tablas y tejido; no se auditó la cobertura exhaustiva de todos los eventos del artículo. La identidad genética por símbolo único es conservadora y versionada; los33 casos ambiguos podrían resolverse por fuentes con IDs trazables, sin cambiar silenciosamente el criterio. El intrón puede exceder límites de anotación de un gen; el chequeo de locus usa cromosoma/hebra, sin rechazar extensión terminal por ausencia en el span canónico.

No se aplican nuevos filtros por grupos clínicos ni se generan p-valores. La intersección con GENCODE y la presencia autoras son auditorías de anotación, no cohortes adicionales. Ningún resultado justifica proponer tratamientos o priorizar un no encontrado como descubrimiento.

## Reproducción y siguiente acción

`python scripts/match_author_junctions.py --cache data/cache/author-supplements --reference RUTA/gencode.v47.annotation.gtf.gz`

Entradas Office recuperables mediante el --fetch de audit_author_catalog.py; manifiesto de fuentes en research/references/bolger_author_catalog_v1.json. Los candidatos, la referencia y el control GTF se fijan por SHA256. Salidas TSV LF, resumen, tests, errores y hashes en este directorio. Sin fórmulas ejecutadas, datos clínicos, fuentes modificadas o fusiones automáticas.

Próxima tarea segura: revisar los conflictos/ambigüedades y la cobertura excluida usando identificadores o estructuras primarias trazables, sin inferir listas de longitudes. Si falta correspondencia con el GTF fuente, documentar el bloqueo y avanzar a reproducción independiente #14. El cruce completo de todos los catálogos autores, su tejido y copias TE específicas no se declara realizado.
