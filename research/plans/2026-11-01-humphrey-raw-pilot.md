# Piloto técnico Humphrey paired-end — plan sin ejecutar

Pregunta: ¿puede un proceso acotado recuperar soporte de uniones UNC13A y cuantificar cobertura por biblioteca en GSE296714, con contabilidad de fragmentos y recursos medidos?

Selección reproducible por menor tamaño FASTQ comprimido dentro de cada condición, desempate por accession; no se usan efectos de STMN2/UNC13A. CTRL-4/GSM8975203/SRR33425816:1.958.406.420bytes. TDP-5/GSM8975210/SRR33425819:4.391.297.461bytes. Total cuatro mates:6.349.703.881bytes. URL, MD5, SRX y BioSample concordantes con ENA actual en reports/gse296714-raw-pilot-plan-20261101/PLAN.json. Estas bibliotecas no son una pareja biológica ni representan al grupo completo; la selección por tamaño limita generalización y cobertura.

## Recursos propuestos y estado real

Entorno medido: límite cgroup8GiB; cuota8CPU, uso propuesto2; disco libre≈62,7GB. HISAT2/STAR/samtools no encontrados. El candidato HISAT2v2.2.3 (commit0d244324f98de541bce04d45c75e83bc3522f7f4) y el índice hg38 previamente verificado son antecedentes, no binarios restaurados. El índice histórico tenía archivo4.355.786.349bytes y archivo+extraído9.019.829.587bytes; su RSS de inspección no es un benchmark PE.

Presupuesto fijo:2hilos, máximo6GiB RAM para el árbol de procesos,25GiB adicionales en disco y reserva8GiB; máximo12GB de transferencia total incluidos índice/referencias/reintentos. Transferencia de FASTQ+índice≈10,71GB si hay que restaurar el índice. Si falta espacio para referencias, binarios, prefijos o salidas dentro de ese presupuesto, detener antes de descargar. No construir STAR ni un índice humano completo en este plan. No guardar SAM/BAM genómico completo ni FASTQ descomprimidos completos.

Tiempo: máximo60min globales de transporte y15min de alineamiento por biblioteca para el prefijo de1.000.000pares; son límites de parada, **no estimaciones de duración ni benchmarks**. No extrapolar la velocidad de GSE122069. No ampliar a bibliotecas completas si el prefijo no alcanza cobertura. Si falla un límite, conservar recibos y detener sin ampliar presupuesto automáticamente.

## Prerrequisitos: única próxima tarea, todavía sin crudos

Implementar y comprobar contrato PE con datos sintéticos, sin instalar/alinear genoma humano o descargar FASTQ. El extractor histórico hisat2_synthetic_gate.py rechaza explícitamente read.is_paired: no puede reutilizarse como si aceptara estos datos.

- Definir unidad: soporte de fragmento por unión por biblioteca. Dos mates del mismo QNAME/RG que apoyen la misma unión cuentan una vez; dos uniones diferentes conservan su soporte separado. No dividir por dos las cuentas globales ni identificar fragmentos con moléculas únicas sin UMI.
- Controles exactos: apoyo en ambos mates, en uno solo, mates solapados, distintos eventos en el mismo fragmento, secundarios/suplementarios/multimapeo, nombres repetidos en otra biblioteca, par perdido, orientación y hebra. Comparar parser SAM/CIGAR propio con implementación independiente HTSlib/PySAM; exigir identidad exacta de eventos y soporte prefijado. Comprobar rechazo del contrato SE conservado.
- Política primaria propuesta: pares primarios concordantes, NH=1 y20≤MAPQ<255 en ambos mates; hebra del evento explícita, anclas contiguas≥15en el mate que aporta la unión. Ancla8solo sensibilidad prefijada. Duplicados marcados se contabilizan/etiquetan, sin afirmar deduplicación molecular. Pares discordantes/huérfanos se registran como exclusiones, no ausencia.
- Antes de datos reales: fijar ensamblaje, geometría exacta críptica/canónica UNC13A, convención de coordenadas y secuencias de empalme con referencia cotejada. No arreglar por semejanza las variantes de coordenadas del compendio. Fijar strandedness FR/RF a partir de evidencia de biblioteca, sin confundirla con orientación física --fr/--rf de HISAT2. Si no se resuelve, detener para definir un análisis unstranded explícito, sin adivinar ni elegir según mayor efecto.

El manual primario HISAT2 distingue entradas PE y strandedness FR/RF; los parámetros de mixed/discordant deben fijarse antes del piloto, y no usar --tmo para un evento críptico no anotado. Referencia consultada:https://daehwankimlab.github.io/hisat2/manual/. La compatibilidad PE no queda acreditada por leer el manual o por los controles SE anteriores.

## Fase real, condicionada a los prerrequisitos

1. Restaurar versión/índice por hashes históricos y verificar referencias/eventos. Medir RAM/disco de ese entorno actual. Registrar argv fijo antes de mirar soporte objetivo; no instalar o restaurar en esta fase de planificación.
2. Descargar los cuatro mates completos con tamaños/MD5de ENA, SHA256local y EOF/CRCgzip válidos. Comprobar R1/R2: nombres, sincronización, iguales números de registros y FASTQválido. El significado del read_countENA debe verificarse antes de compararlo con pares/lecturas. No certificar integridad global con un gzip truncado.
3. Extraer de cada biblioteca los primeros1.000.000pares sincronizados, con hash y ordinales; prefijo técnico no aleatorio, no réplica o fracción representativa garantizada. Alinear2CPUbajo supervisión del árbol de procesos, sin selección de lecturas por gen o alineamiento solo al locus. Flujo SAM hacia dos extractores acotados, sin retener salida genómica completa.
4. Cierre técnico: identidad de soporte entre extractores, métricas de exclusión/alineamiento y recursos dentro de límites. Para calificar cobertura del contraste definido se propone soporte canónico+críptico≥20fragmentos válidos por biblioteca. Es umbral operativo prefijado, no poder estadístico. Menor cobertura significa piloto insuficiente; no ausencia de evento ni permiso para ampliar automáticamente.

Salida: tabla por biblioteca con soporte, cobertura y QC; hashes/logs/versiones/recursos. No PSI, efectos de KD, p-valores, emparejamiento biológico, correlación con PPAU STMN2 o rescate funcional. Un piloto positivo solo demuestra factibilidad técnica; uno negativo cierra o fundamenta una propuesta nueva de recursos. **No se ha ejecutado ninguna fase real de este plan.**
