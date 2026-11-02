# HTTPacotado y manifiesto: pruebas locales — 02/11/2026

## Evidencia ejecutada

bounded_http_transport.py implementa transporte HTTPcon destinos permitidos exactos, redirects/proxies deshabilitados, Content-Length único/exacto y rechazo de codificaciones o Transfer-Encoding ambiguos. Cada read1solicita como máximo min(chunk≤65536,saldo,payloadrestante). El ledger se actualiza y persiste al recibir bytes, antes de escribirlos o validar hashes. Las fases/recibos del runner simulado se conservan; sin CLIpara ejecutar manifiestos o URLsreales.

Nueve tests pasan usando exclusivamente servidor local127.0.0.1y un lector instrumentado: éxito/reutilización sin nueva conexión; cuerpo truncado y bytes cobrados; retryexplícito con conservación de dos recibos; retryrechazado por saldo insuficiente; longitud incorrecta sin leer cuerpo; saldo insuficiente antes de abrir conexión; secuencia de lecturas3/3/3/3/3/1para16bytes; checksumincorrecto cobrado; redirecty origen externo rechazados.

Un caso truncado entrega5bytes; un segundo intento completo de16consume21en total. Con presupuesto16, tras consumir5el segundo intento se rechaza antes de otra conexión. Los parciales de intentos previos se conservan. Reintentos máximos2y desde cero, configurados expresamente: no Rangeo reparación de un archivo truncado. La fase globalfailedno se reintenta al reabrir el ledger sin reconciliación. El primer error local fue una colisión de nombres en importación de tests; se corrigió y se registra en errors.json.

## Integridad y alcance del presupuesto

Se exige tamaño y MD5de origen. SHA256externo, si existe, también se compara; en FASTQENAel SHA256de la descarga se calcularía localmente y no se presentaría como referencia externa ya disponible. Archivo final solo se promueve tras integridad; cada intento mantiene recibo atómico. Los archivos y recibos verificados se revalidan en el runner al reanudar.

El límite es de **cuerpo HTTPentregado al lector**, no bytes totales de red. No contabiliza cabeceras, TLS/TCP, paquetes retransmitidos o buffering adelantado de biblioteca/socket. Rechazar una cabecera no prueba cero bytes de red, solo cero bytes de cuerpo leídos por el adaptador. Los sockettimeoutsy guardas entre lecturas no garantizan un deadlinewall-clockde kernel para una conexión hostil de goteo lento; en producción haría falta el supervisor externo apropiado. No se afirma validación de HTTPSexterno, latencia real o velocidad de descarga.

## Preflight real sin ejecución

preflight.json fija las cuatro URLs/MD5/tamaños seleccionados, el índice histórico por URLversionada/SHAy hashes individuales, los hashes de binarios del minigenoma y el contrato UNC13A. Es lectura de manifiestos ya versionados, no descarga o validación actual del índice. FASTQ+índice comprimido suman10.705.490.230bytes frente al límite de12.000.000.000; eso no reserva margen para reintentos completos arbitrarios ni certifica viabilidad.

Se explicitan fases pendientes: restauración de referencia, integridad gzip/EOFy sincronización de mates, prefijo, alineamiento/colación humanos y comprobación de soporte. **DryRunner.processaún usa5sy128MiBpara simulación**: no sirve para ejecutar el índice humano sin parametrizar/verificar los límites de producción. Ningún bloqueo se convierte en resuelto porque el manifiesto enumere una fase.

## Verificación y siguiente tarea

Plan prospectivo:research/plans/2026-11-02-bounded-http-local.md. tests.txtyvalidation.jsonregistran nueve controles locales, compileall correcto. La CI de la nueva cabeza verificará la suite offline. No se incorporan tests que contacten servidores externos ni se necesita descargar datasets para CI.

Única siguiente tarea: implementar/verificar integridad de FASTQpaired-end y selección de prefijo con fixtures gziplocales (EOF/CRC, nombres/mates, conteos y ordinals), además de parametrizar el runner de procesos con límites explícitos del plan en modo dry-run. Prueba negativa si se conservan accidentalmente los límites sintéticos5s/128MiB. Sin FASTQbiológicos, restaurar índice humano o alineamientos hasta cerrar esas fases y el control externo del transporte. raw_execution_ready=false; sin merge, costes, contactos o clínica.
