# Geometría exacta contra todos los genes de v47 — 29/10/2026

## Resultado

**545 de las 1901 claves candidatas tienen una geometría exacta anotada en GENCODE v47: 17 bajo el mismo gen y 528 solo bajo otros genes.** Buscar únicamente bajo el gen candidato dejaba fuera esas 528 coincidencias. Esto limita reclamos de novedad de la unión; no reasigna su gen de origen ni valida un transcripto completo.

| Estado global de referencia | Claves candidatas |
|---|---:|
| Unión exacta bajo el mismo gen | 17 |
| Unión exacta solo bajo otros genes | 528 |
| No encontrada bajo ningún gen de este snapshot | 1356 |
| Total | 1901 |

Una clave incluye gen candidato+cromosoma+extremos intrónicos+hebra. Quitando el gen candidato quedan **1882 geometrías únicas**: 535 anotadas bajo algún gen y 1347 no encontradas. Las diferencias entre esos conteos se deben a geometrías compartidas por varias claves candidatas; no representan moléculas o réplicas. Ninguna de las 17 coincidencias del mismo gen tiene también testigo de otro gen en este conjunto.

## Cruce con la cobertura de autores

| Partición conjunta de las 1901 claves | Claves | Interpretación limitada |
|---|---:|---|
| Geometría anotada en algún gen v47 | 545 | Ya existe esa unión en la referencia utilizada |
| No encontrada en v47, representada con mismo gen en el subconjunto autor elegible | 353 | 283 etiquetas S8 y70 contextos de transcripto S7; no validación de crypticidad/función |
| No encontrada en v47, identidad de gen autor/referencia no resuelta o conflictiva | 182 | No convertir ambigüedad en ausencia |
| No encontrada en v47 ni en el subconjunto autor elegible | 821 | Doble no coincidencia con cobertura incompleta; **no son821 descubrimientos** |

De las 1159 claves antes no encontradas en el subconjunto autor, 338 sí aparecen en v47 (323 bajo otro gen y15 bajo el mismo). Solo821 permanecen sin coincidencia en ambos recursos inspeccionados. Esto muestra que ausencia en ese subconjunto no era ausencia en referencia. El catálogo autor fue filtrado por reconstruibilidad y gen; no se ha comparado exhaustivamente todo su contenido ni tejido.

Las 354 coincidencias estrictas autoras originales permanecen intactas: una ya está en v47 bajo el mismo gen, las otras353 no se encuentran en v47. La sensibilidad condicional355 de GTPBP6 es otro eje de análisis y no sustituye esos totales. Se conserva tabulación cruzada completa en summary.json; no se mezclan categorías de referencia con evidencia funcional.

## Método reproducible

Plan previo: research/plans/2026-10-29-global-junction-geometry.md. Misma tabla de1901 claves y mismo GENCODEv47/GRCh38 completo fijados por hash que en las auditorías previas. Coincidencia exige cromosoma, hebra y ambos extremos intrónicos1-based exactos; no tolerancia, liftover, alias, proximidad o span génico. Se preservan versiones de ENST y sufijos_PAR_Y de ENSG al retirar solo versión numérica.

Primera pasada sobre el GTF identifica transcritos con al menos un anclaje exacto posible. Segunda pasada recupera **todos** los exones de esos transcritos, incluidos los intermedios, antes de ordenar/agrupar por gen, transcripto, cromosoma y hebra. Así se evita fabricar un salto entre anclajes separados por otro exón. No se presupone que las filas de un transcripto sean consecutivas. Se valida la cadena y se calculan uniones solo entre exones consecutivos del modelo completo.

Se inspeccionaron2155005 registros de exón y78724 registros de gen. El filtro de anclajes seleccionó7023 grupos de transcripto, con46232 exones recuperados completos; no son lecturas ni unidades biológicas. Se exportan3460 referencias de testigos gen/transcripto por clave candidata. Una referencia puede repetirse para varias claves con la misma geometría; no sumar como evidencia independiente.

## Controles y límites

- Se reprodujeron exactamente las17 coincidencias del mismo gen de la auditoría anterior; se exige concordancia de estado para cada una de las1901 claves.
- Se recuperaron todos los testigos de las73 uniones canónicas de genes alternativos del QC de conflictos. El nuevo total528 incluye esas73; no se suman de nuevo.
- Diez pruebas nuevas cubren exón intermedio, transcritos intercalados, genes con igual nombre de transcripto, cromosoma/hebra, ambos extremos, versiones/PAR_Yy separación entre cobertura y novedad. Control positivo sintético solo valida software, no biología.
- **166 tests técnicos pasan.** No se calculan p-valores, tamaños de efecto o potencia ni se adquiere clínica individual. No se autentica el origen de las lecturas ni se cuentan referencias como réplicas.

El resultado describe una versión concreta de referencia. Una unión no encontrada puede depender de cobertura/anotación, genes atribuidos, calidad de modelos, alineamiento o biología no caracterizada. No se identifica su causa en este QC. Del mismo modo, una geometría anotada en otro gen puede coexistir con un transcripto extendido; este análisis no lo confirma o descarta.

## Archivos y siguiente tarea

`annotation.tsv`:1901 claves con estado global, todos los IDs alternativos, conteos y grupo de cobertura. `reference_witnesses.tsv`:todos los testigos ENSG/ENST, relación mismo/otro gen y geometría. `summary.json`:particiones, control de memoria/cobertura y cruce autor. Código: scripts/audit_global_geometry.py; fuentes/hashes/comandos en sources.json y run.json.

Reproducción: `python scripts/audit_global_geometry.py --reference /ruta/gencode.v47.annotation.gtf.gz`; `python -m unittest discover -s tests -v`.

Esta etapa de QC global queda completada. No priorizar las821 sin coincidencia como nuevas dianas: cobertura excluida y lecturas siguen pendientes. Siguiente tarea segura seleccionada del backlog: iniciar reproducción acotada de #14 (GSE126542/GSE121569), verificando paquetes, procedencia, scripts y unidad de replicación antes de recalcular resultados. Solo accesiones/grupos publicados y variables técnicas; excluir clínica personal. Si falta un insumo, documentarlo y retomar QC de cobertura sin simular resultados. No autoriza contactos, gastos, laboratorio o merge.
