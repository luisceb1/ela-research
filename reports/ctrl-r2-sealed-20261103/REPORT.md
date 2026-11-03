# CTRL_R2 completo y verificado — 03/11/2026

Luis aporta el sello `sealed_verified_ctrl_r2_elapsed` de la ejecución c23994f. Archivo completo997.549.457B; MD5entero007d66223fe35f394284e4ebd631eaef coincide con el origen fijado; SHA256b034affa4479b28154fa9217a943128c4513590f6e622690a7af7afd272ca2f6. Los seis hashes y políticaCLOCK_BOOTTIME quedan en user-reported-seal.json. Es evidencia de terminal, no inspección remota del archivo.

Cargo contabilizado7.322.807.977B y saldo4.677.192.023B. Incluye la misma reserva manual de navegador997.549.457B; no es tráfico externo medido. El éxito con el nuevo reloj no prueba por sí solo la causa exacta de los fallos anteriores. No se aportan duración, RSS o eventos de ajuste del nuevo intento; no se inventan ni se deducen de pruebas artificiales.

Índice y CTRL_R1 ya tenían sellos aportados anteriormente. Se completa la recuperación del segundo mate; no repetir descargas de índice/R1/R2. No se ha validado aquí el emparejamiento/EOF de ambos archivos, alineado el control ni calculado cobertura. raw_execution_ready=false corresponde a que el piloto completo sigue pendiente; no invalida el archivo sellado.

Siguiente tarea única: preparar un piloto local sólo del control con estos tres insumos, sin HTTP/TDP. Revalidar cadena y archivos, EOF/CRC/nombres de pares, prefijo fijo1M, alineamiento/extractores y umbral20 ya fijados. Mantener filtros/targets originales y reloj transcurrido en todas las fases; revisar disco del linaje y tiempos de cómputo antes de proponer descriptor concreto. Conservar cargos e intentos. No reutilizar el worker antiguo que volvería a descargar ni activar la segunda biblioteca automáticamente. Plan prospectivo research/plans/2026-11-03-offline-control-after-r2.md.

Entrega documental de actualización del estado, sin cambios de código o reejecución de pruebas. Las460pruebas/CI corresponden al código c23994f, no a una validación humana del alineamiento. PR36 abierta sin merge. Sin PSI,inferencia,rescate o beneficio clínico.
