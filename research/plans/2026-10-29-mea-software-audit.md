# Auditoría técnica de dos prototipos MEA sintéticos

Pregunta: ¿las pruebas de los paquetes anteriores se reproducen y las reglas de elegibilidad, aleatorización, pérdidas y clasificación conservan el estimando declarado?

Predicción refutable: los tests originales pasarán en un entorno compatible, pero eso no garantiza que los importadores rechacen entradas experimentales incompletas ni que todos los escenarios estén libres de sesgo. Buscar contraejemplos con datos artificiales mínimos.

Método previo: verificar hashes de ZIP/miembros frente al inventario; leer código, imports y efectos de nivel superior antes de ejecutar. Ejecutar solo pruebas/funciones revisadas en copia de caché aislada. No invocar generadores de gráficos, informes, consolidadores con efectos al importar ni CLI completo de MonteCarlo. Registrar entorno y versiones; no instalar dependencias sin necesidad.

Controles: ausencia técnica frente a muerte, elegibilidad solo con medidas previas, equilibrio dentro de diferenciación, cambio respecto basal frente a beneficio relativo, unidades anidadas y reagrupación de brazos. Crear pruebas de contraejemplos cuando aporten información distinta a tests existentes.

Fracaso: error de dependencia o test se registra sin fingir reproducción. Clasificador que acepte datos mal definidos o genere etiquetas de recuperación en un control adverso se documenta con fixture; si se corrige, conservar original por hash y cambiar solo copia versionada. No usar estas simulaciones como evidencia biológica, potencia real o tamaño muestral. Sin gráficos simulados. Resultados técnicos en GitHub por PR; siguiente tarea segura se seleccionará según el hallazgo.
