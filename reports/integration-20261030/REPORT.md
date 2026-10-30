# Integración y revisión de planning — 30/10/2026

## Decisión y alcance

Integrar los PR #28 y #29 tras revisión conjunta y autorización del usuario en la conversación. La autorización corresponde a esta integración concreta; no habilita merges futuros, cierres de issues, comunicaciones, gastos, laboratorio o publicación externa. No se ejecuta un análisis biológico nuevo.

Base común: `8dfa7ce7c4cc77f28185eaa286e681b0c9d5ed39`.
Cabeza revisada #28: `27f34d1b9b069616c0b3086518377d3e3df3ea40`.
Cabeza revisada #29: `18affb1f6d06b43ce069960f2088c7a5db4b18e3`.
Merge #28 en main: `fc9aa3835373146988fee5e2274160596457a92f`.

El commit de reconciliación de #29 tiene como padres su cabeza revisada y main tras #28. Los estados finales, SHAs y checks son verificables en los [PR #28](https://github.com/luisceb1/ela-research/pull/28) y [#29](https://github.com/luisceb1/ela-research/pull/29) y en Actions. No se infiere éxito de CI a partir de una cabeza anterior.

## Revisión y controles

Se revisaron AGENTS, protocolo, estado/backlog/evidencia de ambas ramas, issues abiertas, archivos modificados y CI. Las ramas compartían cambios documentales en README, STATE, BACKLOG y MASTER_EVIDENCE. La simulación de fusión produjo conflictos en esos cuatro archivos; se resolvieron manualmente. Los demás cambios se conservan por su blob Git, sin modificar el código de los análisis. Los ocho documentos de origen se conservan en `history/pr28` y `history/pr29`.

Control de integración: conservar ambas líneas de código/resultados sin sobrescrituras, resolver el planning duplicado y ejecutar la suite combinada. Criterio de fracaso operativo: pérdida o divergencia no explicada de blobs, documentos incompatibles, pruebas fallidas o CI fallida en la cabeza que se vaya a fusionar. La integración se detiene ante cualquiera de ellos.

Resultado local: **244 tests correctos en Python 3.12.14**, `python -m unittest discover -s tests -v`; `python -m compileall -q scripts tests` correcto. Son 166 + 183 − 105 tests compartidos, no experimentos ni réplicas. El log se conserva en `combined-tests.txt`; el manifiesto fija los hashes del código, tests y referencias locales usados. CI ejecuta la suite offline en Python 3.11/3.12. No se redescargaron ni reejecutaron todos los pipelines de datos reales en esta revisión.

## Evidencia conservada y resultados negativos

- #28: anotación/catálogos, conflictos e identidad molecular, inventario funcional y originalidad dirigida. La partición 545/353/182/821 no acredita descubrimientos; la propuesta UNC13A v0.4 sigue siendo conceptual.
- #29: reproducción agregada, BED/Rmd, diseño, integridad de cuentas y sensibilidades descriptivas. No refit inferencial propio ni PSI. Los bins examinados no solapan las regiones CE publicadas contrastadas; no se infiere ausencia molecular.
- SH-SY5Y: seis enlaces exactos a ENA, pero cuatro alias y dos conflictos de hebra impiden el reanálisis conjunto de siete uniones. La búsqueda acotada de definición no recuperó el fichero necesario. No repetirla sin fuente nueva.
- No se crean cohortes independientes al reutilizar tablas, series o análisis del mismo estudio.

El resumen semanal existente `reports/weekly/2026-10-30.md` se incorpora con #29; no se genera otro balance de siete días. Sus referencias a ramas pendientes describen el momento de redacción; el estado vigente lo fija `research/STATE.md` y GitHub.

## Planning revisado y siguiente prueba

Una sola tarea nueva: aplicar `research/NEXT_STUDY_GATE.md` a un máximo de tres fuentes independientes nuevas. Antes de calcular efectos se exige identidad de unión, cuentas, controles y unidades biológicas documentadas. Si ninguna cumple, registrar el rechazo y detener ese ciclo. El plan específico debe fijar pregunta, predicción, controles y criterio de fracaso antes de analizar cuentas.

Quedan bloqueados el refit por dependencias incompletas, las siete uniones SH-SY5Y por identidad molecular y la reconstrucción funcional posdéficit por falta de datos enlazados. Las issues técnicas se actualizan con evidencia y pendientes, sin cierre automático. La selección de una fuente no equivale a replicación externa conseguida; tampoco a validación funcional.
