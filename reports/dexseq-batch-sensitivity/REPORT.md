# Sensibilidad descriptiva por lote — 30/10/2026

## Evidencia

Los 102 fragmentos objetivo previos son únicos: 10 STMN2,62 UNC13A,30 TARDBP. Para cada biblioteca se dividieron las cuentas de cada fragmento por la suma de cuentas de los fragmentos disponibles del mismo grupo génico. Se comparó después la media KD menos scramble dentro de cada lote publicado (Batch1:2/2 bibliotecas; Batch2:4/4). Denominadores positivos en todos los casos.

| Gen | Fragmentos | Mismo signo en ambos lotes | Signo opuesto |
|---|---:|---:|---:|
| STMN2 | 10 | 8 | 2 |
| UNC13A | 62 | 36 | 26 |
| TARDBP | 30 | 20 | 10 |

No hubo cambios exactamente cero. Los 204 registros de `fragment_batch_aggregates.tsv` muestran medias y diferencias en puntos porcentuales por fragmento y lote. No contienen cuentas por biblioteca ni datos clínicos. Procedencia: archivo GEO fijado y mapa técnico previamente auditado, hashes en provenance.json.

## Interpretación

La consistencia de dirección es parcial. Estas cifras no prueban ni refutan por sí mismas los resultados ajustados publicados. La comparación es composicional: una subida relativa de un fragmento puede deberse a la bajada de otro. Los bins difieren en longitud, pueden compartir transcritos y no representan moléculas independientes. La fracción de cuentas dentro de grupo no es PSI, abundancia génica total, proporción de isoformas, proteína o función. No se interpreta un aumento relativo como rescate.

## Limitaciones

Se comparan signos exactos, sin umbral mínimo de efecto; cambios diminutos pueden invertir el signo sin relevancia biológica. No hay tests nuevos, intervalos de confianza o selección por significación. Los fragmentos del mismo gen están acoplados por el denominador y no son réplicas independientes. Las bibliotecas se promedian dentro de lote, sin convertirlas en diferenciaciones. Dos lotes del mismo estudio no son validación externa. Reactivo, pozo y fórmula original siguen pendientes. No se combinan estos descriptivos con cuentas nucleares GSE126542.

## Reproducción

Python stdlib, código `scripts/describe_dexseq_batches.py`:

```bash
python -m scripts.describe_dexseq_batches --source <GSE121569_dexseq-all.csv.gz> --mapping reports/gse121569-design/dexseq_column_map.tsv --out reports/dexseq-batch-sensitivity
python -m unittest discover -s tests -v
```

Cuatro tests nuevos: invariancia al escalado uniforme por biblioteca, cierre de fracciones, denominador cero y clasificación de signos. Suite de rama:147 tests correctos. Ejecución completa sin errores. La corrección del software no valida biología. No refit, contactos, costes o merge.

## Siguiente acción

Examinar magnitudes y cobertura de los fragmentos con cambio de signo y su relación con los bins/crípticos publicados antes de priorizarlos. Una sensibilidad de denominador debe distinguir reparto de cuentas de cambios absolutos. Mantener bloqueado el refit inferencial mientras no se resuelva el diseño de reactivos/pozos. Issue14 permanece abierta.
