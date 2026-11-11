# ST7 enlaza con los 45 pares; ajuste tisular común todavía no justificado

11/11/2026. Revisión técnica y de comparabilidad, sin nuevo contraste biológico. [Alcance fijado](../../research/plans/2026-11-11-stmn2-composition-gate.md) antes de leer ST7. Los resultados STMN2 y RIN anteriores ya eran conocidos.

## Evidencia

Se descargó exclusivamente el libro de tablas de expresión de [Zenodo 20090702](https://zenodo.org/records/20090702), 32.702.280 bytes, MD5 `d49eca47d62502c5b89627c96dae4d75`, coincidente con el manifiesto; SHA-256 `6b24edc4279eebb0d8560ef277573745fa0110e1e8d1a07009621d020cd2abfc`. No se descargaron matrices RNA, FASTQ o BAM. El libro permanece temporal; el repositorio contiene solo esquema, agregados y hashes.

ST7 contiene **16.985 filas de estimaciones**, con columnas `Sample`, `cell type`, `estimate`, `tissue`. Hay **1.724 vectores muestra/referencia** válidos: sin claves celulares duplicadas dentro de cada vector, valores numéricos finitos entre 0 y 1, suma uno con tolerancia 10⁻⁶ y todas las categorías observadas en su referencia. No se confunden filas de tipos celulares con réplicas biológicas.

| Comprobación sobre el análisis congelado | Corteza | Cervical |
|---|---:|---:|
| Bibliotecas de los 45 pares originales | 45 | 45 |
| Clave Sample exacta con un único vector válido | 45 | 45 |
| Etiqueta de referencia compatible | Cortex: 45 | Spinal Cord: 45 |
| Categorías por vector | 8 | 11 |

Por tanto **45/45 pares tienen ambas estimaciones**; no hay pérdida de muestra por enlace ST7. El mapa de donante/región/preparación es el previamente validado; el enlace nuevo es por biblioteca exacta, sin deducir individuos por prefijos. El vector de corteza y el cervical no son réplicas independientes del donante.

## Método y comparabilidad

El [trabajo fuente NYGC](https://www.medrxiv.org/content/10.64898/2026.04.29.26350889v1.full), apartado *Cell-type deconvolution*, describe **MuSiC 1.0.0** con controles como referencia: GSE140231 para corteza, GSE190442 para médula y GSE246183 para cerebelo. Son estimaciones derivadas de expresión bulk, no recuentos histológicos. El código de autores, `jackhump/NYGC_ALS_Flagship`, árbol `bed82ad63b0d959237f9368561e1145230463ecb`, separa archivos de proporciones por referencia en `scripts/Deconvolution_scatters.Rmd`; los efectos/estadísticos están en otro script. El método menciona ajustes mediante residuos para comparar composición entre grupos. La hoja ST7 no etiqueta por fila una transformación, por lo que su condición exacta de estimación bruta frente a transformada no queda demostrada solo por el nombre de columna; los vectores pasan las comprobaciones de proporciones.

Las categorías son distintas:

- Corteza: Astrocytes, Endothelial, Excitatory, Inhibitory, Microglia, Oligodendrocytes, Opc y Pericytes.
- Médula: Astrocytes, Endothelial, Ependymal.Cells, Lymphocytes, Meninges, Microglia, Neurons, OPC, Oligodendrocytes, Pericytes y Schwann.

La suma Excitatory+Inhibitory cortical es una agregación plausible para representar neuronas dentro de esa referencia, pero **no verifica por sí sola su calibración frente a Neurons en la referencia medular**. Distintos genes de referencia, poblaciones celulares incluidas y eficiencias pueden cambiar la escala de una proporción estimada. Compartir algoritmo y sumar uno son controles necesarios del archivo, no pruebas de que ambas estimaciones sean intercambiables ni de que midan el porcentaje físico de células sin sesgo.

## Decisión

**Enlace técnico aceptado para los 45 pares. Ajuste único del efecto corteza−médula con fracciones celulares tratadas como una escala común: no habilitado con la evidencia revisada.** No se calculó un nuevo efecto “corregido por composición”, no se restaron porcentajes neuronales de referencias distintas y no se dividió el cociente de STMN2 por una fracción neuronal. No se afirma que sea imposible analizar estas estimaciones ni que usar referencias distintas invalide cualquier modelo; la limitación afecta a la interpretación de una corrección tisular común que aún no se ha validado.

El resultado original sigue siendo asociación tisular exploratoria, con sensibilidad RIN principal positiva en 19 pares y subconjunto estricto de nueve con mediana cero. El enlace de composición no aporta replicación externa ni elimina esos límites. La variación en calidad, profundidad, composición y patología puede coexistir; no se asigna causalidad a una sola vía.

## Siguiente experimento concreto

Hay dos preguntas diferentes y una ruta acotada para cada una:

1. **Compatibilidad de medida para ajustar la comparación tisular:** obtener la procedencia exacta de ST7 (tabla bruta o transformación) y una estimación de clases celulares amplias con referencia armonizada o calibración de las dos referencias. Si se recalcula deconvolución, usar las mismas bibliotecas y fijar antes marcadores, clases y controles; requeriría datos de expresión y no se ha iniciado en este ciclo.
2. **Análisis viable sin asumir una escala común entre tejidos:** estudiar, por separado dentro de corteza y dentro de cervical, la relación de la medida STMN2 con la estimación neuronal de su referencia. Requiere un protocolo único antes de calcular asociaciones, con control de cobertura/RIN y sin presentar dos correlaciones como corrección del efecto tisular. Puede evaluar una explicación alternativa dentro de cada región, pero no demostrar independencia de composición entre regiones.

La prioridad técnica más barata es esta segunda ruta, con los datos ya enlazados. No se ejecuta aquí porque el alcance fijado era la aceptación del covariable, no una nueva búsqueda de asociaciones. No se necesita ampliar cohortes para formularla. #37 UNC13A y #44 K26 permanecen sin cambios.

## Verificación y reproducción

`python scripts/stmn2_composition_gate.py --source-root /ruta/temporal/stmn2-audit-work --output /ruta/temporal/gate.json` reproduce el agregado; el libro temporal está en `source-gate/nygc-expression-tables.xlsx`, y las fuentes/conteos conservan la estructura usada anteriormente. El script verifica el hash y localiza ST7 mediante las relaciones del libro, sin depender del número de hoja. `gate.json` no contiene claves de muestras ni donantes.

Cinco tests nuevos cubren vectores válidos con ceros, claves duplicadas, valores no finitos/fuera de rango, suma incorrecta, categorías incompletas y separación de taxonomías. La cobertura por biblioteca se comprobó sobre los datos reales. No se crearon nuevos modelos ni tests biológicos; la CI del PR verifica la suite offline completa y compilación.
