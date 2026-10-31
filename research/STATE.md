# Estado vigente — 31/10/2026

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

Validar FASTA/índice/versiones del alineador y motivos de las dos uniones STMN2 antes del piloto GSE122069. El contrato de coordenadas ya se fijó en reports/stmn2-junction-contract-20261031, reutilizando proyecciones auditadas y con controles sintéticos: críptica chr8:+ 79611214→79616822, canónica 79611214→79636802 (límites exónicos 1-based, GRCh38). No se ha revalidado GTF completo ni FASTA, ni creado índice o procesado FASTQ. El piloto continúa bloqueado, no se acepta todavía replicación externa.

Base observada en esta ejecución: main f898b2967aae8909db1796753f9d2cae2bf966ef; #28/#29/#31 integrados. Único PR previo abierto: #30, cabeza 053ef70ce437cc637ec18278a2c07e3abd6bf58b, draft y activo con otro chat. Informe y diferencias leídos; no se modifica ni reproduce RiMOD/NYGC. Las ramas históricas permanecen como historial, no trabajo pendiente adicional.


## Verificación y operación

Base main: 244 tests locales correctos en Python 3.12.14 (166 + 183 − 105 compartidos), compileall correcto. CI por SHA en Python 3.11/3.12. No se reejecutaron todos los pipelines de datos reales durante la integración. No se añaden experimentos por combinar tests.

Las diez issues históricas no se cierran automáticamente. Las ya ejecutadas se actualizan con evidencia y pendientes precisos. No contactos, publicación externa, clínica personal, gastos o laboratorio sin autorización. La integración autorizada en este turno no concede autorización general de merges futuros.

Historial anterior de ambos estados: reports/integration-20261030/history. El resumen semanal de 30/10 se conserva sin duplicarlo.

## Auditoría de fuentes en esta propuesta de PR

253 tests locales correctos (244 base + 9 nuevos), compileall correcto. Python 3.12.14; QC real del Parquet con PyArrow 21.0.0 en la ejecución previa de este ciclo, repetición idéntica por bytes y hashes comprobados al retomar. E-MTAB-15653: 2.598.287 registros, 22 bibliotecas; SDRF 44 filas FASTQ, 21 nombres de archivo derivados distintos. Hay un conflicto citosol/núcleo en NMD, sin reparación automática; no afecta el enlace único de las seis bibliotecas citosólicas basales. La independencia biológica sigue sin certificar. No se calcula PSI, inferencia ni función. La integración de esta entrega se verifica por el estado de PR31 y su SHA/CI; no añade replicación biológica.

## Actualización: unidades de E-MTAB-15653

Auditoría acotada completada en reports/fractionation-units-20261030: XML primario y suplemento PDF nuevo verificados por hash. El PDF no aporta un mapa de cultivos independientes; seis enlaces técnicos basales correctos no certifican seis unidades biológicas. La vía inferencial sigue bloqueada y esta búsqueda se cierra sin repetirla. Siguiente trabajo seguro propuesto: redactar plan de recursos y controles de los seis runs GSE122069 ya identificados, sin descargar/alinear ni abrir un cuarto candidato. No efectos, PSI o inferencia en este ciclo. Mismo PR31 abierto; PR30 separado. Los próximos pasos anteriores sobre buscar documentación de unidades quedan reemplazados por este resultado.


## Cierre de revisión y plan operativo

Descripción y punto de continuación reconciliados. La integración concreta de #31 está autorizada por Luis; #30 se mantiene abierto y su rama intacta. Plan GSE122069 en reports/gse122069-resource-plan: RAM disponible 8 GiB, piloto condicionado a índice compatible y medición de recursos; ninguna descarga/alineamiento iniciada. La CI offline no reproduce FASTQ ni certifica viabilidad del piloto.

## Contrato STMN2 — 31/10/2026

Pregunta/falsador fijados antes de ejecutar: research/plans/2026-10-31-stmn2-junction-contract.md. Candidato canónico único en la proyección y coherente con exones de ENST00000220876.12/ENST00000518111.5; no son réplicas biológicas. Conversiones intrónicas/BED y extracción SAM SE sintética comprobadas. 275 tests locales correctos (253 previos +22 nuevos), compileall correcto; Python 3.12.14. Contrato idéntico por bytes en dos ejecuciones, entradas por SHA256 y ficheros heredados cotejados con Git blobs. La CI de este PR se verifica por su nueva cabeza; no se presupone correcta ni reproduce FASTQ.

No efectos, PSI, significación ni función. Razón propuesta críptica/(críptica+canónica) sería condicional a esas dos ramas; otras ramas del donante no medidas. Prototipo requiere XS y NH=1, MAPQ>=20 (excluye255), anclas contiguas>=8; retiene flags de duplicación y rechaza PE. Pendiente comparar con herramienta independiente y semántica del alineador. No producción/crudos desde esta entrega.

Ensembl agotó timeout y no aportó referencia. 8 GiB RAM, ~62,79 GB libres observados, sin HISAT2/STAR/samtools. Esto no es benchmark ni autoriza más recursos que el plan previo. Git clone sin credenciales; acceso al código por conector comprobado. Se registran fallos de materialización local, corregidos por blobs exactos antes de la suite final. Ningún cambio en main o rama30, merge/cierre, gastos, contactos o publicación externa. Las menciones históricas a PR31 abierto y 253 pruebas corresponden al ciclo anterior; este apartado y Única próxima tarea son los vigentes.
