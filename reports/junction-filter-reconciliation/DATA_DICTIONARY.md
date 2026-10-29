# Diccionario

- `reconciliation.json/stages`: conteos de claves exactas después de cada selección. `grouped` agrupa todos los exones por TXNAME; `legacy` reproduce la agrupación consecutiva defectuosa. `positive` exige suma uniqueCounts>0en un modelo que contenga esa unión en cada serie, no lectura directa de la unión.
- `gene_counts`: genes distintos de los conjuntos, no tamaño muestral biológico.
- `datasets/*multiple_exon_runs`: modelos ENSG Bambu con más de un bloque de exones en el orden del GTF. No confundir número de bloques con número de transcritos.
- `comparison`: relaciones de conjuntos originales/agrupados y coincidencias con referencia interna. Un resultado presente en referencia de cualquiera de los dos GTF se excluye del conjunto no anotado.
- `structural_membership.tsv`: unión de las21claves originales y1910de catálogo. Contiene solo gen/cromosoma/límites/hebra y pertenencias booleanas; sin columnas individuales de muestras. Intrones1-based inclusivos en orden genómico, incluso en hebra−.
- `original_21_structural_keys.tsv`: proyección sin metadatos clínicos del CSV original, verificada contra el ZIP. No contiene los demás valores del informe previo.
- `source_inventory.json`: identidad del ZIP, miembros, funciones extraídas y proyección. `original_zip_verified_this_run` en el resultado solo es verdadero al pasar/verificar el ZIP durante esa ejecución.
- Los extractos en research/prototypes/junction_streaming_legacy.py conservan deliberadamente el fallo para demostrarlo en pruebas; no usarlos como parser de producción.
- `run.json`/`tests.txt`: controles de software. No validación experimental, genética, proteómica o clínica. `errors.json` conserva el fallo histórico y el alcance de lo corregido.
