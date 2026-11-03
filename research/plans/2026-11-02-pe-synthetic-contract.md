# Contrato PE prospectivo — solo sintéticos

Unidad: (biblioteca explícita,RG,QNAME,unión). Unión en coordenadas intrónicas0-based half-open [fin del exón izquierdo,inicio del exón derecho), hebra XS. Contar una vez por fragmento/unión, aunque ambos mates la apoyen. No convertirlo en moléculas independientes.

Entrada SAM ordenada lexicográficamente por (RG,QNAME), biblioteca como parámetro obligatorio. Fallar si se repite fuera de orden: no usar un diccionario ilimitado de fragmentos. Se procesa un grupo cada vez, con límite de16registros. No se promete compatibilidad con SAM de alineador sin ordenar/cotejar; la producción requerirá colación externa dentro del presupuesto.

Excluir secundarios/suplementarios; exigir exactamente dos primarios, un read1y un read2, ambos paired/proper-pair, mapeados, sin QC-fail, NH=1y20≤MAPQ<255, referencias/posiciones/flags de mate recíprocos y orientación física inward-FR. Registrar huérfanos/pares discordantes/ambigüedad como exclusiones. RG ausente se representa explícitamente; bibliotecas nunca se mezclan. Duplicados marcados se retienen y etiquetan, sin deduplicación molecular.

Soporte de unión: N en CIGAR con M/= /X contiguo inmediatamente a cada lado, anclas≥15primario y8sensibilidad. I/D/S/H/Prompen ancla contigua. XS+/− obligatorio en el mate que aporta N; conflicto de XS entre mates excluye el fragmento. No inferir hebra transcriptómica de flags físicos. Un mate no empalmado puede carecer de XS.

Predicción: los parsers SAM textual y PySAM/HTSlib producen exactamente los mismos eventos y contadores sobre fixtures con resultados prefijados. Casos: apoyo doble/único, distintos eventos, solapamiento, hebra negativa, ancla14/15, inserción junto al N, secundario/suplementario, NH/MAPQ, mate ausente o inconsistente, orientación incorrecta, XSausente/conflictivo, flags duplicación, nombres iguales en RG/bibliotecas distintas, orden/límite de grupo. Ninguna discrepancia permite usar crudos. No benchmark del alineador ni datos biológicos; orientación real y geometría UNC13A quedan pendientes.
