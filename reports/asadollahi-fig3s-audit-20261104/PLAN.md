# Auditoría de viabilidad A25 Fig.3s — 04/11/2026

Autorización: Luis aceptó expresamente el04/11/2026 una auditoría limitada de un archivo funcional público de Asadollahi et al., Nature Genetics2025, DOI10.1038/s41588-025-02361-5. Máximo inicial: una sesión de dos horas. No autoriza un reanálisis inferencial, mensajes, gastos o laboratorio. #37 y #44 mantienen prioridad y estado; la automatización no se reactiva. PR#46 sigue abierta y separada.

## Pregunta y predicción previas a los valores

¿Permite el archivo original reconstruir los valores de carga eEPSC de neuronas WT y R202H del panel3s y asignarlos a cultivos independientes?

Predicción refutable de viabilidad: existen valores por neurona, unidades/grupos explícitos y claves que permitan distinguir al menos tres cultivos independientes por condición, reconciliables con la leyenda. No se predice ni estima un efecto nuevo en esta auditoría.

## Fuente y límites

Archivo único autorizado: `41588_2025_2361_MOESM10_ESM.xlsx`, Source Data Fig.2–6 y Extended Data Figs.4/8, enlazado por el editor y registro MBExC. URL:
https://static-content.springer.com/esm/art%3A10.1038%2Fs41588-025-02361-5/MediaObjects/41588_2025_2361_MOESM10_ESM.xlsx

Se inspecciona primero el manifiesto ZIP/hojas y después únicamente el bloque experimental del panel3s, sus cabeceras/leyendas y metadatos técnicos pertinentes. No descargar Supplementary Data1, vídeos, fotos, tablas clínicas o archivos distintos. No exportar el libro entero a GitHub; conservar URL/hash para reproducción. No ejecutar fórmulas, macros, vínculos externos ni código de autores. Si no puede aislarse el contenido experimental permitido, parar y registrar el motivo sin divulgarlo.

Python estándar reproducible: recuperación acotada a2MiB, tiempo25s, XML dentro de ZIP con límite por miembro y selección de rango/hoja. Sin paquetes nuevos ni datos simulados de investigación. Registrar versiones, parámetros, tamaños, SHA256 de bytes originales y miembros leídos, errores y celdas fuente.

## Controles

- Identidad: DOI/archivo/panel; distinguir A25 Fig.3s de K26 Fig.4d.
- Medida: carga integrada de eEPSC, no amplitud, frecuencia de mEPSC, proteína o PSI. No trasladar unidades por suposición.
- Dos grupos publicados WT/R202H en el mismo ensayo. Unidad medida neurona; unidad biológica cultivo por demostrar. No deducir independencia por fila, nombre parecido o color.
- Contar valores numéricos, vacíos, errores, fórmulas y valores repetidos. Una coincidencia numérica no demuestra duplicación de neuronas. No completar faltantes con0.
- Buscar clave de célula/cultivo, exclusiones, leyenda y procedencia en el bloque permitido. Los cultivos declarados en métodos no reconstruyen el mapa de cada fila.
- Controles negativos de software: una entrada sin mapa, unidad ambigua o metadatos solo de estilo nunca habilita inferencia.

## Decisión y fracaso

GO solo para proponer posteriormente un plan de reproducción si se verifican archivo numérico original, medida/unidades, grupos, claves biológicas y trazabilidad. No se inicia automáticamente ese análisis.

NO-GO inferencial si solo hay agregados, faltan las claves de cultivo o quedan unidades/asignaciones ambiguas. Si existen medidas por neurona sin mapa, registrar disponibilidad parcial y QC estructural, sin p-valores ni comparar efectos. No inventar IDs de cultivo ni abrir otro candidato para sustituir este bloqueo.

Entrega: script y controles ejecutados, inventario acotado, resultados JSON, decisión y motivos, informe breve y actualización de STATE/BACKLOG mediante PR directa a main. Etiqueta: auditoría de acceso/diseño, sin replicación funcional propia, sin evidencia clínica y sin originalidad acreditada.
