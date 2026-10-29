# Backlog vigente — 29/10/2026

Consultar STATE.md, MASTER_EVIDENCE.md y reports/repository-integration. Las issues históricas describen incidentes iniciales; no repetir correcciones ya ejecutadas.

| Prioridad | Tarea | Estado y siguiente avance |
|---|---|---|
| P0 | Consolidación | Completada mediante PR #26: main verificado, 15 cabezas incluidas, 105 tests en Python 3.11/3.12 y dos auditorías GEO exitosas; PR dependientes cerrados por incorporación |
| P0 | #1 GEO | Inventario y enlace técnico ejecutados; integración no valida calidad biológica completa |
| P0 | #2/#17/#19 mapeo | Ejecutado por ENSG; controles positivos; incidente cero objetivos resuelto técnicamente |
| P0 | #20 catálogo | 21/1910 explicado y GENCODE ejecutada; pendiente catálogo de autores y filtros sobre universo corregido |
| P1 | Suplementos Bolger/crypTE | Próxima tarea científica: descripción/esquema, hashes y convenciones antes de cotejar 1901 claves. No importar tablas clínicas |
| P0 | #14 GSE126542/GSE121569 | 63 campos de agregados y24 de índices concordantes; BED/R Fratta auditados con sensibilidad de fórmula/deduplicación. Siguiente mapa técnico de diferenciación; sin cierre automático |
| P1 | Descriptivos/escala | Ejecutados; paridad sin explicación. Etiquetas depositadas no equivalen a CI/no CI. No inferencia con n=1 |
| P1 | #15 CAMK2B/péptidos | CAMK2B estructural reproducido; genética/péptidos pendientes; sin validación proteómica independiente |
| P1 | #16 MEA | Software auditado; denominadores/completitud y protocolo experimental pendientes. Prototipo solo sintético |
| P1 | #21 AGRN | Verificar isoforma, soporte y antecedentes antes de priorizar ensayo funcional |
| P2 | #18 colaboración | Elegir pregunta falsable y controles; borrador sin envío, gasto o laboratorio |

Si hay bloqueo: registrar fuente, intento y motivo verificable; avanzar por otra vía segura. Persistir fuentes, parámetros, versiones, errores y negativos. Ramas breves desde main; esta consolidación no autoriza futuros merges sin revisión ni cierres automáticos.


## Fase #14 — reproducción agregada, rama independiente desde main

29/10/2026: reports/issue14-reproduction reproduce63campos agregados (45expresión/18extracciónDEXSeq) sin discrepancias. Fuentes GEO descargadas y fijadas; código recibido conservado sin ejecutar, sin tablas por caso/clínicas/genéticas importadas. STMN2/UNC13A mantienen dirección entre CPM/MR; TARDBP cambia de signo. DEXSeq102fragmentos, no refit niPSI; doce columnas de contraste no son doce diferenciaciones. Nueve tests nuevos sobre105de main:114OK. PR28con166tests sigue separado y no fusionado: contiene originalidad/crypTE/QCglobal posteriores al estado base de main. Leer ambos PR y reconciliar estados al integrar; no declarar esos informes ya incorporados. Issue14no se cierra: próximos BED/RdeFratta, deduplicación/denominadores y mapa de diferenciación121569. Sin nuevas cohortes, hallazgos clínicos, contactos, gasto, laboratorio o merge automático.

## Uniones Fratta auditadas — 29/10/2026, ampliación PR29

reports/fratta-junction-audit: BED/Rmd públicos fijados por SHA256 y Gitblob.241filas→69únicas/172repetidas,16muestras/7pares+2unsorted;27combinaciones ausentes rellenadas con0por método autor, no ceros observados.24campos agregados del paquete concordantes. Rmd2694incluye3clasesUNC13A;2766usa2clases. Cambio medio principal72.67puntos, dosclases72.00, sumar duplicados63.81; no porcentaje molecular, sensibilidad biológica ni nueva cohorte. No se leyeron archivos alélicos/clinica ni exportaron filas por muestra.124tests de esta rama (105base+19nuevos), PR28con166sigue separado. Próximo: mapa técnico biblioteca/experimento-diferenciación deGSE121569 antes de cualquier refit; issue14sigue abierta, sin contactos/laboratorio/gasto/merge.
