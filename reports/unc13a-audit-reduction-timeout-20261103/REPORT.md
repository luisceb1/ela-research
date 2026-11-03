# Corrección tras el límite de reducción de la auditoría UNC13A

## Evidencia

El usuario aporta estado y recibo del intento `-locus-audit-01`, resumidos en `operator-failure-evidence.json`. Verificación 20,030 s; preparación 6,058 s; productor 543,471 s y resumen HISAT2 completo con los mismos números globales del control. La fase pendiente era `reduce`, iniciada en tick 576,575804164 con deadline 876,575804164: exactamente 300 segundos. El supervisor cerró el grupo con salida -9 y sin miembros vivos tras 869,893 s desde su propio inicio. Los registros son consistentes con expiración real de esa fase; no muestran un salto del reloj. No hay inventario regional verificado ni nuevo resultado biológico. El control anterior permanece sellado con cobertura insuficiente.

## Corrección

Nuevo ejecutor aislado `unc13a_locus_audit_v2.py`; los ejecutores históricos, el pipeline regional, objetivos y filtros quedan intactos. La guarda anterior consultaba metadatos del estado y arranque en cada checkpoint. En un merge externo hay muchas comprobaciones por fila. La guarda del trabajador usa ahora su estado en memoria y comprueba el tick/plazo en cada llamada; el padre lee el archivo independientemente. Arranque, disco y tamaño del log se muestrean cada 0,25 s. Se conservan comprobaciones de retroceso, política, secuencia de fases, presupuesto y vencimiento real. Los errores incluyen motivo, fase, tiempo transcurrido y deadline.

Se redistribuye la misma ventana máxima de 2100 s (35 minutos): verificar 180, preparar 120, productor 900, reducción 720, finalizar 60; suman 1980 s y margen de 120 s. Los tiempos observados de verificación/preparación fueron inferiores a sus nuevos límites, sin garantía de rendimiento futuro. No se aumentan RAM, CPU, red ni disco: 2 CPU, RSS de grupo muestreada 6 GiB, AS por proceso 8 GiB, disco acumulado 27 GiB y reserva libre 8 GiB. La prueba sigue siendo sólo el mismo millón de pares.

El nuevo plan verifica el descriptor, aceptación, metadatos, secuencia temporal y limpieza del intento fallido, y conserva sus hashes y duración previa. Admite un arranque histórico distinto del nuevo si sus registros internos concuerdan. Cuenta catorce árboles, incluido el fallido, dentro de las mismas particiones. No borra archivos ni adopta texto plano o runs compactos incompletos. Vuelve a usar únicamente los prefijos comprimidos certificados del control y verifica el índice. No hay HTTP ni TDP y el cargo de 7.322.807.977 bytes, con la misma reserva previa del navegador, no se reinicia ni duplica. El tiempo local del intento anterior permanece en la nueva cadena de procedencia.

El resultado sigue exigiendo coincidencia de todos los conteos/QC originales y número de registros, dos decodificadores concordantes y supervisión limpia. Una discrepancia falla, y el inventario no promueve la puerta de cobertura. Raíz nueva con sufijo `-guard-02`, plan deshabilitado, SHA exacto y nueva aceptación local; no se reabre ningún intento.

## Validación y límites

Pruebas y versiones en `validation.json` y `tests.txt`: regresión anterior más 19 tests nuevos. Se reproduce la supervivencia por encima del antiguo límite de 300 s y el corte real al llegar a 720 s. Se verifican plazos y lectura independiente del padre; 10.000 checkpoints del trabajador no leen el estado del disco ni vuelven a leer el arranque dentro del intervalo de muestreo. También se prueban reloj civil, retroceso, arranque, límite total, política falsa, contadores, orden, fallo previo alterado o incompleto, y no adopción de resultados huérfanos.

La integración del trabajador/sellador reproduce SAM de miniaturas, valida prefijos y exige igualdad con el control de fixture. No constituye ejecución nueva de HISAT2 humano. `guard-microbenchmark.json` compara sólo 20.000 llamadas en el entorno del agente, con el muestreo de disco sustituido; no mide la reducción humana completa ni garantiza su duración. No se atribuye al coste de la guarda toda la demora real, que no fue perfilada en WSL.

## Próximo paso

Preparar un descriptor nuevo con `scripts/unc13a_locus_audit_v2.py`, comprobar ventana 2100 s, reducción 720 s, guard_policy `in-memory-worker-independent-parent-v2`, prefijo 1.000.000 y cero bytes nuevos antes de aceptar. Mantener el intento fallido íntegro. Ejecutar sólo la nueva auditoría local, recibir su resumen/inventario y revisar las explicaciones alternativas. PR 36 abierta sin fusionar; sin PSI, comparación entre condiciones ni inferencia clínica.
