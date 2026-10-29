# Auditoría independiente de uniones compartidas — 2026-10-29

**Actualización posterior:** reports/junction-filter-reconciliation recupera el ZIP y explica21/1910por pérdida de exones en el parser consecutivo antiguo; no solo por filtros. Reproduce1910de catálogo y1901con soporte positivo. Mantener el texto siguiente como registro histórico; agrupación clínica corregida en reports/ALS_CI_metadata_correction_2026-10-29.md.

**Fuente:** GitHub Actions [run 40870655234](https://github.com/luisceb1/ela-research/actions/runs/40870655234), artifact id `12895277869`, ejecución completa con código `scripts/audit_shared_junctions.py` sobre 4 ficheros GEO.

## Resultados reproducidos en esta ejecución
- 10.347 modelos BambuTx cuantificados en cultivo, 19.196 en tejido.
- **1.910 uniones intrónicas exactas compartidas** entre ambos GTF, asociadas a **1.255 genes**, ausentes de los ENST internos de los dos GTF bajo este criterio amplio.
- El informe anterior `INFORME_CIENTIFICO.md` comunica **21 uniones / 20 genes** con otra selección previa. **NO son cantidades equivalentes**; hay que reconstruir los filtros originales antes de resolver su diferencia.
- Controles positivos de coincidencia exacta: MAP6D1 (`chr3:183822414-183825146 -`, `BambuTx9001 / BambuTx12784`) y ZNF317 (`chr19:9162961-9163054 +`, `BambuTx6904 / BambuTx2744`) presentes en la reconstrucción.
- Exploración descriptiva adicional sobre las 1.910: condición neuronal estricta (cero en ambos controles, ≥3 en KD con/sin 5Aza) arroja **9 uniones**, no una; criterio en tejido de ≥2 lecturas en al menos 2 columnas `ALS-ci` y cero en las 2 `CTL`: **32** uniones; **intersección = 0**. Este agrupamiento literal de columnas debe confirmarse con metadatos clínicos; el informe antiguo utiliza ALS-CI de forma distinta, por lo que no comparar los numeradores directamente.

## Incertidumbre que requiere atención
- El análisis es sobre **lecturas únicas asignadas a modelos de transcrito**, no sobre lecturas que crucen físicamente la unión.
- Un modelo BambuTx puede originar muchas uniones; una unión compartida no implica dos observaciones independientes, ni novedad frente a GENCODE completa.
- Una biblioteca por condición neuronal; no p-valores válidos entre condiciones.
- Los dos GEO proceden del mismo proyecto Bolger 2026; no validación intergrupo independiente.
- Es necesario auditar los filtros originales que redujeron 1910 a 21, los criterios de pertenencia de muestras clínicas y la exposición de artefactos antes de afirmar que la reproducción es exacta.
- El resultado **0 en la intersección estricta** se sostiene bajo este nuevo criterio, pero no equivale a probar ausencia de dianas biológicas.

## Decisión
No presentar ninguno de los 1.910 eventos como hallazgo nuevo. Próximo paso: contrastar conjunto de 21 eventos previo con lista de 1.910, documentar inclusión/exclusión, aplicar anotación GENCODE/RepeatMasker versionada y lecturas de unión; paralelamente mantener el diseño funcional de UNC13A como propuesta condicionada a revisión de laboratorio.
