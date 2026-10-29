# Contrato de inventario

Cada fila es una proyección de ensayo/versión, no una réplica ni un estudio independiente. Clave id única; version impide transferir automáticamente un preprint a un aceptado. data_access=retrieved solo cuando hay datos tabulados/imágenes pertinentes recuperados; un PDF narrativo o declaración no basta.

Campos verified: unit_key (unidad estable), biological_batch_key (lote/diferenciación), observation_time (tiempo por observación), first_dose_link (primera dosis enlazada), paired_baseline (basal de la misma unidad), post_deficit_start (inicio tras déficit documentado), aligned_control (comparador enlazado al mismo criterio/calendario), functional_outcome (desenlace funcional pertinente documentado). true=verificado para ese campo; false=no presente en proyección o temporalidad incompatible según nota; null=no verificado. No son ausencia biológica.

reconstructible exige todos los campos true, acceso a datos y ninguna categoría temporal incompatible. La salida false significa no reconstruible con materiales inspeccionados, no que el ensayo o sus datos no existan. blockers conserva todos los motivos, sin ocultar enlace faltante por un fallo temporal. synthetic_contract de tests no se incluye en inventario.
