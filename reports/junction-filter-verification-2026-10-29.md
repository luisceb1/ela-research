# Filtros explícitos para cribado Iso-Seq · 2026-10-29

**Actualización posterior:** la clasificación ALS-CI literal de dos columnas fue corregida en reports/ALS_CI_metadata_correction_2026-10-29.md. La fuente21se recuperó y su fallo de agrupación se explica en reports/junction-filter-reconciliation. No interpretar las cifras históricas siguientes como estado más reciente ni como validación del parser antiguo.

**Reproducción ejecutada:** [GitHub Actions 40871481382](https://github.com/luisceb1/ela-research/actions/runs/40871481382), resultado **success**, artefacto `cross-dataset-junction-audit` id `12896421253`.

## Conteos auditados (desde `filter_audit.json`)
| Escalón | Uniones |
|---|---:|
| Intersección exacta de modelos BambuTx de ambas fuentes, ausentes de ENST internos | 1.910 |
| Control = 0 con y sin 5Aza y TDP43KD >=3 en cada condición | 9 |
| >=2 lecturas en las **dos** columnas ALS-ci, ninguna en las **dos** CTL | 32 |
| Intersección simultánea de los dos filtros estrictos | **0** |

Estas cifras se refieren a lecturas únicas **asignadas a modelos de transcrito**; no a lecturas de junction-spanning. La identificación de 1910 eventos usa referencias ENST solo internas y NO acredita descubrimiento de uniones nuevas. El análisis antiguo comunicaba 21 uniones tras otras restricciones que todavía no hemos reconstituido; 21 y 1910 no deben describirse como un resultado discrepante de idéntico procedimiento.

## Auditoría de columnas (observación objetiva)
- Cultura: `i3N_Ctrl_noAza`, `i3N_Ctrl_5Aza`, `i3N_TDP43KD_noAza`, `i3N_TDP43KD_5Aza` (una biblioteca por condición, sin réplicas biológicas).
- Cerebro `ALS-ci`: `ALS-ci_02988`, `ALS-ci_04118` (**dos columnas**).
- Cerebro `CTL`: `CTL_03374`, `CTL_03662` (**dos columnas**).
- El informe anterior cita tres casos ELA-CI. No hay justificación todavía para equiparar sus categorías clínicas con las dos columnas `ALS-ci`. Comprobar GSM, denominaciones y procedencia clínica antes de reclasificar.

## Interpretación y próximos controles
1. El cero en la intersección estricta es reproducible **bajo esta regla de columnas**, pero no demuestra ausencia de mecanismos relevantes.
2. Conservar TSV de 1910 uniones y columnas por muestra; antes de cualquier candidatura exigir profundidad/reads de unión y compatibilidad con GENCODE versionada.
3. Recuperar el código original del filtro de 21; reproducirlo sin asumir que su diferencia es error.
4. Revisar clasificación clínica original y confirmar independencia de muestras.
5. No presentar como validación independiente entre grupos: ambos conjuntos proceden de Bolger et al. 2026.
