# Piloto UNC13A: preparado por componentes, todavía no ejecutable

02/11/2026. Fuente: cabeza de PR36,019572483bf6e88665f9c852c33741c21cede53d.
Decisión: **BLOCKED; raw_execution_ready=false**. Cinco puertas pendientes,
cuatro de integración/contrato y una de preparación efectiva del entorno. No
descargas reales, restauración de índice o alineamientos en esta auditoría.

## Evidencia comprobada

28archivos de código, contratos y recibos cotejados por su Git blobSHA en esa cabeza;
source-manifest.json y audit.json conservan SHA256 adicionales. Diecinueve comprobaciones
de consistencia pasan y tres sondas offline reproducen restricciones reales. Son
comprobaciones de auditoría; no19tests nuevos ni resultados científicos. Se leen
los recibos previos; no se repiten sus experimentos para inflar evidencia.

El contrato PE, coordenadas UNC13A, ruta unstranded, validación EOF/CRC/mates/prefijo,
ligadura al ledger y supervisión externa local están acreditados en su ámbito
sintético. Minigenoma:12expectativas funcionales; decodificación independiente,
política de pares compartida. Sus antiguos fallos de RAM/recibos siguen preservados.

Los dos binarios locales HISAT2v2.2.3sí están presentes fuera de PATH; sus hashes
coinciden con los históricos y --version termina con0. No se ha recompilado.
El índice hg38genome.*.ht2 no aparece en el directorio de trabajo inspeccionado.
PySAM0.23.3/HTSlib1.21 funciona al añadir expresamente pe-deps, pero no se importa
por defecto en el Python del worker. No hace falta inventar que HISAT2 no existe
ni instalar samtools solo por no estar en PATH.

## Lista cerrada de puertas pendientes

| Puerta | Hallazgo verificable | Cierre requerido |
|---|---|---|
| B1: ejecución externa | El worker solo admite HTTP loopback; DryRunner rechaza production=True | Worker fijo de producción, orígenes HTTPS exactos y contratos ligados, ensayado antes de habilitarlo |
| B2: índice por SHA256 | El adaptador exige expected.md5; el índice tiene SHA256 fijado y ETag multipart que no es MD5. La extracción histórica no es fase del ledger actual | Esquema con al menos un checksum fijado, compatible SHA256solo, y extracción acotada por miembros/hashes con recibo global |
| B3: alineamiento/colación/conteo | El flujo minigenoma guarda SAM; collate_pe_sam abre SAM completo y crea keyed+ordered antes de escribir otro SAM | Ruta en flujo o representación compacta acotada, dos decodificadores, QC y soporte, sin SAM/BAM genómico completo o FASTQ completo descomprimido |
| B4: presupuesto de todas las fases | El plan60min se refiere a transporte; el runner tiene un único deadline para todo. Faltan cotas finales de temporales/prefijos/dependencias y política de espacio de direcciones | Fijar reloj acumulado de transporte y reloj total, caps de fase, picos de disco y significado exacto del umbral de cobertura |
| B5: entorno de ejecución | Índice ausente y PySAM fuera del entorno de importación por defecto | Tras cerrar código y decidir ejecución, restaurar/verificar índice actual, fijar rutas/hash/binarios/dependencias y comprobar importación del worker |

B5es un requisito previo a alinear, no una orden para descargar ahora. El no haber
ejecutado aún datos reales no es un fallo de validación: es una fase condicionada.
gate-review.json registra decisiones manuales de revisión con rutas de evidencia;
el script verifica datos/cálculos, no certifica automáticamente exhaustividad del
código. Si aparece un hallazgo nuevo debe revisarse la lista, no ocultarlo.

## Presupuesto reconciliado

| Concepto | Bytes | Lectura correcta |
|---|---:|---|
| Cuatro FASTQgzip |6.349.703.881| Dos bibliotecas técnicas, no pareja biológica |
| Índice comprimido |4.355.786.349| SHA256 y versiónS3 fijados históricamente |
| Transferencia base |10.705.490.230| Sin dependencias nuevas ni reintentos |
| Margen hasta12GB |1.294.509.770| No da para repetir todo el índice ni un mate de TDP-5 |
| Índice extraído, incluido make_hg38.sh |4.664.043.238| Ocho ht2 más receta; no ejecutar la receta |
| Raw+archivo+extraído coexistiendo |15.369.533.468| Piso de disco; no pico completo |
| Margen hasta25GiB adicionales |11.474.012.132| Todavía incluye prefijos, temporales, salidas y dependencias |

El margen permite, individualmente, repetir un mateCTRL de tamaño≈0,96/1,00GB,
si no hubo otro gasto; no ambos. No garantiza que un retry concreto que ya perdió
bytes quepa: el ledger decide con saldo real y conserva reservas inciertas. No
ampliar presupuesto automáticamente.

Disco libre observado≈63,68GB; cgroup8GiB y cuota8CPU, con afinidad disponible para
restringir2. Los límites25GiB+8GiBreserva y6GiBRSS nominales caben en esas cifras,
pero no prueban pico o rendimiento humano. Transportar la base en3600s requiere
≈2,97MB/s de cuerpo sostenido; es requisito aritmético, no velocidad medida. El
presupuesto excluye TCP/TLS/cabeceras/buffering; RSS y disco son muestreados.

## Propuesta concreta, todavía sin ejecutor

execution-proposal.json fija CTRL-4/GSM8975203/SRR33425816 y
TDP-5/GSM8975210/SRR33425819 por menor tamaño dentro de condición. Incluye los
cuatro URLs/tamaños/MD5, el índiceS3versionado/SHA256 y hashes de miembros, un
millón de pares iniciales por biblioteca, geometría0-based y argv de diseño.
No es CLI ejecutable: execution_enabled=false y la ruta de streaming no está implementada.

Se propone, para revisión, un reloj global total de9000s que no reinicie al reabrir:
preflight120s, transferencia acumulada3600s, extracción/verificación600s,
integridad/prefijo900s por biblioteca, alineamiento900s por biblioteca y
colación/conteo300s por biblioteca. Suma8520s más480s de margen dentro del total.
Son cortes propuestos, no tiempos esperados ni una ampliación ya autorizada.
Se mantienen2CPU,6GiBRSS,25GiBdisco adicional,8GiBreserva y12GBtransferencia;
RLIMIT_AS y cotas de temporales deben cerrarse enB4, no asumir equivalencia a RSS.

Orden condicionado: preflight del entorno/contratos → restaurar/verificar índice
→ transferir y validar cada par de mates hasta EOF/CRC → prefijo exacto → alinear
genoma completo en flujo → colar/contar con ambos decodificadores → informe técnico.
Cada fase exige recibo, hashes y límite propio. No reutilizar un result aislado,
adoptar partial, reparar fallos o borrar reservas inciertas automáticamente.

Primary: omitir --rna-strandness y --tmo; orientación físicaFR, NH1,
20≤MAPQ<255, XS− y anclas15; anclas8solo sensibilidad prefijada. Duplicados marcados
se cuentan y etiquetan; no moléculas únicas. El umbral propuesto20se expresa como
suma de soportes por evento canónico/críptico; un fragmento puede apoyar dos eventos.
Reportar eventos separados y esa suma, sin llamarla20moléculas únicas. Esta
semántica debe aprobarse enB4antes de datos; no inventar una equivalencia con poder
estadístico. Por debajo: insuficiente, no ausencia ni ampliación automática.

Las entradas ENA y objetoS3son snapshots históricos, no metadatos revalidados por
red hoy. La semántica read_count_ena sigue sin certificarse y no se usa para exigir
un número de pares. Antes de una fase real habrá que verificar las identidades
vigentes bajo el contrato habilitado. No se infieren grupos/pares independientes,
PSI, p-valores, efectoKD, rescate neuronal o beneficio clínico.

## Validación, errores y siguiente tarea

audit_humphrey_pilot_readiness.py reproduce sumas, cotejos y tres sondas con lector
HTTPsimulado, sin abrir red: producción rechazada antes de fase; HTTPS externo
rechazado; objetoSHA256solo da KeyError('md5') después de tres bytes artificiales
cargados y fasefailed. Ese negativo confirmaB2, no se presenta como éxito del
transporte. Compileall correcto. audit-log.json registra incidencias de preparación.

**Única siguiente tarea:** cerrarB2con checksumSHA256solo y restauración de archivo
sintético ligada al ledger, acotada por miembros/tamaño/hash, con interrupción y
recibos. Ningún índice humano, FASTQreal o alineamiento hasta nuevas puertas.
No hace falta repetir G1–G4sin cambios de política o nueva evidencia. PR36 sigue
abierta y sin merge automático.
