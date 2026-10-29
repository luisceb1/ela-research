# Estado del proyecto ELA

Fecha de arranque del repositorio: 2026-10-29.

## Pregunta central
¿Qué cambios de splicing asociados a pérdida nuclear de TDP-43 se observan de manera consistente en datasets publicados, y qué experimento distinguiría restauración de ARN de recuperación funcional neuronal?

## Datasets prioritarios
- **GSE310723:** modelos neuronales i3N; secuenciación Iso-Seq. Datos de condiciones experimentales; comprobar metadatos y diseño antes de comparar.
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310723
- **GSE315972:** tejido cerebral humano Iso-Seq. Confirmar los GSM, categorías y replicación biológica antes de inferir.
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE315972

## Restricciones
- El diseño previamente revisado de GSE310723 comprende una sola muestra por condición: **no** estimar significación diferencial como si hubiera réplicas biológicas.
- No asumir equivalencia entre neuronas cultivadas y tejido cerebral.
- Auditar IDs de transcritos contra las anotaciones GTF, así como el significado de uniqueCounts frente a counts/CPM.
- Evitar afirmaciones clínicas.

## Hito cero
No hay resultados nuevos verificados por este repositorio. El primer workflow únicamente recopila metadatos PubMed y realiza un inventario estructural de tablas públicas.