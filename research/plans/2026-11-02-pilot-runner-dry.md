# Runner: plan de integración sin transporte real

Definir manifiesto inmutable, presupuestos globales persistidos y fases con recibos atómicos. El reloj/deadline no se reinicia al reanudar; transferencias fallidas siguen consumiendo presupuesto. Reutilizar solo archivos verificados por tamaño/MD5/SHA256; un archivo alterado o fase started/failed impide continuación automática. No borrar parciales o aumentar límites para resolver fallos.

Transporte exclusivamente inyectado con bytes sintéticos; procesos Pythonpequeños mediante supervisorv2. Validar éxito y reutilización, hash incorrecto, cambio de manifiesto/límites, archivo verificado alterado, presupuesto acumulado agotado, deadline global agotado, disco y fase interrumpida; comprobar integración del supervisor con callbackdeguardas globales. Presupuesto de pruebas60s/512MiB/10MB, sin red ni alineaciones. El runner simulado no acredita producción o descarga de6,35GB.
