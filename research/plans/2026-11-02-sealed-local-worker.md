# B1 local: ejecutor fijo y resultado sellado — 02/11/2026

Base PR36:eab691f3c7e0bbf308d3c67c16390bad07d715da.
Pregunta: ¿se puede encadenar transporte→archivo/prefijos→productor→conteo y
aceptar resultados solo después de terminar correctamente la supervisión externa?

Antes de ensayo: HTTP127.0.0.1, tar con ocho miembros índice explícitamente
simulados, gzip de los FASTQ sintéticos existentes y replay del SAMwild ya alineado.
El replay no es un alineador ni demuestra uso biológico de índice/prefijos.
Comprobar identidades/nombres y hashes; ninguna alineación nueva o genoma humano.

Un descriptor exclusivo fija modo sintético, orígenes exactos, pasos permitidos,
política, productor/script/interprete, decoder y procedencia de prefijos/archivo.
Solo worker fijo bajo supervisor puede ejecutar pasos; no comandos libres.
Padre solo lee metadatos acotados, worker realiza rehash/validación voluminosos.
Productor y consumidor en el mismo grupo; stdout en pipe, sin SAM nuevo en disco.

Datos/recibos internos son provisionales hasta que el padre coteje exit0, ausencia
de violación/error y grupo vacío. Sello fija SHA de descriptor/ledger/resultado
interno/recibo externo. Ledger con modo sellado no se puede reabrir sin ese sello.
Revalidación posterior bajo otro supervisor, sin tráfico o cambios de presupuestos.
No sobrescribir jobs ni reconciliar fases incompletas automáticamente.

Controles: recorrido positivo y cobertura insuficiente; origen/URL/redirect y modo
externo rechazados; productor no-cero/bloqueado; hash/identidad prefijo/archivo/
fixture alterados; falta o manipulación de sello/recibo/ledger; fallo de supervisor
posterior a resultados internos; reenviar descriptor existente rechazado. Unir
resultados con argv HISAT2 de diseño fijado, sin ejecutarlo. Caps de clocks/disco/
RSS-AS heredados; límites por fase se vigilan también desde padre.

Predicción refutable: solo recorrido supervisado completo produce sello aceptable;
un resultado interno verified no sobrevive como certificado a un fallo externo.
Fracaso: aceptar negativo, copiar SAM completo, ejecutar comando libre o perder
deadline/consumo al verificar. Cerrar B1solo integración sintética, manteniendo
producción deshabilitada y B5/decisión de ejecución pendientes.
