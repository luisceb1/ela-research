# Plan previo: P1 descriptivo y sensibilidad

Tras el mapeo exacto (#2), seleccionar la siguiente tarea segura: comparación descriptiva de GSE310723, seguida de sensibilidad entre bibliotecas cerebrales sin combinar series.

Pregunta: ¿la dirección del contraste Ctrl→TDP43KD para cada transcrito diana se mantiene con uniqueCounts frente a counts y con o sin ajuste por suma de cuentas? ¿qué tan sensibles son los cocientes cerebrales a retirar una sola biblioteca de cada pequeño grupo?

Predicción refutable específica, fijada tras el mapeo y antes de este contraste: la estructura STMN2 BambuTx9249 tendrá mayor soporte relativo en TDP43KD en ambos brazos con/sin 5Aza, y el ENST principal menor soporte. La selección es exploratoria y dependiente del mapeo, no una hipótesis independiente validada. Los dos brazos no constituyen réplicas biológicas.

Controles: identidad y hash de matrices, muestras y transcritos; mantener counts fraccionales y uniqueCounts separados. Comparar valor bruto, valor por millón de cuentas asignadas a transcritos y cuota dentro del gen (no CPM depositado ni PSI). Denominadores cero producen NA explícito; sin pseudocuentas ni p-valores. Registrar GCD de uniqueCounts por biblioteca para detectar escala/discretización, sin interpretar unidades como moléculas independientes.

Para cerebro, conservar ALS, ALS-ci y ALS-C9 por separado frente a CTL. Mostrar medias, mínimos/máximos y cocientes al retirar una biblioteca del grupo o del control, con n=2 por etiqueta; no estimar significación, causalidad, homogeneidad clínica ni potencia estadística. Nunca comparar directamente niveles cultivo↔cerebro.

Fracaso de robustez: dirección dependiente de medida o normalización, denominador cero o cocientes leave-one-out a ambos lados de 1. No rechazar resultados nulos. Los cambios observados no son rescate molecular/funcional, y los metadatos no prueban que cada biblioteca cerebral tenga una carga TDP-43 equivalente.

Salidas deterministas en reports/descriptive, tests de ceros y sensibilidad, informe Evidencia/Interpretación/Limitaciones/Siguiente prueba. Próxima prueba posterior: verificar evento críptico por coordenadas independientes y soporte de uniones/lecturas; no avanzar a laboratorio ni clínica.
