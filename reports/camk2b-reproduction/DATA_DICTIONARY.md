# Diccionario de salida agregada

`audit.json`:
- `sources`: hashes/URLs públicos cotejados con auditoría previa; no implica que el procesamiento original sea infalible.
- `summary`: número de modelos por gen/serie, suma de cuentas asignadas y presencia agregada en bibliotecas. No contiene nombres de muestras. Sumas entre series no son contrastes normalizados.
- `CAMK2B_target_matches`: número de modelos CAMK2B con coincidencia exacta de gen/cromosoma/hebra/límites. Nulo en otros genes, porque ese evento no se les busca.
- `CAMK2B_target_transcript_assigned_sum`: suma de transcritos coincidentes. Cero si no existe modelo; **no una medición directa de cero lecturas de la unión**.
- `candidate_junctions`: límites exónicos de candidatos celulares y número/suma de modelos cerebrales coincidentes. Un mismo transcrito puede coincidir con varias uniones: no sumar estos renglones.
- `prior_report_predictions`: contraste de resultados esperados frente a observados; el código no descarta resultados discrepantes para forzar una réplica.

`prior_package_check.json`: identidad del ZIP y código recibido, hashes de entradas declaradas y cotejo con fuentes actuales. No ejecuta el código recibido ni copia tablas por persona.

`run.json`, `tests.txt`: comprobaciones técnicas, versión y determinismo. `errors.json`: incidencias recuperadas. Ninguno demuestra réplica biológica ni validación clínica.
