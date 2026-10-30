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
