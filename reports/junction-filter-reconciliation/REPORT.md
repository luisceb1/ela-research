# Por qué21no equivale a1910: pérdida de estructura en el parser original

29/10/2026. Issue#20. **Auditoría estructural y de software, sin nuevos hallazgos biológicos.**

## Resultado principal

El ZIP original se recuperó y verificó:15185bytes, SHA256`73edc0006287f355001f968ce12f54d38a148535c05f7195f2db83e636215393`. Se reprodujeron exactamente sus21claves de unión. La diferencia respecto a1910 **no se explica principalmente por filtros biológicos**: el parser antiguo asumía exones consecutivos por transcrito, pero los GTF contienen múltiples bloques del mismo transcrito. Cada bloque nuevo sobrescribía el modelo anterior, perdiendo exones y uniones.

El mismo supuesto afectaba a la búsqueda de referencias ENST:3de las21uniones estaban presentes en alguna referencia interna, aunque el informe original las clasificaba como no anotadas. Las18restantes pertenecen al conjunto correctamente reconstruido y con soporte positivo. Ninguno de estos números acredita traducción, toxicidad, novedad o beneficio clínico.

## Descomposición reproducida

| Método y escalón | Uniones compartidas |
|---|---:|
| Agrupar todos los exones por transcrito, antes de excluir ENST internos |21715|
| Mismo catálogo, excluyendo ENST internos de ambos GTF |1910|
| Exigir además suma uniqueCounts positiva por modelos que soportan la unión en cada serie |1901|
| Parser consecutivo original, soporte positivo, antes de su control ENST |21|
| Parser original tras su control ENST |21|
| Claves estructurales guardadas en el ZIP |21|

Solo9de1910carecen de soporte positivo en alguna serie bajo esta medida; excluir cuentas cero no reduce1910a21. El catálogo agrupado abarca1255genes y su subconjunto positivo1250; el paquete antiguo contiene20genes. Se comparan conjuntos de claves `(gene_id estable, cromosoma, primer nucleótido intrónico, último nucleótido intrónico, hebra)`, no solo sus tamaños. Todas las21claves existen en la intersección Bambu reconstruida antes de excluir ENST;3se excluyen por referencia interna y18se conservan. Hay1892claves del catálogo de1910que no figuraban en el paquete antiguo.

## Evidencia del fallo de agrupación

| Control sobre GTF real | GSE310723 | GSE315972 |
|---|---:|---:|
| Modelos Bambu con varios bloques de exones separados |9403|16321|
| Modelos con unión tras parser antiguo |278|682|
| Modelos con unión al agrupar todos los exones |9527|16633|
| Uniones Bambu de catálogo, antes de cruce/filtro ENST |53964|66653|

La prueba mínima intercala exones de dos transcritos. El parser antiguo conserva solo el último bloque de cada uno y pierde ambas uniones; el agrupado conserva la unión esperada y es invariante a esa intercalación. Otro test reproduce la pérdida equivalente en la referencia ENST. Son controles de contrato de entrada, no datos experimentales.

El contador histórico `bambu_without_ensg` cuenta pasos por bloques, no transcritos distintos; no reinterpretar1222/3940como exclusiones únicas. Las exclusiones únicas por asignación no ENSG de la fuente anterior eran820/2563. No se arregla ese contador para forzar el resultado; se conserva su alcance en el JSON de auditoría.

## Tres clasificaciones de novedad interna que se corrigen

| Gen depositado | Coordenadas intrónicas GRCh38 | Hebra |
|---|---|---|
| ENSG00000169258 |chr5:176599878–176609998|−|
| ENSG00000274225 |chr21:44475850–44477228|+|
| ENSG00000303579 |chr10:1054246–1056308|−|

No se asignan símbolos no comprobados. La coincidencia procede de ENST internos de estos GTF; no equivale a una auditoría completa de GENCODE, ni los1901restantes son automáticamente crípticos o nuevos. Tampoco demuestra igualdad de transcrito completo ni lecturas físicas que atraviesen la unión.

## Qué se reproduce y qué no

- Se cotejan los cuatro SHA256 GEO con la auditoría previa. El ZIP original tiene siete miembros verificados por CRC/SHA256. Cuatro funciones originales se conservan como extractos exactos, con rangos de línea y hashes; no se importa su CLI ni código de metadatos por persona.
- El soporte por transcrito se reduce internamente a su suma para evaluar cero/no cero. Esto conserva exactamente el criterio de exclusión original; no exporta recuentos por biblioteca/donante ni crea otra observación independiente.
- Se repite la selección original y su búsqueda ENST, y se compara con `scripts/audit_shared_junctions.py` de main. Las21claves reproducidas coinciden con el CSV del ZIP, incluyendo los casos que el parser agrupado excluye por referencia.
- La pertenencia de las21y1910claves se conserva en `structural_membership.tsv`. No se generaron p-valores ni se reejecutaron los filtros clínicos/celulares para darles una nueva interpretación. Los conteos repetidos en varias ejecuciones son idénticos; no son nuevas réplicas.
- El código original ya usa tres índices CI y tres no CI, coherentes con la curación3/3/2de main. La corrección previa de etiquetas ALS-CI sigue vigente, pero no causa la diferencia estructural21/1910. No se hizo una nueva inferencia clínica ni se recopilaron variables personales.

## Consecuencia para el proyecto

El informe antiguo de21eventos deja de ser un cribado exhaustivo válido de estos GTF. Sus proporciones de selección y lista corta reflejan una reconstrucción incompleta. No recomendar experimentos sobre esa lista como si proviniera del catálogo íntegro. La coincidencia de una conclusión nula con otro filtro no valida retroactivamente el parser.

Se reproduce el catálogo de1910del otro flujo;1901cumplen además soporte uniqueCounts positivo en ambas series. Ni la referencia interna ni esa coincidencia entre series establecen novedad. Ambos datasets proceden del mismo estudio de origen, con una biblioteca por condición en cultivo y tejido cerebral heterogéneo; no se convierten en validación experimental/publicacional independiente.

El universo se limita a modelos BambuTx asignados a ENSG y presentes en estos GTF; excluye asignaciones BambuGene, eventos no reconstruidos y otras regiones/células.1901no es un catálogo exhaustivo de eventos crípticos de ELA. Tampoco se presume que todos esos genes codifiquen una proteína o péptido pertinente.

## Reproducción y controles

`python scripts/reconcile_shared_junctions.py --cache RUTA_CACHE_PUBLICA`

El repositorio conserva una proyección segura de las21claves y los cuatro extractos de funciones, fijados por hash. Por tanto, la reproducción de conjuntos ya no depende de recuperar de nuevo el ZIP privado. Para verificar su identidad exacta en una ejecución, añadir `--original-zip RUTA_ZIP`; el JSON distingue si se verificó ese ZIP en la ejecución actual. No afirmar verificación de bytes originales solo porque la proyección coincide.

Cuatro pruebas nuevas cubren intercalación, invariancia de agrupación, soporte cero y referencia ENST. La suite completa de esta rama contiene20tests(12mapeo,4de reconciliación y4generales); CI ejecuta ahora esa suite completa. Se verifican identidad de funciones/proyección, claves sin duplicados y ausencia de intervalos intrónicos inválidos en la comparación. La ejecución y las incidencias se registran en run.json/errors.json.

## Estado y siguiente tarea segura

Issue#20queda documentada para revisión, sin cierre ni merge automático. El bloqueo de acceso al paquete original está resuelto y la causa21/1910reproducida. No es un cambio de evidencia terapéutica.

Siguiente: contrastar las1901claves con GENCODEv47completa y el catálogo público de eventos del artículo de origen antes de priorizar candidatos o la pregunta funcional AGRN de#21. Registrar anotaciones/ambigüedades, no llamar nuevo a lo que solo falta en el ENST interno, y no iniciar laboratorio o contactos sin autorización.
