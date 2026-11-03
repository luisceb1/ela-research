# Estado vigente — 03/11/2026

## Decisión vigente: piloto del control local preparado — 03/11/2026

Nuevo ejecutor aislado `offline_control_pilot.py`: reutiliza índice y R1/R2 sellados, verifica copias locales, valida todos los pares y procesa un prefijo fijo de un millón. Conserva HISAT2, el método pareado y el umbral de 20 grupos. Sin fases HTTP ni TDP; cargo constante de 7.322.807.977 bytes, incluida la reserva manual previa.

Propuesta: 3000 segundos (50 minutos), CLOCK_BOOTTIME en padre, trabajador y subfases; 2 CPU, RSS de grupo de 6 GiB muestreada, espacio virtual por proceso de 8 GiB, disco de 27 GiB y reserva de 8 GiB. Cuenta doce árboles y proyecta las dos copias antes de iniciarlas. Descriptor deshabilitado, SHA exacto y aceptación explícita; sin reintento automático.

485 pruebas locales correctas sin omisiones, incluidas 25 nuevas. Las integraciones usan miniaturas y SAM reproducido; no constituyen alineamiento humano ni benchmark. Informe: `reports/offline-control-preparation-20261103`.

Siguiente tarea: preparación y ejecución en WSL según `research/runbooks/2026-11-03-offline-control-powershell.md`. El sello distingue cobertura suficiente o insuficiente; ninguna habilita otra biblioteca o inferencia biológica. PR 36 abierta sin fusionar. Las cabeceras inferiores son históricas.

## Decisión vigente: R2 completo y sellado; preparar sólo control local — 03/11/2026

Luis aporta sealed_verified_ctrl_r2_elapsed:997549457B/MD5007d66223fe35f394284e4ebd631eaef/SHAb034affa4479b28154fa9217a943128c4513590f6e622690a7af7afd272ca2f6, plan36c64ad4… en código c23994f. Cargo7322807977B/saldo4677192023B incluye misma reserva manual997549457B no medida. Evidencia de usuario, sin acceso remoto ni duración/RSS aportados. Reporte y seis hashes en reports/ctrl-r2-sealed-20261103.

Índice/R1/R2 ya recuperados: no repetir descargas o relanzar workers que vuelvan a pedirlos. Todavía sin validación pareada/EOF, alineamiento, cobertura o datoTDP. La recuperación exitosa no prueba por sí sola causa exacta de fallos anteriores. Código previo460tests/CI ya verificado; esta actualización sólo documentación.

Siguiente única tarea: implementar/probar adopción y cómputo local sólo del control, sinHTTP/TDP, manteniendo1Mpares/filtros/targets/umbral20 y reloj transcurrido en todas las fases; revisar recursos antes de descriptor concreto. Plan research/plans/2026-11-03-offline-control-after-r2.md. Conservar cargos/linaje y pedir ejecución concreta tras preparar; sinmerge/conclusiónbiológica. Cabeceras inferiores históricas.


## Decisión vigente: corregir reloj antes de continuar R2 — 03/11/2026

Luis aporta corte temprano15,5266s, Externalclock/bodycap, grupo vacío y bytes dentro de12GB. Parcial900998714B/cargo7226257234B; quedan96550743B. Recibos apuntan a controlcivil, pero no registran valor exacto disparador/causaWSL. La prueba reproduce falsa alarma del guard anterior con retroceso civil. Evidencia reports/ctrl-r2-elapsed-clock-20261103.

Nuevo recover_ctrl_r2_clock.py conserva históricos y usa CLOCK_BOOTTIME/boot_id en padre/trabajador y sellador; fechas civiles sólo diagnóstico. Misma ventana2400s/copy300s/range1800s/verify300s y caps. Rechaza expiraciones reales/bootcambiado; padre muestrea tick tras leer estado concurrente. IPv4/TLS/Range/MD5 enteros conservados, raíz nueva ySHAexacto/aceptación delreloj. Cargo final esperado7322807977B, misma reserva de navegador ya incluida, sin duplicar. Disco27GiB onceárboles/reserva8GiB/2CPU/RSS512MiBmuestreada/AS1GiB.

Controles envalidation.json; positivos de recuperación con saltos civiles y negativos de vencimiento real, sellado, concurrencia yboot. Siguienteúnica tarea: descriptorWSL comprobado y ejecución explícita con research/runbooks/2026-11-03-ctrl-r2-elapsed-clock-powershell.md. No relanzar intentos, nuevosmates o alineamiento;sinmerge/conclusiónbiológica. Cabeceras inferiores históricas.


## Decisión vigente: Ctrl+C en R2; continuar desde 900 MB — 03/11/2026

Luis aporta parcial900375051B, recibo20971520B, cargoWSL6224513473B; supervisor−9/KeyboardInterrupt/grupo vacío. Navegador sólo74MB aproximados: se eligeWSL y se indica cancelar navegador. No se ha confirmado parada ni tráfico exacto. Quedan97174406B; sinMD5entero/alineamiento.

Nuevo recover_ctrl_r2_resume.py separado conserva históricos y reutiliza transporteIPv4/TLS y sellador. Propuesta: reserva de un archivo completo997549457B para navegador, separada deWSL; no es medición ni cota de retries externos. Cargo inicial propuesto7222062930B/final7319237336B bajo12GB. ExigeSHAexacto/ventana ybrowserdetenido/reserva aceptados. Reloj interrumpido reservado1800s completos, etiquetado conservador,no tiempo medido. Mismos2400s/1800sHTTP,27GiB diezárboles/reserva8GiB,2CPU/RSS512MiBmuestreada/AS1GiB/socket30s.

Controles/informe en reports/ctrl-r2-interrupt-resume-20261103. Siguiente única tarea: plan deshabilitado WSL según research/runbooks/2026-11-03-ctrl-r2-interrupt-resume-powershell.md y revisión de condiciones. No reabrir intentos ni datosTDP; sinmerge/conclusionesbiológicas. Cabeceras inferiores históricas.


## Decisión vigente: CTRL_R2 IPv4 parcial de 876 MB; tramo restante propuesto — 03/11/2026

Luis aporta parcial de 876.279.389 B y recibo de 591.396.864 B nuevos, bloque reservado de 4 MiB. Cargo acumulado 6.199.347.649 B; diferencia conservadora del último intento 4.111.506 B sin reembolso. Copia verificada, Range interrumpido al plazo de 5400 s; supervisor−9/grupo vacío. No MD5 entero, pares o alineamiento. Evidencia en reports/ctrl-r2-final-range-20261103.

Nuevo recover_ctrl_r2_final.py aislado audita la cadena y reutiliza sin cambios el transporte IPv4/TLS y sellador previos. Sólo faltan 121.270.068 B. Cargo final esperado 6.320.617.717 B bajo12GB. Conserva reloj anterior y arrastra los5400s agotados completos:12700,072928190231s, sin reconstruir instante final. Históricos intactos.

Propuesta pendiente2400s total/1800sHTTP, mismos27GiB nueveárboles/reserva8GiB,2CPU/RSS512MiBmuestreada/AS1GiB/socket30s. SHA exacto y aceptación explícita. Controles en validation.json, incluidos TLS previos. Siguiente tarea única: emitir/revisar plan deshabilitado con research/runbooks/2026-11-03-ctrl-r2-final-range-powershell.md. No relanzar intentos; sin merge o conclusiones biológicas. Cabeceras inferiores históricas.


## Decisión vigente: CTRL_R2 fallo TLS sin cuerpo; recuperación IPv4 propuesta — 03/11/2026

Luis aporta fallo dehandshakeTLS de recuperación532778b6…: copia verificada,0B nuevos/cargo5603756481B,32,35191988945sderango,supervisorexit1/sinviolación/grupovacío. HEADWindows200/WSLdefaulttimeout/WSL-4HTTP200y tamaño997549457. Apoya probarIPv4, no demuestra causaIPv6 ni garantizaRange/rendimiento. Evidencia reports/ctrl-r2-ipv4-20261103.

Nuevo recover_ctrl_r2_ipv4.py aislado audita cadena previa/copia/log/cargos y0cuerpo; HTTPSAF_INETconcertificado/hostnameTLSactivos yuna peticiónRange712749730B, MD5entero yexternolimpio antesdesello. Históricosintactos;ningúncambioDNSglobal/WSL. Conserva7267,7210083s+tiempoderangofallido;techo12GB/cargofinalesperado6316506211B. Propuesta pendiente6000s/5400sHTTP,mismos27GiB ochoárboles/reserva8GiB,2CPU/RSS512MiBmuestreada/AS1GiB/socket30s. ExigeSHAexacto yaceptaciónexplícita deventana.

Pruebas ycontroles envalidation.json,incluidoTLSreal localIPv4,CA/hostnamerechazados yrecuperacióncompleta artificial. Primera incompatibilidadPython3.12 detectada/corregida/documentada, sin tocar históricos. SinHTTPENA/alineamientohumanoenhostdelagente. Siguientetareaúnica: emitir/revisarplandeshabilitado conresearch/runbooks/2026-11-03-ctrl-r2-ipv4-powershell.md. No relanzarjobviejo;sinmerge/conclusionesbiológicas. Cabecerasinferioreshistóricas.


## Decisión vigente: CTRL_R2 interrumpido; recuperación aislada propuesta — 03/11/2026

Luis aporta snapshot y stat: CTRL_R2 parcial284.799.727B, recibo281.018.368B, reserva4MiB. Cargo nuevo285.212.672B,total5.603.756.481B;412.945B conservadores sin reembolso. Preflight/R1 verificados; supervisor−9 por cap1800s/grupo vacío. Sin pares/alineamiento/TDP. Snapshot1773,5246675s no es cierre final; discrepancia con monotónico sin causa demostrada. Evidencia en reports/ctrl-r2-recovery-20261103.

Nuevo recover_ctrl_r2.py separado conserva identidades anteriores. Copia/hash de prefijo y una peticiónRange712.749.730B, MD5/tamaño enteros antes de promoción y externo limpio antes del sello. Cargo final esperado6.316.506.211B bajo12GB. Arrastra conservadoramente1800s previos completos más5467,7210083s, manteniendo snapshot original; no inventa reloj final.

Propuesta pendiente: NUEVAventana6000s/5400sHTTP (100/90min), socket30s, disco27GiB siete árboles/reserva8GiB,2CPU/RSS512MiBmuestreada/AS1GiB. ExigeSHAexacto yaceptación expresa; no activa/reinicia piloto ni procesa otros mates. Pruebas y controles en validation.json. Siguiente tarea única: emitir/revisar plan deshabilitado WSL mediante research/runbooks/2026-11-03-ctrl-r2-recovery-powershell.md. Sin merge ni conclusiones biológicas. Cabeceras inferiores históricas.


## Decisión vigente: CTRL_R1 sellado; piloto nuevo desde recuperación — 03/11/2026

Luis aporta sealed_verified_ctrl_r1:960856963B/MD5ed58daa011d6508a3e8d1f05bc39fc29/SHA298a8b4769fcd5434f883706c873d56795c5a20d855917d80a391b2e5c38beff. Cargo5318543809B/saldo6681456191B. Evidencia de usuario, sin tiempos/RSS de recuperación aportados ni acceso remoto. reports/recovered-read-pilot-20261103/user-reported-recovery-seal.json.

Nuevo recovered_read_pilot.py aislado conserva intactos trabajadores/identidades históricos. Valida cadena, copia/hashCTRL_R1 sinHTTP y reutiliza motor pareado/índice/argv/streamPE. Sólo3HTTPrestantes5388846918B, CTRL_R2 antes decomputeCTRL;TDP condicionado a cobertura20. Cargo final mínimo10707390727B bajo12GB. Contador y tiempos históricos se heredan, no se resetearán ni reabrirá root fallido.

Nueva ventana propuesta7200s/1800s transferencias incluyendo copia local≤180s; sockets30s. Disco propuesto27GiB(antes25)/artefactos18GiB(antes16) para preservar parciales/copia960MB;reserva8GiB y demáscapsCPU/RAM/temporales conservados. RequiereSHA exacto y --accept-new-window-and-disk. Preparación no autoriza.

Validación en reports/recovered-read-pilot-20261103; fixtures de copia/corrupción/cargos/orden/cobertura/sello/HTTPtimeout yCLInegativo antesdered. SinHTTP humano/alineamiento enhost delagente. Siguiente tarea única: emitir plan con research/runbooks/2026-11-03-recovered-read-pilot-powershell.md yrevisarJSON/recursos antes deaceptar. Sin conclusiones biológicas/merge; cabeceras inferiores históricas.

## Decisión vigente: timeout de CTRL_R1; recuperación del mate aislado — 03/11/2026

Luis aceptó plan15f85f9d… en49f37a0. Índice preflight verificado; CTRL_R1 timeout, supervisor exit1/sinviolación/grupo vacío. Recibo354.631.727B, cargo nuevo356.515.840B, total4.712.318.573B. Diferencia1.884.113B sin reembolso;4.272,2037699222565s históricos. No otros mates/alineamientos. Evidencia en reports/ctrl-r1-recovery-20261103/user-reported-failure.json.

Nuevo recover_ctrl_read.py prepara descriptor deshabilitado: audita metadatos ypartialSHA, copia comprobada, una peticiónRange606.225.236B, sóloMD5/tamaño enteros permiten promoción yexterno limpio sella. Nueva ventana propuesta2400s/1800sHTTP, socket30s, necesitaSHA yaceptación explícita. No modifica intento ni contador anteriores; cap12GB,512MiBRSSmuestreada/1GiBAS,2CPU,25GiB cinco árboles/reserva8GiB. Sin red real del agente/otros mates/descompresión/alineamiento.

308 pruebas locales pasan sin omisiones(289+19). PositivoHTTP local y negativos; trabajadorCLI falla antes de red/grupo vacío. Dos fallos iniciales de fixtures conservados ycorregidos sin debilitar guardas. Informe reports/ctrl-r1-recovery-20261103/REPORT.md.

Siguiente tarea única: emitir plan enWSL según research/runbooks/2026-11-03-ctrl-r1-recovery-powershell.md y revisarJSON antes de aceptar nueva ventana. Después del sello quedará adopción del mate/cargos por el piloto. No relanzarjob ni resetear. PR36 abierta/sinmerge. Cabeceras inferiores históricas.

## Continuidad comprobada y ayuda offline opcional — 03/11/2026

El piloto desde caché sigue pendiente del descriptor deshabilitado y su revisión en WSL; no se ha recibido aquí ni se ha aceptado la nueva ventana. Se mantiene la tarea real definida abajo y el runbook existente, sin introducir un gate obligatorio adicional.

Añadida ayuda opcional audit_cached_pilot_descriptor.py para revisar campos estáticos del descriptor sin seguir sus rutas/URLs ni ejecutar procesos. La propuesta archivada conserva cargo4355802733B y margen1294493386B; cuatro mates6349703881B cotejados.16tests locales/compileall y22mutaciones negativas rechazadas; resultados repetidos idénticos para un descriptor explícitamente artificial. Informe reports/cached-plan-review-20261103. No es validación del host, código/binario/sellos, manifiesto completo o autorización; todas las salidas mantienen ejecución/readiness/autorizaciónfalse. No datos, descargas o alineamientos nuevos; código del trabajador intacto.

Próximo paso real sin cambios: descriptorJSON ySHA de WSL, revisión concreta y decisión expresa sobre la ventana nueva; no relanzar trabajo antiguo ni renovar cargos/plazos. PR36 abierta, sin merge. Cabeceras inferiores conservan historia y límites científicos.

## Decisión vigente: índice extraído y sellado; preparar piloto desde caché — 02/11/2026

Luis confirma `sealed_verified_extracted_index`, nueve miembros y cero bytes nuevos de descarga. Cargo acumulado 4.355.802.733 B; saldo 7.644.197.267 B. Evidencia de terminal aportada por Luis en reports/cached-index-pilot-20261102/index-seal.user-reported.json; sin acceso directo al host.

Nuevo cached_index_pilot.py: prepara plan deshabilitado, enlaza y verifica sellos/miembros/binario/código; reutiliza fases pareadas y stream compacto. Cero descarga/copia/extracción del índice. CTRL primero y TDP sólo si supera cobertura fija. Nuevo plazo propuesto 7.200 s y HTTP adicional 1.800 s, requiere SHA y aceptación expresa de ventana. Conserva cargo previo, 3.748,515794 s históricos y plazo viejo sin modificar. Cuatro RAW suman 6.349.703.881 B, mínimo final 10.705.506.614 B bajo techo original de 12 GB. Disco suma todo el linaje; caps de RAM, CPU y temporales conservados.

289 pruebas locales pasan sin omisiones, incluidas 16 nuevas y fallo real del trabajador sustituto antes de HTTP. Se conservan dos errores iniciales de fixture y su corrección. No FASTQ ni alineamiento humano en el host del agente; rendimiento y cobertura reales pendientes. Informe reports/cached-index-pilot-20261102/REPORT.md.

**Siguiente tarea única:** emitir plan deshabilitado en WSL con research/runbooks/2026-11-02-cached-index-pilot-powershell.md y revisar JSON antes de ejecución explícita. No reiniciar job viejo ni presupuestos. PR36 abierto, sin merge. Sin conclusiones biológicas. Cabeceras inferiores históricas.

## Decisión vigente: archivo recuperado verificado; extracción local preparada — 02/11/2026

Luis aporta sello real delarchivo4355786349B/SHA1848784403a0fb3ee7735b2f891d8be96fd2782e08aed3d8212d922666f077a5. Recibosnormalizados de recovery-resultyexternocoincidenconSHAenelsello. Tramo2723339065B/148,515s≈18,34MB/s;total167,457s,RSS26,81MiBsolo descargador,exit0/sinviolación/grupovacío. Cargo4355802733B/saldo7644197267B,conserva16KiBprevios. Evidencia deusuario,noaccesoremoto niíndiceennuestrohost; sinatribucióncausaldevelocidad. reports/local-index-extraction-20261102/recovery-review.json.

Nuevo prepare_verified_index.py: paso solo local≤900s(120preflight+600extract+120inspect+60margen),0red,2CPU,6GiBRSSglobal/8GiBAS;fases512MiB/1GiB/6GiBRSS y1/2/8GiBAS. Hasharchivo/recuperaciónsellada,binarionativo2.2.3,extracciónacotadaexactadenuevearchivos/CRC,rehashfuente/salidas e inspectorchr19/58617616. Rootderivadoexclusivo,noadopta/reiniciafallos; padresolometadatos,aceptaciónexterna yseal final. Disco≤25GiBsumando3árboles,reserva8GiB. No cambia cargos/plazosviejos,ningúnFASTQ oalineamiento.

273tests locales pasan sin omisiones(259anteriores+14nuevos),compileallcorrecto. Positivosconarchivosminiaturasfalsosyproductores/resúmenes sustitutos, noíndiceHISAT2real. CLIworkerconELFPythonfalla porversiónantesdeleerarchivoesparcido(sólosimula tamaño),preflightfailed/exit1/grupovacío/sinextracción/red. Metadatostamper,caps,fuente,inventario/CRC,externofallidoyrootreuse rechazados.

**Siguiente tarea única:** Luis actualiza y ejecuta extracciónlocal desdearchivoya recuperado, devuelveJSONsello oerror. Runbook research/runbooks/2026-11-02-offline-index-powershell.md. Despuésadopción delíndice/recibos/cargos paraseguirpilotoconlecturassinredescargarS3. No relanzar jobviejo/noextracciónmanual. Sin nuevodescargaalineamiento ennuestrahost,contactos/costes/merge. raw_execution_ready=false. Cabecerasinferioreshistóricas.


## Decisión vigente: candidato de recuperación del índice porRange preparado — 02/11/2026

Luis devuelve auditoría consistente: parcial1632447284B/SHAaf7750fc6ef148017aab8c339de670faebff34be5de69bddc0275dbeed21216d; cargo1632463668B, diferencia16384Bsinreembolso; supervisor−9/grupovacío. Identidad deparcial, no verificación delorigen. Registro reports/index-range-recovery-20261102/user-reported-audit.json.

Nuevo recover_index_range.py prepara jobdeshabilitado ligado a auditoría/código/Python/origen/caps. Copia/hashdelprefijosin tocaroriginal; única peticiónRangebytes1632447284–4355786348 exige206/Content-Range/Length/versionexactos,sinredirect/retry; soloSHAentero correcto promueve y soloexternolimpio sella. Rootderivadoúnico no admiteotraejecución. Nofastq/extracción/alineamiento.

Propuesta deNUEVAventana2400s(300copia/auditoría+1800transporte+300verificación), pendiente deaceptaciónexpresa por--accept-additional-time-windowySHAexacto. Originaldeadliney3600sgastados no se alteran. Cap12GBsin aumento y cargoprevioincluido; traséxito4355802733Bcargados/saldo7644197267B. Disco25GiBcuentaambosárboles+8reserva,2CPU,512MiBRSSmuestreado/1GiBAS. No ejecuciónS3real aquí.

259tests seleccionados pasan sin omisiones(236anteriores+23nuevos), compileall. Rangospositivos usaníndices pequeñosHTTPloopback; contratos no acreditanS3/tiemporeal. Rechazo200/rango/versión/tamaño/SHA/redirect/truncado,cambiooriginal,exteriorfallido yexigenciaaceptación. WorkerCLIreal conprefixsintéticocambiado cortaantesHTTP:0cargonuevo,copyfailed,exit1/grupovacío/sinsello. PrimeraCI78a53a7falló en2fixturesqueexigían33GiBdelhost; corregidasaislandorecursosycontrolnegativodisco32GiB,sinrelajarguardreal; fallo conservado.

**Siguiente tarea única:** Luisemite planrecuperación deshabilitado y devuelve resumenSHA. Revisar ydecidirexpresamente sobre esos40min adicionales yúnicapetición delíndice; aún no aceptados. Comandos en research/runbooks/2026-11-02-index-recovery-powershell.md. Despuésde restauraciónse necesitará adopción/extracción/pilotorevisados: no relanzar jobviejo. PR36sinmerge/contactos/costes, originalintacto, sinnuevosdatosreales/alineamientos. raw_execution_ready=false. Cabecerasinferioreshistóricas.


## Decisión vigente: primer intento real detenido durante índice; auditoría del parcial — 02/11/2026

Luis ejecutó a3f76b4 con planSHA d813b5d5c738f8391583446df54b744c7987516309aadb5c64eec7ff912bf878. Preflightverified; solo index_archivestarted;1.632.463.668bytes cargados y3600,001265sde transporte agotados. Parcial≈1,6GsinSHA/tamañoexacto aún; logdelworker vacío, padre informa límite acumulado. No índice completo, FASTQoalineamiento. No interpretar como falloHISAT2. Evidencia aportada porusuario enreports/interrupted-index-transport-20261102/user-reported-failure.json.

Descargadorlegacyguardaba3metadatosduraderosporlectura; optimización opt-in reserva bloques4MiBantesdelecturas≤64KiB, conserva guardas y cargo conservador trasSIGKILL/excepción. Microbenchmark8MiBconread1de16KiB:3082→22fsync, mismoSHAybytes;2,54→0,14sen nuestrofilesystem, no medidaWSL/red delusuario. Causa develocidadoriginalno establecida. Entrada sintética antigua conserva comportamiento; nuevo modo cambia identidad/manifesty no admite el plananterior.

236tests seleccionados pasan sin omisiones(222anteriores+8bloques+6inspector), compileallcorrecto. Nuevo inspect_interrupted_pilot.py solo lee: verifica aceptación/fingerprint/recibos, SHA/tamaño delparcialy presupuestocargado. No promociona, reanuda, haceRange/HTTP, borra o renueva límites.

**Siguiente tarea única:** Luis ejecuta auditoríaread-onlyy devuelveJSON. Después preparar recuperación explícita y revisión de tiempos: el3600stransporte está agotado y no se restaura alactualizarsoftware. Reutilizar parcial requeriría diseñoRange/206ySHAcompleto, aún no implementado. No recrear directorio/planpara eludircap o descargar de cero; conservar ejecución01intacta. PR36abierta,sinmerge/contactos/costes/nuevasdescargas/alineamientos. raw_execution_ready=false. Cabecerasinferioreshistóricas.


## Decisión vigente: candidato real preparado para WSL; validación humana pendiente — 02/11/2026

Usuario confirmó201tests correctos en su WSL, Python3.12.3/PySAM0.23.3, RAMWindows15,8GiB, WSL7,6GiBtotal/7,1disponible y C:613,2GiBlibres. Evidencia aportada por él, no inspección remota. Nuevo CLI separado real_pilot_workflow: --host/--prepare no descargan ni alinean; --execute exige aceptación SHA256exacta del archivo preparado y rootnuevo. Política real solo con opt-in explícito; entradas sintéticas mantienen sus guardas. Se fijan orígenes,5transferencias,2bibliotecas,1Mpares y umbral20; no argvlibre o override de presupuesto.

Corregido supuesto anterior de pasar gzipdirecto a hisat2-align-s: stagingplano acotado2GiB, colación4GiB dentro de temporales6GiB; stdoutSAMsolo pipe. Índiceextraído/verificado y resumenchr19porinspector antes de cualquier FASTQ; probe120s ocupa margen previo, envolvente8640s, mismo9000global. Supervisor publica identidad de grupo en recibo.started. Sellado/revalidación conservan deadliney bloquean adopción de fallos.

222tests seleccionados locales pasan sin omisiones (201anteriores+20ruta nueva+1supervisor); compileall. Control CLIreal con ejecutablePythonrenombrado falla por versión antes deHTTP:0bytes, solo preflightfailed, supervisor1/grupovacío, sinsello; no es alineamientoHISAT2. Controlespositivos del adaptador sustituyen productorconSAMsintético, no acreditan genoma humano. Informe reports/wsl-real-pilot-preparation-20261102 y runbook research/runbooks/2026-11-02-wsl-pilot-powershell.md.

**Siguiente tarea única:** Luis instala fuenteHISAT2fijada (aligner+inspector), emite configuración deshabilitada ligada a su host y devuelve diagnóstico/SHApara revisión. Después decisión expresa sobre ejecución acotada. No nuevas simulaciones salvo fallos/cambios. Índice/dialecto/compatibilidad/recursos humanos siguen sin ejecutar en este host. Sin descargas biológicas/alineamientos/contactos/costes/merge en esta entrega; raw_execution_ready=false. Las cabeceras inferiores son historia.


## Decisión vigente: B1 integrado y sellado localmente; B5/activación pendientes — 02/11/2026

Worker fijo encadena4HTTPloopback,archivo,prefijos y productor/consumidor; solo se acepta tras sello padre de descriptor/ledger/resultado/recibo externo. 201tests locales pasan (18nuevos+183existentes), compileall; reports/sealed-local-workflow-20261102. Revalidación supervisada conserva ledger y no descarga. Productor no-cero/bloqueado, capRSSde fase y fallo externo trasresultado interno impiden sello. Siete fases,7.890bytes,9pares y6grupos objetivo en replay; no alineación nueva.

B1integración sintética verificada: índice de ocho miembros es placeholder, productor compara nombres/reproduce SAMexistente; no prueba uso de índice/FASTQpara alinear. ArgvHISAT2fijo preparado/pinado pero ejecución realrechazada antes de acceder a entradas. B5host/índice/dialecto/dependencias y puerta de activación revisada/decisión expresa pendientes. Producción=false,raw_execution_ready=false.

**Única siguiente tarea:** preflightB5de solo lectura del entorno disponible y paquete concreto de activación (rutas/hashes/orígenes/argv/caps/bloqueos). Sin descargar índice/FASTQreal, nueva alineación o activar producción. PR36abierta, sin merge/contactos/costes. Cabeceras inferiores son historia.

## Decisión vigente: B4 cerrado localmente, B1/B5 pendientes — 02/11/2026

Política opt-in ligada a fingerprint: total/transporte acumulado/fase/subfase, RSS/AS explícitos y particiones de disco; cómputo ligado a fuente/objetivos/decoder+scripts/recibos y rehash. 183tests locales pasan (20nuevos+163existentes), compileall; reports/b4-ledger-policy-20261102. Worker bloqueado se corta por guarda padre≈1,097s para productor1s; exit−9, sin vivos, ledger.started conservado. Cache mantiene plazos/consumo; cambios y commits expirados fallan.

Cobertura prospectiva: mínimo20grupos aceptados(RG,QNAME) con≥1objetivo a15; suma por evento separada, no moléculas únicas. Fixturedoble apoyo=unión1/suma2; wildunión6 insuficiente bloquea iniciar fase nueva sin ampliar. Borrador anterior queda histórico. Política humana9000s/3600stransporte,envolvente8520s;25GiB particionados24,75yreserva8;2CPU;6GiBRSSgrupo/8GiBASproceso en cómputo, solo planificación sin benchmark.

**Única siguiente tarea B1:** worker fijo de procedencia prefijos/índice/alineador/stream/conteo y orígenes exactos, probado solo con productores/servidores sintéticos locales y producción deshabilitada. B5entorno/índice y decisión de ejecución pendientes. raw_execution_ready=false; sin URLsreales, FASTQbiológico, índice humano, nuevo alineamiento/contactos/costes/merge. Cabeceras inferiores son historia.

## Decisión vigente: B3 cerrado localmente, tres puertas pendientes — 02/11/2026

Flujo SAM→metadatos/eventos JSONderivados→merge acotado→conteo objetivo/QC, sin guardar SAM/SEQ/QUAL/CIGARoriginal. Texto/HTSlib decodifican por separado a15/8; metadatos concordantes y reducción compartidos. 156tests locales pasan (19nuevos+137existentes);4SAMsintéticos existentes comparados con baselines, resultados repetidos idénticos. Fuente8SAMcotejada por blobs y SHA. Productor no-cero rechaza EOF; pipebloqueada se corta≈1,010s y termina2procesos sin vivos, recibo.started no se adopta. Informe reports/compact-pe-stream-20261102. Sin nueva alineación, índice humano o FASTQreal.

B3componente local, no integración humana. QuedanB1worker externo,B4ledger/caps/relojes/temporales/RLIMIT_AS/cobertura yB5entorno real. DependenciaPySAMobligatoria, workflowPEejecuta19nuevos+17previos con pin. raw_execution_ready=false; producción deshabilitada.

**Única siguiente tarea B4:** ligar cómputo a manifiesto/ledger, cerrar límites globales y de fase, disco temporal/dependencias, memoria RSS/AS, reloj de transporte y semántica de cobertura. Solo preflight/dry-run sintético, sin descarga, nuevo alineamiento, contacto/gasto o merge automático. Cabeceras inferiores son historia.

## Decisión vigente: B2 cerrado localmente, cuatro puertas pendientes — 02/11/2026

Checksum con tamaño y al menos MD5/SHA256 fijado; todos los aportados se verifican. DryRunner.archive liga inventario/caps/SHA256/recibos al ledger, valida cabeceras/tamaños/hash/EOF-CRC y rehashea al reutilizar. 118tests locales pasan (39nuevos+79existentes), compileall correcto; recibos HTTPlocal→archivo→reapertura y corte externo retenidos en reports/archive-ledger-local-20261102. Corte≈1,008s termina2procesos sin miembros vivos; started/partials conservan presupuesto/plazo y bloquean reapertura. Error inicial de generadorUSTAR documentado y corregido, no se relajó extractor.

B2solo componente local: regular tar y padres esperados, PAX/GNUextensiones/enlaces rechazados. Índice humano real no restaurado ni dialecto verificado. B1/B3/B4/B5 siguen pendientes; readiness-delta.json conserva auditoría anterior como snapshot. Producción deshabilitada, raw_execution_ready=false.

**Única siguiente tarea B3:** flujo/colación/conteo compacto y acotado sin SAMgenómico completo, preservando fragmentos/QC y doble decodificación. Usar SAMsintéticos existentes bajo supervisión, sin nueva alineación, índice humano o FASTQreal. Sin contactos/gastos/merge automático. Cabeceras inferiores son historia.

## Decisión vigente: auditoría integrada completada, cinco puertas pendientes — 02/11/2026

28fuentes cotejadas en01957248,19comprobaciones y3sondas offline; informe reports/pilot-readiness-audit-20261102. Contratos PE/referencia, minigenoma funcional, FASTQ/ledger y supervisión local ya acreditados en su ámbito; no repetirlos sin cambios. HISAT2 local conserva hashes y --version2.2.3, índice humano ausente, PySAM solo vía pe-deps explícito. Transferencia base10.705.490.230bytes; margen1.294.509.770 hasta12GB; disco base15.369.533.468bytes sin prefijos/temporales. No benchmark humano.

Cinco puertas: B1ruta externa/producción deshabilitada; B2índiceSHA256solo incompatible con MD5 obligatorio y extracción sin ledger; B3pipeline sin SAM genómico completo pendiente; B4reloj global/caps de fase/temporales/RLIMIT_AS y cobertura por evento pendientes; B5entorno/índice/PySAM. execution-proposal.json es diseño no ejecutable y propone9000s totales para revisión, sin cambiar límites activos. raw_execution_ready=false.

**Única siguiente tarea:** B2: admitir checksumSHA256solo y extracción de archivo sintético acotada por miembros/tamaños/hashes, ligada al ledger y con recibos/interrupción. Sin índice humano, FASTQreal, alineamiento, contactos, gastos o merge automático. Cabeceras inferiores son historia.

## Decisión vigente: supervisión externa local ejecutada — 02/11/2026

Worker fijo HTTP loopback/paired bajo supervisor externo; cortes en cabeceras, cuerpo, goteo y validador detenido con descendiente dejan cero miembros vivos. 79tests locales pasan (12 nuevos+67 existentes), recibos y logs retenidos en reports/external-local-supervision-20261102. Reserva duradera previa a read evita subcontabilizar por SIGKILL; consumo puede ser conservador y recibos internos started bloquean reapertura. Timeout monotónico recortado al plazo persistente, con latencia observada de sondeo/limpieza; no garantía de tiempo real o spawn bloqueado. Producción deshabilitada; sin crudos, índice o alineamientos.

**Única siguiente tarea:** auditoría integrada de preparación del piloto sin descargas: contratos, recursos, fases, binarios/referencias/recibos; lista cerrada de bloqueos y propuesta de ejecución revisable antes de habilitar producción. raw_execution_ready=false. PR36 abierta y sin merge automático. Cabeceras inferiores son historia.

## Decisión vigente: integridad ligada al ledger — 02/11/2026

Fase paired_fastq integrada al manifiesto y recibos de transferencia/HTTP. Rehash completo streaming, recibos finales y prefijos cotejados al reabrir. 67 tests locales pasan (19 nuevos +48 existentes); salida dura deja started/partial y bloquea reanudación. Fixture ejecutado conserva 102bytes y deadline original; reloj inyectado, no benchmark. Informe reports/paired-fastq-ledger-20261102. Sin crudos biológicos, índice o alineamientos; producción deshabilitada.

**Única siguiente tarea:** supervisión externa del transporte HTTP y validador con servidor local lento/bloqueado y sintéticos; cortes, limpieza y recibos/consumo persistentes tras interrupción. Sin descargas reales o restaurar índice. raw_execution_ready=false; PR36 sin merge automático. Cabeceras inferiores son historia.

## Decisión vigente: integridad paired local y límites explícitos — 02/11/2026

Ejecutado el siguiente gate de PR36 con fixtures locales: tres pares escaneados hasta EOF/CRC y prefijo determinista de dos; corrupción posterior al prefijo rechazada. Validador de cuatro líneas, mates/nombres/etiquetas y hashes; recibo final atómico y prefijos con fsync. 48 tests locales seleccionados (29 nuevos+19 existentes), compileall; no equivalen a suite completa o experimentos. Informe reports/paired-fastq-local-20261102.

El runner admite límites explícitos ligados a caps/firma de fase. Configuración900s/6GiB comprobada solo en plan; producción se rechaza y el fallback5s/128MiB queda sintético. No datos biológicos, índice humano, alineamientos, gastos o contactos. No se certifica unicidad global de nombres ni codificación Phred. raw_execution_ready=false.

**Única siguiente tarea:** conectar el validador como fase del ledger/manifiesto con recibos de transferencia y pruebas locales de interrupción/reanudación/identidad; sin FASTQreal o restauración de índice. Debe rechazar prefijo parcial, hash cambiado y límites nuevos conservando deadline/consumo. PR36 sigue revisable y sin merge automático; las cabeceras inferiores son historia.

## Decisión vigente: transporte HTTPlocal validado — 02/11/2026

Adaptador HTTPacotado con servidor127.0.0.1y lector instrumentado:9tests pasan. Lecturas limitadas al saldo/restante/chunk, retriesexplícitos cobrados, truncamiento/hash/redirectrechazados y recibos por intento. Informe reports/bounded-http-local-20261102. Presupuesto de cuerpo leído, NOtráfico TCP/TLS/cabeceras o buffering; no se acredita red externa/deadlineestricto de socket.

Preflight metadatos fija4mates+índiceversionado/hashes,10.705.490.230bytes mínimos de cuerpo; no descargas. DryRunner.processsiguelimitado a5s/128MiBsintéticos, no puede ejecutar índice humano. Integridad gzip/mates/prefijo/fases humanas pendientes. **Única siguiente tarea:** fixturesgziplocales paraEOF/CRC/sincronización/prefijo y parametrización explícita de límites de proceso del plan en dry-run. Sin FASTQbiológico/índice/alineación. raw_execution_ready=false; PR36sin merge automático. Las prioridades inferiores son historia.


## Decisión vigente: runner simulado integrado — 02/11/2026

pilot_dry_runner.py integra supervisorv2, hash de manifiesto/límites, deadline persistente, ledger de bytes acumulados, guardas de disco/reserva y fases atómicas. Diez tests pasan; simulación y reanudación idénticas, sin nueva transferencia. Fases.failed/startedbloquean continuación; solo archivos/recibos revalidados se reutilizan. Informe reports/pilot-runner-dry-20261102. No HTTPni comandos humanos expuestos enCLI; no crudos/alineamientos.

**Única siguiente tarea:** adaptador HTTPacotado y preflight de manifiesto real mediante transporte simulado/local, sin usar URLsdeFASTQni índice humano. Acotar lecturas a saldo, contabilizar fallos/reintentos y fijar referencias/binarios/fases por hash antes de ejecución. El iterable simulado puede entregar un chunkmayor que saldo y solo permite detectarlo/contarlo: no se certifica límite de red estricto. RSS/disco son watchdogmuestreados. raw_execution_ready=false; PR36sin merge automático. Las prioridades inferiores son historia.


## Decisión vigente: supervisor v2 validado con procesos sintéticos — 02/11/2026

Causa de RSSidentificada: PIDdePython y procfsen namespaces distintos. Nuevo scripts/process_supervisor_v2.py obtiene identidad procfsdelhijo; mide grupo y termina descendientes. Casos conocidos32MiBy2×24MiBdan≈40/65MBRSS; cortes memoria/timeouty limpieza pasan. Recibos individuales atómicos con reserva exclusiva, sin lista read-modify-write. Informe reports/supervisor-repair-20261102;7tests. No se reconstruyen recibos ni RAMdel minigenoma antiguo.

Límite: vigilancia muestreada, no cgroupagregadoestricto; comandos no pueden detach/setsid; supervisorsecuencial. Procesos breves no medidos se marcan como tales. Pendientes disco/red/deadlineglobaly manejo de recibos.startedtras interrupción. **Única siguiente tarea:** runner del piloto con modo planificación/dry-run y controles simulados de presupuesto/hashes/reanudación. Sin índice humano, repetir alineaciones o descargar crudos. raw_pilot_ready=false; PR36sin merge automático. Las cabeceras inferiores son historia.


## Decisión vigente: minigenoma funcional pasa, supervisor pendiente — 02/11/2026

HISAT2v2.2.3compilado y ejecutado sobre referencia mínima, no índice humano. reports/unc13a-minigenome-20261102:12expectativas por fragmento concordantes, cuatro referencias, XS-para positivos sin --rna-strandness, multimapeo/hebra/motivo y anclas comprobados; colación externa lexicográfica funciona, dos tests añadidos. Decodificadores coinciden, política de pares compartida.

El supervisor NOqueda acreditado: RSSnulo/implausible en varias tareas y dos recibos ausentes al final de commands.jsonpese a logs/SAM/resultados presentes. Datos preservados sin reconstruir recibos ni reintentar. No certificar límite2GiBo integridad de todos los registros. Tiempo/disco/transporte observados dentro de límites pequeños; no extrapolar a humano. raw_pilot_ready=false.

**Única siguiente tarea:** reparar y comprobar monitoreo de árbol de procesos y persistencia atómica de recibos mediante procesos sintéticos conocidos y plan nuevo. Sin repetir alineaciones, índice humano o FASTQbiológico. No reutilizar el deadline/carpeta original como una ejecución nueva. PR36sin merge automático; sin clínica/contactos/costes. Las prioridades inferiores son historia.


## Decisión vigente: referencia UNC13A y ruta unstranded fijadas — 02/11/2026

Contrato en reports/unc13a-reference-strand-20261102. UCSC/hg38/GENCODEv47: canónica intrónica0-based[17641556,17642844),CEizquierda[17641556,17642413),CEderecha[17642541,17642844),hebra−,motivosCT/AC. Canónica apoyada por4transcritos;128bpentre brazos crípticos. Mismo proveedor para secuencia/anotación, no validación biológica. Pares históricos de límites exónicos1-based se convierten[a,b-1); no se modifican conteos o esquemas previos automáticamente.

La química del kit hace plausible RF, pero no acredita layout real. Ruta primaria prospectiva: omitir --rna-strandness, orientación físicaFR, exigir XS-por motivos y referencia. Aún sin prueba de alineador. **Única siguiente tarea:** research/plans/2026-11-02-unc13a-unstranded-minigenome.md, HISAT2y colación en minigenoma pequeño dentro de límites prefijados; sin índice humano o FASTQbiológicos. Si no recupera positivos/XScorrecto, detener sin elegir orientación por efecto. raw_execution_ready=false. PR36sin merge automático. Las cabeceras inferiores son historia.


## Decisión vigente: contrato PE sintético ejecutado — 02/11/2026

Implementado en scripts/pe_fragment_contract.py; informe reports/pe-synthetic-contract-20261102.17tests locales con PySAM0.23.3/HTSlib1.21 pasan;22comparaciones texto/HTSlib concordantes. Una unidad por fragmento/unión/biblioteca, pares recíprocos, exclusiones y anclas explícitas. Política de pares/reducción compartida: independencia solo en decodificación. Entrada lexicográficamente agrupada(RG,QNAME), límite16registros; colación externa aún pendiente. Legacy SE intacto, sin piloto real o alineador ejecutado.

**Única siguiente tarea:** puerta de referencia/orientación UNC13A mediante fuentes primarias pequeñas y controles sintéticos. Ensamblaje, hebra, geometría y FR/RF no están acreditados para las bibliotecas reales; si orientación irresoluble, fijar alternativa unstranded explícita antes de datos. No escoger por efecto. Después seguirá pendiente end-to-end/colación con supervisión. raw_execution_ready=false; no FASTQ, índice humano, merge automático, contactos, clínica o laboratorio. Las tareas inferiores son historia y el contrato PE ya no es pendiente.



## Decisión vigente: plan de piloto Humphrey preparado — 01/11/2026

Plan reproducible en research/plans/2026-11-01-humphrey-raw-pilot.md y reports/gse296714-raw-pilot-plan-20261101. Selección técnica de menor FASTQpor condición: CTRL-4/SRR33425816 y TDP-5/SRR33425819; cuatro mates6.349.703.881bytes, enlaces/MD5actuales ENA concordantes. No pareja biológica, no selección por efecto. Entorno cgroup8GiB,2CPUpropuestas,disco≈62,7GBlibres; alineadores no instalados. Límites y criterios de parada fijados; ninguna descarga de crudos, instalación o alineamiento.

**Única siguiente tarea:** contrato PE con controles sintéticos y dos extractores, según el plan. El extractor anterior rechaza read.is_paired. Deben resolverse doble apoyo de mates por fragmento, exclusiones/orientación, referencias y geometría UNC13A antes de restaurar índice o descargar datos. No tratar la disponibilidad de disco o la CI como piloto real viable. raw_execution_ready=false. No ampliar79GBni costes, no merge automático o clínica. Las cabeceras inferiores son historia.


## Decisión vigente: procesados UNC13A bloqueados — 01/11/2026

Puerta ejecutada y cerrada en reports/unc13a-humphrey-processed-gate-20261101. En cryptic_biology80fa3d7 se encontró la familia Humphrey en el compendio agregado (861filas,6UNC13A), pero no soporte ni identidad de las doce bibliotecas. Cero enlaces por muestra aceptados; no PSI, efecto o ausencia biológica inferidos. No repetir esta fuente o las auditorías cerradas SH-SY5Y/fraccionación/RiMOD.

**Única siguiente tarea propuesta:** preparar un plan de recursos y valor informativo para un piloto de crudos Humphrey limitado, sin descargar/alinear: selección técnica explícita, diseño paired-end, referencias, RAM/disco/tiempo y criterio de decisión. No asumir runtime de GSE122069, no ejecutar79GBni ampliar presupuesto automáticamente. Si no es viable, detener con bloqueo. STMN2TPM/PPAU permanece reproducida; mapa biológico de unidades pendiente. PR36sin merge automático; sin contactos/costes/clínica/laboratorio.

Las cabeceras inferiores conservan historia y sus tareas ya cerradas quedan sustituidas por esta decisión.


## Decisión vigente: PPAU STMN2 desde TPM reproducida — 01/11/2026

Fase ejecutada y cerrada en reports/stmn2-papa-tpm-reproduction-20261101. Concordancia en las 12 bibliotecas, diferencia absoluta máxima 4,440892098500626e-16 frente a tolerancia prospectiva 1e-6. Numerador TPM del grupo STMN2_1; denominador todos los grupos del mismo gene_id exacto en la matriz completa. Se recuperó solo el miembro TPM por Range/CRC/SHA; sin FASTQ o ZIP completo. El contraste con cuentas permanece fallido y sus artefactos conservan los hashes originales.

Etiqueta: reproducción aritmética de datos publicados por biblioteca, no nueva validación biológica, independencia de diferenciaciones, PSI de unión o función. Sin medias de grupos, p-valores o inferencia clínica. No repetir esta reproducción ni el contraste con cuentas como tareas pendientes.

**Única siguiente tarea:** puerta acotada de procesados UNC13A en las mismas doce bibliotecas, según research/plans/2026-11-01-gse296714-unc13a-processed-gate.md. Solo código/índices/cultivos, con límites de tamaño y sin datos post mortem; exigir enlaces y definición de evento antes de aceptar valores. No ejecutada en esta fase. Si no hay fuente apta, cerrar con bloqueo y no ampliar fuentes automáticamente. El mapa biológico/lotes sigue pendiente antes de inferencia.

Esta ampliación continúa la PR #36, sin fusión automática. Los encabezados inferiores son historia, incluida la tarea TPM que ahora queda completada. Ningún envío de correos, costes, laboratorio o indicación clínica.

## Decisión vigente: contraste con cuentas cerrado — 01/11/2026

Reproducción STMN2 ejecutada en reports/stmn2-papa-reproduction-20261101 sobre la misma PR #36, sin merge. La predicción preregistrada counts/suma(counts) = PPAU falla en las 12 bibliotecas (0 aceptadas, 12 rechazadas), diferencia absoluta máxima 0,17013297835212804; tolerancia 1e-6 intacta. Se preservan el denominador de todos los grupos STMN2, las doce bibliotecas y los resultados negativos. La salida correcta del programa y sus tests no acreditan concordancia de la hipótesis.

Código primario PAPA: la PPAU usa TPM/suma(TPM), mientras la exportación de cuentas usa lengthScaledTPM. La fórmula que propusimos anteriormente no era equivalente a la definición de autores. No se ha ejecutado una sustitución por TPM ni se ha corregido retrospectivamente el resultado. Tabla PPAU recuperada por Range/CRC/SHA sin ZIP completo o crudos. Mapa de diferenciaciones/lotes aún no reconstruido; sin promedios de grupos, p-valores, función o validación clínica.

**Única siguiente tarea:** ejecutar el nuevo plan prospectivo research/plans/2026-11-01-stmn2-papa-tpm-reproduction.md: recuperar solo TPM del mismo directorio; calcular grupo _1/suma de todos los grupos STMN2 y cotejar PPAU por biblioteca, misma tolerancia 1e-6 y sin inferencia. Esa fase aún no se ha ejecutado. Si falla, detener sin adaptar. No repetir el contraste cerrado con las mismas cuentas ni descargar FASTQ para resolverlo.

Las secciones siguientes conservan historia. La PR #36 anterior a esta ampliación pasó CI (415 tests observados en Python 3.12 y éxito también en 3.11); verificar nueva cabeza por SHA. No se autoriza merge automático, envío de correos, costes, clínica o laboratorio.

## Decisión vigente tras auditoría GSE296714 — 01/11/2026

Luis autorizó explícitamente la alternativa GSE296714 para avanzar al margen de los correos. Auditoría prospectiva ejecutada sobre main 6b0d420 (#35 ya fusionada); informe reports/gse296714-design-20261101. Doce bibliotecas (6 CTRL/6 KD) enlazadas GEO→SRX/SAMN→ENA y a tabla de autores. Matriz génica válida de 61.126 filas; tabla PAPA válida de 43.630 grupos, 12 columnas. STMN2: grupo críptico ENSG00000104435.14_1 enlazado a anotación curada y grupo de referencia _2; siete registros GTF, no siete réplicas. UNC13A: cuentas génicas y de grupos de exones finales disponibles, pero no sus uniones crípticas medidas.

Aptitud aceptada para descripción de abundancia génica y de grupos PAPA por biblioteca; no aceptada todavía para inferencia de unidades biológicas, nueva replicación independiente, rescate o función. La tabla de autores solo contiene muestra/condición/rutas, no diferenciación/lote/pares; no inferirlos de sufijos ni negar réplicas declaradas. La pérdida de TDP-43 precede a diferenciación, recogida día30. Proyecto ENA mezcla109runs; solo12 seleccionados. Crudos seleccionados79.276.637.720bytes según ENA: no descargados. ZIP Zenodo831.190.727bytes: solo índices y tres miembros por Range206/CRC; no ZIP entero ni MD5 global verificado.

**Única siguiente tarea:** fijar y ejecutar una reproducción descriptiva STMN2 por biblioteca de la proporción de abundancia estimada del grupo _1 respecto de todos los grupos de ese gen en PAPA, cotejándola con la tabla PPAU original del mismo miembro/familia. Prefijar denominador y comprobar enlace/identidad antes de leer PPAU. No PSI de unión, p-valores, promedios con independencia presupuesta, comparación clínica ni FASTQ. Si el cotejo falla, detener y documentar. No repetir auditoría/descargas ya cerradas. Los correos Keuss/Guo quedan en paralelo, sin envío autorizado ni dependencia para esta tarea.

La cabecera histórica siguiente sobre una única tarea de solicitud queda sustituida por esta decisión; sus límites científicos y las búsquedas cerradas se conservan. Esta entrega se propone en PR revisable, sin merge automático.


## Estado de integración y decisión vigente

PR #30 fusionada en main mediante 39e0479306c9e810f8bd3846bba7b79d7b49fba7; #33 mediante 95fea38d y #34 mediante 85135ba. La CI de main en 39e0479 pasó en Python 3.11/3.12 (404 tests observados en log 3.12). Esta entrega documental no presume CI nueva ni añade validación biológica. La rama histórica de #30 no se modifica.

Luis autorizó continuar el inventario funcional Keuss/Guo y reconciliar el planning. Auditoría terminada en reports/functional-source-access-20261101: dos familias, ninguna tabla numérica enlazada verificada. XML primario del preprint Guo recuperado y comprobado; PDF solicitado devolvió HTML; editorial final 403 y Scite solo acceso parcial. iGluSNFR3 fijado por commit: código, sin datos experimentales enlazados verificados. No estimación funcional, nueva replicación ni descarga masiva.

El calendario del preprint Guo comienza ASO antes de KD; no acredita inicio tras déficit medido. Las versiones se separan. Falta de acceso no demuestra inexistencia de datos ni dependencia de réplicas declaradas.

Único siguiente paso: revisar DATA_REQUEST_SPEC.md y preparar, si procede, una comunicación concreta solo con autorización expresa de envío. La especificación ya está escrita, no hay que repetirla. La búsqueda de estas dos familias se cierra; reabrir solo con enlace numérico concreto, nueva versión o respuesta autorizada. Sin nueva evidencia no repetir índices/PDF/Scite, QC STMN2 ni sensibilidades RiMOD/NYGC. Si se opta por otra pregunta, fijar prospectivamente una única alternativa antes de ejecutarla.

El gate distingue reproducir un desenlace funcional (requiere tabla con unidad/grupo/tiempo) de relacionarlo con RNA/proteína (exige además enlace entre ensayos). El archivo FUNCTIONAL_RESCUE_DATA_GATE.md contiene esta aclaración; no exige misma célula.

Los apartados inferiores conservan historia. Cualquier mención a #30/#33 abiertos, merge pendiente, próxima descarga o CI pendiente de fases anteriores queda superada por esta cabecera. Este PR es revisable; no se fusiona automáticamente. Sin contactos, costes, datos personales, clínica o laboratorio.

## Fase actual cerrada: QC técnico seleccionado — 01/11/2026

QC integrado mediante PR #33. Replay seleccionado de SRR8144908 terminado en 371,380 s≤600 s: 4.292.655 lecturas realineadas de los cinco bloques fijados; fuente completa de 54.292.655 escaneada para ordinales y EOF/CRC. Predicción 13 canónicas/3 crípticas a15 y15/4 a8 reproducida exactamente, cuentas e histogramas concordantes entre texto/CIGAR y PySAM/HTSlib. Informe: `reports/stmn2-control2-target-qc-20261101/REPORT.md`.

Las cuatro observaciones crípticas a8 tienen MAPQ60, NM0, AS0 y softclip0; las tres a15 están contenidas en ellas. La adicional tiene ancla derecha13. Atributos técnicos, no moléculas independientes, efecto de TDP-43 o validación funcional. No se estiman tasas sobre la selección post hoc. El resultado del control completo sigue111/3 y154/4, SHA original cb266041… intacto; denominador114≥20 no se reevalúa sobre la selección enriquecida. No nueva biblioteca ni cohorte.

392 tests locales (378 previos+14 nuevos), compileall correcto y preflight real PySAM0.23.3/HTSlib1.21 concordante. Exportadores repetidos idénticos por bytes y seis controles de artefactos alterados rechazados. Nueve módulos de ejecución cotejados con Git blobs remotos antes del replay. FASTQ/índice restaurados por hashes idénticos; una descarga de rango truncada se recuperó por el reintento de transporte preexistente, recibo completo98rangos yMD5/SHA verificados. Cero reintentos de replay, errores de watchdog o ampliaciones de recursos. CI final se verifica por cabeza del PR; la CI previa920414d pasó392tests en3.11/3.12.

Fase técnica cerrada e integrada; la coordinación con la PR #30 es la siguiente puerta. No repetir estos bloques ni ampliar bibliotecas para resolver soporte bajo sin un plan nuevo. La inferencia permanece bloqueada por el mapa de unidades/lotes/pareamiento; conservar la declaración publicada3/3, sin negarla por falta de mapa. No merge/cierre automático, clínica personal, gastos, contactos, publicación externa o laboratorio. PR #30 separado e intacto053ef70c.

## Alcance

Esta entrega reconcilia los contenidos de PR #28 y #29. El PR #28 fue incorporado a main mediante fc9aa3835373146988fee5e2274160596457a92f; la reconciliación de #29 se registra en el acta de integración y su estado final se verifica en GitHub por SHA y CI. La versión conjunta contiene ambas líneas de trabajo, sin añadir por ello evidencia científica independiente.

Hay auditorías técnicas, reproducción numérica, descriptivos y propuestas. No hay una nueva diana validada, experimento propio o beneficio clínico demostrado. Las series o tablas reutilizadas no se cuentan como cohortes nuevas.

## Completado

| Línea | Resultado | Informe |
|---|---|---|
| #1/#2/#17/#19 | Inventario técnico y mapeo por ENSG; fallo de cero objetivos corregido | reports/geo-audit, isoforms, mapping-positive-controls |
| #20 | Parser histórico corregido; 1910 uniones agrupadas y 1901 con soporte asignado positivo | reports/junction-filter-reconciliation |
| Catálogos y geometría | 545 anotadas v47, 353 solo autores, 182 pendientes, 821 sin coincidencia en recursos limitados; no novedad inferida | reports/global-junction-geometry y auditorías de autores |
| Originalidad | Auditoría dirigida, límites documentales e inventario funcional; propuesta v0.4 conceptual | reports/originality-audit, functional-data-inventory |
| #14: expresión/uniones | 45 campos de expresión, 18 de extracción DEXSeq y 24 de índices concordantes; duplicados/fórmulas auditados | reports/issue14-reproduction, fratta-junction-audit |
| #14: DEXSeq | Diseño por dos lotes, 7030428 cuentas concordantes; sensibilidad de magnitud/denominadores y regiones CE comprobadas | reports/gse121569-design, dexseq-qc, dexseq-magnitude, dexseq-coverage, ce-bin-coordinate-audit |
| SH-SY5Y | Seis enlaces exactos a ENA; S6 y convenciones inspeccionadas; búsqueda histórica acotada concluida | reports/shsy5y-junction-map, junction-definition-search |
| GSE122069 control completo | 37.518.164lecturas,38bins/dosparsers; STMN2canónica72/críptica0 a15; criterio técnico20superado, no contraste biológico | reports/gse122069-full-control-20261031 |

Los informes preservan los hashes, parámetros, errores y resultados negativos de cada ejecución. Sus antiguos apartados «siguiente tarea» son históricos; no reemplazan este estado.

## Bloqueos científicos, no tareas activas

- Refit GSE121569: pozo/reactivo/fórmula y estructura de dependencia incompletos. No promover bibliotecas a diferenciaciones.
- Siete uniones SH-SY5Y: cuatro alias UNC13A y dos conflictos de hebra STMN2 pendientes. El fichero de definición referenciado por el pipeline no se recuperó en la revisión acotada. No reabrir sin fuente nueva.
- Contraste funcional posdéficit: seis fichas no permiten reconstruirlo con los materiales inspeccionados. No ausencia universal, ni ensayo ejecutado.
- 821 claves sin coincidencia: referencia/cobertura/asignación/soporte de lecturas incompletos. No priorizar como descubrimientos.
- Paridad de uniqueCounts y soporte por lecturas crudas siguen sin explicación completa. No dividir cuentas por dos ni llamarlas moléculas.

## Fases y resultados anteriores (no sustituyen la próxima decisión vigente)

QC del control completo SRR8144907 TERMINADO en reports/gse122069-full-control-20261031:37.518.164lecturas exactas,EOF/CRC válido,38bins concordantes en dosparsers,47.124.040registrosSAM,96,21%alineamiento. STMN2canónica72/críptica0 a15;110/0 a8. Exon1:169solapamientos únicos; exon2:1308. Regla técnica canónica+críptica≥20 superada paraestecontrol. El primer1M conserva exactamente sus cuentas previas, pero su0no calificaba toda la biblioteca. No sumar piloto/bins como réplicas ni inferir ausencia deCE, efecto,PSI o función.

Ejecución1373,82s<30min,2CPU,caps virtuales5,75GiB,sinSAM/BAMcompleto.335tests locales/compileallOK. Fuente/binario recompilado/índice yFASTQ verificados porhash; fallo previo de restauración por disco guardado,48rangos reusados trasSHA y35faltantes recuperados. Descargar/restaurar no crea nuevasmuestras. Checkpoints parciales en historia dePR33 quedan superados por resultado completo; no declararlos pasadas adicionales. Ninguno de los otros cinco runs procesado.

Auditoría acotada de diseño GSE122069 CERRADA con mapa biológico pendiente en reports/gse122069-design-20261031. Seis experimentos+seis muestras públicas válidos, enlaces técnicos GSM/SRX/SRS/SAMN coherentes; fuente nueva Reporting Summary SHA256ea09e2569478fecd927fb1340424e1fbbbe32e46d3815beb7c1b433296b7b772, inspección visual/técnica de3páginas. No recupera asignación biblioteca→unidad de cultivo/lote/pareamiento; no contradice la declaración previa de3réplicas biológicas por condición. Lote de suero531342 no es lote experimental. Diferencia de medio F12+MEM en suplemento frenteDMEM/F12 enGEO, sin resolver automáticamente.

Fallo del parser de identidad SRS/SAMN conservado ycorregido medianteSECONDARY_ID explícito;6respuestas corregidas idénticas porSHA a las originalmente rechazadas, sin relajar grupo/cultivo.349tests locales ycompileallOK; replayJSON/TSVidéntico porbytes. Auditoría documental técnica, sinFASTQ/alineamientos nuevos, inferencia,PSI o función. Consulta cerrada: solo reabrir mapa con fuente nueva concreta, no repetir las mismas búsquedas. Manifiestos históricos se cotejan con sucommit: control completo fijado a167d370, no aSTATE posteriores.

Parametrización por accession TERMINADA en reports/gse122069-parameterization-20261031. Manifiesto de seis cultivos fijado por SHA; recibos run/GSM/bytes/MD5/SHA ligados a selección antes de abrirFASTQ. Runner yresumen genéricos, sin reutilizar piloto deotrocontrol; salida deejecución yrecibo previos protegidos. Argv históricos1M/completo iguales yresumen histórico igual encada campo sobreJSON archivados. Extractores base/runner1M sin modificar. Modosplan/plan-only ejecutados sin datos/red de descarga.

374tests locales/compileallOK (349+25nuevos), preflight texto/HTSlib concordante en28consultas sintéticas únicas reutilizadas para2contextos, dosproyecciones estables idénticas porbytes. NoHISAT2, FASTQreal o biblioteca nueva ejecutados. Cinco negativos deidentidad/configuración rechazados. Límite global de descarga30min ahora supervisado a nivel proceso; timeout de proceso sintético20ms produjo recibo no verificado. Noampliación/reinicio automático; errores dechild/recibo no habilitan procesamiento. Datos/publicaciones/modelos biológicos previos intactos, mapa deunidades/lotes/pares siguependiente.

Segundo control SRR8144908 COMPLETADO Y VERIFICADO antes de perderse el entorno:54.292.655lecturas,55bins concordantes,EOF/CRC válido,salida0,1919,35s<2700s. Canónica111/críptica3 a15;154/4 a8;211solapamientos únicos exon1. Denominador114≥20. Sin otros4runs o repetición delprimercontrol. No efecto,PSI,moléculas independientes o función; soporte críptico bajo encontrol necesitaQC específico.

CIERRE DE RECUPERACIÓN —01/11/2026: el entorno volvió a responder; se encontraron los artefactos originales completos. JSONcompleto SHA256cb26604160e43cdc04d2eab0a2525fc02f296059d70f5e0d9d731a32d9f6b4a7 idéntico al registrado antes de caída. Arrays de ambos extractores,55filasTSV,QC,logs,comandos ylauncher recuperados. Conteos porbin/global/primarios/exones concordantes, prefijo30M remoto idéntico. Resumen yFASTQQC conservan susSHA originales. No quedan artefactos finales pequeños pendientes; elSAM/BAMcompleto no se retuvo por diseño. Historia de pérdida/recuperación parcial preservada, sin fabricar filas.

378tests locales/compileallOK; dos pruebas nuevas compruebanSHA completo yconsistencia de los55bins. Reexportación sobreJSON idéntica porbytes; ceroFASTQ/alineamientos/replay seleccionados nuevos. Informe yacta en reports/gse122069-next-control-20261031; manifiestos históricos porcommit. Bloqueo operativo cerrado; entrega delsegundo control terminada ypersistida mediantePR33revisable.

Próxima tarea científica propuesta, NOiniciada en este cierre: QC delsoporte críptico bajo según research/plans/2026-10-31-stmn2-low-count-control-qc.md. Tresobservaciones primarias no son moléculas independientes/efecto/función; mapa biológico/lotes/pares siguependiente, sin inferencia. Sinotros4runs, merge/cierre automático, contactos/gastos/laboratorio/publicación externa. PR30intacto053ef70c.

Mapeabilidad del primer exón completada en reports/stmn2-exon1-mappability-20261031: las 194 lecturas perfectas de 50/51 nt del exón1 se recuperan íntegras en su origen con NH1/MAPQ>=20. Incluye las 54 contenidas en el tramo compartido de63 nt de dos transcritos anotados. También pasan680 controles exónicos posteriores,8 positivos de unión y1 negativo. 883 consultas sintéticas, no réplicas biológicas. Dos ejecuciones producenSAM/resultados/tabla idénticos por bytes. No nuevosFASTQreales.

La proyección GENCODEv47 es coherente con exon1 de98nt (ENST00000220876.12) y63nt (ENST00000518111.5), ambos con el mismo donante. No se observa imposibilidad general de mapear estas secuencias perfectas con esta configuración. No se demuestra sensibilidad equivalente con errores/variantes ni se determina qué isoforma se expresa. El cero del piloto real sigue siendo falta de cobertura aceptada, no ausencia molecular.

El piloto previo de1M continúa sin soporte de ambas uniones15/8, pese a628solapamientos del locus,31exon2 y48uniones posteriores. Sus cuentas no se recalcularon ni se modificaron aquí. No descartar/aceptar la biblioteca completa según el subconjunto: la propuesta completa es una sola fase prefijada que podrá confirmar cobertura o rechazar aptitud para este contraste, sin inferencia biológica.

Registro histórico anterior al merge: en la cabeza 76ddc67f236e2f60f099897a116a229c76f25d7a, la rama estaba sin fusionar y la CI de la nueva cabeza pendiente. Después, la PR #33 se revisó y fusionó según el encabezado vigente. Los 226 archivos cotejados, los hashes y los resultados de esa fase permanecen en el informe correspondiente; no se reejecutaron los alineamientos.


## Verificación y operación

Base de la integración de PR #28/#29: 244 tests locales correctos en Python 3.12.14 (166 + 183 − 105 compartidos), compileall correcto. La posterior PR #33 se integró con 399 tests locales y CI Python 3.11/3.12. No se reejecutaron todos los pipelines de datos reales durante la integración; los tests no son experimentos.

Las diez issues históricas no se cierran automáticamente. Las ya ejecutadas se actualizan con evidencia y pendientes precisos. No contactos, publicación externa, clínica personal, gastos o laboratorio sin autorización. La integración autorizada en este turno no concede autorización general de merges futuros.

Historial anterior de ambos estados: reports/integration-20261030/history. El resumen semanal de 30/10 se conserva sin duplicarlo.

## Auditoría de fuentes en esta propuesta de PR

253 tests locales correctos (244 base + 9 nuevos), compileall correcto. Python 3.12.14; QC real del Parquet con PyArrow 21.0.0 en la ejecución previa de este ciclo, repetición idéntica por bytes y hashes comprobados al retomar. E-MTAB-15653: 2.598.287 registros, 22 bibliotecas; SDRF 44 filas FASTQ, 21 nombres de archivo derivados distintos. Hay un conflicto citosol/núcleo en NMD, sin reparación automática; no afecta el enlace único de las seis bibliotecas citosólicas basales. La independencia biológica sigue sin certificar. No se calcula PSI, inferencia ni función. La integración de esta entrega se verifica por el estado de PR31 y su SHA/CI; no añade replicación biológica.

## Actualización: unidades de E-MTAB-15653

Auditoría acotada completada en reports/fractionation-units-20261030: XML primario y suplemento PDF nuevo verificados por hash. El PDF no aporta un mapa de cultivos independientes; seis enlaces técnicos basales correctos no certifican seis unidades biológicas. La vía inferencial sigue bloqueada y esta búsqueda se cierra sin repetirla. Siguiente trabajo seguro propuesto: redactar plan de recursos y controles de los seis runs GSE122069 ya identificados, sin descargar/alinear ni abrir un cuarto candidato. No efectos, PSI o inferencia en este ciclo. Mismo PR31 abierto; PR30 separado. Los próximos pasos anteriores sobre buscar documentación de unidades quedan reemplazados por este resultado.


## Cierre de revisión y plan operativo

Descripción y punto de continuación reconciliados. La integración concreta de #31 está autorizada por Luis; #30 se mantiene abierto y su rama intacta. Plan GSE122069 en reports/gse122069-resource-plan: RAM disponible 8 GiB, piloto condicionado a índice compatible y medición de recursos; ninguna descarga/alineamiento iniciada. La CI offline no reproduce FASTQ ni certifica viabilidad del piloto.

## Contrato STMN2 — 31/10/2026

Pregunta/falsador fijados antes de ejecutar: research/plans/2026-10-31-stmn2-junction-contract.md. Candidato canónico único en la proyección y coherente con exones de ENST00000220876.12/ENST00000518111.5; no son réplicas biológicas. Conversiones intrónicas/BED y extracción SAM SE sintética comprobadas. 275 tests locales correctos (253 previos +22 nuevos), compileall correcto; Python 3.12.14. Contrato idéntico por bytes en dos ejecuciones, entradas por SHA256 y ficheros heredados cotejados con Git blobs. La CI de este PR se verifica por su nueva cabeza; no se presupone correcta ni reproduce FASTQ.

No efectos, PSI, significación ni función. Razón propuesta críptica/(críptica+canónica) sería condicional a esas dos ramas; otras ramas del donante no medidas. Prototipo requiere XS y NH=1, MAPQ>=20 (excluye255), anclas contiguas>=8; retiene flags de duplicación y rechaza PE. Pendiente comparar con herramienta independiente y semántica del alineador. No producción/crudos desde esta entrega.

Ensembl agotó timeout y no aportó referencia. 8 GiB RAM, ~62,79 GB libres observados, sin HISAT2/STAR/samtools. Esto no es benchmark ni autoriza más recursos que el plan previo. Git clone sin credenciales; acceso al código por conector comprobado. Se registran fallos de materialización local, corregidos por blobs exactos antes de la suite final. Ningún cambio en main o rama30, merge/cierre, gastos, contactos o publicación externa. Las menciones a PR31 abierto y 253 pruebas corresponden a ciclos anteriores. Esta nota también es histórica; la próxima decisión vigente figura en la cabecera de estado.

## Puerta de referencia — 31/10/2026, posterior a #32

reports/stmn2-reference-gate-20261031 conserva seis respuestas mínimas públicas de secuencia con URL/hashes, metadatos de ensamblaje, candidato de índice fijado y revisión de manual HISAT2v2.2.3, commit0d244324. Código ejecutado conPython3.12.14, dos replays idénticos por bytes,284pruebas locales (275+9) y compileall correctos; CI de nueva cabeza por verificar. Un primer timeout de Ensembl críptico se resolvió con un reintento; el error se conserva. La herramienta web falló con los parámetros UCSC; las recuperaciones reales fueron solicitudes Python satisfactorias.

Solo48bases de referencia en tres ventanas, cotejadas entre dos proveedores del mismo ensamblaje; no réplica externa biológica ni soporte de lectura. Sin descarga de índice/FASTQ, instalación de alineador, alineamientos o efectos. Próximo gate de software: ejecutar versión fijada y comprobar NH/XS/MAPQ contra controles; NH informa alineamientos reportados, no unicidad exhaustiva. No -k1 ni strandness asumida. Los ejemplos del manual incluyenMAPQ255; el prototipo actual los rechaza: comprobar comportamiento de versión real sin cambiar filtros tras ver efectos. Los apartados previos de secuencia/motivos pendientes son históricos y quedan sustituidos por este resultado acotado.

## Inspección real de índice — actualización posterior en PR33

Plan previo research/plans/2026-10-31-hisat2-index-inspection.md; fuente de HISAT2 fijada acommit0d244324, SHA256 del paquete y del binarioInspector, g++13.3.0, comandos/recursos/hashes por fichero registrados. Python3.12.14;295pruebas locales correctas (284+11) ycompileall; no tests como experimentos. No inferencia, efectos, validación funcional ni clínicos personales. Un intento de medir compilación con/usr/bin/time falló antes de compilar porque no está disponible; reintento Pythonresource/monotonic compiló correctamente. Sin coste/contactos/laboratorio. CI de nueva cabeza por comprobar.

## Gate sintético del alineador — actualización en PR33

Plan previo research/plans/2026-10-31-hisat2-synthetic-gate.md. Solo referencia pública y lecturas artificiales explícitas; no datos clínicos, gastos/contactos/laboratorio. Alineamiento humano sintético~11,49s, máximo hijo observado4.633.708KiB (~4,42GiB); no extrapolar a un millón de lecturas. PySAMvenv de tarea, wheel0.23.3 SHA cotejado contraPyPI; APIHTSlib independiente de parsing, filtros conceptuales iguales. Los resultados descriptivos son de software, no prevalencia/eficacia. Asimetría a8bases queda como resultado negativo explícito, no solucionada por declarar8en el extractor. La nueva política15/8 solo se aplicará prospectivamente al piloto técnico, sin razones biológicas en esta fase.

## Piloto real y diagnóstico — actualización en PR33

Los apartados anteriores que dicen ningúnFASTQreal procesado o piloto pendiente son históricos. Ahora hay un piloto técnico de un solo control y un diagnóstico del mismo subconjunto, ambosconcordantes; ninguna inferencia porcondición. No ampliarlo para conseguir cobertura. La siguiente prueba es mapeabilidad/definición del primerexón con datos sintéticos, antes de decidir una fase completa de tamaño fijado. Protocolo públicoTruSeq verificado por fuenteprimaria; hipótesis3prime-only noacreditada. No tratamientos, clínica personal, gastos, contactos o laboratorio.

## Mapeabilidad exon1 — actualización31/10/2026

Plan previo research/plans/2026-10-31-stmn2-exon1-mappability.md; solo referencia/lecturas sintéticas. 98/98 consultas de50nt y96/96de51nt del primerexón pasan criterio de origen completo. No se trataron solapamientos de ventanas, orientaciones o transcritos como unidades biológicas. El siguiente paso fijado es QC del control completo, no nuevos controles sintéticos equivalentes ni procesamiento de seisbibliotecas. No gastos, contactos, publicación externa, clínica personal, laboratorio o indicaciones terapéuticas.
