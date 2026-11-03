# Control local completado y auditoría exploratoria de UNC13A

## Evidencia

Luis aporta el sello del control y los extractos de QC, resumen HISAT2 y recibo del supervisor, transcritos en `operator-control-evidence.json`. No se ha accedido remotamente a su sistema. Se validaron 12.709.444 pares; el prefijo fijo fue de 1.000.000. HISAT2: 851.945 pares concordantes únicos, 69.461 múltiples y 78.594 sin concordancia (92,14 % global). En la ruta de sensibilidad aportada se aceptaron 850.834 pares y se excluyeron 1.111 por hebra del evento. No se recibió en el chat el JSON completo de las otras rutas; la nueva auditoría comprobará sus recibos locales.

El sello reporta un grupo canónico y ninguno de los dos eventos crípticos; unión de soporte 1 frente al mínimo prospectivo de 20, sin cambio al anclaje de 8 bases. Supervisor: salida 0, sin violaciones ni miembros vivos; 713,146 s y pico RSS muestreado de 4.882.288.640 bytes. Cargo constante de 7.322.807.977 bytes; cero nuevos bytes de descarga. La reserva de navegador previa no se suma de nuevo.

## Interpretación y límites

La ejecución técnica terminó. El prefijo no superó la puerta de cobertura. Esto no demuestra ausencia de eventos crípticos ni valida una comparación biológica. Los ceros tampoco prueban que los objetivos sean incorrectos. La referencia cacheada ya distingue las coordenadas exónicas candidatas de los intervalos intrónicos con inicio incluido y final excluido: (17641556,17642844), (17641556,17642413), (17642541,17642844). Los motivos y la anotación cacheados apoyan esta geometría, pero proceden de un único proveedor UCSC.

## Próxima prueba definida antes de ejecutarla

Pregunta: ¿la escasez se limita a los objetivos exactos o afecta al soporte de uniones de toda la región? Auditoría exploratoria del mismo prefijo ordinal 1–1.000.000, en chr19:[17600000,17690000), que abarca los transcritos UNC13A cacheados con margen. No es una anotación exhaustiva del gen ni una estimación de expresión. Se incluyen ambos signos de hebra y sólo eventos cuyo intrón solapa la ventana. Se cuentan grupos con alineamientos primarios que comienzan en la ventana y grupos con uniones solapantes antes de filtros; no son cobertura base a base ni moléculas únicas.

Se conserva exactamente el alineador, índice, argumentos, filtros y objetivos. Se inventarían todas las uniones regionales aceptadas a 15 y 8 bases, con contadores de descarte de grupos regionales y offsets de hasta dos bases respecto de los objetivos originales. La reducción por (RG,QNAME) evita contar dos veces una unión apoyada por ambos mates. Los dos decodificadores deben concordar. Tope de 4096 uniones por ruta y límite de tamaño del resultado; si se excede, falla sin truncar. El programa exige reproducir todos los conteos y QC originales, así como el número de registros, antes de sellar.

Predicción discriminante: soporte abundante en otras uniones y escaso en los objetivos dirige la revisión a la unión/isoforma seleccionada; escasez regional general apunta a representación limitada de la región en el prefijo. Descartes regionales concentrados permiten investigar filtros. Ningún resultado por sí solo prueba expresión, ausencia, PSI o causalidad. El inventario exploratorio no promueve la puerta de cobertura ni habilita TDP. Una discrepancia de replay obliga a detenerse y examinarla.

## Ejecución y recursos

Nuevos scripts `unc13a_locus_audit.py` y `unc13a_locus_pipeline.py`; el segundo deriva del motor compacto sin cambiar el histórico. Se verifican los cinco hashes del control aportados por Luis, la cadena de recibos, las identidades y los dos prefijos ya certificados. No se vuelven a copiar los FASTQ completos. El trabajador verifica hashes de prefijos/índice, descomprime los prefijos y vuelve a alinear sólo esos pares; no conserva SAM.

Nueva ventana máxima de 2100 s (35 minutos): verificar 300, preparar texto plano 300, productor 900, reducción 300, finalizar 180 y margen 120. CLOCK_BOOTTIME y arranque actual en trabajador/padre. Dos CPU; RSS de grupo muestreada de 6 GiB y espacio virtual por proceso de 8 GiB. Se cuentan trece árboles: once históricos, control sellado y auditoría. Disco acumulado 27 GiB, reserva 8 GiB; históricos hasta 18 GiB, texto plano hasta 2 GiB, compactos hasta 6 GiB y recibos hasta 0,25 GiB. La preparación sigue requiriendo 35 GiB libres y la memoria disponible previa; no aumenta recursos automáticamente.

Preparación deshabilitada, SHA exacto y aceptación de ventana; raíz nueva, sin reintentos automáticos. El hook de Python bloquea conexiones; no es aislamiento de red de procesos nativos. El código nativo fijado se ejecuta sin URL. No HTTP ni TDP; presupuesto histórico constante. Mantener originales. La autorización de Luis corresponde a preparar esta auditoría y entregar el bloque local; no consta aún su ejecución.

El sello conserva el inventario completo de las cuatro rutas. La consola muestra sólo las rutas de texto a 15 y 8 bases, sus 20 uniones con mayor soporte y todas las vecinas de los objetivos; se etiqueta como resumen y comunica la ruta del inventario completo. No se trunca el archivo de evidencia.

## Validación

506 pruebas locales correctas sin omisiones (485 previas y 21 nuevas). Pruebas y versiones en `validation.json` y `tests.txt`. Miniaturas con SAM reproducido verifican el inventario, ambos anclajes/decodificadores, igualdad con el motor previo, desplazamiento de una base sin retargeting, filtrado regional, límite sin truncar, CRC/hash de prefijos, negativa del productor, plazos y supervisión. Integración del trabajador/sellador usa fuentes de fixture y productor sustituto; no es un nuevo alineamiento humano ni benchmark. La regresión conserva los ejecutores históricos. La CI general puede omitir tests con PySAM ausente; la CI pareada lo instala y los ejecuta en Python 3.11 y 3.12.
