# ELA Research Lab — MVP 0.1

**Estado: código experimental en PR; no está desplegado ni realiza investigaciones programadas.**

Cuatro funciones secuenciales, implementadas con llamadas diferenciadas al modelo: **literature**, **hypothesis**, **skeptic** y **director**. Operan exclusivamente sobre los metadatos y resúmenes recuperados de PubMed. No constituyen cuatro modelos independientes ni sustituyen revisión humana, validación biológica o investigación clínica.

## Inicio rápido

Solo recuperar bibliografía (sin coste de IA):

~~~bash
python -m agent_lab --preview --query "UNC13A TDP-43 synaptic rescue" --max-papers 5
~~~

Ejecutar las cuatro fases, **solo mediante autorización explícita del operador**, con coste de API:

~~~bash
export OPENAI_API_KEY="your-private-key"
export ELA_LAB_MODEL="gpt-6.1-terra"
python -m agent_lab --live --query "UNC13A TDP-43 synaptic rescue" --max-papers 5 --output reports/agent_lab/local-draft.json
~~~

En PowerShell, sustituir **export** por **$env:OPENAI_API_KEY="..."** y **$env:ELA_LAB_MODEL="..."**. No introducir claves en GitHub ni en los comandos compartidos. Recomendable definir **NCBI_EMAIL** según las directrices de NCBI. **NCBI_API_KEY** es opcional.

Las dependencias del MVP son solo las de la biblioteca estándar Python 3.11+. Los modelos compatibles con Structured Outputs pueden configurarse con **ELA_LAB_MODEL**. Cuatro llamadas por ejecución, sin bucles o reintentos automáticos. El modelo por defecto es `gpt-6.1-terra` (Responses API, Structured Outputs); el adaptador limita cada respuesta a 3.500 tokens de salida, con razonamiento bajo. Debe verificarse la tarifa API vigente antes de ejecutar; la suscripción ChatGPT no incluye crédito API. La primera prueba de extremo a extremo de la API real sigue pendiente de credenciales y aprobación de gasto. La ejecución en modo **--preview** consulta PubMed pero **no** llama a modelos.

Las ejecuciones **--live** guardan además el informe y las hipótesis candidatas en SQLite, por defecto en **data/ela-agent-lab.sqlite** (ignorado por Git). Para inspeccionar memoria local sin red ni coste:

~~~bash
python -m agent_lab --history
~~~

Los informes se guardan como **borradores inmutables** identificados por hash. La memoria es local y no sincroniza contenido con terceros. No equivale a una enciclopedia verificada.

## Primera misión y benchmark (10/11/2026)

Se ha añadido **un corpus de 20 publicaciones indexadas en PubMed** (los preprints están etiquetados como tales), más un conjunto de **20 afirmaciones de control sobre 8 artículos**. Son dos objetos distintos: no confundir veinte artículos con veinte afirmaciones.

~~~bash
# Validación de formatos y claves, siempre offline
python -m agent_lab.benchmark --validate
python -m agent_lab.benchmark --validate-corpus

# Comprobación REAL de metadatos por HTTPS: 8 artículos, o los 20 en grupos 8+8+4
python -m agent_lab.benchmark --source-check
python -m agent_lab.benchmark --check-corpus

# Pruebas offline del evaluador
python -m unittest discover -s tests -p 'test_agent_benchmark.py' -v
~~~

Un workflow específico de PR ejecuta la comprobación bibliográfica, sin modelos de pago. Los controles comprueban únicamente identidad, DOI cuando consta y presencia de resumen. **No demuestran que el etiquetado científico sea correcto.**

**Informe de revisión exploratoria:** [contraste UNC13A por tipo neuronal](../reports/agent-lab/2026-11-10-unc13a-context/REPORT.md). Los dos preprints de septiembre de 2026 (Mallika y Cao) merecen revisión crítica de sus diferencias entre neuronas espinales y del prosencéfalo. No implican eficacia clínica ni una nueva replicación del proyecto.

**Estado de los cuatro agentes:** su código y su test con proveedores simulados están integrados; ejecutar los cuatro de verdad exige clave API, permiso de coste y evaluación manual de sus resultados. No se ha hecho tal ejecución por defecto.

## Garantías y límites

- Solo dos endpoints oficiales NCBI: esearch + efetch; máximo ocho artículos por solicitud, tamaño y tiempo limitados.
- Los PMIDs proceden exclusivamente del resultado de PubMed. Las citas inventadas son rechazadas. La correspondencia PMID **no verifica** que el modelo interprete bien el artículo.
- Se leen AGENTS, STATE, BACKLOG y PROTOCOL con sus SHA256 y contenido acotado. No se modifican.
- No se descargan datos masivos; no se ejecutan estadísticas experimentales, shell, Git, comunicaciones ni tratamientos.
- Las propuestas quedan marcadas **DRAFT_REQUIRES_HUMAN_REVIEW**; nunca como descubrimiento, replicación o eficacia demostrada.
- No se aceptan datos de pacientes ni mensajes privados como fuentes. El sistema remite **solo datos públicos recuperados** a la API del proveedor bajo **--live**.
- Para el MVP hay memoria local SQLite de informes e hipótesis, pero no hay bucle autónomo periódico, memoria vectorial, sincronización editorial ni interfaz web. Esas capacidades dependen de controles y revisiones posteriores.
- Fuentes externas pueden contener instrucciones maliciosas: su contenido se transmite solo como datos y los agentes están instruidos para ignorarlas. Esto no equivale a una garantía absoluta contra prompt injection.

## Pruebas

~~~bash
python -m unittest discover -s tests -p test_agent_lab.py -v
python scripts/run_offline_tests.py --fail-on-skip --report test-results/offline.json
~~~

La segunda orden ejecuta toda la suite del repositorio y necesita las dependencias indicadas en **research/requirements-ci.txt**. Las pruebas del MVP utilizan dobles de PubMed y del proveedor; **no validan llamadas reales ni hallazgos científicos**.

## Desarrollo posterior

1. Evaluar manualmente 20 artículos y las afirmaciones extraídas; medir precisión, trazabilidad y omisiones.
2. Añadir verificador de afirmaciones contra pasajes exactos y deduplicación bibliográfica; conservar solo contenido cuyo uso y licencia estén permitidos.
3. Incorporar memoria con historial versionado de hipótesis e informes, no editar hallazgos anteriores.
4. Habilitar ejecutor bioinformático en sandbox únicamente para una fuente aceptada con protocolo prospectivo y aprobación concreta.
5. Solo después de esas pruebas considerar una tarea periódica bajo límites explícitos de presupuesto, permisos y capacidad de detención.

Referencias técnicas: https://www.ncbi.nlm.nih.gov/books/NBK25497/ y https://platform.openai.com/docs/guides/structured-outputs.
