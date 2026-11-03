# Revisión de PR #39 — 03/11/2026

Cabeza revisada: `1688e806e8071f6edb7b7d2a283cedd086b1e5a7`; base main `9076802fa78bfd1e4cdc97a3b92dd24a06d054c4`. PR abierta, no fusionada, sin comentarios de revisión ni nuevos datos en GitHub. Las búsquedas de literatura/acceso cerradas no se repiten: no hay una fuente numérica nueva concreta que habilite su reapertura.

## Corrección de entrada

Se detectó que el validador exigía amplitud y día a células excluidas por registro fallido. Eso puede inducir a borrar exclusiones o rellenar valores inexistentes. Ahora conserva sus IDs y motivo, sin exigir esas mediciones y sin incluirlas en n=34/30/25 ni en ningún efecto. Una célula incluida sigue requiriendo valor finito, unidad y calendario válidos. Los metadatos numéricos de filas excluidas no se consideran validados ni analizables por esta puerta; permanecen como registro de exclusiones para revisión.

También se rechazan contratos/revisiones JSON de tipo incorrecto y filas CSV con más campos que cabecera. Son controles de formato, no evidencia experimental. Se mantienen los tres bloques completos del contrato v1 y la regla de enmienda previa si los datos reales tienen otro diseño. No se suaviza el criterio científico para superar un bloqueo de datos.

Pruebas artificiales nuevas: exclusión sin medición conservada; contrato JSON no objeto; revisión no objeto; CSV desbordado. No se genera un conjunto neuronal simulado ni se implementa el LMM sobre datos inventados.

## Solicitud preparada

`FIG4D_DATA_REQUEST.md` concreta el mensaje y destinatario de correspondencia verificado en el manuscrito. No se ha enviado ni creado borrador externo. No se pide autorización de contacto como parte de una confirmación rutinaria: el encargo original la exige expresamente para comunicaciones externas.

## Dictamen científico

La PR sigue siendo una auditoría con plan condicional. No acredita un rescate propio, originalidad biológica, acceso a datos ni reversión posdéficit. La validación informática no resuelve el bloqueo. Única continuación útil de esta línea: obtener el archivo original y sus claves por un enlace nuevo o por petición específicamente autorizada.
