# Fuentes públicas de cuentas de uniones — 30/10/2026

## Evidencia comprobada

**Hay un archivo público procesable con cuentas de uniones concretas, pero todavía no hay un nuevo contraste externo listo para analizar.** Se verificó el CSV de cultivos `data/kd_experiments_relative_rna_and_unc13a_cryptic_junction_counts.csv` del repositorio de Brown et al. (2022), fijado al commit `e05e8723e3d18e64c6c559db18de423282511c91` y blob `c8715e2b6452f0e32bf56bd315171213950d0dff`.

Python verifica 42 registros únicos, 26 columnas y 294 celdas enteras no negativas en siete campos: dos de STMN2 (anotada/críptica) y cinco de UNC13A (anotada/cuatro clases de unión críptica). Se comprueba el esquema; **no se calculan efectos, PSI o significación**. Se exportan solo los cinco agregados siguientes, sin alias individuales, sufijos genotípicos o valores de expresión.

| Grupo literal de la tabla, sin sufijo genotípico | Control | KD | Procedencia y decisión |
|---|---:|---:|---|
| Appocher |3|3|El artículo remite al conjunto publicado GSE97262; pendiente mapa fila→run e identidad corregida|
| Klim iPSC MN |11|6|Reutiliza GSE121569; no es réplica externa de nuestra fase #14. Selección de 17 registros por reconciliar|
| SH-SY5Y |3|3|Disponibilidad de estudio PRJEB42763; no mapa de unidades comprobado|
| SK-N-DZ, etiqueta antigua |3|3|Disponibilidad de estudio PRJEB42763; identidad de línea y mapa de unidades pendientes|
| iPSC Neurons |4|3|Disponibilidad de estudio PRJEB42763; mapa de biblioteca/run/diferenciación pendiente|

**Estas cifras son filas técnicas, no réplicas biológicas independientes.** Tampoco se equiparan los 17 registros Klim con las 12 columnas DEXSeq, el contraste publicado de 15 bibliotecas o las 18 depositadas. No se ha explicado aquí esa selección; queda como bloqueo explícito.

## Corrección editorial que afecta al siguiente análisis

Brown et al. (2024), DOI10.1038/s41586-024-07577-9, corrigen la identidad de una línea antes llamada SK-N-DZ a SK-N-BE(2). Se inspeccionó el texto primario indexado por scite, no solo sus metadatos. Evidencia breve: “This line has since been conclusively identified as SK-N-BE(2).” El artículo PMC actualizado usa etiquetas corregidas, pero el CSV conserva las antiguas. **No se renombra automáticamente ninguna fila ni se supone que ambas categorías antiguas corresponden a las mismas unidades.** La correspondencia debe documentarse desde fuentes técnicas.

La página editorial directa redirigió a autenticación inaccesible y la página PMC del aviso mostró recaptcha. Eso no bloqueó recuperar su texto primario vía scite ni leer la disponibilidad del original actualizado. No se declara comprobación editorial universal. La consulta de scite de accesiones devolvió autorías resaltadas inconsistentes: se mantuvieron los autores del registro bibliográfico sin término de búsqueda; los resaltados no se trasladaron a las referencias.

## Qué aporta cada archivo y qué no

- El CSV es una tabla de cuentas por etiquetas de unión. **No contiene coordenadas de cada unión** ni acredita por sí solo ensamblaje o unidad independiente.
- `unc13a_cryptic_exons.bed`, blob `da9b1de024f7bb045417d1ffcc20fa634a3eb7b6`, contiene dos intervalos de exón, no los extremos de las uniones. Las longitudes y la convención requieren revisión: no asumir que toda extensión `.bed` usa el mismo esquema.
- El artículo identifica Supplementary Table 6 como las coordenadas hg38 de uniones usadas para los índices. Es el siguiente objeto molecular concreto que hay que contrastar, no una licencia para transferir coordenadas por semejanza.
- El pipeline público `frattalab/bedops_parse_star_junctions`, commit `987893efd84a5c5c20ddac9bf33e137c1c6b33ae`, documenta una salida de siete campos (cromosoma/extremos/archivo/cuentas/hebra/etiqueta). Se leyeron README y conversor, **no se ejecutó código externo**. El conversor usa el campo de lecturas únicas de STAR y transforma los extremos; un ejemplo comentado no coincide con la operación ejecutable del extremo final. Se registra como motivo para contrastar convención con código, sin atribuir aún el CSV a una ejecución concreta.
- El BED amplio `kds_stmn2_and_unc13aaggregated.clean.annotated.bed` mezcla fuentes de mayor alcance. Tras el sondeo inicial se retiró de la caché de este bloque; no se exportan sus filas ni se utiliza para calcular nada. Los archivos clínicos, de covariables y genotipos identificados por sus nombres no se abrieron. La fuente Liu/Fratta ya auditada sigue siendo reutilización, no un nuevo análisis.

## Resultado de la predicción, QC y límites

La predicción prefijada exigía una fuente nueva con archivo recuperable, evento y unidades enlazados. **No se cumple todavía**: el CSV es accesible y sus cuentas son procesables, pero los cuatro grupos candidatos carecen del mapa completo que necesitamos; el quinto reutiliza GSE121569. Esto no demuestra ausencia universal de datos ni es un resultado biológico negativo.

Validador reproducible en `scripts/inventory_junction_sources.py`, tabla curada en `research/references/junction_source_inventory_20261030.json`. Python3.12.14, stdlib, sin aleatoriedad. Se verifican Git blob y SHA-256 del CSV, dimensiones, columnas, alias únicos, grupos/condiciones permitidos y cuentas enteras. Hashes y versiones en run.json. Las proyecciones curadas de fuentes no equivalen al hash de bytes de los artículos completos; sus URL, DOI y localizadores quedan explícitos.

Ocho tests nuevos cubren falta de inspección/coordenadas/unidades/identidad, reutilización convertida en independencia, clínica prohibida, eliminación de sufijos genotípicos, cuentas negativas/fraccionarias/no finitas, grupos desconocidos y alias duplicados. **175 tests locales correctos (167 previos + 8), compileall correcto.** Son tests del contrato de evidencia y software, no experimentos.

```bash
python -m scripts.inventory_junction_sources \
 --source data/cache/junction-source-inventory/kd_experiments_relative_rna_and_unc13a_cryptic_junction_counts.csv \
 --manifest research/references/junction_source_inventory_20261030.json \
 --out reports/junction-source-inventory
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

## Siguiente prueba discriminante

Contrastar **Supplementary Table 6 (solo coordenadas moleculares)** con etiquetas y convención del pipeline, y enlazar las bibliotecas de un único grupo candidato de PRJEB42763 con sus unidades técnicas. Empezar por iPSC Neurons o SH-SY5Y, manteniendo fuera las etiquetas de línea corregidas hasta resolverlas. Si no hay enlace verificable, no estimar efectos ni llamar réplica externa a las filas. DEXSeq permanece cerrado como evidencia indirecta de esos CE; no se repite Fratta ni se suman cohortes reutilizadas.

Entrega en el mismo PR29, sin merge/cierre de issue, comunicación externa, coste, laboratorio o datos clínicos personales nuevos. El resumen semanal existente no se duplica.

## Referencias

- Brown, A.-L., Wilkins, O. G., Keuss, M. J., et al. (2022). *TDP-43 loss and ALS-risk SNPs drive mis-splicing and depletion of UNC13A*. Nature,603,131–137. https://doi.org/10.1038/s41586-022-04436-3 . Métodos, disponibilidad y leyenda de Supplementary Table6; PMC8891020 actualizado.
- Brown, A.-L., Wilkins, O. G., Keuss, M. J., et al. (2024). *Author Correction: TDP-43 loss and ALS-risk SNPs drive mis-splicing and depletion of UNC13A*. Nature,631,E7. https://doi.org/10.1038/s41586-024-07577-9 . Texto primario recuperado por scite; identidad de línea.
- Repositorios primarios de autores: https://github.com/frattalab/unc13a_cryptic_splicing y https://github.com/frattalab/bedops_parse_star_junctions . Commits y blobs fijados arriba y en manifiesto.
