# Corregir el control de tiempo antes de continuar CTRL_R2

Pregunta técnica: ¿puede completarse el mismo archivo con plazos transcurridos independientes del reloj civil, manteniendo los límites originales y rechazando vencimientos reales?

Hipótesis de fallo: el guard anterior comparaba time.time con timestamps guardados; un ajuste del reloj puede producir falsos cortes. Los recibos señalan un corte a15,526642s con7.226.257.234B bajo12GB y deadline civil todavía lejano al último snapshot. No documentan el instante/causa del ajuste enWSL; la raíz del sistema no queda probada. Reproducir el defecto mediante reloj civil que retrocede y comprobar positivos/negativos antes de descarga humana.

Método nuevo aislado: CLOCK_BOOTTIME/boot_id comunes a padre y trabajador; timestamps civiles sólo informativos. Total2400s/copy300s/range1800s/verify300s, sin aumentar. Validar relojes/ticks y vencimientos desde padre aun con trabajador bloqueado. Muestrear tick después de leer un estado concurrente. Sellador valida duración y deadlines por ticks, no por diferencias civiles. Guardar ajustes civiles observados como diagnóstico.

Origen/rango fijos900998714–997549456 (96550743B), IPv4 conTLS/certificado/hostname, una petición206 yMD5entero007d66223fe35f394284e4ebd631eaef. Cargo inicial7226257234B incluye reserva previa de navegador997549457B, sin añadirla otra vez. Finalesperado7322807977B/saldo4677192023B bajo12GB. No reembolsar bloque anterior. Arrastre conservador16300,072928190231s no es tiempo medido.

Plan deshabilitado, ligado a código/Python/boot actual, root nuevo, identidad y cadena anterior. Ejecución requiereSHA exacto yaceptación de ventana40min con reloj transcurrido. Mismos27GiB onceárboles/reserva8GiB,2CPU/RSS512MiBmuestreada/AS1GiB/socket30s. Sin red al preparar, sin retry, otrosmates o alineamiento. Tras reinicio debe emitirse otro descriptor; no se reabre un intento.

Fracaso: cambia cadena/boot/source/prefijo, falla respuesta/MD5/tamaño o límites/reloj transcurrido/supervisor. Conservar intento y no ampliar automáticamente. Éxito: archivo entero verificado y sello externo; sólo habilita preparar cómputo posterior del control.
