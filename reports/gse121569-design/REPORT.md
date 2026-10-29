# GSE121569: bibliotecas, lotes y diferenciaciones

29/10/2026. Evidencia: auditoría técnica de fuentes primarias; mapa publicado reproducido, sin nueva inferencia biológica.

## Evidencia

Las 18 descripciones GSM del SOFT oficial enlazan de forma única con los alias de cultivo. Las 12 columnas `countData.*` del archivo DEXSeq enlazan exactamente con seis `siScr` y seis `siTDP43`. Las otras seis bibliotecas corresponden a tres `siRED` y tres `NoTx`. No son muestras de pacientes.

La figura suplementaria 3a de Klim et al. muestra explícitamente los 18 alias y su lote. Se inspeccionó visualmente `word/media/image3.jpg` del suplemento 1 y se transcribieron sus etiquetas, conservando hash del miembro y del DOCX. No se dedujeron los lotes de un dendrograma, del orden de columnas, del número `rep` o de la fecha. El manifiesto está en `research/references/gse121569_published_batches.json`; el enlace ejecutado está en `dexseq_column_map.tsv`.

| Grupo de cultivo | Batch 1 | Batch 2 | Total |
|---|---:|---:|---:|
| Scramble | 2 | 4 | 6 |
| TDP43 siRNA | 2 | 4 | 6 |
| Fluorescent siRNA | 1 | 2 | 3 |
| Sin transfección | 1 | 2 | 3 |

La leyenda de la figura 1b confirma dos experimentos independientes de diferenciación de MN y transfección de siRNA. Los métodos los denominan Exp 1 / Exp 2. Se conserva la agrupación publicada Batch 1 / Batch 2; los identificadores de experimento/diferenciación en el TSV significan exclusivamente esa agrupación publicada. No se reconstruyeron pozos ni subcultivos independientes.

Las dos fechas GEO (campo `date`, sin semántica experimental definida) concuerdan con los lotes de la figura: 2013-01-10 y 2013-06-10. Esto es comprobación cruzada, no la prueba inicial de independencia. `NoTx_2` y `siRED_2` pertenecen a Batch 2, mientras que `siScr_2` y `siTDP43_2` pertenecen a Batch 1: el sufijo 2 no asigna un lote universal.

Los métodos describen 15 bibliotecas para el contraste de expresión: nueve controles (siRED y dos siSCR) y seis KD, de dos experimentos. La figura suplementaria muestra también las tres NoTx, sumando 18. Las columnas de cuentas exportadas en `dexseq-all` contienen solo 12 bibliotecas siScr/siTDP43: no se transfiere automáticamente el tamaño de 15 del contraste de expresión a esta matriz. Tampoco se ha reconstruido la fórmula exacta del ajuste DEXSeq que produjo los p ajustados publicados.

## Interpretación

Se ha resuelto el mapa de las 12 columnas a GSM y lote publicado. Hay dos experimentos independientes publicados, no seis diferenciaciones por condición ni doce en total. Las dos condiciones están presentes en ambos lotes (2/2 y 4/4); condición y lote no están completamente confundidos. Esto no demuestra independencia de todas las bibliotecas dentro de lote.

## Limitaciones y bloqueo del refit

Los métodos distinguen dos reactivos scramble y dos reactivos TDP43, pero los alias depositados no explicitan qué reactivo y qué pozo originó cada biblioteca. No asignar `siTDP43_1` a reactivo 1 por semejanza de nombre. No conocemos el modelo original, la estructura de subréplicas ni los identificadores de pozo. No se calculan nuevos p-valores, grados de libertad o intervalos inferenciales. Los p ajustados extraídos antes siguen siendo resultados de autores, no una reestimación propia.

Con dos diferenciaciones, una futura sensibilidad por lote será descriptiva y no convertirá subréplicas en diferenciaciones. No se interpreta uso de fragmentos como PSI, proteína o rescate funcional. El mapa procede de una transcripción visual revisable, no de un archivo original de diseño legible por máquina.

## Controles y reproducción

Python stdlib. Enlace por alias exacto, unicidad GSM/alias, validación del modelo HUES3 y condición, rechazo de metadatos ausentes, columnas no enlazadas y manifiestos incompletos. Once tests nuevos; suite de rama: 135 tests correctos (105 main + 30 de issue14). CI de esta entrega se verifica por separado después del commit.

```bash
python scripts/audit_gse121569_design.py \
  --soft data/cache/gse121569/family.soft.gz \
  --dexseq ../ela-consolidation/data/cache/issue14/GSE121569_dexseq-all.csv.gz \
  --published-batches research/references/gse121569_published_batches.json \
  --primary-cache data/cache/gse121569 \
  --out reports/gse121569-design
python -m unittest discover -s tests -v
```

La ruta DEXSeq es solo una ubicación de caché de esta ejecución; el archivo puede ubicarse en cualquier ruta y se identifica por el hash de `sources.json`. Fuentes grandes y figuras no se redistribuyen. `culture_libraries.tsv` contiene únicamente metadatos técnicos de cultivos públicos, sin filas clínicas, datos alélicos o contactos. `sources.json`, `errors.json` y `run.json` fijan procedencia e incidencias.

## Siguiente acción verificable

Antes de un refit, auditar integridad de las cuentas `countData` y del archivo `combined.dexseq` (esquema, enlace de fragmentos, ceros, duplicados y concordancia), y buscar en recursos públicos un diseño con reactivo/pozo y fórmula original. Si no aparece, mantener bloqueado el refit inferencial y limitar la sensibilidad por lote a descriptivos. No contactar autores sin autorización. Issue #14 permanece parcial; sin merge automático.

Fuentes primarias: GEO GSE121569, Klim et al. 2019 DOI 10.1038/s41593-018-0300-4 (manuscrito PMC7153761, Fig.1b y métodos RNA), suplemento 1 Fig.S3a. Los hashes y URLs exactos están en `sources.json`.
