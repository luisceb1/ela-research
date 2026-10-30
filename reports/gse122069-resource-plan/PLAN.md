# GSE122069: plan de recursos y controles — 30/10/2026

## Estado
Plan prospectivo; no FASTQ descargado, índice creado, alineamiento o efecto calculado. No gasto, contacto o servicio externo. Este documento no certifica que el pipeline quepa o funcione. Las fuentes, QC y bloqueos previos de #31 se conservan; #30 continúa separado para pruebas con otro chat.

## Pregunta y falsador
¿La pérdida de TDP-43 en el contraste de cultivo SH-SY5Y publicado por Melamed aumenta el soporte de la unión STMN2 exon1→exon2a frente a exon1→exon2 canónico? Predicción: dirección de aumento consistente entre las tres unidades publicadas por condición; no suponer pares por compartir sufijo. Es reproducción de un evento conocido, no descubrimiento ni rescate funcional.

Antes de leer cuentas del evento deben fijarse los dos extremos, hebra, ensamblaje y denominador. La proyección molecular existente reports/event-reference/paper_evidence.json proporciona el candidato críptico GRCh38 chr8:+, límites exónicos 79611214→79616822, DOI10.1186/s13024-025-00820-5. No basta por sí sola: confirmar la convención y el extremo canónico contra GTF/FASTA versionados antes de cuantificar; mantener explícita la conversión exónico/intrónico/0–1-based. No inferir sitio polyA o identidad de transcrito completo. No usar un exón como si fuera una unión.

Fracaso técnico: hash distinto, biblioteca no enlazada, convención no resuelta, prueba sintética incorrecta, cobertura insuficiente o recursos superados. Fracaso de la predicción: dirección no consistente según el contraste predefinido; registrar el negativo, sin cambiar evento/umbral para obtenerlo. Diseño/unidades insuficientes: solo un bloqueo, no p-valores. Si todo pasa, primero descriptivos por condición/unidad, sin promover lecturas o fragmentos a réplicas.

## Entradas y dependencia
input_manifest.json fija seis GSM→SRX→SRR, URL HTTPS y MD5 ENA por FASTQ. Total publicado 9.474.892.575 bytes comprimidos (~8,82 GiB). El manifest deriva de la fuente ENA fijada por SHA256 en #31; no es verificación de bytes de FASTQ todavía. Al descargar habría que comprobar MD5 y añadir SHA256 propio, fecha, tamaño, métricas técnicas y errores.
GSM3454242–244 = siControl; GSM3454245–247 = siTDP-43. El manuscrito declara tres experimentos biológicamente independientes por condición. Confirmar cómo los vincula a bibliotecas y si hay lote/pareamiento antes de una inferencia. Excluir las otras cuatro bibliotecas de edición genética y todos los metadatos personales. No mezclar este cultivo con tejido ni con los seis runs SH-SY5Y ya auditados de Brown.

## Recursos observados y presupuestos propuestos
environment.json registra el entorno, no un benchmark: límite RAM 8.589.934.592 bytes (8 GiB), cuota CPU equivalente a 8 núcleos, unos 30,8 GB de disco libre al comprobarlo. STAR, HISAT2, samtools y fastp no instalados en esa comprobación.

No lanzar un índice STAR humano ni asumir que cabe en 8 GiB. Evaluar como alternativa un alineador de splicing con índice compacto, por ejemplo HISAT2, sujeto a versión, licencia, hash y compatibilidad con referencia/anotación. No instalarlo ni crear índice en este paso. Preferir índice público trazable y compatible; no mezclar builds por conveniencia.

Presupuesto inicial de viabilidad, no consumo medido: máximo 6 GiB de RAM, 2 hilos y 15 GiB adicionales de disco; mantener al menos 8 GiB libres. Índice/referencia dentro de ese presupuesto. Si no cabe o no existe índice trazable, detener y presentar otro plan de entorno; no ampliar límites o contratar cómputo automáticamente. Tiempo y coste no estimados como benchmark; coste autorizado actual: cero.

Piloto técnico propuesto: primer control por orden de accession, SRR8144907 (1.391.030.664 bytes comprimidos según ENA), fijado antes de efectos. Descargar solo ese archivo tras decidir ejecución; descomprimir en flujo y usar como máximo el primer millón de lecturas para comprobar el pipeline, sin contraste biológico ni extrapolación de cobertura. El orden de lectura no es una muestra aleatoria. Medir pico RAM/disco/tiempo y registrar fallos; límite inicial 30 min de reloj para el piloto, con parada si se supera el presupuesto. No equivale a prometer que termina en ese plazo.

Solo después del piloto técnico correcto: procesar los seis archivos completos secuencialmente con QC por run, sin almacenar FASTQ descomprimidos, SAM o BAM completos. Cuentas de unión y QC pequeños como productos. Un piloto no acepta la fuente ni valida potencia estadística. Estimar duración total solo tras medición representativa; un millón de lecturas no predice linealmente todos los costes.

## Contrato de cuantificación antes de ejecución
- Congelar versiones de software, comandos completos, GRCh38 FASTA/GTF e índice con hashes. Semilla determinista si el software la usa; no ejecutar código de autores sin revisión.
- Probar con SAM/lecturas sintéticas positivas y negativas la conversión de CIGAR N a límites, hebra, unión canónica y críptica, multimapeo, alineamientos secundarios/suplementarios y anclas cortas. Comparar una extracción con una herramienta independiente en el piloto.
- Definir antes de observar efectos: soporte primario único, exclusión de secundarios/suplementarios, MAPQ≥20 y anclas≥8 bases a cada lado. Revisar significado de unicidad/MAPQ/NH en el alineador concreto antes de congelarlo; MAPQ solo no certifica unicidad. No eliminar duplicados de RNA sin justificación; reportar sensibilidad y escala de lecturas, no moléculas.
- QC de esquema, lecturas procesadas, pérdidas, alineamiento, profundidad total y soporte canónico. Umbral de factibilidad propuesto: denominador comparable ≥20 lecturas en cada biblioteca; es una regla técnica prospectiva, no garantía de potencia. Si falla, marcar no evaluable, sin imputar cero.
- Denominador: únicamente uniones que comparten el sitio alternativo justificado, no todos los bins o cuentas del gen. Mantener dos conteos por biblioteca separados hasta confirmar geometría. Una razón de cuentas no se llama PSI molecular.
- Registrar expresamente diferencias de profundidad, lote, perturbación y número de unidades. No sumar otras fuentes, variantes CE o fracciones para aumentar n. Ninguna conclusión clínica o funcional.

## Criterio para iniciar la siguiente fase
Revisar este plan; completar referencia/eventos/índice/versiones y confirmar recursos antes del piloto. La preparación documental está autorizada; no se ha iniciado descarga de crudos. Costes, comunicaciones o cambio sustancial de alcance requieren autorización. Si no se resuelven entradas y presupuesto, el entregable es un bloqueo reproducible, no una ejecución supuesta.

Referencias: Melamed et al. (2019), DOI10.1038/s41593-018-0293-z; GEO GSE122069/PRJNA503396. Manifest y auditoría previa: reports/source-selection-20261030. Proyección del evento: reports/event-reference, DOI10.1186/s13024-025-00820-5, alcance limitado a unión.
