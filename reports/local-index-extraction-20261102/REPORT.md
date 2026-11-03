# Recuperación comprobada y siguiente fase local — 02/11/2026

Base8cd1df988c6329c3694269c2a2cde395c60f779e. Planprevio:
research/plans/2026-11-02-local-index-extraction.md.

## Evidencia nueva aportada

Texto pegado(2).txt, adjunto delusuario. Seextraen2recibosJSONysello sinmodificar
eladjunto. TrasnormalizarCRLF→LF, SHA256de recovery-result.json ysupervision/run.json
coincidenexactamenteconelsello queaporta Luis. Seconservan esosbytesnormalizados
como user-reported.json yprocedencia/SHAadjunto enrecovery-review.json. No es
acceso remotodelagente a su máquina ni hashindependientedelarchivo4,36GB aquí.

ArchiveSHA1848784403a0fb3ee7735b2f891d8be96fd2782e08aed3d8212d922666f077a5,
4.355.786.349B. Tramo2.723.339.065B/148,514528751s≈18,337MB/sdecimal;
externo167,457363098s, RSS28.110.848B≈26,81MiB,exit0,sinviolación,sinvivos.
Cargoacumulado4.355.802.733B, saldo7.644.197.267B, conserva16KiBsinarchivo.
Memoriadeldescargador, no coste medido delalineador; no atribucióncausaldeaceleración.

Internopending_outer_seal es snapshotanterior aaceptación; elselloexternoposterior
sealed_verified_index_archive confirma cierre. No es unfallo o motivo pararepetir.
Índiceaúnnoextraído, sinFASTQ/alineamiento/PSI/nuevaevidenciabiológica.

## Cambio preparado

prepare_verified_index.py ejecuta unpasosolo localnuevo: verificametadatossellados,
aceptación/fuente/cargos, binarios/version2.2.3, hashentero delarchivo; extrae con
parseracotadoexistente(tamaños/hashes/inventario/EOFCRC/capstar); rehasharchivoantes
depromover miembros. Inspeccionaíndiceconargvfijo -s y exigechr19/58617616;
rehashsalidasyrecibosantesdefinalizar. No ejecutarecetadelarchivo ni shelllibre.

Padresolometadatos; workerhaceI/Ovoluminoso bajo supervisorLinux/CPU/AS/RSS y
relojglobal/fases. Discochildsecomprueba cada100msparaevitarrecorrerárbolentero
porcada64KiB; padreindependientemuestreaconwatchdogy mantieneclocks/RSS. No cuotas
duras o garantías de tiempo real, como enpasosanteriores.

Nuevo joblocal900s:120preflight/600extract/120inspect+60margen,2CPU,
6GiBRSSglobal/8GiBASporproceso;fases512MiB/1GiB/6GiBRSS y1/2/8GiBAS.
25GiBsumandooriginal+recuperado+nuevo,8GiBreserva.0bytesred,cargoyplazosviejos
inalterados. No nuevaaceptación detransporteporque no haypetición ni nuevo tiempo
de red. Se autoriza mediante elcomandolocal delrunbook, dentro delobjetivodelpiloto.

Rootderivadoexclusivo,no sobrescribe,reabre o adopta fallos. Sello externo solo
trassupervisorfinished/exit0/sinviolación/error/grupovacío, resultadocoherente,
prefixexacto/tamaños yrecibos correctos. verified internono basta paraadopción.
Si falla eldialectodeltar, no relajar elparser ni reiniciar automáticamente.

## Validación y límites

14pruebas nuevas conarchivosminiaturafalsos explícitos; noindexHISAT2real.
Prueban extracción/CRC/tamper/inventario/SHA/nooverwrites, resúmenesconproductor
sustituto, metadatossellados/contabilidad/caps/orígenes ydecisiónexterna.
CLI/workerreal conPythonELFrenombradofalla por versión antesde leerelsparsefile
que sólosimula tamaño:preflightfailed,exit1/grupovacío,sinextracción/transferencias.
No se hasheaoextrae archivoesparcidode4GB enesecontrol.
Fixturederesumen/decisiónlimpia produce sello; exteriorincorrecto no lohace.
273tests seleccionados pasan sin errores/omisiones(259anteriores+14nuevos), compileallcorrecto; validation.json/tests.txt.

Estaspruebas no acreditan aún dialectotar/inspector/consumohumano enelhostdelusuario.
Nuestrohostno descargó/extrae índicehumano, datosbiológicos oalineamientos nuevos.
Loslímitesdelwatchdog y hosthostildeanterioresinformesaplican; no firmacontroldueño.

Siguiente: Luisactualiza y ejecutacomandolocaldocumentado. DespuésdevuelveJSONsello
(oerror), ysepreparaadopcióndelíndiceverificadoparalecturas sinredescargarS3 ni
renovarcargosviejos. No relanzarjoboriginal ni prometerpipelinebiológico yaejecutado.
Sinmerge/contactos/costes/publicaciónclínica. raw_execution_ready=false.
