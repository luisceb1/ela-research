# Segundo control GSE122069: ejecución completa y recuperación parcial de artefactos

31/10/2026. **El análisis terminó y se verificó antes de quedar indisponible el entorno. La persistencia del paquete completo de artefactos quedó incompleta.** Esta distinción no se oculta mediante una nueva ejecución.

## Evidencia ejecutada

SRR8144908 / GSM3454243 / SRX4965535, grupo publicado siControl2, cultivo SH-SY5Y: **54.292.655 lecturas**, EOF/CRC válido, 55bloques concordantes entre texto/CIGAR y PySAM/HTSlib y salida0. Límite prospectivo2700s; tiempo observado1919,35s (31,99min), incluidos15,71s de verificación previa. El resumen fue calculado y validado en el entorno operativo antes de la pérdida y quedó impreso con suSHA en la salida capturada.

| Biblioteca control de la misma fuente | Lecturas completas | Canónica≥15 | Críptica≥15 | Canónica≥8 | Críptica≥8 |
|---|---:|---:|---:|---:|---:|
| SRR8144907, resultado previo | 37.518.164 | 72 | 0 | 110 | 0 |
| SRR8144908, esta fase | 54.292.655 | **111** | **3** | 154 | 4 |

[Resumen final recuperado](summary.json), [tabla de cifras capturadas](recorded-two-control-qc.tsv). Denominador técnico114≥20: criterio de factibilidad superado para este control. No es potencia, efecto ni validación del diseño. No se calculan fracciones, PSI o estadística inferencial. El primer1M está incluido en el primer control y no se suma como otra muestra; ambas bibliotecas pertenecen a GSE122069, no son dos cohortes externas.

TotalSAM67.839.111:54.292.655primarios y13.546.456secundarios,0suplementarios/0QCfail. HISAT2 informó46.250.576lecturas alineadas exactamente una vez,6.595.623multialineadas,1.446.456no alineadas y97,34%alineamiento. Intrones elegibles globales:3.054.343 a15 y4.964.625 a8. Locus:35.135primarios solapantes,35.128únicos/MAPQ≥20,211exon1,1.880exon2,2.802lecturas únicas con splicing. Solapar el locus no acredita por sí solo asignación génica.

FASTQ:2.742.080.165bases,234.093N,longitudes36–51nt,ASCII35–74 ymedia39,3685 siPhred33; histograma exacto en[QC recuperado](execution/fastq_qc.json). Antes de perder el entorno se comprobaron suma de lecturas/bases, primarios yCRC. La comparación con el piloto de otrocontrol quedó deshabilitada (null).

## Método, hashes y recursos

Pregunta, predicción técnica refutable, controles yfracaso fijados en[plan previo](../../research/plans/2026-10-31-gse122069-control2-execution.md) y[protocolo](protocol.json). Una pasada completa fija, no parada por señal. Código/manifiesto verificados porblobs deff69669fd2e5786d36a2b7126467347e6d752eaa antes deejecutar.

Misma geometría GRCh38 chr8:+, límites exónicos1-based: canónica79611214→79636802, críptica79611214→79616822. Primarios,no unmapped/QCfail/secundarios/suplementarios,MAPQ20–254,NH1,XS,anclas15primaria/8sensibilidad; duplicados retenidos. NH1 es unicidad reportada conk5, no una certificación exhaustiva.

HISAT2 v2.2.3, mismo binario SHA256736b75476c6b0b041d7520821e16435c7e9afcdde5fe7863d20992e3fb044ee2; PySAM0.23.3/HTSlib1.21; Python3.12.14 ejecutado. Seed0,k5,2hilos,no-temp-splicesite,reorder; sinGTF/sitios inyectados/strandness impuesta/deduplicación. CPUafín0/1; capsvirtuales5GiB+512MiB+256MiB, total5,75GiB. MaxRSShijo4.647.336KiB,padre31.668KiB,worker31.668KiB; noRSScombinado medido. Watchdog sin errores. Guard de disco15GiBdesde baseline63.427.059.712bytes,reserva8GiB.

Archivo1.640.602.052bytes; MD5ENA0cd29fe9f8bdf1a6f3596891b783990d ySHA256propioed2f2f4a30b7f448c246029b0407e20e142493b2d74345e674c4e7b3c3e5527f, revalidados por elrunner. HEAD200/tamaño/ETag fuerte propios; no se asumeMD5=ETag. Transporte supervisado1069,92s<1800s,98rangos,0errores por rango,salida0. [Recibo](download.json),[comandos](alignment-command.json),[código verificado](executed-code-provenance.json).

La primera comprobación detectó ausente el destino temporal del enlace deíndice. [Incidente](initial-resource-check.json). Se restauró el mismo archivo fijado porversionId/SHA2561848784403a0fb3ee7735b2f891d8be96fd2782e08aed3d8212d922666f077a5, nueve miembros yCRC idénticos; comprimido duplicado retirado. Restauración operativa, no nuevo referente/estudio, separada de los relojes30/45min. [Verificación](index-restore-verification.json).

## Integridad de la recuperación y bloqueo real

Después de completar el análisis, el entorno pasó a unavailable y una llamada posterior no devolvió resultado. La prueba de recuperación local respondió explícitamente “No usable execution environment is available”. No se afirma que el informe/replay de esa llamada terminara. No se ha repetido el alineamiento ni abierto nuevas lecturas para reconstruirlo.

Dos documentos se recuperaron desde su salida completa capturada:
- summary.json: SHA256 **71eeabbc01277786fd7a849958c4fdc2eadb127ed6e7bba7d984b7c46052cf87**.
- execution/fastq_qc.json: SHA256 **8b4c0704ab24ac103b7abea19cd79b761c49ef9931b042bf963af0504e6a7641**.

Esos hashes habían sido registrados por el exportador antes de la caída. Dos pruebas nuevas en[CI de recuperación](https://github.com/luisceb1/ela-research/actions/runs/41240518570),Python3.11/3.12, prueban igualdad exacta debytes con los hashes originales. **376tests pasan en cada job**,374previos+2deintegridad, no376experimentos. Las374pruebas locales también habían pasado antes de la pérdida. No son una nueva ejecución del pipeline de54M.

No recuperados:JSONcompleto original con todos losbins, arrays completos de ambosparsers, TSVcompleto55bins ylogs originales de disco. Su inspección/cuentas globales sí quedaron capturadas; no se fabrican las filas no impresas ni se reemplazan por simulación. ElSHA delresultado originalcb26604160e43cdc04d2eab0a2525fc02f296059d70f5e0d9d731a32d9f6b4a7 se conserva como referencia, **sin afirmar que ese archivo se recuperó**. El checkpoint30M está íntegro enGitHub,superado como resultado parcial por el resumen completo, no como otra pasada. [Proveniencia y lista de faltantes](artifact-recovery-provenance.json).

## Interpretación y siguiente prueba discriminante

Las tres observaciones primarias corresponden a la misma unión críptica enbins18,43,55; la sensibilidad añadeuna en38. [Cifras capturadas porbin positivo](recorded-cryptic-positive-bins.tsv). Bins yobservaciones no son réplicas o moléculas independientes. Un control no debe imputarse a cero por definición. No se atribuye este soporte bajo a patología,TDP-43,función o rescate.

La concordancia de extractores prueba conteo a partir delmismo alineamiento, no origen molecular ni exactitud del alineamiento. Los perfiles individuales deMAPQ/NM/AS/anclas no se guardaron originalmente porque no se retuvo elSAM/BAMcompleto; no es un dato que pueda inventarse tras la caída. Procesamiento basal yexplicaciones técnicas quedan sin adjudicar. El mapa biológico/lotes/pares sigue sin acreditarse explícitamente; se conserva la declaración previa de los autores de3réplicas porcondición, sin refutarla porla carencia.

Prioridad inmediata: recuperar los artefactos originales pendientes cuando vuelva el entorno, sin reejecución automática para ocultar la pérdida. Después, QC específico del soporte bajo con selección/controles previos ysin modificar las cuentas históricas: [propuesta](../../research/plans/2026-10-31-stmn2-low-count-control-qc.md). Todavía no se ha ejecutado. No iniciar otros cuatro runs.

Solo datos publicados de cultivo, accesiones/grupos yvariables técnicas; sin datos clínicos personales,QNAME o secuencias exportados. Exploración/QC técnico; no replicación externa establecida ni validación funcional. PR33revisable,sinmerge/cierre;PR30intacto;sin costes,contactos,publicación externa o laboratorio.
