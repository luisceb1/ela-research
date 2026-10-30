# Tres fuentes para un contraste directo — 30/10/2026

## Pregunta, predicción y resultado

Pregunta prefijada en `PLAN.json`: ¿alguna de un máximo de tres fuentes nuevas de cultivos aporta identidad de evento, cuentas crípticas/canónicas, controles y al menos tres unidades biológicas independientes documentadas por condición? Predicción: al menos una cumple todos los requisitos. Fracaso: ninguna los cumple o un enlace esencial sigue sin poder verificarse. No calcular efectos/PSI ni inferencia en ese caso.

**Resultado: tres candidatos revisados, ninguno listo para ese contraste completo.** Se cierra este ciclo sin un cuarto candidato. Es un resultado negativo de disponibilidad/documentación, no una refutación biológica. La auditoría recupera una fuente real de cuentas de uniones para una futura decisión, sin presentarla como replicación externa conseguida.

Base remota verificada: main `f028b88879abed0b92d157e1236dc68ccfd6e60e`; #28/#29 fusionados, cero PR abiertos al inicio y diez issues abiertas. Se leyeron instrucciones, protocolo, estado, backlog, criterios de entrada, ramas y el inventario anterior. No se repitió GEO/mapeo, Fratta, DEXSeq ni la búsqueda histórica de SH-SY5Y. Las nuevas accesiones no habían sido auditadas como fuentes de este contraste; los artículos conocidos no se presentan como descubrimientos bibliográficos.

## Decisiones

| Fuente | Comprobación ejecutada | Decisión para este ciclo |
|---|---|---|
| Ma et al., GSE182976 | SOFT, lista y TAR originales: 12 miembros BigWig, todos con cabecera válida; hg38 y generación de cobertura documentados | No listo: cobertura no conserva por sí sola las cuentas de cada unión. iMN1/2/3 y rep1/2 no certifican la jerarquía de unidades. El RNA-seq GSE126543 reutilizado en el artículo queda excluido como nueva replicación |
| Melamed et al., GSE122069 | SOFT y ENA: selección exacta de seis runs de siControl/siTDP-43; publicación declara tres experimentos biológicamente independientes por condición. Depósito procesado: RSEM gene TPM | No listo con procesados: expresión génica no es cuenta de unión. La alternativa desde crudos requiere otro plan y recursos |
| Brown et al., E-MTAB-15653 | BioStudies API, IDF/SDRF, puntero LFS y payload Parquet real: 22 bibliotecas y cuentas de uniones recuperables | Candidato preferente para resolver factibilidad, aún no aceptado: unidad independiente no documentada explícitamente y falta fijar/enlazar un evento, hebra y denominador antes del contraste. Existe un conflicto técnico en metadatos NMD, sin reparación automática |

La tercera fuente se atribuye a un preprint público de 2025; no se certifica revisión por pares ni independencia de sus cultivos por el mero cambio de accession o fecha de depósito. No se abrieron datos de cohortes post mortem, covariables o genotipos individuales del repositorio mixto de autores. E-MTAB-15433 y PRJNA1256902 aparecen en la disponibilidad bibliográfica, pero no se evaluaron como cuarto candidato.

## QC concreto de E-MTAB-15653

El puntero Git de 133 bytes se distingue del payload de **81.873.975 bytes**, cuyo SHA-256 coincide con el OID LFS `35dd2cf8ed18439733d756fe2ca3cc2c518ea533c91ef31dbbe143ba7756ff60`.

Python/PyArrow lee **2.598.287 filas**. Cuentas enteras, cero valores negativos, cero nulos y cero claves muestra/unión duplicadas. Hay **71.524 ceros explícitos** de lecturas únicamente mapeadas; no se imputan ceros a combinaciones ausentes ni se infiere ausencia molecular. El esquema no incluye una columna de hebra; su interpretación para un evento concreto requiere otra comprobación.

El SDRF tiene **44 filas FASTQ para 22 bibliotecas**, no 44 unidades biológicas. Sus nombres de archivo derivado son solo 21 distintos. Una muestra citosólica `ERR15663627` apunta a `NT_NMD_nucleus_1.quant.sf`, también asignado al run nuclear `ERR15663630`. El Parquet conserva las claves citosólica y nuclear por separado. Al enlazar únicamente por nombre de archivo depositado: 20 claves tienen enlace único, una queda sin enlace y una es ambigua. No se reasigna por semejanza del nombre.

El conflicto pertenece al brazo con inhibición NMD. **Las seis bibliotecas citosólicas basales de control/KD tienen enlace único**; eso no acredita que sean seis cultivos independientes. No hay campo explícito de réplica biológica/lote en el SDRF inspeccionado ni una declaración de independencia encontrada en los métodos consultados. No se convierte el sufijo 1/2/3 en prueba de independencia, ni las fracciones de un cultivo en réplicas.

## Alternativa acotada desde crudos

Para GSE122069, seis GSM seleccionados enlazan por SRX a seis runs ENA. Suman **9.474.892.575 bytes FASTQ comprimidos**, 292.441.551 lecturas y 14.773.033.916 bases según ENA. Son tamaños publicados, no descargas realizadas. El espacio temporal y de alineamiento sería adicional y no se ha medido. STAR, samtools, HISAT2, Bowtie2 y fasterq-dump no estaban instalados en este entorno. No se descargaron FASTQ, se creó índice, se alineó ni se estimaron tiempos/presupuesto como si fueran benchmarks. Antes de comenzar se necesita un plan concreto de referencias, recursos y controles, con autorización aplicable para costes o cambio de alcance.

## Reproducibilidad, errores y pruebas

Python **3.12.14**, PyArrow **21.0.0**, sin aleatoriedad. El manifest fija URL, tamaño y SHA-256 de once entradas públicas. Originales fuera de Git; se exportan solo accesiones, condiciones publicadas, variables técnicas y QC agregado. No se ejecutó código R de autores.

```bash
python scripts/fetch_independent_source_gate.py --manifest research/references/independent_source_gate_20261030.json --cache data/cache/source-gate
python -m pip install -r research/requirements-source-selection.txt
python scripts/audit_independent_source_gate.py --cache data/cache/source-gate --manifest research/references/independent_source_gate_20261030.json --out reports/source-selection-20261030 --parquet
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

El fetcher se verificó con las once entradas ya fijadas en caché; no se declara una nueva descarga integral por ese comando. Las recuperaciones reales y fallos están en `retrievals.json`. Hubo HTTP503 en las rutas habituales de EBI; la API proporcionó la ruta exacta `E-MTAB-/653/...`, que permitió recuperar IDF/SDRF. La ruta inferida inicialmente sin guion final no se presenta como URL válida. Scite devolvió metadatos de los DOI, pero el filtro editorial emitió un mensaje de «no indexado» incompatible con esa recuperación; no se certifica ausencia de avisos editoriales a partir de esa respuesta.

Dos ejecuciones del código final produjeron `results.json` idénticos por bytes; hash y verificación en `repeat_verification.json`. Suite final: **253 tests correctos** (244 de main + 9 nuevos), compileall correcto. Los controles nuevos impiden duplicar bibliotecas por mates, colapsar contradicciones, contar un run dos veces, convertir etiquetas en independencia o reparar enlaces ambiguos; verifican también privacidad de la proyección y rechazo de hashes alterados.

Los primeros intentos de suite usaron una copia local incompleta: faltaban un módulo histórico y dos fixtures de informes. Se conservan logs de 250 tests/10 errores y 253 tests/5 errores. Recuperadas esas dependencias de main, la suite pasó sin modificar el código previo. Un intento local de copiar esas dependencias usó una ruta relativa incorrecta y falló; se corrigió a rutas absolutas. Ninguno de estos fallos se oculta como resultado biológico. CI remota debe comprobarse por la cabeza del PR; sus tests offline no ejecutan este Parquet ni todos los pipelines.

## Siguiente prueba discriminante

Conservar E-MTAB-15653 como candidato, **sin calcular efectos todavía**. La siguiente revisión debe conseguir una fuente primaria adicional concreta que identifique las unidades de cultivo de las seis bibliotecas citosólicas basales y fijar la identidad molecular de un único evento. Si la independencia no puede documentarse, no aceptar la fuente para la replicación prevista. No repetir las descargas y búsquedas ya completadas, ni abrir un cuarto candidato en este ciclo. La reconstrucción desde crudos de GSE122069 queda como alternativa con tamaño conocido y alcance por revisar. Sin nuevas afirmaciones de función, originalidad o beneficio clínico.

## Referencias

- Ma, X. R., Prudencio, M., Koike, Y. M., et al. (2022). TDP-43 represses cryptic exon inclusion in the FTD–ALS gene UNC13A. *Nature, 603*, 124–130. https://doi.org/10.1038/s41586-022-04424-7. GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE182976.
- Melamed, Z., López-Erauskin, J., Baughn, M. W., et al. (2019). Premature polyadenylation-mediated loss of stathmin-2 is a hallmark of TDP-43-dependent neurodegeneration. *Nature Neuroscience, 22*, 180–190. https://doi.org/10.1038/s41593-018-0293-z. GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE122069. Métodos y Extended Data Fig. 1: tres experimentos independientes; sin reutilizar datos clínicos del artículo.
- Brown, A.-L., Zanovello, M., Mikheenko, A., et al. (2025). Sensitivity to TDP-43 loss and degradation resistance determine cryptic exon biomarker potential. *bioRxiv*, preprint. https://doi.org/10.1101/2025.11.23.689722. Secciones Cell fractionation experiment y Data and code availability. BioStudies: https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-15653.
- Repositorio primario `frattalab/cryptic_biology`, commit `80fa3d70418a4665a85d414e33c7c470a9312086`; payload LFS y procedencia arriba. Repositorio Ma inspeccionado solo por árbol/README: `rosaxma/TDP-43-UNC13A-2021`, commit `97c3ab74294d01bb302081dc6f9004dc3d61b704`. No se leyeron sus tablas de tejido como una fuente nueva de cultivos.
