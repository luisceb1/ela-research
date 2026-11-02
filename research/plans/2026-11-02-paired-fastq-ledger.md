# Fase paired FASTQ ligada al ledger — 02/11/2026

Pregunta técnica: ¿puede reutilizarse un prefijo certificado sin desvincularlo de
los mates transferidos, del manifiesto y del presupuesto original?

Antes de ejecutar controles: solo gzip sintéticos de tres pares; prefijo de dos.
Sin red externa, datos biológicos, índice o alineación. CPython y stdlib locales.
La firma incluye identidad ordenada de mates, tamaño/MD5 esperado, SHA256 local,
recibo ledger de transferencia, recibo HTTP cuando exista, política y fingerprint.
El ledger fija límites y deadline; ninguna reanudación reinicia consumo o plazo.

Predicción refutable: una fase verificada se reutiliza sin transferir ni escribir
prefijos; cualquier identidad/hash/recibo/prefijo/límite cambiado se rechaza.
Interrupción dura deja started y bloquea apertura; excepción deja failed. No se
reconcilian automáticamente huérfanos ni se adopta un result.json aislado.

Controles negativos: gzip CRC inválido después del prefijo, transferencia no
verificada, hashes esperados incompatibles, mates invertidos, recibos incompletos,
prefijo truncado, manipulación durante la validación, deadline agotado y salida
previa huérfana. También comprobar recibos HTTP con servidor loopback simulado
mediante recibo equivalente, sin certificar transporte remoto.

Fracaso: cualquier control negativo reutiliza/certifica; presupuesto o deadline
se reinicia; phase verified sin recibo final cotejado; consumo nuevo al reanudar.
Registrar versiones, hashes de código y salida de tests. Evidencia de ingeniería,
no replicación científica o validación funcional. Producción continúa deshabilitada.
