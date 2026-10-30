# Backlog vigente — 29/10/2026

Consultar STATE.md, MASTER_EVIDENCE.md y reports/repository-integration. Las issues históricas describen incidentes iniciales; no repetir correcciones ya ejecutadas.

| Prioridad | Tarea | Estado y siguiente avance |
|---|---|---|
| P0 | Originalidad — solicitud Luis | Auditoría dirigida entregada en reports/originality-audit; reclamos amplios descartados. Cierre documental acotado en FOLLOWUP.md; CTR2026 calendario indexado verificado, Guo final y solapamiento siguen limitados. Protocolo v0.4 incremental. Inventario funcional completado: seis fichas sin contraste posdéficit reconstruible; cierre acotado y sin certificación de novedad. QC de identidades completado en author-gene-ambiguity; 74conflictos auditados (73geometrías ya anotadas en otro gen); control global completado (528 claves anotadas solo en otros genes); siguiente reproducción acotada #14 y cobertura pendiente |
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

## Cierre documental de originalidad y propuesta vigente

Ciclo29/10/2026: reports/originality-audit/FOLLOWUP.md. CTR2026: métodos primarios indexados verifican administración a seis semanas con temblor; solapamiento de datos con CTR2025no resuelto, sin sumar replicaciones. Guo final sigue sin métodos accesibles; no trasladar preprint. Autoría bibliográfica corregida con PubMed/Stanford y original conservado en closure.json. Protocolo vigente v0.4 como extensión, originalidad no certificada; registros del mismo pozo son medidas repetidas. El cierre documental es acotado con bloqueos explícitos, no declaración de novedad. Siguiente tarea segura: inventario de disponibilidad de datos funcionales para unidad/basal/primera dosis; sin efectos hasta enlace de unidades. Si no hay brazo posdéficit reconstruible, documentarlo y volver al QC del backlog. Sin autorización de laboratorio/contactos/merge.

## Inventario funcional completado — 29/10/2026

reports/functional-data-inventory: seis fichas de ensayo/versión de cuatro familias; ninguna permite reconstruir nuestro contraste posdéficit con los materiales inspeccionados. Suplemento Keuss2024recuperado y texto revisado, sin manifiesto MEA de unidades; aceptado sigue403y calendario ASOpreKD. Chan/Beccari datos fuente existentes sin enlace biológico/longitudinal suficiente; Baughn anexo devuelveHTML. No ausencia universal ni resultado experimental negativo; no efectos calculados.140tests técnicos locales. Cierre de esta vía con bloqueos explícitos: no repetir sin nueva fuente primaria. Siguiente tarea segura seleccionada: QC de cobertura crypTE,36identidades de referencia no resueltas y278coincidencias autoras de gen ambiguo; sin reparar por proximidad ni priorizar novedad. Protocolo funcional v0.4 sigue conceptual.

## QC de identidad de genes — 29/10/2026

reports/author-gene-ambiguity:33de36claves tienen ENSG/locus confirmado;3deENSG00000276256ausente en v47con procedencia GTF GEO recuperada. Las278claves autoras ambiguas permanecen sin resolución única; no forzar por proximidad. Una clave GTPBP6chrYcondicional adicional, comprobada en3filasS8, dependiente de locus declarado y sin auditoría de lecturasX/Y.354estrictas originales intactas; sensibilidad355no las reemplaza.149tests técnicos locales, cuatroTSVidénticos en dos pasadas. Siguiente tarea segura: auditar74claves con coordenadas atribuidas a otro gen, conservar conflictos no resolubles; después cobertura/#14. No significado funcional, novedad, replicación nueva o autorización de laboratorio/merge.

## Conflictos de gen auditados — 29/10/2026

reports/author-gene-conflicts:74claves/23genes,298referencias a56filas autoras originales comprobadas.73uniones ya anotadas exactamente en v47bajo gen autor; en ambosGTFtambién existen modelos de los dos genes. Una unión deENSG00000278915frenteaENSG00000278946no encontrada bajo ninguno en v47, persiste conflicto. No reasignar ni inferir origen molecular;354estrictas intactas.156tests técnicos locales. Resultado limita reclamo de novedad basado en no encontrado para mismo gen. Siguiente tarea segura: geometría exacta contra todos los genes de v47para1901claves, sin restricción de gen candidato/autor; después cobertura/#14. No clínica, contactos, laboratorio, gasto o merge.

## Geometría global completada — 29/10/2026

reports/global-junction-geometry: 1901 claves / 1882 geometrías únicas. Coincidencias v47: 17 bajo mismo gen + 528 solo otros genes; 1356 claves no encontradas. Partición conjunta: 545 anotadas, 353 solo representadas con mismo gen en autores (incluye contexto S7), 182 de identidad/conflicto pendiente y 821 sin coincidencia en ambos recursos limitados. No 821 descubrimientos. Los 17 controles y todos los testigos de los 73 conflictos se reproducen; 166 tests técnicos locales. No reasignación molecular, función o novedad inferidas.354estrictas/355condicionales históricas intactas. QCglobal cerrado; siguiente tarea segura seleccionada: reproducción acotada #14 GSE126542/GSE121569, primero procedencia/paquetes/scripts/unidad de replicación, sin clínica personal ni resultados simulados. Cobertura excluida de821sigue pendiente; no priorizarlas como dianas. Sin contactos, gastos, laboratorio o merge automático.
