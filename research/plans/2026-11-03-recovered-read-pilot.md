# Piloto con CTRL_R1 recuperado

Evidencia previa: Luis aporta sello sealed_verified_ctrl_r1,960856963B/MD5ed58daa011d6508a3e8d1f05bc39fc29/SHA298a8b4769fcd5434f883706c873d56795c5a20d855917d80a391b2e5c38beff; cargo5318543809B/saldo6681456191B. No alineamiento. Pregunta: ¿puede continuarse el piloto sin repetir índice/CTRL_R1 ni borrar cargos o fallos?

Diseño: nuevo módulo aislado para no cambiar identidad del trabajador histórico. Cadena sellada de recuperación/índice, estado nuevo con cargo anterior, copia/hash local del mate antes deHTTP. Sólo3HTTPrestantes, CTRL_R2 primero, luego prefix/computeCTRL yTDP condicional al umbral20. Se reutilizan íntegramente algoritmoPE, validador de pares, preflightíndice,argvHISAT2 ystreamcompacto.

Plan deshabilitado; nueva ventana7200s total/1800s acumulados de transferencias(incluye copia local conservadoramente). La copiaCTRL_R1≤180s, preflight≤180s. Cap de cuerpo12GB intacto. Se propone disco27GiB yartefactos18GiB, en vez de25/16: preservar todos los parciales/copia de960MB exige margen adicional, sin borrar evidencia. Demás particiones2GiBprefix/6temporales/.5dependencias/.25recibos yreserva8GiB,2CPU,RSS6/AS8 conservados. Se exige aprobación exacta deSHA/ventana/recursos, no autoriza por preparar.

Predicción: fixtureadopción no emiteHTTP y conservaSHA/contadores; alteración de dato/sellos/cargo/recursos/código/root falla. Workerreal con metadatos ausentes falla antes deHTTP. Positivos de datos/stream ya probados con fixtures; no alineamiento humano del agente. Criterio de fracaso: descarga repetida deR1, contador a0, promoción corrupta o ejecución sin aceptación. No resultados biológicos nuevos.
