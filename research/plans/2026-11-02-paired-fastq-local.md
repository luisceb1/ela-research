# Integridad paired FASTQ y límites explícitos — previo a ejecución

02/11/2026; continúa PR36, cabeza22d285f8. Solo fixtures generadas localmente. No red externa, datos biológicos, índice humano o alineamientos.

Pregunta: ¿podemos rechazar archivos gzip/mates/prefijos incoherentes y representar límites de proceso explícitos sin confundirlos con los límites sintéticos? Predicción refutable: fixture de tres pares produce un prefijo exacto de dos; el escaneo completo de ambos gzip valida EOF/CRC incluso tras el prefijo. Cada corrupción controlada debe impedir una salida verificada. Los límites por proceso forman parte de la firma de fase: cambiarlos no permite reutilizar un recibo anterior.

Controles positivos: nombres idénticos sin sufijo, /1 y /2, etiquetas CASAVA compatibles, datos deterministas y prefijo byte-idéntico en dos ejecuciones. Negativos: CRC, truncamiento, mate extra/ausente/desordenado, nombre o número de mate incorrectos, secuencia/calidad de longitud distinta, identidad repetida en línea+, etiquetas contradictorias, prefijo mayor que fuente. Solo FASTQ de cuatro líneas; variantes multilínea se rechazan explícitamente, sin pretender un parser universal.

Registrar únicamente métricas agregadas, tamaños/hashes, parámetros y excepciones genéricas; no nombres ni secuencias en los informes. Las secuencias artificiales de prueba no son observaciones biológicas. Calidad ASCII33–126 como rango sintáctico; no inferir codificación Phred ni calcular puntuaciones clínicas.

Límites: simulación local ≤60s por comando de pruebas, archivos pequeños, dos CPU como máximo, sin elevar recursos del piloto. Los valores del plan real se validan en dry-run pero no se ejecutan procesos con presupuesto humano. Configuración de producción debe ser explícita, nunca fallback silencioso a5s/128MiB. RAM RSS muestreada no es límite agregado de kernel. No cambia raw_execution_ready=false: transporte externo, integración de fases reales, prueba de recursos y autorización siguen pendientes.

Fracaso: aceptación de un negativo, hashes/prefijo distintos, cambio de plazo global o reuso de fase con límites diferentes, o resultados fuera del alcance. Conservar errores y detener esa vía; no ampliar datos/presupuestos o repetir alineamientos anteriores.
