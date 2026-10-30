# ELA — investigación computacional reproducible

Estudio de las consecuencias transcriptómicas de la pérdida nuclear de TDP-43, con foco en STMN2 y UNC13A. El proyecto reúne reproducciones técnicas, descriptivos y propuestas experimentales. No acredita una nueva diana, un tratamiento propio o beneficio clínico.

## Estado y próxima tarea

Leer [AGENTS](AGENTS.md), [estado vigente](research/STATE.md), [evidencia](research/MASTER_EVIDENCE.md), [backlog](research/BACKLOG.md) y [protocolo](research/PROTOCOL.md), y comprobar las cabezas remotas antes de actuar.

Esta versión reúne los contenidos de los PR #28 y #29, conservando la procedencia y los bloqueos. La próxima tarea es **seleccionar una sola fuente independiente con entradas públicas completas para un contraste directo de uniones**, siguiendo [el criterio de entrada](research/NEXT_STUDY_GATE.md). No repetir auditorías cerradas o búsquedas bloqueadas sin fuente nueva.

## Resultados y límites

- GEO/mapeo y corrección del parser: ejecutados. Las 21 uniones históricas no constituían un cribado exhaustivo válido.
- Catálogo: 1901 claves; partición conjunta de referencia/autores 545 anotadas, 353 solo autores, 182 de identidad pendiente y 821 sin coincidencia en recursos limitados. No son 821 descubrimientos.
- GSE126542/GSE121569: reproducción agregada e integridad técnica ejecutadas. DEXSeq no mide directamente las regiones CE contrastadas; no se ha reajustado el modelo inferencial.
- SH-SY5Y: seis bibliotecas enlazadas a ENA; reanálisis conjunto de siete uniones bloqueado por cuatro alias y dos conflictos de hebra sin resolver.
- Originalidad: revisión dirigida y propuesta UNC13A v0.4 como extensión conceptual. No validación funcional propia ni originalidad certificada.

## Verificación

```bash
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

La combinación de ambas ramas supera 244 tests offline en Python 3.12.14. La CI ejecuta Python 3.11/3.12 por commit; consultar el SHA correspondiente. Las pruebas de software no sustituyen replicación biológica. Los análisis reales requieren sus fuentes y dependencias fijadas en cada informe; una CI offline correcta no significa que se hayan redescargado y reejecutado todos los análisis.

Originales fuera de git, en cachés reproducibles con URL/hash. Código e informes conservan comandos y límites. [Acta de integración](reports/integration-20261030/REPORT.md) e historial documental están separados del estado vigente.

Sin datos clínicos personales, contactos, publicación externa, costes o laboratorio sin autorización. No inferencia con replicación inadecuada ni equivalencia entre cuentas, ARN funcional, proteína y recuperación neuronal. Esta integración concreta está autorizada; futuros merges o cierres de issues requieren la autorización aplicable.
