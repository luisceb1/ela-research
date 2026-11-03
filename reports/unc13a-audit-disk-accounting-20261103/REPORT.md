# Corrección de clasificación de disco antes de la auditoría local

## Evidencia y causa

Luis seleccionó correctamente el commit 0c486916 y el ejecutor v2. La preparación se detuvo en `disk_guard` con `Historical artifact partition cap`, antes de abrir el archivo del plan, crear la raíz nueva o iniciar un alineamiento. No proporcionó el desglose real de tamaños. Los errores de plan/SHA posteriores son secundarios: siguió pegando comandos separados en la consola después del fallo de preparación. No son nuevos fallos de cómputo.

La guarda sumaba el árbol completo del intento fallido a los artefactos históricos de 18 GiB. Así reclasificaba su texto plano y sus runs compactos como artefactos y podía rechazar un conjunto que cumplía las cuotas reales. La regresión reproduce ese caso: históricos justo por debajo de 18 GiB, temporales antiguos y nuevos dentro de 6 GiB y texto plano dentro de 2 GiB. El código previo habría sumado los temporales antiguos a los 18 GiB; el nuevo cuenta cada byte en su categoría.

## Cambio

Se corrige sólo `unc13a_locus_audit_v2.py`, cuya preparación fallida no produjo un plan aceptado. Los ejecutores históricos, el pipeline regional, objetivos, filtros y tamaño del prefijo quedan intactos. Nueva política explícita `cumulative-audit-partitions-v1`, incluida en el descriptor y en la salida de preparación con `disk_used_bytes`.

Los once árboles históricos y el control sellado siguen en artefactos. El intento de auditoría fallido y la nueva auditoría se clasifican por ruta: `alignment-inputs` como texto plano, `compact` como compactos y el resto como recibos. Ambas auditorías comparten las cuotas; no se asigna una cuota adicional al intento viejo. Se exigen catorce raíces distintas. Los errores incluyen cuotas y tamaños observados, sin lecturas masivas, cambios o borrado de datos.

| Categoría acumulada | Límite |
|---|---:|
| Artefactos históricos, incluido el control | 18 GiB |
| Texto plano de ambas auditorías | 2 GiB |
| Compactos de ambas auditorías | 6 GiB |
| Recibos de ambas auditorías | 0,25 GiB |
| Total de los catorce árboles | 27 GiB |
| Reserva libre mínima | 8 GiB |

No se amplían disco, RAM, CPU, red o tiempo. Continúan ventana 2100 s y reducción 720 s, dos CPU, RSS de grupo muestreada 6 GiB y AS por proceso 8 GiB. Se conserva íntegro el intento fallido, sin adoptar sus runs ni su texto plano. Cargo 7.322.807.977 bytes invariable, sin sumar de nuevo la reserva del navegador. La puerta del control sigue cerrada y el inventario continúa siendo exploratorio.

El bloque de ejecución se entrega dentro de un único scriptblock PowerShell (`& { ... }`), con errores terminantes y comprobaciones inmediatas de `$LASTEXITCODE`. De este modo un `throw` sale del bloque y no continúa hasta una ejecución sin SHA. Se usa un nombre de plan nuevo; no se borra ni sobrescribe uno existente. La raíz de ejecución no cambia porque el fallo ocurrió antes de crearla.

## Validación

27 pruebas específicas pasan con PySAM, sin omisiones, incluidas ocho nuevas regresiones de disco. Ver `validation.json`. Comprueban que los temporales antiguos no consumen artefactos, que todos los bytes siguen contando, que texto plano/compactos/recibos antiguos y nuevos comparten cuotas y que se mantienen límites de artefactos, total, reserva, raíces distintas y rechazo de enlaces. Se usan archivos dispersos de fixture: representan tamaños grandes sin ocupar ese espacio ni usar datos humanos. La contabilidad no abre su contenido.

Las pruebas previas de guarda, vencimiento, procedencia, replay y sellado siguen pasando. Sin PySAM se omiten sólo cinco integraciones dependientes de él. Compilación correcta. La regresión completa anterior de 525 pruebas corresponde al commit previo; no se presenta como nueva ejecución local de este cambio. GitHub vuelve a ejecutar las comprobaciones, incluida la matriz pareada con PySAM. No se ha vuelto a alinear una muestra humana en el entorno del agente.

## Próximo paso

Preparar un plan nuevo y comprobar la política de disco, el desglose y los campos fijos antes de aceptar la auditoría. Si el conjunto excede una cuota real, se detiene con cifras concretas: esta corrección no garantiza que cualquier tamaño quepa. No eliminar archivos ni ampliar límites automáticamente. Plan y bloque: `research/plans/2026-11-03-unc13a-audit-disk-correction.md`. Mantener todos los archivos y la PR abierta, sin fusionar.
