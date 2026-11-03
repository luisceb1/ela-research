# Recuperación aislada de CTRL_R2 — 03/11/2026

## Evidencia

Salida de terminal aportada por Luis, sin acceso remoto a su WSL. El piloto da8e2e6 aceptó el plan SHA 1a982933968c1d808c9e0e6e0fdc274548ad1f694275288868147c10e7b4887a. Preflight y copia local de CTRL_R1 verificados; CTRL_R2 quedó started y el supervisor terminó con -9, error de límite acumulado de transferencias y grupo vacío. No pares, alineamiento ni TDP iniciados.

El recibo duradero de CTRL_R2 conserva 281.018.368 B recibidos, con un bloque de 4.194.304 B reservado. El archivo real mide 284.799.727 B: puede contener bytes del último bloque que el recibo todavía no reflejó antes del SIGKILL. Cargo nuevo 285.212.672 B, total 5.603.756.481 B; diferencia 412.945 B sin reembolso. El parcial se identifica por SHA calculado al preparar; aún no está validado contra el origen.

El último ledger registra 1.773,5246675014496 s en esta ejecución y 7.241,245675802231 s acumulados; no es un cierre final. El padre alcanzó el techo de 1.800 s. La propuesta conserva el snapshot original y arrastra conservadoramente los 1.800 s completos, más 5.467,721008300781 s anteriores: 7.267,721008300781 s. No se reconstruye un tiempo exacto de parada. El reloj civil y la duración monotónica del supervisor no concuerdan; no hay evidencia para atribuirlo a suspensión, ajuste de reloj o a la red exclusivamente. Se mantienen ambos límites; no se altera el código histórico para ocultar el fallo.

## Cambio

Nuevo módulo `recover_ctrl_r2.py`, separado de los trabajadores anteriores para conservar sus identidades. Audita el job exacto, aceptación, fingerprint, preflight, cadena sellada de R1/índice, recibo de grupo vacío, snapshot, reserva y parcial. Copia y verifica el prefijo en una raíz nueva. Reutiliza el transporte Range ya probado: una sola solicitud HTTP206, Content-Range y Content-Length exactos, sin proxies, redirects, respuestas completas, contenido codificado, chunked o multipart. MD5 completo esperado 007d66223fe35f394284e4ebd631eaef y tamaño 997.549.457 B antes de promoción; SHA256 completo queda en el sello. No retry ni reinicio del piloto, descompresión o alineamiento.

Tramo restante 712.749.730 B. Cargo final esperado 6.316.506.211 B, saldo 5.683.493.789 B bajo el mismo techo de 12 GB. El cargo conservador anterior no se rebaja. Todos los archivos originales se conservan.

Propuesta deshabilitada: NUEVA ventana 6.000 s (100 minutos), incluidos hasta 5.400 s (90 minutos) de transferencia, copia 300 s y verificación 300 s. A la velocidad media aproximada del intento previo, el tramo llevaría unos 75 minutos; no es garantía de rendimiento ni de finalización. Socket 30 s, 2 CPU, RSS muestreado 512 MiB, AS por proceso 1 GiB. Mismo límite de disco 27 GiB incluyendo siete árboles del linaje, reserva libre 8 GiB; exige 35 GiB libres antes de iniciar. Sin cambio de umbral, número de bibliotecas o pregunta científica. Preparar no acepta la ampliación; ejecutar requiere SHA exacto y aceptación explícita de la ventana adicional.

## Validación y límites

24 pruebas nuevas: Range real contra HTTP local con datos artificiales, archivo completo/MD5/sello, errores de respuesta, truncado, corrupción, timeout y reserva, original modificado, grupos activos, snapshot started tras SIGKILL, discrepancia de bytes duraderos, contabilidad conservadora de reloj, siete árboles de disco y monitor externo ante lectura bloqueada. CLI worker supervisado falla antes de HTTP con metadatos ausentes y deja grupo vacío. Validación total y versiones en validation.json y tests.txt. Primer fallo de fixture (mock de alias SHA inexistente) conservado y corregido; no se cambió una guarda para hacerlo pasar. Compileall correcto.

Los positivos son artificiales; no certifican ENA, velocidad WSL, alineamiento humano o validez biológica. RSS y disco se muestrean; se conservan los límites previamente documentados del supervisor y del host. No se han descargado crudos humanos en el host del agente.

## Siguiente paso

Emitir y revisar el plan deshabilitado real en WSL. Después, decidir sobre la nueva ventana concreta; no ejecutar el piloto fallido ni editar su ledger. Si se obtiene un sello de CTRL_R2, quedará preparar la adopción de ambos mates para un piloto de cómputo sin redescargarlos. No PSI, inferencia, rescate o beneficio clínico; PR36 sigue sin merge.
