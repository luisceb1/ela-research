# Plan prospectivo FR-K26-4d v1

Fecha: 03/11/2026. Estado: **seleccionado, bloqueado por datos**. Este plan se fija antes de obtener valores individuales. No autoriza laboratorio ni otro experimento alternativo.

## Pregunta y estimando

¿El ASO M21-6 aumenta la magnitud de eEPSC frente a TDP-43 KD en motoneuronas espinales del experimento K26 Fig.4d? Es reproducción de una intervención concurrente, no reversión iniciada posdéficit. Se elige este panel por disponer de tres brazos, tres diferenciaciones y tipo neuronal espinal; Fig.4a/b no proporciona control sano dentro de cada contraste de ASO y Fig.4e tiene conflicto de tratamiento en Table6. Fig.4g es una alternativa descartada en esta fase para evitar selección posterior de endpoint.

Los autores informan 34 células control, 30 KD y 25 KD+M21-6 (89 total) en tres experimentos/diferenciaciones. El n de análisis biológico no es 89. Gapmer TDP-43 y M21-6 empiezan en paralelo DIV45, 2–4 μM, semanal durante tres semanas; registro una semana después de última dosis. Métodos de autapsis indican DIV60–70: no convertirlo en día único por inferencia aritmética si falta el metadato de cada registro (pp.20–21,27,45,62).

## Condiciones de aceptación

1. Archivo numérico original, versión, licencia/acceso, URL y SHA256; no puntos digitalizados.
2. Identificadores y mapa de independencia revisados; separación de diferenciación, cultivo, coverslip, célula y medición. Tres brazos por diferenciación según contrato v1, sin fabricar claves. Un diseño real distinto exige enmienda prospectiva antes de analizar efectos.
3. Unidades, convención de signo y procesamiento claros; excluir por protocolo, no por magnitud favorable. Conservar todos los IDs, exclusiones y discrepancias con 34/30/25.
4. Dosis/días/replicados comparables; diferencias se modelan o invalidan el contraste, no se ocultan al promediar.
5. Describir pérdida de TDP-43 y controles de registro; obtener resistencia serie/QC y explicación de exclusiones cuando disponibles. No exigir RNA y eEPSC de la misma célula.

## Análisis cuando se supere la puerta

- Exportar tabla de todas las células y tabla por diferenciación/condición con n, media, mediana y dispersión. Promediar repeticiones técnicas dentro de célula antes de comparar grupos. No ponderar una diferenciación por tener más células registradas.
- Reproducir el modelo publicado en **R**, no sustituirlo silenciosamente por OLS: magnitud no negativa en la unidad original, `log1p(value) ~ condition + (1|differentiation)`; REML, lme4/lmerTest, referencia KD y contrastes Satterthwaite. Si las claves revelan cultivos adicionales anidados, revisar jerarquía antes del ajuste. Fijar versiones y guardar sessionInfo/diagnósticos. El código exacto espinal/modelo debe verificarse con los datos; no se presume que macro MATLAB de otro laboratorio sea el usado aquí.
- Primario: contraste ASO−KD en escala transformada con estimación e intervalo; secundario control−KD. Declarar multiplicidad, diferencias con el script original y no seleccionar transformación por p-valor. Informar convergencia y ajuste singular; tres niveles de lote limitan estimación de varianza.
- Sensibilidades predefinidas: diferencias entre medias por diferenciación con igual peso; dirección por bloque; exclusión de una diferenciación cada vez como fragilidad, no n adicional. Gamma solo para valores estrictamente positivos y si su soporte es adecuado. No añadir constante a ceros para forzar Gamma.
- Fracción de déficit recuperado descriptiva: `R=(ASO−KD)/(control−KD)` con medias de diferenciaciones de igual peso. No recortar a [0,1]; no informar R si no hay déficit positivo interpretable o si su denominador es inestable. Informar también unidades absolutas. R cercano a 1 o p>0.05 frente a control **no demuestra equivalencia ni rescate completo**; necesitaría margen de equivalencia justificado previamente y precisión suficiente.
- Comparar estimación con datos/estadística publicada; toda discrepancia se rastrea a versión, escala, exclusiones o modelo. No ajustar el pipeline para coincidir con la conclusión.

Predicción refutable: el contraste ASO−KD debe ser favorable; si dirección/magnitud difiere del original tras validar datos y modelos, registrarlo. Resultado incierto con tres diferenciaciones no refuta por sí solo función de UNC13A. No análisis causal de mediación, correlación RNA/función o comparación Keuss–Guo sin diseño y datos nuevos específicos.

## Qué está ejecutado ahora

`scripts/check_functional_rescue_input.py` es solo un validador de entrada: procedencia/hash, declaración de revisión de independencia, tres brazos y unidades independientes, IDs, unidades, valores finitos y recuentos esperados. No calcula efectos ni potencia. El contrato deshabilitado produce NO-GO; las pruebas usan archivos mínimos artificiales explícitos. El LMM, R y estimaciones **no están ejecutados ni implementados** porque no se han inspeccionado los datos. Implementarlos tras la puerta evita prometer compatibilidad con una tabla desconocida.

Comando reproducible desde raíz:

```bash
python scripts/check_functional_rescue_input.py --contract reports/functional-rescue-20261103/input_contract.json --output reports/functional-rescue-20261103/input_gate.json
python -m unittest discover -s tests -p 'test_functional_rescue_input.py' -v
```

El primer comando devuelve 2 cuando la puerta está cerrada; es un bloqueo esperado, no un resultado experimental negativo. Cerrar este ciclo sin búsquedas automáticas adicionales. Reabrir solo con un archivo fuente nuevo verificable; no contactar o solicitar acceso sin autorización.
