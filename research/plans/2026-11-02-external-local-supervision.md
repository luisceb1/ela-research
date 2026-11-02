# Supervisión externa local — 02/11/2026

Pregunta: ¿termina el grupo de trabajo cuando HTTP o el validador se bloquean sin
ejecutar sus guardas cooperativas, conservando deadline, consumo y evidencia?

Controles previstos antes de ejecutar: servidor127.0.0.1 con éxito, cabeceras
bloqueadas, cuerpo bloqueado y goteo inferior al timeout de socket. Validador con
gzip sintéticos y pausa inyectada al existir partial. Descendiente sintético en el
mismo grupo. Sin URLs externas, crudos biológicos, índice o alineaciones.

Método: worker fijo separado y supervisor Linux existente con timeout monotónico
acotado al deadline persistente. Recibo externo exclusivo; no ejecutar comandos
arbitrarios. Worker usa DryRunner y solo HTTP loopback o fase paired. Producción
continúa deshabilitada. Límites de test pequeños y explícitos; no extrapolables.

Corregir antes del ensayo la ventana read->save: reservar duraderamente la cantidad
máxima de la siguiente lectura antes de bloquear. Tras retorno se liquida con los
bytes efectivos; si hay corte, queda consumo conservador, no contador exacto.
No devolver reservas de intentos interrumpidos automáticamente. No cuenta tráfico
TCP/TLS/cabeceras o buffering. El modo histórico conserva su contrato anterior.

Predicción refutable: timeout externo con grupo sin miembros vivos, recibo terminal
externo y ledger interno started/failed que impida reabrir; deadline/consumo no se
reinician. Test de goteo debe cortarse aunque cada lectura tenga progreso. Un caso
normal termina verified y puede reutilizarse sin bytes nuevos. Fracaso: proceso
vivo residual, aceptación de fase incompleta, consumo perdido frente a lectura
reservada o reinicio del deadline. Registrar fallos, tiempos observados y hashes.

Límites: watchdog de usuario, no garantía de tiempo real; tolerancia por sondeo,
planificación y limpieza. No certificar muerte del supervisor anfitrión, grupos
desacoplados, pérdida de máquina o sistema de archivos hostil.
