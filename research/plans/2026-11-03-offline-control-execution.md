# Piloto local sólo del control

Pregunta prospectiva: ¿tiene el prefijo fijo de 1.000.000 pares de CTRL-4 / GSM8975203 / SRR33425816 soporte suficiente en UNC13A con el método original? Criterio: al menos 20 grupos (RG, QNAME) aceptados con al menos un objetivo con anclaje de 15 bases. Los eventos se cuentan por separado. La sensibilidad conserva el anclaje de 8 bases. No se cambian objetivos ni filtros tras observar cobertura.

Se reutilizan el índice hg38 y ambos FASTQ sellados. La preparación comprueba metadatos y tamaños. El trabajador comprueba los hashes de las lecturas y del índice, valida todos los pares y extrae el prefijo. Los sellos históricos pueden proceder de otro arranque; la ejecución nueva queda ligada al arranque actual y a CLOCK_BOOTTIME.

| Fase | Máximo |
|---|---:|
| Preflight | 180 s |
| Copia local R1 | 300 s |
| Copia local R2 | 300 s |
| Validación completa y prefijo | 900 s |
| Cómputo: productor / reducción | 900 / 300 s |
| Total, incluido margen de 120 s | 3000 s |

Se conserva HISAT2, sus argumentos y el motor pareado original. Límites: 2 CPU, RSS de grupo de 6 GiB muestreada y espacio virtual de 8 GiB por proceso. Disco: 27 GiB más reserva de 8 GiB; particiones de 18 GiB para artefactos, 2 para prefijos, 6 para temporales, 0,5 para dependencias y 0,25 para recibos. Se cuentan doce árboles. Antes de copiar se exige que el histórico y las dos copias nuevas (1.958.406.420 bytes) quepan en artefactos. No se eliminan originales.

No hay fases HTTP ni TDP. El cargo permanece en 7.322.807.977 bytes, incluida la reserva de navegador ya contabilizada. El audit hook de Python bloquea conexiones y resolución; no constituye un aislamiento de red de procesos nativos. Los ejecutables y argumentos están fijados y no contienen URL.

El descriptor se prepara deshabilitado y exige aceptar su SHA exacto y la ventana local. La raíz es exclusiva. Ante fallo se conservan recibos y no se reintenta automáticamente. Una ejecución completa se sella tanto con cobertura suficiente como insuficiente. Ninguna habilita una segunda biblioteca ni permite inferir PSI, efecto, causalidad, función o beneficio clínico.
