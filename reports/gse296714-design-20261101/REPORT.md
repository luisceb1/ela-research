# GSE296714: fuente molecular recuperada — 01/11/2026

## Resultado

**Apta para descripción molecular por biblioteca, todavía no aceptada para inferencia entre unidades biológicas.** Se recuperaron y verificaron dos tablas numéricas reales, además del mapa técnico de muestras y la anotación de los grupos STMN2. No es necesario descargar los crudos para iniciar una reproducción descriptiva de ese evento bajo el modelo PAPA.

Base remota: main6b0d4204241d316f12a90915d61e79c4904be104, PR35 fusionada. El usuario autorizó expresamente esta alternativa para avanzar sin depender de correos. Plan fijado antes de recuperar la matriz: research/plans/2026-11-01-gse296714-design-gate.md. Sus extensiones acotadas de miembros PAPA/anotación se escribieron antes de leerlos. No contactos, costes, FASTQ, alineamientos, clínica o fusión automática.

## Evidencia

| Comprobación | Resultado ejecutado | Límite |
|---|---|---|
| GEO | 12 GSM únicos:6controles y6KD | 12bibliotecas no acreditan por sí solas12diferenciaciones |
| Identidad técnica | Cada GSM enlaza con un SRX, SAMN y run ENA; alias y BioSample concordantes | Identidad técnica, no independencia biológica |
| Selección ENA | Proyecto109runs; seleccionados solo12 por SRX explícito | El BioProject incluye otras series; no analizar todos sus runs como GSE296714 |
| Tabla de autores | 12etiquetas y condiciones concordantes, enlace por basename BAM | Columnas:muestra,condición,rutas. Sin lote/diferenciación/pareamiento explícitos |
| Matriz génica | 61.126genes×12bibliotecas; sin claves duplicadas ni valores negativos/no finitos; STMN2/UNC13A/TARDBP presentes | 162.743valores fraccionarios: estimaciones Salmon/tximport, no moléculas o soporte directo |
| Tabla PAPA | 43.630grupos×12bibliotecas; claves únicas, valores válidos, columnas enlazadas mediante tabla de autores | Abundancia estimada de grupos de exones finales, no cuenta de uniones |
| Anotación STMN2 | Grupo ENSG00000104435.14_1 enlazado a ALE críptico; _2 incluye transcritos de referencia | Siete registros GTF para dos grupos; no siete eventos independientes ni siete réplicas |
| UNC13A | Dos grupos PAPA y expresión génica localizados | No se ha medido su unión críptica; un grupo a cero no demuestra ausencia de CE |

Los enlaces y recibos están en samples.tsv, retrievals*.json e input_hashes.json. target_gene_counts.tsv y target_pas_group_counts.tsv contienen únicamente las proyecciones de genes objetivo; sus números son observaciones de tablas de autores, no resultados de una nueva alineación. target_annotations.tsv conserva los siete registros de anotación relevantes con coordenadas GTF1-based inclusivas.

La anotación curada asigna al grupo STMN2_1 cuatro modelos con comienzo chr8:79616822(+) y distintos extremos. El grupo_2 contiene tres modelos ENST de referencia con inicio79664815. Se preservan las distintas geometrías; no se fuerza una única posición de poliadenilación ni se equiparan estos grupos a las dos uniones medidas en GSE122069.

## Diseño y procedencia

GEO y métodos describen WTC11, neuronas corticales derivadas de iPSC, CRISPRi dirigido al promotor TARDBP o guía no dirigida, recogidas30días después de diferenciación. La intervención se hace en iPSC, antes de diferenciar. No hay brazo de rescate, ni inicio de tratamiento después de un déficit funcional medido. Es una comparación molecular de perturbación temprana, con posibles efectos sobre maduración.

Preparación poly(A), strand-specific,Kapa mRNA Hyper Prep,2×150bp NextSeq2000. El alineamiento descrito para Humphrey usa GRCh38/GENCODEv30/STAR2.7.2a y el recuento génico depositado usa transcritosGENCODEv40/Salmon1.8.0/tximport. Son pasos y referencias distintos; no declarar automáticamente contradicción ni mezclar sus coordenadas. Las estimaciones fraccionarias son compatibles con ese método y no se redondearon para simular cuentas enteras.

La publicación declara replicación biológica en sus materiales. Esa declaración se conserva; no se demuestra pseudorreplicación por ausencia de campos en GEO. Sin embargo, la tabla recuperada no reconstruye qué biblioteca corresponde a qué diferenciación, lote o pareja. Esta auditoría **no certifica que6/6equivalgan a6/6unidades independientes**. No se han calculado p-valores, efectos inferenciales o intervalos basados en esa suposición. Una sola línea WTC11 tampoco permite generalizar a donantes con ELA.

Se compararon identificadores explícitos actuales con tres entradas fijadas de main: geo-audit/samples.tsv,gse121569-design/culture_libraries.tsv y source-selection-20261030/results.json. Cero identificadores compartidos en esas entradas. Es una comprobación limitada, no un análisis de identidad por secuencias ni una certificación de ausencia de solapamiento en todos los estudios. El trabajo de Brown sobre sensibilidad/degradación ya incluye el conjunto Humphrey; se registra su reutilización bibliográfica, no como una segunda validación independiente. No se ha reabierto la búsqueda histórica de E-MTAB-15653.

## Recursos: descarga grande evitada

ENA anuncia79.276.637.720bytes comprimidos para los24mates de los12runs seleccionados y520.986.256en read_count. Son metadatos ENA, no lecturas procesadas por nosotros ni benchmark; no se confunden mates, fragmentos y moléculas. No se descargó FASTQ.

Zenodo15538002resuelve a la versión15538003. El ZIP completo mide831.190.727bytes, MD5publicado323be7f29bb04bdf14a351bbda06ce51. Se recuperaron262.144bytes finales y445.027del directorio central, que enumera2690entradas. Solo se extrajeron tres miembros de cultivos mediante respuestas206con Content-Range verificado, longitud, descompresión limitada y CRC:

- Tabla de muestras:3863bytes descomprimidos.
- Cuentas PAPA Humphrey:7.148.108bytes descomprimidos.
- GTF curado crípticos:408.294bytes descomprimidos; se exportan solo registros objetivo.

El tráfico de esos cinco rangos fue4.019.043bytes. Se añadieron SOFT,GEO,ENA,XMLdel artículo y metadatos Zenodo pequeños. El ZIP íntegro no se descargó y su MD5global **no está verificado**; CRCySHAde miembros/segmentos no equivalen a ese MD5. La caché temporal contiene originales, no se añaden a Git artículos completos, matriz íntegra ni tablas post mortem. archive_members.json es una proyección del índice con los miembros seleccionados y el puntero PPAU de continuación.

## Interpretación y decisión

Se ha superado el bloqueo de acceso a una fuente numérica molecular concreta: tenemos tablas reales, condiciones y enlaces por biblioteca. Para STMN2 puede reproducirse descriptivamente el uso relativo de sus grupos de exones finales sin depender de una respuesta de autores. Esto añade una capacidad al proyecto; no descubre la asociación TDP-43/STMN2, no mide recuperación neuronal y no acredita una cohorte independiente nueva.

Para UNC13A no hay aceptación como análisis de CE con estos miembros. Su expresión génica o uso de exones finales no sustituyen sus uniones crípticas. No se hará una comparación conjunta STMN2/UNC13A de splicing hasta tener una medición comparable para ambos.

## Reproducibilidad, errores y verificación

Código estándar Python3.12, sin instalar dependencias. Se ejecutaron el parser SOFT, enlace ENA, validación de cuentas génicas/PAPA y proyección GTF. Dos ejecuciones offline finales produjeron los seis artefactos deterministas idénticos por bytes; repeat_verification.json fija sus hashes. Once pruebas locales específicas pasan; tests.txt conserva salida. La suite histórica completa no se materializó localmente: se verificará en CI remota sobre la cabeza de la PR. Tests de software no acreditan replicación biológica ni descargan los datos reales.

Errores preservados en errors.json: clone sin credenciales,403del FTP directo (recuperación satisfactoria por el enlace GEO), cola ZIP insuficiente para todo el directorio (se pidió después el rango central exacto), y auxiliar de test denominado run que ocultaba TestCase.run (renombrado run_row, suite final correcta). Tres consultas opcionales a Ensembl para cotejar nombres agotaron timeout; se conservaron los identificadores objetivo ya usados por el proyecto, sin declarar una validación nueva de Ensembl. STMN2 queda además enlazado por gene_name en el GTF de autores. Ninguno de esos fallos se interpreta como hallazgo biológico. No se repitieron alineamientos históricos ni filtros RiMOD/NYGC.

Reproducción con fuentes en caché o recuperación acotada:

```bash
python scripts/fetch_gse296714_audit.py
python scripts/index_gse296714_archive.py
python scripts/fetch_gse296714_zip_metadata.py
python scripts/fetch_gse296714_zip_metadata.py --counts
python scripts/fetch_gse296714_zip_metadata.py --annotation
python scripts/audit_gse296714_design.py
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

Los scripts no ejecutan código de autores; los hashes de las fuentes necesarias se verifican contra recibos antes del análisis. Los recibos nuevos no sustituyen los históricos y una fuente cambiada requiere revisar la discrepancia.

## Única siguiente prueba

Reproducción **descriptiva por biblioteca** de STMN2_1/suma de todos los grupos STMN2 de PAPA, cotejada con PPAUoriginal de esa misma versión. Plan prospectivo: research/plans/2026-11-01-stmn2-papa-description.md. No ejecutada en este ciclo. No denominarla PSI de uniones ni validación independiente; sin medias de grupo,p-valores,crudos o nuevo cribado. El posible análisis inferencial sigue condicionado a una estructura experimental justificable.

## Referencias primarias

- GEO GSE296714:https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE296714
- Bryce-Smith et al.(2025),*TDP-43 loss induces cryptic polyadenylation in ALS/FTD*,Nature Neuroscience:https://doi.org/10.1038/s41593-025-02050-w. XMLEuropePMC12586162,hash en recibo.
- Zenodo versión15538003:https://doi.org/10.5281/zenodo.15538003. Índice y miembros, no archivo completo verificado.
- Código de autores frattalab/tdp43-apa,commit e0d54b6f60a094c79f05f57ab4c88e451127bcbb:https://github.com/frattalab/tdp43-apa/tree/e0d54b6f60a094c79f05f57ab4c88e451127bcbb
- Brown et al.(preprint2025),*Sensitivity to TDP-43 loss and degradation resistance determine cryptic exon biomarker potential*:https://doi.org/10.1101/2025.11.23.689722. Métodos incluyen el conjunto Humphrey; no se cuenta como nueva cohorte.
