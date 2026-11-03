# Próxima reproducción descriptiva STMN2, aún no ejecutada

Pregunta: ¿reproduce la tabla de abundancias por grupo de exones finales la PPAU de STMN2 publicada por los autores para las mismas doce bibliotecas?

Datos ya aceptados: Zenodo15538003, miembro Humphrey `summarised_pas_quantification.counts.tsv`, SHA2565b25fdea528e99ba647fd20b0d5f4ca5aab401d0e373df131bdc2145ded1a296. Dos grupos STMN2: ENSG00000104435.14_1 y _2. Anotación curada: _1 como ALE críptico; _2 contiene transcritos de referencia. No convertir los múltiples extremos de cada grupo en eventos únicos de corte ni moléculas.

Estimando prospectivo: para cada biblioteca, abundancia estimada _1 / suma de abundancias de **todos** los grupos cuyo gene_id sea ENSG00000104435.14. Verificar que la tabla contiene todos los grupos del gen y ninguna columna repetida; si el denominador es cero, producir indeterminado, no cero. Es uso relativo de grupos de exones finales bajo el modelo PAPA/Salmon, no PSI de uniones, moléculas independientes ni recuperación de función.

Predicción falsable: la proporción coincide con la PPAU original (miembro del mismo directorio `summarised_pas_quantification.ppau.tsv`) para cada etiqueta explícitamente enlazada a GEO. Primero comprobar si la unidad de esa tabla es proporción o porcentaje. Tolerancia absoluta1e-6 tras armonizar unidades; no cambiarla al ver discrepancias. La coincidencia solo certifica reproducción aritmética del mismo resultado, no validación experimental independiente.

Método: recuperar solo el miembro PPAU por Range206 con límites, CRC y SHA; sin ZIP entero, crudos ni tablas post mortem. Exportar tabla por biblioteca con numerador/denominador/proporción/autores/diferencia/criterio. No seleccionar bibliotecas por profundidad o por efecto; no inferir pares de sus números. Sin medias de grupos, p-valores, efectos inferenciales ni afirmación de novedad. Preservar y explicar discrepancias entre índices de anotación/medición.

Cierre: tabla por biblioteca reproducida, discrepancia documentada o bloqueo del enlace. Si falla identidad, denominador o tolerancia, detener sin ajustes retrospectivos. El mapa de diferenciaciones/lotes sigue siendo necesario antes de modelar incertidumbre entre unidades biológicas. Esta próxima fase no se ejecutó durante la auditoría de diseño.
