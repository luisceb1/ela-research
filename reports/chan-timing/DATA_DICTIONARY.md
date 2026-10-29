# Diccionario

- `audit.json`: extracción técnica de temporalidad explícita y metadatos. `figure7` se limita a7f–i; `figure8` al experimento de axotomía. DIV=tiempo de cultivo indicado por autores; no edad total desde iPSC ni inicio agudo de enfermedad.
- Campos `*_verified`: nulo=sin verificación en esta auditoría, falso solo cuando se declara una comprobación técnica negativa. No transformar nulos en falsos para clasificar prevención/reversión.
- `endpoint_DIV`: suma calculada de DIV lesión y días hasta inmunotinción; no dato de eficacia ni latencia ASO.
- `N` y rango `n`: cifras transcritas de pies, no tamaños recalculados ni diferenciaciones verificadas. Varias figuras del mismo estudio no son replicaciones externas.
- `numeric_cells_by_column_not_replicates`: número de valores almacenados, incluye respuesta/etiquetas numéricas según hoja. No n biológico.
- `explicit_DIV_labels_only_no_interpolation`: solo tiempos expresamente escritos en columnaA. No completar filas en blanco ni inferir frecuencia desde posición.
- `sources.json`: URLs canónicas, tamaño, SHA256, alcance de lectura. Copias editoriales, no originales experimentales verificados.
- `errors.json`: incidencias de acceso, disponibilidad, extracción y resolución. Errores recuperados no invalidan por sí solos los datos originales.
- `run.json`, `tests.txt`: entorno, repetición y pruebas técnicas. No validación científica independiente.
