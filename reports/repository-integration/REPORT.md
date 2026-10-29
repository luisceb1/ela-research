# Consolidación de las dos cadenas de investigación — 29/10/2026

## Evidencia

Luis autorizó revisar y consolidar el trabajo en main tras el balance de ramas. Se fija main en `13ccbc5c9f1c9744c57ed9abb822d169772e32a5`, la cadena PR3–13/#22 en `e3ca351d5bf79430abf283b12f65862e363bc707` y PR23–25 en `963b176436907be0ba265bd2ff9c4a2f2e05d45a`. Las 15 cabezas de PR y la selección de blobs están en inputs.json. La cadena antigua había divergido de main: 13 commits propios frente a 33 del otro lado; la reciente era descendiente de main.

Se reunieron 231 rutas de entrada. 222 se conservan idénticas por hash Git, incluidos todos los scripts, tests y tablas existentes. Ocho documentos/workflow se modifican explícitamente y un workflow offline duplicado se retira. AGENTS.md y PROTOCOL.md conservan sus blobs remotos originales. No se importan datos nuevos ni se reejecutan análisis científicos.

Suite conjunta: **105 tests pasan en Python 3.12.14**, y compilación Python sin errores. Son 85 de la cadena antigua más 24 de la reciente menos cuatro compartidos. No se suman como 109 ni como réplicas experimentales. CI del PR comprobará 3.11 y 3.12; resultado remoto se consulta en Checks, no se presume a partir de esta ejecución local.

## Resoluciones

- Seis rutas comunes difieren entre cabezas: daily.yml, README, informe diario PubMed, BACKLOG, STATE y seen_pubmed_ids. Se conservan daily.yml y snapshots de vigilancia del lado reciente. README/STATE/BACKLOG se reescriben con ambas líneas y los bloqueos actuales.
- MASTER_EVIDENCE se actualiza: mapeo, CAMK2B estructural, software MEA y parser ya tienen entregables; GSE126542/GSE121569, genética/péptidos y catálogo de autores mantienen sus pendientes explícitos.
- Notas en informes geo-audit/descriptive separan etiquetas depositadas de los grupos cognitivos corregidos. No se modifican tablas ni se recalculan efectos por grupo. La propuesta UNC13A v0.3 enlaza las auditorías posteriores Keuss/Chan sin declararse validada.
- Se unifica CI offline en tests.yml, matriz 3.11/3.12 para PR y push a main. isoseq-tests.yml se sustituye por esa misma cobertura completa, evitando duplicación de jobs. El workflow de auditoría GEO real y la vigilancia diaria se conservan.
- El commit de integración usará main y ambas cabezas como padres; un merge posterior debe conservar el grafo. No usar squash/rebase que convierta la incorporación de antecedentes en una copia sin su historia.

## Interpretación y limitaciones

Integrar código/documentos mejora continuidad; no aporta evidencia biológica, nueva revisión científica externa o certeza de originalidad. Los informes históricos conservan el contexto de su ejecución y pueden describir pendientes ya resueltos; STATE y MASTER_EVIDENCE son el punto de continuación actual. La lista antigua de 21 no recupera validez por quedar archivada en main.

No se cierran issues científicas automáticamente. Las ramas originales solo se consideran incorporadas tras comprobar ancestry remoto y PR; no se sobrescriben. El conector disponible no expone borrado de ramas: se conservarán las referencias históricas si no hay mecanismo autorizado, sin presentarlas como líneas activas de trabajo.

## Verificación y continuación

inputs.json: fuentes y procedencia de cada blob; validation.json: resoluciones y preservación; tests.txt: suite conjunta; errors.json: incidencias operativas. Reproducción del chequeo técnico: `python -m unittest discover -s tests -v` y `python -m compileall -q scripts tests`. Las fuentes/versiones científicas siguen en los manifiestos de cada análisis.

Antes de merge: comprobar checks sobre el SHA exacto del PR y revisar que main no cambió. Después: verificar blobs, ancestry de las 15 cabezas y estado de PR; registrar resultado y actualizar Work. Mantener nuevas ramas breves desde main. Próxima tarea científica: descripción/esquema de los 17 suplementos Bolger/crypTE y convenciones antes de cruzar el catálogo de autores.

## Comprobación posterior al merge

PR #26 integrado como 2c0ef89207e81194f6d167f4ef3b01929a672f82, con el árbol 709936bcd7b83598db9ae9cd899f8f52fa2c100b idéntico al validado. Se verificaron los 236 archivos remotos y ancestry de las 15 cabezas. Los cuatro checks del SHA exacto fueron exitosos: 105 tests en cada versión Python 3.11/3.12, auditoría de uniones (1910, filtros 9/100/0) y mapeo GEO (11/10 modelos diana). No son nuevas réplicas ni descubrimientos.

GitHub marcó #3/#23 como merged por ancestry. Los otros 13 PR dependientes se cerraron con nota de incorporación mediante #26, sin afirmar merge individual. Ninguna issue científica se cerró. Las 15 ramas originales permanecen como referencias históricas por limitación del conector; no constituyen tareas pendientes. Este checkpoint documental actualiza el estado posterior sin cambiar scripts o resultados.
