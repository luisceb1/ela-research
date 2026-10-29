# Issue14: reproducción numérica agregada — 29/10/2026

## Resultado y alcance

**Se reproducen los 63 campos numéricos cotejados de los resúmenes recibidos, sin discrepancias dentro de la tolerancia de redondeo.** Son45 campos de expresión y18de extracción DEXSeq. No constituye replicación biológica independiente, descubrimiento ni prueba terapéutica. La issue14 permanece parcialmente abierta: falta auditar uniones/índices de Fratta y reconstruir el diseño por diferenciación antes de cualquier refit estadístico.

Se recuperaron los dos archivos directamente de GEO. El de recuentos GSE126542 coincide también byte a byte con el comprimido del ZIP recibido. El hash de dexseq-all coincide con el que figuraba en la auditoría previa. Los scripts recibidos se conservan sin modificar para revisión, pero **no se ejecutaron**: incluyen salidas por caso o gráficos individuales. Se reimplementaron sus métodos para exportar solo resultados agregados. No se leyeron miembros de tablas por caso, clínicas o genéticas de los ZIP.

## GSE126542: expresión nuclear total

Matriz de58567 filas,57865 símbolos identificables únicos y702 filas de identificador literalNA. Contiene14 bibliotecas clasificadas, siete pares TP/TN publicados; la serieGEOcompleta lista16 muestras, incluidas dos no clasificadas que no aparecen en esta matriz. No tratarlas como dos pares adicionales. La publicación de Liu et al. (2019), Results/RNA Dysregulation, confirma siete unidades emparejadas con las dos fracciones nucleares. Se usan exclusivamente etiquetas técnicas de emparejamiento, sin variables clínicas individuales ni salidas identificables por caso.

| Gen | Cambio geométrico TN/TP, CPM+0.5 en log | Median-of-ratios | Dirección CPM entre pares |
|---|---:|---:|---|
| STMN2 | −55.50% | −51.48% | Descenso en7/7 |
| UNC13A | +29.32% | +41.75% | Aumento en7/7 |
| TARDBP | −1.41% | +7.93% |3 aumentos/4 descensos |

Los porcentajes son resúmenes geométricos de recuentos totales normalizados por gen en núcleos. El incremento de UNC13A **no demuestra incremento de ARN canónico o proteína funcional**. El ARN de TARDBP no mide la localización nuclear de TDP43. Son comparaciones de fracciones de tejido, no un seguimiento temporal ni intervención de rescate.

CPM incluye todas las filas para el denominador, incluidas las702NA; median-of-ratios excluye esas filas y usa20437 genes positivos en todas las bibliotecas. Es una normalización análoga al preprocesamiento de DESeq2, no un ajuste DESeq2. Sensibilidad adicional: excluirNA del denominador CPM produce −55.5022%, +29.3209% y −1.4149%, respectivamente; mantiene su dirección. Cambiar a median-of-ratios sí cambia el signo de TARDBP. Esto impide describirlo como un efecto de dirección estable entre normalizaciones.

Se reproducen también los intervalos t descriptivos y p de inversión de signos del paquete. Son exploratorios: siete pares, supuestos de distribución/simetría y sin corrección nueva por multiplicidad. No son un test de tratamiento aleatorizado, prueba de causalidad o validación clínica. No se estimó dispersión RNAseq ni se ajustaron covariables clínicas.

## GSE121569: extracción de DEXSeq publicado

Archivo procesado de589903 filas y37 columnas;98236 símbolos ausentes. Se recuperan102 fragmentos de los tres genes. Los p ajustados siguientes son **los proporcionados por los autores**, no un modelo o FDRrecalculados aquí:

| Gen | Fragmentos | p ajustado evaluable | p ajustado<0.05 | p ajustado<0.10 |
|---|---:|---:|---:|---:|
| STMN2 |10|10|3|4|
| UNC13A |62|58|1|1|
| TARDBP |30|26|0|0|

GEO documenta18 bibliotecas en la serie, pero esta tabla contiene12 columnas countData:6siScr y6siTDP43. No equiparar esas12 columnas ni las18 bibliotecas a diferenciaciones independientes. Supplementary Fig3 de Klim et al. (2019) declara dos experimentos independientes para RNAseq. El vínculo biblioteca→diferenciación no se ha reconstruido en este ciclo; la descripción previa «dos diferenciaciones» no se considera por sí sola un mapa validado. El término `als` del archivo designa el contraste experimental de siRNA TDP43, no un grupo de pacientes con ALS.

Se reprodujo el chequeo de los intervalos CE declarados en el código recibido (GRCh37/hg19): ningún fragmento diana los solapa; distancias mínimas5031 bp para STMN2 y304 bp para UNC13A. Esos intervalos **no se validaron independientemente** en este ciclo: resultado condicional a su definición/ensamblaje. No se infiere ausencia biológica del exón, ni se obtiene PSI a partir de fragmentos anotados. Los cuatro fragmentos STMN2 bajo0.10 tampoco son cuatro eventos crípticos independientes.

## Calidad y trazabilidad

Plan: research/plans/2026-10-29-issue14-reproduction.md. Entradas públicas fijadas por SHA256, manifiesto de paquetes/miembros y código recibido en package_provenance.json. Comprobación: comparison.tsv y comparison.json. Tolerancia de expresión1e−8relativa/absoluta para CSVredondeado; DEXSeq1e−12relativa/1e−14absoluta. Cero discrepancias en dimensiones y63 campos cotejados; esto no valida automáticamente la interpretación de los informes antiguos.

Nueve pruebas nuevas cubren pares incompletos/duplicados, orden de columnas, signo exacto, valores no finitos, normalización con ceros, NA literal, genes duplicados y coordenadas. Esta entrega es **independiente desde main** (base105 tests):114 tests pasan, incluidos los9nuevos. El PR28 contiene166 tests en su propia rama; no se ha fusionado ni se presenta ese código como incorporado a main. Su cierre documental acotado se registra en PR28_REVIEW.md.

La reproducción completa usa Python3.12ySciPy1.17.0para cuantiles t; los métodos restantes usan biblioteca estándar. Las pruebas offline no requieren descargar datos ni SciPy. Versiones, comandos y hashes en run.json; originales en caché, sin republicación de matrices individuales. Datos GEO públicos atribuidos a sus depositantes; licencia específica de cada matriz no verificada, sin extender automáticamente una licencia de artículo a todo anexo. Código recibido procedente del usuario, sin licencia separada inferida.

## Pendientes y siguiente tarea

1. Auditar BEDoriginal y códigoRde Fratta: duplicados, uniones clasificadas, denominadores y fórmula de índices. Los paquetes de expresión/splicing/genética reutilizan GSE126542; no son tres cohortes.
2. Reconstruir mapa técnico de diferenciación/bibliotecas GSE121569 antes de reestimar modelos. Esta entrega solo reproduce extracción del DEXSeq procesado.
3. Validar independientemente coordenadas/ensamblaje de CEsi se reutilizan para una conclusión estructural.

No cerrar issue14 ni priorizar una diana nueva a partir de estos resúmenes. Sin gasto, comunicación, laboratorio o merge automático.

## Fuentes primarias

- GEO:GSE126542, https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE126542 ; Liu et al. (2019), https://doi.org/10.1016/j.celrep.2019.04.003 , sección RNA Dysregulation del autor-manuscritoPMC6508629.
- GEO:GSE121569, https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE121569 ; descripción de columnas en GSM3439296; Klim et al. (2019), https://doi.org/10.1038/s41593-018-0300-4 , Supplementary Fig3 (texto primario indexado). El acceso directo editorial devolvió redirección no accesible; no se afirma lectura integral nueva del PDF.
