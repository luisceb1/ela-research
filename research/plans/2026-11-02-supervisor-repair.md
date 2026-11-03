# Supervisor v2: plan prospectivo, sin alineaciones

Pruebas de procesos sintéticos: comando rápido, fallo explícito, asignación conocida de32MiB, hijo+ nieto con asignaciones independientes, memoria por encima de límite de prueba y timeoutcon descendientes. Presupuesto de la prueba60s,2CPU,512MiBRAM,10MBdisco; ningún dato externo o alineamiento. Timeout individual≤5s; negativos por memoria usan límites deliberadamente bajos, sin acercarse al máximo real del entorno.

Hipótesis: los identificadores de os.getpid y /proc/self difieren por namespaces; obtener del propio hijo su identificador procfs antes de exec, leer PGIDdel mismo procfs y sumar RSSde ese grupo en ese espacio. killpgse mantiene en el espacio de IDsde Python. No mezclar numeraciones. Prohibir cambios de sesión/grupo por el comando; la prueba no certifica procesos que escapen con setsid.

Recibo por comando con nombre único, estado started/finished y escritura temporal+fsync+replace+fsyncdirectorio. Conservar errores/timeouts; impedir sobrescritura y regenerar índices desde recibos, sin sustituir los registros del minigenoma. Un proceso demasiado breve puede escapar al muestreo; marcar RSSno medido, nunca cero certificado. Límites RSSson watchdogmuestreado, no garantía de kernel/cgroup. Usar RLIMIT_ASadicional por proceso de prueba y afinidad2CPU. No extrapolar benchmarks a genoma humano.
