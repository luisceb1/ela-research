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
