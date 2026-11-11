# Fuente QC recuperada; replicación independiente aún no aceptada

11/11/2026. Revisión de disponibilidad, sin nuevos contrastes biológicos. [Alcance fijado](../../research/plans/2026-11-11-paired-stmn2-source-gate.md): tres familias, inspección de fuentes y manifiestos pequeños, sin matrices RNA ni solicitudes de acceso.

## Evidencia y decisiones

| Fuente concreta | Qué está comprobado | Qué falta | Decisión |
|---|---|---|---|
| NYGC 2026, Zenodo 20090702 / 19223231 | ST3 con claves de biblioteca/donante, región, RIN, preparación/plataforma y métricas QC; manifiesto público de cuentas de splicing | Composición por muestra todavía sin inspeccionar; lote de extracción/secuenciación no explícito; presencia de nuestras uniones en matriz Leafcutter filtrada sin verificar | **Aceptada como candidata técnica para QC de la cohorte actual**, no como replicación independiente |
| EGA EGAD00001009686 / estudio EGAS00001006711 | Colección con bulk RNA y snRNA, diez casos ALS con corteza/médula emparejadas según catálogo, tecnología y acceso identificados | Acceso controlado; cuentas de nuestras uniones, calidad/lote y composición enlazada; independencia de donantes respecto a TARGET_ALS sin verificar | **Pendiente**, diseño relevante, no ejecutable con acceso actual |
| GSE330130 / DOI 10.64898/2026.07.24.740361 | GEO público: 44 bibliotecas multiome, de 20 tejidos lumbares y 24 de corteza; matrices snRNA/snATAC y métricas por barcode | Número de donantes con ambos tejidos, independencia, calidad/lote enlazados y cobertura de la unión STMN2 no establecidos | **No aceptada para replicar el endpoint sellado**; posible referencia de composición, con anatomía lumbar distinta de cervical |

**Cero fuentes cumplen hoy toda la puerta de replicación independiente.** No se interpreta como inexistencia de datos útiles ni como imposibilidad de investigar. Sí se ha recuperado una entrada técnica nueva para abordar una limitación concreta del resultado actual.

## NYGC: calidad disponible para 308/313 bibliotecas

El código del navegador [AlsGeneBroswer](https://github.com/Eastmanmd/AlsGeneBroswer), árbol `1003dd81b540a34791a83ceedb0538530800bac3`, enlaza el [depósito de metadatos](https://zenodo.org/records/20090702). Su diccionario público separa ST3 (RNA) de tablas clínicas/genéticas; solo se inspeccionó la hoja ST3 para claves y calidad.

Archivo `NYGC_Flagship_ST_1_3_Metadata.xlsx`, 4.136.212 bytes, MD5 `4f0ff6f23ca0e48da461a6574a146a93`, SHA-256 `c1bf21493c4a2773e27ff787e60267fc2e1304ce11e84e644c03c700cc68f048`. El checksum coincide con el manifiesto. No se incorpora el libro mixto al repositorio.

El inspector comprueba coincidencia exacta y única entre external_id recount y rna_id de ST3, sin quitar sufijos. El ámbito recount sigue siendo región más rail_id. Comprobación de disponibilidad, no aceptación definitiva de un modelo ajustado:

| Región | Bibliotecas originales | Coincidencia exacta única | RIN numérico finito entre 1 y 10 | Preparación informada | Región fuente compatible |
|---|---:|---:|---:|---:|---:|
| Corteza lateral | 149 | 147 | 147 | 147 | 147 |
| Cervical | 164 | 161 | 161 | 161 | 161 |

La hoja tiene 2.574 registros RNA. `qc_availability.json` conserva solo agregados y hash. La incorporación comprobada de 308 bibliotecas originales demuestra solapamiento: **este recurso no es una cohorte independiente por llevar otro nombre**. No se calculó todavía cuántos de los 45 pares finales pasan un nuevo filtro QC ni ningún efecto ajustado.

Campos relevantes observados: `rna_id`, `donor_id`, `rin`, `rna_prep`, `rna_platform`, `sra_run`, regiones, profundidad y sesgo de cobertura 5′/3′. No se ha demostrado que todos los valores QC adicionales estén completos, ni que preparación/plataforma sustituyan al lote real. No se usaron diagnóstico nuevo, edad, sexo, mutación ni evolución de este libro.

El mismo depósito anuncia estimaciones de deconvolución en **ST7** dentro de un libro de expresión de 32.702.280 bytes; **no se descargó**. Su granularidad y clave de enlace deben comprobarse antes de asumir que ofrece composición por biblioteca. [Zenodo 19223231](https://zenodo.org/records/19223231) anuncia una matriz Leafcutter de 282.523 uniones y 1.718 muestras (210.147.878 bytes), pero no se inspeccionó su contenido: un catálogo de splicing no demuestra inclusión del evento STMN2 sellado. Tampoco se descargó.

## Otras candidatas: límites concretos

[EGA](https://ega-archive.org/datasets/EGAD00001009686) describe diez casos ALS con ambos tejidos y controles repartidos por región. Combina bulk TruSeq v2 con núcleos 10x 3′ v3; algunos pools requieren desmezcla. El catálogo muestra solicitud al DAC VIB y acuerdo de transferencia, no acceso ya obtenido. No se descargaron FASTQ, claves individuales ni datos controlados. El siguiente insumo útil sería una tabla derivada mínima de C/K por biblioteca junto a claves anónimas de donante/región, calidad/lote y composición. La posible entrega pública o autorizada de esa tabla debe aclararse; no se ha enviado solicitud.

[GSE330130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE330130) se leyó por endpoint GEO de texto al fallar la página en el buscador. El manifiesto distingue 44 bibliotecas de 87 registros de ensayos; no son 87 donantes ni demuestra que los tejidos sean del mismo individuo. El [preprint](https://pmc.ncbi.nlm.nih.gov/articles/PMC13483793/) no tiene texto completo archivado en PMC y el servidor original devolvió 403. No se sustituyó por inferencias de un resumen. Las matrices por gen no contienen por sí mismas cuentas de la unión exón 1→2a; queda sin comprobar si los reads crudos de este ensayo permiten medirla con precisión. Una comparación lumbar/corteza, además, sería una generalización anatómica, no replicación cervical exacta.

## Siguiente paso operativo

**Prioridad inmediata: prefijar un control de calidad sobre los 45 pares originales usando los RIN recuperados**, comprobando primero concordancia de donante/región/preparación y completitud en esos pares. No cambiar el endpoint ni presentar el mismo análisis como nueva replicación. Definir el filtro o ajuste antes de mirar su efecto; si no hay datos de lote o composición, mantener expresamente esas limitaciones.

Para composición, la entrada concreta es **ST7 NYGC**, no una descarga masiva de RNA. Antes de incorporarla, fijar un alcance de extracción de esa hoja y verificar que proporciona estimaciones por muestra y claves exactas. Eso puede reforzar el control de confusión en la misma cohorte; una replicación externa seguiría pendiente.

Para replicación independiente, conservar EGA como la candidata de diseño más relevante de estas tres, condicionada a datos derivados accesibles y exclusión de donantes compartidos. No abrir otra ronda de cohortes por inercia. #37 UNC13A y #44 K26 no cambian.

## Reproducción y límites de verificación

`python scripts/inspect_stmn2_qc_availability.py /ruta/temporal/stmn2-audit-work` reproduce el agregado con el libro temporal en `source-gate/nygc-metadata.xlsx` y las fuentes previas. Se verificaron tamaño, MD5, SHA-256, coincidencias exactas únicas, etiqueta regional y rango numérico del RIN. Se conserva el manifiesto de archivos y sus checksums en `sources.json`, sin datos de personas. La búsqueda quedó limitada a las tres familias. No hubo nuevo análisis de asociación, contacto, gasto ni cambio en las cifras del resultado emparejado. Los fallos de lectura de páginas se registran como acceso fallido, no como prueba de ausencia de datos.
