# Cola priorizada de investigación

**P0 — Auditoría de GEO** [ejecutada; pendiente revisión PR]
Inventariar GSE310723 y GSE315972: muestras GSM, grupos, profundidad y estructura de uniqueCounts y GTF. Crear diccionario de datos y control de calidad.
Entregado: `reports/geo-audit/` y `scripts/geo_audit.py`; controles técnicos completos, independencia/covariables limitadas por metadatos depositados.

**P0 — Mapeo transcriptos/genes** [estructura ejecutada; revisión y atribución críptica pendientes]
Vincular identificadores de isoformas a GTF, centrado en STMN2, UNC13A y otros transcritos crípticos. Registrar los no asignados.
Entregado: `reports/isoforms/`; cero IDs no asignados según auditoría; un candidato STMN2 no ENST en cultivo. No se ha validado su identidad críptica con coordenadas independientes.

**P1 — Comparación descriptiva de GSE310723** [ejecutada; pendiente revisión PR]
Comparar condiciones experimentales sin p-valores espurios; comprobar profundidad, normalización y alternativas.

**P1 — Consistencia de GSE315972** [sensibilidad descriptiva ejecutada; covariables pendientes]
Analizar distribución entre muestras, sensibilidad a atípicos, replicación y heterogeneidad celular.

**P1 — Evidencia funcional independiente** [pendiente]
Contrastar hallazgos moleculares con experimentos de rescate y métricas de función neuronal publicados.

**P2 — Preparación de colaboración** [pendiente]
Proponer una hipótesis falsable y protocolo mínimo; redactar un correo, pero no enviarlo sin autorización.

Regla antiestancamiento: si una tarea falla por falta de datos o acceso, dejar constancia y avanzar a la siguiente segura. Registrar el estado de cada tarea solo después de producir artefactos comprobables.

## Próxima tarea segura seleccionada (tras estos PR)
1. Verificar coordenadas independientes del evento STMN2 candidato y sus límites de terminación; no atribuir críptico solo por ser no ENST.
2. Auditar semántica y escala de uniqueCounts (GCD=2 en las 12 bibliotecas), con fuente primaria bambu/estudio; no dividir cuentas por suposición.
3. Si estas comprobaciones están bloqueadas, avanzar a evidencia funcional independiente.

Los PR #3 y #4 están abiertos, con CI offline exitosa; los nuevos análisis descriptivos dependen de ambos. No duplicar trabajo leyendo solo main, ni cerrar #1/#2 antes de revisión.
