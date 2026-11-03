# STMN2: PPAU reproducida desde TPM — 01/11/2026

## Evidencia

**12 de 12 bibliotecas concordantes**, ninguna rechazada o indeterminada. La diferencia absoluta máxima entre PPAU calculada y publicada es **4,440892098500626e-16**, con tolerancia prospectiva **1e-6** en unidades de proporción. No se ajustaron fórmula, escala, tolerancia o selección de bibliotecas después de observar los resultados.

Se aplicó el plan research/plans/2026-11-01-stmn2-papa-tpm-reproduction.md, fijado en fd74d931dbf58673983366c19678bbc213dce45c antes de recuperar la tabla TPM. execution_plan.json fija el miembro y las condiciones de ejecución. Numerador: TPM del grupo ENSG00000104435.14_1. Denominador: suma de TPM de todos los grupos con gene_id exacto ENSG00000104435.14 en la matriz completa, sin usar la matriz génica GEO como sustituto. Hay dos grupos STMN2 en ambas matrices; cada matriz tiene 43.630 filas.

La tabla per_library_comparison.tsv conserva GSM, biblioteca, condición, grupos, TPM numerador/denominador, proporción calculada, PPAU autores, diferencia y aceptación. comparison_table.md presenta los mismos datos por biblioteca. No se calcularon medias por condición, p-valores o intervalos inferenciales.

## Interpretación

Se reproduce correctamente la **aritmética de uso relativo de grupos de exones finales** del modelo PAPA para STMN2. Es la definición TPM/suma(TPM) del código primario de autores fijado en el informe anterior. Esto permite utilizar esta tabla descriptivamente sin confundirla con una proporción de cuentas ajustadas por longitud.

El contraste anterior counts/suma(counts) frente a PPAU **permanece rechazado en 12 de 12 bibliotecas**. Sus resultados y tabla conservaron sus hashes originales; no se reejecutó ni se sobrescribió. El éxito de este nuevo contraste no altera retrospectivamente el anterior. El código anterior solo se reutilizó como biblioteca para parsear matrices y aplicar los mismos controles de denominador/tolerancia, sin ejecutar su main.

La concordancia usa insumos y resultados de los mismos autores: no añade una réplica biológica independiente. No valida el algoritmo de cuantificación desde lecturas, los límites moleculares de cada modelo, un efecto causal nuevo, rescate neuronal o beneficio clínico. Tampoco convierte la PPAU en PSI de uniones. Se mantienen la línea única WTC11, intervención anterior a diferenciación, mapa de lotes/unidades no reconstruido y falta de medición comparable del evento UNC13A.

## Recuperación y reproducibilidad

Se recuperó únicamente el miembro summarised_pas_quantification.tpm.tsv del directorio Humphrey en Zenodo **15538003**, ya localizado en el índice remoto: 1.694.976 bytes comprimidos, 4.937.870 descomprimidos. Respuesta HTTP206 y Content-Range comprobados; longitud, formato, descompresión limitada y CRC verificados. Tráfico: 1.826.076 bytes. SHA256 TPM: 1037570e97c8ad4536f092a7bfb2b83c9710e8b402d04acdd6e3f0d69ba0466b. Recibo completo en retrieval.json.

Se reutilizaron, tras verificar SHA, PPAU c4828ee5edd25a8c6c29719366735df268a669d8d5ba8d075dd015bdccd5ac42 y mapa de muestras 818b8f6553a3ea1b44e0c1cf511c5dec1fcc35f7ccd68e2d8b45af6c46087573. No se descargó el ZIP íntegro, FASTQ, tablas post mortem o datos clínicos; no se afirma haber verificado el MD5 del ZIP completo.

Dos ejecuciones offline del código final produjeron result.json y per_library_comparison.tsv idénticos por bytes. repeat_verification.json registra también la conservación del contraste fallido anterior. Pasan 23 tests locales de los tres módulos añadidos en esta PR, incluyendo tres controles nuevos de semántica TPM, diferencias entre mediciones y rechazo de entradas alteradas. Compileall correcto en Python3.12.14. La CI completa se comprobará sobre la nueva cabeza de la PR; los tests no añaden réplicas biológicas.

```bash
python scripts/fetch_stmn2_papa_tpm.py
python scripts/reproduce_stmn2_papa_tpm.py
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

El fetcher rechaza sobrescribir una caché existente. Para repetir el cálculo se reutilizan fuentes verificadas, sin repetir la descarga. No hubo fallos de acceso o ejecución en esta fase; el resultado negativo anterior se conserva como evidencia metodológica.

## Siguiente prueba discriminante

Esta reproducción está cerrada; no repetirla como nueva tarea. El único siguiente paso propuesto es comprobar una fuente concreta de procesados de **uniones UNC13A para las mismas doce bibliotecas**, antes de plantear una descarga de crudos o una comparación entre genes. Plan prospectivo, aún no ejecutado: research/plans/2026-11-01-gse296714-unc13a-processed-gate.md.

La puerta exige identidad de bibliotecas, ensamblaje/hebra/coordenadas y definición molecular del evento y su comparador. Se limita a cultivos y recursos pequeños. Su resultado podrá ser una fuente aceptada para QC por biblioteca o un bloqueo preciso. No se presume que exista, ni se abre inferencia biológica antes de resolver las unidades experimentales.

Fuentes primarias: https://doi.org/10.5281/zenodo.15538003 y definición de PPAU en https://github.com/frattalab/PAPA/blob/d2ed20d217d9e3e397fa92dbcf9dc72a000f37b8/scripts/tx_to_polya_quant.R. Enlaces técnicos y versiones de GEO/ENA constan en la auditoría GSE296714 anterior; no se presentan como fuentes nuevas.
