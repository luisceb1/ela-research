# Piloto con índice extraído sellado, sin volver a descargarlo

Evidencia aportada porLuis: sealed_verified_extracted_index,nuevearchivos,
prefix /home/luisceb/ela-piloto-real-01-index-recovery-01-extracted-01/index/files/hg38/genome,
0bytesnuevos,cargo4355802733B/saldo7644197267B; índicearchivado4.355.786.349B
conSHA18487844…; tiempo/RAMdeextracción no aportados,no inventarlos.

Pregunta: ¿puedeelpiloto técnico reutilizaresteíndice conservando cadena/cargos,
y ejecutar ruta ya probada sinotraHTTPdeíndice o ampliaciónadaptativa?
Predicción: preflightrehashea nuevearchivos yencadena sellos; solo4HTTPdeFASTQ,
CTRLprimero;1Mpares,umbral20,paradaantesdeTDPsifalta cobertura. End-to-endhumano
pendiente; controlesunitarios sólofixtures/mocks,no descargas reales aquí.

Cambio acotado: nueva configuracióncached estricta; helpers existentesdeHTTP,
FASTQ/compact/HISAT2/supervisión,sin duplicar algoritmoPE. Guardas anteriores
siguen para modo no-cache. Saldo inicial no0 sino4355802733B; minfuturo6349703881B,
cargofinalmínimo10705506614B,margen1294493386Balcap12GB. Disco25GiBcuenta4árboles,
artefactos16GiBincluyehistoria,8GiBreserva. Capstemporales2+4GiB,2CPU,RSS6/AS8.

Propuesta de NUEVAventana7200sglobal/1800sHTTP,preflight180,2prefix900,
2compute1200(900producer+300reduce),envolvente6180s,margen1020s. Capsnopronóstico.
Relojes/cargos anteriores inalterados; plan deshabilitado y ejecución requiere
aceptarSHAexacto,conscopeexpresodenueva ventana. Rootderivadoúnico,sinreset/retry.
Pruebas: cachemetadata/hash/pins/prefix/origen/caps/cargo,floorcontador,
noadopciónsinsello,noHTTPantesdepreflight,noíndiceHTTPenmanifiesto,
reducciónI/Odeguardadisco sinrelajar watchdog externo. ActualizarSTATE/BACKLOG/PR.
