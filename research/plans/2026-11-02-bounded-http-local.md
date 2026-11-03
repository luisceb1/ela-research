# HTTP acotado: plan previo de pruebas locales

Solo servidor127.0.0.1con bytes sintéticos, sin URLsFASTQ/índice. Límite por lectura=min(chunk,saldo,payloadrestante); cobrar bytes entregados incluso ante fallo; Content-Length obligatorio y exacto, sin redirects/Content-Encodingtransformado. Reintentos explícitos desde cero, conservando parciales y consumos; no prometer Range/reanudación de archivos truncados. Reanudación solo de fases verificadas del runner.

Tests: éxito/hash/reutilización, truncamiento, cabecera incorrecta, checksumincorrecto, agotamiento acumulado, retryexplícito con bytes fallidos cobrados, redirecty destino no permitido. Evidencia de solicitudes/lecturas; presupuesto refiere a cuerpo leído, no TLS/cabeceras o buffering TCP. Presupuesto60s/512MiB/10MB. Preflight del manifiesto real, solo metadatos/versiones y fases pendientes, sin ejecución. raw_execution_ready=false.
