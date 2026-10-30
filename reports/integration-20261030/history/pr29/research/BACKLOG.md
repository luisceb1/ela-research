# Backlog vigente — 29/10/2026

## Definición de uniones: cierre acotado con bloqueo — 30/10/2026

La búsqueda histórica dirigida identifica stmn2_and_unc13a.bed como entrada local del pipeline (dos versiones con blobs fijados), sin recuperar su contenido en los ocho árboles inspeccionados. Alcance: 264 metadatos de commits, ocho árboles históricos, cinco scripts y cuatro búsquedas dirigidas; no revisión integral de todos los commits/ramas/forks. El Rmd histórico lee el CSV ya calculado. No se resolvieron cuatro alias UNC13A ni dos conflictos de hebra STMN2. Se conservan los seis enlaces técnicos a ENA, sin independencia biológica inferida. Informe en reports/junction-definition-search.

Esta vía de reanálisis conjunto de siete uniones queda BLOQUEADA por definición molecular incompleta. No repetir búsquedas idénticas ni auditorías de los mismos bins sin una fuente nueva. Condición para reabrir: definición original o paso generador explícito que resuelva etiquetas/extremos/hebra. La próxima decisión científica debe seleccionar una pregunta con insumos públicos completos, sin sumar esta fuente como replicación ni promover candidatos por este bloqueo. Issue14 permanece parcial; no se cierra ni fusiona nada. 183 tests existentes correctos, compileall correcto y tres controles negativos de estado ejecutados; no son nuevos experimentos.

## SH-SY5Y: mapa técnico completado y geometría parcial — 30/10/2026

reports/shsy5y-junction-map enlaza exactamente CTR07/08/09 y TDP10/11/12 con seis runs de PRJEB42763 por nombres de BAM en XML ENA (3control/3KD), sin descargaBAM/FASTQni independencia biológica inferida. Supplementary6recuperada como XLS válido desdePMCS3:16uniones;de7camposdecuentas,3nombresidénticos,soloUNC13A_annotatedconhebraconcordante. STMN2_annotated/cryptic tienen conflicto S6−frenteaGCv47+;4aliasUNC13ACEpendientes,sinreasignación. PipelineSTARinicio−1/final+1sonlímitesflanqueantes,noBEDintrónicoestándar;comentario difiere del código,noejecutadocódigoexterno.183tests locales(175+8),compileallOK.

Predicción de6bibliotecas cumplida;7enlacesmolecularesno. Siguienteúnicaprueba:definición original deuniones/paso generadorque documentelos4aliasUNC13AyhebraSTMN2;sinella,nocalcularefectosCEconidentidadnoresuelta. Unidadesbiológicassiguenpendientes. PR29abierto,PR28separado,sinmerge/cierre/contactos/gastos/laboratorio. Estecheckpointprevalecesobretareasprevias.

## Fuentes de uniones — checkpoint posterior del 30/10/2026

Inventario reproducible en reports/junction-source-inventory: CSV público de Brown2022, commit e05e8723 y blob c8715e2b; 42 filas de cultivo, 5 grupos, 7 campos de cuentas de unión, 294 celdas enteras. Sin efectos o PSI calculados; solo cinco agregados exportados. Klim17filas (11control/6KD) reutiliza GSE121569, no réplica nueva ni equivalente a12DEXSeq/15expresión; selección pendiente. Cuatro grupos candidatos de otras fuentes, ninguna unidad independiente certificada. PRJEB42763 es disponibilidad de estudio, no mapa de filas. Corrección Brown2024 cambia una línea SK-N-DZ a SK-N-BE(2): CSV antiguo conserva nombres, no reasignar sin mapa. BED amplio excluido por mezcla de fuentes; no computado/exportado.175tests locales(167+8),compileallOK.

Predicción de nueva fuente lista no cumplida aún. Próxima prueba única: tabla molecular Supplementary6 de Brown (extremos hg38 de uniones), convenciones del pipeline y mapa fila→run/unidad de un solo grupo de cultivo PRJEB42763. Sin ese enlace no analizar efectos ni declarar replicación. No repetir Fratta ni binsDEXSeqya cerradoscomoindirectos. PR29abierto,PR28separado,sin merge/cierre/contactos/gastos/laboratorio. Este checkpoint prevalece sobre las acciones antiguas inferiores.

## Intervalos CE y bins — checkpoint posterior del 30/10/2026

reports/ce-bin-coordinate-audit: fuentes primarias independientes del código recibido verifican las regiones de recuento hg19 STMN2chr8:80529057–80529284 yUNC13A128bpchr19:17753223–17753350. SOFT/XML de Klimconfirmanhg19paraDEXSeq. Ninguno de72bins(10/62)solapa las regiones,tampoco con9combinaciones±1deextremos. Mínimas diferenciasentreextremos5031/304bp(5030/303bases interpuestas). Los4discordantes quedan fuera; no son mediciónCE,no ausencia biológica. Convención formal del artículo limitada; no liftover de varianteshg38ni validación de extremos completos. CorrecciónKoike2023leída:conceptual,no coordenadas.167tests locales(160+7),compileallOK.

Pendiente de coordenadas cerrado acotadamente. Siguiente:disponibilidad de lecturas/cuentas de uniones que realmente midan eventosCE,fuente pública independiente de las mismas cohortes;Fratta ya auditado,no repetirlo ni sumarreplicaciones. Si no hay fuente nueva,documentar bloqueo y cerrarDEXSeqcomo evidencia indirecta. Refit sigue bloqueadopozo/reactivo/fórmula. PR29abierto,PR28independiente,sin merge/cierreautomático,contactos,gastos o clínica nueva. Este checkpoint prevalece sobre las acciones antiguas siguientes.

## Cuentas y denominadores — checkpoint posterior del 30/10/2026

Originales recuperados de caché con SHA256verificados; bloqueo anterior de acceso a matriz resuelto aquí, sin nueva descarga. reports/dexseq-coverage:408agregados de cuentas,612efectos y204medias previas concordantes. Los cuatro destacados tienen mínimos908/38/40/29cuentas,sin ceros. UNC13AE026/E030conservan inversión con3denominadores;STMN2E009yUNC13AE054son discordantes dentro del gen pero descienden en ambos lotes por biblioteca. H1>=10no refutada;H2todosdiscordantesen3métodosrefutadaen2casos. No inferir ruido,CE,proteína o función.160tests locales(153+7),compileallOK.

Siguiente tarea seleccionada:coordenadas/ensamblajeCEdeSTMN2/UNC13Acon primaria independiente antes de interpretar bins como evento. Cobertura aquí es cuentas de bin,no lecturas de unión o profundidad por base. Refit pendientepozo/reactivo/fórmula. PR28sigue separado,no incorporado;PR29abierto,sin merge/cierreautomático. Resumen semanal existente sin duplicar. Este checkpoint sustituye el pendiente de acceso/cobertura por cuentas que figura en las secciones históricas inferiores.

## Checkpoint vigente — 30/10/2026 (esta rama PR29, pendiente de revisión)

Main sigue en8dfa7ce7. PR28 sigue independiente en27f34d1b, no incorporado: catálogo/originalidad/QCglobal completados allí (545/353/182/821, sin novedad inferida; protocoloUNC13Av0.4conceptual). Leer sus informes antes de retomar; no repetir ni tratar los pendientes históricos de esta página como actuales. No se han reconciliado mediante merge las dos ramas.

PR29: magnitud descriptiva ejecutada en reports/dexseq-magnitude sobre tabla agregada del commit18abfa54. De38inversiones de signo,4persisten con>=0.1pp en ambos lotes:STMN2E009yUNC13AE026/E030/E054;0con>=0.5pp. Umbrales arbitrarios, no significación/ruido/función demostrados.153tests locales (147+6), compileallOK. Fallos iniciales por checkout incompleto resueltos; errores/hashes/logs conservados. GEOdirecto timeout28: no nueva descarga original, cuentas/profundidad/ceros ni sensibilidad de denominador ejecutados en este ciclo. Sin refit por diseño pozo/reactivo/fórmula pendiente.

Resumen24–30/10 en reports/weekly/2026-10-30.md, sin informe previo localizado. Siguiente prueba: recuperar matriz con hash conocido y auditar agregados de cobertura/ceros y denominadores en todos los objetivos, destacando los cuatro discordantes. Si bloqueada, verificar coordenadasCE/ensamblaje con primaria independiente. #1/#2técnicamente ejecutadas, sin repetir; lecturas crudas y cobertura siguen pendientes. Issue14parcial. Sin merge/cierre/contactos/gastos/publicación externa. Secciones siguientes conservan historial: sus cifras de tests y tareas antiguas no reemplazan este checkpoint.

Consultar STATE.md, MASTER_EVIDENCE.md y reports/repository-integration. Las issues históricas describen incidentes iniciales; no repetir correcciones ya ejecutadas.

| Prioridad | Tarea | Estado y siguiente avance |
|---|---|---|
| P0 | Consolidación | Completada mediante PR #26: main verificado, 15 cabezas incluidas, 105 tests en Python 3.11/3.12 y dos auditorías GEO exitosas; PR dependientes cerrados por incorporación |
| P0 | #1 GEO | Inventario y enlace técnico ejecutados; integración no valida calidad biológica completa |
| P0 | #2/#17/#19 mapeo | Ejecutado por ENSG; controles positivos; incidente cero objetivos resuelto técnicamente |
| P0 | #20 catálogo | 21/1910 explicado y GENCODE ejecutada; pendiente catálogo de autores y filtros sobre universo corregido |
| P1 | Suplementos Bolger/crypTE | Próxima tarea científica: descripción/esquema, hashes y convenciones antes de cotejar 1901 claves. No importar tablas clínicas |
| P0 | #14 GSE126542/GSE121569 | 63 campos de agregados y24 de índices concordantes; BED/R Fratta auditados con sensibilidad de fórmula/deduplicación. Siguiente mapa técnico de diferenciación; sin cierre automático |
| P1 | Descriptivos/escala | Ejecutados; paridad sin explicación. Etiquetas depositadas no equivalen a CI/no CI. No inferencia con n=1 |
| P1 | #15 CAMK2B/péptidos | CAMK2B estructural reproducido; genética/péptidos pendientes; sin validación proteómica independiente |
| P1 | #16 MEA | Software auditado; denominadores/completitud y protocolo experimental pendientes. Prototipo solo sintético |
| P1 | #21 AGRN | Verificar isoforma, soporte y antecedentes antes de priorizar ensayo funcional |
| P2 | #18 colaboración | Elegir pregunta falsable y controles; borrador sin envío, gasto o laboratorio |

Si hay bloqueo: registrar fuente, intento y motivo verificable; avanzar por otra vía segura. Persistir fuentes, parámetros, versiones, errores y negativos. Ramas breves desde main; esta consolidación no autoriza futuros merges sin revisión ni cierres automáticos.


## Fase #14 — reproducción agregada, rama independiente desde main

29/10/2026: reports/issue14-reproduction reproduce63campos agregados (45expresión/18extracciónDEXSeq) sin discrepancias. Fuentes GEO descargadas y fijadas; código recibido conservado sin ejecutar, sin tablas por caso/clínicas/genéticas importadas. STMN2/UNC13A mantienen dirección entre CPM/MR; TARDBP cambia de signo. DEXSeq102fragmentos, no refit niPSI; doce columnas de contraste no son doce diferenciaciones. Nueve tests nuevos sobre105de main:114OK. PR28con166tests sigue separado y no fusionado: contiene originalidad/crypTE/QCglobal posteriores al estado base de main. Leer ambos PR y reconciliar estados al integrar; no declarar esos informes ya incorporados. Issue14no se cierra: próximos BED/RdeFratta, deduplicación/denominadores y mapa de diferenciación121569. Sin nuevas cohortes, hallazgos clínicos, contactos, gasto, laboratorio o merge automático.

## Uniones Fratta auditadas — 29/10/2026, ampliación PR29

reports/fratta-junction-audit: BED/Rmd públicos fijados por SHA256 y Gitblob.241filas→69únicas/172repetidas,16muestras/7pares+2unsorted;27combinaciones ausentes rellenadas con0por método autor, no ceros observados.24campos agregados del paquete concordantes. Rmd2694incluye3clasesUNC13A;2766usa2clases. Cambio medio principal72.67puntos, dosclases72.00, sumar duplicados63.81; no porcentaje molecular, sensibilidad biológica ni nueva cohorte. No se leyeron archivos alélicos/clinica ni exportaron filas por muestra.124tests de esta rama (105base+19nuevos), PR28con166sigue separado. Próximo: mapa técnico biblioteca/experimento-diferenciación deGSE121569 antes de cualquier refit; issue14sigue abierta, sin contactos/laboratorio/gasto/merge.

## Diseño GSE121569 contrastado — 29/10/2026, PR29

`reports/gse121569-design` enlaza las 12 columnas DEXSeq con GSM y lote publicado. El SOFT contiene 18 bibliotecas HUES3; Fig.S3a etiqueta explícitamente Batch 1/2 y Fig.1b confirma dos experimentos independientes de diferenciación y transfección. Transcripción visual con hash del miembro DOCX: las fechas solo sirven de cotejo. Contraste 2 scramble/2 KD en Batch 1 y 4/4 en Batch 2; 6 siRED/NoTx fuera de countData. No confundir las 15 bibliotecas del contraste de expresión publicado con las 12 columnas DEXSeq.

Identidad de pozo/reactivo y fórmula original de ajuste pendientes: no refit inferencial, doce bibliotecas no son doce diferenciaciones. Mapa técnico completo, no nueva replicación. Once tests nuevos: 135 en esta rama (105 main +30 issue14); PR28 sigue independiente con166. Siguiente tarea segura: integridad y concordancia countData/combined.dexseq y diseño público reactivo/pozo antes de sensibilidad por lote. Issue14 abierta; sin contactos, gastos, laboratorio o merge automático. Reconciliar STATE/BACKLOG con PR28 al integrar.

## Cuentas DEXSeq verificadas — 30/10/2026, PR29

reports/dexseq-qc: 585869 fragmentos únicos, 18 bibliotecas originales/12 columnas de contraste. 7030428 cuentas comparadas exactamente, cero discrepancias y cero claves sin enlazar. Las 589903 filas DEXSeq incluyen4034 repeticiones con diferencias exclusivamente de anotación, sin conflictos de cuentas/campos no anotativos; no sumar como fragmentos nuevos. Cinco filas de resumen técnico separadas. Ocho tests nuevos:143 en rama. Sin refit ni nueva replicación; pozo/reactivo/fórmula pendientes. Próximo: unicidad de102fragmentos objetivo y sensibilidad descriptiva por lote. PR28independiente; sin merge o cierre automático.

## Sensibilidad por lote — 30/10/2026, PR29

reports/dexseq-batch-sensitivity:102fragmentos objetivo únicos. Fracción de cuentas dentro de grupo por biblioteca, medias KD-control por lote: mismo signo8/10STMN2,36/62UNC13A,20/30TARDBP; resto signo opuesto. NoPSI ni isoformas/proteína, sin nuevos p-valores. Cambios pequeños y dependencia composicional limitan signos.147tests en rama. Próximo magnitud/cobertura y sensibilidad de denominador de fragmentos discordantes antes de priorizar; refit pendiente de diseño. Sin merge/cierre automático.
