# QC de identidad y ambigüedad de genes

Pregunta: ¿qué parte de36identidades candidatas no resueltas y278coincidencias geométricas con gen autor ambiguo se explica por exigir unicidad global de símbolos, y qué parte persiste al usar identificadores estables y locus explícito?

Fuentes: salidas fijadas por hash del cruce anterior, GENCODEv47completo y GTF originales del proyecto si hace falta procedencia. No consultar ni descargar clínica. No resolver por vecino más cercano, alias no trazables, span canónico, frecuencia o fuerza del efecto.

Controles y falsación: un ENSG presente debe coincidir con cromosoma/hebra del candidato; preservar sufijo_PAR_Y. Para autores, expandir todos los tokens a sus ENSG del mismo snapshot. Solo ofrecer diagnóstico condicional si todos los tokens son conocidos y la restricción explícita de cromosoma/hebra deja un único ID, igual al candidato. Tokens desconocidos o varios IDs compatibles mantienen ambigüedad. No usar límites génicos para excluir extensiones no canónicas ni convertir el diagnóstico en validación molecular.

Mantener354coincidencias estrictas originales como resultado histórico. Si aparece resolución adicional por locus, exportarla separada como sensibilidad dependiente de anotación, con todos los IDs/tokens descartados y motivo; no sobrescribir tablas. Varias filas/sheets de un mismo transcrito no son replicación. Criterio de fracaso: cualquier resultado promovido con token no resuelto, locus discordante, ambigüedad persistente o clave fuera de universo.

Entregables: tabla36por clave, tabla278por clave y evidencias relacionadas, resumen de estados antes/después y fuentes/hashes; Python reproducible y tests adversariales. No significación, función ni novedad inferidas. Si la resolución requiere metadatos inexistentes, registrar el límite y seleccionar siguiente QC/#14del backlog.

Sondeo inicial: algunas etiquetas de autores contienen un ENSG literal junto a símbolos. Se permite reconocer ese identificador solo por igualdad exacta con el índicev47, eliminando únicamente versión numérica y conservando_PAR_Y. No convertir un ENSG desconocido a un símbolo inferido. Registrar por token si la evidencia procede de ID o símbolo; las demás reglas conservadoras se mantienen.
