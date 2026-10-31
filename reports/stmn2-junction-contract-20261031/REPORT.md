# Contrato de uniones STMN2 para GSE122069 — 31/10/2026

## Evidencia

Plan prospectivo: research/plans/2026-10-31-stmn2-junction-contract.md. Pregunta técnica: fijar comparador canónico del mismo donante y conversiones verificables antes de contar lecturas. Falsador: comparador ausente/ambiguo, geometría incompatible o controles incorrectos. Se cumple esta puerta técnica, no el gate completo de piloto o replicación.

Se reutilizan las proyecciones de GTF v47 ya auditadas (SHA256 del original df11938c66d2b39f8ebbdb5f1720919321f9cf9d58f02b019753f6a24ca3db24), sin volver a ejecutar mapeo #1/#2. Hashes de las cuatro entradas locales en research/references/stmn2_junction_contract_20261031.json; blobs fuente cotejados contra main f898b2967aae8909db1796753f9d2cae2bf966ef. No son GTF/FASTA íntegros nuevamente recuperados. El candidato críptico procede de la proyección molecular previa de Fig.5 de Smith et al. (2025), no de una lectura nueva del texto completo por scite.

| Unión GRCh38 chr8:+ | Límites exónicos 1-based | Intrón 1-based inclusivo | Intrón BED 0-based semiabierto | CIGAR N |
|---|---|---|---|---|
| Críptica candidata | 79611214 → 79616822 | 79611215–79616821 | [79611214,79616821) | 5607 |
| Canónica comparadora | 79611214 → 79636802 | 79611215–79636801 | [79611214,79636801) | 25587 |

La proyección ofrece un solo aceptor canónico desde ese donante, con testigos exónicos ENST00000220876.12 y ENST00000518111.5. Dos transcritos y dos tablas del repositorio no añaden unidades biológicas. La hebra viene de la proyección auditada, no de una declaración explícita en la leyenda molecular inspeccionada anteriormente.

Prototipo SAM SE: NH:i:1 obligatorio; XS:A:+/- obligatorio; MAPQ≥20, excluyendo255; excluye no alineados, secundarios, suplementarios y QCfail; anclas alineadas contiguas≥8 bases M/=/X. La orientación de alineamiento flag16 no se convierte en hebra transcrita. Indels rompen anclas contiguas; D no es N; el flag1024 se conserva, sin deduplicación RNA arbitraria. Rechaza PE, etiquetas duplicadas, NH/XS inválidos, posiciones/CIGAR/longitudes de secuencia inválidos. Campos o hebra ausentes no dan soporte. No hay CLI de procesamiento de crudos, solo auditoría de contrato; semántica XS/NH y comparación con herramienta independiente pendientes antes de aplicar a datos reales.

22 nuevas pruebas cubren positivos, offsets±1, cromosoma/hebra, anclas, indels/clipping, múltiples uniones, controles negativos, hashes alterados y flags. Suite conjunta: **275 tests correctos**, Python3.12.14, compileall correcto. Esto comprueba software, no biología. Dos ejecuciones generan contract.json idéntico por bytes, SHA256 4778971a7764cb92cec06e5788ccc8ddc15b5e4c0dfad9998f4cc310d1a8b8c8. Sin aleatoriedad ni dependencias externas nuevas.

## Interpretación y límites

El contrato fija un comparador y evita errores de una base al extraer N del CIGAR. **No demuestra** soporte real de lectura, correcta anotación del transcrito completo, polyA, un efecto TDP-43, replicación externa, función neuronal o beneficio clínico. No se inspeccionan efectos ni se modifica un umbral para obtener resultados.

La razón propuesta críptica/(críptica+canónica) sería una razón condicional de cuentas para esas dos ramas del donante; otras ramas pueden existir. No es PSI molecular, y todavía no se calcula. No se descargó FASTQ, instaló alineador, creó índice, alineó o procesó lectura biológica. FASTA, motivos, índice y comparación con herramienta independiente siguen sin validar: pilot_ready=false.

Entorno observado: límite RAM8GiB; disco libre62.793.551.872bytes; sin HISAT2/STAR/samtools. No benchmark ni ampliación del presupuesto previo (6GiB RAM, 2hilos, 15GiB adicionales, reserva8GiB). Acceso GitHub comprobado mediante conector; clon directo falló por falta de credenciales. Ensembl REST agotó timeout20s, sin obtener exones ni secuencia. Scite recuperó metadatos del DOI pero no pasajes/avisos editoriales; el filtro de correcciones devuelve un mensaje incompatible de DOI no indexado. No se afirma revisión editorial completa. Logs en errors.json/scite_checks.json.

La primera suite local sobre copia incompleta tuvo258tests/1fallo/3errores; recuperados módulos/fixtures se detectó un salto de línea extra introducido en una copia local. Se restauraron cinco fixtures por sus Git blobs y se cotejaron los ficheros heredados presentes; sin editar el código anterior,275tests correctos. Los fallos y el intento de transferencia con argumentos demasiado largos se conservan como errores técnicos, no negativos biológicos. La CI remota debe verificarse por la cabeza del PR y no ejecuta FASTQ ni certifica recursos.

## Reproducibilidad y continuación

```bash
python scripts/audit_stmn2_junction_contract.py --manifest research/references/stmn2_junction_contract_20261031.json --out reports/stmn2-junction-contract-20261031
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

Se revisaron protocolo, estado, backlog y las diez issues abiertas. #1/#2 ya ejecutadas, con soporte crudo pendiente; no repetidas. Único PR previo abierto #30, draft, cabeza053ef70ce437cc637ec18278a2c07e3abd6bf58b; informe y diferencias inspeccionados, rama intacta, sin reproducir RiMOD/NYGC ni almacenar sus datos individuales. #28/#29/#31 están incorporados; sus ramas históricas no son nuevas tareas. No merge/cierre automático. Sábado: informe semanal30/10 ya existente, no duplicado.

Única próxima prueba discriminante: conseguir FASTA/índice trazables del mismo ensamblaje, comprobar motivos y versión/semántica del alineador bajo presupuesto. Si falta un enlace o se supera el presupuesto, mantener bloqueo sin ejecutar piloto. Después, si cumple el plan, contrastar la extracción con una herramienta independiente en el piloto predefinido, sin inferencia biológica de ese subconjunto. Solo fuentes públicas; sin clínica personal, contactos, costes, publicación externa o laboratorio.

## Referencias

- Smith, A., Shepherd, C. E., Henden, L., et al. (2025). Multi-region brain transcriptomic analysis of amyotrophic lateral sclerosis reveals widespread RNA alterations and substantial cerebellum involvement. *Molecular Neurodegeneration,20*. https://doi.org/10.1186/s13024-025-00820-5. Metadatos verificados en scite; coordenadas reutilizadas del expediente molecular previo, no nueva confirmación de texto completo.
- Melamed, Z., López-Erauskin, J., Baughn, M. W., et al. (2019). Premature polyadenylation-mediated loss of stathmin-2 is a hallmark of TDP-43-dependent neurodegeneration. *Nature Neuroscience,22*,180–190. https://doi.org/10.1038/s41593-018-0293-z. Contexto GSE122069 del plan previo, sin nuevo resultado biológico aquí.
- GENCODE human v47, GRCh38. https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_47/gencode.v47.annotation.gtf.gz. Proyección previa y hash citados; original no redescargado.
