# UNC13A: reproducción molecular del repositorio Fratta — 04/11/2026

## Resultado

Se han procesado **138 mediciones depositadas**, reconstruido **42 grupos moleculares** y reproducido en Python la agrupación y unión de tablas del bloque público «Dox curves and protein/RNA levels». El orden original de renombrado/unión deja sin error estándar los seis grupos `13A-Correct RNA`; unir por las claves originales antes de renombrar conserva esos seis errores, sin cambiar ninguna media.

**Alcance:** reproducción aritmética de un CSV y de las transformaciones descritas por un bloque R; R no está instalado y **no se ejecutó el Rmd**. No hay ajuste estadístico, descubrimiento biológico, replicación experimental independiente o rescate funcional. No se certifica cómo se generó la figura final del artículo.

Luis autorizó expresamente el 04/11 avanzar con los repositorios públicos de Fratta. El plan previo se publicó en commit `9d61c4da691ab5c4aac34a036a4b8608f190f744`, antes del cálculo. Tarea distinta de la auditoría de uniones ya completada, de STMN2/PPAU y de A25 Fig.3s (#47). No se cambian prioridades ni entradas de #37/#44. STATE/BACKLOG no se editan para evitar interferir con #46/#47.

## Fuentes y método

- Repositorio `frattalab/unc13a_cryptic_splicing`, commit `e05e8723e3d18e64c6c559db18de423282511c91`.
- `data/Protein_RNA_Corr_3.csv`: 4.738 bytes; SHA256 `c7de1f2d44f9a5ac243e0ef380f50c455254c1cbefc6a217dc091505918526e5`.
- `paper_figures.Rmd`: 148.855 bytes; SHA256 `3c46c164af6572bef28507b707f39d996d687abb06da00bf5468f89d0d491502`.
- Ambos bytes cotejados también con sus Git blob originales. No se clonó el repositorio ni se leyeron sus archivos clínicos/genéticos. Originales temporales; los enlaces inmutables y hashes permiten recuperarlos.

Se agrupa por Treatment/Gene/Line_Group/Color_Group y se calcula media, desviación muestral y `sd/sqrt(n_rows)`, tal como el bloque autor. La aritmética de los 42 grupos se coteja con fracciones racionales independientes. Permutar filas no cambia los resúmenes. Una segunda ejecución produce los mismos cuatro CSV numéricos por bytes.

Estas operaciones reproducen la aritmética especificada, **no validan que cada fila sea una réplica biológica independiente**. Faltan identificadores de experimento, cultivo/diferenciación y emparejamiento entre ensayos. No se emparejan filas por orden ni se calcula correlación entre ARN y proteína.

## A. Datos publicados y B. cálculo de nuestro proyecto

Las mediciones son de los autores; nuestro trabajo reconstruye sus resúmenes. En la escala relativa original del archivo (NT aproximadamente 100), las medias calculadas para UNC13A son:

| Condición | ARN total | ARN correcto | Proteína |
|---|---:|---:|---:|
| NT | 101,00 | 100,33 | 100,03 |
| Dox-1 | 95,00 | 94,00 | 80,53 |
| Dox-2 | 59,33 | 55,33 | 33,17 |
| Dox-3 | 50,33 | 45,33 | 14,33 |
| Dox-4 | 42,33 | 30,67 | 8,03 |
| Dox-5 | 25,33 | 10,00 | 4,30 |

La figura `unc13a-molecular.svg` conserva los 54 puntos de estas tres series y sus medias, sin intervalos inferenciales. Es un gráfico descriptivo nuevo a partir de datos ya publicados, no una copia exacta del gráfico autor: este elimina ARN total UNC13A y muestra también series UNC13B/TDP-43. Todas las series están disponibles en `all-groups.csv`.

La diferencia entre las tres medidas es visible en este conjunto: ARN total, ARN correctamente procesado y proteína no deben tratarse como lecturas intercambiables. **No demuestra por qué difieren**, una relación temporal, un umbral terapéutico, una pérdida de función o una significación estadística entre ensayos. No se infieren concentraciones, duración ni magnitud exacta de perturbación desde las etiquetas `Dox-1…5`.

## Incidencia de las claves de unión

El bloque autor:

1. Calcula medias y errores por las cuatro claves originales, incluido `Line_Group`.
2. Quita `13A-RNA` del gráfico.
3. Cambia `Correct_RNA` a `RNA` en la tabla de medias.
4. Hace `left_join(tmp)` sin especificar claves. Las columnas comunes incluyen `Line_Group`; `tmp` conserva `Correct_RNA`.

En la reproducción explícita de esas claves, los seis grupos de ARN correcto ya no tienen coincidencia: seis errores estándar ausentes de 36 grupos gráficos. Cambiar la secuencia a **unir primero y renombrar después** produce 36 coincidencias y deja todas las medias idénticas. `source-order-join.csv` y `key-preserving-join.csv` conservan ambos resultados.

Esto es una incidencia técnica reproducible del bloque público fijado. No hemos ejecutado dplyr/ggplot en su entorno ni cotejado qué revisión generó la figura editorial. No se concluye que el artículo esté equivocado, que sus conclusiones cambien o que los autores omitieran deliberadamente incertidumbre. No se envía aviso ni se abre una issue externa sin autorización.

## Composición y controles

- 36 grupos contienen tres filas cada uno. Los seis grupos de proteína UNC13B contienen cinco. Un promedio global de todas las filas daría pesos distintos a los ensayos; no se realiza.
- Existen 16 filas idénticas adicionales respecto a sus combinaciones de valores únicas. **Se conservan todas**: sin identificadores no se sabe si son repeticiones legítimas o duplicados. No se aplica la deduplicación de otra tabla histórica a esta fuente distinta.
- Los errores `sem_rows` reproducidos usan filas; no se presentan como errores biológicos, IC o evidencia de significación. La figura descriptiva muestra puntos y medias sin esos errores.
- Los valores cero de TDP-43 proteína se conservan; no se dividen valores por esa serie ni se calculan cocientes con denominadores cero.
- El script verifica hashes, cabecera, etiquetas conocidas, valores finitos/no negativos y cuadrícula de grupos completa. Cinco pruebas de transformación verifican cambios de claves, desviación muestral, permutación, conservación de valores idénticos y rechazo de grupos de una sola fila.

## Reproducción

Descargar únicamente los dos archivos desde los enlaces inmutables de `sources.json`. El script exige que sus SHA256 coincidan. Desde raíz del proyecto:

```bash
python scripts/reproduce_fratta_dox.py --source-csv /ruta/Protein_RNA_Corr_3.csv --source-rmd /ruta/paper_figures.Rmd --output reports/fratta-dox-replay-20261104 --plot
python -m unittest discover -s tests -p 'test_fratta_dox_replay.py' -v
```

Python 3.12.14; biblioteca estándar para tablas; Matplotlib 3.10.8/Agg para la figura, ya instalado. Sin paquetes nuevos, entrenamiento, descargas masivas o costes. `--plot` es opcional: sin él no se necesita Matplotlib. R no ejecutado; no se atribuye una concordancia de p-valores o gráficos editoriales.

Se corrigió un fallo inicial de transporte local: el base64 del conector incluía saltos de línea y una cadena literal Python no los aceptó. No llegó a crearse el CSV; se eliminaron los espacios del base64 y después se verificaron tamaño, SHA256 y Git blob. No se modificó el dato para superar los hashes. Errores y validación en archivos adjuntos.

## C. Interpretación y siguiente paso

La contribución actual es técnica y descriptiva: resúmenes ejecutados, distinción entre lecturas moleculares y una incidencia de unión verificable. No es una nueva contribución biológica acreditada. Para inferencia molecular se necesitaría el mapa de independencia y emparejamiento de esta tabla; no se solicita ni se abre esa línea por defecto.

Este ciclo termina con un único CSV/bloque. El siguiente objetivo funcional sigue siendo K26 Fig.4d cuando se publiquen sus datos. La respuesta de Fratta aportada por Luis el04/11 anticipa disponibilidad la semana siguiente; no constituye datos ya recibidos. No se repiten búsquedas ni se amplía a más herramientas para eludir el bloqueo.
