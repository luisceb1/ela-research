# Cierre del piloto local UNC13A — 03/11/2026

Luis autoriza expresamente cerrar el piloto, anotarlo en GitHub e integrar la PR si la revisión lo permite. Estado definitivo del piloto: **cerrado, técnicamente completado, cobertura objetivo insuficiente**. No queda pendiente repetirlo o ampliarlo automáticamente.

## Resultado conservado

- CTRL-4 / GSM8975203 / SRR33425816: 12.709.444 pares validados; prefijo ordinal fijo de 1.000.000 analizado.
- Soporte canónico/crípticos [1,0,0] a anclajes 15 y 8, frente al mínimo prospectivo de 20 grupos. No ausencia biológica demostrada.
- Auditoría regional: 29/31 y 31/33 uniones coinciden con la anotación cacheada; las dos restantes, soporte unitario fuera de los objetivos, no constituyen nuevos hallazgos validados.
- Sello completo aportado, comparación, hashes y límites en `COMPLETE_REPORT.md`, `complete-assessment.json`, `operator-audit-seal.json` y `complete-comparison/`.
- Cargo de 7.322.807.977 bytes, incluida la reserva previa de navegador sin medición exacta; sin nuevas descargas para las auditorías. Mantener cargos, archivos, intentos fallidos y procedencia. No borrar ni reutilizar outputs huérfanos.

El cierre integra código, contratos y evidencia; no integra una conclusión biológica favorable ni habilita TDP. No modificar retrospectivamente objetivos o umbral para superar la puerta. No se han verificado independientemente todos los archivos WSL o el recibo externo de la auditoría nueva; los límites del informe siguen vigentes.

## Alcance de la integración

La PR 36 reúne las auditorías de GSE296714, la reproducción descriptiva STMN2/PAPA desde TPM (12/12 bibliotecas concordantes), los contratos/pruebas del procesamiento pareado y el resultado insuficiente del piloto UNC13A. Se conservan también las comprobaciones rechazadas y errores históricos. STMN2/PPAU no equivale a PSI de uniones, réplica biológica externa o rescate funcional.

Antes de integrar: revisar cabeza exacta, archivos cambiados, comentarios y CI. En la cabeza previa 184c6c4638296a7f4e97a80ab2678bf100db0af3 las tres familias de CI están correctas y no hay comentarios/revisiones pendientes. El commit documental de cierre tendrá sus propias comprobaciones. La fusión conservará el historial de commits y la rama, útil para los checkouts y planes fijados del operador. El estado de integración real se consulta en PR #36; este documento no anticipa el SHA del merge.

## Continuación priorizada

La issue #37 es el único seguimiento nuevo: https://github.com/luisceb1/ela-research/issues/37.

1. Auditar acceso a cuentas de uniones por muestra o alineamientos procesados y reconstruir unidades biológicas/lotes; evitar búsquedas ya cerradas. El procesado Humphrey ya inspeccionado no se presenta de nuevo como fuente inédita. Fijar un máximo de tres candidatos no agotados o una fuente nueva que resuelva un bloqueo concreto.
2. Contrastar coordenadas con una anotación más amplia o independiente y registrar uniones no coincidentes sin calificarlas como nuevas. Mantener la distinción entre gen, isoforma, unión y función.
3. Entregar una tabla de aceptación/rechazo con medición, cobertura documentada, independencia, réplicas, dependencias y coste. Si ninguna fuente cumple, cerrar ese ciclo; sólo una fuente aceptada justifica un nuevo plan prospectivo de cómputo.

No se inicia ahora otra descarga masiva, otra biblioteca, un contacto o una inferencia. Para inferencia se mantienen las unidades independientes verificables y las reglas de `research/NEXT_STUDY_GATE.md`; varias bibliotecas no sustituyen réplicas. Próximo entregable concreto: tabla de candidatos y una recomendación trazable, no más infraestructura por defecto.
