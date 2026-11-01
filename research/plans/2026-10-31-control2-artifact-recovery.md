# Recuperación de artefactos tras pérdida del entorno — plan previo a validación

31/10/2026. El segundo control completó la fase con salida0,55bins concordantes y54.292.655lecturas; su resumen yQC deFASTQ se imprimieron antes de perderse el entorno. La operación posterior de escritura de informe/replay no retornó: no declarar su finalización.

Pregunta: ¿pueden recuperarse exactamente dosJSON a partir de la salida capturada? Predicción refutable: deben coincidir con losSHA256 originales que el exportador registró antes del fallo. Control independiente delformato/contenido: comparación criptográfica de bytes enCI Python3.11/3.12, además de conteo/histogramas. Fracaso si cualquiera difiere: no llamarlo recuperación exacta ni cambiar hashes para conseguir aprobación. No nuevo alineamiento, datos, cohortes o inferencia.

No reconstruir filas25últimas delTSV niJSON completos de extractores que no fueron impresos. Conservar elcheckpoint30M ya remoto ylos archivos faltantes como bloqueo. Registrar porseparado análisis completo verificado ypaquete deartefactos incompleto. No nueva ejecución de54M para encubrir pérdida, ni autorización de gastos/publicación/contactos/merge/cierre.
