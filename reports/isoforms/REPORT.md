# Mapeo STMN2 / UNC13A — 2026-10-29

Evidencia: **exploratoria, estructura y cuantificación depositadas; sin validación de eventos crípticos**. Relacionado con #2; depende de la auditoría del PR #3.

## Evidencia

Se verificaron los símbolos/ENSG de STMN2, UNC13A, ACTB y GAPDH frente a `gene_name` de GENCODE v47, GRCh38 (Ensembl 113). El GTF oficial de referencia tiene 58.953.903 bytes comprimidos y SHA256 `df11938c66d2b39f8ebbdb5f1720919321f9cf9d58f02b019753f6a24ca3db24`. Fuente/versionado en `reference_source.json`; identidad exacta de los datos GEO en el manifiesto de auditoría.

| Serie | Gen | Transcritos en tabla/GTF | ENST / no ENST | Con cuenta única >0 en alguna biblioteca | Cadena exacta en GENCODE v47 |
|---|---|---:|---:|---:|---:|
| GSE310723 | STMN2 | 4 | 3 / 1 | 4 | 3 |
| GSE310723 | UNC13A | 7 | 7 / 0 | 3 | 7 |
| GSE315972 | STMN2 | 3 | 3 / 0 | 3 | 3 |
| GSE315972 | UNC13A | 7 | 7 / 0 | 3 | 7 |

El único transcrito no ENST asignado exactamente a las dianas es `GSE310723:BambuTx9249`, STMN2 (`ENSG00000104435.14`), chr8, hebra +, dos exones: **79.611.092–79.611.214** y **79.616.822–79.619.794** (GRCh38, coordenadas 1-based cerradas). Su unión conecta las bases exónicas 79.611.214 y 79.616.822. La cadena y la unión no están en GENCODE v47. Ambos exones son terminales en esta estructura: una búsqueda limitada a exones internos habría omitido el candidato.

| Biblioteca de cultivo | BambuTx9249 uniqueCount | ENST00000220876.12 uniqueCount |
|---|---:|---:|
| Ctrl + 5Aza | 4 | 162 |
| Ctrl sin 5Aza | 0 | 154 |
| TDP43KD + 5Aza | 10 | 22 |
| TDP43KD sin 5Aza | 24 | 34 |

Son **unidades de la matriz depositada**, no una afirmación sobre moléculas independientes. Las diferencias no tienen réplica biológica por condición y no se les atribuye significación estadística.

Se comparten exactamente tres cadenas STMN2 y siete UNC13A entre los GTF de las series; todas corresponden a ENST de referencia. **Compartir anotación no constituye replicación de expresión ni evidencia de un evento patológico**: algunos ENST tienen cero cuentas en todas las bibliotecas. La estructura BambuTx9249 no figura asignada a STMN2 en el GTF cerebral.

Control adicional de locus: dos transcritos asignados a otros genes solapan el intervalo de UNC13A en cada serie, ambos en la hebra opuesta. No aparecen otros transcritos de distinta asignación en la misma hebra solapando STMN2/UNC13A según este control. No se reasignaron por proximidad. Tabla: `other_gene_locus_overlaps.tsv`.

## Interpretación

El mapeo resuelve identificadores y estructura. El patrón de BambuTx9249 merece contrastarse con coordenadas independientes de eventos STMN2 y con soporte de lecturas/uniones; su falta de anotación no basta para denominarlo un exón críptico validado. La ausencia de isoformas UNC13A no anotadas en estos GTF es un resultado negativo de **este catálogo**, no una refutación de mecanismos conocidos ni prueba de ausencia en las muestras.

ACTB/GAPDH verifican enlace de símbolos/IDs y estructura bajo el mismo código; no se usan como genes cuya expresión deba ser estable. Las diferencias de hebra, exones terminales y coordenadas de unión son explícitas y tienen pruebas offline.

## Limitaciones y explicaciones alternativas

- Los GTF incluyen referencia aunque no haya expresión. Los ceros de uniqueCounts pueden reflejar ambigüedad, escasa profundidad, degradación o límites del descubrimiento; no se convierten en ausencias biológicas.
- La referencia externa aporta nombres y estructuras, pero fue la misma versión usada por el depositante: **no es una cohorte de validación independiente**.
- El control por locus solo examina intervalos de transcritos del catálogo, no BAM/FASTQ, soporte de empalme o regiones transcritas fuera de ese catálogo. Tampoco estima falsos negativos de bambu.
- No se ha contrastado una coordenada críptica publicada independiente, ni secuencia, poliadenilación, CDS, NMD, traducción o función. `cryptic_event_status` queda explícitamente no validado.
- `share_of_gene_unique_counts` es una cuota de cuentas asignadas; no es PSI. El ajuste por millón usa la suma de cuentas transcriptómicas depositadas; no es el CPM publicado y no se compara cuantitativamente entre cultivo y cerebro.
- No hay análisis de rescate molecular/funcional, tratamientos ni beneficio clínico.

## Reproducción e incidencias

`python scripts/geo_audit.py` seguido de `python scripts/map_isoforms.py`; pruebas: `python -m unittest discover -s tests -v` (25 pruebas al cerrar esta etapa). No requiere paquetes Python externos. `transcripts.tsv`, `exons.tsv`, `junctions.tsv`, `support.tsv`, `shared_full_chains.tsv` y `mapping_controls.tsv` son salidas del código, no tablas simuladas.

El primer intento se detuvo ante el atributo repetido `ont` de GENCODE. Se corrigió la lectura para permitir `tag`/`ont` repetidos, manteniendo rechazo de identidades contradictorias; se añadió prueba. La ejecución final terminó sin errores (`errors.json`). No se descartó el fallo previo: queda registrado aquí.

Criterio de cierre parcial: mapeo exacto y comparación estructural ejecutados; **pendientes revisión del PR y validación independiente de eventos crípticos**. Siguiente tarea segura: comparación descriptiva con `counts` y `uniqueCounts` separados y sensibilidad al denominador. Próxima prueba discriminante posterior: obtener coordenadas de eventos de una fuente primaria y verificar ensamblaje/hebra/soporte de unión. Abandonar la atribución específica si la unión no coincide o no tiene soporte suficiente.
