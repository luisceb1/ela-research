# Próxima tarea: alineador y colación en minigenoma — no ejecutada

Construir un minigenoma sintético documentado a partir de la ventana hg38chr19:17641000-17643500ya recuperada, con proyección explícita a coordenadas globales. No índice humano completo o FASTQbiológicos. Fijar HISAT2v2.2.3y su procedencia antes de instalar/compilar; presupuesto de esta prueba:2CPU,2GiB,1GiBdisco adicional,300MBtransferencia y15minwall-clock global, sin reintentos o aumentos automáticos.

Modo primario prospectivo: sin --rna-strandness (unstranded), orientación física FR y pares concordantes; no --tmo, no forzar XSpor la expectativa RFdelkit. Generar fixtures PEcon secuencias conocidas para canónica y ambos brazos crípticos, negativos de hebra/motivo incorrecto, diferentes anclas y duplicación del mismo evento en dos mates. Asegurar que la longitud/multiplicidad de las secuencias permite predicción exacta antes de alinear; regiones multicopia controladas se excluyen porNH.

Comprobar que HISAT2emite XS-por señales de empalme en los positivos, sin inducirlo con una opción de strandness. Si falta XS, la convención difiere o una unión no se recupera con el criterio fijado, detener y registrar; no invertir FR/RFpara mejorar el resultado. La región mínima no reproduce el multimapeo global del genoma humano: su éxito solo valida el flujo pequeño y la proyección.

Implementar colación/ordenación externa lexicográfica (RG,QNAME) antes de pe_fragment_contract.py, con límites reales y prueba de nombres repetidos/RGdistintos; no usar el orden accidental del alineador como garantía. Exigir concordancia exacta de los decodificadores y resultados prefijados, recoger memoria/disco/tiempo/argv/hashes. Ningún éxito habilita por sí solo crudos: referencias/recursos/runner de la fase humana deberán verificarse aparte dentro del plan de6,35GB.

Se mantiene el contraste con cuentas fallido, la PPAUSTMN2reproducida, el bloqueo de procesados UNC13Ay las limitaciones biológicas. Sin PSI, p-valores, rescate, contactos, costes o merge automático. Esta prueba no se ha ejecutado durante la puerta de referencia.
