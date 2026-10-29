# Inventario público de datos funcionales — 29/10/2026

## Evidencia ejecutada

**Ninguna de las seis fichas de ensayo/versión permite reconstruir el contraste posdéficit propuesto con los materiales inspeccionados.** No es un resultado experimental negativo, ni prueba de que esos datos no existan en otro lugar. Son seis proyecciones de cuatro familias de publicaciones, no seis estudios independientes. No se calcularon efectos, p-valores o potencia.

El inventario se planificó en `research/plans/2026-10-29-functional-data-inventory.md`. Registro curado: `research/references/functional_data_inventory_20261029.json`. `inventory.tsv` distingue desconocido de ausente en la proyección inspeccionada. Los calendarios se fundamentan en auditorías anteriores de métodos, no se infieren de la forma de curvas o de nombres de archivos.

| Ensayo/versión | Material verificado | Falta para el contraste propuesto |
|---|---|---|
| Keuss2024 neuronal ASO | XML público y suplemento PDF recuperado; índice PMC AWS con nueve objetos | No recuperamos una tabla de registros MEA con unidad/diferenciación/tiempo/dosis. Además, el calendario neuronal ya auditado es concurrente |
| Keuss aceptado2026, MEA late-KD | Curación previa del manuscrito aceptado y registro institucional; enlace PDF público vuelve a403 | Datos fuente de esta versión no recuperados; ASO DIV14 precede KD tardío DIV33. No usar preprint como datos del aceptado |
| Chan2026, Fig7f–i | XLSX fijado por hash, cuatro hojas con etiquetas DIV y valores agrupados; dosis inicial DIV4 según figura | Falta clave estable de pozo/diferenciación y enlace explícito de cada observación con tiempo y primera dosis. Sí hay trayectoria de crecimiento previa: no confundir el bloqueo con ausencia de cualquier basal |
| Chan2026, Fig8b/c | Dos hojas de datos fuente y calendario específico | Falta mapa por chip/diferenciación; primera dosis inmediatamente posaxotomía, no brazo seleccionado tras deterioro funcional persistente |
| Beccari2025, Fig7 | XLSX de Zenodo y27cabeceras TIFF auditadas previamente | Sin enlace axón/imagen/cámara/diferenciación. No emparejar filas24/48h por posición. Expresión anterior a lesión |
| Baughn2023, función neuronal | XML autor-manuscrito recuperado; disponibilidad y referencia a DOCX suplementario | No se recuperó registro bruto con claves de tráfico/pozo/diferenciación. Tratamiento posterior al inicio del KD no demuestra déficit funcional medido antes de la dosis |

## Nuevos accesos y controles

Keuss2024: `https://pmc-oa-opendata.s3.amazonaws.com/PMC11230273.1/media-1.pdf`,3272060bytes, SHA256`b5319cef383db704843c17fc4f62c6c95557d663eed08a7b512fdc21a14ae283`. Tiene11páginas. Se extrajo texto con Poppler; no se digitalizaron gráficos ni se interpretaron valores desde píxeles. El texto contiene Extended Data Fig1–7 y Tables1–4 (reactivos, oligonucleótidos, anticuerpos, software). No se localizó allí un manifiesto de registros experimentales. La declaración del XML «Source data is provided with this paper» no constituye por sí sola un archivo de registros recuperado. El índice de objetos de esta versión no contiene un XLSX/CSV independiente; eso limita este depósito concreto, no todos los repositorios posibles.

Baughn2023: XML oficial PMC AWS138129bytes, SHA256`52929e64b9b48918412e5ef3865a5bc78713bfd7deab19c6d063ecfefa7ea6bb`; no se considera idéntico a otras serializaciones del mismo manuscrito. El índice de esta versión contiene tres objetos: JSON/TXT/XML. La página PMC sí enlaza DOCX suplementario; su URL devolvió1817bytes de HTML/preparación, no ZIP/DOCX válido. No se analizó ni se declaró ausente el contenido del suplemento no recuperado. Disponibilidad remite al manuscrito/suplemento y materiales bajo solicitud/MTA; no se inició ninguna solicitud.

KCL aceptado: URL observada `https://kclpure.kcl.ac.uk/portal/files/391373721/LossOfTDP_Keuss_GreenAAM.pdf`,403. El registro institucional sigue accepted/in press6octubre2026. La lectura previa de una copia aportada no convierte este bloqueo de datos fuente en resuelto. Registro y preprint no se cuentan por separado como replicación.

Chan/Beccari: se reutilizaron las proyecciones ya auditadas, sin fingir una segunda extracción independiente. Los hashes de los XLSX locales se volvieron a comprobar; detalles y URLs en sources.json. La tabla Figure7 de Beccari contiene diferente número de observaciones a24/48h: cantidades de filas no identifican ni emparejan unidades. En Chan, valores por columna tampoco identifican diferenciaciones. No se rellenaron metadatos faltantes ni se transfirió calibración entre imágenes.

## Interpretación y límites

Para reconstruir el contraste necesitamos claves de unidad y lote biológico, tiempo de observación, enlace de primera dosis, basal emparejado, inicio tras déficit documentado, comparador temporal y desenlace funcional. Cada requisito se registra como true/false/null con localizador; el código no deduce identidades por orden ni transforma desconocido en no existente. El registro es curación manual y requiere revisión científica: una marca true no autentica por sí sola el diseño de un experimento.

Algunas fuentes aportan calendarios a nivel de ensayo, no por fila; otras contienen resultados tabulados sin manifiesto. Un bloqueo de acceso y un calendario que responde a otra pregunta son límites distintos. No se propone obtener una comparación posdéficit mediante digitalización de curvas preventivas o agrupación de estudios/modelos. La auditoría no cuestiona automáticamente los análisis originales: delimita lo que podemos reconstruir para **nuestra** pregunta.

## Reproducción, pruebas y decisión

`python scripts/inventory_functional_data.py` genera inventory.tsv y summary.json a partir del registro curado. Siete pruebas nuevas verifican el contrato positivo sintético, cada enlace faltante, acceso declarado, registros numéricos, temporalidad y desconocido frente a ausente. El control sintético no es evidencia experimental. Suite completa: **140tests OK**. Hashes/versiones/comandos en run.json. No se amplió clínica individual ni se ejecutaron macros, contactos o experimentos.

**Decisión:** contraste funcional posdéficit bloqueado con estos materiales; propuesta v0.4 permanece conceptual y no certificada original. No repetir esta búsqueda sin un nuevo depósito/enlace primario. Siguiente tarea segura seleccionada: QC de cobertura del cruce crypTE, comenzando por las36identidades de referencia no resueltas y278coincidencias de coordenadas con gen ambiguo; revisar procedencia/identificadores sin reparar datos por proximidad. No priorizar dianas ni declarar novedad por no coincidencia. Esta selección queda registrada en STATE/BACKLOG, sin autorización de laboratorio o comunicación.

## Referencias y datos

- Keuss, M. J., et al. (2024). *Loss of TDP-43 induces synaptic dysfunction that is rescued by UNC13A splice-switching ASOs* [Preprint]. https://doi.org/10.1101/2024.06.20.599684 ; PMC11230273.
- Keuss, M. J., et al. (2026, aceptado). *UNC13A splice correction rescues synaptic dysfunction induced by TDP-43 loss*. Registro: https://kclpure.kcl.ac.uk/portal/en/publications/unc13a-splice-correction-rescues-synaptic-dysfunction-induced-by-/ .
- Chan, T. K., et al. (2026). *Human iPSC-derived motor neurons with TDP-43 nuclear loss present early ALS pathological phenotypes*. https://doi.org/10.1038/s42003-026-10832-6 ; fuente/hojas en reports/chan-timing.
- Beccari, M. S., et al. (2025). *Stathmin-2 enhances motor axon regeneration after injury independent of its binding to tubulin*. https://doi.org/10.1073/pnas.2502294122 ; https://zenodo.org/records/15346391 .
- Baughn, M. W., et al. (2023). *Mechanism of STMN2 cryptic splice-polyadenylation and its correction for TDP-43 proteinopathies*. https://doi.org/10.1126/science.abq5622 ; PMC10148063.
