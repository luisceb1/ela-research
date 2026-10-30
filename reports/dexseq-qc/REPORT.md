# Integridad y concordancia DEXSeq — 30/10/2026

## Evidencia

Se leyeron íntegros los dos archivos GEO públicos de cultivos HUES3. `combined.dexseq` contiene 585869 fragmentos únicos, 18 bibliotecas y cinco filas de resumen técnico separadas. La tabla `dexseq-all` contiene 589903 filas de resultados, pero solo 585869 fragmentos únicos: 4034 filas adicionales tienen diferencias exclusivamente en los campos de anotación definidos por el script. No hay conflictos entre sus vectores de cuentas ni entre sus campos no anotativos.

Las 12 columnas del contraste enlazan por alias, independientemente del orden. Se compararon 7030428 celdas de fragmentos únicos: cero discordancias, cero fragmentos sin correspondencia y cero discordancias fragment/groupID/featureID. Todas las cuentas de ambos archivos son literales enteros no negativos. Los grupos multigénicos separados por + se conservan íntegros y en su orden: no se fuerza un gen único ni se ordenan sus componentes.

La tabla de resultados contiene 2577055 celdas cero y 113300 filas con las doce cuentas cero, contando sus repeticiones de anotación. Estos valores no son denominadores de fragmentos únicos. Los ceros son cuentas publicadas, no prueba de ausencia molecular. Las cuentas de resumen técnico no son fragmentos, profundidad molecular única ni bases para inferir calidad biológica por sí solas.

## Interpretación y límites

Hay concordancia técnica exacta entre dos proyecciones del mismo estudio, no validación independiente. Sumar filas por símbolo sin resolver las repeticiones de anotación puede duplicar cuentas. El resultado no cambia los descriptivos previos de los tres genes objetivo ni reestima los p ajustados de autores. No se ajustó DEXSeq, calculó PSI ni infirió proteína o rescate funcional. Persisten dos diferenciaciones publicadas y la falta de mapa de reactivos/pozos y fórmula original.

## Reproducción y controles

`scripts/audit_dexseq_counts.py`, Python stdlib, SHA256 en sources.json. Ejecutado con:

```bash
python scripts/audit_dexseq_counts.py --combined data/cache/dexseq-qc/combined.txt.gz --dexseq ../ela-consolidation/data/cache/issue14/GSE121569_dexseq-all.csv.gz --out reports/dexseq-qc
python -m unittest discover -s tests -v
```

Las rutas son ubicaciones de caché; los archivos se identifican por hash, no por ruta. No se redistribuyen matrices originales. Ocho tests nuevos, incluido enlace completo con columnas reordenadas, anotación repetida y cuenta conflictiva: 143 tests de rama correctos. Los tests usan datos sintéticos pequeños para controles de software; las cifras de arriba proceden de los archivos públicos completos. Fuentes, errores y ejecución registrados. Sin filas clínicas o genéticas ni contacto externo.

## Siguiente acción

Comprobar si los 102 fragmentos objetivo previos incluyen repeticiones de anotación y crear una proyección única por fragmento con sensibilidad descriptiva por lote. Preservar p ajustados publicados sin recalcularlos ni considerar bibliotecas como diferenciaciones. Si no aparece el diseño público de reactivo/pozo, mantener bloqueado el refit inferencial y avanzar con la siguiente auditoría verificable. Issue14 permanece abierta; PR29 pendiente de revisión, sin merge.
