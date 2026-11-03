# B3 local: flujo PE sin conservar SAM genómico completo — 02/11/2026

Base: PR36,76e1f9b9bd082adf8f7db728758eec548777f2c6.
Pregunta: ¿se conservan soporte objetivo y QC por fragmento al decodificar SAM
en flujo, colar representaciones derivadas y reducir grupos acotados?

Antes del ensayo: usar los cuatro SAM sintéticos ya alineados y fixtures PE del
repositorio. Ninguna alineación nueva, FASTQ biológico, índice humano o red.
Contrastar con los dos decodificadores originales sobre SAM ordenados previos,
para anclas15 y8. No confundir comparación con nueva evidencia ELA.

Diseño: una línea SAM acotada en memoria; texto y HTSlib decodifican CIGAR por
separado. Comparar metadatos y conservar solo campos necesarios y eventos de cada
ruta/ancla en JSON derivado. No retener SEQ, QUAL, CIGAR original o SAM completo.
No filtrar por locus antes de seleccionar pares: conservar todos los eventos
de cada registro para que el QC de hebra no cambie. Acumular globalmente solo el
inventario objetivo; máximo16registros por grupo como contrato existente.

Colación externa en runs limitados por bytes, merges con fan-in y espacio
controlados, orden ASCII(RG,QNAME). Cotas de entrada/línea/cabecera/registros/fila/
chunk/runs/disco/objetivos. Fallar antes de exceder salidas controladas. Memoria
de Python y buffers no son un cap kernel: usar supervisor externo. Recibo started/
failed/verified, hashes y EOF; exigir estado de productor0 además de EOF. El
componente sigue local y no habilita el alineador o producción.

Predicción refutable: cuentas objetivo y QC iguales para cuatro rutas
(texto/HTSlib ×15/8), input desordenado, RGdistintos y doble apoyo; sin payload
de lecturas en disco. Negativos: exceso de cotas, grupo17, productor no-cero,
SAM truncado, tags repetidos, metadatos o decodificadores discordantes, destino
existente y corte externo. Conservar recibos de fallo; no adoptar partials.

Fracaso: discrepancia sin rechazo, QC alterado por filtro objetivo, soporte
doble por mates, crecimiento sin cota, retener SAM/SEQ/QUAL, certificar EOF con
productor fallido o promover un resultado interrumpido. Si pasa, cerrar B3solo
como componente local; integración real y B1/B4/B5seguirán pendientes.
