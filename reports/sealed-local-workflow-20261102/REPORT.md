# B1: integración local fija y aceptación tras supervisión

02/11/2026. Base PR36:eab691f3c7e0bbf308d3c67c16390bad07d715da.
Plan previo: research/plans/2026-11-02-sealed-local-worker.md.
**Integración sintética verificada; ejecución real deshabilitada.**

## Evidencia ejecutada

201tests locales pasan sin omisiones:18nuevos y183existentes. CPython3.12.14,
PySAM0.23.3, samtools_version1.21. Compileall correcto. executed/tests.txt y
validation.json conservan la batería completa. targeted-rss-check.txt repite solo
el negativoRSScon productor detenido para hacerlo independiente de lo rápido que
termine; no se cuenta como otro test único. Las baterías locales199/200pasaron.
La primera CI con PySAMen3.11 detectó una carrera del monitor al eliminarse un
directorio partial durante pathlib.rglob;3.12fue cancelada por fail-fast. Se cambia
a os.walk con handler solo para FileNotFoundError, manteniendo errores de acceso
fatales, y se añade un control determinista. ci-initial-failure.txt conserva el
fallo; la batería final201/201pasa con recibos regenerados bajo el código corregido.

Se verifica un recorrido de siete fases en el mismo worker: cuatro HTTPloopback
(archivo de índice simulado,R1,R2,SAMfixture), extracción, prefijo y cómputo en
pipe. 7.890bytes transferidos, nueve pares sintéticos en el prefijo y seis grupos
con soporte objetivo. Tres fuentes anteriores cotejadas con Git blob/SHA256;
fixture-sources.json. El tar contiene ocho archivos etiquetados explícitamente
SYNTHETIC PLACEHOLDER, **no un índice HISAT2 válido**.

| Caso retenido | Resultado |
|---|---|
| Recorrido correcto + revalidación | Sello,4peticiones,7fases verificadas, ledger idéntico tras revalidar |
| Mínimo20con fixturede6grupos | Sello indica coverage_insufficient; no se transforma en cobertura adecuada |
| Productor que emite datos válidos y sale7 | Consumidor/worker1, fasefailed, sin sello |
| Productor bloqueado tras emitir | Corte por subfase productor1s; tiempo del recibo incluye arranque/fases previas;−9,sin vivos,sin sello |
| Rechazo externo inyectado después del resultado interno | Resultado interno complete, sin sello; reapertura denegada |
| Prefijo alterado después de sellar | Revalidación supervisada rechazada, sin nueva peticiónHTTP |

case-summary.json y executed/cases conservan metadatos y logs. En el rechazo
externo, el supervisor real terminó0y se preserva su recibo real: el test devuelve
al padre un objeto de decisión con exit9y lo registra aparte como inyección. No
se falsifica el recibo original ni se presenta como fallo real de proceso.

El caso positivo usa umbral1solo para probar el cierre de orquestación. Otro caso
usa20y queda insuficiente. La propuesta humana mantiene20grupos, no se rebaja por
el resultado del fixture. Estos tiempos no son benchmarks del genoma humano.

## Contrato fijo y procedencia

sealed_local_workflow valida un descriptor exclusivo de tamaño≤1MiB: esquema,
modo sintético, inventario exacto de orígenes HTTPdeIPloopback, pasos permitidos,
política y hashes de productor/worker/interprete/decoder. No shell o argvlibre.
Origen distinto, redirect, modo producción, hash incorrecto o pasos desconocidos
fallan. Las descargas usan reservas duraderas y el transporte ya comprobado.

Archivo/prefijos deben estar verificados antes del stream; se ligan sus recibos,
inventario de ocho miembros, identidades y hashes. El productor fijo valida
nombres de los dos prefijos contra el SAMreproducido, con límite64pares/1MiBde
fixture. No infiere mapeo ni utiliza la secuencia del índice para alinear.
ProductorPythonyconsumidor comparten grupo supervisado. Stdoutsolo en pipe; no
SAMde salida nuevo en disco. La copia SAMde entrada es el fixturehistórico
transferido para este ensayo, no un archivo de alineamientos genómicos nuevo.

El adaptador HISAT2 tiene argv fijo de diseño con binario absoluto/ejecutable y
SHA256concordante, índice/prefijos derivados, -S /dev/stdout,--no-mixed,
--no-discordant,--fr,-p2,--seed0. Omite --rna-strandness y--tmo. Su prueba usa el
ejecutablePythoncomo archivo stand-in para verificar el contrato de argumentos;
no acredita que ese archivo sea HISAT2o que el índice sea compatible. La ejecución
real se rechaza antes de tocar binario/entradas. PRODUCTION_ENABLED=False,
modo de descriptor sintético y política production_enabled=false permanecen.

## Aceptación externa y reuso

El padre no construye un DryRunner ni rehashea entradas voluminosas. Lee solo
metadatos acotados, lanza un worker fijo bajo supervisión y vigila clocks/disco/RSS
de la fase activa. El hijo realiza hashes, archivo, prefijos y pipeline. El límite
ASsoft se ajusta al de la fase bajo el hardglobal; el productor lo hereda. El
supervisor recibe un callback de RSSpor grupo para exigir un cap de fase inferior
al global. El negativo1MiBRSScon productor detenido lo comprueba.

Un ledger de modo sellado no se puede reabrir solo porque sus fases figuren
verified. El padre debe comprobar supervisorfinished/exit0/sinviolación/sinerror/
grupo vacío y resultado interno coherente. Entonces escribe un sello que fija
SHA256de descriptor,ledger,resultado interno y recibo externo. Si el padre muere
antes o el supervisor falla, no se adopta el resultado interno. No se inventan
recibos faltantes o se sobrescriben descriptores/ejecuciones.

La revalidación posterior es otro worker supervisado: primero comprueba sello y
después rehashea fuentes/salidas y recorre sus contratos. No realiza transferencias,
no modifica ledger, bytes consumidos o clocks; conserva el deadline original.
Una modificación de metadatos sellados falla por SHA; una modificación de datos
falla dentro del worker. El sello es un mecanismo de integridad local, no firma
criptográfica contra un anfitrión hostil capaz de reescribir toda la evidencia.

## Límites y preparación real pendiente

B1queda verificado como integración local, no como ejecución HISAT2humana. No se
ha alineado otra vez, instalado/restaurado índice real, abierto FASTQbiológico,
contactado terceros o incurrido costes. No nuevos PSI, p-valores, efectos o rescate.

Los caps de RSS/disco se muestrean, no cuotas kernel agregadas. No garantía de
tiempo real, spawn bloqueado, I/O ininterrumpible, muerte del supervisor, grupos
desacoplados o modificación hostil concurrente. CuerpoHTTPexcluye TCP/TLS/cabeceras/
buffering. Un sello válido puede documentar cobertura insuficiente; no autoriza
ampliación. No extrapolar recursos/velocidad de este replaya lecturas reales.

**B5sigue abierto:** comprobar host elegido, binario2.2.3yhashes, índice real y su
dialecto, dependencias del worker y restricciones de ejecución. La activación es
otra puerta explícita: el código actual rechaza descriptores reales, HTTPSexterno
y producción. Habilitarlos requiere un cambio revisado con orígenes exactos y una
decisión expresa de ejecución; este informe no los activa. No venderlo como un
piloto ya listo o autorizado por haber pasado pruebas.

## Reproducción y siguiente tarea

Con PySAM0.23.3: python scripts/run_sealed_workflow_gate.py --report
/tmp/ela-sealed-new (directorio nuevo). El harness conserva JSON/logs de seis casos;
no duplica payloadsFASTQ/SAM. Rutas/puertos de los recibos corresponden al ensayo,
no a ubicaciones persistentes de datos. Crear fixtures nuevos para reproducirlos.

**Única siguiente tarea:** preflightB5de solo lectura del entorno disponible y
paquete revisable de activación: rutas/hashes/orígenes/argv/caps y bloqueos exactos.
Sin descarga de índice o lecturas reales, alineamiento nuevo o activación. Mantener
la PR36 abierta sin merge automático y conservar snapshots históricos.
