# Contrato paired-end sintético — 02/11/2026

## Evidencia

Implementado scripts/pe_fragment_contract.py, separado del extractor SE histórico. Pasan17tests locales con PySAM0.23.3/HTSlib1.21;22comparaciones de decodificación textual frente a HTSlib coinciden exactamente en eventos y contadores. Los controles tienen expectativas explícitas, no solo comparación de un parser con otro. No se ha ejecutado alineador, descargado FASTQ o restaurado índice humano.

Unidad: fragmento por unión y biblioteca. Un par que apoya la misma unión desde ambos mates aporta uno; distintos eventos del mismo par se conservan. Se separan biblioteca, RG y QNAME. Se comprueban dos primarios, roles read1/read2, referencias/posiciones/flags de mate recíprocos, orientación física inward-FR, proper-pair, NH=1y20≤MAPQ<255. Los duplicados marcados se conservan y etiquetan, sin afirmar deduplicación molecular.

Los controles incluyen apoyo doble/único, XSnegativa, eventos distintos, anclas14/15y8, bloques M/= /X contiguos, inserción que interrumpe ancla, huérfano, primario extra, secundarios/suplementarios, NH/MAPQ/QC-fail, roles/orientación/reciprocidad incorrectos, XSausente o conflictiva, duplicación marcada y aislamiento por RG/biblioteca. Orden fuera de contrato y grupos de más de16registros provocan error, no una tabla aparentemente válida. Los cromosomas/posiciones de fixtures son artificiales: no definen UNC13A.

## Alcance de la independencia

El primer decodificador usa texto SAM y regex CIGAR; el segundo usa registros y códigos CIGAR de PySAM/HTSlib. **La política de selección de pares y la reducción por fragmento se comparten.** La concordancia valida dos rutas de lectura/extracción, no dos algoritmos completamente independientes de filtrado. Las expectativas de tests de selección cubren esa política común. No se ejecutaron HISAT2ni controles biológicos; no se acredita la semántica efectiva del SAM que genere ese alineador en producción.

Se exige entrada lexicográficamente agrupada por(RG,QNAME), con biblioteca explícita. El consumo del núcleo se limita a un grupo de hasta16registros. La colación/ordenación externa de SAM real aún no está implementada o medida: debe incluirse en el presupuesto de disco/tiempo antes del piloto. No se declara que un SAM cualquiera de HISAT2sirva directamente. El extractor SE anterior se conserva sin modificar; no se ejecutó su suite local completa en este entorno.

## Reproducibilidad

Plan escrito antes de implementar: research/plans/2026-11-02-pe-synthetic-contract.md. Fixtures generadas por tests/test_pe_fragment_contract.py; resultados por fixture/ancla en results.json, salida de tests y versiones/hashes en validation.json. Instalada únicamente la dependencia de análisis PySAM0.23.3en directorio temporal separado del repositorio; descarga de rueda≈24MB. Sin instalación de alineador. Dependencia fijada en research/requirements-pe-contract.txt.

CI estándar puede omitir la comparación HTSlib si no tiene PySAM; por ello se añade un workflow específico paired-end-tests.yml que instala el pin y ejecuta estos17tests en Python3.11/3.12. La CI completa se comprobará por la cabeza nueva. Tests y fixtures no son lecturas biológicas o nuevas réplicas.

## Limitaciones y siguiente prueba

El contrato computacional sintético está ejecutado. **El piloto real sigue sin estar listo.** Faltan: definición molecular y convenciones de las uniones UNC13A cotejadas con referencia; orientación transcriptómica real de la biblioteca; prueba end-to-end del alineador y colación bajo límites. Una biblioteca descrita como strand-specific no fija por sí sola FR/RF, y los flags físicos de los mates no sustituyen XSni documentación de protocolo.

Única siguiente tarea propuesta: puerta de referencia/orientación UNC13A, solo fuentes primarias pequeñas y contratos sintéticos; no instalar índice humano o descargar los6,35GB. Fijar ensamblaje, hebra, coordenadas canónica/críptica y prueba explícita de la orientación de biblioteca. Si no se puede demostrar FR/RF, preparar y evaluar un contrato unstranded explícito antes de datos reales; nunca elegir orientación por maximizar soporte o efecto. Las búsquedas cerradas de alias SH-SY5Yy el compendio agregado no se repiten.

La fase no acredita PSI, efecto de KD, rescate, independencia experimental o beneficio clínico. PR36sin merge automático, costes externos, contactos o laboratorio.
