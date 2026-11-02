# Extracción local desde archivo recuperado, sin red

Evidencia aportada en Texto pegado(2).txt: recoverysealed,4355786349B/SHA18487844…;
tramo2723339065B/148.5145287513733s, total167.457363098s, RSS28110848B,
externofinished/exit0/sinviolación/grupovacío. Cargoacumulado4355802733B/saldo7644197267B.
No extrapolar memoria deldescargador alalineador. Resultadointernopending_outer_seal
es snapshotprevio; sello externo posterior acredita cierre, no contradicción.

Pregunta: ¿se puede verificar/extractar/inspeccionar el índice restaurado sin nueva
transferencia o adopción de resultadoshuérfanos? Preflightidentidad/sello yversión,
SHAentero; extracción acotada exacta/CRC/nuevearchivos; inspectorchr19/longitud y
rehashsalidas. Predicción: solo se sella trasgrupo limpio e inventariocorrecto.
Controles: metadata/source/hash/versión/members/caps y estadoexterno incorrectos
rechazados; no reemplazo de directorios; pruebaCLInegativa antesde leeríndice.

Scope: ningunaHTTP/FASTQ/alineación. Original+recovery+salidas≤25GiB,reserva8GiB,
2CPU,900sglobales(120preflight+600extract+120inspect+60margen). RSSfase512MiB/1GiB/
6GiB,AS1GiB/2GiB/8GiB; supervisorgrupo. Archivos fuenteoriginalesyrecuperados no
se modifican. Jobnuevolocalfixaidentidades/rutas/límites yrootderivadoexclusivo.
CLIlocalreversible no requiereotraaceptaciónde tiempo detransporte:0bytes nuevos;
elpresupuesto yplazos previos no se renuevan. Padre no rehasheavoluminosos.
No descarcarga/índicehumano ennuestrohost; probar sólofixturespequeñoslocales.
