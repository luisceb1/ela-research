# Auditoría técnica de prototipos MEA sintéticos

29/10/2026. Relacionado con issue#16. **Evidencia de software, sin datos biológicos ni ensayo experimental validado.** No se generaron gráficos ni se repitieron las7560ejecuciones del MonteCarlo previo.

## Resultado

Se reprodujeron las11pruebas originales (6del prototipo base,5del de sensibilidad). Pasan con el entorno registrado. Sin embargo, seis entradas artificiales inválidas pasan el validador original. Se añadió un control previo independiente que las rechaza y se preservaron los originales por SHA256 para hacer la comparación reproducible.

| Entrada artificial | Validador original | Ejecución posterior original | Control nuevo |
|---|---|---|---|
| Caso válido de demostración | Acepta | Etiqueta recuperación simulada | Acepta solo estructura |
| T0=5,9 con observación en5 | Acepta | Convierte T0 a5; etiqueta recuperación simulada | Rechaza T0 no entero |
| Basal0/1/2 sin ninguna observación válida | Acepta | KeyError al ajustar al basal | Rechaza basal no válido |
| Falta control sano en un tiempo requerido | Acepta | KeyError al buscar referencia | Rechaza cobertura incompleta |
| Estado muerto seguido de observado vivo | Acepta | Produce resumen sin rechazar secuencia imposible | Rechaza reversión del estado muerto |
| Viabilidad1,5 en escala declarada0–1 | Acepta | Etiqueta recuperación simulada | Rechaza dominio inválido |
| Solo brazo tardío sin control del mismo bloque | Acepta | ValueError al resumir | Rechaza brazo faltante |

Las etiquetas de la tabla son resultados de una **fixture artificial diseñada para ejercitar código**, no evidencia de función recuperada. No se estiman magnitudes terapéuticas. La fixture válida usa un solo bloque por simplicidad: no permite inferencia experimental.

## Otro defecto: denominador de bloques en sensibilidad

Con `Config(technical_missing=1.0, mortality_hazard=0.0)`, escenario nulo y semilla13, el prototipo informa `n_analyzable_blocks=8`, aunque ninguno de los cuatro contrastes medios es finito. La etiqueta de recuperación queda falsa, pero8describe registros de bloque formados, no bloques con contraste analizable. El código abandona la estimación al detectar insuficientes valores finitos; **no** debe interpretarse la etiqueta falsa como evidencia contra recuperación.

No se corrigió silenciosamente ese campo en el archivo histórico: se conserva y documenta el contraejemplo. Antes de reutilizar resultados deben distinguirse bloques formados, válidos por contraste y válidos para la intersección de los cuatro contrastes. El control nuevo rechaza un brazo×bloque×desenlace enteramente perdido por fallo técnico; no lo convierte en0 ni en resultado negativo.

## Qué cubren las pruebas y qué no

La base revisada genera historia antes de asignación y aleatoriza por diferenciación/T0 en pares ordenados por déficit. Los pozos huérfanos quedan fuera de la comparación. El resumen promedia por diferenciación; los pozos/electrodos no se cuentan automáticamente como diferenciaciones. Las pruebas comprueban estos aspectos en sus escenarios simulados, no en un experimento real.

El prototipo de sensibilidad usa contrastes entre diferenciaciones y una regla conjunta de medias y límites inferiores unilaterales. Que esa regla se ejecute correctamente en ejemplos no valida sus supuestos ni su calibración en datos reales. En el escenario llamado nulo, el código aún añade una respuesta aleatoria por diferenciación con media0: es un efecto medio nulo simulado, no necesariamente ausencia exacta de efecto en cada bloque. Las pérdidas informativas dependen del estado latente; calcular medias con datos disponibles no elimina su posible sesgo.

Los contadores de muerte de sensibilidad pueden contar al mismo pozo en+3y+4; son observaciones de seguimiento, no muertes únicas. En ambos prototipos, muerte se codifica0 para el desenlace compuesto elegido y falta técnica sigue ausente. Ese0 no es una medición observada de sincronía. Índices+3/+4 no son días; umbrales0,19/0,60/0,06 son supuestos de demostración y no criterios clínicos ni calibraciones de laboratorio.

## Cambio entregado

- `research/prototypes/mea_synthetic`: cinco fuentes originales byte por byte, manifiesto de procedencia de los dos ZIP y versiones usadas. No se importaron datos individuales, CSV sintéticos, figuras ni consolidadores. Los consolidadores y generadores de informes con efectos al importar se leyeron/inventariaron pero no se ejecutaron.
- `scripts/audit_mea_software.py`: verifica hashes, reproduce tests en procesos separados y contrasta las seis entradas adversas. Solo llama al núcleo revisado; no llama CLI de simulación, gráficos o escritores de informes históricos.
- `scripts/mea_input_qc.py`: control estructural para fixtures explícitamente sintéticas. Comprueba tiempos/T0 finitos enteros, basal/screening, referencia sana, constancia de brazo/unidad, estados, viabilidad, absorción de muerte y soporte de desenlaces por bloque/brazo.
- Ocho pruebas nuevas en suite estándar, con subcasos adversos:85pruebas del repositorio pasan. **No confundir** estas85con las11pruebas originales, que se ejecutan por separado y necesitan las dependencias científicas registradas.

El control nuevo es una API separada: no se ha conectado automáticamente a los CLI originales, que permanecen como archivo histórico y no deben ser usados como importadores reales. Aceptar una estructura sintética no verifica elegibilidad biológica, métrica de sincronía, cegamiento, dosis, número de diferenciaciones independientes ni eficacia. No se habilita una vía de análisis clínico/experimental.

## Reproducción e incidencias

Plan previo: research/plans/2026-10-29-mea-software-audit.md. Comando `python scripts/audit_mea_software.py`; suite estándar `python -m unittest discover -s tests -v`. Resultado estructurado y entorno en audit.json/environment.json. Las semillas originales permanecen en las fuentes fijadas; fixtures adicionales usan42para20remuestreos puramente técnicos y13para el caso extremo de sensibilidad. Repetición del audit.json idéntica por bytes; logs de duración no se consideran deterministas.

`tabulate` no está instalado: solo lo necesitaría la salida Markdown del generador de informe, que no fue ejecutada. No se instalaron dependencias. No hubo fallos inesperados de las suites; los KeyError/ValueError de la tabla son contraejemplos reproducidos y registrados, no resultados ocultados.

## Continuidad con main y siguiente tarea

Durante esta auditoría se detectaron actualizaciones concurrentes de main y las issues14–21. Se leyeron nuevamente AGENTS, PROTOCOL, STATE y BACKLOG remotos; no se sustituye el estado de las ramas pendientes por main ni viceversa. El presente PR amplía el trabajo de las ramas#3–#13 y cubre parcialmente issue16; no la cierra ni acredita un protocolo listo para laboratorio.

Prioridad siguiente: reconciliar main con los informes/controles ya producidos y comprobar el P0#19 sobre selección de genes sin gene_name, revisando el script y el run actuales antes de repetir análisis. Después resolver P0#20 (21frente a1910uniones) con el paquete original y criterios exactos, sin mezclar filtros. Las deficiencias MEA de completitud y denominadores quedan registradas para corregir antes de cualquier reutilización; no justifican nuevas simulaciones masivas ni un ensayo. Sin fusión automática, envío de mensajes, gasto o laboratorio.
