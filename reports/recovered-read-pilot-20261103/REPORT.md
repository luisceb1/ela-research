# Piloto con CTRL_R1 recuperado — 03/11/2026

## Evidencia

Luis aporta sealed_verified_ctrl_r1:960.856.963B, MD5ed58daa011d6508a3e8d1f05bc39fc29 ySHA298a8b4769fcd5434f883706c873d56795c5a20d855917d80a391b2e5c38beff. Cargo5.318.543.809B, saldo6.681.456.191B. Los seis hashes de metadatos/recibos quedan en user-reported-recovery-seal.json. Es evidencia de terminal, no acceso remoto al host. El sello significa archivo verificado y externo limpio según el trabajador; no hay resultado biológico. No se aportan tiempos niRSS de esta recuperación; no se inventan. La nueva configuración obtiene tiempo acumulado de los metadatos sellados locales.

## Cambio

recovered_read_pilot.py crea una ejecución exclusiva y separada; no modifica archivos históricos de transporte/caché/piloto/algoritmoPE ni reabre ledger fallido. Valida recuperación exacta aceptada, hashes de seis recibos, grupo externo, estado/MD5/SHA/tamaño/cargos y cadena del índice. Padre sólo metadatos. Worker comienza con5.318.543.809B y tiempos anteriores; revalida índice mediante el motor previo. CopiaCTRL_R1 y verificaMD5/SHA antes/después, sin nuevaHTTP de ese mate. Los otros tres mates usan wrapper de respuesta200 exacta/MD5, socket30s y bloque de reserva4MiB/lecturas≤64KiB; sin redirects/proxy/encoding/chunked/retry. Aumento de espera no garantiza conectividad futura.

Se reutilizan validador pareado, prefijos fijos1M, argvHISAT2 y stream/reductor existentes. CTRL_R2 primero; control completo y cobertura≥20 antes deTDP. Read1 local queda en fase transfer con recibo de procedencia ynew_body_bytes0; su tiempo de copia se carga conservadoramente al límite acumulado de transferencias. No engaña un reciboHTTP, no se añade attempts_used a la copia. La comprobación gzipEOF/CRC/mates se hará en fase pareada existente. El módulo nuevo se fija por identidad propia, además del motor histórico fijado en el manifiesto; conserva la validación histórica del job fallido.

Propuesta explícita nueva:7200s total/1800s transferencias incluida copia, copia≤180s, preflight≤180s; caps2CPU/RSS6GiBmuestreada/AS8GiB. Cuerpo nuevo máximo planificado5.388.846.918B, cargo final mínimo10.707.390.727B y margen1.292.609.273B bajo techo12GB sin reembolso. Disco propuesto27GiB(total antes25) yartefactos18GiB(antes16): suma seis árboles, preserva parciales y copia960MB adicional. Otras particiones2GiBprefix/6temporales/.5dependencias/.25recibos yreserva8GiB conservadas. Lo acepta sólo SHA exacto más --accept-new-window-and-disk. Preparar no acepta ni ejecuta.

## Validación y límites

328 pruebas locales sin errores/fallos/omisiones (308 anteriores+20 nuevas), Python3.12.14/PySAM0.23.3; compileall correcto. Pruebas y versiones en validation.json/tests.txt. Fixtures artificiales: metadatachain, no acceso bulk en padre, copia local hash/cargos intactos, datos corruptos rechazados, selección de tresHTTP/orden/umbral, rutas/caps/código/counter-floor/tiempos/exclusividad. Loop de trabajador con helpers de cómputo sustitutos se detiene por cobertura yparent sella correctamente, sinTDP. WrapperHTTP se prueba con respuestas en memoria: MD5, cargo, estadoHTTPincorrecto, timeout conservador. WorkerCLI supervisado real falla por metadataausente antes deHTTP y deja grupo vacío. No ejecución humana en nuestro host; no se presenta como validación end-to-end humana. AlgoritmoPE existente y su regresión también se prueban. RSS/disco muestreados no son cuotas agregadas duras; límites previos de host/WSL/I/Oininterrumpible conservados. Un sello no es protección contra control hostil del equipo.

## Siguiente prueba

Emitir descriptor deshabilitado real enWSL, revisarJSON/SHA/27GiB propuestos yaceptar ventana/recursos después. No editar ledger ni volver a ejecutar planes anteriores. Primer resultado discriminante: validación pareadaCTRL y cobertura del control; si insuficiente, parar antes deTDP, sin expansión adaptativa. NoPSI, p-valores, efecto, rescate o beneficio clínico demostrados por estos controles. PR36 abierta sinmerge.
