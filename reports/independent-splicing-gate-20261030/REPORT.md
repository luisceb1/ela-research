# Gate de replicación independiente STMN2/UNC13A — 2026-10-30

## Objetivo y decisión
Pregunta prospectiva conforme a research/NEXT_STUDY_GATE.md: ¿se incrementa el soporte de una unión críptica **predefinida** STMN2 o UNC13A con pérdida de función nuclear de TDP-43, respecto a una unión canónica comparable, entre unidades biológicas independientes?

**Resultado de este ciclo: ninguna fuente aceptada todavía para el contraste de uniones.** Se ha auditado metadato GEO/publicación, no descargado ni contado lecturas FASTQ/BAM/CRAM, no estimado efectos, ni ejecutado un experimento funcional. Se exige nueva verificación de dependencia y archivos antes de iniciar procesamiento pesado. Los tres registros corresponden a **dos estudios**; las modalidades GSE290436/GSE290441 no son cohortes independientes.

## Candidatos y puerta de entrada

| Registro | Diseño público verificado | Datos accesibles | Dependencia / principal bloqueo | Gate |
|---|---|---|---|---|
| GSE304550, PRJNA1301730 | 16 bibliotecas de motoneuronas iPSC: scramble, siTDP43, siUPF1, doble KD; dos batches con dos repeticiones etiquetadas por condición/batch; 4 control y 4 siTDP43 | Tabla procesada `GSE304550_MN-samples-counts-processed.txt.gz` (cuentas génicas); lecturas en SRA; PE150 y STAR / GENCODE v38, GRCh38 indicados para una GSM | No hay cuentas explícitas de uniones crípticas/canónicas en tabla; no está verificado que 2 reps por batch sean diferenciaciones independientes, ni la profundidad para el evento. No inferir n=4 biológico | **No aceptado aún**; apto para auditar métodos/SRA |
| GSE290436, PRJNA1228024 | 14 bibliotecas Illumina de motoneuronas iPSC con TDP43 nuclear vs relocalizado; E5/E8 y AAVS1, diferentes diseños que no deben agruparse automáticamente | Dos matrices de cuentas por gen; lecturas en SRA; estudio eLife 2025 | Falta mapa unidad→línea→diferenciación→tratamiento; no hay cuentas de uniones en tablas. No es perturbación idéntica a siTDP43 | **No aceptado aún** |
| GSE290441, PRJNA1228031 | 8 bibliotecas Nanopore E5/E8 del **mismo estudio** GSE290436 | `GSE290441_tdp43_all_chr.counts.tsv.gz` (cuentas génicas); lecturas SRA; minimap2/FLAIR y hg19 documentados en GSM8812855 | Misma familia experimental que GSE290436, no réplica externa; 2 R por brazo/línea con independencia por resolver; cambio de referencia hg19 vs GRCh38 | **No aceptado como fuente independiente**; solo complemento estructural |

GSE304550 fuente primaria https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304550 ; descripción de GSM https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9152781 ; artículo https://pmc.ncbi.nlm.nih.gov/articles/PMC12704819/ . La publicación informa diferentes cifras de diferenciaciones independientes para diferentes figuras; **no** transferirlas automáticamente al conjunto RNAseq depositado.

GSE290436 https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE290436 ; GSE290441 https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE290441 ; metadata de muestra ONT https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8812855 ; artículo https://elifesciences.org/articles/95062v1 . El artículo declara conjuntamente las accesiones y no deben contarse como evidencias independientes.

## Auditoría pendiente y criterio de aceptación
1. Recuperar manifest SRA/ENA para bibliotecas candidatas, acceso y tamaño; comprobar los metadatos de cada GSM/SRX y la relación explícita entre diferenciación, lote, pozo y biblioteca. Verificar solapamiento entre fuentes/autores y con datos ya revisados en este repositorio.
2. Buscar archivos públicos **de junction counts** y definiciones inequívocas de evento antes de programar alineamientos. Las tablas localizadas son de cuentas **a nivel gen**, inadecuadas para el objetivo. Fijar evento, referencia, hebra, coordenadas, comparador canónico y versionado previamente a inspeccionar efectos.
3. Comprobar >=3 **unidades biológicas independientes por condición** según el criterio prospectivo de NEXT_STUDY_GATE; no equiparar los cuatro GSM etiquetados control y cuatro TDPkd a n=4 biológico. Determinar covariables de lote y control de KD de TDP-43.
4. Solo tras aceptar fuente y definir coste computacional, autorizar pipeline de lecturas; separar QC técnico, soporte por lectura y contrastes por unidad. Ceros reales distintos de eventos no evaluables; no llamar PSI a una razón de cuentas sin justificación de geometría. Controles negativos y criterios de fracaso prospectivos.

## Resultado utilizable
Este ciclo aporta **inventario y rechazo de aceptación prematura**, no replicación biológica. GSE304550 queda como primer candidato para aclarar el mapa de diferenciaciones; si no cumple, evaluar GSE290436 sin contar GSE290441 como cohorte adicional. Si ninguno cumple, detener el ciclo y replantear vía de acceso a cuentas de uniones/lecturas. No se han hecho descargas de gran volumen, cambios de `main`, comunicaciones ni gastos.


## Addendum: verificación directa de publicación primaria y tamaño — 30/10/2026

La inspección de GEO GSE304550, BioProject PRJNA1301730 y del texto completo de Alessandrini et al. (*Neuron* 2026, doi:10.1016/j.neuron.2025.11.001; PMC12704819) matiza el inventario inicial:

- GEO enumera exactamente GSM9152768–GSM9152783; por cada uno de los 2 lotes hay 2 bibliotecas etiquetadas como réplicas para scramble, TDP43 KD, UPF1 KD y doble KD. Las etiquetas **no** demuestran cuatro diferenciaciones independientes por brazo.
- La publicación describe el análisis de uniones diferenciales con **MAJIQ**, presenta Sashimi de **UNC13A críptico** en Fig. 5F y medidas **RT-qPCR de UNC13A-CE y STMN2-CE** en Fig. 5H. Esas alteraciones ya fueron examinadas por los autores: una reproducción propia no constituye novedad biológica.
- Fig. 5 declara para varios paneles **4 réplicas biológicas de 2 diferenciaciones independientes**. La leyenda no permite trasladar automáticamente esta unidad a cada archivo GSM, pero impide tratar provisionalmente las 4 bibliotecas/condición como >=3 diferenciaciones independientes. El gate de independencia **continúa sin superar**.
- BioProject refiere **16 experimentos SRA, 355 Gbases y 0,11 TB** totales. No descargar el proyecto completo ni procesar lecturas crudas sin plan de almacenamiento y necesidad concreta de cuantificar las uniones.
- El archivo suplementario de GEO es de **cuentas a nivel gen**, no una matriz verificable de uniones. Identificar primero si los suplementarios de la publicación contienen salidas MAJIQ, definiciones de eventos y cuentas por biblioteca; una figura de Sashimi no sustituye una matriz.
- GSE304550 es apropiado como **reproducción técnica/control positivo**, pero bajo la regla vigente de >=3 unidades independientes por condición **no se acepta aún como fuente inferencial**. El objetivo de replicación externa debe buscar otra unidad biológica o precisar y revisar prospectivamente el umbral; nunca relajar el umbral tras ver un efecto favorable.

Referencias verificadas: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304550 ; https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1301730 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12704819/ (Fig. 5 y leyenda). Esto es auditoría documental, no reanálisis cuantitativo.


## Addendum: comprobación de los seis suplementos del artículo — 30/10/2026

Fuente primaria revisada: https://pmc.ncbi.nlm.nih.gov/articles/PMC12704819/ (sección **Supplementary Material**, **Splicing analysis** y **Data and Code Availability**).

Se enumeran seis anexos tabulares/PDF científicos y una tabla adicional de tejido post mortem: suplemento 1 PDF figuras S1–S9; Table S1 UPF1 targets; Table S2 GO UPF1; Table S3 **APA** TDP43 KD; Table S4 **APA** UPF1 KD/pacientes; Table S5 primers qPCR/ASO; Table S6 información de tejido de pacientes. **Ninguno está identificado por los autores como exportación MAJIQ/VOILA con cuentas por biblioteca, coordenadas y uniones críptica/canónica.** Esto se basa en índice y descripciones publicados; los XLSX no pudieron leerse íntegramente en esta revisión debido al acceso intermitente de PMC (redirección/recaptcha). No afirmar inspección exhaustiva del contenido interno.

El manuscrito especifica MAJIQ `v2.4.dev102+g2cae150`, `majiq build --min-intronic-cov 1 --simplify`, `majiq deltapsi`; VOILA view `--threshold 0.1 --probability-threshold 0.95`. Los resultados MAJIQ en figura 5A/F y RT-qPCR figura 5H **no constituyen cuentas de unión descargables**. Data and Code Availability enumera GEO GSE304547, GSE304548, GSE304550, pero no archivo de salidas MAJIQ ni repositorio de código de splicing verificable en ese apartado.

**Decisión tras esta comprobación:** No hay archivo MAJIQ de cuentas/eventos verificado entre los suplementos descritos y GEO disponible. Persisten la falta de mapa biblioteca→diferenciación y la imposibilidad de convertir cuatro bibliotecas/condición en cuatro unidades independientes. **No ejecutar inferencia de splicing sobre estas tablas de genes**. Próxima verificación acotada: comprobar un manifiesto de SRA y disponibilidad de BAM/junction outputs sin descarga masiva, o buscar una fuente alternativa precomputada. No contactar autores ni inferir un resultado nuevo.


## Addendum: RiMOD sample metadata located and group-level extractor — 30/10/2026

Primary author repository: https://github.com/frattalab/cryptic_biology/blob/80fa3d70418a4665a85d414e33c7c470a9312086/data/metadata_rimod.csv ; use alongside `preprocessing_rimod.Rmd` and `burden_analyses.R` at the same commit. This file maps `rimodN` to published `genotype` and contains sample-level demographic and sequencing fields. **Do not commit/emit patient-level metadata or individual count tables.**

In the author's table: control 16, MAPT 11, C9orf72 13 and GRN 7; total 47 RNAseq entries. Authors generally compare GRN/C9orf72 as FTLD-TDP against control/MAPT comparators, but genotype is a proxy for expected pathology and does not establish pathology in an individual. All samples are post mortem FTLD/control, not an ALS cohort.

User's local ZIP integrity CRC passed; an exploratory extraction at **candidate** UNC13A GRCh38 coordinates reports: canonical 7074 total, 47 positive samples; three candidate cryptic junctions 80/53/23, positive in 16/13/8. There are 188 unique sample-junction records, no duplicate keys or invalid counts. These counts were **reported by the user** from their local execution and have not been reproduced inside the GitHub execution environment or cross-checked with genomic reference conventions. No genotype comparison or significance computed yet.

New script `scripts/rimod_unc13a_group_summary.py` locally fetches the version-pinned author metadata to ignored `data/external`, validates exact sample-ID match and 4 events per sample, and **prints only aggregate group summaries**. Require running and reviewing stdout before claiming a group association. No normalization, PSI, p value, model, biological validation or newly discovered UNC13A event claimed. The author repository already interrogated cryptic burden; this is a reproducible technical extension/comparison of published data.

Next safeguards: verify precise LeafCutter coordinate convention and exact UNC13A CE identity in author event reference, check whether same splicing branch is assigned distinct clusters, and validate sample-level sequencing depth / RIN, tissue region, genotype/pathology grouping before drawing associations. Any downstream inferred statistic needs preregistered numerator, denominator and independent units; avoid publishing row-level donor data.
