# Acceso a datos funcionales: Keuss y Guo — 01/11/2026

## Resultado
Dos familias auditadas; **cero fuentes aceptadas todavía para un reanálisis numérico**. Ninguna tabla experimental enlazada verificada. Esto es un resultado de acceso/procedencia, no ausencia universal de datos ni un resultado biológico negativo. No se estiman efectos, correlaciones, retrasos o eficacia. No se descarga una tercera familia ni datos masivos.

La revisión se apoya en el plan local research/plans/2026-11-01-functional-source-access.md. Inventario en inventory.tsv; mapa de ensayos en assay_matrix.tsv; recibos técnicos en retrievals.json y fuentes en sources.json.

## Evidencia nueva y reutilizada
- Keuss: índice KCL vigente y sección de disponibilidad PMC comprobados; se reutiliza research/KEUSS_UPLOADED_PDFS_DIRECT_AUDIT_2026-11-01.md. El manuscrito y el suplemento ya examinados no constituyen una tabla numérica enlazada. No se repite su inspección.
- Guo: el XML primario del **preprint** se descargó y validó como XML; su índice repite el mismo suplemento, no dos archivos distintos. El supuesto PDF devolvió HTML, no se inspeccionó como PDF. El acceso editorial final devolvió 403. Scite mostró extractos iniciales del artículo final, pero su lectura lineal devolvió solo resumen y las consultas posteriores denegaron contenido; no afirmar lectura completa. El calendario preprint registra primera dosis antes del KD y evaluación posterior. Por ello no acredita inicio tras déficit funcional confirmado.
- iGluSNFR3: revisión fijada a 0155d8dbe116a09e5e67cae4749675965515a508, árbol completo de 107 archivos. No hay imágenes del estudio con etiquetas enlazadas verificadas; el único MAT observado es un ejemplo de terceros de otra aplicación. Código disponible no equivale a datos del experimento.

El XML se conserva solo como material temporal de lectura. No se incorporan artículos completos, suplementos, tablas clínicas ni imágenes de terceros a Git. Solo se persisten hashes, índices, proyecciones técnicas y síntesis original. Un hash de HTML no es un hash del PDF buscado.

## Qué análisis permiten ahora
| Análisis | Decisión | Requisito para reabrir |
|---|---|---|
| Auditar calendario, ensayos y nivel de unidad | Viable; entrega actual | Nuevas versiones con evidencia que cambie el mapa |
| Reproducir una figura funcional numéricamente | No iniciar todavía | Tabla original con valor, unidad, condición y agrupación |
| Correlacionar RNA/proteína y función | Bloqueado | Claves compartidas y justificación del emparejamiento |
| Inferir rescate iniciado posdéficit | No acreditado | Basal deficitario antes de primera dosis y diseño comparativo apropiado |
| Comparar porcentajes entre estudios | No iniciar | Mismo estimando o modelo puente justificado |

No se exige medir RNA y función en la misma célula. Un diseño de cultivos hermanos puede servir si está documentado. Tampoco hace falta emparejar RNA y función para reproducir **por separado** un desenlace funcional. Esta distinción evita bloquear preguntas más modestas por un requisito que solo corresponde al acoplamiento entre ensayos.

La declaración de réplicas biológicas del artículo se conserva. No conocer su mapa no demuestra pseudorreplicación; impide reconstruir por nuestra cuenta la jerarquía experimental. No reconstruirla a partir de sufijos ni convertir células en diferenciaciones.

## Limitación y regla de cierre
La tabla diferencia índice, contenido leído, auditoría previa, extracto y acceso bloqueado. NO/UNVERIFIED significa que no hay enlace confirmado en los materiales examinados. No se afirma inexistencia en la editorial ni imposibilidad de conseguirlo. Guo final puede incluir cambios no accesibles: los números de figura y la matriz temporal se refieren al preprint.

Las búsquedas de retractación/corrección filtradas en Scite devolvieron cero y una explicación genérica de no indexación, pese a la recuperación previa del DOI. El campo editorialNotices no se devolvió. Resultado **no concluyente**, no una certificación de ausencia de avisos.

## Único siguiente paso
Completar una solicitud técnica **sin enviar** ya especificada en DATA_REQUEST_SPEC.md. El ciclo de búsqueda de estas dos familias queda cerrado; reabrir solo con un enlace concreto a archivos numéricos, una versión editorial nueva o una respuesta de autores obtenida con autorización. No repetir los mismos índices, PDF, replay STMN2, filtros RiMOD/NYGC o búsquedas equivalentes.

Si el acceso no llega, elegir prospectivamente entre una reproducción molecular externa de un evento conocido y una nota metodológica estrecha. Esa decisión no queda ejecutada ni permite anunciar novedad. No abrir AGRN, péptidos o nuevos simuladores para sustituir la evidencia ausente.

## Verificación
Recibos HTTP y firma de formato comprobados; DOI/PMCID extraídos del XML; referencias entre filas y fuentes comprobadas. Revisión documental, sin tests nuevos que reflejen tablas estáticas. La CI del PR verificará el código existente, no acceso editorial ni validez biológica. No contactos, gastos, laboratorio, indicaciones clínicas, FASTQ, matrices individuales o fusión automática.

## Referencias
- Keuss, M. J., et al. (2024). Loss of TDP-43 induces synaptic dysfunction that is rescued by UNC13A splice-switching ASOs. bioRxiv. https://doi.org/10.1101/2024.06.20.599684
- Keuss, M. J., et al. (2026, aceptado). UNC13A splice correction rescues synaptic dysfunction induced by TDP-43 loss. Nature. Registro KCL en sources.json.
- Guo, C., et al. (2025). Cryptic splicing in synaptic and membrane excitability genes links TDP-43 loss to neuronal dysfunction. bioRxiv. https://doi.org/10.1101/2025.08.28.672801
- Guo, C., et al. (2026). Cryptic splicing in synaptic and membrane excitability genes links TDP-43 loss to neuronal dysfunction. Science Translational Medicine, 18(852), eaeb8517. https://doi.org/10.1126/scitranslmed.aeb8517

Scite confirmó metadatos y proporcionó extractos puntuales; su salida de lectura lineal se etiquetó abstract/contentDenied. El acceso de cada versión se conserva por separado. Texto de comprobación mínimo del preprint: “on Days 20 and 27 ... on Day 21” (Results, Fig.4E); esa secuencia apoya la distinción temporal, no una conclusión de eficacia propia.

