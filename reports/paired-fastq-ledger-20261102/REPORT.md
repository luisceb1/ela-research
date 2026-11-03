# Integridad paired ligada al ledger — 02/11/2026

## Evidencia

Código ejecutado: paired_fastq_phase.py, integrado mediante DryRunner.paired_fastq.
Plan previo: research/plans/2026-11-02-paired-fastq-ledger.md. Base remota
b1b0f0b63191f79771f2a9f184380c51498593a7, PR36. CPython3.12.14, stdlib.

67 tests locales pasan:19 nuevos de integración +48 de FASTQ/runner/límites/HTTP.
No equivalen a suite completa o experimentos independientes. Compileall correcto.
tests.txt y validation.json registran ejecución final. Entre los nuevos controles:
salida dura os._exit(73) durante validación conserva started y prefijo partial;
KeyboardInterrupt conserva failed; ambos impiden reabrir. También se rechazan
CRC tardío, prefijo cambiado, recibos incompletos/alterados, identidad/orden/límites
cambiados y modificaciones de fuente durante el scan. Un test utiliza un servidor
HTTP127.0.0.1 real con dos peticiones, transfer_http y reapertura sin nuevas peticiones.

Fixture retenido en executed: manifiesto, ledger, result y recibo finales. Tres
pares artificiales, prefijo exacto de dos. Reapertura conserva ledger entero,
102bytes transferidos y deadline200 usando reloj inyectado100→101. No mide tiempo
real. Los gzip pequeños se regeneran con run_paired_fastq_ledger_fixture.py;
sus hashes están en manifiesto/result. No se almacenan como texto gzip inválido.

Firma: política v1, contrato ordenado del manifiesto, identidades, prefijo, recibos
ledger de transferencia y fingerprint de manifiesto/límites. Recibo HTTP final,
cuando existe, se coteja por estado/tamaño/MD5/SHA y se fija además su SHA256.
Result y recibo de fase se fijan por SHA; prefijos se rehashean al reutilizar.
Entradas comprimidas completas se rehashean por streaming antes/después del scan.
MD5 esperado procede del manifiesto y debe coincidir con transferencia verificada;
SHA local no se presenta como hash independiente del proveedor si no existía.

## Interpretación

El prefijo certificado está ligado al origen transferido y al presupuesto original.
Reanudación significa reutilizar una fase verificada; no reparar una fase fallida.
Una salida huérfana o result aislado jamás se adopta automáticamente. La promoción
de la fase exige recibo final; un fallo posterior puede dejar result verified pero
ledger failed, que bloquea uso. Ambas capas son necesarias.

## Limitaciones

Ingeniería local con sintéticos, sin inferencia biológica o rescate funcional.
No FASTQ biológico, índice humano, alineaciones, gastos o contactos. Producción
deshabilitada. Las guardas son cooperativas y el watchdog RSS es muestreado;
ningún certificado de límite kernel, red externa o deadline duro de socket.
Se exige que ningún proceso externo modifique los archivos durante validación;
los rehash detectan cambios persistentes, no garantizan aislamiento ante un escritor
hostil que restaura bytes. El ledger no es una firma criptográfica contra ataques.
La política FASTQ previa sigue limitada a cuatro líneas/ACGTN, sin unicidad global
de QNAME o inferencia Phred. Rehashear fuentes añade I/O local, no bytes de red.
Los recibos históricos incompletos se preservan; no se reconstruyen.

## Errores y correcciones

Primera regresión del runner:3 errores por imports diferidos tras retirar scripts
de sys.path en tests existentes. Imports cargados al inicio. Segunda regresión:
1 error porque guard de presupuesto se evaluaba antes del rechazo de una fase
fallida; ahora se comprueban todos los estados antes de revalidar archivos. La
ejecución final de67tests pasa; no se ocultan estos intentos como éxito inicial.

## Siguiente experimento

Única puerta siguiente: supervisor externo del transporte HTTP y del validador,
solo con servidor local lento/bloqueado y sintéticos. Comprobar corte global duro,
limpieza del grupo y conservación de consumo/recibos ante terminación abrupta.
No habilitar producción o descargas reales por superar este gate local. PR36
permanece abierta y sin merge automático. raw_execution_ready=false.
