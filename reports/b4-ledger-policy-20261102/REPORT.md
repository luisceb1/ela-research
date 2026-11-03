# B4 local: cómputo, clocks, recursos y cobertura ligados al ledger

02/11/2026. Base PR36:b6522a94689eee057b7abddb72bde7b5497b37dc.
Plan previo: research/plans/2026-11-02-b4-ledger-policy.md.
**B4 cerrado como política/componente local; B1yB5 pendientes. Producción=false.**

## Evidencia ejecutada

183tests locales pasan sin omisiones:20nuevos y163existentes (156de la batería
anterior más7del supervisor reparado). CPython3.12.14, PySAM0.23.3,
samtools_version1.21. Compileall correcto. executed/tests.txt y validation.json
registran la ejecución final. Primera batería183/183también pasó; revisión añadió
detección de retrocesos respecto a observaciones dentro del mismo runner y se
repitió la batería. No sumar repeticiones como tests/experimentos únicos.

La fuente sigue siendo SAMsintético ya existente; no nueva alineación, índice
humano, FASTQbiológico, tráfico externo o gasto. Las sondas de tiempo usan un
reloj inyectado, además de un worker local real bajo supervisor.

| Control | Resultado |
|---|---|
| Transferencia simulada de3s y reapertura20s después | Conserva3sconsumidos y deadline original; espera entre fases no se cobra como transporte |
| Dos transferencias de6sy5s con cap acumulado10s | Segunda rechazada; registra11s del intento fallido, no reinicia a0 |
| Phase/subphase, commit expirado o reloj atrás | Rechazo y fallo/incompleto conservado; no promoververifiedal cerrar fuera del cap |
| Dos objetivos en un par conocido | Suma de apoyos2; unión de grupos1; no moléculas únicas |
| Fixturewild |6grupos objetivo, mínimo20: cálculo verificado pero cobertura insuficiente; bloquea fase nueva |
| Fuente/resultado/recibo/cobertura/HTTP/dependencia o política alterados | Reuso/reapertura rechazados |
| Worker local correcto | Recursos fijados256MiBRSS/384MiBAS;exit0y sin miembros vivos |
| Worker bloqueado tras comenzar productor | Guarda padre corta≈1,097s desde lanzamiento por subdeadline1s;exit−9y sin vivos; ledger.started conserva7151bytes y reloj |

Los casos retenidos están en executed/cases y case-summary.json. En el último,
violation=null y supervisor_error="RuntimeError: Phase/subphase deadline": es la
guarda del padre, no el timeout externo de4s. El recibo externo queda finished;
no se inventa un fallo interno limpio. El started impide reabrir. No se deducen
valores de RAM ausentes en un recibo abortado ni se reconstruyen retrospectivamente.

## Política opt-in y compatibilidad

execution_policy usa schema pilot-b4-local-v1 y production_enabled=false. El
fingerprint fija límites y fases; los ledgers históricos sin esta política siguen
su contrato anterior. No se convierten ni se amplían automáticamente. Una fase
no declarada, de tipo equivocado o concurrente se rechaza; límites de proceso
requieren valores explícitos concordantes. La ruta de producción sigue cerrada.

Cada fase fija started/deadline/finished. Cómputo compacto añade productor y reduce
con subdeadline propio. Clocks: plazo total persistente y transporte acumulado
separados. Este último suma intervalos de transferencia, incluidos fallos y retries
del mismo intento de fase, y excluye esperas entre fases. No reset al reabrir o
reintentar. Un presupuesto consumido por completo no prohíbe inspeccionar fases
no transferidas si el total sigue válido; no permite transferir más.

Las guardas comparan el reloj con highwater persistido y observado en la sesión.
Antes de guardar una fase nueva verified se cierra su tiempo y se revalida el cap;
si falló, ledgerfailed. No es una fuente de tiempo confiable contra manipulación
hostil del anfitrión o del ledger, ni garantía de tiempo real. La supervisión usa
también timeout monotónico del proceso. B1debe mantener todas las operaciones
voluminosas del worker real, incluso rehash, bajo supervisión, sin ejecutarlas en
un padre sin límites como si ya fueran un pipeline humano acreditado.

El worker local ahora acepta compact. El padre recorta el timeout por política,
plazo y saldo; aplica RSS/AS de la fase, vigila clocks/particiones leyendo el ledger
atómico y termina el grupo aunque el hijo no llame a su guarda. El supervisor
registra exit_codey miembros restantes también al abortar por callback. No hay
reconciliación automática: fallos/incompletos siguen bloqueados.

## Ligadura de cómputo

compact_ledger_phase exige source_scope=existing-synthetic-sam-only y una
transferencia verificada. Fija biblioteca, objetivos, cotas del componente,
umbral, identidad de decoder y recursos de fase. Rehashea fuente; liga snapshot
del recibo de transferencia y, cuando existe, HTTPfinal. Identidad: versiónPySAM,
samtools_version y SHA256de__init__, libcalignedsegment, libchtslib y siete scripts
del motor/política. No se reutiliza un resultado al cambiar bindings o código.

Después de EOF, la fuente debe seguir concordando y el pipeline debe haber
terminado con productor0. Recibo del cómputo fija SHA256de result, binding y cobertura;
ledgerfija SHA256de ese recibo. Reapertura/reuso revalida todo, incluidas copias de
cobertura en ledger/recibo/resultado. Un resultverifiedaislado o directorio previo
no basta. El componente de fuente es sintético/local; B1debe fijar la procedencia
del stream humano al índice/prefijos/binarios antes de cualquier uso real.
Un recibo interno verified acredita cómputo/integridad; una llamada API directa
no prueba que se aplicara RLIMIT_AS/RSS. El worker local sí los aplica y conserva
su recibo externo. B1debe sellar esa evidencia de supervisión junto al resultado
antes de permitir una ejecución real.

## Cobertura: decisión prospectiva explícita

Se reemplaza la suma solapada del borrador anterior por un mínimo de20grupos
aceptados(RG,QNAME) con al menos un objetivo a ancla15. Se informa por separado
soporte por evento, suma de eventos y unión de grupos. Dos brazos en un mismo
par aportan2a la suma y1a la unión. Duplicados marcados se retienen y etiquetan;
no UMI ni deduplicación molecular. No llamar moléculas o réplicas biológicas a
esos grupos. El umbral es operativo, no poder estadístico.

Cambio fijado antes de lecturas reales y sin elegir por un efecto observado.
El borrador histórico permanece intacto. Una fase puede terminar técnicamente
verifiedy resultar coverage.adequate=false. Puede inspeccionarse/reutilizarse;
se prohíbe iniciar otra fase automáticamente. No ampliar prefijo o recursos para
perseguir positividad. El fixturecon6grupos no es evidencia de cobertura humana.

## Propuesta humana, solo planificación

planning-envelope.json se genera con plan_b4_execution_policy.py; no tiene
fuentes ejecutables completas ni habilita producción. Caps de parada, no benchmarks.

| Reloj | Cap propuesto |
|---|---:|
| Total |9000s|
| Transporte acumulado5objetos |3600s en conjunto, no por cada objeto |
| Preflight |120s|
| Extracción índice |600s|
| Integridad/prefijo |900s por biblioteca |
| Cómputo por biblioteca |1200s, productor900+reduce300 |
| Envolvente conservadora |8520s y480s de margen |

Máximo2CPU. Cómputo:6GiBRSSde grupo muestreada y8GiBde RLIMIT_AS por proceso;
son límites distintos. Transferencia/preflight512MiBRSS/1GiBAS; archivo/prefijos
1GiBRSS/2GiBAS. No se ha comprobado el índice real bajo estos recursos. Los límites
por proceso virtual no son un cap de memoria agregada de kernel.

| Disco adicional | Partición |
|---|---:|
| Artefactos transferidos, partials y extraídos |16GiB|
| Prefijos de ambas bibliotecas |2GiB|
| Derivados/merges temporales |6GiB|
| Dependencias nuevas |512MiB|
| Recibos/logs/salidas |256MiB|
| Sin asignar dentro de25GiB |256MiB|

Reserva física8GiB libre; total particionado24,75GiB. Clasificación por rutas
controladas; todos los demás archivos cuentan como recibos. Guardas en hijo y
padre, no cuotas kernel: puede haber latencia/overshoot hasta siguiente muestra,
metadatosFSno incluidos en suma de st_sizey dos copias atómicas transitorias.
El componente sí carga sus runs antes de escribir y limita sus recibos.

12GBde cuerpo transferido+índice extraído4.664.043.238=16.664.043.238bytes,
dentro de16GiBpara artefactos. Mínimo4mates+archivo10.705.490.230; si hubiera que
transferir512MiBcompletos de dependencias, serían11.242.361.142bytes, margen757.638.858
hasta12GB. No garantiza retries completos. Dependencias actuales pueden no requerir
descarga; cualquier descarga nueva necesita una fase declarada antes, no saltarse
el catálogo del plan. No construir índice nuevo o ampliar a doce bibliotecas.

## Límites y siguiente tarea

No certifica precisión temporal, spawn bloqueado, I/O ininterrumpible, muerte del
supervisor, grupos desacoplados o escritores hostiles. Cuerpo HTTPno cuenta TLS/
TCP/cabeceras/buffering. La política debe volver a cotejarse con entorno e índice
reales enB5. Ningún resultado nuevo de splicing, PSI, p-valores o rescate funcional.

Reproducción con PySAM0.23.3: python scripts/run_b4_local_gate.py --report
/tmp/ela-b4-new (directorio nuevo). Retiene JSON/logs sin copiar SAMpayloads.

**Única siguiente tarea B1:** worker fijo que una prefijos/índice/alineador/stream/
conteo bajo la misma política y contrato de procedencia. Diseñar la ruta externa
con orígenes exactos y probarla mediante productores/servidores sintéticos locales;
mantener el interruptor de producción cerrado. Sin descargas reales o nuevas
alineaciones. B5entorno/índice y decisión expresa de ejecución seguirán pendientes.
PR36 abierta y sin merge automático.
