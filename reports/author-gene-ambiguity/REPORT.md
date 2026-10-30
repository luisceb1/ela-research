# Identidad de genes y ambigüedad del catálogo — 29/10/2026

## Evidencia

Se revisaron las 1901 claves y 4008 referencias a filas autoras del cruce anterior, con entradas fijadas por SHA256. Estas filas no son réplicas biológicas. El análisis se centra en las 36 claves con identidad de referencia pendiente y las 278 con coincidencia geométrica y gen autor no resuelto. Plan previo: `research/plans/2026-10-29-author-gene-ambiguity.md`.

| Conjunto | Resultado de este QC | Límite |
|---|---|---|
| 36 identidades candidatas, de 17 ENSG distintos | 33 claves tienen ENSG presente y cromosoma/hebra concordantes; 3 de un solo ENSG no están en v47 | Resolver el ID del candidato no equivale a resolver el gen de la fila autora |
| 278 claves con gen autor ambiguo | Ninguna obtiene una fila del mismo gen inequívoca bajo la sensibilidad conservadora | No usar vecino, span canónico, símbolo preferido o mayoría de filas para forzar identidad |
| 354 coincidencias estrictas originales | Todas se conservan como controles positivos | Resultado histórico sin sobrescribir |
| Una clave adicional | Coincidencia condicional GTPBP6 en chrY, en 3 filas S8 | Dependiente de locus declarado/anotación; no prueba origen cromosómico de lecturas |

Las 33 identidades estaban bloqueadas por unicidad **global del símbolo**, aunque el ENSG exacto ya estaba disponible. Esto es una limitación conservadora de aquella regla, no prueba de asignación errónea del gen. El diagnóstico por ID se registra aparte y no reescribe el cruce original.

## Método y controles

GENCODE v47 completo, mismo snapshot que el cruce: SHA256 `df11938c66d2b39f8ebbdb5f1720919321f9cf9d58f02b019753f6a24ca3db24`. Se elimina solo versión numérica del ENSG, preservando `_PAR_Y`. Para cada candidato se exige que el ID exista y coincida en cromosoma/hebra. No se usa distancia ni span génico para resolver una unión no canónica.

Cada token autor se expande por símbolo exacto al conjunto completo de ENSG de ese snapshot, o por un ENSG literal que exista. Se conservan por fila todos los tokens, IDs globales, IDs compatibles, descartes por locus y tokens no resueltos. Solo se ofrece `conditional_same_gene` cuando todos los tokens son conocidos y cromosoma/hebra dejan un único ID, igual al candidato. Un token desconocido o `None` bloquea esa resolución; no se descarta para favorecer al token conocido. Varios IDs en el mismo cromosoma/hebra siguen siendo ambiguos, aunque un gen esté más cerca.

Las 278 claves tienen 1202 referencias a filas: 1144 conservan varios IDs compatibles; 54 apuntan condicionalmente a otro gen único; 4 tienen token `None`. Ninguna fila de este conjunto pasa a mismo gen. La presencia de una fila de otro gen no elimina las demás evidencias ambiguas ni convierte automáticamente todo el candidato en ese otro gen.

## GTPBP6: sensibilidad, no nueva coincidencia estricta

Clave: `ENSG00000292358 / chrY:317052–317278 / -`, coordenadas intrónicas 1-based. El símbolo GTPBP6 devuelve también `ENSG00000178605` en chrX. Ambos registros v47 tienen intervalo génico 303346–318798 y hebra negativa. Restringir al cromosoma Y declarado en la fila autora selecciona un solo ID; sin esa restricción, el símbolo no es único.

Se volvieron a leer directamente las filas S8A 16245/16246 y S8D 13754 del XLSX original, verificado por hash. En las tres se recuperan bloques válidos y etiqueta elegible con esa geometría. Localizadores/transcriptos/campos originales en `conditional_primary_rows.json`. Son tres referencias del mismo estudio, no tres replicaciones ni evidencia de tres moléculas independientes.

La sensibilidad produce 355 claves con alguna fila condicional del mismo gen: las 354 anteriores más esta. **No sustituye el total estricto 354 por 355.** La coincidencia depende del cromosoma declarado; no audita alineamiento de lecturas entre X/Y, identidad completa del transcrito, función, crípticidad independiente ni novedad. La etiqueta autora NovelExon se conserva como etiqueta, no se valida biológicamente aquí.

## Las tres claves ausentes de v47

Las tres corresponden a `ENSG00000276256`, en `chrUn_GL000195v1`, hebra negativa. Se verificó procedencia en los dos GTF GEO fijados previamente: 16 líneas en cultivo y 21 en cerebro contienen `ENSG00000276256.1`; son registros de anotación, no cuentas ni réplicas. Ejemplos/hashes en `missing_gene_provenance.json`. No es un ID inventado por este QC, pero tampoco se encontró en la referencia v47 utilizada. No se asigna un reemplazo, alias, causa histórica de ausencia ni locus alternativo sin fuente.

## Interpretación y limitaciones

Este avance separa identidad del candidato y atribución del autor. La exigencia anterior de símbolo globalmente único puede excluir candidatos cuyo ID es válido; relajarla de forma explícita recupera identidad técnica, no validación molecular. En el conjunto ambiguo dominante, cromosoma/hebra por sí solos no bastan. Resolverlo requeriría vínculo primario transcrito→ENSG o nueva evidencia que distinga genes compatibles. No seleccionar por cercanía o por resultado esperado.

Las tablas originales y su QC de filas inválidas/conversión de coordenadas permanecen intactos. Se reutilizan sus evidencias de geometría fijadas por hash y se comprueban de nuevo las tres filas de la única clave adicional. No se reejecuta aquí todo el cribado XLSX como si fuera una validación externa. Sigue siendo subconjunto elegible de cultivo; no análisis completo del catálogo/tejido. No se estudia clínica ni se calcula significación.

## Reproducción, errores y siguiente tarea

`python scripts/audit_gene_ambiguity.py --reference /ruta/gencode.v47.annotation.gtf.gz --author-cache /ruta/author-supplements --geo-cache /ruta/cache_GEO` genera tablas y comprobaciones primarias. Sin las dos opciones de caché se puede regenerar el diagnóstico desde TSV + referencia, pero no las comprobaciones primarias; el par de opciones se exige completo. Fuentes GEO/autor y hashes en manifiestos citados por sources.json.

Nueve pruebas nuevas comprueban ambigüedad en el mismo locus, token desconocido, ID versionado, `_PAR_Y`, cromosoma/hebra, gen distinto y tokens vacíos. Suite completa: **149 tests OK**. Las cuatro tablas TSV fueron idénticas en dos pasadas completas; hashes y comandos en run.json. No se encontraron discrepancias en las tres filas primarias revisadas. Los estados no resueltos son resultados, no errores de ejecución.

Siguiente tarea segura seleccionada: auditar las 74 claves con coincidencia de coordenadas atribuida a otro gen único, contrastando anotación y evidencia primaria sin adoptar automáticamente la asignación autora o del candidato. Después evaluar cobertura antes de priorizar candidatos; no elevar las 1159 no encontradas a novedad. Si falta vínculo primario, conservar conflicto y avanzar a reproducción acotada de #14 conforme al backlog. No contactos, gastos, laboratorio o merge automático.
