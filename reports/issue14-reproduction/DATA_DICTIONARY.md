# Diccionario

expression_aggregate.tsv: una fila por gen, siete pares técnicos TP/TN correspondientes al diseño emparejado publicado. Deltas=TN−TP en log2. Cambio porcentual=100×(2^delta_media−1). Intervalos t descriptivos y pruebas de inversión de signos exploratorias reproducidas; no nuevas afirmaciones de significación. CPM_named_only es sensibilidad que elimina filasNAde la suma de biblioteca, no una nueva cohorte. No se exportan recuentos, factores ni diferencias por caso.

dexseq_aggregate.tsv: una fila por gen con conteos de fragmentos y p ajustados preexistentes. provided_padj_missing no significa efecto nulo. Los umbrales0.05/0.10son descriptivos sobre el resultado publicado; no FDRreajustada a tresgenes ni PSI. qc.json incluye nombres técnicos countData y cobertura condicional de intervalos recibidos, no filas clínicas.

comparison.tsv: valor agregado esperado frente al recalculado y tolerancia indicada en informe;63 comparaciones no son63 experimentos. package_provenance.json:hashes de trespaquetes y miembros permitidos; no lectura de tablas por caso ni genéticas. received_code conserva scripts sin ejecutar, incluidos sus exportadores históricos, para revisión de procedencia.
