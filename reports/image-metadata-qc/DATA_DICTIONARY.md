# Salidas
- tiff_headers.json: tags observados, rango exacto y hash del rango, tamaño/checksum esperado del origen, escala física solo cuando explícita. MD5 del fichero completo no verificado.
- figure7_workbook_cells.tsv: referencias de celda Figure7, texto/valor original y fórmula cuando exista, sin evaluarla. Campo sheet identifica la hoja; no identificador biológico.
- summary.json: recuentos estructurales; entradas de longitudes por columna no son réplicas.
- errors.json y run.json: estado y fallos de cabecera; generated solo si se leyeron las27. Archivo vacío de errores no prueba calidad biológica.
- tests.txt:59controles de software offline, no validación de efectos ni calibración de imágenes sin tags.
