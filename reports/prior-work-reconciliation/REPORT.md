# Continuidad de otros chats — revisión inicial

Fecha: 29/10/2026. Evidencia: auditoría documental/técnica; resultados científicos de los paquetes **pendientes de reproducción en este repositorio**.

## Qué se había utilizado

Los PR #3–#10 se construyeron con el estado visible, datos públicos descargados y fuentes consultadas expresamente, incluida la copia del manuscrito aceptado de Keuss. No se habían incorporado sistemáticamente los ocho paquetes ZIP y tres propuestas PDF ahora disponibles. No corresponde afirmar que todo el trabajo de los otros chats ya alimentaba esos análisis. La búsqueda de contexto personal de esta sesión recuperó antecedentes; se usa para localizar trabajo y decisiones, nunca como sustituto de las fuentes o del código ejecutado.

## Control ejecutado

`python scripts/inventory_prior_work.py ../upload --output reports/prior-work-reconciliation/inventory.json`

11 paquetes: 8 ZIP, 3 PDF; 114 miembros de ZIP. SHA256 de paquetes y miembros, CRC de todos los miembros leídos; cero errores. No extracción, ejecución de scripts recibidos ni copia de filas de datos al repositorio. No se verifica origen público, autenticidad editorial o validez científica por esta comprobación. El informe JSON es determinista para los mismos bytes de entrada.

Dos grupos de tablas idénticas por SHA256 entre paquetes:

- `resultados_por_caso.csv` del reanálisis inicial = `resultados_por_caso_v1.csv` de splicing.
- `cruce_por_caso.csv` de splicing = `cruce_por_caso_reanalisis_02.csv` de genética.

Esto confirma reutilización de resultados, no una validación independiente. El paquete inicial contiene además un archivo fuente comprimido de GSE126542; su presencia no implica autorización para importar datos individuales. Este ciclo se limita a metadatos, hashes y conclusiones documentales sin tablas por persona ni lecturas alélicas.

## Matriz de continuidad

La lectura fue dirigida: secciones de pregunta, fuentes, resultados resumidos y límites de informes; primera página de cada PDF. No se declara lectura exhaustiva de anexos, auditoría del código recibido ni reproducción numérica. Los siguientes contenidos se atribuyen a los informes, no a nuevos cálculos nuestros.

| Paquete, nombre abreviado | Tipo y contenido declarado | Relación con el trabajo actual | Estado de incorporación |
|---|---|---|---|
| GSE126542 reanálisis real | Expresión génica nuclear, diseño pareado | No equivale a ARN funcional/proteína ni a rescate | Registrado; reproducción pendiente |
| GSE126542 02 splicing | Índices de uniones publicados; reutiliza expresión previa | Misma cohorte; índice UNC13A agrega varias uniones y no es porcentaje molecular absoluto | Registrado; fuente/transformación pendientes de cotejo |
| GSE126542 03 genética | Evidencia alélica de ARN sobre la misma cohorte | No es genotipo de ADN validado; no constituye cohorte independiente | Solo delimitación documental; no importar datos individuales |
| Reanálisis 05 cierre splicing | DEXSeq de GSE121569, fragmentos exónicos anotados | No mide directamente los exones crípticos; antecedentes de rescate ya revisados parcialmente en PR #7–#9 | Evitar repetir extracción como hallazgo; cotejar fuente si se reutiliza |
| 06 cribado péptidos | ARN total y bibliografía de candidatos | ARN total no demuestra péptido/toxicidad. Su bloqueo de acceso GSE310723/315972 es histórico: resuelto por PR #3 | Candidatos registrados; bibliografía/novelty no revalidada aquí |
| 06 CAMK2B validación independiente | Comparación por coordenadas; informe declara unión ausente del catálogo cerebral | Ausencia de modelo no prueba ausencia biológica; no replicación positiva. Misma pareja GEO ya auditada | Resultado negativo previo registrado como declarado; reproducir cotejo agregado antes de usarlo |
| MEA simulador UNC13A | Datos artificiales y pipeline de demostración | Solapa con diseño de rescate diferido de PR #9 | **Simulación**, no evidencia experimental; ejecución pendiente |
| MEA sensibilidad UNC13A | Monte Carlo del simulador; umbrales ilustrativos | No estima potencia/varianza reales ni tamaño muestral experimental | **Simulación**, no validación del ensayo; ejecución pendiente |
| STMN2 propuesta y revisión PDF | Ventana de recuperación después de déficit; piloto conceptual | Pregunta ya desarrollada en otros chats, no nueva de PR #9; cita Chan 2026 como antecedente a revisar | Primera página revisada; integrar requisitos ya definidos |
| UNC13A propuesta y antecedentes PDF | MEA longitudinal y corrector tras déficit | Coincide con separación protección/recuperación de PR #9 | Primera página revisada; propuesta, no protocolo validado |
| UNC13A concept note for Prof Fratta PDF | Propuesta en inglés, calendario ASO DIV14 / KD DIV14 o 33 | Coincide con auditoría Keuss de PR #8; destinatario escrito no autoriza envío | Primera página revisada; no enviada |

## Implicaciones y errores evitados

- Reconocer que el rescate tras déficit documentado ya estaba planteado en los otros chats. El valor del trabajo nuevo es verificar fuentes/calendarios y límites de reanálisis, no reclamar originalidad de la propuesta.
- No sumar expresión/splicing/genética como tres cohortes ni interpretar DEXSeq como medición directa de uniones crípticas.
- No trasladar p-valores o conclusiones de los informes a resultados validados del repositorio. No recalculamos significación en este ciclo.
- La lectura longitudinal de las mismas redes es una elección del diseño MEA. No es un requisito universal para demostrar rescate en cualquier experimento; cohortes paralelas comparables pueden ser adecuadas.
- La anotación histórica de falta de acceso en el cribado no debe volver a bloquear los GEO que ya descargamos.
- El contexto recuperado menciona un reanálisis 04 de GSE121569; no hay paquete 04 autónomo entre estos 11 archivos. No afirmar que fue importado o reproducido. Hay resultados de ese conjunto citados en otros informes.

## Próxima tarea segura

Antes de otra descarga de imágenes: cotejar la fuente primaria Chan 2026, DOI `10.1038/s42003-026-10832-6`, citada por los documentos previos, especialmente cronología de figuras 7/8. El resultado debe ampliar la matriz de evidencia, sin certificar novedad. Si se bloquea, reproducir únicamente la comparación estructural agregada de CAMK2B con los GTF públicos ya cacheados, sin trasladar tablas individuales. Los paquetes sintéticos permanecen separados hasta auditar código y supuestos. No ampliar a inferencia genética individual ni importar datos personales.

Validación del inventario: cuatro pruebas nuevas de límites de entrada/identidad; suite completa en `tests.txt`. Persistir solo esta trazabilidad y el estado en GitHub. Los originales permanecen como entradas proporcionadas por el usuario; el manifiesto permite identificarlos pero no los sustituye. Una reanudación sin esos archivos debe declarar el bloqueo, nunca reconstruirlos desde recuerdos.

## Actualización posterior: una reproducción completada

`reports/camk2b-reproduction` reproduce la comparación estructural agregada CAMK2B con GTF/uniqueCounts públicos fijados por hash. Las predicciones del paquete coinciden:1modelo celular con la unión y32unidades asignadas;0de49modelos cerebrales. Se mantiene la ausencia de modelo como resultado de catálogo, no ausencia biológica. Este pendiente concreto pasa de lectura documental a reproducción técnica; los demás pipelines recibidos permanecen pendientes. `reports/chan-timing` también confirma el antecedente de las propuestas mediante fuente primaria, sin constituir un experimento nuevo.
