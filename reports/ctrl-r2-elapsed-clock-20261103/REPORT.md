# CTRL_R2: control de tiempo independiente del reloj civil — 03/11/2026

## Evidencia y diagnóstico

Luis aporta el fallo del intento de continuación:15,526642242s externos, exit−9, error genérico External clock/body cap y grupo vacío. Estado7.226.257.234B bajo techo12GB, fase Range fallida conRuntimeError después de623.663B recibidos,4MiB reservados. Parcial900.998.714B; quedan96.550.743B. No MD5 entero, pares o alineamiento. Se conserva cargo conservador3.570.641B por encima de lo recibido en este intento.

El guard anterior agrupaba retroceso civil, deadline civil y cuerpo fuera de rango. El snapshot está dentro del presupuesto y alejado del deadline; el corte temprano y las discrepancias temporales anteriores apuntan al reloj. No se registró el valor exacto de time.time que disparó el guard ni la causa del sistemaWSL. Una prueba reproduce el falso corte del guard anterior al hacer retroceder el reloj civil con presupuesto y duración disponibles. No se afirma diagnóstico definitivo de hardware, suspensión o sincronización deWindows.

## Cambio

Módulo aislado recover_ctrl_r2_clock.py, históricos intactos. Mantiene transporteIPv4/TLS y contabilidad. Cambia plazos a LinuxCLOCK_BOOTTIME compartido por padre/trabajador y liga el plan alboot_id actual. Fechas civiles informativas; el guard y sellador usan ticks/intervalos y verifican boot, límites total/fase y cuerpo. Padre revisa vencimientos sin depender de otra lecturaHTTP. Su tick se toma después de leer el estado para evitar confundir un estado concurrente recién guardado con un reloj que retrocede. Diagnóstico de cambios de offset civil acotado a16 entradas.

El nuevo sellador comprueba duraciones y vencimientos reales, estado completo, checksums/recibos, cuenta de cuerpo y supervisor limpio. No exige fechas civiles crecientes ni finge epochs monotónicos. Archivo final se acepta únicamente tras MD5entero007d66223fe35f394284e4ebd631eaef/tamaño997549457 y SHA256 registrado.

Recupera sóloRange900998714–997549456. Cargo inicial7.226.257.234B/finalesperado7.322.807.977B/saldo4.677.192.023B bajo12GB. Incluye la misma reserva manual de navegador997.549.457B ya aceptada, no se suma otra vez. Su consumo real sigue sin medir. Conserva los metadatos y reserva de reloj anterior; arrastre conservador16.300,072928190231s no representa tiempo observado.

Propuesta pendiente: mismos2400s total/copy300s/range1800s/verify300s,27GiB onceárboles/reserva8GiB(35libres previos),2CPU/RSS512MiBmuestreada/AS1GiB/socket30s. Sólo cambia la base de reloj en un intento nuevo aceptado; no se edita ni reabre el anterior. Preparar deshabilitado sin red y ejecución conSHAexacto/--accept-elapsed-clock-window. Nootrosmates, retries, descompresión o alineamiento.

## Validación y límites

32 pruebas nuevas: reproduce guard anterior; retrocesos y saltos civiles grandes; recuperación completa/checksum y sello pese a esos saltos; deadlines transcurridos reales total/fase; trabajador bloqueado vigilado por padre; reloj transcurrido inválido/retroceso; cambio deboot; lectura concurrente; sello falsificado en deadline rechazado; reserva/cargo/prefijo/grupo/cadena; onceárboles; respuestasRange/MD5/timeout; CLIsupervisado falla antes deHTTP ante metadatos ausentes y deja grupo vacío. RegresiónTLSlocal previa conserva certificados y hostname verificados. Total/versiones envalidation.json/tests.txt ycompileall correcto.

Dos fallos iniciales de fixtures quedaron conservados: alias de shutil yconstanteGiB usados por tests procedían del módulo anterior. Se corrigieron los mocks sin debilitar guardas. No haycrudos humanos ni alineamientos enhostdelagente. Positivos artificiales no certifican ENA/WSL o validezbiológica. CLOCK_BOOTTIME cuenta suspensiones que contabilice el kernel; no se ha ensayado aquí suspensión real deWindows/WSL. RSS/disco siguen muestreados; host/I/O/DNS conservan limitaciones previas.

## Siguiente paso

Preparar y comprobar descriptorWSL y ejecutar con aceptación explícita de los mismos40/30min mediante reloj transcurrido. De obtener sello, adoptar ambosmates para cómputo sólo delcontrol, sin redescargas. Mantenertodoslosintentos; PR36sinmerge. NoPSI,inferencia,rescate o beneficio clínico.
