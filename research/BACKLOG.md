# Cola priorizada de investigación

**P0 — Auditoría de GEO** [inventario y enlace técnico ejecutados; revisión/integración pendientes]
Inventariar GSE310723 y GSE315972: muestras GSM, grupos, profundidad y estructura de uniqueCounts y GTF. Crear diccionario de datos y control de calidad.

**P0 — Mapeo transcriptos/genes** [STMN2/UNC13A ejecutados por ENSG; controles reforzados, pendiente revisión]
Vincular identificadores de isoformas a GTF, centrado en STMN2, UNC13A y otros transcritos crípticos. Registrar los no asignados.

**P1 — Comparación descriptiva de GSE310723** [pendiente]
Comparar condiciones experimentales sin p-valores espurios; comprobar profundidad, normalización y alternativas.

**P1 — Consistencia de GSE315972** [pendiente]
Analizar distribución entre muestras, sensibilidad a atípicos, replicación y heterogeneidad celular.

**P1 — Evidencia funcional independiente** [pendiente]
Contrastar hallazgos moleculares con experimentos de rescate y métricas de función neuronal publicados.

**P2 — Preparación de colaboración** [pendiente]
Proponer una hipótesis falsable y protocolo mínimo; redactar un correo, pero no enviarlo sin autorización.

Regla antiestancamiento: si una tarea falla por falta de datos o acceso, dejar constancia y avanzar a la siguiente segura. Registrar el estado de cada tarea solo después de producir artefactos comprobables.

## Continuación tras reconciliar issue19 (29/10/2026)
reports/mapping-positive-controls confirma que la selección cero ya se corrigió en main y reproduce11/10modelos con fuentes fijadas. Se corrige la prueba que no se descubría y se añade fallo ante salida vacía/conflictiva. Resultados concordantes con PR4; no representan otra réplica.

Próximo P0: issue20, recuperar ZIP original del cribado y explicar21vs1910mediante filtros explícitos. No duplicar la corrección ENSG ni la de ALS-CI ya ejecutadas; verificar siempre su estado actual. Leer PR3–13/#22además de main para conservar los análisis pendientes. MEA sigue siendo simulación/software, y las propuestas requieren laboratorio autorizado para validarse. No cerrar issues o fusionar automáticamente.

## Reconciliación issue20 ejecutada
reports/junction-filter-reconciliation recupera ZIP y reproduce21claves: parser consecutivo fragmenta exones/referencias.1910reproducidas con agrupación,1901con soporte positivo;3de las21eran referenciaENSTy18se conservan. No usar lista21como cribado exhaustivo o evidencia de novedad.20tests pasan; proyección estructural sin filas personales y extractos de código quedan por hash.

Siguiente tarea segura: anotar1901contraGENCODEv47completa y catálogo público del estudio antes de priorizar candidatos/AGRN#21. No nueva búsqueda por fuerza bruta ni inferencia con n=1. Cierre de#20e integración de PR requieren revisión; revisar también estados de ramas anteriores.
