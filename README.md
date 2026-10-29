# ELA — investigación computacional reproducible

Proyecto sobre pérdida nuclear de TDP-43, splicing STMN2/UNC13A y recuperación funcional neuronal. Hay auditorías técnicas, análisis exploratorios y propuestas; no una nueva diana validada ni resultados clínicos propios.

## Continuidad

Leer [AGENTS.md](AGENTS.md), [estado](research/STATE.md), [backlog](research/BACKLOG.md), [protocolo](research/PROTOCOL.md), [evidencia](research/MASTER_EVIDENCE.md) e issues/PR remotos. Main contiene ambas cadenas mediante el PR #26; es la base común. Los PR originales están cerrados y las ramas conservadas son referencias históricas. Comprobar siempre su cabeza actual antes de trabajar.

Cruce elegible crypTE ejecutado:284etiquetas S8y70solo contextoS7con gen/unión exactos. [Informe](reports/author-junction-match/REPORT.md). Próximo: conflictos de identidad y cobertura excluida con fuentes trazables. Las ausentes de GENCODEo del subconjunto no son automáticamente nuevas.

## Verificación y reproducción

Python 3.11/3.12; biblioteca estándar para la suite:

```bash
python -m unittest discover -s tests -v
python scripts/geo_audit.py
python scripts/map_isoforms.py
python scripts/describe_targets.py
```

Los últimos tres comandos verifican/recuperan fuentes públicas y generan informes. Leer manifiestos y límites: los descriptivos cerebrales históricos usan etiquetas depositadas, no estratos cognitivos corregidos.

```bash
python scripts/reconcile_shared_junctions.py --cache RUTA_CACHE_PUBLICA
python scripts/annotate_gencode_junctions.py --reference RUTA/gencode.v47.annotation.gtf.gz
```

Originales fuera de git en data/, URL/SHA256 en manifiestos. Informes históricos conservan entorno y número de tests de su ejecución, no estado actual. [Consolidación](reports/repository-integration/REPORT.md) registra procedencia/resoluciones. Prototipos MEA archivados para auditoría sintética; no análisis experimental.

## GitHub y Work

- CI offline unificada:125tests en esta entrega (base consolidada105más veinte de auditoría/cruce crypTE), Python3.11/3.12; comprobar el SHA/PR antes de asumir integración en main.
- GEO Iso-Seq real-data audit: cuatro entradas públicas y artefactos temporales; éxito técnico no valida biología.
- ELA source watch: vigilancia diaria 07:17 UTC/manual, registro de fallos y salidas; no decide experimentos por sí sola.
- Work: 08:00 Europe/Madrid, resumen viernes; comprobar acceso/herramientas cada vez, sin cómputo continuo garantizado.
- Ramas breves desde main, revisión y pruebas antes de integrar. Esta consolidación no concede autorización general para futuros merges.

## Límites

No datos clínicos personales, contactos externos, publicación de hallazgos, costes o laboratorio sin autorización. No inferencia con n=1, cuentas asignadas como lecturas de unión o equivalencia entre ARN, proteína, recuperación neuronal y beneficio clínico.
