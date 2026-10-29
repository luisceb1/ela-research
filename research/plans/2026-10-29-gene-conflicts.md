# Conflictos de asignación de gen

Auditar74claves con geometría coincidente y gen autor único diferente. Son23genes candidatos según sondeo inicial; no estudios/replicados. Contrastar ambos IDs contra GENCODEv47y modelos de los dosGTFGEO fijados previamente. No aceptar ninguna asignación como verdad por defecto.

Método predefinido: expandir símbolos con índice global exacto, verificar cromosoma/hebra y comparar unión intrónica exacta en transcritos GENCODE de ambos genes. En cada GTFGEO, agrupar todos los exones por IDdegen/transcripto/cromosoma/hebra antes de formar uniones; no asumir bloques consecutivos. Exportar IDs de transcritos testigos y distinguir modelos de lecturas. Solapamiento/span génico solo diagnóstico geométrico, nunca resolución por proximidad o eliminación de extensiones.

Controles: hashes de74claves/evidencias, referencias y GTF; gen contrario inequívoco; comparación exacta y hebra; conservar todos los modelos/genes compatibles. Una unión canónica del gen autor aporta una explicación alternativa, no demuestra que el candidato esté mal asignado. Un mismo salto puede existir en modelos de dos genes. No transformar modelos en moléculas, función, replicación o novedad.

Falsación: si el conflicto desaparece solo al excluir genes superpuestos, no se considera resuelto. Si ambas anotaciones tienen la misma unión, mantener atribución múltiple. Cierre: tablas por74claves y referencias de autores, partición por soporte de referencia/modelos, limitaciones y siguiente QCde cobertura o #14. Pruebas adversariales para exones intercalados, hebra y confusión entre canonización y causalidad.
