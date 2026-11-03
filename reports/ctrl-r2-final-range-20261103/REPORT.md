# CTRL_R2: recuperación del tramo restante — 03/11/2026

## Evidencia

Luis aporta recibos del intento IPv4 aceptado con SHAea8d25ad…: copia verificada, fase Range interrumpida por plazo, supervisor−9 con `External phase deadline` y grupo vacío. El parcial tiene876.279.389B. El recibo conserva591.396.864B nuevos, rango desde284.799.727 y un bloque de4.194.304B reservado. El archivo incluye82.798B de ese bloque que no llegaron a registrarse en el recibo antes del corte. Cargo nuevo595.591.168B, acumulado6.199.347.649B. La diferencia4.111.506B entre cargo nuevo y crecimiento real permanece contabilizada.

Quedan121.270.068B para el tamaño esperado997.549.457B. La descarga IPv4 recibió contenido, pero el MD5 entero sigue pendiente; ningún par, alineamiento o dato TDP se ha procesado. La duración monotónica externa5156,817107145s no coincide con el reloj civil de la fase y su ventana5400s. Se conservan ambas observaciones; no se atribuye la discrepancia a suspensión, red o reloj sin evidencia adicional. El snapshot no es un recibo final.

## Cambio

Nuevo `recover_ctrl_r2_final.py`, con trabajadores históricos intactos. Audita SHA exacto del plan aceptado, aceptación, toda la cadena anterior, counters, reserva, rango, archivo y grupo vacío. Copia y hash del parcial en una raíz exclusiva y reutiliza sin cambios el transporte IPv4 y el sellador externo de `recover_ctrl_r2_ipv4.py`. No hay cambios globales de DNS o TLS. Una petición Range876279389–997549456, longitud121270068, MD5 entero007d66223fe35f394284e4ebd631eaef, tamaño y SHA antes de promoción/sello. El sello mantiene el tipo `sealed_verified_ctrl_r2_ipv4`; su plan y raíz identifican este tramo.

Cargo final esperado6.320.617.717B, saldo5.679.382.283B bajo el techo12GB. Conserva7.300,072928190231s anteriores y arrastra conservadoramente toda la ventana agotada5400s:12.700,072928190231s. No usa el snapshot como instante final ni devuelve reservas. Propuesta pendiente2400s total/1800sHTTP, copia300s/verificación300s. A la velocidad media observada, el tramo llevaría unos19min; no garantiza finalización. Mismos27GiB incluyendo nueve árboles/reserva8GiB,35GiB libres al iniciar,2CPU/RSS512MiBmuestreada/AS1GiB/socket30s. Preparar no acepta ni ejecuta; SHA exacto y aceptación explícita de ventana para iniciar.

## Validación y límites

24 pruebas nuevas: recuperación completa artificial y sello con transporte IPv4 heredado; rango/cabeceras/MD5 incorrectos, truncado, reserva y timeout; carga/clock/reserva alterados, últimos bytes no incluidos aún en recibo, archivo cambiado, stop reason y grupo, nueve árboles y reutilización exacta del transporte. CLI worker supervisado rechaza metadatos ausentes antes de HTTP y deja grupo vacío. Validación agregada y versiones en validation.json/tests.txt; compileall correcto. La regresión incluye las pruebas anteriores de TLS real local, certificado no confiable y hostname incorrecto rechazados, y recuperación completa por TLS/IPv4.

Positivos artificiales no certifican ENA, velocidad WSL, alineamiento humano ni interpretación científica. Se mantienen las limitaciones previas de cuotas RSS/disco muestreadas, DNS, I/O y host. No se descargaron crudos humanos ni se alineó en el host del agente.

## Siguiente paso

Emitir/revisar plan deshabilitado WSL y decidir sobre la ventana concreta. Si se obtiene el sello, preparar adopción de ambos mates para cómputo sin redescargas. No repetir el piloto ni editar metadatos históricos. PR36 abierta, sin merge ni PSI, p-valores, rescate o beneficio clínico.
