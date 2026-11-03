# Plan prospectivo: recuperar CTRL_R2 sin reiniciar el piloto

Pregunta técnica: ¿permite una petición Range completar el parcial de 284.799.727 B y recuperar exactamente el mate de SRR33425816, manteniendo cargo y evidencia previos?

Diseño: raíz exclusiva, copia/hash de prefijo, rango exacto 284799727–997549456, HTTP206 con longitud/rango exactos y MD5 entero 007d66223fe35f394284e4ebd631eaef. Cargo inicial5.603.756.481 B y final esperado6.316.506.211 B; sin reembolso por reserva ni reinicio de tiempos agotados. Nueva ventana propuesta6000s/5400s HTTP, aceptación pendiente. Disco27GiB siete árboles/reserva8GiB, RSS512MiBmuestreada/AS1GiB/2CPU. Sólo transporte, sin FASTQ descomprimido, alineamiento, TDP o cambio de pregunta.

Fracaso: respuesta distinta, cabeceras o MD5/tamaño incorrectos, archivos previos cambiados, límites de tiempo/disco/memoria/bytes o supervisor no limpio. Conservar resultado/fallo, no repetir automáticamente ni ampliar presupuesto. Éxito sólo con sello externo limpio. Validar pares y cobertura será otro paso, no una conclusión de esta recuperación.
