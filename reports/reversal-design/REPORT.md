# Reversibilidad: búsqueda dirigida y especificación falsable

Beccari et al., PNAS2025, DOI10.1073/pnas.2502294122, PMC12130871, Fig7: expresión introducida tres días antes de la axotomía, con crecimiento seguido después. El fondo es STMN2 nulo: la expresión se introduce después de la deficiencia genética, pero antes de lesión mecánica. Ambos relojes difieren. La comparación de genotipos tras lesión en ratón tampoco es administración correctora tardía.

Fuente: https://pmc.ncbi.nlm.nih.gov/articles/PMC12130871/ . XML oficial SHA256 en source.json; extracción del intervalo en regeneration_timing.json. Depósito de datos https://doi.org/10.5281/zenodo.15346391 . No se han cuantificado vídeos ni generado nuevas medidas de regeneración.

Búsqueda dirigida29/10/2026: STMN2/UNC13A, ASO, delayed, rescue, established dysfunction y regeneration. Fuentes primarias y versiones separadas. Nature Neuroscience DOI10.1038/s41593-023-01496-0 permite resumen/figuras, restringe cuerpo: no se le atribuye recuperación por retirada aquí. El enlace editorial al modelo humano2026 DOI10.1038/s42003-026-10832-6 falló; candidato pendiente, no evidencia incorporada. No revisión sistemática ni prueba de inexistencia universal de tratamiento diferido.

La ficha EXPERIMENT_SPEC.md convierte el límite de los diseños revisados en una comparación falsable con brazo concurrente, corrector diferido, control temporal y persistencia del daño. No se reivindica novedad de la pregunta. Se matiza que medir la misma unidad es preferible para MEA, no condición universal: cohortes paralelas bien controladas pueden establecer rescate.

Reproducción: python scripts/audit_regeneration_timing.py, con XML recuperable por URL de source.json; python -m unittest discover -s tests -v. 48 pruebas offline pasan. Código verifica DOI y extrae un intervalo explícito, sin inferirlo desde la palabra regeneración. No hay datos simulados, metaanálisis, p-valores nuevos ni experimentos.

Próxima tarea: inventario/reanalizabilidad de Zenodo y unidades independientes; un vídeo representativo no es réplica. Si está bloqueado, modelo humano2026 por otra fuente primaria. Antes de colaboración, contrastar exhaustivamente literatura y disponibilidad; la ficha no autoriza envío ni laboratorio.

Inventario ejecutado: 100 archivos,15.009.420.706bytes;27 imágenes Figure7 se agrupan por nombres en nueve series completas0/24/48h. Etiquetas de fichero no acreditan nueve réplicas biológicas; Fig7 del artículo declara dos diferenciaciones independientes. Debe resolverse asignación a diferenciación/cultivo antes de inferencia. No se descargaron esos TIFF ni se estimaron efectos. Reproducción del inventario guardado: python scripts/inventory_regeneration_data.py. Próxima tarea concreta: revisar descripción/metadatos del depósito, correspondencia de unidades y calibración de imagen; explorar después una muestra acotada para QC, manteniendo exploración separada de inferencia.
