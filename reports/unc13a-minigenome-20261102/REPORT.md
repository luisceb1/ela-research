# Minigenoma UNC13A: función concordante, recursos sin certificar

Fecha:02/11/2026. Base:10530d1211a4c8fd364b96f740f74bb37c488312. Plan prospectivo:research/plans/2026-11-02-unc13a-unstranded-minigenome.md.

## Resultado funcional ejecutado

Se descargó y compiló HISAT2v2.2.3 desde el commit fijado0d244324f98de541bce04d45c75e83bc3522f7f4, sin modificar código ajeno. Descarga7.061.238bytes; SHAyURLen source.json. make-j1/USE_SRA=0compiló align-sybuild-s. Versiones y SHAdebinarios en versions.json; fuente, binarios e índices no se añaden a Git.

Se construyeron cuatro referencias diminutas: ventana hg38de2.500bases, copia duplicada, canónica con motivos invertidos a hebra positiva y canónica con motivo no válido. fixture_plan.json se escribió antes de alinear y fija nueve casos de la referencia original y tres negativos. Lecturas de secuencia conocida, sin errores, generadas de la referencia; ninguna es una lectura experimental.

**Las12expectativas por fragmento se cumplen.** En referencia original se recuperaron canónica y ambos brazos crípticos con anclas75y15, XS− y soporte de un fragmento aunque ambos mates apoyen la misma unión. Los tres casos de ancla14no pasan el umbral primario15. Las dos rutas de decodificación coinciden en eventos y QCen las cuatro referencias. HISAT2se ejecutó sin --rna-strandness y sin --tmo: la hebra negativa no se indujo mediante RFforzado.

El control multicopia se excluye por calidad/NH. El control con motivos de hebra opuesta da el evento XS+, **no el objetivo XS−**; no se presenta como falta de alineamiento. El control de motivo no válido no aporta un objetivo aceptado. Los detalles, incluidas exclusiones, están en result.json y SAMsintéticos en fixtures/. Las coordenadas locales se proyectan sumando origin0=17641000, fijado antes de alinear.

## Colación comprobada

collate_pe_sam.py añade claves RG/QNAMEy usa GNU sort con LC_ALL=C,ordenlexicográfico estable,buffer1MBy temporales en disco; elimina los ficheros temporales al terminar. No se presupone que el orden de salida del alineador cumpla el contrato PE. Dos tests adicionales comprueban mates intercalados, RGdistintos, ordenq10/q2, conservación de soporte y rechazo de RGduplicado. La colación de cada SAMdel experimento ocurrió antes de ambos parsers. La política de pares/reducción continúa compartida: independencia limitada a decodificación de SAM/CIGAR.

## Limitación material del supervisor

**El gate de recursos no queda certificado y el piloto real sigue bloqueado.** El muestreo de RSSdel grupo de procesos devuelve valores nulos o implausiblemente bajos para varias tareas, incluida compilación. No puede usarse para afirmar un máximo agregado inferior a2GiB. No se atribuye el valor cero a consumo cero; tampoco se infiere que hubiera un exceso.

Además, commands.json conserva11recibos, pero faltan los recibos finales align_wrongmotifycollate_wrongmotif, aunque existen sus logs/SAMy la validación de resultados. Se preserva esa discrepancia; no se fabrican recibos de ejecución a partir del argv previsto. La trazabilidad de las órdenes y el monitoreo deben repararse antes de datos reales. No se reintentó el experimento ni se ampliaron límites para ocultar estos problemas.

El estado observado al cierre era≈252segundos desde iniciar descarga,≈62,7MBde archivos del experimento y7,1MBtransferidos, por debajo de sus límites de tiempo/disco/transporte. Son medidas de este experimento pequeño, no una proyección del genoma humano. La afinidad propuesta se restringió a dos CPU; los huecos de muestreo impiden certificar íntegramente el control de recursos. No afirmar que todos los requisitos del plan estén superados.

## Límites científicos

Estos resultados acreditan el flujo funcional sobre entradas conocidas, no sensibilidad, especificidad o mapeabilidad del genoma completo, orientación real de las bibliotecas, soporte de UNC13Aen las personas/cultivos estudiados, independencia biológica o rescate neuronal. No se descargó el índice humano ni FASTQbiológico. La referencia mínima tampoco representa el conjunto de isoformas y paralogías reales. No PSI, p-valores, efecto de KD, comunicación externa, costes o merge.

## Reproducción y siguiente tarea

Scripts nuevos:mini_limits.py,prepare_unc13a_mini.py,run_unc13a_mini.py,collate_pe_sam.py. Source.jsonyfixture_plan.jsonfijan fuente, límite temporal y expectativas de la ejecución original; no volver a ejecutar sobre el deadline vencido ni sobrescribirla como una repetición histórica. Preparar otra carpeta/plan para una ejecución futura. Compileall y dos tests de colación pasan. La CI verificará controles offline sobre la nueva cabeza, no repetirá compilación/alineamientos.

**Única siguiente tarea:** reparar/verificar el supervisor y la persistencia atómica de recibos en procesos sintéticos de consumo conocido (árbol de procesos, proceso breve, timeout y terminación de descendientes), con plan nuevo y sin índice humano/lecturas reales. Solo después decidir un nuevo gate de recursos. No repetir las alineaciones exitosas como evidencia biológica ni iniciar los6,35GBmientras raw_pilot_ready=false.
