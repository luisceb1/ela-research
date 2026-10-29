# Reconciliar issue19 con main y ramas revisables

Pregunta: ¿la selección cero de STMN2/UNC13A sigue presente en main, y qué controles impiden repetir una salida vacía aparentemente exitosa?

Estado inicial comprobado: main13ccbc5c9f1c9744c57ed9abb822d169772e32a5 ya selecciona por ENSG. El test sin gene_name está fuera de la clase y usa separadores literales; el CLI solo falla si no coincide ningún TXNAME. El run histórico40868865843 fue marcado success pese a cero objetivos, según issue19.

Predicción refutable: al ejecutar el mapper actual sobre los mismos cuatro archivos públicos fijados por SHA256 obtendremos STMN2/UNC13A=4/7en cultivo y3/7en cerebro, como en las ramas previas. Si difiere, registrar discrepancia sin forzar los valores. El guard debe rechazar cero objetivos, identidad discordante y cuentas inválidas.

Método: fijar snapshotmain y fuentes históricas; usar checkout separado basado en main para un PR directo pequeño. Cotejar ensayos actuales y anteriores, crear tests realmente descubiertos sin gene_name y negativos, referencia GENCODEv47 fijada por hash. Reproducir mapper anterior/corregido con caché pública sin exportar filas individuales. Comparar resultados agregados con reports/isoforms en ramas pendientes, sin fusionarlas automáticamente.

Criterio de fracaso: fuente/identidad/cobertura de controles no verificada se marca insuficiente; no inferir ausencia biológica de un cero técnico. No repetir auditoría biológica o nuevos contrastes por arreglar el software. Tras controles, seguir issue20 según disponibilidad del ZIP original y filtros; no mezclar21/1910uniones.
