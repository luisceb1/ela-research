# Cuentas asignadas y sensibilidad del denominador — 30/10/2026

## Evidencia ejecutada

Se localizaron ambos originales en la caché disponible de este entorno. Sus SHA-256 coinciden con los GEO fijados en la auditoría anterior: `dexseq-all` daaf355a…814f4 y `combined.dexseq` ded98175…fea6e (completos en run.json). **No hubo nueva descarga.** Esto desbloquea la falta de matriz del ciclo anterior sin invalidar el timeout que entonces se registró.

Se procesaron todos los102fragmentos objetivo, no solo los cuatro destacados:408agregados de cuentas por condición/lote y612comparaciones de medias (102×2lotes×3denominadores). Se reproducen las204medias/cambios anteriores dentro de tolerancia. La cobertura aquí significa **cuentas asignadas al bin**, no cobertura por nucleótido ni lecturas que crucen uniones.

| Fragmento destacado previamente | Mínimo en las12bibliotecas | Bibliotecas con cero | Fracción dentro del gen: signo entre lotes | Cociente frente a otros bins | Normalización por biblioteca |
|---|---:|---:|---|---|---|
| STMN2 E009 |908|0|Opuesto|Opuesto|Mismo, ambos descensos|
| UNC13A E026 |38|0|Opuesto|Opuesto|Opuesto|
| UNC13A E030 |40|0|Opuesto|Opuesto|Opuesto|
| UNC13A E054 |29|0|Opuesto|Opuesto|Mismo, ambos descensos|

H1prefijada (los cuatro con>=10cuentas en cada biblioteca) no se refuta. El umbral10es técnico/arbitrario: no acredita precisión, calidad universal o independencia. H2prefijada (discordancia de los cuatro con los tres denominadores) **se refuta** paraE009/E054; persiste descriptivamente paraUNC13AE026/E030. No demuestra mecanismo, ruido ni causalidad.

Con normalización por biblioteca, E026cambia−1.145731/+0.092082 yE030−0.941268/+0.153560cuentas por millón de cuentas asignadas a bins (Batch1/2). Los cambios positivos del segundo lote son pequeños en esta escala. No transferir0.1ppdel análisis previo a esta unidad ni declarar efectos robustos por conservar solo el signo.

## Métodos y alcance de cada denominador

1. `within_gene_pp`:100×cuentas bin/suma de bins del mismo groupIDpor biblioteca, luego mediaKD−mediaScrdentro del lote. Reproduce el descriptivo previo.
2. `other_bins_ratio`:bin/(suma génica−bin) por biblioteca, después diferencia de medias. Sin pseudocuentas. Un denominador cero devuelve no evaluable, no infinito ni cero inventado. No es una réplica metodológica independiente de1: es una transformación relacionada y no lineal.
3. `assigned_bin_CPM`:1e6×bin/suma de todas las cuentas asignadas a bins de la biblioteca original. Excluye las cinco filas técnicas de resumen. No equivale al número de fragmentos secuenciados únicos: los bins pueden compartir soporte. Mide abundancia relativa a biblioteca, mientras1/2miden reparto dentro del gen. **El cambio de dirección entre estas preguntas no invalida por sí solo DEXSeq.**

Cada condición se promedia sin ponderar sus bibliotecas dentro deBatch1(2/2)yBatch2(4/4). No se asignan pozos/reactivos ni se estiman grados de libertad. Las bibliotecas no se convierten en diferenciaciones. No p-valores, intervalos inferenciales, ajusteDEXSeqoPSI.

| Gen | Discordancias fracción génica | Discordancias otros bins | Discordancias normalización biblioteca |
|---|---:|---:|---:|
| STMN2 |2/10|2/10|0/10|
| UNC13A |26/62|27/62|12/62|
| TARDBP |10/30|10/30|1/30|

Se exportan todas las clasificaciones, incluidas las no destacadas. La diferencia26→27deUNC13Aes compatible con que transformar antes de promediar no conserve necesariamente la clasificación entre medias; no se omite. No hubo denominadores no evaluables o cambios exactamente cero en los datos reales bajo estas reglas.

## QC, controles y reproducción

Plan previo:research/plans/2026-10-30-dexseq-coverage.md. Python3.12.14,stdlib,sin aleatoriedad. Hashes de fuentes/mapa/tabla previa/script, parámetros y versiones enrun.json; salidas con hashes enoutput_hashes.json. Verificados585869bins únicos al sumar denominadores originales, cinco resúmenes separados, cuentas enteras no negativas,12columnas únicas, cruce2/2y4/4,catálogo10/62/30,ausencia de duplicados objetivos y concordancia de204agregados previos. No se repitió la comparación completa7millones de cuentas: se reutiliza su auditoría histórica.

Siete pruebas nuevas: invariancia al escalado de biblioteca; cero observado sin pseudocuenta; denominadorotrosbinscero; jerarquía/tipos/no finitos; agregación y permutación; vectores inválidos; diseño duplicado/incompleto. **160tests locales correctos (153previos+7),compileallcorrecto.** Log conservado. CI del nuevo commit se consulta tras guardarlo, sin trasladar éxito de un commit anterior.

```bash
python -m scripts.audit_dexseq_coverage \
  --dexseq ../ela-consolidation/data/cache/issue14/GSE121569_dexseq-all.csv.gz \
  --combined data/cache/dexseq-qc/combined.txt.gz \
  --mapping reports/gse121569-design/dexseq_column_map.tsv \
  --previous reports/dexseq-batch-sensitivity/fragment_batch_aggregates.tsv \
  --out reports/dexseq-coverage
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

Rutas de caché sustituibles, hashes obligatorios. Solo agregados técnicos exportados; sin cuentas por biblioteca, datos clínicos, genéticos personales, nuevas cohortes o redistribución de originales.

## Interpretación, límites y siguiente prueba

El patrón de los cuatro destacados no se explica por ceros observados o por estar todos por debajo del umbral prefijado10; **eso no descarta variabilidad de conteos ni influencia de una biblioteca**. Dos conservan inversión con todos los denominadores, pero su efecto pequeño, dependencia de normalización, diseño interno y reactivos/pozos desconocidos impiden elevarlos a hallazgo biológico. No se identifican automáticamente con el exón crípticoUNC13A, un transcripto completo o proteína.

Siguiente tarea segura: verificar de forma independiente coordenadas y ensamblaje del exón crípticoSTMN2/UNC13Aantes de usar estos bins como evidencia estructural. Si no puede enlazarse un bin con el evento, conservarlo como bin anotado y no como medida deCE. Solo después valorar una sensibilidad descriptiva a exclusión de bibliotecas, sin confundirla con réplica externa o corregir el diseño desconocido. El refit permanece bloqueado por pozo/reactivo/fórmula; issue14parcial.

MismoPR29sobre main8dfa7ce7;PR28independiente/no incorporado. El resumen semanal existente no se duplica. Sin merge/cierre/contactos/gastos/laboratorio/publicación externa.

## Fuentes y evidencia

GEO,GSE121569: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE121569 . Archivos originales públicos de cultivo:`GSE121569_dexseq-all.csv.gz`y`GSE121569_combined.dexseq.txt.gz`, https://ftp.ncbi.nlm.nih.gov/geo/series/GSE121nnn/GSE121569/suppl/ . Atribución:Klimet al.(2019). Licencia separada de matrices no verificada; no se redistribuyen. Evidencia de diseño ya auditada enreports/gse121569-design; métodos/limitaciones de las fuentes enreports/dexseq-magnitude. Este ciclo es análisis computacional descriptivo del mismo estudio, no nueva validación funcional.
