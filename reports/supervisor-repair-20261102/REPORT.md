# Supervisor v2: namespaces y recibos — 02/11/2026

## Evidencia

Se reprodujo la causa del muestreo incorrecto: en este entorno os.getpid() devolvió6y/proc/self apuntó a626. El supervisor anterior comparaba PGIDobtenido con os.getpgid(namespacePID)con IDsdel procfsmontado, mezclando espacios de numeración. El nuevo hijo comunica antes de execsu PIDy PGIDtal como aparecen en su propio procfs; la lectura de RSSusa ese espacio. killpgusa el identificador del namespace de Python, como corresponde al proceso lanzado. En un entorno sin diferencia de namespaces la misma ruta es válida.

process_supervisor_v2.py procesa el grupo completo y distingue procesos vivos de zombis. Los controles conocidos dieron aproximadamente40MBpara una asignación32MiBy65MBpara padre+hijo con24MiBcada uno. No son medidas de HISAT2o del genoma humano. summary.json conserva cifras exactas, identificadores y resultados. Los casos de exceso de memoria y timeoutterminan el grupo; los seis casos ejecutados no dejan miembros vivos tras limpieza.

Siete tests pasan: asignación conocida, memoria de descendientes, corte por memoria, timeoutcon descendiente, salida no cero, preservación/no sobrescritura de recibos y fallo de lanzamiento con recibo terminal. La prueba incluye rechazo de reutilización del mismo nombre. Las fixtures son procesos sintéticos, sin lecturas, alineaciones o transferencias externas.

## Persistencia

Cada comando tiene su propio recibo.started/finishedse persisten mediante fichero temporal,flush/fsync,replaceatómico yfsyncdel directorio; una reserva O_EXCLimpide colisiones. No hay read-modify-write de una lista compartida. Un índice agregado futuro debe derivarse de estos archivos, sin sustituirlos. Los seis recibos nuevos existen y son JSONválidos; los errores y paradas quedan registrados, no solo los éxitos.

Esto elimina la dependencia de la lista común en el nuevo supervisor. **No reconstruye los dos recibos antiguos ausentes ni demuestra retrospectivamente por qué se perdieron.** Los artefactos del minigenoma anterior se preservan intactos; su gate funcional sigue positivo y su RAMhistórica no certificada.

## Límites explícitos

RSSes un muestreo de grupo, no máximo continuo ni límite agregado de kernel. Procesos breves pueden quedar sin medición; se informa None/no observado en vez de certificar cero. El grupo RSSpuede contabilizar páginas compartidas varias veces y es conservador. Se añade RLIMIT_ASpor proceso y afinidad de dos CPU, pero no se equipara ese límite de espacio virtual a una cuota agregada física. No se afirma que el supervisor capture toda subida transitoria entre muestras.

Contrato: los comandos no deben cambiar de grupo/sesión o escapar con setsid; esa fuga no está cubierta. El supervisor es secuencial, con preexec_fn; no se declara seguro para lanzamientos desde múltiples hilos. Desconexiones abruptas/SIGKILLdel propio supervisor pueden dejar un recibo.startedque debe reconciliarse como incompleto antes de reanudar. La supervisión de disco/red y el presupuesto global del piloto no están integrados aquí.

## Reproducibilidad y continuación

Plan previo:research/plans/2026-11-02-supervisor-repair.md. Ejecuciones y logs pequeños en receipts/;summary.json,tests.txtyvalidation.json. Compileall correcto. La CI nueva verificará los siete tests en Python3.11/3.12; la suite histórica completa no se ejecutó localmente. Ningún índice humano, paquete nuevo, alineamiento o crudo se descargó/ejecutó.

**Única siguiente tarea:** integrar supervisorv2en un runner del piloto con planificación/dry-run, presupuestos globales de tiempo/disco/transferencia, hashes, recibos por fase y rechazo de reanudación incompleta. Validar con transporte/procesos simulados, sin iniciar descarga6,35GBni restaurar índice humano. Esta reparación habilita esa integración técnica; raw_pilot_readypermanecefalsehasta verificar el contrato completo. Sin merge automático, costes, contactos o clínica.
