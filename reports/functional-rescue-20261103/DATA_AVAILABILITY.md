# Disponibilidad y calidad — corte 03/11/2026

| Recurso | Qué se ha inspeccionado | Qué falta | Decisión |
|---|---|---|---|
| K26 manuscrito aceptado | Copia aportada, texto pp.7–11,19–29,35–36,43–45,62; registro KCL vigente | Archivo numérico Fig.4d con célula→cultivo→diferenciación, unidades y exclusiones | NO-GO numérico |
| K26 datos fuente | Declaración p36 de que se proporcionan con el artículo | Enlace/archivo concreto, hojas y claves leídas | Declaración no equivale a tabla recuperada |
| K26 código | p36: MATLAB a JB, R LMM a PH, ImageJ a REJ; iGluSNFR3 público ya auditado en #35 | Código exacto/modelo de Fig.4d, versiones de paquetes; Igor Pro macros del laboratorio espinal según p27 | No confundir código de imagen con datos de patch clamp |
| K24 suplemento | PDF anterior ya auditado, sin tabla individual verificada | No resuelve Fig.4d añadida en K26 | No mezclar números de figura |
| G26 final | DOI, fecha, volumen y resumen verificados en PubMed/Scite; enlace editorial y enlace de autor devuelven 403 | Métodos/suplementos finales legibles y arrays de datos | Métodos finales desconocidos |
| G25 preprint | Texto principal y leyendas; suplemento indexado PDF 7.8 MB devuelve comprobación de navegador | Bytes PDF válidos y tabla numérica con claves | No declarar suplemento leído ni inexistencia universal de datos |
| Motor2026 negativo | Resumen y fragmentos primarios indexados Fig.1/2; ya catalogado en proyecto | Texto/suplementos completos y trazabilidad de cohortes con CTR2025 | No sumar como replicación independiente |

No se recuperó ninguna medición funcional numérica individual nueva. No se hicieron descargas masivas. La primera petición pública de PMC por Python devolvió HTTP203/HTML (5,581 bytes), no artículo ni dataset; se descartó como evidencia de contenido. No se calculó hash de ningún PDF a partir de ese HTML.

La inspección del texto aceptado se hizo mediante lectura del archivo aportado; el SHA256 de bytes `4c0c9e6c0a532dbf62f9630a47f7fb4730c069d7990ccb81a9fd9d1dfa562ef8` procede de la auditoría directa previa del 01/11, **no de una nueva materialización/hash**. La copia histórica del 28/10 tenía un byte menos; no se afirma identidad binaria entre copias o con KCL. No se redistribuyen PDFs.

## Entrada mínima para Fig.4d

Necesitamos amplitud eEPSC por célula en unidad original, identificadores de línea/clon, diferenciación/cultivo, coverslip y célula, condición, día de registro, primera dosis, inicio KD, concentraciones, criterio de exclusión, y procedimiento de extracción de amplitud. Unidades/polaridad son esenciales: corrientes entrantes negativas no se transforman silenciosamente con valor absoluto. Registrar si el archivo ya contiene magnitudes positivas.

Una cifra agregada por condición, 89 puntos sin lote, un p-valor o una imagen no permite reconstruir el LMM. No necesitamos emparejar RNA y función para reproducir eEPSC; sí lo necesitaríamos para estudiar relación molecular-funcional. No inferir ese emparejamiento de etiquetas parecidas.

## Puerta de entrada y parada

Solo se acepta un archivo original con URL/procedencia y versión fijadas, SHA256 local comprobado, claves explicadas por los autores y al menos tres diferenciaciones independientes con los tres brazos identificables. Este requisito operativo no afirma que las tres diferenciaciones publicadas contengan todos los brazos: debe comprobarse. Si no son bloques completos, documentar el diseño real y revisar prospectivamente el plan, sin rellenar celdas ni descartar bloques para forzar el contrato.

El validador nuevo produce únicamente control de entrada, **nunca un efecto**. Requiere una revisión humana documentada de la independencia biológica; las cadenas de IDs por sí solas no la prueban. El archivo `input_contract.json` queda deshabilitado. Sin datos no hay sustitución por simulación, estimación ni prueba inferencial.

Regla de reapertura: enlace concreto nuevo al archivo fuente, versión editorial con adjuntos nuevos o datos aportados autorizadamente. No se autoriza contactar, solicitar acceso, pagar o subir material ajeno por este informe.
