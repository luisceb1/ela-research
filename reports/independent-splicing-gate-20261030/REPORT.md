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


## Addendum: local group summary reported by user (2026-10-30)

Execution: `py scripts/rimod_unc13a_group_summary.py` against locally downloaded RiMOD ZIP; author metadata SHA256 `40b246f817835b0db6453c5ce348d7590df185692a4998bdc1dd3c86c060c4b5`; 4127 real chr19 Parquets, 47 joined sample IDs (16 control, 11 MAPT, 13 C9orf72, 7 GRN). **Reported stdout, not independently re-executed here.**

| Event | Control n=16 positive; counts | MAPT n=11 positive; counts | C9orf72 n=13 positive; counts | GRN n=7 positive; counts |
|---|---|---|---|---|
| canonical | 16; 2771 | 11; 1247 | 13; 2268 | 7; 788 |
| cryptic_1 | 0; 0 | 0; 0 | 9; 42 | 7; 38 |
| cryptic_2 | 0; 0 | 0; 0 | 8; 33 | 5; 20 |
| cryptic_long | 0; 0 | 0; 0 | 4; 18 | 4; 5 |

Total per event: canonical 7074, cryptic_1 80, cryptic_2 53, cryptic_long 23. No metadata IDs or patient-level counts exported in this report. Positive means `junction_count > 0`, not proven CE expression, severity, nor per-transcript abundance.

**Observation:** these candidate junctions have positive counts in C9orf72/GRN and no positives among 27 control/MAPT samples; this is a selected, previously published cohort comparison, **not** external independent replication or newly validated diagnostic specificity. Do not equate genotype grouping with independently measured TDP43 pathology or infer ALS-specific clinical implications.

**Next gates, before tests, PSI or claims:** verify strand/reference/coordinate offset and assignment to exact UNC13A canonical/CE events; establish whether cryptic_1 and cryptic_2 represent two junctions of the same transcript (avoid counting molecules twice); document sample-level total junction depth, QC, coverages, tissue source and cluster definition; create threshold sensitivity summaries (e.g. count >=1/3/5) and controls. Keep group statistics descriptive until analysis plan and biological units are properly established.


## Addendum: local threshold QC results — 2026-10-30

User-reported execution of `scripts/rimod_unc13a_threshold_qc.py`: 47 samples, 4,127 chr19 Parquets. All four queried junctions have the same LeafCutter cluster identifier `clu_46643_-`. This does **not** by itself certify precise event annotations or independent transcript molecules.

Positives among combined C9orf72+GRN (n=20); all three queried cryptic candidates remain 0/27 in combined control+MAPT at thresholds >=1, >=3 and >=5:

| Candidate | >=1 | >=3 | >=5 |
|---|---:|---:|---:|
| cryptic_1 | 16 | 11 | 7 |
| cryptic_2 | 13 | 8 | 3 |
| cryptic_long | 8 | 2 | 2 |

In C9orf72+GRN, 17/20 have at least one of three positive at >=1; 12/20 have cryptic_1 and cryptic_2 simultaneously; 6/20 have all three. In control+MAPT all these co-occurrence summaries are zero. These thresholds were chosen for exploratory robustness, not prevalidated clinical classification. Coverage attenuation is strong: only 7/20 have cryptic_1 >=5, for example. Reported counts are the user's local output, **not independently run or audited against raw reads in this session**.

Next mandatory scientific QC before interpretation: confirm assembly and LeafCutter end-point convention; determine whether canonical and CE junctions share a mathematically suitable denominator (cluster_count is not automatically PSI); sensitivity of the result to sequencing depth, RIN, tissue composition and batch; assess individual-metadata restrictions and avoid publishing row-level donor output. No p values, causal inference, ALS extrapolation, independent replication or biomarker performance claim.


## Addendum: local UNC13A denominator/depth audit — 2026-10-30

User-reported run of `scripts/rimod_unc13a_depth_qc.py`: 47/47 joined samples, 4,127 chr19 Parquets; all four target junctions share cluster `clu_46643_-` and the same `cluster_count` for each sample (0 inconsistent, 0 zero-denominator). This supports consistent computation of per-junction `junction_count/cluster_count` as in the authors' workflow; it does not validate exact transcript identities or absolute PSI.

| Minimum cluster_count | Comparison N / cryptic_1 >=1 | C9orf72+GRN N / cryptic_1 >=1 |
|---|---|---|
| 0 | 27 / 0 | 20 / 16 |
| 20 | 26 / 0 | 20 / 16 |
| 50 | 25 / 0 | 20 / 16 |
| 100 | 23 / 0 | 15 / 12 |

Cluster depth median: comparators 129 (range 4–288), FTLD-TDP genotype proxy 148 (range 67–366). RIN median: comparators 7.1, FTLD-TDP proxy 6.4; all 47 RIN values reported as available. Per-junction ratio medians in FTLD-TDP: canonical 0.97, cryptic_1 0.019, cryptic_2 0.0119, cryptic_long 0; in comparators 1, 0, 0, 0. These are unadjusted descriptive summaries, and QC filters are exploratory.

**Open limitations:** nonrandom RIN differences require a stratified/confounding sensitivity analysis; confirm genomic reference and event transcript annotation; genotype is not per-sample direct pathology assessment; no independent validation; 47 donors/47 libraries assumed one each only pending provenance. Do not claim diagnostic accuracy or causal TDP-43 effect.


## Addendum: RiMOD RIN-stratified UNC13A sensitivity (user-reported local run, 2026-10-30)

`scripts/rimod_unc13a_rin_strata.py` completed with n=47. Outcome: candidate `cryptic_1`, minimum 1 count, grouped by RIN:

| RIN stratum | FTLD-TDP genotype proxy | Control/MAPT comparator |
|---|---|---|
| <6.5 | 8/11 | 0/5 |
| 6.5–<7.5 | 7/7 | 0/9 |
| >=7.5 | 1/2 | 0/13 |

At local cluster depth >=100 in the intermediate RIN stratum: FTLD-TDP proxy 6/6 vs comparators 0/6, minimum 1 count; >=3 counts 5/6 vs 0/6; >=5 counts 3/6 vs 0/6. Source: user-provided stdout; not independently reproduced in this assistant environment. The high-RIN FTLD-TDP stratum has n=2 and is underpowered. Bands and read thresholds exploratory; they do not establish RIN adjustment or eliminate library/tissue/cell composition confounders. No claim of biomarker specificity, causal molecular rescue, ALS cohort replication or original discovery.

Immediate scientific gate: confirm exact donor-level identity/region of each UNC13A splice junction in author event table and the genomic assembly/conventions; then consider a pre-specified matched/adjusted sensitivity, and external ALS data.


## Addendum — direct original-author UNC13A event annotation checked (2026-10-30)

At Fratta Lab `cryptic_biology` pinned commit `80fa3d70418a4665a85d414e33c7c470a9312086`:
- `data/compendium_cryptics.csv` explicitly labels `UNC13A,chr19:17641556-17642414` **novel_donor**, strand minus; and `UNC13A,chr19:17642541-17642845` **novel_acceptor**, strand minus, across multiple experimental entries.
- `data/noDox-dox0075.cryptic_exons.bed` has `chr19 17642413 17642541 UNC13A|chr19:17641556-17642414 0 -`, corroborating an author-annotated putative cryptic exon interval.
- `data/all_events.closest_tdp_bind.bed` independently lists `chr19 17641556 17642414` donor and `chr19 17642541 17642845` acceptor, both `Early` and `-` strand.
- The long variant `chr19:17642591-17642845` **does not exactly match** the `chr19:17642592-17642844` candidate in `compendium_cryptics.csv`; do not assert verified identity for this alternate junction pending coordinate convention assessment. The canonical junction is a local cluster comparator, not a cryptic event from these author tables.
- This is **source-to-source annotation corroboration**, not independent biological validation or a new molecular finding. Human assembly and 0/1-based endpoint conventions still require complete verification.

Next: inventory NYGC public ZIP using `scripts/nygc_zip_inventory.py` without decompressing. Examine chr19 partition, Parquet schema and sample-to-tissue/pathology metadata before computing any NYGC junction comparison. NYGC is separately labelled as cohort but sample provenance, overlapping donors, brain region and ALS/non-ALS strata must be audited.


## Addendum — NYGC local UNC13A molecular scan (user-reported, 2026-10-30)

User ran `scripts/nygc_unc13a_scan.py` against `nygc_parquets.zip`: 3548 Parquets scanned; 1 file contained queried chr19 interval; 12,380 region records (5 distinct candidate junctions x 2,476 sample IDs). Four preselected junctions: canonical candidate 2,476 records / 2,476 positive / total 250,272 reads; `17641556-17642414` 2,476 records / 153 positive / total 254; `17642541-17642845` 2,476 records / 129 positive / total 202; `17642591-17642845` 2,476 records / 114 positive / total 144. All belong to local NYGC cluster `clu_179275` (-). Additional `17641556-17642557`: 2,476 records; not yet interpreted. Here a positive means nonzero counts, NOT a demonstrated event in 2,476 donors.

This reproduces **coordinates with read support in a distinct public dataset**, not yet a group association or external **biological** replication: absence of matched clinical pathology/tissue/sample independence prevents that claim. RiMOD group data and NYGC data must not be treated as comparable cohorts before technical, donor and tissue metadata checks.

Pinned Fratta Lab author file `data/metadta_nygc.csv` contains `sample`, `tdp_proteinopathy`, `rna_tissue_source_simplified`, `external_subject_id`, `rin` and other metadata. New `scripts/nygc_unc13a_metadata_audit.py` joins exact sample IDs, groups by region and TDP-43 pathology, reports unique donor-ID counts and aggregate nonzero junctions; suppresses event counts for N<5 groups. Still needs local execution. Pay attention to multiple tissues from a single donor and provenance/overlap. The original source itself groups observations by tissue and pathology; do not call data independent biological confirmation until cohort identity is verified.


## NYGC donor-deduplicated motor cortex QC (user-provided local stdout, 2026-11-01)

Ran `scripts/nygc_unc13a_donor_qc.py`: 515 cortex-motor sample records selected by pathology and joined metadata; 361 donor IDs (313 ALS-TDP, 48 control); 154 additional library records removed by selecting the maximum local cluster depth per donor without using the cryptic outcome; zero missing donor IDs in this subset. **Source: user-reported stdout, not an independent execution in this environment.** Donor IDs are proxies from the author metadata and require independent provenance review.

| Cluster depth minimum | ALS-TDP donors: donor-junction positive / N | Control donors: positive / N | ALS-TDP acceptor-junction positive / N |
|---|---|---|---|
| 0 | 33/313 | 0/48 | 27/313 |
| 50 | 33/301 | 0/45 | 25/301 |
| 100 | 26/244 | 0/38 | 22/244 |

RIN sensitivity for donor junction at depth >=100: RIN<6.5: ALS-TDP 14/93 vs Control 0/21; RIN 6.5–<7.5: ALS-TDP 7/77 vs Control 0/7; RIN>=7.5: ALS-TDP 4/55 vs Control 0/3. Groups are imbalanced; a higher RIN is associated with sparse control samples. Donor-level RIN missing at all-depth: ALS-TDP 31/313, Control 9/48. Median cluster depths at all-depth ALS-TDP 130 and Control 143.5. **This is not a fully adjusted association or estimated biomarker accuracy.**

Next decision: stop running unplanned repeated sensitivity filters on the same cohort; verify source pipeline/genome build, the 313 unmatched metadata IDs from broader NYGC scan, donor overlap and anatomical classifications; compare directly with original author analysis and choose a preregistered independent validation question. Risk: multiple tissues per donor, source-specific batch/RIN/cell composition and biological non-independence of reanalysed author data.
