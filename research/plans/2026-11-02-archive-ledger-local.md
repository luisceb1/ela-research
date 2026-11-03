# Cierre local B2: checksums y archivo ligado al ledger — 02/11/2026

Base: PR36,7126bc52aa25f70322dc840b380cfbe2d2354956.
Pregunta técnica: ¿puede transferirse un objeto con SHA256 fijado, sin MD5 de
proveedor, y extraerse solo su inventario esperado bajo presupuesto y recibos?

Antes de ejecutar: únicamente tar.gz sintéticos y HTTP127.0.0.1. No índice humano,
FASTQ biológico, alineamiento o habilitación de producción. Mantener MD5solo y
doble checksum existentes. Exigir tamaño y al menos un checksum fijado, validar
el esquema antes de abrir red y verificar todos los checksums que se proporcionen.

Archivo: contrato del manifiesto fija transferencia/identidad, SHA256comprimido,
miembros regulares con tamaño/SHA256 y caps de miembros, datos y flujo tar. Leer
cabeceras de512bytes sin interpretar metadatos PAX/GNUlongname; rechazarlos antes
de cargar su payload. Rechazar rutas no canónicas, enlaces, dispositivos, miembros
extras/duplicados y colisiones archivo/directorio. Leer datos en chunks≤64KiB,
validar padding/final tar y consumir gzip hastaEOF/CRC completo. Un byte centinela
puede detectar exceso de cola; no escribir datos por encima de cap/inventario.

Fase archive con started/failed/verified, fingerprint, snapshot de recibo de
transferencia y HTTP cuando exista. Solo ledger+recibo final concordantes permiten
reuso; rehash de fuente y salidas al abrir/reutilizar. No adoptar directorios
huérfanos o reiniciar plazo/consumo. Conservar partials/fallos sin reparación.

Predicción refutable: SHA256solo pasa un recorrido HTTPlocal→archivo→reapertura
sin transferencia extra y con mismo plazo. Cada negativo falla sin fase verificada;
interrupción deja started o failed y bloquea apertura. Controles: checksum ausente/
malformado, checksum erróneo, ambos checksums exigidos, gzip truncado/CRC tardío,
traversal/enlaces/miembro extra/duplicado/tamaño/hash/tarheader/cola no cero/caps,
recibo/fuente/salida modificados y corte de proceso real durante extracción.

Fracaso: aceptar un control negativo, extraer fuera del destino, promoción pese a
CRC inválido, recibo reutilizado sin rehash o reset de presupuesto. Registrar
versiones, hashes, resultados y errores. La compatibilidad del índice humano real
seguirá sin ensayar; dialectos fuera del contrato se rechazan. Cerrar B2solo como
componente local, sin reducir las otras cuatro puertas o inferir resultados ELA.
