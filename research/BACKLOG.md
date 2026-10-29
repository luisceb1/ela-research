# Cola priorizada de investigación

**P0 — Auditoría de GEO** [ejecutada; pendiente revisión PR]
Inventariar GSE310723 y GSE315972: muestras GSM, grupos, profundidad y estructura de uniqueCounts y GTF. Crear diccionario de datos y control de calidad.
Entregado: `reports/geo-audit/` y `scripts/geo_audit.py`; controles técnicos completos, independencia/covariables limitadas por metadatos depositados.

**P0 — Mapeo transcriptos/genes** [estructura ejecutada; revisión y atribución críptica pendientes]
Vincular identificadores de isoformas a GTF, centrado en STMN2, UNC13A y otros transcritos crípticos. Registrar los no asignados.
Entregado: `reports/isoforms/`; cero IDs no asignados según auditoría; un candidato STMN2 no ENST en cultivo. No se ha validado su identidad críptica con coordenadas independientes.

**P1 — Comparación descriptiva de GSE310723** [pendiente]
Comparar condiciones experimentales sin p-valores espurios; comprobar profundidad, normalización y alternativas.

**P1 — Consistencia de GSE315972** [pendiente]
Analizar distribución entre muestras, sensibilidad a atípicos, replicación y heterogeneidad celular.

**P1 — Evidencia funcional independiente** [pendiente]
Contrastar hallazgos moleculares con experimentos de rescate y métricas de función neuronal publicados.

**P2 — Preparación de colaboración** [pendiente]
Proponer una hipótesis falsable y protocolo mínimo; redactar un correo, pero no enviarlo sin autorización.

Regla antiestancamiento: si una tarea falla por falta de datos o acceso, dejar constancia y avanzar a la siguiente segura. Registrar el estado de cada tarea solo después de producir artefactos comprobables.
