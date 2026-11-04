# Plan previo — reproducción molecular Fratta Dox

Fecha: 04/11/2026. Encargo expreso de Luis: avanzar con los repositorios públicos de Fratta mientras se espera K26. Alcance adicional acotado, independiente de #37/#44 y PR #46/#47: un CSV de medidas moleculares y un bloque R, sin repetir la auditoría de uniones ni STMN2/PPAU.

## Pregunta y criterio de éxito

¿Se pueden reconstruir las medias y los errores estándar de fila del bloque «Dox curves and protein/RNA levels» a partir de Protein_RNA_Corr_3.csv? ¿El orden de renombrado/unión conserva los errores de las series de ARN correctamente procesado?

La inspección previa del código muestra que agrega Value por Treatment/Gene/Line_Group/Color_Group, calcula sd/sqrt(n), elimina 13A-RNA, cambia Correct_RNA a RNA y hace un left_join sin claves explícitas. Predicción falsable: si esas claves dejan de coincidir, aparecerán errores ausentes exclusivamente en la serie renombrada; unir antes de renombrar los conservará sin cambiar medias. Si las claves coinciden, registrar que la sospecha no se reproduce. No afirmar daño a figuras publicadas sin cotejar su procedencia y versión.

## Fuentes fijadas antes de calcular

Repositorio frattalab/unc13a_cryptic_splicing, commit e05e8723e3d18e64c6c559db18de423282511c91:
- data/Protein_RNA_Corr_3.csv, blob 490ccce919f32f0b74ffd4a756fa721610877f48, tamaño del índice 4738 bytes.
- paper_figures.Rmd, blob 1534a7312bcee102fae9a60bb450ddd37da5c96c, 148855 bytes; bloque líneas 3779–3833 aproximadamente (comprobar localizadores exactos).

No se copian artículos ni datos clínicos/genotipos. Solo se leen estos dos archivos de código/cultivos. Presupuesto máximo de transferencia de contenido: 200 KiB, sin clon completo ni nueva instalación. Originales conservados temporalmente, derivados y hashes en Git privado. Verificar bytes mediante SHA256 y hash Git blob antes del análisis.

## Método

Reproducción en Python estándar de agrupación, media, desviación muestral y sd/sqrt(n); tablas con cantidad de filas por grupo. Emular explícitamente las claves comunes del left_join del Rmd y comparar con unión antes del renombrado. No ejecutar el Rmd completo, que instala dependencias; R no está disponible en este host. No se presenta la emulación como ejecución de R ni reproducción exacta de ggplot.

Conservar filas idénticas: sin IDs no se sabe si son duplicados o mediciones distintas. No emparejar filas de RNA/proteína por orden. No convertir filas en diferenciaciones. Reproducir el cálculo de error estándar del código como aritmética de filas, no como estimación de precisión biológica. Auditar la composición de grupos, incluidos los valores adicionales UNC13B, sin eliminarlos por suposición.

Descriptivo secundario prefijado: tabla y gráfico de medias de ARN total, ARN correcto y proteína UNC13A para NT y Dox-1…5, en escala original del archivo. No deducir dosis/concentraciones/tiempos desde las etiquetas Dox. No ajustar curvas, umbrales, correlaciones, mediaciones o p-valores; no comparación de eficacia ni rescate funcional.

Control: cálculo independiente con fracciones racionales de medias/varianzas, permutación del orden de filas, conservación de puntos y rechazo de datos no finitos/grupos desconocidos. Figura de tres series con puntos individuales y medias, sin intervalos de confianza ni inferencia; comprobar visualmente etiquetas, unidades y datos.

## Límites y parada

Falta mapa de independencia biológica y emparejamiento. Un resultado molecular publicado no es una nueva validación externa ni explica por sí solo una discrepancia RNA/proteína. Una incidencia en el código público no demuestra un defecto en la figura final. No contactar autores ni abrir issues en sus repositorios.

Entregar un único informe con tablas, gráfico, script, versiones y hashes en una PR sin fusionar. No modificar STATE/BACKLOG mientras #46/#47 trabajan en ellos: explicar este alcance en el informe y la PR, con referencia a sus prioridades bloqueadas. Terminar después de este CSV/bloque, sin saltar a otros repositorios. K26 Fig.4d sigue siendo el objetivo funcional.
