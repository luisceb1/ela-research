# Plan prospectivo — contrato STMN2 GSE122069, 31/10/2026

Base: main f898b2967aae8909db1796753f9d2cae2bf966ef. PR30 053ef70ce437cc637ec18278a2c07e3abd6bf58b inspeccionado, no modificado. Issues1/2 ejecutadas; sus pendientes no se resuelven repitiendo mapeo.

Pregunta técnica: ¿se puede fijar un contrato de coordenadas para la unión STMN2 críptica y un comparador canónico del mismo donante, con conversiones SAM/BED/intrón inequívocas y rechazo de soporte ambiguo antes del piloto?
Predicción refutable: la proyección v47 ya auditada identifica un único aceptor canónico compartiendo el donante publicado, y el extractor recupera exactamente los límites esperados bajo controles positivos y no cuenta negativos.
Entradas: projections públicas reports/isoforms/junctions.tsv, exons.tsv, reference_source.json; reports/event-reference/paper_evidence.json. Reutilización explícita, no otra auditoría GEO o nueva réplica. Fijar hashes locales antes de ejecutar.
Controles: offsets ±1; cromosoma; operaciones CIGAR M/=/X/N/D/I/S/H; hebra XS separada del flag de alineamiento; NH=1, MAPQ>=20, flags secundarios/suplementarios/no alineados/QCfail; anclas contiguas >=8; CIGAR malformado, campos inválidos; no eliminación de duplicados sin UMI; lecturas SE exclusivamente.
Fracaso: cero o >1 comparador inequívoco; evento no coherente con exones; conversiones incorrectas; falso positivo en negativos; hashes distintos; dependencia nueva no resuelta. Mantener bloqueo en lugar de imputar.
Alcance: auditoría de contrato y software sintético; sin FASTQ, índice, alineamiento, cuentas biológicas, efectos, PSI, p-valores o rescate. No reclamar validación de FASTA/índice a partir de proyecciones. Si red impide FASTA/índice, registrar el error y dejar piloto bloqueado.
Siguiente prueba: validar referencia FASTA/índice compatibles y motivos, versión/semántica del alineador; contrastar extractor con herramienta independiente en piloto antes de aceptar soporte real.

