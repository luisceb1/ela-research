# Asadollahi2025 Fig.3s: datos numéricos disponibles, mapa de cultivo ausente

Auditoría de viabilidad autorizada por Luis el04/11/2026. No es reanálisis de efectos ni validación funcional propia. Base: main95bf05ecc1f991ec9843d48519d0764b29dc5dfb. PR#46 sigue pendiente e independiente; sus informes/avisos no se presentan como incorporados a main.

## Decisión

**Disponibilidad parcial. NO-GO para inferencia que respete el cultivo como unidad independiente.** Se recuperó un archivo fuente original con73 entradas numéricas para Fig.3s:38 WT y35 R202H. La hoja inspeccionada no aporta identificadores de neurona ni asignación de esas entradas a cultivos. Tampoco documenta exclusiones. No se calcula diferencia, ratio, media por grupo, p-valor o intervalo de confianza.

La predicción prospectiva de disponer de valores, unidades y claves biológicas se cumple solo parcialmente. Se alcanza la parada prevista por falta del mapa, conservando una proyección experimental verificable. No se inventan tres cultivos, IDs por fila o pareamiento entre columnas.

## Evidencia del archivo

- Fuente editorial: `41588_2025_2361_MOESM10_ESM.xlsx`, enlazada por [el artículo](https://doi.org/10.1038/s41588-025-02361-5) y [registro MBExC](https://mbexc.uni-goettingen.de/literature/publications/1299). URL exacta en PLAN.md y retrieval.json.
- Descarga HTTP200,1185531 bytes. SHA256 original: `42f9a2266bf8e7dc157350fe588f1d87deb8d0e4c5067bc2c780b9fc7851a49f`. Verificación CRC del ZIP correcta en la recuperación; hashes de los miembros utilizados en audit.json.
- Nueve hojas visibles en el manifiesto. Se selecciona `Figure 3_R202H`, miembro `xl/worksheets/sheet3.xml`, con dimensión A1:AB41. No se interpretan valores de otras hojas. Se leen los rótulos técnicos de la hoja seleccionada para localizar la medida y comprobar la ausencia de campos de diseño.
- I1 identifica literalmente `Figure 3s: Initial EPSC Charge (pC)`; I3/J3: `UNC13AWT` y `UNC13AR202H`. Es **carga integrada**, no amplitud de corriente, frecuencia mEPSC o cantidad de proteína. Se conserva la convención numérica depositada sin transformar signos o unidades.

| Grupo publicado | Rango fuente numérico | Entradas | Huecos internos | Ceros/negativos | Repeticiones numéricas dentro del grupo | Fórmulas/errores |
|---|---|---:|---:|---:|---:|---:|
| UNC13AWT | I4:I41 |38|0|0/0|0|0/0|
| UNC13AR202H | J4:J38 |35|0|0/0|0|0/0|

J39:J41 son tres celdas vacías al final de una columna más corta. No se convierten en ceros ni se presentan como tres neuronas perdidas o excluidas. No conocer IDs impide verificar duplicados biológicos aunque no se repitan valores numéricos. Las73 coordenadas Excel son distintas; eso no demuestra73 unidades biológicas independientes.

La revisión de rótulos encuentra solo los nombres de medidas y grupos de los cinco bloques experimentales. No hay celdas pobladas fuera de sus columnas de medida que proporcionen una clave de diseño. No hay nombres definidos, comentarios, tabla estructurada o archivo de relaciones de esta hoja que contenga una asignación adicional. Todos los valores objetivo usan el mismo estilo2: no se convierte formato/color en cultivo. Estos hallazgos se limitan a la fuente y hoja inspeccionadas, no a toda documentación posible del estudio.

## Controles de procedencia y significado

La leyenda de [Fig.3](https://pmc.ncbi.nlm.nih.gov/articles/PMC12597829/) describe neuronas hipocampales de ratón en cultivo autáptico que expresan UNC13A WT o variantes, carga evocada en el panel3s, puntos correspondientes a neuronas y datos procedentes de al menos tres cultivos independientes por condición. Esa declaración no permite asignar cada fila al cultivo ni comprobar balance, reutilización o dependencia. No se atribuye a los autores un análisis incorrecto por falta del mapa en este archivo.

| Requisito prospectivo | Resultado |
|---|---|
| Fuente editorial, identidad, bytes y hash | Verificados |
| Panel, medida, unidades y grupos | Verificados |
| Entradas numéricas a nivel de los puntos publicados | Disponibles,38/35; identidad por neurona declarada en la leyenda, sin clave de neurona en la tabla |
| Identificadores de neurona y correspondencia con cultivos | No aportados en la hoja inspeccionada |
| Número efectivo y balance de cultivos del contraste | No reconstruibles; no deducidos de las filas o del n mínimo de la leyenda |
| Exclusiones y correspondencia con todos los registros adquiridos | No verificadas |
| Aceptación para inferencia jerárquica | No |

La proyección fig3s-projection.csv contiene únicamente coordenada fuente, grupo experimental y valor depositado en pC. `neuron_id` y `culture_id` quedan vacíos, sin claves fabricadas. La alineación de filas I/J no acredita parejas. No se vincula esta proyección con otras medidas de la hoja.

## Ejecución y pruebas

Python3.12.14, biblioteca estándar; sin instalaciones, Excel, MATLAB, R o fórmulas ejecutadas. El plan y su hash se guardaron antes de descargar. retrieval.json conserva el recibo de esa recuperación inicial; execution.json identifica la ejecución del lector final sobre esos mismos bytes y el SHA256 del script. Semilla no aplicable: no se genera aleatoriedad.

Trece controles de software pasaron localmente, cero fallos/errores/omisiones. Cubren: preservación de cero/vacío, rechazo de unidad/grupo/hash incorrectos, fórmula con caché y números no finitos, grupo vacío, ausencia de mapa sin inferencia, estilo sin cultivos inventados, exclusión de otra hoja no interpretable, marcador de contenido fuera de alcance y metadatos inesperados. Una repetición numérica de una fixture se marca sin eliminarla. Son fixtures informáticas, **no experimentos ni réplicas biológicas**.

QC independiente de la salida:73 filas y73 coordenadas únicas,38/35 según grupo, ambas claves de identidad vacías y ningún efecto estimado. Compilación correcta. tests.json/tests.log conservan el resultado local; la CI remota debe leerse por cabeza exacta y no se presume correcta por estos controles.

No hubo error de red en esta descarga. La consulta web posterior de PMC devolvió una comprobación de navegador; no se trató ese HTML como artículo ni como datos. La leyenda se había recuperado por el servicio de búsqueda primaria y el enlace de archivo por el editor/MBExC. No se afirma haber leído Supplementary Data3, cuyo contenido no forma parte del archivo único autorizado.

## Reproducción

Desde la raíz del repositorio, con Python3.11 o3.12:

```bash
python scripts/audit_asadollahi_fig3s.py --download --source /tmp/asadollahi-MOESM10-source.xlsx --output-dir /tmp/asadollahi-fig3s-audit
python -m unittest discover -s tests -p test_audit_asadollahi_fig3s.py -v
```

Sin `--download`, se audita una copia local con el mismo hash esperado. Un archivo remoto cambiado se rechaza antes de interpretarlo; no se acepta silenciosamente como la versión auditada. El proceso exitoso significa auditoría completada; la decisión científica permanece en `PARTIAL_VALUES_AVAILABLE_NO_GO_INFERENCE`.

## Interpretación, límites y siguiente prueba

Este es un avance de acceso y trazabilidad: ya hay valores funcionales experimentales, a diferencia de un mero PDF con puntos. No reproduce todavía la comparación biológica. Es otro modelo y perturbación: variantes UNC13A en neuronas de ratón, no corrección ASO tras pérdida TDP-43 en motoneuronas humanas. No sustituye K26 Fig.4d, no mide recuperación posdéficit, no demuestra beneficio en ELA y no acredita un descubrimiento original.

No se descargaron los suplementos clínicos, imágenes/vídeos de personas u otros archivos. No se exporta el libro completo a GitHub. Se conserva solo la proyección de cultivo autorizada y sus resultados técnicos.

**Única prueba discriminante siguiente:** una tabla o documentación técnica primaria que vincule inequívocamente las entradas de Fig.3s con sus cultivos y aclare la identidad de las observaciones/exclusiones. Informar únicamente de un n total de cultivos no resuelve el mapa. Cualquier ampliación a otro archivo/análisis queda fuera de esta auditoría limitada. Se cierra esta sesión de viabilidad con disponibilidad parcial; no se ajusta un modelo, no se abre otro candidato y no se reactivan tareas automáticas. #37/#44 siguen bloqueadas por sus entradas respectivas.
