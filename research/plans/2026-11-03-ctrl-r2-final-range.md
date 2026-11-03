# Recuperar el tramo restante de CTRL_R2

Pregunta técnica: ¿puede completarse el parcial de 876.279.389 B con una única petición HTTPS/IPv4 y verificarse el MD5 entero, conservando los cargos y fallos anteriores?

Diseño fijado: copiar y comprobar el SHA del parcial; pedir bytes876279389–997549456; exigir206/Content-Range/Content-Length exactos, TLS con certificado y hostname verificados, IPv4 y sin proxies/redirects/retry. Reutilizar sin cambios el transporte y sellador del módulo IPv4 anterior. MD5 entero007d66223fe35f394284e4ebd631eaef y tamaño997549457 antes de promoción/sello.

Cargo inicial6.199.347.649 B, tramo121.270.068 B y final esperado6.320.617.717 B bajo el mismo techo12GB. No devolver4.111.506 B de reserva anterior. Conservar los7.300,072928190231s anteriores más la ventana agotada completa5400s:12.700,072928190231s, sin inventar el instante de parada. Todos los intentos permanecen intactos.

Propuesta pendiente: nueva ventana2400s total/1800sHTTP, copia300s/verificación300s; mismos27GiB contando nueve árboles/reserva8GiB,2CPU/RSS512MiBmuestreada/AS1GiB/socket30s. SHA exacto y aceptación explícita para ejecutar. Preparar no acepta ni descarga.

Fracaso: origen/metadatos/prefijo modificados, conexión fallida, respuesta/rango/longitud distintos, MD5/tamaño incorrectos, límites excedidos o supervisor no limpio. Guardar el fallo, sin repetir ni ampliar automáticamente. Éxito sólo con archivo completo y sello externo. No otros mates, descompresión o alineamiento; cómputo posterior requiere adopción del control verificado.
