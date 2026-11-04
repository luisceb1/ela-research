# Plan previo de trazabilidad y comprobación R — 04/11/2026

Luis autoriza completar la trazabilidad y comprobar el bloque mínimo R en la misma PR48. Se conserva el análisis descriptivo previo; no se añade un contraste inferencial.

1. Identificar el panel editorial y contrastar modelo, perturbación, duración, normalización, n declarado y avisos editoriales con texto/métodos/leyendas primarios. No transferir datos de otras figuras o del modelo K26.
2. Intentar recuperar solo Source Data Fig.2 (41586_2022_4436_MOESM16_ESM.xlsx, límite 3MiB por petición). Contrastar etiquetas y valores, si sus bytes son válidos. Registrar errores o accesos HTML sin declarar lectura de la hoja. No descargar tablas clínicas o genotipos.
3. Separar identidad del modelo, n declarado y claves por observación verificadas. El CSV contiene cinco valores de proteína UNC13B por condición frente a tres de las demás series; no seleccionar los tres primeros ni imputar emparejamientos. Dosis enumeradas en métodos no prueban por sí solas la asignación de cada etiqueta Dox.
4. R no está disponible localmente; apt no ofrece candidato y la actualización falla al intentar cambiar UID/GID. No escalar privilegios ni modificar el sistema. Ejecutar una comprobación aislada en GitHub Actions: R4.4.3, dplyr desde snapshot CRAN/Posit 2025-06-01, trabajo limitado a10min y descarga CSV<16KiB/20s, sin Rmd completo, pruebas biológicas o servicios de pago. Solo el bloque de preparación de datos y la comparación con las salidas Python. El workflow temporal se retira tras obtener resultado/registro; Rscript y recibo se conservan para repetición.
5. Predicción técnica ya registrada: el R original perderá seis errores estándar y la variante de unión previa conservará todos; medias idénticas. Aceptar o refutar con ejecución y diferencias numéricas <=1e-12, registrar versión/sessionInfo y cabeza CI. Una incidencia de código no implica error de la figura editorial.

Finalización: informe de trazabilidad con confirmado/desconocido, resultado R o bloqueo explícito, enlaces/hash y actualización de PR48. Sin contactos, gastos, nuevos análisis/figuras biológicas, fusión automática o cambios en #46/#47.
