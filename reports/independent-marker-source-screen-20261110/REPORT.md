# Fuente independiente para UNC13A–STMN2: tres candidatas, ninguna lista para inferencia

Fecha: 10/11/2026. Autorización: Luis indicó continuar hacia una fuente independiente tras el análisis condicionado por subtipo. Protocolo de este ciclo: [plan](../../research/plans/2026-11-10-independent-marker-source-screen.md), commit `2b23019a9836767ddffc50fb0e9627425d6471da`, anterior a inspeccionar el libro de valores originales. Es una auditoría acotada de viabilidad, no otro contraste de H2.

## Evidencia y decisión

**0/3 fuentes admitidas para calcular ahora una asociación emparejada ajustada por TDP-43.** Una fuente sí aporta un archivo original público recuperado y verificado; falta la identidad de las unidades. No se estimó ninguna nueva correlación ni se promovieron réplicas técnicas a biológicas.

| Fuente | Qué aporta | Qué impide el análisis ahora |
|---|---|---|
| [Agra Almeida Quadros 2024](https://doi.org/10.1007/s00401-023-02655-0) | PCR de ambos marcadores crípticos y carga de pTDP-43 en tejido humano; además, experimento separado de dosis de siTDP-43 | Valores originales emparejados por solicitud a los autores; no se ha recuperado una tabla pública que permita el ajuste |
| [Gittings 2023](https://doi.org/10.1007/s00401-023-02599-5) | snRNA-seq en C9ORF72 ALS/FTD, eventos crípticos en STMN2 y KALRN | Los autores no detectaron el evento críptico de UNC13A; no puede sustituirse por expresión génica ni por ausencia biológica |
| [Ramsey 2026](https://doi.org/10.1172/JCI190035) | Libro original público con PCR y mediciones de pTDP-43, organoides y tejido FTLD-GRN | Sin claves verificables de muestra/réplica ni enlace PCR→patología; los organoides no muestran retención críptica detectable según el artículo |

[Decisiones completas](candidate-decisions.json), [tabla exportable](candidate-decisions.tsv), [recibos y hashes](source-receipts.json).

### Quadros: candidata prioritaria para una petición específica

El estudio humano procede de tejido del Massachusetts Alzheimer’s Disease Research Center; Ikegami procede de otro estudio y centro. No se declara identidad de cohortes ni se han comparado identificadores de participantes. Cambian enfermedad y región cerebral: estos datos serían una comprobación externa de asociación en otra proteinopatía TDP-43, **no replicación de los subtipos de ELA** ni de su relación con progresión.

El artículo publica una correlación entre ambos marcadores en Fig. 2f y relaciones con carga de pTDP-43 en la amígdala. La sección de disponibilidad remite a los autores para los datos del estudio. Los accesos Mayo `syn5550404` y MSBB `syn3157743` se refieren a recursos RNA-seq separados: no se presumen equivalentes a los sujetos de las mediciones PCR/histológicas.

El estudio también aporta una explicación alternativa ya publicada: en un experimento de SH-SY5Y, STMN2 y UNC13A responden a distintos niveles de reducción de TDP-43 (Results, primer apartado, Fig. 1). Esto motiva considerar curvas con umbrales y contexto celular; **no es un descubrimiento nuestro ni demuestra que explique los subtipos de Ikegami**. Una correlación homogénea no es una consecuencia necesaria de compartir una causa.

No se descargó el suplemento que agrupa tablas de participantes/demografía; no se digitalizaron gráficas. Que no se haya localizado una tabla pública utilizable no prueba que no exista en otra ruta.

### Gittings: un fallo de medición relevante, no una refutación de H2

El texto primario explica que la región críptica de UNC13A no se detectó en sus núcleos y analiza la cobertura escasa y el sesgo 3-prime de 10x. El catálogo inicial de posibles eventos usa Liu 2019, pero eso no convierte su propio conjunto snRNA-seq en una medición de UNC13A. Se detiene aquí: sin descargar matrices, archivos por participante ni lecturas crudas. Muchas células no solucionan la falta de medición del evento objetivo.

### Ramsey: archivo recuperado, pero unidades y enlaces no verificables

Descarga editorial: [Supporting Data Values](https://dm5migu4zj3pb.cloudfront.net/manuscripts/190000/190035/JCI190035.sdval.xlsx), **74.783 bytes**, SHA256 `db027322133460279ceacdc3d5fccd314c9f262cff8a45c7a2ad7bd57a9779ad`, 34 hojas. Se inspeccionó su estructura y las etiquetas de las hojas objetivo con openpyxl 3.1.5; [inventario de celdas](ramsey-workbook-layout.json), sin exportar los valores moleculares.

- `Fig6E`: bloques de organoides de 16/25 semanas, WTC11/GRNKO. Filas 18 y 20: retención críptica UNC13A/STMN2. **3 entradas numéricas por marcador y condición**, sin identificadores de cultivo/diferenciación/replicado.
- `Fig6F`: tejido humano. Filas 14 y 16: UNC13A/STMN2 crípticos. **18 entradas Control (B:S) y 27 FTLD (V:AV)** por marcador. Son entradas numéricas, **no 45 sujetos**. No se infiere una estructura de triplicados ni se emparejan genes solo por posición de columna.
- `Fig6D`: el bloque etiquetado de pTDP-43 está en E:F, filas 3–10: **8 entradas por grupo**. No hay claves que las vinculen con las 18/27 entradas PCR. No se presupone que procedan de los mismos sujetos.
- Las hojas objetivo no tienen comentarios explicativos con mapas de muestras. El libro no contiene hoja separada `Fig6G`; se informa la localización literal por contenido. Las letras del archivo y las referencias de la leyenda no se igualan silenciosamente.

También se recuperó el suplemento editorial SD1: **11.476.925 bytes**, hash en recibos, 19 páginas. Es un suplemento de 11 figuras y leyendas; su texto, incluida la leyenda S9, no aporta un mapa de las observaciones PCR. Se inspeccionó el árbol del código v1.0 publicado por los autores: cuadernos de análisis scRNA-seq, no una tabla de enlace PCR→patología. No se ejecutó código ajeno.

El artículo describe acumulación astroglial de pTDP-43 en organoides sin detectar retención de los exones crípticos estudiados. Esto es un ejemplo **publicado y contextual** de por qué carga de pTDP-43 y función de splicing neuronal no se equiparan. No se transfiere ese resultado a ELA ni se calcula un efecto propio.

## Interpretación y límites

El bloqueo actual es la disponibilidad de una tabla emparejada con unidades identificables y medida de TDP-43 interpretable. La presencia de ambos genes, múltiples puntos o un repositorio abierto no satisface ese requisito. Ninguna candidata ofrece en lo inspeccionado una prueba nueva ejecutable de la asociación condicionada por pérdida nuclear de TDP-43.

Esto tampoco invalida los estudios: la identificación de unidades necesaria para nuestra pregunta puede estar en archivos no públicos o requerir aclaración. No se ha auditado exhaustivamente cada recurso enlazado; se aplicó el criterio de parada ante la falta de un marcador o de su mapa de enlace. La independencia por estudio/sitio no demuestra por sí sola ausencia de todo solapamiento de muestras. Los resultados PCR no son cuentas de uniones; **#37 y #44 siguen bloqueadas**.

Sin datos nuevos suficientes, no se modifica el resultado de Ikegami: rho ajustado 0,31669; p=0,07825; incertidumbre compatible con una asociación positiva. Tampoco se elige un subgrupo favorable para redefinir H2.

## Siguiente experimento y entrada exacta

Prioridad propuesta: obtener una **tabla pública completamente anonimizada** de Quadros para los paneles 2f/3, una fila por unidad biológica y región, con ambos marcadores, carga de pTDP-43, escala/normalización, regla de no detección/exclusiones y descripción de agregación de réplicas técnicas. Sin nombres, demografía, variables clínicas o claves reidentificables. Que los autores consideren qué información puede publicarse de forma segura.

Solo después de recibir una fuente pública admisible se fijaría un protocolo de asociación ajustada por carga, sensibilidad a censura/no detección y reglas de exclusión, con efectos e intervalos. Si el archivo no permite enlazar ambos marcadores y patología, o las unidades son desconocidas, no se calcula. No se exige que la asociación sea positiva para aceptar la fuente.

Se deja [una solicitud redactada](DATA_REQUEST_DRAFT.md), **no enviada**. Destinataria propuesta: Clotilde Lagier-Tourenne, una de las tres autoras de correspondencia; dirección publicada en la página del artículo. La consulta de Gmail por nombres/título no devolvió mensajes; no se afirma ausencia universal de correspondencia. No se copian automáticamente las otras dos autoras.

## Verificación y cierre

Protocolo anterior al libro; hash, cabeceras, hojas y posiciones verificados directamente. Tres XML primarios recuperados por Europe PMC y hashados; originales no redistribuidos. Descargas de datos/métodos: 11.551.708 bytes, por debajo del límite de 25 MB. No se descargaron BAM/FASTQ ni matrices de expresión. No hay inferencia nueva ni pruebas de software que ejecutar por esta auditoría documental. CI del repositorio se revisa por commit si se activa. Ciclo de tres candidatas cerrado, sin cuarta fuente por inercia. Ningún contacto enviado, gasto, intervención ni nueva indicación clínica.
