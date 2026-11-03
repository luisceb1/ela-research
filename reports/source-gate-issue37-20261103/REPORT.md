# Issue #37: selección acotada y anotación independiente — 03/11/2026

## Decisión

**Tres familias revisadas; ninguna aceptada para el contraste completo de uniones UNC13A. Ciclo cerrado, sin cuarto candidato.** Se obtiene además una aclaración real de anotación: una de las dos uniones unitarias no contenidas en la caché GENCODE aparece exactamente en RefSeq. No es un descubrimiento nuevo ni habilita otro piloto.

Base inspeccionada: main `9076802fa78bfd1e4cdc97a3b92dd24a06d054c4`, merge de #36 confirmado por el ref de main. Se leyeron AGENTS, STATE, BACKLOG, PROTOCOL, NEXT_STUDY_GATE, issue #37 sin comentarios y los informes de cierre/selección anteriores. Lista fijada **antes de recuperar las nuevas fuentes**, en PLAN.json, commit `a62a0d78541b1226907314168d02bdc9ad5af931`. Los tres artículos ya se conocían bibliográficamente: lo nuevo es esta auditoría de acceso a sus datos, no su descubrimiento.

Pregunta: ¿alguna familia aporta cuentas directas de las uniones canónica/crípticas por biblioteca, o alineamientos procesados accesibles, con coordenadas verificables y al menos tres unidades biológicas independientes por condición? La predicción de disponibilidad no se cumple. Un archivo no verificado no equivale a un cero molecular ni a inexistencia universal de datos.

## Tabla de aceptación/rechazo

Tabla exportable completa: `candidate_decisions.tsv`. Evidencia primaria, versiones, archivos realmente enumerados, hashes y localizadores: `sources.json` (S1–S10).

| Familia | Medición/archivos comprobados | Coordenadas y cobertura disponible | Condiciones, unidades y lotes | Dependencia y decisión |
|---|---|---|---|---|
| Seddighi 2024 — S1–S4 | El artículo remite RNA-seq/Ribo-seq a AD Workbench. Zenodo 10479046 es **software v1**, ZIP 8.083.304 B no descargado. Árbol Git completo y README inspeccionados; incluye matriz **génica** de 7.219.943 B no leída. Ningún BAM/BAI o matriz de cuentas de uniones verificado | README requiere BAM/BAI y `all_bams.tsv` del usuario; utiliza GRCh38.p13, GENCODE v38 y Ensembl 103. No se validó geometría de un archivo de cuentas ni cobertura objetivo. **Desconocida, no cero** | Cultivos control/KD de TDP-43 en descripción del pipeline; sin mapa verificable biblioteca→línea→diferenciación→lote. El ejemplo de 18 BAM no acredita 18 unidades. Perturbación por biblioteca no auditada | Solapamiento de unidades con otras fuentes desconocido; autores o artículos distintos no lo resuelven. **Rechazada para iniciar contraste; acceso bloqueado** |
| Irwin 2024 — S5–S6 | Disponibilidad remite RNA-seq a SRP166282 y SRP057819; NAUC/ASCOT mide expresión. El índice de Source Data describe inmunoblots/geles. No matriz nueva de uniones ni BAM accesible verificado | Visualización GRCh38 no basta para validar cuentas críptica/canónica. Cobertura objetivo no comprobada; sin convertir NAUC en soporte de uniones | Dataset neuronal remite a Klim 2019, ya auditado. SRA enumera 18 registros técnicos de esa serie; no se reconstruyen nuevas unidades/lotes desde sus sufijos. No se accede a Supplementary Data 1, identificado como datos de participantes | **Rechazada como nueva réplica neuronal independiente**: reutiliza Klim. SRP057819 corresponde al trabajo HeLa de Ling 2015, no a una tercera fuente neuronal nueva; no se abre como cuarto candidato |
| Baughn 2023 — S7 | Disponibilidad remite al manuscrito/suplemento y acuerdos de materiales. No se enlaza en esa sección una matriz de uniones/BAM o accession RNA-seq utilizable para UNC13A. Índice: DOCX 7,5 MB; no descargado | No hay ensamblaje/convención/cobertura de una tabla UNC13A comprobada en los materiales inspeccionados | Fig. 3 documenta cultivos diferenciados y tratados independientes en otros ensayos. No trasladar ese n al RNA-seq UNC13A. Mapa de bibliotecas y lotes no disponible para este contraste | **Rechazada por falta de medición directa verificable**. No se reevalúa rescate STMN2 ni se afirma que el estudio carezca de otros datos no inspeccionados |

La puerta inicial sigue exigiendo ≥3 unidades independientes por condición. No declaramos que los autores tengan pseudorreplicación: no hemos podido reconstruir la unidad para el contraste propuesto. Cobertura mínima de 20 grupos del contrato local no certificada en ninguna candidata; otras herramientas contarían lecturas/uniones con filtros diferentes y exigirían justificar su equivalencia.

## Acceso, presupuesto y límites de inspección

- **Seddighi:** AD Workbench devolvió solo la página que exige JavaScript; no un manifiesto. Eso no demuestra que requiera autenticación o que no existan alineamientos. El árbol Git v1 está completo, SHA de árbol `8a1606bef9e1637c745828e997f3f39e79342129`; README blob `fb06f63d1d410645ce12b043b694be0e07cb2ead`. No se ejecutó código ajeno. Los ≈180 GB/120 GB RAM/≈2 días del README son un ejemplo de los autores para su pipeline completo con 18 BAM, **no presupuesto medido o necesario para nuestro análisis estrecho**. El tamaño real accesible del depósito y el coste de una extracción regional son desconocidos. No descargar el ZIP para suplir datos ausentes.
- **Irwin:** reutilizar la serie neuronal no añade independencia; gasto futuro aceptado en este ciclo: ninguno. La corrección `10.1038/s41591-024-02966-z` cambia el primer HDG F del método RT-PCR; se comprobó su texto mediante Scite. No es una retractación ni un nuevo archivo de uniones. No se descargaron datos de participantes.
- **Baughn:** sin archivo directo verificado no se puede estimar almacenamiento o cómputo útil. No se descarga el suplemento de 7,5 MB dentro de esta revisión. No se afirma haber leído su contenido interno.

Scite `search_literature` confirmó las tres referencias. `editorialNotices` muestra la corrección de Irwin; el campo no se devolvió para Seddighi/Baughn, por lo que su ausencia de avisos **no queda certificada**. Se usaron extractos y Smart Citations para localizar reutilización/ensayos, sin convertir sus etiquetas automáticas en evaluación de calidad. Lectura lineal parcial Baughn: `source=fulltext`; no lectura completa en este ciclo. Seddighi final: `contentDenied=true` en Scite, y el enlace OA lleva al preprint; no se atribuye ese preprint al texto final.

Se conservan recibos de las recuperaciones Python y el registro de búsquedas/accesos en `retrievals.json`/`SEARCH_LOG.md`. Límites de cuerpo aplicados a solicitudes Python; los conectores no exponen bytes de transporte y no se inventa un cargo global para ellos. Cero FASTQ/BAM/BAI, datos individuales clínicos, contactos, costes o nuevos alineamientos. Los 7.322.807.977 bytes históricos del piloto siguen intactos y separados de estos pequeños metadatos públicos.

## Contraste con RefSeq: resultado ejecutado

Se consulta el locus **completo** chr19:[17600000,17690000), hg38, pista NCBI RefSeq `ncbiRefSeq`, release `GCF_000001405.40-RS_2025_08`, actualización UCSC 13/08/2025. Respuesta de 8.358 B, SHA256 `ec28d8d0bdf2fd6352ede23be272f05a2a1cc1c891a4873ae93f99573ccc9c1a`, conservada en `inputs/refseq-hg38.json`. Siete transcritos UNC13A, 49 uniones distintas. Comparación exacta de ambos extremos/cromosoma/hebra contra el **inventario sellado completo ya existente**; sin modificar coordenadas, recuentos, prefijo o filtros.

| Anclaje | Uniones del inventario cerrado | Coincidencias GENCODE cacheada (histórico) | Coincidencias RefSeq | Sin coincidencia exacta RefSeq |
|---|---:|---:|---:|---:|
| 15 | 31 | 29 | 30 | 1 |
| 8 | 33 | 31 | 32 | 1 |

| Unión intrónica, base cero/semiabierta, chr19 hebra − | Soporte 15/8 | Resultado nuevo de anotación |
|---|---:|---|
| 17627940–17629242 | 1/1 | Coincidencia exacta en **NM_001387022.1** (RefSeq curado) y **XM_017026502.2** (predicho) |
| 17648988–17649507 | 1/1 | Sin coincidencia exacta en esta respuesta RefSeq; sigue sin validar |

La anotación NCBI es distinta de GENCODE; ambas comparten UCSC y hg38, y no constituyen evidencia biológica independiente. Una coincidencia de referencia no prueba qué transcrito produjo una observación. Una falta de coincidencia tampoco acredita novedad. La primera unión era una observación no clasificada por la caché limitada; ahora puede anotarse como conocida en RefSeq. La segunda no recibe prioridad como descubrimiento.

Control de convención: el inventario sellado contiene la canónica intrónica **17641556–17642844**, también exacta en RefSeq. El extremo 17642845 en etiquetas históricas de autores usa la convención exónica previa; no se sustituye por 17642844 silenciosamente ni se mezclan ambas en una comparación. Esta entrega compara los extremos literales ya convertidos del sello, sin cambiar el catálogo histórico o los objetivos.

**El piloto permanece CERRADO con [1,0,0] y cobertura insuficiente frente a 20.** La anotación no aporta lecturas nuevas, no rescata cobertura, no valida ausencia críptica ni autoriza el control completo/TDP. No se recalcularon hashes de archivos remotos WSL ni su recibo externo.

## Verificación reproducible

Código nuevo de solo lectura: `scripts/compare_unc13a_refseq.py`, stdlib de Python. Cuatro pruebas con controles de extremo desplazado una base, hebra, referencia vacía/truncada/incoherente, inventario parcial/duplicado/promovido y soporte inválido. Las pruebas de software no son experimentos biológicos. Comparación real y repetición idéntica por bytes; detalles en `validation.json`. No se materializó ni ejecutó toda la suite histórica local; CI del PR prueba el repositorio completo por su cabeza exacta.

```bash
python scripts/compare_unc13a_refseq.py \
  --inventory reports/unc13a-control-annotation-20261103/operator-audit-seal.json \
  --annotation reports/source-gate-issue37-20261103/inputs/refseq-hg38.json \
  --out /tmp/ela-issue37-refseq-new
python -m unittest discover -s tests -p test_compare_unc13a_refseq.py -v
python -m compileall -q scripts/compare_unc13a_refseq.py tests/test_compare_unc13a_refseq.py
```

El directorio de salida debe ser nuevo. Inventario SHA256 `a42c22813d033baff2f73de07a894eb62f11624659790d3e6c5e3ef0cb74d8c8`; blob Git de origen `e59107a1fcd05ab8af6b4aeea94d80f3c6172b84`. No se incorpora el texto completo de artículos, código ajeno o matrices de terceros a Git; sí metadatos de anotación, índices, hashes y síntesis propia.

## Única vía siguiente

**Resolver acceso al manifiesto concreto de Seddighi/AD Workbench**, con los requisitos de `ACCESS_REQUIREMENTS.md`. Se necesita un archivo de cuentas de uniones por biblioteca o enlaces BAM/BAI y el mapa condición→unidad independiente→lote. No basta el código, un Sashimi o una matriz génica.

Esta es una puerta de acceso pendiente, **no una fuente aceptada ni un plan de cómputo autorizado**. No enviar solicitudes ni instalar/usar otra conexión de cuenta por esta PR. Una respuesta o exportación de metadatos que Luis aporte puede reabrir únicamente esa puerta. Si no aparece el archivo concreto y su mapa, mantenerla bloqueada; no repetir las consultas de este ciclo ni sumar más candidatos. No se redacta plan de contraste porque ninguna fuente cumple. Issue #37 queda abierta por ese bloqueo; la selección actual está terminada.

## Referencias

- Seddighi, S., Qi, Y. A., Brown, A.-L., et al. (2024). Mis-spliced transcripts generate de novo proteins in TDP-43–related ALS/FTD. *Science Translational Medicine, 16*(734), eadg7162. https://doi.org/10.1126/scitranslmed.adg7162. Disponibilidad y código versionado: S1–S4.
- Irwin, K. E., Jasin, P., Braunstein, K. E., et al. (2024). A fluid biomarker reveals loss of TDP-43 splicing repression in presymptomatic ALS–FTD. *Nature Medicine, 30*, 382–393. https://doi.org/10.1038/s41591-023-02788-5. Corrección: https://doi.org/10.1038/s41591-024-02966-z. Solo disponibilidad/ensayos de cultivo, sin reanálisis de participantes.
- Baughn, M. W., Melamed, Z., López-Erauskin, J., et al. (2023). Mechanism of STMN2 cryptic splice-polyadenylation and its correction for TDP-43 proteinopathies. *Science, 379*, 1140–1149. https://doi.org/10.1126/science.abq5622. Disponibilidad y límites de unidad: S7.
- UCSC Genome Browser / NCBI RefSeq (2025, consultado 03/11/2026). RefSeq All, hg38, GCF_000001405.40-RS_2025_08. API, pista y convención: S8–S10.
