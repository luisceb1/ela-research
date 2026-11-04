# A25 Fig.3s: reproducción aritmética descriptiva — 04/11/2026

Las dos medias calculadas con los 73 valores experimentales depositados concuerdan con Supplementary Data 3 dentro del redondeo definido antes del cálculo. Se reconstruyeron todos los puntos y sus medias; no se recibió un mapa observación→cultivo.

## Evidencia

| Grupo publicado | Observaciones | Media calculada (pC) | Media publicada (pC) | Diferencia absoluta (pC) | Tolerancia de redondeo (pC) | Concordancia |
|---|---:|---:|---:|---:|---:|---|
| UNC13A WT | 38 | 24.209923 | 24.2 | 0.009922895 | 0.05 | Sí |
| UNC13A R202H | 35 | 15.009117 | 15.01 | 0.000882571 | 0.005 | Sí |

Las cifras mostradas están redondeadas para lectura. [result.json](result.json) y [mean-concordance.csv](mean-concordance.csv) conservan el cálculo Decimal con precisión 50. Son dos comprobaciones de medias del mismo experimento publicado, no dos experimentos o cohortes nuevos.

El [plan prospectivo](PLAN.md) fijó pregunta, predicción, controles, tolerancia inclusiva de media unidad de la última cifra decimal publicada y criterios de fracaso antes de extraer las medias y ejecutar el cálculo. Ninguna diferencia excedió su tolerancia. Esta tolerancia describe representación decimal, no incertidumbre experimental.

## Fuentes e identidad del endpoint

Estudio: Asadollahi et al., Nature Genetics 2025, [DOI 10.1038/s41588-025-02361-5](https://doi.org/10.1038/s41588-025-02361-5).

- [MOESM10: Source Data](https://static-content.springer.com/esm/art%3A10.1038%2Fs41588-025-02361-5/MediaObjects/41588_2025_2361_MOESM10_ESM.xlsx), 1,185,531 bytes; SHA256 `42f9a2266bf8e7dc157350fe588f1d87deb8d0e4c5067bc2c780b9fc7851a49f`. Hoja `Figure 3_R202H`, I1 identifica Initial EPSC Charge (pC); I4:I41 WT y J4:J38 R202H. J39:J41 son vacíos terminales, no ceros.
- [MOESM8: Supplementary Data 3](https://static-content.springer.com/esm/art%3A10.1038%2Fs41588-025-02361-5/MediaObjects/41588_2025_2361_MOESM8_ESM.xlsx), 18,581 bytes; SHA256 `7ba494959360e824eb333eeadb2e0fd1bb431a32859da92cabdd5a958cf1c2e7`. Table 3: B35=Charge (pC), I35=3s, C18/E18 identifican grupos, C35/E35 contienen medias y C36/E36 confirman n=38/35. B33 es amplitud en nA y queda fuera de este análisis.

Se reutilizaron los lectores ZIP/XML y sus verificaciones de hash, hoja, grupos, unidades, coordenadas y n. El lector del suplemento añade una opción explícita para recuperar solo C35/E35 de este endpoint; su salida predeterminada previa no cambia. El cálculo toma únicamente el componente de media de esas dos celdas. No se exportaron tablas de otros paneles ni se recalcularon SEM o p-valores. Los XLSX originales permanecen sin modificar.

## Método, ejecución y QC

Media aritmética no ponderada: suma de todas las observaciones del grupo dividida por su n, sin exclusiones, deduplicación, normalización, imputación o pareamiento por fila. Python 3.12.14 real, biblioteca estándar para el cálculo; Matplotlib 3.10.8/Agg para la figura. No se instalaron paquetes.

```bash
python scripts/reproduce_asadollahi_fig3s_descriptive.py \
  --measurements /tmp/asadollahi-MOESM10-source.xlsx \
  --summary /tmp/asadollahi-MOESM8-supplement3.xlsx \
  --output-dir reports/fig3s-descriptive-20261104 \
  --plot --preview-png /tmp/fig3s-descriptive-preview.png
```

Sustituir las rutas de entrada por los dos originales con los hashes indicados. La ejecución del 04/11/2026, 10:44:39 Europe/Madrid, terminó correctamente con concordancia verdadera. [execution.json](execution.json) registra versión, plataforma, parámetros, tiempos, hash del script y del SVG/PNG de revisión. El PNG fue una vista temporal; se conserva el SVG exportado. La salida numérica funciona sin Matplotlib si se omite `--plot`.

Controles completados:

- 24 pruebas de software correctas, sin fallos, errores u omisiones: 19 controles previos de los lectores y 5 de precisión, límite inclusivo, denominador completo, formato ambiguo/no finito y n incorrecto. [Registro](tests.log), [resumen](tests.json). No se cuentan como experimentos.
- Cotejo independiente con fracciones racionales exactas desde el CSV de proyección anterior: ambas medias Decimal difieren del cociente exacto en menos de 1e-46 pC; conteos y concordancia revalidados.
- Reejecución numérica en directorio temporal: `result.json` y CSV idénticos byte a byte. No implica que los tiempos de ejecución sean idénticos.
- Conteo de objetos gráficos: 38/35 puntos. Revisión visual: se movió la leyenda al espacio superior izquierdo para evitar cubrir un punto alto. No se cambió ningún valor. No hubo fallo de lectura o cálculo en esta etapa. [QC](qc.json).

Los controles negativos de software rechazan conteos incorrectos, medias ambiguas/no finitas y discrepancias que exceden el límite. El resultado negativo científico persiste: ninguno de los dos suplementos inspeccionados proporciona la asignación de estas observaciones a cultivos; la declaración de al menos tres cultivos no reconstruye ese mapa. El acceso público denegado a GOE-Seek está documentado en la [auditoría anterior](../asadollahi-fig3s-audit-20261104/PUBLIC_ACCESS_REPORT.md); no se repitió la consulta en esta etapa.

La verificación remota registró un rechazo del conector al consultar una ruta de rama codificada; se cotejó la cabeza con la lista de PR y el objeto commit. [Registro técnico](verification-errors.json). No afectó al análisis o sus datos.

## Figura

[SVG reproducible](fig3s-descriptive.svg): muestra los 73 valores reales y dos líneas de media no ponderada, sin barras SEM/IC, estrellas o pruebas. Los desplazamientos horizontales son cosméticos y deterministas: `(((row_index*7)%17)-8)*0.014`; no representan cultivos, parejas o nuevos datos. Tamaño 6.4×4.8 pulgadas, fuente DejaVu Sans, SVG sin fecha y sal fija, PNG de revisión a 160 dpi. Parámetros completos en código y ejecución.

## Interpretación y limitaciones

**Nivel de evidencia: reproducción descriptiva de resúmenes del mismo estudio.** Esta concordancia apoya la identidad y el cálculo del endpoint seleccionado. No constituye una replicación biológica externa ni validación funcional propia.

Son neuronas autápticas hipocampales de ratón Unc13a/b DKO que expresan WT o R202H. El modelo, la perturbación y el endpoint no sustituyen el rescate con ASO tras déficit TDP-43 en neuronas motoras espinales humanas de Keuss Fig.4d. No se demuestra eficacia en ELA, beneficio clínico, mecanismo nuevo u originalidad.

Faltan identidades de cultivo por observación, exclusiones y estructura de dependencia verificables. 38/35 observaciones no se convierten en 38/35 unidades biológicas independientes. La media publicada podría ponderar cultivos de otra manera; esta comprobación solo reproduce la media no ponderada de los valores depositados, sin resolver ese diseño. No se estimaron diferencias/ratios entre grupos, p-valores, SEM, IC ni efectos de rescate. El NO-GO inferencial permanece.

## Siguiente prueba discriminante y parada

Entrada necesaria: mapa técnico primario que vincule de manera inequívoca las observaciones depositadas con cultivos independientes y aclare exclusiones. Comprobar integridad, grupos, unidades y denominadores antes de definir cualquier análisis de dependencia. Si falta o es ambiguo, mantener el NO-GO; no sustituirlo por etiquetas de fila o simulación.

La consulta de soporte ya autorizada y enviada se conserva en su [registro](../asadollahi-fig3s-audit-20261104/COMMUNICATION_LOG.md). No se envió un nuevo mensaje en esta etapa. La sesión descriptiva queda completada, en PR revisable, sin merge, cierre de issues o reactivación automática.

