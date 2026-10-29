# Diccionario

- `paper_evidence.json`: DOI, referencia de Figura 5, ensamblaje y límites de unión extraídos del XML de la fuente primaria. Hebra ausente del pie = null. No contiene tablas clínicas individuales.
- `event_matches.tsv`: coincidencias exactas de unión del catálogo anterior; identidad de unión distinta de transcrito completo/poliA, que permanecen no establecidos.
- `target_full_length_support.tsv`: valores depositados de counts, uniqueCounts, fullLengthCounts y CPM por biblioteca/transcrito diana. full/total y unique/total son cuotas de las estimaciones, no PSI ni porcentaje de moléculas independientes.
- `depth_and_cpm.tsv`: sumas por biblioteca; denominador CPM implícito de las sumas redondeadas y su diferencia respecto a counts asignados; número de celdas fraccionarias, GCD cuando toda la columna es entera y discordancia full/unique. El exceso de denominador no es un conteo directo de incompatibles observado en el objeto original.
- `deposited_cpm_contrasts.tsv`: contrastes aritméticos de cultivo basados en CPM original; control cero = NA, sin pseudocuentas ni significación.
- `quant_violations.tsv`: casos que superan counts con tolerancia absoluta 1e-4; solo encabezado = ningún caso en una ejecución completa. No se exige fullLength <= unique ni lo contrario.
- `sources.json`: originales/proyecciones nuevos, URL, fecha, bytes, hashes y commit/blob cuando corresponda. Entradas anteriores en los manifiestos de auditoría/mapeo. Código externo completo y XML íntegro no se publican en este repositorio.
- `summary.json` y `run.json`: alcance de atribución, límites, metadatos y ejecución; el testigo algebraico está explícitamente separado de ejecutar R/bambu. `EXECUTION_NOTES.md` retiene fallos de acceso y bloqueo de trazabilidad. `tests.txt` son pruebas de software offline.
