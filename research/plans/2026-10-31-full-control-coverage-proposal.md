# Propuesta prospectiva: cobertura del control completo GSE122069

Estado: fase siguiente no ejecutada. No cambia ni amplía retrospectivamente el piloto fijo de1M.

Tras recuperar todas las lecturas perfectas50/51nt del primer exón en su origen, la mapeabilidad general del referente no explica por sí sola su falta de cobertura aceptada en el subconjunto real. La siguiente pregunta es si esa limitación persiste en la biblioteca completa SRR8144907 o depende del orden/submuestreo.

Entrada única fijada: todo SRR8144907,37.518.164lecturas según ENA, mismo archivoMD5/SHA256ya verificados; ninguna bibliotecaKD ni los otros cinco runs. Proponer una sola pasada completa con límite de tiempo, sin detenerla al aparecer señal ni ampliar muestras si no aparece. No nueva unidad biológica.

Antes de ejecutar: generalizar el código para un número esperado de registros por parámetro, preservando modo1M para reproducción; controles sintéticos de frontera yparsers. Verificar archivo/índice/binario yrecursos actuales. Usar mismos filtros15/8,coordinates,seed,k5 ysemántica deHISAT2. Bins de orden de lectura fijados a1M (último parcial), con soloQC/cobertura agregados porbin, sin exportar IDs. Las particiones no son réplicas biológicas. SinSAM/BAM completo.

Predicción refutable: o se recupera cobertura de primerexón/donante al usar todos los registros, o persiste su falta. Ambas conclusiones son técnicas sobre un control. Sin efecto, PSI o prueba de ausencia molecular. No sustituir el objetivo por uniones posteriores.

Criterios: confirmar exactamente37.518.164primarios, hashes, concordancia global/target entreextractores yCRC al leer archivo completo. Informar bloque/exon1, unióncanónica/críptica y cobertura mínima20sinfracción. Si la biblioteca completa tampoco aporta cobertura del sitio, rechazar su aptitud para este contraste antes de procesar los otros cinco; no generalizar ausencia biológica. Si sí aporta, revisar viabilidad de una fase de seisbibliotecas con unidades y recursos suficientes, sin inferencia automática.

Recursos propuestos, pendientes de revisión operativa:2CPUs, caps deespacio virtual5GiB+512MiB+256MiB, límite30min de fase, reserva8GiB ypresupuesto de disco previo, sin nuevas descargas. Medir entrada/salida/rendimiento de principio a fin. Si el límite de tiempo resulta insuficiente, guardar estado parcial yno presentarlo como pasada completa; proponer revisión de recursos antes de reintentar. El tiempo del primer1M no garantiza extrapolación lineal ni coste de37,5M.

No iniciar esta fase en la entrega de mapeabilidad. Mantener mismoPR33 revisable sinmerge yPR30intacto.
