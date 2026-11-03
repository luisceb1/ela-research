# CTRL_R2: ruta IPv4 tras fallo TLS — 03/11/2026

## Evidencia

Luis aporta el intento `532778b6…` ejecutado con bead910: copia del prefijo verificada; fase Range fallida con URLError durante el handshake TLS antes de respuesta/cuerpo. Cargo acumulado sigue en5.603.756.481B, copia local284.799.727B, supervisor exit1/sinviolación/grupo vacío. Duraciónexterna33,5461694s; fase de rango32,35191988945007s (diferencia de epochs aportados). No se inventa un resultado molecular ni se sustituye ese intento.

Consultas de cabeceras posteriores: curlWSLpor defecto daSSLconnectiontimeout; PowerShellInvoke-WebRequestHEAD devuelve200; curl-4WSL devuelve200, Content-Length997549457 yAccept-Rangesbytes. Estas consultas no simultáneas apoyan probar una rutaIPv4; no demuestran queIPv6 sea lacausa ni garantizan descargaRange, estabilidad o rendimiento. Windows no tuvo curl.exe disponible; ese comando no llegó a probar red.

## Cambio

Módulo nuevo `recover_ctrl_r2_ipv4.py`, históricos intactos. Audita SHAexacto deplan aceptado, aceptación, códigoanterior, ledger/recibos/logTLS, ausencia de resultado/sello, grupo vacío y cero bytes/reservas de cuerpo nuevos. Audita también piloto original y comparaSHA de copiafallida con parcial original. Nueva raíz exclusiva para recuperar sólo el mismoR2; disco cuenta ochoárboles.

ConectorHTTPS local resuelve sóloAF_INET y prueba un candidatoTCP; no altera socket.getaddrinfo global ni DNS/Windows/WSL. Se conserva el hostname original para SNI y validaciónTLS; ssl.create_default_context conCERT_REQUIRED/check_hostname activos, sin proxies/redirect/retry. Range206y Content-Length/Range exactos, sinencoding/chunked/multipart; MD5entero007d66223fe35f394284e4ebd631eaef/tamaño997549457 antes de promoción ysupervisor limpio antes de selloIPv4.

Mantiene cargo5603756481B, tramo712749730B yfinalesperado6316506211B, saldo5683493789B bajo12GB. Conserva7267,7210083s anteriores más tiempo de faseTLSfallida leído de metadatos; no descuenta fallo por haber recibido0B. Propuesta pendiente6000s total/5400sHTTP, copia/verificación300scada; mismo27GiB/reserva8GiB (35GiB libresprevios),2CPU/RSS512MiBmuestreada/AS1GiB/socket30s. Preparar offline no acepta ventana ni ejecuta. SHAexacto yaceptación explícita para ejecutar. No descompresión, otrosmates, alineamiento o reinicio automático.

## Validación y limitaciones

28pruebas nuevas: recuperación/rango local artificial, MD5, reserva/timeouts/estado; cadena exacta fallida/cargos/tiempos/copia/grupo; disco ochoárboles; TLSreal localconCAautogenerada yAF_INET observado, recuperacióncompleta sobreTLSIPv4 conchecksums, certificado no confiable yhostnameerróneo rechazados; contextoinseguro rechazado ysocketcerrado anteerror sinfallbackIPv6. CLIworkersupervisado rechaza metadatos ausentes antesdeHTTP ygrupo queda vacío. Resultados agregados/versiones en validation.json/tests.txt; compileall correcto.

Primera pruebaTLSpositiva detectó incompatibilidad `_check_hostname` enHTTPSHandlerPython3.12. Corregido el adaptador para pasar el SSLContext verificado directamente; las negativas comprueban SSLCertVerificationError, no cualquier excepción. Initial-tests ynota preservan el hallazgo. No se modificaron guardas o código histórico.

Positivos artificiales enloopback no acreditan ENA, rendimiento real, método molecular o efectobiológico. DNS puede bloquear hasta intervención del supervisor; caps deRSS/disco son muestreados y siguen los límites previos dehost/I/O yprocesos. No crudos oalineamientos humanos enhostdelagente.

## Siguiente paso

Emitir planIPv4deshabilitado enWSL yrevisarJSON/SHA antesdeaceptación deventana. SiR2quedasellado, preparar adopcióndeambosmates para cómputosinredescargas. No tocar ni relanzar intentosfallidos. PR36abierta/sinmerge; sinPSI,p-valores,rescate obeneficio clínico.
