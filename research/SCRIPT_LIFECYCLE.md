# Ciclo de vida de scripts — 03/11/2026

Este inventario orienta la elección de código; no habilita ejecuciones. Clasificación revisada sobre main `867e1478d4eaa5f31d078001785eed246783a27d`. Los scripts de análisis científicos restantes mantienen el alcance y las dependencias de sus informes.

| Grupo | Archivos o punto de entrada | Estado y uso |
|---|---|---|
| Entrada condicional Fig.4d | `scripts/check_functional_rescue_input.py` | Validador vigente de esa línea, contrato deshabilitado; no estima efectos ni certifica independencia por IDs |
| Comparación cerrada RefSeq | `scripts/compare_unc13a_refseq.py` | Reproducción offline del inventario congelado; no selecciona otro piloto |
| Recuperaciones del piloto CTRL | `recover_index_range.py`, `recover_ctrl_read.py`, `recover_ctrl_r2.py`, `recover_ctrl_r2_ipv4.py`, `recover_ctrl_r2_final.py`, `recover_ctrl_r2_resume.py`, `recover_ctrl_r2_clock.py` | Históricos: intentos, fuentes y cargos específicos; conservar junto con sus pruebas |
| Ejecución del piloto cerrado | `real_pilot_workflow.py`, `cached_index_pilot.py`, `recovered_read_pilot.py`, `offline_control_pilot.py` | Históricos y ligados a linajes/recibos concretos; no son la entrada genérica de un nuevo estudio |
| Auditoría del locus cerrado | `unc13a_locus_audit.py`, `unc13a_locus_audit_v2.py`, `unc13a_locus_pipeline.py` | Histórico; v2 es la corrección final de guarda/contabilidad de ese linaje, no autorización de reejecución |
| Infraestructura compartida existente | `bounded_http_transport.py`, `process_supervisor_v2.py`, `workflow_seal.py`, `pilot_execution_policy.py`, `pe_fragment_contract.py` | Candidatos a reutilización bajo contrato probado; sus usuarios históricos siguen dependiendo de identidades concretas |
| Verificación de software | `scripts/run_offline_tests.py` | Entrada de CI con informe de éxitos/fallos/omisiones; no ejecuta análisis científicos nuevos |

Todos los nombres de script de la tabla pertenecen a `scripts/`. Los runbooks de recuperación en `research/runbooks/` son instrucciones históricas: consultar STATE/BACKLOG antes de usarlos.

## Deuda comprobada

Funciones `recover` y `monitor` idénticas se repiten en las variantes R2 final/IPv4/resume; también se repiten guardas y entradas CLI. Las auditorías locus v1/v2 comparten 206 líneas idénticas de 271/306, según comparación de líneas de la base indicada. Hay dependencias transitivas como `transport.base.Budget` y `base.real`. Mantener una corrección en varias copias aumenta el riesgo de divergencia.

La conservación histórica explica parte de la duplicación, pero no convierte esas variantes en una arquitectura reutilizable. Una nueva implementación debe importar servicios comunes directamente, recibir configuración explícita y comparar salidas/recibos con fixtures. No editar código sellado solo para reducir duplicación: los hashes de identidad forman parte de la procedencia.

## Verificación

Trabajo general: `python scripts/run_offline_tests.py --report test-results/offline.json`. Permite omisiones, enumera IDs/motivos y publica resumen. Si no descubre pruebas o un patrón solicitado no encuentra ninguna, falla.

Trabajo paired-end: instala `research/requirements-pe-contract.txt` y ejecuta los mismos 21 módulos seleccionados previamente con `--fail-on-skip`. Cualquier omisión hace fallar ese trabajo. El filtro de rutas incluye el runner y sus pruebas.

Los informes JSON y el resumen de GitHub Actions distinguen pruebas descubiertas, ejecutadas (descubiertas menos omitidas), correctas, fallos, errores y omisiones. El verde de un trabajo con omisiones no acredita esos controles omitidos ni pruebas de datos reales.
