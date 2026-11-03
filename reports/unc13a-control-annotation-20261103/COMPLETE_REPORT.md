# Contraste completo del inventario comunicado de UNC13A

## Evidencia y comprobaciones

Luis adjunta el archivo completo `ELA-UNC13A-audit-seal.json`, conservado sin modificar bytes como `operator-audit-seal.json`. SHA256: a42c22813d033baff2f73de07a894eb62f11624659790d3e6c5e3ef0cb74d8c8. El hash del plan en el sello coincide con el comunicado al preparar: 27c4a38229d621059da941b84fadc3053dac811bf5d5e4ff497c17d99146121b.

Se comprueba concordancia íntegra entre las rutas de texto y HTSlib a 15 y 8 bases, y coherencia de todas las filas visibles, QC y coordenadas con el resumen previamente aportado. Ahora están disponibles las 31/33 uniones, sin filas pendientes. El archivo comunica ejecución sellada y replay idéntico del control; no se han podido recalcular los hashes de los demás archivos WSL ni consultar por separado el recibo externo de este intento. No se atribuyen nuevos tiempos o RSS. Cargo 7.322.807.977 bytes, cero bytes nuevos y puerta de cobertura insuficiente, sin promover.

## Método ejecutado

El mismo comparador probado previamente (`scripts/compare_unc13a_inventory_annotation.py`) se ejecuta sobre el sello completo, con la anotación cacheada cuyo hash coincide con el recibo de origen. No se cambia código, filtro, objetivo o umbral. Tabla completa y resultados: `complete-comparison/junctions.tsv` y `complete-comparison/comparison.json`. Comprobaciones de coherencia y conteos objetivo en `complete-assessment.json`. La ejecución previa parcial se conserva como histórica en `REPORT.md` y `comparison/`.

Referencia: cuatro transcritos UNC13A de hg38/GENCODE v47 cacheados desde UCSC; 47 uniones distintas, coordenadas intrónicas de base cero con inicio incluido y final excluido. La selección original de transcritos solapa una ventana concreta: no equivale a todas las anotaciones posibles ni a una fuente independiente.

## Resultado completo

| Anclaje | Uniones observadas | Coincidencias exactas con anotación cacheada | No contenidas en esa anotación |
|---|---:|---:|---:|
| 15 bases | 31 | 29 | 2 |
| 8 bases | 33 | 31 | 2 |

Las dos uniones no coincidentes son las mismas en ambas rutas, en hebra negativa y con un grupo de soporte cada una:

| Inicio0 | Fin0 | Soporte a 15 / 8 | Unión anotada más próxima | Diferencia inicio / fin |
|---:|---:|---:|---|---|
| 17627940 | 17629242 | 1 / 1 | 17627940–17629239 | 0 / +3 |
| 17648988 | 17649507 | 1 / 1 | 17648983–17649508 | +5 / −1 |

La proximidad se calcula por suma de diferencias absolutas de extremos entre uniones anotadas con la misma hebra/cromosoma. Es una descripción geométrica; no identifica el origen de la discordancia. Ninguna es uno de los dos eventos crípticos objetivo. Pueden reflejar una anotación incompleta, splicing alternativo o error de alineamiento; este único control con soporte unitario no discrimina esas explicaciones. No se califican como isoformas nuevas o hallazgos de ELA.

Las dos uniones adicionales al reducir el anclaje a 8 bases son anotadas (17639525–17639839 y 17639908–17640510), con un grupo cada una. La suma de soportes de eventos de toda la región es 76/79; no representa grupos únicos y no sustituye la cobertura del objetivo. Los conteos objetivos se confirman en [1,0,0] para ambas rutas. No hay otra unión dentro de ±2 bases de esos objetivos con la hebra esperada.

## Interpretación y decisión

La mayoría de las uniones coincide exactamente con la referencia y los dos decodificadores concuerdan. No aparece evidencia de un error general de coordenadas que explique la escasez del objetivo. Los filtros regionales tampoco descartan masivamente candidatos: 115 de 116 grupos aceptados. Esto apoya cerrar la depuración técnica con cobertura objetivo insuficiente, sin afirmar ausencia biológica de eventos crípticos.

No ampliar automáticamente a los 12.709.444 pares ni descargar/iniciar TDP con este control. Un grupo objetivo en el prefijo ordinal de un millón no permite garantizar que el resto alcance el mínimo prospectivo de 20, ni estimar de forma estable su profundidad. No relajar el mínimo ni reemplazar el objetivo por la suma de otras uniones tras observar el resultado.

El próximo trabajo recomendado es auditar anotación más extensa/metadatos o datos procesados disponibles del estudio para valorar qué biblioteca/diseño ofrece cobertura y réplicas útiles, antes de otro cómputo masivo. Las dos uniones unitarias quedan en un registro de observaciones sin priorizarlas como descubrimientos. Sin PSI, contraste entre condiciones, causalidad, rescate o inferencia clínica.

## Validación y alcance

Comparación real ejecutada sobre todas las filas del archivo adjunto; todas las comprobaciones de `complete-assessment.json` concuerdan. Se reutiliza el comparador con sus ocho pruebas previas, sin modificación de programa. No hay nuevo alineamiento, descarga o ejecución WSL. PR 36 sigue abierta sin fusionar.
