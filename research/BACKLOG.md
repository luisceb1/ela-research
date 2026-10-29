# Backlog vigente — 29/10/2026

Consultar STATE.md, MASTER_EVIDENCE.md y reports/repository-integration. Las issues históricas describen incidentes iniciales; no repetir correcciones ya ejecutadas.

| Prioridad | Tarea | Estado y siguiente avance |
|---|---|---|
| P0 | Consolidación | Completada mediante PR #26: main verificado, 15 cabezas incluidas, 105 tests en Python 3.11/3.12 y dos auditorías GEO exitosas; PR dependientes cerrados por incorporación |
| P0 | #1 GEO | Inventario y enlace técnico ejecutados; integración no valida calidad biológica completa |
| P0 | #2/#17/#19 mapeo | Ejecutado por ENSG; controles positivos; incidente cero objetivos resuelto técnicamente |
| P0 | #20 catálogo | 21/1910, GENCODE y subconjunto autorS7/S8ejecutados;284S8+70soloS7. Pendiente cobertura completa, conflictos/ambiguos y filtros sobre universo corregido |
| P1 | Suplementos Bolger/crypTE | Descripción/esquema y QC ejecutados: reports/author-catalog-schema. Cotejo elegible ejecutado en reports/author-junction-match. Próximo resolver cobertura/ambiguos con fuentes trazables; separar no evaluables y no encontradas. S12 excluida; no importar clínica |
| P1 | #14 GSE126542/GSE121569 | Paquetes inventariados; reproducción completa pendiente. Auditar procedencia, licencia, réplicas, denominadores y sensibilidad |
| P1 | Descriptivos/escala | Ejecutados; paridad sin explicación. Etiquetas depositadas no equivalen a CI/no CI. No inferencia con n=1 |
| P1 | #15 CAMK2B/péptidos | CAMK2B estructural reproducido; genética/péptidos pendientes; sin validación proteómica independiente |
| P1 | #16 MEA | Software auditado; denominadores/completitud y protocolo experimental pendientes. Prototipo solo sintético |
| P1 | #21 AGRN | Verificar isoforma, soporte y antecedentes antes de priorizar ensayo funcional |
| P2 | #18 colaboración | Elegir pregunta falsable y controles; borrador sin envío, gasto o laboratorio |

Si hay bloqueo: registrar fuente, intento y motivo verificable; avanzar por otra vía segura. Persistir fuentes, parámetros, versiones, errores y negativos. Ramas breves desde main; esta consolidación no autoriza futuros merges sin revisión ni cierres automáticos.

Auditoría crypTE en rama breve desde main,115tests locales. Fuentes verificadas recuperables con --fetch del script audit_author_catalog.py; S7/S8 contienen filas no reconstruibles y siete etiquetas intrónicas no explicadas. Corregir cobertura/unidades antes de priorización; no producir coincidencias por proximidad ni reparar tablas silenciosamente.

Ampliación de PR28:125tests y354coincidencias estrictas en subconjunto de cultivo(284S8+70soloS7);1159no encontradas no son nuevas ni ausentes. Control STMN2canónico recuperado; críptico excluido por bloques inválidos. Revisar conflictos de gen y cobertura mediante fuente primaria trazable antes de filtros/priorización; alternativa segura #14 si falta enlace de modelos. No crear otra cadena de PR dependientes.
