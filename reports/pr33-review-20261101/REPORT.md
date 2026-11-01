# Revisión de integración del PR #33 — 01/11/2026

## Evidencia y alcance

Revisados el estado remoto, las issues abiertas, los dos PR abiertos, las cuatro páginas de cambios del PR33 (332 archivos) y la divergencia con main. La lectura de código se concentra en identidad/configuración, descarga acotada, ejecución completa, selección de ordinales, extracción de uniones y validación/exportación de QC; el inventario no implica una nueva auditoría científica de cada informe histórico. No hay reviews ni hilos de revisión previos registrados en la consulta.

Cabeza revisada: cd0fe69541cb252c356dce33308dc09851d3b43a. Main consultado: d1bbf0e1df64c68e28597da339f23029c83df2cd. Main tiene dos commits automáticos posteriores al ancestro común; sus tres rutas son reports/2026-10-31-pubmed.md, reports/2026-11-01-pubmed.md y state/seen_pubmed_ids.json. No coinciden con las rutas del PR33. GitHub devuelve mergeable=true; esto no equivale a una fusión realizada ni a revisión externa.

Pregunta de revisión: ¿los resultados conservados son coherentes y los validadores rechazan artefactos incompletos antes de considerar la integración? Criterio de fracaso: aceptación silenciosa de QC incompleto, discrepancia en resultados preservados, regresión de pruebas o solapamiento no resuelto con main. La revisión no abre una nueva hipótesis biológica ni autoriza datos adicionales.

## Hallazgo corregido

El validador comprobaba las sumas de los histogramas existentes, pero no exigía que existieran las siete métricas. Dos archivos igualmente incompletos, con histograms={} en el objetivo críptico, podían superar la validación. Se reprodujo el defecto sobre copias en memoria de JSON agregados. Los archivos reales sí contienen las siete métricas: este hallazgo no cambia las cuentas ni invalida retrospectivamente sus atributos guardados.

Ahora se exige el esquema de dos políticas de anclas, dos objetivos, campos de observación e histogramas, y las siete métricas exactas. Las observaciones deben ser enteros no negativos; las ponderaciones, enteros positivos con etiquetas de texto. Se rechazan métricas ausentes/adicionales, pesos negativos que se cancelan y booleanos contados como enteros. Los histogramas vacíos siguen siendo válidos cuando hay cero observaciones y se conserva el esquema completo.

## Pruebas y resultados negativos

399 tests locales correctos con Python3.12.14: 392 anteriores y siete regresiones nuevas. Compileall correcto. Sobre los resultados publicados en el PR: el validador corregido los acepta, el TSV vuelve a producir exactamente los mismos bytes y el resultado original completo conserva SHA256 cb26604160e43cdc04d2eab0a2525fc02f296059d70f5e0d9d731a32d9f6b4a7. La copia con esquema vacío, antes aceptada, ahora se rechaza. results.json y tests.txt conservan evidencia de esta revisión.

Sin descargas, FASTQ, alineamientos, nueva réplica o inferencia. La CI anterior de cd0fe695 tiene 392 tests en3.11/3.12, workflow41255076133; la CI de la corrección debe verificarse en la nueva cabeza y quedará enlazada en el PR. No contar las pruebas como experimentos.

## Trazabilidad y límites

Los manifiestos y los 392 tests de la fase científica anterior siguen referidos a sus commits históricos, especialmente cd0fe695 para el paquete final y920414d para el código ejecutado. La corrección posterior del validador no se presenta como código usado para realinear los datos. No se reescriben los JSON originales, sus manifiestos o sus informes para hacerlos corresponder con el código actual.

La evidencia continúa siendo reproducibilidad técnica exploratoria. No resuelve independencia molecular, unidades/lotes/pareamiento, efecto de TDP-43 ni función. La declaración publicada de tres réplicas biológicas por condición se conserva; no se la refuta por ausencia de mapa. Tampoco se deduce ausencia de splicing críptico del cero del primer control.

## Decisión y siguiente puerta

Recomiendo integrar el PR33 como entrega técnica después de verificar la CI de esta corrección. La ejecución de la fusión queda pendiente de decisión explícita; no hay merge o cierre automático. El PR30, usado en paralelo, sigue abierto e intacto en053ef70ce437cc637ec18278a2c07e3abd6bf58b.

Después de consolidar esta entrega, coordinar el siguiente contraste con el trabajo ya existente en PR30 antes de escoger fuente o descargar datos. No repetir los controles STMN2 para acumular soporte. Una nueva replicación biológica requiere cuentas de uniones, definición de evento y unidades experimentales independientes documentadas; los bloqueos actuales permanecen hasta recibir evidencia concreta nueva.
