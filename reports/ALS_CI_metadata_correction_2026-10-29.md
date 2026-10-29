# Corrección de grupos clínicos y reanálisis GEO — 2026-10-29

Ejecución verificada: [GitHub Actions run 40872016985](https://github.com/luisceb1/ela-research/actions/runs/40872016985), conclusión `success`; artefacto `cross-dataset-junction-audit` id `12896272868`. Se inspeccionaron `filter_audit.json` y `summary.json`.

## Corrección fundamentada
Fuente primaria: [GSE315972, GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE315972), GSM9441959–GSM9441966.

| Grupo clínico | Donantes de GEO | n |
|---|---|---:|
| ALS-CI | 03363, 02988, 04118 | 3 |
| ALS-nonCI | 02759, 02763, 03634 | 3 |
| Controles | 03374, 03662 | 2 |

El prefijo `ALS-C9_03363` en la matriz de transcritos **no sustituye** el fenotipo anotado ALS-CI en GSM9441960. Clasificar por prefijo `ALS-ci_` excluía erróneamente al donante 03363. Se corrigió `scripts/filter_shared_junctions.py` para agrupar por IDs verificados, y para exigir ≥2 lecturas únicas asignadas en al menos 2 de los 3 ALS-CI, 0 en ambos controles.

## Resultados antes/después
| Métrica | Antes: 2 columnas ALS-ci | Corregido: 3 donantes ALS-CI |
|---|---:|---:|
| Uniones compartidas con filtro amplio | 1910 | 1910 |
| Filtro celular estricto | 9 | 9 |
| Filtro cerebral estricto | 32 | **100** |
| Intersección estricta | 0 | **0** |

**Interpretación:** el cero en intersección persiste en estos datos y reglas; NO equivale a imposibilidad de uniones crípticas relevantes. Las 100 uniones cerebrales no son descubrimientos ni las 9 neuronales tienen una prueba de replicación (una biblioteca por condición). Los recuentos son por isoforma, no lecturas que atraviesen físicamente uniones.

## Bloqueo de reproducción exacta de los 21
El informe anterior declara un conjunto base más restrictivo de 21 uniones / 20 genes; el script actual aplica una intersección más amplia de 1910, por lo que **aún no se ha reproducido el paso 1910→21**. El ZIP original `ELA_06_cruce_sistematico_longread_2026-10-29.zip` se identificó en la biblioteca, pero su materialización binaria no estaba autorizada en esta sesión. Sin código original o filtros exactos, no atribuir diferencia a un error ni afirmar equivalencia.

## Siguiente evidencia discriminante
Importar código original del cribado 21, comparar IDs y motivos de exclusión, verificar lecturas de unión con BAM/SRA y anotación GENCODE completa versionada. Mantener UNC13A como hipótesis experimental funcional, no resultado clínico.
