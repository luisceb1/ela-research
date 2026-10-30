# Estado vigente — 30/10/2026

## Alcance

Esta entrega reconcilia los contenidos de PR #28 y #29. El PR #28 fue incorporado a main mediante fc9aa3835373146988fee5e2274160596457a92f; la reconciliación de #29 se registra en el acta de integración y su estado final se verifica en GitHub por SHA y CI. La versión conjunta contiene ambas líneas de trabajo, sin añadir por ello evidencia científica independiente.

Hay auditorías técnicas, reproducción numérica, descriptivos y propuestas. No hay una nueva diana validada, experimento propio o beneficio clínico demostrado. Las series o tablas reutilizadas no se cuentan como cohortes nuevas.

## Completado

| Línea | Resultado | Informe |
|---|---|---|
| #1/#2/#17/#19 | Inventario técnico y mapeo por ENSG; fallo de cero objetivos corregido | reports/geo-audit, isoforms, mapping-positive-controls |
| #20 | Parser histórico corregido; 1910 uniones agrupadas y 1901 con soporte asignado positivo | reports/junction-filter-reconciliation |
| Catálogos y geometría | 545 anotadas v47, 353 solo autores, 182 pendientes, 821 sin coincidencia en recursos limitados; no novedad inferida | reports/global-junction-geometry y auditorías de autores |
| Originalidad | Auditoría dirigida, límites documentales e inventario funcional; propuesta v0.4 conceptual | reports/originality-audit, functional-data-inventory |
| #14: expresión/uniones | 45 campos de expresión, 18 de extracción DEXSeq y 24 de índices concordantes; duplicados/fórmulas auditados | reports/issue14-reproduction, fratta-junction-audit |
| #14: DEXSeq | Diseño por dos lotes, 7030428 cuentas concordantes; sensibilidad de magnitud/denominadores y regiones CE comprobadas | reports/gse121569-design, dexseq-qc, dexseq-magnitude, dexseq-coverage, ce-bin-coordinate-audit |
| SH-SY5Y | Seis enlaces exactos a ENA; S6 y convenciones inspeccionadas; búsqueda histórica acotada concluida | reports/shsy5y-junction-map, junction-definition-search |

Los informes preservan los hashes, parámetros, errores y resultados negativos de cada ejecución. Sus antiguos apartados «siguiente tarea» son históricos; no reemplazan este estado.

## Bloqueos científicos, no tareas activas

- Refit GSE121569: pozo/reactivo/fórmula y estructura de dependencia incompletos. No promover bibliotecas a diferenciaciones.
- Siete uniones SH-SY5Y: cuatro alias UNC13A y dos conflictos de hebra STMN2 pendientes. El fichero de definición referenciado por el pipeline no se recuperó en la revisión acotada. No reabrir sin fuente nueva.
- Contraste funcional posdéficit: seis fichas no permiten reconstruirlo con los materiales inspeccionados. No ausencia universal, ni ensayo ejecutado.
- 821 claves sin coincidencia: referencia/cobertura/asignación/soporte de lecturas incompletos. No priorizar como descubrimientos.
- Paridad de uniqueCounts y soporte por lecturas crudas siguen sin explicación completa. No dividir cuentas por dos ni llamarlas moléculas.

## Única próxima tarea

Aplicar [NEXT_STUDY_GATE.md](NEXT_STUDY_GATE.md): seleccionar o rechazar una fuente independiente con coordenadas de unión, cuentas, controles y unidades biológicas documentadas. Revisar como máximo tres candidatos nuevos en un ciclo. Si ninguno cumple, registrar el resultado y detener esa selección, sin otra cadena de búsquedas equivalentes.

## Verificación y operación

Suite conjunta: 244 tests locales correctos en Python 3.12.14 (166 + 183 − 105 compartidos), compileall correcto. CI por SHA en Python 3.11/3.12. No se reejecutaron todos los pipelines de datos reales durante la integración. No se añaden experimentos por combinar tests.

Las diez issues históricas no se cierran automáticamente. Las ya ejecutadas se actualizan con evidencia y pendientes precisos. No contactos, publicación externa, clínica personal, gastos o laboratorio sin autorización. La integración autorizada en este turno no concede autorización general de merges futuros.

Historial anterior de ambos estados: reports/integration-20261030/history. El resumen semanal de 30/10 se conserva sin duplicarlo.
