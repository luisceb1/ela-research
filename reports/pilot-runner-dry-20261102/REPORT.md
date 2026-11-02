# Runner con supervisor: integración simulada — 02/11/2026

## Resultado

Implementado pilot_dry_runner.py con manifiesto/límites ligados por hash, ledger persistido, deadline global sin reinicio, contabilidad acumulada de transferencias y comprobaciones de disco/reserva. process_supervisor_v2.py recibe un checkpointdepresupuesto en su bucle; si la guarda falla, termina el grupo y conserva recibo terminal. No se modifican retroactivamente los datos de recursos del minigenoma.

La CLI solo acepta --simulate: no incluye cliente HTTP, URLs de ejecución o comando de alineador. La simulación transfirió bytes sintéticos a dos archivos, verificó tamaño/MD5/SHA256y ejecutó un proceso Pythonpequeño con el supervisor. La segunda invocación reutilizó las fases verificadas; first-run.json y resume-run.json son semánticamente idénticos, sin transferir bytes adicionales ni reiniciar el plazo. No son archivos FASTQbiológicos ni resultados de un piloto humano.

## Controles ejecutados

Diez tests pasan: éxito y reanudación verificada; cambios de manifiesto/límites; presupuesto acumulado agotado; hash incorrecto y conservación de parcial; archivo verificado alterado; deadline agotado; fase interrumpida; disco/tipo de fase; recibo del supervisor y su reutilización; guarda global que interrumpe un proceso. Compileall correcto. La CI nueva comprueba la suite completa; no se ejecutó localmente la suite histórica entera.

Las fases.startedse escriben antes de operar; solo alcanzan.verifiedtras integridad/supervisión. Las excepciones conservan.failedy los parciales. Un estado.started/failedimpide reanudar automáticamente: requiere reconciliación explícita, no borrar recibos o reiniciar consumos. Artefactos y recibos de proceso verificados se revalidan porSHAal abrir un estado existente. Se rechazan cambios de parámetros o reutilizar el nombre de una fase para otro tipo/operación.

Se usa bloqueo exclusivo del ledger para un único controlador, escritura atómica y sincronización en disco; el ledger conserva los bytes recibidos incluso si la fase falla. No se garantiza transacción de filesystem frente a todas las caídas: si ocurre una caída entre promover el archivo y cerrar el recibo, el siguiente arranque se bloquea como incompleto, sin certificar el archivo por mera existencia.

## Presupuesto y límites

preflight.json calcula el presupuesto del manifiesto real sin ejecutar sus URLs. Mantiene6.349.703.881bytes de FASTQseleccionados, límites de transferencia/disco del plan y disponibilidad actual de espacio. Que el disco encaje no acredita tiempo, memoria, referencia, integridad de pares o posibilidad de ejecutar el piloto real.

La entrada sintética es un iterable de chunks. Si un chunkentregado supera el saldo, se contabiliza completo y se detiene; **esto no certifica un límite estricto de red**. Un futuro adaptador HTTPdebe acotar la lectura al saldo disponible y contabilizar reintentos antes de transferir. Las guardas de disco/RSSson muestreadas; pueden existir picos entre muestras. La fase de proceso conserva timeoutindividual y guardas globales, no una cuota de kernel agregada. No se habilitan comandos que detach/setsidni ejecución multihilo del controlador.

No se han integrado todavía descarga HTTP, restauración del índice, EOF/CRCgzip, sincronización de FASTQ, prefijos ni el comando humano de alineamiento/extracción. Los datos de prueba no validan esos pasos. Las dependencias/rutas del supervisor mantienen los límites descritos en el informe anterior.

## Siguiente tarea única

Implementar el adaptador HTTPacotado y el preflight del manifiesto real con pruebas de transporte local/simulado: saldo por lectura, respuestas truncadas, reintentos contabilizados, hashes y rechazo de estado incompleto. Fijar antes el runner completo de fases y las referencias/binarios por hash, sin ejecutarURLsdeFASTQo descargar el índice humano en esa siguiente validación. raw_execution_ready=falsehasta cerrar esos requisitos. No repetir simulaciones exitosas como progreso biológico.

Plan fijado antes del código:research/plans/2026-11-02-pilot-runner-dry.md. Sin descarga externa, índices humanos, alineamientos, PSI, efectos, inferencia clínica, costes, contactos o merge automático.
