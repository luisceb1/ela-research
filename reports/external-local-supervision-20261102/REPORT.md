# Supervisión externa de transporte y validador — 02/11/2026

## Evidencia

Base: PR36, abf7a54961fa47cd2d2597f7fce7cdb7382b4f21. Plan previo:
research/plans/2026-11-02-external-local-supervision.md. CPython3.12.14/stdlib,
Linux/procfs. Solo servidor127.0.0.1 y lecturas artificiales. Sin datos biológicos,
índice humano, alineamientos, terceros o costes.

79 tests locales pasan, sin omisiones:12 nuevos y67 existentes. tests.txt y
validation.json son la ejecución final retenida; los ensayos iniciales12/12 también
pasaron. No sumar repeticiones como pruebas únicas. Primera CI de análisis falló
en el test de goteo: suponía corte dentro de read1 y reserva exactamente1; puede
ocurrir entre lecturas tras liquidar y ser0. Corregido a0/1, conservando consumo
mayor/igual a body_bytes y bloqueo de reapertura. El caso de cuerpo bloqueado
sigue exigiendo reserva1. Ver ci-initial-failure.txt; no fue pérdida de consumo.
Revisión añadió tolerancia a renombres atómicos concurrentes en la guarda de
disco y fijó límites de supervisión en el descriptor del job antes de ejecución final.

external_local_stage.py lanza un worker fijo bajo el supervisor v2. Solo permite
HTTP a IP loopback literal o la fase paired del manifiesto; no shell arbitrario,
DNS localhost, HTTPS o URL externa. Job exclusivo con límites, manifiesto y deadline;
recibo del supervisor y outcome final con hash del job. Padre libera flock antes
del hijo. El timeout monotónico externo se recorta al plazo persistente restante.
Supervisión de RSS y disco muestreada; límites de memoria positivos explícitos.

Resultados finales en case-summary.json y cases/ (JSON y logs de cada ensayo):

| Control | Resultado observado |
|---|---|
| Cabeceras bloqueadas | SIGKILL por timeout; ≈1,005s;0bytes de cuerpo cargados |
| Cuerpo bloqueado | SIGKILL; ≈1,004s;1byte reservado, recibo HTTP started |
| Goteo cada50ms | SIGKILL; ≈1,005s;20bytes cargados, última reserva pendiente |
| Plazo global1,5s, petición de10s | Timeout efectivo≈1,497s; termina≈1,508s |
| Validador con pausa inyectada y descendiente | SIGKILL; ≈1,010s;2miembros observados; partial sin recibo final |
| HTTP correcto |128bytes exactos cargados; fase verificada reutilizable |
| Paired correcto |3pares escaneados, prefijo2;102bytes de transferencia previos conservados |
| Salida abrupta del worker | Código74 registrado como fallo externo |

Todos los grupos de procesos de estos casos terminan sin miembros vivos. Los
timeouts son controles negativos esperados, no fallos ocultos. Fases internas
started tras corte se conservan y bloquean reapertura; los tests comprueban que
consumo/deadline no cambian al rechazarlas. Job/recibo externo no se sobrescribe.
En la salida74 previa a empezar una fase, el ledger no inventa un intento interno;
el fallo está en el recibo externo y el job exclusivo impide repetirlo con ese nombre.

## Reserva duradera de lectura

El antiguo modo HTTP registra bytes después de leerlos. Para un proceso que puede
recibir SIGKILL, existe una ventana read→save. El nuevo reserve_reads=True fija una
firma distinta y carga el máximo de la próxima lectura antes de bloquear. Cuando
read1 retorna, liquida solo la parte no recibida; si hay interrupción/error incierto,
la reserva queda consumida. Los dos tests de unidad verifican reserva en disco
antes de read1, excepción con carga conservadora y liquidación de lecturas cortas.
El wrapper externo siempre usa este modo; el modo histórico conserva su contrato.

transfer_bytes_consumed puede ser mayor que cuerpo realmente leído después de un
corte. No se devuelve automáticamente ninguna reserva incierta. El recibo HTTP
interno puede quedar started y su body_bytes por debajo de la carga conservadora;
no se reconstruye un total exacto. Se conserva evidencia sin convertirla a verified.

## Interpretación y limitaciones

Se valida corte externo de las operaciones locales ensayadas aunque el worker no
ejecute su guarda, incluido goteo que evita el timeout por lectura. Es evidencia
de ingeniería; no prueba funcional neuronal ni replicación de un resultado ELA.

No es garantía de tiempo real: hay latencia de sondeo/planificación/limpieza. El
wrapper recorta tiempo restante justo antes de lanzar supervise; no certifica un
spawn/preexec bloqueado, parada del anfitrión o muerte del propio supervisor. Se
requiere mismo grupo, sin detach/setsid; un proceso que escape no está cubierto.
RSS no es un cap kernel agregado. Disco también se muestrea y puede sobrepasarse
entre muestras. Presupuesto HTTP sigue excluyendo TLS/TCP/cabeceras y buffering.
No se ha ensayado red externa, DNS, índice humano,900s/6GiB reales o escala humana.
Los límites de tests no validan esos recursos. Producción continúa deshabilitada.

Las rutas temporales, puertos y tiempos de los recibos son de esta ejecución;
no son ubicaciones de datos recuperables. Los fixtures están en código. Para
reproducir y retener recibos nuevos: python scripts/run_external_local_gate.py
--report /tmp/ela-local-supervision-new (directorio nuevo). Los gzip se regeneran;
se conservan sus hashes en los recibos/manifest, no archivos binarios incompletos.

## Siguiente experimento

Única tarea siguiente: auditoría integrada de preparación del piloto, sin ejecutar
descargas. Cotejar contratos, planes, presupuestos, fases, binarios/referencias y
recibos; preparar una lista cerrada de bloqueos y una propuesta concreta revisable
de ejecución. Decidir qué falta antes de habilitar producción, sin inferir que una
CI verde equivale a permiso o viabilidad del piloto humano. raw_execution_ready=false.
PR36 abierta, sin merge automático. No repetir búsquedas científicas cerradas.
