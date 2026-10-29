# Unión STMN2, soporte full-length y semántica de cuentas — 2026-10-29

**Evidencia:** identidad de unión contrastada con fuente primaria independiente; cuantificación exploratoria del mismo experimento. No validación de transcrito completo, poliadenilación ni función neuronal. Continúa el PR #5 y los límites dejados en #2/#4.

## Evidencia

### 1. La unión candidata coincide con un evento STMN2 conocido

Grima et al., Molecular Neurodegeneration 20:40 (2025), DOI [10.1186/s13024-025-00820-5](https://doi.org/10.1186/s13024-025-00820-5), Figura 5, identifica la unión críptica STMN2 **chr8:79611214:79616822**. Sus métodos especifican GRCh38.primary_assembly. El script extrae el dato del XML primario [PMC12023386](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12023386/fullTextXML), valida DOI/ensamblaje/unicidad del evento y conserva solo una proyección molecular y el hash de la fuente.

La comparación exacta contra las uniones GTF de las dianas recupera **un solo transcrito**, `GSE310723:BambuTx9249`, y ninguno del catálogo cerebral. La hebra + procede de GENCODE v47 verificado por hash; **el pie de figura no informa hebra**, por lo que no se afirma que ese pie por sí solo la confirme. Las coordenadas se comparan como bases exónicas limítrofes (las del GTF), sin desplazar ±1 ni convertirlas silenciosamente a inicios/finales intrónicos. Las pruebas rechazan desplazamientos, otra unión anotada, otro cromosoma y hebra opuesta.

Esto cambia la clasificación del candidato de 'unión no anotada sin atribución independiente' a **'transcrito depositado que contiene una unión críptica STMN2 ya descrita'**. No es un descubrimiento de una nueva unión. Coincidir con esa unión no acredita que el inicio 5′, el extremo final 3′, la secuencia completa o el sitio de poliadenilación sean los mismos que en el estudio independiente. El final del segundo exón del GTF, 79.619.794, sigue sin validación independiente en este análisis.

### 2. Soporte depositado de BambuTx9249

| Biblioteca de cultivo | counts | uniqueCounts | fullLengthCounts | CPM depositado |
|---|---:|---:|---:|---:|
| Ctrl +5Aza | 4,04542 | 4 | 0 | 4,33744 |
| Ctrl sin 5Aza | 0 | 0 | 0 | 0 |
| TDP43KD +5Aza | 10 | 10 | 8 | 10,46853 |
| TDP43KD sin 5Aza | 24 | 24 | 12 | 15,63271 |

`fullLengthCounts` es una **estimación producida por bambu** de asignación de longitud completa; puede ser fraccionaria. En este candidato presenta valores positivos solo en KD, pero eso no vuelve independientes las bibliotecas ni valida moléculas completas de manera experimental. La cuenta única positiva en el control +5Aza carece de soporte full-length en la matriz correspondiente; no se deben equiparar las dos medidas.

Se auditaron las cuatro matrices por serie (counts, uniqueCounts, fullLengthCounts y CPM) sobre **392.871 / 401.720 filas**, con identidad exacta de encabezados, TXNAME y GENEID. No hubo cuentas inválidas, `uniqueCounts > counts` ni `fullLengthCounts > counts` por encima de tolerancia absoluta 1e-4 para redondeos independientes. No se impuso una relación de inclusión entre full-length y únicas, que son criterios diferentes.

### 3. CPM publicado usa otro denominador

La versión exacta [bambu 3.2.6](https://github.com/bioc/bambu/blob/2fb886442096896807f44191ad2d1e00b43ceadd/DESCRIPTION) se localizó en el espejo oficial Bioconductor, commit `2fb886442096896807f44191ad2d1e00b43ceadd`. En [calculateCPM](https://github.com/bioc/bambu/blob/2fb886442096896807f44191ad2d1e00b43ceadd/R/bambu-quantify_utilityFunctions.R), el denominador incluye asignaciones compatibles **e incompatibles**. La suma del CPM depositado queda entre 584.587,98 y 723.370,16, por debajo del millón en las 12 bibliotecas, coherente con que las tablas transcriptómicas exportadas solo contengan una parte de ese denominador.

`depth_and_cpm.tsv` calcula el denominador implícito como suma(counts)×1e6/suma(CPM). Su exceso sobre las cuentas asignadas está entre aproximadamente 192.520 y 637.758 unidades. **Es un cálculo a partir de matrices redondeadas, no una medición directa de incompatibleCounts del objeto original.** No debe confundirse con reads brutos ni calidad celular. El ajuste previo por millón de cuentas asignadas sigue siendo válido como sensibilidad descriptiva etiquetada, pero no equivale al CPM depositado.

Al usar directamente el CPM publicado, el cociente KD/Ctrl del candidato con 5Aza es **2,414**, y sin 5Aza sigue indefinido porque el control es cero. El ENST principal STMN2 conserva dirección menor (cocientes **0,146 / 0,191** con/sin 5Aza). UNC13A ENST00000519716.7 da **1,065 / 0,727**, manteniendo la falta de una dirección única entre los dos brazos. No hay p-valores ni estimación factorial con bibliotecas sin réplicas.

### 4. La causa de la paridad queda sin resolver

Se revisaron fuentes R/C++ de **3.2.6** fijadas por SHA256 y Git blob SHA. [writeCountsOutput](https://github.com/bioc/bambu/blob/2fb886442096896807f44191ad2d1e00b43ceadd/R/readWrite.R) exporta el assay correspondiente sin un factor dos explícito. La ruta de cuantificación usa cuentas observadas y matrices de asignación; el testigo algebraico escalar del script admite salida 1 para entrada 1. **Ese testigo no ejecuta R ni reproduce el pipeline completo** y no explica las matrices reales. El origen del GCD=2 puede estar en entradas, agregación u otro paso no trazado; no se adjudica a ninguno sin evidencia.

Las fullLengthCounts contienen entre 1.825 y 3.411 celdas fraccionarias por biblioteca, mientras uniqueCounts es entero par en todas. No se divide ningún fichero por dos. La escala y la independencia de las unidades permanecen como limitación abierta.

## Interpretación

Se ha cerrado una incertidumbre concreta: el candidato contiene una unión críptica STMN2 ya publicada, y la cuantificación depositada aporta soporte full-length en las dos bibliotecas KD. También se ha comprobado que cambiar al CPM publicado no revierte el patrón descriptivo de cultivo STMN2. Ninguna de estas comprobaciones genera una réplica biológica, una nueva medición ni una validación funcional.

El resultado negativo cerebral sigue siendo ausencia en este catálogo de isoformas asignadas a STMN2, no ausencia biológica de la unión. Tampoco hay demostración de un evento críptico UNC13A en los catálogos analizados.

## Limitaciones y siguiente prueba

- Falta comprobar directamente alineamientos, extremos y poliadenilación. El nombre 'fullLengthCounts' no certifica el extremo 3′, integridad química del ARN o ausencia de sesgo de catálogo.
- La fuente independiente respalda la identidad de una unión; no es una reanálisis de sus datos ni replicación de nuestros cocientes de abundancia. La diferencia de versión GENCODE (43 en ese estudio, 47 en el depósito) no impide comparar esta coordenada en GRCh38, pero no se generaliza esa equivalencia a otros eventos.
- La revisión de código no equivale a ejecutar bambu; R no estaba disponible. No se puede reconstruir la causa de la escala a partir del exportador y las matrices solamente. Bloqueo documentado en EXECUTION_NOTES.md.
- No se infieren CDS, traducción, NMD, rescate axonal/sináptico ni efecto clínico. No hay tratamientos o recomendaciones para pacientes.

Siguiente tarea segura seleccionada: preparar un contraste de **evidencia funcional publicada** que distinga corrección del ARN, recuperación proteica y función neuronal, con temporalidad y controles. Mantener abierta la trazabilidad de escala y extremos; si una fuente no confirma los extremos, conservar solo la atribución de unión. No contactar a autores ni iniciar experimentos sin autorización.

## Reproducción

`python scripts/check_event_reference.py` y `python -m unittest discover -s tests -v`. Requiere las entradas de los PR #3–#5 y acceso a fuentes públicas en la primera ejecución. Se añadieron cuatro archivos GEO públicos y seis archivos de código externo fijados por commit, además de la proyección del artículo. Originales recuperables por URL/hash en `sources.json`; los binarios y las fuentes externas completas quedan fuera de git. **37 pruebas offline pasan.** `run.json`, `errors.json`, tablas TSV y `research/plans/2026-10-29-event-reference.md` registran parámetros/entorno, resultados y plan previo. Estado: pendiente revisión de PR.
