# Plan: esquema y comparabilidad del catálogo crypTE

Pregunta: ¿qué suplementos del preprint Bolger DOI10.64898/2026.01.09.698641 contienen catálogos estructurales comparables con las 1901 uniones compartidas, y permiten verificar exactamente gen, ensamblaje, hebra y límites intrónicos?

Base: main 8dfa7ce7c4cc77f28185eaa286e681b0c9d5ed39. XML primario PMC12803201 fijado por SHA256 en el informe GENCODE anterior; comprobar hash antes de extraer. Fuentes adicionales solo primarias y públicas, con URL, fecha, tipo de archivo, tamaño, hash y errores registrados.

Método previsto: extraer llamadas a tablas de los párrafos del XML y distinguir descripción semántica de nombres genéricos media-N. Recuperar primero la leyenda/índice de suplementos. No asumir que media-N corresponde a Tabla SN. Elegir después solo tablas de anotación estructural autorizadas; no descargar/importar suplementos clínicos por persona. Inspección XLSX de solo lectura, sin ejecutar fórmulas, macros ni enlaces externos.

Controles: identidad de DOI/PMC y XML; medios deduplicados; correspondencia explícita tabla/archivo; campos y coordenadas no inferidos por extensión. Los eventos TSS/ApA/TE-exón y las uniones sin TE son categorías distintas. Un gen compartido o intervalo TE solapado no cuenta como coincidencia exacta de unión.

Predicción refutable: podremos documentar qué tipos de eventos y tablas son pertinentes. Solo ejecutar cruce exacto si se verifican ensamblaje y transformación inequívoca de coordenadas a intrón1-based inclusivo para mismo gen/cromosoma/hebra. Si falta esa información o el acceso a bytes, resultado = comparabilidad no establecida, no cero coincidencias.

Criterio de fracaso/bloqueo: HTML en lugar de Office, fuente no identificable, archivo clínico personal, esquema ambiguo o convención sin verificar. Registrar fallo y continuar con mapa de tablas/métodos y otra ruta primaria. Entregable mínimo: inventario semántico reproducible, elegibilidad/motivo y próximos pasos; sin inventar cruce, novedad, significación o función.

Validación: pruebas automatizadas con XML sintético (deduplicación, referencias ambiguas, archivo noOffice, límites de archivo y selección estructural); suite completa existente. Registrar resultado y errores en reports/author-catalog-schema, actualizar estado/backlog y preparar PR breve desde main. Sin merge automático.
