# Registro de consultas y errores — 03/11/2026

Plan fijado en a62a0d7 antes de consultar las tres familias. Sin cuarto candidato. Los resultados incidentales de motores generales no se abrieron ni se añadieron como candidatas. No se usa el número de resultados como prueba de ausencia.

## Lectura previa, sin nueva búsqueda de fuentes agotadas

Main 9076802: AGENTS, STATE, BACKLOG, PROTOCOL, NEXT_STUDY_GATE; issue #37 y comentarios (ninguno); CLOSURE/COMPLETE_REPORT UNC13A; informes de Humphrey procesado, selección30/10, fraccionación/unidades (límite recogido en estado e informe de selección), independent-splicing, junction-source-inventory, MASTER_EVIDENCE, originality-audit, geo-audit, functional-data-inventory y functional-source-access. Versiones/blob de los localizadores en `prior_sources.tsv`. Se consolidan conclusiones históricas sin volver a descargar sus datos.

## Consultas bibliográficas acotadas

| Canal | Consulta exacta o parámetros | Resultado utilizado |
|---|---|---|
| Scite search_literature | DOIs adg7162, s41591-023-02788-5, abq5622; término `"data availability" OR "data and materials availability" OR "RNA sequencing" OR "GSE" OR "GEO"`; limit3 | Metadatos, extractos y Smart Citations; corrección Irwin visible; Seddighi fulltext denegado |
| Web motor1 | `"Mis-spliced transcripts generate de novo proteins" "GSE"` | Artículo/PMC, sin accessionGSE verificada; no prueba de inexistencia |
| Web motor1 | `"A fluid biomarker reveals" "Data availability"` | Sección primaria remite SRP166282/SRP057819 |
| Web motor1 | `"Mechanism of STMN2" "GSE"` | Sin depósito de uniones verificado |
| Scite search_literature | DOIs abq5622, s41591-023-02788-5 y corrección s41591-024-02966-z; `"GSE" OR "availability" OR "correction"`; limit3 | Texto de corrección del primer; no nuevo dataset |
| Web motor2 | `site:pmc.ncbi.nlm.nih.gov/articles/PMC11325748 "Data and materials availability"` | Texto primario indexado de disponibilidad Seddighi |
| Web motor2 | `site:pmc.ncbi.nlm.nih.gov/articles/PMC10148063 "Data and materials availability"` | Texto primario indexado de disponibilidad Baughn |
| Web motor2 | `site:pmc.ncbi.nlm.nih.gov/articles/PMC11325748 "GSE" "RNA"` | Sin nueva accession verificada; resultados incidentales ajenos ignorados. No se repite |
| Scite read_fulltext | DOIabq5622, offset40000/length8000 y offset48000/length2405 | Dos segmentos finales `source=fulltext`, no artículo completo; unidades de ensayos distintos de RNAseq |

## Accesos primarios y controles de formato

Seddighi: ocho accesos directos de metadatos: PMC vía web (recaptcha), EuropePMC XML(500), PMC vía Python(203/HTML recaptcha), Zenodo web(inaccesible), Zenodo API(200/JSON), ADWB web(shellJS), árbol Git v1(completo), README v1(texto). Límite de ocho alcanzado, no se amplía. Las consultas bibliográficas/Scite de la tabla anterior se registran aparte; no se les atribuyen bytes HTTP no expuestos.

Irwin: editorial web(bloqueo de redirección), EuropePMC XML(200/XML válido), SRA SRP166282(18registros). Se analizó disponibilidad, referencias7/11 e índice de suplementos; no las tablas de participantes. Baughn: PMC web(recaptcha), EuropePMC XML(500), PMC Python(203/HTML recaptcha); disponibilidad recuperada mediante índice de búsqueda y segmentos Scite. No se convierte HTMLrecaptcha en artículoXML ni se llama PDF a ninguna de estas respuestas.

Anotación: UCSC API recuperada por Python(200,8358B); acceso web a esa misma URL falló por reescritura de punto y coma. Se usa solo el JSON realmente recuperado. Documentación oficial de pista/release y formato consultada por web. Datos de versión/ensamblaje en sources.json.

## Errores locales y correcciones

- `git ls-remote` al proxy no pudo obtener credenciales. Se empleó el conector GitHub autorizado; no se buscó credenciales ni se modificó main.
- Un intento de inspecciónHTML importaba BeautifulSoup, ausente. Falló antes de leer contenido; no se instaló. Las respuestasHTML ya identificadas como recaptcha no se usan como textos del artículo. El XMLIrwin se analizó con stdlib.
- La primera materialización local por parche añadía una línea final al sello; se detectó al comprobar hashes. Se restituyó el contenido exacto del blob: 37382B, SHA256a42c2281… y Gitblobe59107a1… coincidentes. El primer resultado provisional con hash89217b56… se conserva solo en caché temporal de esta sesión y no es el resultado entregado. No se modificó el sello de GitHub ni ningún archivoWSL.
- Un intento de restituir varios textos en una sola orden superó el límite de argumentos antes de ejecutar; se completó por archivo con comillas seguras. No afecta a resultados.

No se presentan estos errores de acceso/materialización como resultados biológicos. Metadatos originales temporales de artículos fuera de Git; se persisten solo recibos, hashes, índices técnicos y síntesis propia.
