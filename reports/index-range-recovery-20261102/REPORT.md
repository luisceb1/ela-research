# Recuperación por rango del índice: propuesta preparada — 02/11/2026

Base8d1b2d9c6f67b85eab6707820f487e9874b3da22. Plan previo:
research/plans/2026-11-02-index-range-recovery.md.
Sin S3real, lecturasbiológicas/alineamientos o aceptación de tiempo real aquí.

## Evidencia nueva

Luis aporta auditoría completa: metadata/fingerprint/aceptación coherentes,
supervisor−9/grupovacío, parcial1.632.447.284B/SHAaf7750fc6ef148017aab8c339de670faebff34be5de69bddc0275dbeed21216d.
Cargo1.632.463.668B: diferencia16.384BNOreembolsada. source_verified=false;
identidad de bytes no prueba correspondencia con elorigen. Datosaportados,no
acceso delagente alordenador. user-reported-audit.json conserva hashes originales.

## Candidato implementado

recover_index_range.py separa --prepare de --execute. Preparación reaudita el
original de sololectura y emitearchivo nuevo deshabilitado ligado a paths,
auditoría,código/Python, fuente y límites fijos. Directorio de recuperaciónderivado
único, fuera deloriginal; si existe, no admiteotrointento ni rootalternativo.
No sobrescribe, reanuda, modifica ledger o extiende deadline deejecución01.

Ejecutar requiereSHAexactodelplan y--accept-additional-time-window, todavía no
aceptadosporLuis. La ventana nueva propuestaes2400s(copy/auditoría300,
transporte1800,verificación300),con supervisiónexterna y plazo persistente nuevo.
Se conserva deadlineoriginaly3600,001265sgastados, no se afirma continuar bajo
elcapantiguo. Bytes12GBsin aumento y cargo anteriorconservado,25GiBdiscoenambos
árboles+8GiBreserva,2CPU,512MiBRSSmuestreado/1GiBASporproceso. No benchmarks.

Worker reaudita antesdeHTTP, copia/hashprefixoriginalsin modificarlo, pide solo
bytes1632447284–4355786348 a laURL S3versionadaprevia. RequiereHTTP206,
Content-Range yLengthúnicos/exactos, x-amz-version-id exacto. Prohíberedirect,
200,encoding/chunked/multipart yretry. Crédito4MiBse reservaantesdeleer≤64KiB;
error incierto conserva cargo conservador, nunca reinicia elcontador.

Despuésdecola exacta, hashcompletodelarchivo y reauditoríadeloriginal. Solo SHA256
1848784403a0fb3ee7735b2f891d8be96fd2782e08aed3d8212d922666f077a5permite promoción;
resultadointerno queda pendiente deexterno. Padresolo lee metadatos, exige
supervisorfinished/exit0/sinviolación/error/grupovacío y coherenciarecibos/cargos/
planaceptado. Entonces sella6metadatosmásSHA/tamañoarchivo. No adoptarestado
internoverified sinseal. Archivos/fallos quedan retenidos enrootexclusivo.

Traséxito:Cargototal4.355.802.733B,queincluye16KiBsinarchivo; saldo7.644.197.267B.
Solo archivo deíndice: no extracción, FASTQ, HISAT2,piloto, PSI o efecto biológico.
Paso posterior de extracción/adopción requiere revisar procedenciaycontabilidad;
no se puede relanzar eljobviejo o presentar elrestablecimiento comoanálisis.

## Validación

23tests nuevos: HTTPloopbackreal coníndice/prefixsintéticos pequeños. Recuperación
positiva conservaoriginal, rangoúnico, SHAcompleto/cargocon16KiBextra; rechaza
200/rango/tamañoduplicado/versión/encoding/chunked/redirect,truncado,SHAincorrecto,
prefixalterado,cambiooriginaltrasHTTP, reutilizaciónroot,caps/aceptaciónincorrecta.
Resultadointernocorrectoconrechazoexterno no se sella; externolimpio yrecibos
coherentes sí. CLI/worker real supervisadoconprefixsintéticocambiado se corta
antes deHTTP:exit1/grupovacío/soloCopyfailed/sincargosnuevos/sinsello. NoHISAT2.
Batería integrada259tests correctos sin fallos/errores/omisiones(236anteriores+23nuevos); compileallcorrecto. validation.json/tests.txt.

La primeraCIen78a53a7falló en2testsdepropuesta porque exigían33GiBfísicos alhostdeCI. Se corrigenfixtures para simular recursos yse añade uncontrol negativo explícito de disco32GiB. No se relaja elguardreal de33GiB. ci-initial-failure.txt conserva trazabilidad.

## Límites y siguiente paso

La respuestaS3real yelrendimiento no sehanprobado enestaentrega. Testsinyectan
fuente/tamañossintéticos a funcionesinternas; CLIreal validaURL/version/SHA/caps
pinadossin opcionesparacambiarlos. Conserva límitesmuestreados delsupervisor,
I/Oininterrumpible/procesosdesacoplados/muerteWindowsWSL/hosthostil; sincuotasduras.
HTTPbudgetesentitybody leído,noTLS/TCP/cabeceras/buffering. Configuraciones/recibos
locales previenen erroresaccidentales, no atacante concontrol totaldelhost.

Siguiente: Luisactualiza y emiteplan deshabilitado. Revisar resumen y aceptar
expresamente, si decide, nueva ventana40min antes de únicapeticiónS3. No pedir
ampliación abstracta de horas ni descartar elparcial. Si noacepta, trabajoqueda
preparado yno descarga. Estadofuente/parcial/ejecución01permanecen intactos.

Fuenteprimaria decontratoRange/206/Content-Range/versionId:
https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html
