# Chan2026: tratamiento posterior a lesión y seguimiento previo ya publicados

Fecha de auditoría: 29/10/2026. Fuente: Chan et al., DOI `10.1038/s42003-026-10832-6`. Texto editorial publicado el 10/10/2026 como artículo aceptado/in press, sujeto a edición; no denominarlo versión final. PDF editorial completo recuperado desde el enlace `_reference.pdf` de la página oficial. Caché fijada por SHA256 en `sources.json`.

**Resultado:** se confirma un antecedente directo de ASO STMN2 inmediatamente después de axotomía y otro de crecimiento de neuritas registrado antes/después de administrar ASO. Ni «tratar después de lesión» ni «seguir las mismas culturas antes/después» justifican por sí solos originalidad de nuestra propuesta. No verificamos un brazo de inicio retrasado seleccionado prospectivamente tras dos mediciones deficitarias ni una comparación de múltiples demoras desde ese criterio. Esto es una delimitación de lo revisado, no prueba de ausencia de antecedentes.

## Evidencia de la fuente primaria

| Experimento | Orden de eventos | Desenlace | Replicación declarada |
|---|---|---|---|
| Figura7f/g, PDF p12 | Dosis única DIV4; curvas incluyen periodo anterior y posterior | Longitud de neuritas/área de cuerpos celulares | N=3 experimentos; n=3–5 pozos |
| Figura7h/i, PDF p12 | Dosis DIV4 y DIV7; mismo inicio que dosis única | Misma lectura longitudinal morfológica | Mismo conjunto de figuras; no contarlo como otra cohorte independiente |
| Figura8a–c, PDF p13 | Axotomía DIV14 → ASO inmediatamente después → inmunotinción 3d después | Regeneración axonal normalizada por área somática y señal STMN2 | N=2 experimentos; n=3–5 chips; al menos3 campos/chip |

DIV17 para la lectura de Figura8 se calcula como14+3; el retraso exacto en horas/minutos entre lesión y ASO no se especifica y queda nulo. Tres días es el seguimiento al desenlace, **no** una demora antes de empezar tratamiento. Una segunda dosis DIV7 tampoco equivale a un brazo cuyo tratamiento comienza DIV7.

Control: TDP-43WT con ASO control, TDP-43ΔNLS con ASO control y TDP-43ΔNLS con ASO10. Figura7 incorpora ARN críptico/completo, inmunotinción de proteína y viabilidad; la curva funcional examinada es morfológica, no tráfico lisosomal ni MEA. Las curvas y flechas se comprobaron visualmente en PDF p12; no se digitalizaron puntos ni se estimaron efectos. El panel7n de KD adicional tiene otro calendario y no se le asignan automáticamente los de7f–i.

El método general de regeneración (p15) describe recuperación10d, compatible con el experimento de caracterización de Figura1; Figura8 especifica3d. Conservamos ambos localizadores y usamos el pie específico para Figura8, sin sustituirlo por10d.

## Qué significa el basal previo

La Figura7 muestra una trayectoria de crecimiento menor en el modelo mutante y lectura antes de DIV4. No corresponde etiquetar todo el estudio como preventivo sin medición previa. Tampoco esa diferencia morfológica demuestra que cada cultivo haya perdido una función adquirida: crecimiento menor durante maduración, regeneración después de lesión y reversión de un deterioro longitudinal son preguntas distintas. La mutación de localización nuclear existe desde la línea celular; no se conoce un día de inicio agudo de la perturbación que pueda restarse a DIV4.

Lo que sigue pendiente es establecer operacionalmente un déficit funcional pretratamiento y comparar demoras desde ese punto, con controles temporales, persistencia de perturbación y supervivencia. La propuesta STMN2 del otro chat ya reconocía estos antecedentes: este ciclo confirma y precisa esa lectura, sin atribuirnos una pregunta nueva. No se certifica novedad del contraste más estrecho.

## Unidad experimental y sesgos

- Método p17: observaciones celulares proceden de pozos tratados independientemente de la misma o distintas placas y del mismo clon. N se define como experimentos independientes en los pies; **no equivale automáticamente a diferenciaciones independientes**, donantes o fondos genéticos diferentes.
- El modelo compara una línea editada heterocigota ΔNLS con control isogénico. La identidad y generación de clones están descritas en p14; no se extrajeron datos clínicos de personas.
- Reporting Summary p2, leído por OCR y cotejado visualmente: asignación aleatoria declarada; investigadores conocían grupos durante adquisición/análisis; no cálculo formal de tamaño muestral. Se registran exclusiones por pérdidas de tinción o adquisición no analizable. No convertimos esa declaración en comprobación independiente del procedimiento.
- No se recalculan p-valores del artículo, no se convierten campos/células/pozos en réplicas biológicas y no se deriva eficacia clínica. Las afirmaciones clínicas de la discusión quedan fuera de esta auditoría experimental y no se adoptan como conclusión.

## Fuente cuantitativa: disponibilidad y límites iniciales

Se descargó Supplementary Data1 (`MOESM3_ESM.xlsx`,434970bytes), solo lectura XML sin macros ni fórmulas ejecutadas. Contiene83hojas; se auditaron metadatos de7f–i y8b/c. `audit.json` conserva etiquetas y conteos de celdas numéricas por columna; **esos conteos no son n biológicos**. No se reexportan aquí los valores de respuesta.

Las hojas de7f–i contienen etiquetas DIV dispersas en columnaA (no un tiempo explícito en cada fila); no interpolamos automáticamente tiempos faltantes. Las columnas de respuesta están agrupadas por condición pero las etiquetas seleccionadas no identifican experimento/diferenciación/pozo. En8b/c hay5valores por condición, que no se reinterpretan como5diferenciaciones ni sustituyen N=2 experimentos del pie. Se necesita resolver el enlace entre unidades y las filas/columnas antes de un análisis jerárquico.

## Modelo y UNC13A: no transferir el fenotipo

La discusión p11 y Supplementary Figure6 describen ausencia del evento críptico UNC13A basal en este modelo de pérdida nuclear parcial; KD adicional de TDP-43 induce el evento. No asumir que un sistema válido para STMN2 reproduce el déficit de UNC13A de Keuss. Un piloto UNC13A exigiría confirmar su ARN/proteína y el déficit funcional específico bajo la perturbación elegida. Añadir KD cambia la condición experimental y requiere caracterización; no queda autorizado ningún ensayo.

## Reproducción, errores y siguiente paso

Plan previo: `research/plans/2026-10-29-chan-timing.md`. `python scripts/audit_chan_timing.py` extrae tiempos explícitos de pies por Poppler y metadatos XLSX con Python estándar. Los números N/n son transcripción manual verificada visualmente, identificada como tal. `null` significa dato no verificado, no ausencia demostrada.

Se preservan los fallos de acceso/extracción en `errors.json`. El primer parser falló ante la palabra de inmunotinción dividida por guion entre líneas: corregido con normalización y prueba de regresión. La suite técnica pasa; no valida el experimento ni sus conclusiones. El informe no es revisión sistemática ni reanálisis de datos experimentales.

Siguiente tarea segura: comparación estructural agregada CAMK2B con los GTF públicos ya auditados para reproducir el resultado negativo declarado en el paquete del otro chat, sin tablas individuales. El reanálisis de curvas Chan queda condicionado a resolver identidad de unidades y tiempos por fila; no suplirlos por el número de columnas. No descargar imágenes masivas para resolver una pregunta que ya cuenta con este antecedente documental.
