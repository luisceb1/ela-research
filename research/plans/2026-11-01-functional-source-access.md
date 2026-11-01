# Plan de auditoría: acceso funcional Keuss/Guo — 01/11/2026
Base: 39e0479306c9e810f8bd3846bba7b79d7b49fba7. Alcance autorizado por Luis: ejecutar inventario y reconciliar planificación; PR revisable, sin fusión.
Pregunta: ¿existen archivos públicos numéricos que permitan reproducir un desenlace funcional y/o enlazarlo con RNA/proteína a nivel de unidad experimental?
Fuentes fijadas: familia Keuss (2024 y aceptado 2026, versiones del mismo trabajo) y Guo (2025 y final 2026); iGluSNFR3 como recurso técnico relacionado. No contar versiones como independencia.
Predicción de viabilidad: al menos una tabla con condición, valor, unidad biológica/lote y cronología. Para acoplamiento molecular-función se exige clave experimental compartida explícita, no misma célula.
Método: indexar los adjuntos efectivamente anunciados, distinguir lectura de contenido, índice, extracto y acceso bloqueado; registrar URL, fecha, tamaño/hash si se obtienen bytes. Reutilizar auditoría previa de los PDF de Keuss sin repetirla.
Límites: dos familias; acceso público normal, sin CAPTCHA automatizado, credenciales nuevas, costes o terceros. Descargar solo documentos pequeños necesarios, no FASTQ o proteómica.
No-go: tablas/identificadores no verificados; o tratamiento previo sin comparación de inicio posdéficit para una pregunta temporal. Falta de acceso no demuestra inexistencia.
Entregables: inventory.tsv, assay_matrix.tsv, fuentes/errores, informe y petición de datos sin enviar si falta el enlace.
Verificación: consistencia entre tablas, fuentes y decisiones; diff documental y CI existente. No crear tests que reflejen tablas estáticas.
Siguiente paso: si no hay fuente aceptada, cerrar este ciclo y dejar una petición concreta o aceptar otra pregunta prospectivamente; no repetir búsquedas equivalentes.


Cronología: el plan local se registró tras orientación documental inicial y antes de la recuperación XML y construcción de inventario. No se presenta como prerregistro externo ni como plan anterior a toda consulta. No se examinaron arrays de efectos.
