# Plan: cruce exacto con subconjuntos reconstruibles de S7/S8

Pregunta: ¿cuántas de las1901 claves intrónicas compartidas tienen la misma unión y una asignación genética inequívoca en los catálogos de cultivo de los autores?

Base main8 dfa7 ce7 c4 cc77 f28185 eaa286 e681 b0 c9 d5 ed39; reutilizar auditoría PR28(cabeza73 effb271 e835 fff59 e15039 e3303 f2 c4 a14 ec7 d), ampliando ese mismo PR, sin nueva cadena ni merge automático. Fuentes fijadas: annotation.tsv1901 y GENCODEv47 completa, S7/S8 por SHA256/MD5 del manifiesto. No descargar tablas clínicas ni analizar S15 por persona.

Método predefinido:
1. Resolver símbolos contra todos los genes de GENCODEv47. Para match genético estricto, un único símbolo en fila autora, un único ENSG global para ese símbolo y coincidencia con el candidato, cromosoma/hebra y locus. No asignar genes solo por proximidad; símbolos múltiples/ausentes/ambiguos se separan.
2. Validar bloques con el contrato ya auditado; no reparar filas. En S8 solo considerar las etiquetas N que coinciden con sus límites exónicos reconstruidos y convertirlas a intrón1-based(+1/−1). Excluir etiquetas no explicadas. En S7 reconstruir intrones de bloques válidos; esa coincidencia es contexto de transcrito con TE, no prueba de que esa unión específica sea TE-derivada.
3. Exigir igualdad exacta cromosoma, hebra, primer/último nucleótido intrónico y gen resuelto. Mantener clases S8 críptica, S7 contextoTE, coordenada con gen no resuelto, coordenada con otro gen, identidad de referencia no resuelta y no encontrada en subconjunto elegible.
4. Deduplicar evidencia por fila/candidato; exportar1901 filas y referencias estructurales de evidencia, sin clínica ni cuentas por persona. Presencia en hoja no demuestra expresión positiva, independencia o efecto KD; no usar Score como cuenta.

Controles y falsación: fixtures con exónico versus intrónico, hebra incorrecta, gen incorrecto, símbolos múltiples/reutilizados, locus discordante, bloques/etiquetas inválidos y duplicados. Buscar además STMN2 conocido chr8+, límites exónicos79611214/79616822(intervalo intrónico79611215–79616821), separado de1901 porque no está reconstruido en catálogo cerebral. Si el control real falta, documentar causa; no forzar coincidencia. Verificar hashes, filas1901 y únicos, conservación de denominadores y resultados repetidos. Una coincidencia de gen sin unión o de coordenadas sin gen nunca valida match estricto.

Predicción refutable: existirá un subconjunto cuantificable con coincidencias exactas; los no encontrados/no evaluables pueden constituir la mayoría. Ninguno acredita novedad, traducción, efecto clínico ni replicación independiente (son datos del mismo estudio). La ausencia en tablas incompletas no equivale a ausencia biológica o novedad.

Criterio de fracaso: fuentes modificadas, claves duplicadas/invalidas, identidad no trazable, controles fallidos o cruce por criterio laxo no declarado. No producir una lista de nuevas dianas; registrar bloqueos y continuar con contraste de incidencias mediante GTF o reproducción independiente #14.
