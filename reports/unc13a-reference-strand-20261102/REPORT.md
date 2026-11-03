# UNC13A: geometría de referencia y alternativa unstranded — 02/11/2026

## Evidencia y contrato

Se recuperaron solo7.623bytes de JSONde UCSC:2.500bases de hg38chr19:17641000-17643500y GENCODEv47en esa ventana. URL/fecha/SHA256y estados HTTP en retrievals.json. Son secuencia y anotación del mismo proveedor; no se afirma cotejo entre dos proveedores independientes ni replicación biológica.

Los cuatro modelos de conversión prefijados en research/plans/2026-11-02-unc13a-reference-strand.md se evaluaron antes de datos biológicos. Una única conversión de los pares históricos da los límites canónicos anotados y CT/ACen la secuencia positiva para los tres eventos: si el par representa límites exónicos1-based(a,b), su intrón0-basedhalf-open es[a,b-1). En la hebra negativa CT/ACcorresponde a GT/AGen orientación transcriptómica.

| Evento | Intervalo intrónico0-basedhalf-open | Hebra |
|---|---|---|
| Canónica | [17641556,17642844) | − |
| Brazo críptico izquierdo genómico | [17641556,17642413) | − |
| Brazo críptico derecho genómico | [17642541,17642844) | − |

La canónica coincide con exones consecutivos de cuatro transcritos UNC13A:ENST00000519716.7,ENST00000551649.5,ENST00000552293.5yENST00000550896.1. Los brazos crípticos delimitan el intervalo candidato [17642413,17642541),128bases. Su compatibilidad geométrica/motivos no valida una isoforma completa o su expresión. Los múltiples eventos alternativos publicados quedan fuera de este contrato primario.

Usar directamente el par histórico(17641556,17642845)como intervalo0-basedhalf-open da CT/CC, no CT/AC. Por ello el nuevo parser debe usar end0=17642844. No se alteraron conteos RiMOD/NYGCni se reasignó automáticamente una convención a todos los archivos de autores: el mapeo debe ser específico del esquema de cada fuente. El ejemplo intrónico1-based(17641557,17642413)convierte al mismo intervalo que el ejemplo exónico(17641556,17642414), pero esa igualdad matemática no demuestra identidad universal de sus etiquetas.

## Orientación de biblioteca

La descripción GEO ya recuperada documenta bibliotecas strand-specific con KAPA mRNA HyperPrep. La fuente primaria del fabricante explica incorporación de dUTPen la segunda hebra y ausencia de amplificación de esa hebra. Bajo adaptadores Illumina convencionales es compatible con una expectativa de primera hebra/RF; esto es una **inferencia metodológica**, no verificación empírica del layout de estas bibliotecas. No se han examinado lecturas o adaptadores de los archivos reales ni se afirma FR/RFcertificado.

Se fija prospectivamente el modo primario **unstranded: omitir --rna-strandness**, conservando la orientación física de pares FR. Se exigirá XS-para estos eventos por señales de empalme y concordancia con la referencia, sin inducir XSmediante RFforzado. Si HISAT2no emite la hebra esperada en los positivos conocidos, el gate fallará; no se escogerá la configuración que más soporte produzca. La alternativa pierde información direccional de biblioteca, pero permite comprobar una extracción técnica definida sin adivinarla. Aún no está validada con el alineador.

Fuente de protocolo consultada por web, solo síntesis propia persistida:https://rochesequencingstore.com/catalog/kapa-mrna-hyperprep-kit/?attribute_options=96rxn. No se ejecutaron sus instrucciones como órdenes operativas ni se sustituyó el kit por versiones comerciales nuevas.

## Verificación y límites

scripts/unc13a_reference_contract.py verifica hashes, ensamblaje, longitud de secuencia, pista y geometría; exporta models.json y contract.json. Dos ejecuciones produjeron ambos JSONidénticos por bytes. Cuatro tests comprueban conversiones, desfase de una base, límites de ventana e integración del intervalo canónico con el Ndel parser PE. Compileall correcto. La CI de la cabeza nueva comprobará la suite completa; no se reejecutaron las auditorías cerradas.

Etiqueta de evidencia: referencia/anotación y contrato computacional, no soporte de lecturas reales. No FASTQ, índice humano, instalación de alineador, alineamientos, PSI, p-valores, nuevos efectos o beneficio clínico. La prueba sintética previa de dos decodificadores comparte política de pares y no sustituye la futura prueba end-to-end.

## Única siguiente prueba

Contrato/refencia ya fijados; no repetir como nueva tarea. Plan prospectivo siguiente, aún no ejecutado: research/plans/2026-11-02-unc13a-unstranded-minigenome.md. Probar HISAT2y colación sobre un minigenoma pequeño con positivos/negativos conocidos, modo unstranded y proyección explícita a estos intervalos, dentro de un presupuesto separado pequeño. No descargar6,35GBde crudos hasta resolver esa prueba y el runner supervisado humano. raw_execution_ready=false.
