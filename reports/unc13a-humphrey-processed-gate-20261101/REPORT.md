# UNC13A/Humphrey: puerta de procesados cerrada con bloqueo

Fecha: 01/11/2026. Plan prospectivo: research/plans/2026-11-01-gse296714-unc13a-processed-gate.md, fijado en b9bba151d423b652516de7162872158357aac10a antes de esta ejecución.

## Evidencia

Se enumeró el árbol completo de frattalab/cryptic_biology, commit80fa3d70418a4665a85d414e33c7c470a9312086, sin truncamiento. Se inspeccionaron cuatro archivos de código, sin ejecutarlos ni abrir las tablas post mortem que referencian. main_fig.Rmd y supplementary.Rmd vinculan explícitamente Humphrey-i3Cortical al compendio data/compendium_cryptics.csv.

La tabla contiene861filas con la etiqueta Humphrey-i3Cortical y6filas UNC13A en esa comparación. Su esquema es gene_name,paste_into_igv_junction,junc_cat,baseline_PSI,contrast_PSI,comparison,strand,is_cryptic,n_significant_data. Son resultados agregados publicados: no hay identificadores GSM/SRX/run, etiquetas de las doce bibliotecas ni cuentas de soporte por muestra.

Se exportaron únicamente coordenadas textuales, categoría, etiqueta de comparación y hebra de las seis filas UNC13A a event_definitions.tsv. No se exportaron ni recalcularon PSI o efectos. La existencia de varias filas/convenciones no permite adjudicarles automáticamente las dos uniones deseadas, corregir posiciones en una base o inventar el comparador canónico. La convención de coordenadas no queda validada por esta proyección.

Los únicos Parquet de cuentas STAR localizados por nombre pertenecen a nuc_cyto, la fraccionación ya auditada; no son una prueba de soporte Humphrey. No se descargó su payload ni se reabrió ese análisis. Los scripts de curvas usan archivos de SH-SY5Y, no aportan enlaces verificables para las doce bibliotecas objetivo; no se repitió su búsqueda cerrada. Las entradas grandes y los archivos clínicos/post mortem no se descargaron.

Resultado del código:0bibliotecas enlazadas a soporte individual, fuente no aceptada para cobertura/PSI por biblioteca. Esto significa ausencia de enlace verificable en los materiales inspeccionados, **no ausencia biológica de UNC13A ni inexistencia universal de datos**. La etiqueta de comparación reconoce la familia experimental; no certifica identidad de cada biblioteca.

## Interpretación y cierre

No se supera la puerta prevista. No se puede combinar numéricamente este resumen con las doce PPAU individuales STMN2, ni convertir medias publicadas en réplicas o cuentas de lecturas. Se cierra esta fuente sin abrir otra en el mismo ciclo. STMN2 permanece reproducida y la PR36conserva sus resultados positivos y el contraste inicial fallido.

No hay evidencia nueva para autorizar una descarga de79GB. El siguiente trabajo propuesto es un **plan de recursos y valor informativo para un piloto de crudos limitado**, todavía sin ejecutarlo: identificar control/KD y tamaños por enlaces técnicos, definir una extracción compatible con paired-end, referencias y límites RAM/disco/tiempo, y determinar qué decisión resolvería. No repetir los controles históricos GSE122069 ni asumir su runtime para bibliotecas de otro diseño. El piloto no debe ejecutarse hasta que ese plan resulte viable dentro de recursos concretos.

## Verificación y procedencia

scripts/audit_unc13a_humphrey_gate.py se ejecutó sobre el CSV recuperado; esquema, filas de comparación y proyección de definición verificables en result.json. Dos ejecuciones produjeron artefactos idénticos por bytes. No se añaden tests que solo reflejen una tabla estática. Compileall correcto; CI remota comprobará el código existente en la cabeza actualizada. La suite completa no se materializó localmente en este entorno nuevo.

El acceso al código/datos se realizó por el conector GitHub: se registran commit y SHAdeblob, no se inventan estados HTTP o hashes binarios no observados. La caché CSV normaliza saltos de línea, y su SHA256se etiqueta como caché normalizada, distinto del SHAdeblob Git. No se incorporan a Git el CSV completo ni código ajeno; sí el árbol, proyección, recibos y síntesis propia. Hubo un fallo inicial de lectura de un plan local ausente tras cambiar el entorno; se recuperó el plan fijado desde GitHub antes del análisis.

Fuente primaria: https://github.com/frattalab/cryptic_biology/tree/80fa3d70418a4665a85d414e33c7c470a9312086. Tabla: data/compendium_cryptics.csv, blobfa4bb9dfa5d9c6132524c7750c0304184a70552b. Los cuatro scripts inspeccionados se enumeran en sources.json. No contactos, costes, FASTQ, laboratorio, inferencia o fusión automática.
