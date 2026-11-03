# CTRL_R2: continuación tras Ctrl+C — 03/11/2026

## Evidencia

Luis interrumpió el intento cbf56db7… con Ctrl+C al probar el navegador. El supervisor terminó con−9/KeyboardInterrupt y grupo vacío; una segunda ejecución fue rechazada antes de reabrir la carpeta. Copia verificada, Range started sin cierre final. Parcial900.375.051B; recibo20.971.520B nuevos desde876.279.389 y4MiB reservados. CargoWSL6224513473B; cargo nuevo25165824B y diferencia conservadora1070162B respecto al crecimiento real. Quedan97174406B. No archivo entero verificado ni alineamiento.

Navegador: Luis declara74MB aproximados. WSL tiene90,3%; se elige el parcial deWSL y se indica cancelar navegador. No hay recibo de cuerpoHTTP del navegador ni verificación de su parada todavía.

## Cambio y propuesta

Nuevo recover_ctrl_r2_resume.py aislado valida la cadena anterior, planSHA exacto, aceptación, KeyboardInterrupt/grupo vacío, counters/reserva y parcial. Copia/hash y una peticiónRange900375051–997549456 reutilizando sin cambios transporteIPv4/TLSverificado y sellador heredados. MD5entero007d66223fe35f394284e4ebd631eaef/tamaño997549457 antes de promoción/sello. No modifica DNS, históricos o ledgers; sin retries, otrosmates, descompresión o alineamiento.

Propone reserva explícita997549457B para un intento manual de navegador (un archivo entero), separada de6224513473B medidos/conservadores deWSL. No se afirma que el navegador transfirió ese tamaño ni que sea una cota de múltiples retries externos. Cargo inicial propuesto7222062930B/final7319237336B/saldo4680762664B bajo12GB; debe aceptarse browser detenido/reserva. Registrar o aclarar tráfico externo antes de ampliar a otras bibliotecas.

Nueva ventana2400s total/1800sHTTP, copia y verificación300s. Arrastra conservadoramente los1800s de la ventana interrumpida además de12700,072928190231s:14500,072928190231s. No es medición de tiempo gastado: el supervisor registra347,572033296s externos, y el snapshot no es cierre. Mismos27GiB contando diez árboles/reserva8GiB,35GiB libres previos,2CPU/RSS512MiBmuestreada/AS1GiB/socket30s. Preparación deshabilitada no descarga ni acepta; ejecución exigeSHAexacto, tiempo y navegador detenido/reserva aceptados.

## Validación y límites

24 pruebas nuevas correctas: recuperación/sello artificial, Range/MD5/cabeceras, reserva/timeout, original cambiado, interrupción/grupo, cambios de clocks/cargos, diez árboles, propuesta/reserva manual fijada y aceptación de browser antes de acceso al plan. CLI worker supervisado falla antes deHTTP con metadatos ausentes y deja grupo vacío. Regresión incluye TLS real local y certificado/hostname rechazados. Total/versiones en validation.json/tests.txt; compileall correcto. Positivos artificiales, sinHTTP de crudos humanos ni alineamientos en el host del agente. Persisten límites de host/I/O, DNS, RSS/disco muestreados y contabilidad externa no medida.

## Siguiente paso

Emitir/revisar planWSL, confirmar navegador detenido y aceptar ventana/reserva concretas antes de ejecutar. Tras eventual sello, preparar cómputo sólo del control con ambos mates locales. No se ha demostrado efecto biológico, PSI, rescate o beneficio clínico. PR36 permanece abierta, sin merge.
