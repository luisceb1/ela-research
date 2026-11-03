# Auditoría local completada y contraste parcial con la anotación

## Evidencia disponible

Luis adjuntó `Texto pegado(8).txt`, con preparación y resumen final de la ejecución e521c124. El JSON comunicado se conserva en `operator-console-summary.json`. Reporta `sealed_exploratory_locus_audit`, igualdad de conteos/QC con el piloto previo, cero bytes nuevos y cargo acumulado constante de 7.322.807.977 bytes. No se dispone aún del archivo completo `audit-seal.json`, de sus hashes internos o del recibo externo de esta ejecución; no se afirma verificación independiente del sistema WSL ni duración/RSS nuevos.

El resumen informa de 116 grupos candidatos regionales, 115 aceptados, un descarte por calidad y 46 grupos con uniones solapantes antes de filtros, tanto a 15 como a 8 bases. Son grupos (RG,QNAME), con duplicados marcados retenidos; no moléculas únicas ni cobertura base a base. Las uniones distintas son 31 y 33. El objetivo canónico conserva soporte 1 y es la única unión comunicada dentro de dos bases de los objetivos y con la misma hebra. La puerta prospectiva permanece en cobertura insuficiente. No se suman otras uniones del gen para superar artificialmente el mínimo de 20 en los objetivos.

La preparación informa artefactos 19.279.425.997 bytes, texto plano 717.353.956, compactos 687.509.370 y recibos 20.931. Los artefactos están por debajo de 18 GiB; el error anterior de sumarles los temporales explica por qué la preparación anterior se bloqueaba. Son cifras de preparación, no el pico final de uso.

## Pregunta y método definidos antes de la comparación

Pregunta: ¿las uniones observadas coinciden exactamente con las uniones de los transcritos UNC13A cacheados en hg38? Control: correspondencia de cromosoma, ambos extremos intrónicos y hebra; un desplazamiento de una base o hebra contraria no cuenta como coincidencia. Criterio de fracaso: referencia/versiones distintas, geometría inválida, recuentos contradictorios o inventario incompatible. Las filas ausentes del resumen no se tratan como ceros y las no coincidentes no se etiquetan como nuevas isoformas.

Se verifica el SHA256 de la anotación contra `reports/unc13a-reference-strand-20261102/retrievals.json`. Fuente: UCSC, track wgEncodeGencodeCompV47, consulta cacheada de la ventana original. Sus cuatro transcritos UNC13A contienen 47 uniones distintas derivadas de extremos exónicos. Es una referencia de un proveedor y selección de transcritos que solapan la consulta, no inventario exhaustivo de isoformas. Convención: intrones con inicio incluido y final excluido, base cero.

El nuevo script `compare_unc13a_inventory_annotation.py` procesa JSON completo o el resumen de consola, deduplica filas repetidas por evento y rechaza soportes contradictorios. Genera `comparison/comparison.json` y `comparison/junctions.tsv`, con hashes de entrada, coincidencias y transcritos por unión. No alinea ni accede a red. Comando reproducible:

```bash
python scripts/compare_unc13a_inventory_annotation.py --inventory reports/unc13a-control-annotation-20261103/operator-console-summary.json --annotation reports/unc13a-reference-strand-20261102/sources/annotation.json --retrievals reports/unc13a-reference-strand-20261102/retrievals.json --out SALIDA_NUEVA
```

## Resultado ejecutado

| Ruta | Uniones comunicadas | Uniones con coordenadas disponibles | Coincidencias exactas | Filas todavía no disponibles |
|---|---:|---:|---:|---:|
| Anclaje 15 | 31 | 21 | 21 | 10 |
| Anclaje 8 | 33 | 21 | 21 | 12 |

Las 20 uniones de mayor soporte y la canónica fuera de ese listado aportan 21 uniones distintas en cada ruta; el conjunto de coordenadas es el mismo entre rutas. Las 21 coinciden exactamente con uniones de los cuatro transcritos cacheados de UNC13A. Hay 42 filas en la tabla porque cada unión figura una vez por ruta; no son 42 uniones distintas. El soporte de eventos visibles suma 66/67, sin equivaler a ese número de grupos únicos. El soporte máximo por unión visible es seis. No se clasifican las 10/12 filas que faltan.

## Interpretación y decisión

La comparación disponible apoya una asignación coherente a UNC13A y la geometría exacta de las uniones observadas; no revela un desplazamiento general de coordenadas. La escasez se mantiene en los objetivos y el filtro regional sólo descarta uno de los 116 grupos candidatos. No prueba ausencia de eventos crípticos, expresión diferencial, identidad funcional ni efecto de TDP-43.

No ampliar automáticamente el análisis a los 12.709.444 pares del control ni iniciar TDP. Con un único grupo en el primer millón no hay una estimación estable de profundidad esperable al completar el archivo. El prefijo es ordinal y no fue seleccionado aleatoriamente; una extrapolación lineal no justifica garantizar que se alcance el umbral de 20. Primero completar la clasificación de las filas restantes y revisar si hay uniones no contenidas en esta anotación cacheada. Si continúa el soporte escaso, cerrar el piloto como insuficiente y evaluar otra estrategia/dataset con criterio prospectivo, sin gastar nuevas descargas por inercia.

## Validación y siguiente paso

Ocho pruebas locales correctas sin omisiones: manejo explícito de resumen incompleto, deduplicación sin sumar dos veces, conflicto de cuentas, desplazamiento de una base, hebra errónea, referencia distinta, tamaño/ventana/cuentas inválidas y formato de inventario completo de fixture. Esta última prueba no completa las filas humanas que faltan. Sin nuevo alineamiento humano ni descarga. Detalles en `validation.json`.

Para terminar, el usuario debe adjuntar el archivo pequeño `audit-seal.json` ya existente en la raíz `-locus-audit-01-guard-02`. No hace falta volver a ejecutar ningún análisis. El próximo contraste reutilizará el mismo script sobre ese inventario comunicado completo; seguirá sin ser una comprobación independiente de archivos WSL. PR 36 abierta, sin fusionar.
