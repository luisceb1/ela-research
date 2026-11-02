# B2 cerrado como componente local: SHA256 y archivo con ledger

02/11/2026. Base de PR36:7126bc52aa25f70322dc840b380cfbe2d2354956.
Plan previo: research/plans/2026-11-02-archive-ledger-local.md.
CPython3.12.14, stdlib, Linux/procfs. **raw_execution_ready=false**.

## Evidencia

118 tests locales pasan:39 nuevos (32 de archivo y7 de checksums) y79 existentes.
Sin omisiones locales. Compileall correcto. executed/tests.txt y validation.json
conservan la ejecución final; no equivalen a suite completa o experimentos únicos.
Se retienen cinco casos de JSON/logs en executed/cases, resumidos en case-summary.
Fixtures regenerables en test_archive_ledger_phase.py y test_artifact_checksum_transport.py.

| Control retenido | Resultado observado |
|---|---|
| SHA256solo, HTTP127.0.0.1→extracción→reapertura |1petición,128bytes transferidos,197bytes en2archivos,10.240bytes tar; mismo ledger/plazo al reusar |
| Transferencia sintética→extracción→reapertura | Archivos y recibo iguales, sin nueva transferencia o escritura |
| CRC incorrecto después de miembros | Fuente transferida por hash pero extracción failed; ninguna salida final certificada |
| Cabecera PAX con payload declarado1TiB | Rechazo en cabecera; no se interpreta ni carga ese payload |
| Corte externo durante extracción |≈1,008s para límite1s; SIGKILL,2procesos observados y0miembros vivos al cerrar; ledger/recibo started y partials conservados |

Otros negativos: cabecera tar corrupta, gzip truncado, tar incompleto dentro de
gzip válido, falta de segundo bloque cero, datos no cero tras fin, miembros gzip
concatenados no ignorados, padding no cero, miembro extra/duplicado/faltante,
tamaño/hash/caps incorrectos, traversal/ruta absoluta/no canónica, enlaces duros
y simbólicos, colisión archivo/directorio, recibos/fuentes/salidas alterados,
identidad/límites nuevos y directorio huérfano. Los fallos impiden reapertura.
Nombres con sufijo .partial no colisionan con el staging separado.

## Cambios y garantías verificadas

artifact_checksums.py exige tamaño entero no negativo y al menos un checksum
fijado MD5oSHA256. El esquema se valida antes de abrir red o crear fase. Si ambos
están presentes deben coincidir ambos. MD5solo sigue admitido; SHA256solo ya no
produce KeyError. Se calculan ambos localmente, pero expected_checksums del recibo
HTTP distingue los fijados de los meramente calculados; no inventar MD5de proveedor
para el índice o interpretar su ETagmultipart como MD5. Firmas existentes de
transferencias con mismos parámetros permanecen compatibles; no se adoptan fallos.

DryRunner.archive(name) exige contrato archives del manifiesto: identidad,
transferencia verificada, SHA256comprimido, inventario exacto de archivos/tamaños/
SHA256 y límites de miembros, datos expandidos y bytes tar. Firma ligada al
fingerprint y snapshot del recibo de transferencia; recibo HTTP final cotejado y
fijado también por SHAcuando existe. Fuente completa rehasheada antes y después.

No se utiliza tarfile.extract. Se lee una cabecera de512bytes con TarInfo.frombuf
y se rechazan extensiones PAX/GNUlongname, enlaces, especiales y rutas no seguras
antes de cargar su contenido. Lecturas de datos≤64KiB y guardas globales entre
chunks. Tamaño declarado debe igualar el inventario y caber antes de escribir.
Se validan checksum de cabecera, padding y dos registros cero de fin; se drena
gzip hastaEOF/CRC, incluidas colas/miembros concatenados. Solo ceros tras fin tar.

Archivos provisionales en partial/ separado, sin permisos/metadatos ejecutables
restaurados. Solo tras validar archivo completo y rehash se promueven todos,
fsync de datos/directorios y recibo atómico, seguido de ledgerverified. En un corte
entre promociones y commit no se adopta el directorio: started/failed bloquea.
Al reutilizar se cotejan contrato, recibo, fuente y cada salida por tamaño/SHA.
No se reinicia el plazo ni el consumo; no hay reparación o limpieza automática.

external_local_stage permite ahora el tipo archive, con el mismo worker fijo,
supervisor y prohibición de URLs externas. stall_archive es una pausa de prueba
explícita al existir un partial; crea un descendiente para comprobar limpieza.
No se ha habilitado process(production=True) o transporte externo del worker.

## Limitaciones y errores

Compatible con cabeceras regulares tar y directorios padres esperados; se rechazan
extensiones y dialectos no admitidos. **No se ha comprobado el formato del índice
humano real**, ni restaurado ese objeto. En la fase futura, si no cumple el contrato,
detener y revisar sin relajar validación automáticamente. Los checksums históricos
y límites reales se conservan como configuración, no como ejecución acreditada.

El cap tar incluye cabeceras/padding/cola. Puede leerse1bytecentinela por encima
del cap para detectar exceso; no se escribe ese exceso. No es un cap de tráfico
de red o buffers internos de gzip/TLS. Las guardas de disco/RSS son muestreadas;
la supervisión externa no garantiza tiempo real, spawn bloqueado, pérdida de
máquina, muerte del supervisor o procesos que cambien de grupo. No hay aislamiento
frente a escritores externos hostiles que alteren/restauren bytes durante el scan.
Rehash detecta cambios persistentes. Miembros ya preparados siguen siendo partials
si falla CRC o un miembro posterior. Ambos recibo y ledger son necesarios.

Primer ensayo:28/29tests de archivo correctos y1error del generador de fixture:
USTAR no codifica un número1TiB en su campo octal. Cambiado el generador de esa
cabecera a representación numérica GNU; el lector sigue rechazando tipoPAX antes
de payload. No se suavizó el extractor. errors.json registra el fallo. La batería
final118/118pasa. Los negativos esperados no se cuentan como fallos de test.

Solo ingeniería sintética: no FASTQbiológico, índice humano, alineamientos, costes,
comunicaciones, inferencia biológica o función neuronal. B2se cierra localmente;
B1/B3/B4/B5siguen pendientes. El informe de auditoría anterior es un snapshot
histórico: no regenerarlo sobre código cambiado como si fuera la misma cabeza.
readiness-delta.json explicita el cambio sin alterar esos resultados.

## Reproducción y siguiente tarea

python scripts/run_archive_local_gate.py --report /tmp/ela-archive-new
(directorio nuevo). Retiene JSON/logs, no gzip o payloads binarios. Versiones,
contratos, tamaños y hashes de fixtures están en los casos; rutas/puertos/plazos
temporales pertenecen a esta ejecución y no son ubicaciones persistentes de datos.

**Única siguiente tarea B3:** flujo de alineamiento/colación/conteo sin SAM genómico
completo, con representación compacta y cotas de registros/disco, preservando
fragmentos/QC y las dos rutas de decodificación. Usar SAMsintéticos existentes y
procesos locales bajo supervisión; sin índice humano, FASTQreal o nuevos
alineamientos. Mantener4puertas pendientes y producción deshabilitada. PR36 abierta,
sin merge/cierre automático.
