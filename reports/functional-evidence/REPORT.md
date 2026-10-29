# Auditoría funcional: qué rescatan y cuándo

Evidencia curada manualmente de fuentes primarias; no reanálisis experimental ni revisión sistemática exhaustiva. Matriz reproducible en matrix.tsv; cinco unidades de evidencia, no cinco estudios independientes. Los dos registros Keuss son versiones relacionadas.

## Evidencia e interpretación

**STMN2 — Baughn 2023.** El resumen primario de Science (PMID36927019, DOI10.1126/science.abq5622) informa recuperación de regeneración axonal y transporte lisosomal en motoneuronas humanas tras corrección del procesamiento. El experimento de ratón humanizado informa corrección molecular y recuperación de expresión: no trasladar allí automáticamente la función observada en células. La cronología y controles detallados quedan sin auditar porque el XML completo devolvió HTTP500 dos veces. No se concluye reversión tardía.

**UNC13A — Keuss 2024, preprint.** El texto completo distingue ARN, proteína y frecuencia de mEPSCs (Fig4), con ASO control scrambled. Su sección de tratamiento indica que, en HaloTDP iNeurons, ASO y PROTAC comenzaron juntos y continuaron durante dos semanas. Ese diseño demuestra protección/rescate frente a la perturbación concurrente; no establece administrar ASO después de medir disfunción en las mismas neuronas. Los experimentos de otras líneas celulares tienen calendarios distintos y no deben sustituir al del ensayo neuronal funcional.

**Keuss/Harley 2026.** El registro institucional confirma aceptación/in press a 6/10/2026 y comunica recuperación sináptica en neuronas humanas. El PDF aceptado devolvió HTTP403; no se asigna a esta versión la cronología de 2024. Registro y preprint no se cuentan como replicaciones independientes. Campo protein=false en la matriz significa no extraído en esta revisión del abstract, no ausencia de rescate proteico.

**Control de temporalidad adicional, preprint 2025 (PMC12424808).** Los autores administran ASOs en días3/10 y shRNA TDP43 en día5; recogen ARN en día12 y proteína en día15. El primer tratamiento precede la perturbación. Este calendario es evidencia de prevención/concurrencia, no de reparación tardía. La atribución de función por cada diana no se ha adjudicado aquí.

## Qué cambia para nuestro proyecto

Existe evidencia funcional celular publicada más allá del ARN; nuestras matrices GEO no la reproducen ni la validan. El hueco discriminante es probar reversibilidad tras un déficit funcional documentado, con neuronas todavía viables. En las unidades revisadas no se ha verificado esa secuencia en las mismas unidades experimentales. Esto no demuestra que ningún estudio la haya realizado.

La siguiente tarea segura es recuperar la versión aceptada de Keuss por otra fuente pública autorizada y completar sus diagramas temporales/figuras. Después redactar una especificación falsable de rescate diferido: establecer basal funcional, documentar descenso sin pérdida celular, intervenir, repetir la misma medida y comparar controles temporales. Es una pregunta de colaboración, no un protocolo de laboratorio autorizado ni una recomendación clínica. La muerte neuronal, la regeneración axonal y la comunicación sináptica son desenlaces distintos.

## Calidad, incidencias y reproducción

Fuentes con XML descargado: PMC11230273 y PMC12424808, URL/SHA256/bytes en sources.json. Originales solo en caché, fuera de git; no se retuvieron tablas clínicas individuales en la entrega. Baughn se limita al resumen primario consultado por búsqueda; Keuss2026 al registro institucional (sin hash de un PDF que no se pudo obtener). No se inventan tamaños muestrales, efectos ni significación.

`python scripts/audit_functional_evidence.py` valida la matriz manual y produce TSV/JSON; no extrae automáticamente conclusiones científicas. `python -m unittest discover -s tests -v`: 41 pruebas offline pasan. Las nuevas pruebas impiden promover concurrencia a reversión tardía sin basal verificado, inferir eficacia clínica o duplicar unidades. Plan previo en research/plans/2026-10-29-functional-evidence.md.

Fuentes: https://pubmed.ncbi.nlm.nih.gov/36927019/ ; https://doi.org/10.1101/2024.06.20.599684 ; https://kclpure.kcl.ac.uk/portal/en/publications/unc13a-splice-correction-rescues-synaptic-dysfunction-induced-by-/ ; https://doi.org/10.1101/2025.08.28.672801 .
