# Índice interrumpido: evidencia y corrección de I/O — 02/11/2026

Basea3f76b4a97061b81c1b4ca68cef838eaeb8e1ca4. Plan previo:
research/plans/2026-11-02-interrupted-index-transport.md.

## Evidencia del usuario

Preflightverified; solo index_archivestarted,1.632.463.668bytescargados,
3600,0012652873993sacumulados y reserva pendiente0. Padre cortó elgrupo por
Cumulative transfer time cap; logdelworker vacío. Parcial mostrado≈1,6Gsin
tamañoexacto/hash. Aún no índicecompleto/lecturasbiológicas/alineamiento. Registro
user-reported-failure.json: evidencia aportada porLuis, no inspección remota.

Promedio observado delcargo:0,45346MB/sdecimal. Equivale al37,48%del tamañodel
índice en términos de bytescargados; no certifica el contenido persistido. Falta
verificar tamañoexacto/hashes/recibo externo delusuario. Límite de tiempo agotado
no indica un error delalineador ni ausencia de señal biológica.

## Hipótesis y corrección

Legacyreserva,settleyrecibo:3escriturasatómicasporread1, cadauna confsyncarchivo
+directorio. Con lecturasde16KiB,8MiBprovocan512lecturas y3082fsyncen elensayo.
Esto es un coste evitable confirmado; no demuestra que fuese la causa únicade
lavelocidadenWSL o que laredS3fuese rápida.

Nuevo opt-in reservation_block_bytes=4MiB: antesdecualquierlectura de bloque se
carga duraderamente todoelcrédito, selee≤64KiBy seexigen guardas porlectura,
secompletaelbloquey despuésseactualizanmetadatos. Si muere oreadlanzaexcepción,
elbloquecompletocargadoqueda conservadoramenteconsumido, incluso parte noleída.
No reembolso incierto. UnEOFvacío retornadopermite descontarsolo créditono usado
probado; elresultado queda fallido/no promovido. No reanudación de fases.

Modolegacy porlectura sigue siendo default para losusuariosanteriores; su firma
no cambia. Modo porbloques usa firma nueva. La configuración real nueva fija
bloque/lectura/intentos como parte delmanifiesto reconstruido; cualquiercambio
es rechazado. Actualizarsoftware invalida elplananterior para ejecución: no es
una migración/reanudación implícita o un permiso de renovación de presupuesto.

## Mediciones y pruebas

benchmark.json: respuesta simulada enmemoria, lecturas16KiB,8MiBdebody, escrituras
reales en filesystemdelagente. MismoSHAy8.388.608bytesverificados/cargados;
3082→22fsync(140,09vecesmenos);2,5388s→0,1381s. No descargasHTTPreales, benchmark
deWSL, velocidadENAoS3 o garantía de aceleración futura. No extrapolarlos tiempos.

8tests de bloques: crédito duradero antesdelectura, error incierto,EOFconocido,
checksum, reducciónfsync, configuracióninválida y SIGKILLrealtrasunaprimeralectura
sintética. Esteúltimodeja1MiBcargado/statusstarted y bloquea adopción. No es un
alineamiento.6tests del inspector: evidenciainmutable/caps, fingerprint/aceptación,
checksumdepreflight, cargo incierto,symlink/tamañocompleto, supervisor/seal.
La batería integrada pasa236tests sin fallos/errores/omisiones(222anteriores+14nuevos); compileallcorrecto. validation.json/tests.txt.

## Auditoría del parcial antes de recuperación

inspect_interrupted_pilot.py es independiente delworker y sólousa stdlib.
Comprueba archivoaceptado, fingerprint/limits, preflight, descriptoríndicepinado,
reciboexternofallido/congrupo vacío alcleanup, inventariodefases, ausencia de
promoción/sello ySHA/tamañoestable delparcial. Hashesdemetadatosantes/después;
rechaza modificacionesconcurrentes detectadas y no escribe enroot.

SalidaAUDITED_INTERRUPTED_NOT_RESUMABLE,source_verified=false. IdentificarelSHA
delparcialNOpruebaque susbytesseanprefijodelíndicefuente. Loscargosprevios no se
reembolsan. Muestra saldo, mínimo futuro si sevalidaseRange ydeadlineoriginal.
No abreURLs, no Range, no hace descargas, no modifica elplan/ledger o reinicia.

Siguiente: Luis devuelve elJSONdelinspector. Preparar después, si procede, un
procedimientorevisable deRangeHTTP206conContent-Rangeexacto, identidaddelobjeto,
contabilidadsinrefundincierto ySHA256completo antesdepromover. NOimplementadoen
estaentrega. El3600stransporteestáagotado: cualquier continuación necesita una
decisiónexpresayplan de tiempos, no crearcarpetanueva o aumentarcapsautomáticamente.
No borrarparcial, índice o recibos; no repetir descargaentera. NoFASTQ/alineamiento,
merge/contactos/costes. raw_execution_ready=false. Fuente original y negativo
real seconservan. Los límitesmuestreados y amenazasdelhost delprotocoloanterior
siguen aplicándose; elinspector no es verificación contra propietariohostil.
