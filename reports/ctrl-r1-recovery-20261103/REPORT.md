# Recuperación de CTRL_R1 — 03/11/2026

## Evidencia

Luis ejecutó el descriptor15f85f9d… en49f37a0. Preflight verificado en25,472s. CTRL_R1 falló por timeout de lectura tras523,688s; supervisor exit1, sin infracción/grupo vacío,535,117s yRSS46.907.392B. No alineamiento. Datos aportados por Luis, no inspección remota. Recibo354.631.727B, cargo356.515.840B: diferencia1.884.113B conservada. Total4.712.318.573B y4.272,2037699222565s históricos.

## Interpretación y cambio

No se agotó la ventana global ni se registró un exceso de RAM. Timeout no determina si falló servidor, ruta o equipo. El transporte anterior usa5s de socket; la recuperación propone30s por operación bajo watchdog1800s, sin garantía de éxito futuro.

recover_ctrl_read.py sólo admite este mate/interrupción concretos. Audita job aceptado, ledger, preflight, error, supervisor y cadena del índice. Comprueba tamaño real/SHA del parcial y genera plan deshabilitado con raíz exclusiva. Copia el prefijo comprobado, hace una petición Range354631727–960856962; exige206/Content-Range/Length exactos y rechaza200, redirect, proxy, encoding, chunked o multipart. Tamaño completo960856963 yMD5ed58daa011d6508a3e8d1f05bc39fc29 permiten promover CTRL_R1.fastq.gz; añadeSHA256 local, no presentado como hash publicado. Padre sella sólo con recibos y grupo limpios. No ejecuta todavía descompresión/CRC pareada.

Nueva ventana propuesta2400s(300copia/auditoría+1800HTTP+300verificación), requiereSHA y --accept-additional-time-window. Original inmutable, sin reinicios/reembolsos/retries. Descarga restante606.225.236B; cargo final5.318.543.809B ysaldo6.681.456.191B del techo12GB. Caps512MiBRSSmuestreada/1GiBAS,2CPU,disco25GiB en cinco árboles yreserva8GiB. No modifica trabajador existente ni su identidad. No otros mates, índice, descompresión ni alineamiento.

## Validación y límites

308 pruebas locales correctas sin omisiones:289 anteriores+19 nuevas. Positivo con HTTP local artificial, copia/hash/MD5 y sello externo; negativos de cabeceras/rangos/short/corrupción/tamper/cargo/deadline/disco/aceptación/reutilización. Trabajador CLI real supervisado falla antes deHTTP con metadatos ausentes y grupo vacío. Dos fallos iniciales de fixtures quedan en initial-tests-failure.txt y audit-fixture-failure.txt: faltaban directorio supervision ycampo index_root; corregidos sólo fixtures. No HTTP ENA ni alineamiento humano en nuestro host. La verificación completa de gzip/pares seguirá pendiente. Muestreo RSS/disco no equivale a cuotas duras del kernel; límites del supervisor anteriores conservados. No inferencia biológica o clínica.

## Siguiente prueba

Emitir plan local deshabilitado, revisar JSON/SHA antes de aceptar tiempo nuevo. Sólo tras eventual sello diseñar adopción del mate/cargos en el piloto; no reabrir el trabajo fallido. Si servidor ignoraRange o checksum falla, detenerse sin promoción. PR36 abierta sin merge. Véase runbook research/runbooks/2026-11-03-ctrl-r1-recovery-powershell.md.
