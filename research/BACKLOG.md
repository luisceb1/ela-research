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

## Ciclo siguiente — evento/escala (29/10/2026, pendiente revisión)
- Unión STMN2 de BambuTx9249 coincide exactamente con Figura 5 de Grima 2025 (GRCh38). Identidad de unión contrastada; extremos/transcrito completo/poliA pendientes.
- FullLengthCounts del candidato: 0/0 en controles y 8/12 en KD; medidas depositadas, sin réplica nueva ni independencia de moléculas verificada.
- CPM original auditado: denominador documentado incluye incompatibles; contraste STMN2 conserva dirección.
- Semántica bambu 3.2.6 revisada por commit; causa de uniqueCounts par **bloqueada** sin trazabilidad de entradas/objetos intermedios. No corregir cuentas por suposición.
- **Próxima tarea segura: evidencia funcional independiente publicada**, separar rescate de ARN/proteína/función y auditar temporalidad/controles. No esperar a resolver la escala para revisar literatura funcional.

P1 evidencia funcional: primera auditoría completada con límites de acceso; reports/functional-evidence. Temporalidad neuronal Keuss2024 concurrente; aceptado2026 pendiente texto completo. Próximo: fuente pública alternativa del aceptado y diagrama temporal, sin extrapolar versiones ni eficacia clínica.

Aceptado Keuss: lectura resuelta con copia aportada; MEA con KD tardío no es ASO tardío (14frente33). Tabla de calendario en reports/accepted-keuss. Próximo: evidencia pública de intervención tras déficit verificado y ficha de pregunta discriminante, sin laboratorio ni contacto externo.

P1 reversibilidad: cronología PNAS2025 y ficha conceptual completadas; reports/reversal-design. Próximo inventario Zenodo15346391/unidad experimental y modelo humano2026. Búsqueda dirigida no demuestra ausencia universal de rescate diferido. Sin ejecución de laboratorio ni contacto.

P1 imagen: auditoría TIFF/hoja realizada, reports/image-metadata-qc. Solo4/27calibrados; independencia y enlace longitudinal no resueltos. Próximo suplemento alternativo e inspección visual de par calibrado; no inferencia grupal ni valores físicos imputados a23archivos.

## Ajuste por trabajo de otros chats (29/10/2026)
Prioridad de continuidad: consultar reports/prior-work-reconciliation antes de abrir otra línea. Once paquetes inventariados; revisión documental inicial, no reproducción de sus cálculos. No repetir GSE126542/DEXSeq como descubrimiento ni usar MEA artificial como evidencia biológica. No importar tablas individuales/genotipos.

Próximo: auditar Chan2026 DOI10.1038/s42003-026-10832-6, figuras7/8 y tratamiento respecto a déficit/lesión, ya citado en las propuestas antiguas. Si falla acceso, contraste estructural agregado CAMK2B con GTF públicos cacheados. Imagen Zenodo permanece pendiente después de resolver esta continuidad; no descartada. Paquete04 autónomo no disponible entre estos archivos: localizar solo si hace falta reproducir ese análisis. Los scripts recibidos requieren lectura y reproducción antes de atribuirles controles locales.

Chan2026 temporalidad completada en reports/chan-timing: tratamiento inmediato poslesión y curvas pre/post son antecedentes confirmados. SupData1 recuperada; no identificación de unidades independientes en etiquetas de hojas seleccionadas, tiemposDIV dispersos. Reanálisis jerárquico bloqueado por ese mapa; no fabricar diferenciaciones ni interpolar tiempos. Próxima tarea segura: CAMK2B cotejo estructural agregado para reproducir el resultado negativo previo, sin importar datos individuales. La especificación de rescate tardío reconoce ahora explícitamente Chan; no certifica originalidad.
