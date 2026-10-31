# GSE122069: auditoría acotada del diseño — 31/10/2026

## Evidencia

Python ejecutado realmente (3.12.14). Acceso remoto a GitHub comprobado; PR33 seguía abierto en167d370ed8b8ffd7feeb24b81208f15ed4492d35 y PR30 en053ef70ce437cc637ec18278a2c07e3abd6bf58b, sin modificarlo. Main avanzó a96975b1c4bea6cf9267d03c15bdd4373dad3966e únicamente por auditoría automática PubMed, sin solapamiento con esta fase. Leídos AGENTS, STATE, BACKLOG, PROTOCOL, issues y ramas abiertas. Las otras ramas son historial; no se reejecutaron sus análisis.

Pregunta y predicción previas en[plan](../../research/plans/2026-10-31-gse122069-design-gate.md): ¿una fuente técnica explícita permite enlazar las seis bibliotecas con unidades experimentales, lotes y pares sin ambigüedad? Fracaso previsto: falta/conflicto de ese mapa o fuente inaccesible. Controles: seis accesiones y grupos fijados, cultivos SH-SY5Y, declaración previa de tres réplicas biológicas por condición; no derivar unidades o pares de sufijos/fechas/accesiones distintas.

**Resultado:** seis experimentos y seis muestras públicas recuperados y proyectados por lista de campos técnicos permitidos. Doce registros válidos, cero errores finales. [Mapa técnico](library-design.tsv) y[resultados](results.json). Los seis enlaces GSM→SRX→SRS/SAMN concuerdan con las condiciones publicadas. La identidad de accesión no demuestra independencia de cultivo.

| Dependencia de diseño | En las fuentes revisadas |
|---|---|
| Relación de las seis bibliotecas con muestras públicas | Documentada |
| Declaración de autores: tres réplicas biológicas por condición | Conservada como evidencia previa |
| Asignación explícita biblioteca→unidad de cultivo/experimento biológico | No recuperada |
| Asignación de lotes experimentales/cultivo o constancia explícita de ausencia de lotes | No recuperada |
| Pareamiento o constancia explícita de diseño no pareado | No recuperada |

No hay candidatos de campos de diseño en la lista técnica inspeccionada. El gate completo permanece cerrado; no se prueba que los experimentos sean dependientes ni se contradice la declaración de los autores.

Nueva fuente concreta:[Reporting Summary del editor](https://static-content.springer.com/esm/art%3A10.1038%2Fs41593-018-0293-z/MediaObjects/41593_2018_293_MOESM2_ESM.pdf),75.419bytes,SHA256ea09e2569478fecd927fb1340424e1fbbbe32e46d3815beb7c1b433296b7b772. Inspección visual de páginas1/2 y del párrafo de cultivo de página3, más extracción textual de las tres páginas. No se descargaron las tablas clínicas ni se conservaron sus datos. El formulario remite los números de réplicas a figuras/texto y declara repetición independiente general; no enlaza bibliotecas con culturas o lotes. La ausencia de tokens GSM/SRX/SRR es solo un control textual, no la prueba semántica por sí sola. [Proyección](reporting-summary-projection.json),[QC](reporting-summary-qc.json).

Hallazgos técnicos adicionales del formulario: STAR2.5.3a,RSEM1.3.0,DESeq2 1.14.1 son versiones de los autores, no las usadas en nuestro alineamiento. Declara ausencia de aleatorización y de cegamiento a escala del estudio; no atribuir sin más una estructura específica de lotes a esta afirmación general. El lote531342 corresponde al suero, **no a un experimento de cultivo o secuenciación**.

Discrepancia de protocolo, sin reconciliación automática: el formulario describe F12+Minimum Essential Medium1:1; el campo de crecimiento de GEO para el control describeDMEM/F12. Reconsulta justificada por esta discrepancia nueva, no nueva prueba del kit previamente auditado. La respuesta GEO conserva exactamente elSHA previo05c506968dddc7fb1b3efd602e2d9f6463f53523d9562cc6ad75a744b32ee14e. [Proyección técnica](growth-protocol-recheck.json). No asignar una formulación a un grupo ni explicar causalmente la cobertura con este conflicto.

## Pruebas, errores y reproducibilidad

Primer intento: las seis muestras se rechazaron porque el parser exigía SRS como identificador principal, mientras ENA devuelve SAMN como principal y SRS comoSECONDARY_ID explícito. Se preservan las seis incidencias y sus hashes en[source-projections-attempt1.json](source-projections-attempt1.json). Se corrigió el contrato de identidad para admitir solo una identidad primaria/secundaria explícita, sin relajar condición, cultivo o coincidenciaGSM. Se recuperaron únicamente las seis respuestas fallidas; las seis respuestas originales y corregidas tienen el mismoSHA256. Ningún experimento se consultó de nuevo por este arreglo. [Comprobación](parser-repair-qc.json).

El acceso web al editor falló por redirección de identidad; PythonHTTP obtuvo200 y permitió descubrir el PDF. No se presenta ese fallo del navegador como falta de publicación. URLs, fechas, tamaños ySHA originales de cada recuperación están en las proyecciones/recibos; cuerpos con contactos no retenidos. Datos guardados: accesiones, grupos de cultivo publicados y variables técnicas por lista permitida. Ningún dato clínico personal, FASTQ nuevo, alineamiento, efecto o comunicación externa.

**349 pruebas locales y compileall correctos**:335 anteriores+14 nuevas. Controles de identidad secundaria explícita, conflicto de grupos, accesiones duplicadas, metadatos ausentes, exclusión de valores no técnicos, fuentes insuficientes de unidades, lotes de reactivo y falso benchmark completo. No son349 experimentos. Repetición del mismo análisis sobre las mismas proyecciones produceJSON/TSV idénticos por bytes;[verificación](repeat-verification.json). PySAM/HISAT2 no se ejecutaron en esta fase.

Desde raíz:

```bash
python scripts/gse122069_design_gate.py collect --out reports/gse122069-design-20261031
python scripts/verify_gse122069_reporting_projection.py /ruta/al/ReportingSummary.pdf
python scripts/gse122069_design_gate.py audit --out reports/gse122069-design-20261031
python scripts/plan_gse122069_remaining_resources.py
python -m unittest discover -s tests -v
```

El modoaudit usa proyecciones congeladas y revisión manual de evidencia explícitamente marcada; no deduce independencia mediante búsqueda de palabras. La colección de muestras ya corregida no necesita la reparación histórica; `--retry-errors` existe únicamente para reproducir ese recorrido si hay errores previos. VerificaciónPDF usa Poppler24.02.0. No se ejecutó código de autores. El origen delPDF y el método visual/textual quedan fijados en recibos y proyecciones; no se redistribuye el PDF completo.

## Interpretación y límites

Auditoría documental técnica, con resultado negativo para el mapa explícito pedido; no replicación externa o validación funcional. La independencia reportada y la trazabilidad por biblioteca son niveles distintos de evidencia. Esta revisión acotada no prueba que el mapa no exista en cualquier recurso público. Cerrar esta búsqueda con la carencia precisa; no repetir iguales consultas sin una fuente nueva concreta. Se mantiene bloqueada la inferencia bajo nuestro criterio prospectivo. El conflicto de medio tampoco modifica las cuentas técnicas ya medidas.

El control completo permanece como resultado previo:37.518.164lecturas,72canónicas/0crípticas a15 y38bins concordantes; **no reejecutado ni añadido como réplica nueva**. Su manifiesto histórico se verifica en[commit167d370](https://github.com/luisceb1/ela-research/blob/167d370ed8b8ffd7feeb24b81208f15ed4492d35/reports/gse122069-full-control-20261031/artifact-hashes.json), no contra STATE/BACKLOG editados posteriormente. El manifiesto de esta fase corresponde a sus archivos nuevos y estado actual.

## Siguiente prueba discriminante y vía segura

Como continuación segura del bloqueo, se calculó un **presupuesto prospectivo**, no se procesaron nuevas lecturas. [Tabla](remaining-resource-estimates.tsv): otros cinco suman254.923.387lecturas y8.083.861.911bytes comprimidos. Escalado lineal simple del único control observado:23,5–40,9minporrun; no benchmark de los otros cinco ni garantía de duración/cobertura.

Única tarea siguiente: parametrizar el runner por accession y probarlo con controles sintéticos, conservando exactamente filtros15/8, objetivos, semilla y controles. SinFASTQ nuevo. Para una ejecución futura se propone seleccionar de antemano el siguiente controlSRR8144908,54.292.655lecturas, no cambiarlo por señal. Estimación33,1min; propuesta de límite45min para esa fase nueva, pendiente de revisión antes de ejecutarla. No ampliar el límite30min de una ejecución en curso ni lanzar automáticamente otros runs.

Futura exploración solo técnica/descriptiva mientras el diseño siga sin mapa explícito: no p-valores, PSI molecular, efecto inferencial ni independencia supuesta. El nuevo plan detalla límites y criterio de fracaso. Sin merge/cierre automático; PR30 separado e intacto; sin costes, contactos, publicación externa o laboratorio.
