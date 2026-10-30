# Intervalos publicados y bins DEXSeq — 30/10/2026

## Evidencia y resultado

Los intervalos que el código recibido declaraba sin validación independiente **sí aparecen en métodos publicados**. Almeida Quadros et al. (2024), sección Bioinformatics analysis of RNA-seq data, especifican las regiones de recuento STMN2 chr8:80529057–80529284 y UNC13A chr19:17753223–17753350, ambas en hg19. Se comprobó el pasaje mediante scite y HTMLeditorial. Koike et al. (2023), métodos de análisis de motivos y Fig. S5, corroboran el intervalo UNC13A de 128 bp con hg19 explícito. No se han importado datos individuales de esos estudios.

GEO GSE121569 y métodos Klim et al. (2019) declaran GRCh37/hg19 para el alineamiento de FASTQ; los metadatos describen dexseq-all como tabla de fragmentos y combined como cuentas de partes de exón. La verificación del ensamblaje se ejecutó sobre SOFT/XML locales ya recuperados, con hashes. No se realizó liftover.

| Gen | Intervalo de recuento publicado, hg19 | Bins evaluados | Bins solapados | Bin más próximo | Distancia entre bases extremas |
|---|---|---:|---:|---|---:|
| STMN2 |chr8:80529057–80529284|10|0|E003|5031bp|
| UNC13A128bp |chr19:17753223–17753350|62|0|E037|304bp|

Las bases estrictamente interpuestas son5030y303,respectivamente; no confundirlas con la diferencia de coordenadas extremas. Así se conserva la definición de distancia de la reproducción anterior, ahora con procedencia del intervalo contrastada. La predicción previa de cero solapamientos no se refuta. **Cero bins solapados no significa cero lecturas deCE ni ausencia molecular.**

| Fragmento discordante destacado | Intervalo del bin hg19 | Distancia al intervaloCE del mismo gen |
|---|---|---:|
| STMN2E009 |chr8:80577117–80577242|47833bp|
| UNC13AE026 |chr19:17740049–17740132|13091bp|
| UNC13AE030 |chr19:17743917–17744002|9221bp|
| UNC13AE054 |chr19:17785466–17785565|32116bp|

No se presentan esos cuatro bins como eventos crípticos ni como indicadores directos de su inclusión. E026/E030conservan su resultado descriptivo de cuentas de bins del análisis anterior; este contraste no lo transforma en un resultadoCE.

## Convenciones y límites

Los 72 bins cumplenwidth=end−start+1. Se evaluaron los intervalos publicados como cerrados 1-based; el artículo de Quadros no declara formalmente si trasladó sus números a BED antes de contar. Se conserva esa incertidumbre y se ensayan las nueve combinaciones de desplazamiento independiente −1/0/+1 de cada extremo: **ninguna produce un solapamiento**. No se corrigen coordenadas silenciosamente.

La región STMN2 es una región de recuento publicada, no una validación de todos los extremos de un transcripto terminal o de poliadenilación. Las fuentes utilizadas para estos números no especifican aquí hebra: se conserva la hebra de los bins sin atribuir a la publicación una validación independiente de ella. La comparación por gen/cromosoma/intervalo no necesita inventarla.

Ma et al. (2022) describen variantes UNC13A de 128/178 bp **en hg38**. Se registra como advertencia de alcance: este análisis valida solo la región hg19 de 128 bp; no importa la de 178 bp mediante una resta constante o conversión no auditada. La unión STMN2 en hg38 del informe histórico event-reference es otra representación y no se mezcla con estos intervalos.

## Avisos editoriales y fuentes

Scite identifica una corrección de Koike (14/07/2023), DOI 10.1371/journal.pbio.3002228. Se leyó el aviso editorial completo: corrige la definición de exones crípticos en la Introducción; no contiene una modificación de coordenadas. No se ignoró el aviso ni se sustituyó por el resumen del artículo.

Los otros tres filtros editoriales no devolvieron registros y mostraron el mensaje genérico de no indexación pese a recuperar los artículos sin filtro. Es una limitación del resultado del conector: no certifica ausencia universal de avisos. Para Quadros no se devolvió aviso en esas consultas dirigidas. Registro curado con DOI, URL, localizadores y alcance en research/references/ce_intervals_hg19_20261030.json. Ejemplos breves de texto primario verificado: Quadros,“the cryptic exon of STMN2” ; Koike,“UNC13A cryptic exon”. Los números y ensamblajes se guardan como datos moleculares. No se afirma descarga/hash del HTML completo nuevo; se guarda la proyección curada y su hash. Los originales GEO, XML y SOFT locales sí tienen hash de bytes.

## Reproducción y controles

Plan previo: research/plans/2026-10-30-ce-coordinate-audit.md. Python 3.12.14, stdlib, sin aleatoriedad. Manifest curado separado del programa; verificación de DOI/ensamblaje en XML/SOFT, hash del DEXSeq original, unicidad de 72 bins, anchos, genes, cromosoma y ensamblajes. Exporte completo de los 72 intervalos y resultado negativo, no solo los destacados. No tablas clínicas ni cuentas por biblioteca.

```bash
python -m scripts.audit_ce_bin_coordinates \
 --source ../ela-consolidation/data/cache/issue14/GSE121569_dexseq-all.csv.gz \
 --manifest research/references/ce_intervals_hg19_20261030.json \
 --soft data/cache/gse121569/family.soft.gz \
 --xml data/cache/gse121569/PMC7153761.1.xml \
 --out reports/ce-bin-coordinate-audit
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

**167 tests locales correctos (160 previos + 7 nuevos), compileall correcto.** Controles positivos de identidad/contención; negativos de adyacencia, distancia, cromosoma/hebra, ensamblaje incompatible, coordenadas inválidas. Estos tests verifican geometría/software, no biología ni verdad de las publicaciones. Logs, versiones, hashes y parámetros en esta carpeta. CI se comprueba por el nuevo commit.

## Decisión y siguiente prueba discriminante

La extracción DEXSeq queda como evidencia de fragmentos anotados y **no como cuantificación directa de las regiones CE contrastadas**. Este pendiente de procedencia/coordenadas se cierra de forma acotada; no se repiten los análisis de cuentas para buscar una señal CE que el catálogo no representa. Issue #14 sigue parcial por pozo/reactivo/fórmula y otros límites; no se cierra automáticamente.

Siguiente acción segura: revisar el acceso público a conteos/lecturas de uniones que sí representen el evento específico, distinguiendo las uniones Fratta ya auditadas de cualquier fuente realmente independiente. Si los únicos datos son los ya auditados o no hay soporte de lectura accesible, registrar el bloqueo y cerrar esta vía como indirecta antes de otra auditoría de bins. No crear réplicas de la misma cohorte ni interpretar modelos completos sin soporte. Sin p-valores/refit/PSI/función, contactos, gastos, laboratorio, publicación externa o merge. PR #28 sigue independiente.

## Referencias

- Almeida Quadros,A.R.A.,Li,Z.,Wang,X.,et al.(2024). *Cryptic splicing of stathmin-2 and UNC13A mRNAs is a pathological hallmark of TDP-43-associated Alzheimer’s disease*. Acta Neuropathologica,147,9. https://doi.org/10.1007/s00401-023-02655-0 . Métodos de intervalos y ensamblaje,HTML editorial/scite, 30/10/2026.
- Koike,Y.,Pickles,S.,Estades Ayuso,V.,et al.(2023). *TDP-43 and other hnRNPs regulate cryptic exon inclusion of a key ALS/FTD risk gene,UNC13A*. PLOS Biology,21(3),e3002028. https://doi.org/10.1371/journal.pbio.3002028 . Métodos de motivos/Fig. S5.
- Koike,Y.,Pickles,S.,Estades Ayuso,V.,et al.(2023). *Correction:TDP-43 and other hnRNPs regulate cryptic exon inclusion of a key ALS/FTD risk gene,UNC13A*. PLOS Biology,21(7),e3002228. https://doi.org/10.1371/journal.pbio.3002228 . Aviso completo inspeccionado.
- Klim,J.R.,Williams,L.A.,Limone,F.,et al.(2019). *ALS-implicated protein TDP-43 sustains levels of STMN2,a mediator of motor neuron growth and repair*. Nature Neuroscience,22,167–179. https://doi.org/10.1038/s41593-018-0300-4 . XML PMC7153761 y SOFT GSE121569: ensamblaje de la matriz.
- Ma,X.R.,Prudencio,M.,Koike,Y.,et al.(2022). *TDP-43 represses cryptic exon inclusion in the FTD–ALS geneUNC13A*. Nature,603,124–130. https://doi.org/10.1038/s41586-022-04424-7 . Fuente hg38, excluida del cruce hg19 sin conversión auditada.
