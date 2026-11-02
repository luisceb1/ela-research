# B3 local: SAM en flujo, colación derivada y conteo acotado

02/11/2026. Base de PR36:76e1f9b9bd082adf8f7db728758eec548777f2c6.
Plan previo: research/plans/2026-11-02-compact-pe-stream.md.
**B3 cerrado como componente local; B1/B4/B5 pendientes. Producción deshabilitada.**

## Evidencia ejecutada

156 tests locales correctos, sin omisiones:19 nuevos y137 existentes (118 de
runner/archivo/transporte,17 PE y2 de colación previa). CPython3.12.14,
PySAM0.23.3/HTSlib1.21 por ruta explícita. Compileall correcto. executed/tests.txt
y validation.json registran esa batería; targeted-recheck.txt repite los19 con
expectativas numéricas explícitas después de revisar las comprobaciones. No sumar
repeticiones como tests únicos. No hubo fallos inesperados de tests en esta fase.

Ocho SAM sintéticos originales/ordenados cotejados con los blobs de la cabeza base;
fixture-sources.json añade SHA256. Los cuatro SAM ya alineados se consumen en flujo
y se comparan con las rutas anteriores a anclas15/8:16comparaciones de cuentas/QC,
incluida comparación texto/HTSlib. Repetición de los cuatro resultados idéntica por
contenido, sin nuevas alineaciones, índice, FASTQbiológico o conexiones de datos.

Orden de objetivos: canónica, brazo críptico izquierdo y derecho en coordenadas
locales del minigenoma; no cuentas observadas en bibliotecas reales.

| Fixture existente | Registros | Soportes15 | Soportes8 | QCprimario conservado |
|---|---:|---|---|---|
| wild |18|2,2,2|3,3,3|9grupos/9pares aceptados |
| multicopy |4|0,0,0|0,0,0|1grupo excluido por calidad/NH,2no primarios |
| wrongstrand |2|0,0,0|0,0,0|1par aceptado con XS+, sin objetivoXS− |
| wrongmotif |2|0,0,0|0,0,0|1grupo excluido por flags |

case-summary.json y executed/cases conservan controles negativos y tuberías:
productorPython→pipe→consumidor correcto sale0; productor que emite SAMválido y
sale7 deja resultfailed/producer_exit_code7, consumidor1; productor que no cierra
stdout deja lector bloqueado, supervisor corta≈1,010s para límite1s, observa2procesos
y cierra sin miembros vivos. El recibo del consumidor permanece started, no se
adopta ni sobrescribe. No se toma EOF como prueba suficiente de productor correcto.

## Cambio de representación

compact_pe_pipeline.run recibe un stream binario no seekable, una biblioteca,
inventario de objetivos, límites y callback obligatorio para comprobar el fin del
productor. La CLI solo reproduce un SAMfixture local y no lanza un alineador.
El llamante de una tubería debe supervisar productor/consumidor en el mismo grupo.

pe_fragment_contract conserva sus algoritmos; ahora expone generadores de líneas
y segmentos para reutilizarlos sin ficheroSAMintermedio. Texto y HTSlib decodifican
CIGAR separadamente para15y8. Se compara cada metadato y lista de eventos antes de
aceptar el registro; discordancia aborta. Tras coincidir se almacena metadato común
y cuatro listas de eventos. La independencia es de decodificaciónCIGAR, no cuatro
implementaciones biológicas independientes; normalización y reducción de pares
son compartidas, como antes.

La representación temporal JSONderivada contiene clavesRG/QNAME, flags, referencias,
posiciones, MAPQ/NH/XS y eventos decodificados. No contiene SEQ, QUAL, CIGARoriginal,
cabecerasSAMo payload de tags. No se escribe SAM/BAMgenómico completo. Conserva
eventos de todos los loci por registro hasta reducir pares: filtrarlos antes
cambiaría QCde hebra; un test con evento off-target discordante exige la misma
exclusión. Solo los objetivos prefijados se acumulan globalmente.

Colación por ASCII(RG,QNAME) mediante chunks ordenados y merges multipaso, con
fan-in limitado. Se leen como máximo16registros por grupo;17rechaza la ejecución.
La memoria de contadores globales depende del inventario objetivo, no del número
de uniones genómicas. No se presupone adyacencia de mates en el stream. RGdistintos,
doble apoyo y secundarios conservan soporte/QC. Se eliminan temporales al certificar;
si falla quedan derivados para reconciliación, sin reuso automático.

## Cotas y límites de interpretación

Se fijan máximos de entrada, línea, cabecera aceptada, registros, fila derivada,
chunk, runs iniciales, fan-in, bytes temporales, bytes de recibo y objetivos. Carga
de temporales antes de cada escritura, incluidos archivos de entrada+salida de un
merge; no se deducen hasta borrar el run ya consumido. El cap temporal cubre bytes
de runs, no bloques/directorios/metadatosFS. Recibo verificado también tiene cap;
escritura atómica puede requerir dos copias acotadas. La entrada puede consumir
1bytecentinela sobre el cap para detectar exceso; ese registro no se procesa.

En replaywild, entrada7.151bytes,18registros,2runs,1merge y pico temporal10.030bytes.
No afirmar que una representación derivada siempre ocupa menos que el origen:
metadatos/eventos repetidos y coexistencia de runs pueden superar un SAM pequeño.
El caso de test con chunks1KiB fuerza varias pasadas; límites humanos siguen sin
asignarse enB4. Lecturas acotadas y fan-in no son un cap kernel de memoria Python.

DependenciaPySAMobligatoria para este componente; no hay fallback que certifique
con un solo decodificador. La CIgeneral puede omitirlo cuando no está instalado;
el workflowPEinstala la versión fijada y ejecuta explícitamente19tests nuevos más
17previos en3.11/3.12. No confundir omisión con prueba ejecutada.

Faltan unión a ledger/contratos/caps globales y worker real fijo enB4/B1; no se
ha habilitado producción, alineado genoma humano o medido su rendimiento. Tampoco
se acredita spawn bloqueado, muerte del supervisor, procesos desacoplados o I/O
físico ininterrumpible. ASCII SAMcon referencias declaradas; formatos fuera del
contrato fallan. Los fallos de formato/dependencia no son ausencia de un evento.

## Reproducción y siguiente tarea

Con PySAM0.23.3 disponible: python scripts/run_compact_pe_gate.py --report
/tmp/ela-compact-new (directorio nuevo). Retiene JSON/logs y ejemplos derivados,
no copias de payloadsSAM. Los fixtures fuente siguen en su ubicación histórica.
Resultados/recibos no contienen un nuevo efecto biológico, PSI, p-valor o rescate.

**Única siguiente tarea B4:** ligar el componente a manifiesto/ledger y cerrar
límites globales/de fase, temporales/dependencias, RLIMIT_AS frente a RSS, reloj de
transporte y semántica de cobertura. Preparar y ejecutar solo preflight/dry-run
con sintéticos. B1ruta externa yB5entorno real siguen pendientes. No restaurar
índice, abrirFASTQreal o lanzar nuevos alineamientos. PR36 abierta, sin merge.
