# Misión 001 — evidencia de rescate funcional de UNC13A

**Estado:** protocolo de revisión bibliográfica propuesto; **sin ejecución de modelos ni análisis biológico**. No reabrir issues #37 o #44 sin nuevas fuentes concretas y aprobación para el trabajo adicional.

## Pregunta

En modelos experimentales con pérdida de función de TDP-43, ¿qué evidencia publicada distingue **prevención de un déficit** de **recuperación de una función neuronal ya alterada** mediante corrección del procesamiento de UNC13A?

## Búsqueda inicial reproducible

Consulta PubMed:

~~~text
(UNC13A[Title/Abstract] OR "UNC13A cryptic exon"[Title/Abstract]) AND (TDP-43[Title/Abstract] OR TARDBP[Title/Abstract]) AND (synaptic[Title/Abstract] OR rescue[Title/Abstract])
~~~

Ejecutar solo una vista previa bibliográfica antes de habilitar el análisis multiagente:

~~~bash
python -m agent_lab --preview --query '(UNC13A[Title/Abstract] OR "UNC13A cryptic exon"[Title/Abstract]) AND (TDP-43[Title/Abstract] OR TARDBP[Title/Abstract]) AND (synaptic[Title/Abstract] OR rescue[Title/Abstract])' --max-papers 8
~~~

Esta búsqueda limitada **no es exhaustiva**: después debe revisarse manualmente la cobertura de autores, preprints y términos alternativos. No permite declarar novedad ni ausencia universal de estudios.

## Extracción que deben contrastar los agentes

1. Identidad exacta del estudio, PMID/DOI, especie y modelo celular.
2. Nivel de intervención: ASO, edición u otro enfoque; cuál es el objetivo molecular.
3. Cronología: reducción de TDP-43, medición de déficit basal, comienzo de intervención, medición posterior.
4. Resultado medido: splicing, ARN, proteína, eEPSC u otro endpoint funcional; no equipararlos.
5. Unidad biológica independiente, cultivo, diferenciación, células técnicas, lotes y controles.
6. Disponibilidad real de valores crudos y claves experimentales (no inferirla de una figura).
7. Alternativas causales, sesgos y resultados nulos.

## Propuesta falsable

**Hipótesis para evaluar, no resultado:** corregir el splicing patológico de UNC13A después de demostrar un defecto sináptico podría recuperar parte de la función neuronal bajo ciertas condiciones.

**Predicción:** en unidades biológicas independientes, medidas basales de déficit y seguimiento posterior, el grupo tratado presenta una recuperación funcional mayor que sus controles temporales adecuados.

**Qué la refutaría o limitaría:** recuperación solo del ARN sin cambio funcional, efecto explicado por el tiempo/cultivo, ausencia de replicación independiente o intervención anterior al déficit que solo demuestre prevención.

## Condiciones para pasar a análisis de datos

- Fuente numérica original nueva, identificada y verificable; no datos simulados como evidencia.
- Mapa célula→cultivo→diferenciación y criterios de exclusión, unidad de análisis y cronología.
- Protocolo prospectivo con controles, umbrales y regla de parada aprobados antes de analizar.
- Revisión humana y autorización específica. No se permiten nuevas descargas masivas ni contacto con autores por continuidad.

## Resultado admisible de esta misión

Un informe crítico con bibliografía verificable, matriz de diseños **preventivo/posdéficit/no determinable**, lagunas documentales y propuesta de siguiente verificación. Nada de ello implica hallazgo terapéutico o beneficio clínico.

Referencias internas: `research/STATE.md`, `research/BACKLOG.md`, `research/PROTOCOL.md`, issues #37 y #44.
