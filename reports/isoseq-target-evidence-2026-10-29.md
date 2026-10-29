# Resultado Iso-Seq STMN2/UNC13A con datos GEO reales — 2026-10-29

## Procedencia técnica
- [GitHub Actions run 40870066862](https://github.com/luisceb1/ela-research/actions/runs/40870066862): **success**. Artefacto `geo-isoseq-audit` id 12896240123, descargado e inspeccionado.
- Entrada GSE310723: GEO uniqueCounts + extended_annotations.gtf.gz, 392871 filas; 4 condiciones experimentales **sin réplicas independientes por condición**.
- Entrada GSE315972: GEO uniqueCounts + extended_annotations.gtf.gz, 401720 filas; 8 muestras.
- GTF sin `gene_name`; se resolvieron genes por identificadores estables ENSG00000104435 (STMN2) y ENSG00000130477 (UNC13A).
- Cobertura TXNAME/GTF 100% dentro de estas tablas; conflictos GENEID = 0.
- Transcritos objetivo: 11 en i3N (STMN2 4, UNC13A 7); 10 en cerebro humano (STMN2 3, UNC13A 7).
- Los resultados por biblioteca están en el ZIP del run; no es lícito usar recuentos sumados entre condiciones para inferencia.

## Evento STMN2 BambuTx9249 (GRCh38; GTF de GSE310723)
- 2 exones: `chr8:79611092-79611214`, `chr8:79616822-79619794`. Uniones y clasificación necesitan evaluación específica con BAM y anotación externa.
- Recuentos de lecturas **únicas asignadas al transcrito**, no lecturas independientes que crucen la unión:

| Condición | BambuTx9249 | ENST00000220876.12 (STMN2 referencia en este conjunto) |
|---|---:|---:|
| Control sin 5Aza | 0 | 154 |
| TDP43KD sin 5Aza | 24 | 34 |
| Control + 5Aza | 4 | 162 |
| TDP43KD + 5Aza | 10 | 22 |

- Los tres modelos ENST de STMN2 incluidos en el GTF presentan estructuras exónicas distintas del modelo BambuTx9249; en concreto, ninguna tiene como segundo exón `chr8:79616822-79619794`. Es una diferencia **respecto a las anotaciones internas**; no certifica novedad frente a GENCODE completa, ni identidad molecular precisa con el exón críptico STMN2 publicado.
- GSE315972: el ID BambuTx9249 no aparece entre los modelos de STMN2 cuantificados. No implica ausencia del evento en cerebro (distinto procesamiento, profundidad, cohortes, anotación y nomenclatura BambuTx).
- El cambio 0→24 en cultivo sin 5Aza es descriptivamente compatible con dependencia de TDP-43, **pero una columna por condición impide estimación estadística de replicación biológica**. En +5Aza 4→10, también aumenta; la azacitidina es un factor de confusión experimental y no una réplica.
- Las lecturas están asignadas a transcrito; confirmación de unión requiere inspeccionar lecturas de empalme de BAM o evidencias de alineamiento.
- El fenómeno STMN2 críptico asociado a pérdida nuclear TDP-43 ya es conocido; **no anunciar descubrimiento nuevo**.

## UNC13A
- Siete isoformas ENST identificadas en ambos conjuntos. Por ejemplo ENST00000519716.7: cultivo [56,28,50,40] orden Ctrl+5Aza, Ctrl-noAza, KD+5Aza, KD-noAza. Tejido [46,46,48,68,34,54,82,86] según columnas del artefacto.
- No identificar indebidamente el mecanismo críptico de UNC13A por expresión total de una isoforma canónica. Requiere cuantificación específica de uniones crípticas.

## Próximo experimento computacional
1. Contrastar las coordenadas BambuTx9249 con el exón críptico / poliadenilación prematura de STMN2 publicados, GRCh38, y GENCODE versionada.
2. Verificar lecturas que atraviesan las uniones, calidad, cobertura, longitud del transcrito y orientación en BAM.
3. Validar contra muestras independientes, controles adecuados y profundidad; sin esto no inferir efecto biomédico.
4. Priorizar `UNC13A` como pregunta funcional externa posdéficit confirmado, sin concluir eficacia terapéutica del simulador.

## Contraste directo con literatura primaria — corrección de originalidad
El artículo Melamed et al. 2019 identifica **exón críptico STMN2 2a** en GRCh38 en `chr8:79616822-79617048`, dentro del segundo exón del modelo BambuTx9249 (`79616822-79619794`). Más importante aún, un estudio independiente de análisis cerebral (Molecular Neurodegeneration, 2025, DOI 10.1186/s13024-025-00820-5) señala expresamente la unión críptica `chr8:79611214:79616822`. **La frontera exónica exacta coincide con nuestro modelo BambuTx9249: exón 1 termina en 79611214 y exón 2 inicia en 79616822.**

Por ello este evento es **compatible con la unión críptica conocida de STMN2**, no con una unión nueva. El modelo BambuTx9249 termina más lejos que el exón 2a de 227 nucleótidos publicado; las diferencias de final 3' pueden reflejar anotación de extremos, lecturas incompletas o procesamiento alternativo. No afirmar que se ha demostrado una poliadenilación idéntica sin inspección de lecturas y extremo 3'.

Fuentes primarias:
- Melamed et al., 2019, *Nature Neuroscience*: https://pmc.ncbi.nlm.nih.gov/articles/PMC6348009/
- Estudio multirregional 2025, *Molecular Neurodegeneration*: https://doi.org/10.1186/s13024-025-00820-5

**Decisión:** BambuTx9249 es control positivo de detección del mecanismo STMN2 previamente publicado, **no candidato novedoso**. El valor operativo es validar el pipeline; priorizar hallazgos que superen comparación con referencias externas y cohortes independientes.
