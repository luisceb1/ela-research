# Anotación externa de1901uniones

Pregunta: ¿cuántas uniones con soporte asignado positivo, ausentes de ENST internos, coinciden exactamente con GENCODEv47completa bajo mismo gen/cromosoma/hebra/límites intrónicos?

Predicción refutable: puede haber coincidencias externas pese a ausencia en ENST locales; si no se encuentran, no implica novedad. Separar gen ausente de referencia, locus discordante y unión no encontrada con gen reconocido.

Método: verificar hashes de tabla de pertenencias y GENCODE; agrupar exones por transcrito sin asumir orden consecutivo, deduplicar y comparar claves1-based intrónicas. Tests de coordenadas, hebra/gen, intercalación y soporte. No reestimar expresión ni significación.

Localizar además el catálogo primario Bolger/crypTE. Solo cotejar si se dispone de tabla/convención inequívocas; si no, documentar acceso/esquema pendiente y no convertir ausencia de coincidencia GENCODE en evento nuevo. Entrega reproducible, sin datos individuales ni contacto externo.
