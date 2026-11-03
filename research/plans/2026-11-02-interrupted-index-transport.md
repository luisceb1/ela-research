# Descarga del índice interrumpida: diagnóstico y optimización

Evidencia aportada por Luis: preflightverified, index_archivestarted,
transfer_bytes_consumed=1632463668, elapsed=3600.0012652873993s,
unsettledreservation=0; parcial≈1.6GiB; log delworker vacío y padre cortó por
tiempo acumulado. No índicecompleto/FASTQ/alineamiento. No atribuirlo aún a la red.

Pregunta: ¿pueden reservas duraderas porbloque reducir sincronizaciones manteniendo
contabilidad conservadora ante SIGKILL/lecturasfallidas y los mismos límites?
Predicción: para8MiByread1de16KiB, bloques4MiBreducenlas escrituras de metadatos
frente al esquema porlectura; mismosbytes/SHA/resultado. No extrapolar velocidad
medida en nuestrohost aWSLdelusuario. Comparar número de fsync y tiempos separados.
Controles: reservaantesdeprimera lectura, excepción a mitad de bloque sinrefund
incierto, truncación/checksum y guardadetiempo, consumo≤cap, metadatosde modo
histórico intactos, esquema sintético previo sin cambios de contabilidad.
Fracaso: lectura sincrédito duradero, reembolso incierto, promover parcial,
reanudar o renovar tiempo/presupuesto automáticamente.

Además: inspector de solo lectura de la ejecución interrumpida: comprobar hashes
metadatos/fingerprint, tamaño/SHAparcial y presupuesto ya consumido. El parcial
no estáverificado; informe no habilita recuperación. Mantener ejecución original
intacta; no Range, HTTPreal, borrados, extensión de caps, descarga o alineamiento.
La recuperación porRange y eventual nuevo plan de tiempos son tareas posteriores
con decisión expresa y evidencia del estado exacto del parcial.
