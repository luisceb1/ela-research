# Plan previo: mapeabilidad del primer exón STMN2 — 31/10/2026

Base PR33: 76ddc67f236e2f60f099897a116a229c76f25d7a. Mismo PR; sin merge ni cambios en PR30. La copia local de trabajo se aísla y se coteja por Git blobs. Insumos grandes se reutilizan solo si sus hashes coinciden; no volver a procesar FASTQ reales.

Pregunta técnica: ¿el primer exón canónico STMN2 permite recuperar lecturas perfectas de 50/51 nt en su ubicación de origen con la configuración HISAT2 fijada, o existe una limitación de mapeabilidad suficiente para explicar la falta de cobertura aceptada del piloto?

Predicción refutable: al menos una ventana de cada longitud del primer exón, en ambas orientaciones, se recupera íntegra en el origen con NH=1 y MAPQ>=20, distinto de255. Si ninguna pasa, limitación del alineador/configuración para estas secuencias; si pasan todas/muchas, no atribuir la ausencia del piloto a una imposibilidad general de mapear lecturas perfectas. No extrapolar a errores, variantes o sesgos de biblioteca.

Regiones prefijadas de proyección GENCODEv47 auditada: ENST00000220876.12, exon1 chr8:[79611116,79611214) (98 nt), exon2 [79636801,79636897) (96 nt), exon3 [79641377,79641550) (173 nt). ENST00000518111.5 comparte el donante y tiene inicio de exon1 en79611151 (0-based): analizar como subgrupo las ventanas contenidas en la intersección de63nt; no reinterpretar dos TSS como réplicas o asumir cuál se expresa. Reutilizar proyección versionada; no nueva auditoríaGEO/ENSG.

Diseño: todas las ventanas posibles de50 y51nt en exon1, exon2 yexon3, con sus reverse-complement; controles positivos equilibrados de las dos uniones prefijadas a50/51nt y negativoN50. No seleccionar ventanas según su resultado. Lecturas perfectas sin aleatoriedad. Fijar coordenadas esperadas por lectura antes de alinear. Es síntesis de referencia, no experimento biológico.

Método: obtener secuencias desde el índice fijado en flujo sin FASTA completo; conservar solo regiones mínimas. HISAT2v2.2.3 directo, mismo índice y SHA, -p2 -k5 --seed0 --no-temp-splicesite --reorder, sin anotación/sitios inyectados o strandness impuesta. Memoria virtual5GiB alineador y CPUafín2; no nuevo índice. Exactitud exige chr8, posición y orientación esperadas, CIGAR completo50M/51M, NM0, primario/NH1/MAPQ>=20no255. Registrar también alineamientos parciales/multi/noalineados o a otras ubicaciones, sin llamar NH exhaustividad. Controles de unión deben recuperar extremos esperados; negativo no debe aceptarse.

Fracaso: hash/referencia distintos, esquema o coordenadas ambiguas, positivos equilibrados fallan, negativo se acepta, hay recursos excedidos o resultado no reproducible. No mover donante/aceptor o filtros después de observar resultados. Ausencia de cobertura real no es ausencia biológica. No p-valores, efectos/PSI ni réplicas por ventana. Guardar todos los resultados, errores y controles, actualizar único P0 según lo que discrimine este ensayo.
