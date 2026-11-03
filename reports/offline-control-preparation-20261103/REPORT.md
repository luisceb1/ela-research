# Preparación del control local de UNC13A — 03/11/2026

Luis ha aportado ambos FASTQ completos y sellados. Esta implementación prepara únicamente la validación pareada y la cobertura del control local. No se han descargado lecturas ni alineado datos humanos en el entorno del agente.

El nuevo `offline_control_pilot.py` conserva los ejecutores históricos. Verifica el plan R2 aceptado, sus seis hashes, identidad y contabilidad, y los metadatos históricos. El padre no vuelve a leer los parciales antiguos. El trabajador comprueba las fuentes y las copias locales mediante tamaño, MD5 y SHA; valida todos los pares, EOF, CRC y nombres; extrae el prefijo prospectivo de un millón de pares y usa HISAT2 y el motor compacto originales. Sólo se procesa CTRL.

La propuesta y las guardas se describen en `research/plans/2026-11-03-offline-control-execution.md`: 50 minutos, CLOCK_BOOTTIME, 2 CPU, RSS de grupo de 6 GiB muestreada, espacio virtual por proceso de 8 GiB, disco de 27 GiB y reserva de 8 GiB. Se cuentan doce árboles y se proyectan ambas copias antes de iniciarlas. El cargo histórico permanece constante; no se añade HTTP ni se vuelve a reservar el navegador.

El sellador exige supervisión limpia, aceptación exacta, identidad, reloj, contadores, orden y recibos concordantes; comprueba el prefijo, los argumentos, la salida del productor, las métricas y la retirada del texto plano. La cobertura suficiente o insuficiente puede producir sello técnico, sin activar TDP.

## Validación

485 pruebas locales correctas, sin omisiones: 460 previas y 25 nuevas; Python 3.12.14, PySAM 0.23.3 y compilación correctos. Véanse `validation.json` y `tests.txt`.

Las integraciones pequeñas usan 9 y 36 pares de fixture con gzip y validación real. Un productor sustituto reproduce el SAM existente; ambos decodificadores y anclajes producen uniones de 6 y 24 grupos, verificando ambos resultados sin cambiar el umbral de 20. Sólo en pruebas se adapta el prefijo al tamaño de la miniatura; producción conserva un millón sin opción de cambio. No son alineamientos HISAT2 ni una medición de rendimiento humano.

Se prueban corrupción y alteraciones de metadatos, identidad, procedencia, contadores y recibos; enlaces simbólicos; orden, raíces y reuso; reloj civil y plazos de subfases; RSS, particiones y proyección de disco. Un subproceso real demuestra el bloqueo de red por audit hook; un trabajador CLI supervisado falla antes de cómputo ante una fuente ausente y deja el grupo vacío. Esto no garantiza rendimiento ni compatibilidad de HISAT2 en WSL.

La CI general omite las 20 pruebas que requieren PySAM cuando no está instalado, conforme al resto del repositorio. La CI pareada instala la dependencia fijada y debe ejecutarlas todas en Python 3.11 y 3.12. El primer envío reveló esta condición ausente; se corrigió en los tests, sin cambiar el ejecutor.

## Siguiente paso

Preparar el descriptor en WSL, comprobar los campos y aceptar la ventana local con el bloque PowerShell. Mantener los originales. Ante fallo, conservar los recibos y no repetir. Si la cobertura resulta insuficiente, registrar ese límite sin inferir ausencia biológica. No hay nuevos resultados biológicos, PSI, comparación entre condiciones, rescate ni beneficio clínico. La PR 36 sigue abierta, sin fusionar.
