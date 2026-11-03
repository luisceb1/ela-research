# Puerta prospectiva UNC13A referencia/orientación

No crudos, índice humano ni alineamientos. Pregunta: ¿qué convención de coordenadas de los eventos previamente citados coincide con límites exónicos de referencia y motivos de empalme en GRCh38, hebra negativa UNC13A?

Recuperar respuestas pequeñas UCSC hg38: secuencia chr19:17641000-17643500 y anotación GENCODE en esa ventana; fijar URL/fecha/SHA. No equiparar coordenadas del compendio a intervalos SAM sin comprobarlas. Candidatos históricos: canónica(17641556,17642845),CEizquierda(17641556,17642414),CEderecha(17642541,17642845). Evaluar explícitamente modelos0-basedhalf-open,intrón1-basedinclusivo,límitesexónicos1-based y0-basedclosed; el resultado se acepta solo si referencia y motivos concuerdan, no por señal biológica. XSde fragmentos y strandnessde biblioteca son conceptos separados.

Revisar la descripción GEO ya recuperada y fuente primaria del protocolo, si accesible, para FR/RF. No usar el término strand-specific para adivinar la dirección. Si no hay prueba para el kit exacto, dejar FR/RFno acreditado y definir prospectivamente ruta unstranded con motivos de referencia y XSno forzado por una opción de strandness. Debe verificarse en prueba del alineador antes de crudos. Si un requisito no se puede verificar, conservarlo como bloqueo; no elegir la convención por maximizar cuentas.
