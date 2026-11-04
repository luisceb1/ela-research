# Reproducción aritmética descriptiva A25 Fig.3s —04/11/2026

Luis autoriza «adelante» tras la propuesta de reconstruir puntos y medias, cotejarlos con los resúmenes publicados y registrar discrepancias. Se amplía explícitamente la auditoría previa solo a esta comprobación descriptiva. No se autoriza inferencia, nuevos contactos/datasets o reactivación automática. No se fusionan PR por defecto.

## Pregunta y predicción refutable

¿Las38 entradas WT y35 R202H depositadas para Fig.3s reproducen las dos medias publicadas en Supplementary Data3, Table3, C35/E35?

Predicción: las medias aritméticas no ponderadas de todos los valores válidos de cada grupo concuerdan con las publicadas dentro del redondeo de sus cifras. Comparación exacta de los n. La comprobación no presupone independencia biológica.

## Datos fijados y controles

- MOESM10: SHA25642f9a2266bf8e7dc157350fe588f1d87deb8d0e4c5067bc2c780b9fc7851a49f. Figure3_R202H, I1/J3, I4:I41 yJ4:J38. Reutilizar el lector validado; no reconstruir otro parser.
- MOESM8: SHA2567ba494959360e824eb333eeadb2e0fd1bb431a32859da92cabdd5a958cf1c2e7. Table3, C18/E18=grupos, B35=Charge(pC), I35=3s, C36/E36=n38/35. Recuperar solo la parte de media de C35/E35; no extraer p-valores ni recalcular SEM.
- Mantener cada valor fuente, sin exclusiones, deduplicación, ceros imputados, recortes o conversiones. Vacíos terminales no son0. No vincular filas I/J como parejas.
- No confundir amplitud nA de B33 con carga pC de B35 ni usar otros paneles/condiciones por compartir n. No buscar otra combinación de valores si falla la predicción.
- Cálculo Decimal con precisión50; suma/n. Tolerancia inclusiva de media unidad de la última cifra decimal escrita en la media publicada. Esta tolerancia es de redondeo, no error de medición, intervalo de confianza o incertidumbre biológica. Si el texto de media no se interpreta inequívocamente, registrar fallo sin adivinar.

## Figura y límites

Figura estática de los73 puntos depositados y las dos medias calculadas; posiciones horizontales separadas de forma determinista para visualización, sin pareamiento ni datos nuevos. No barras SEM/IC, pruebas, estrellas, efecto entre grupos, normalización porcentual o conclusión de eficacia. Etiquetar observaciones y ausencia de mapa de cultivos. Guardar versión del trazador, parámetros, hashes, PNG/SVG y revisión visual.

## Criterio de fracaso y parada

Fracaso de concordancia si cambia un hash, faltan/grupos/unidades/n o alguna diferencia supera la tolerancia declarada. Conservar todo resultado negativo y revisar solo controles de identidad, selección, unidades y denominador ya definidos. No ajustar a posteriori redondeo, excluir valores o cambiar endpoint para obtener concordancia.

Concordancia significa reproducción aritmética de resúmenes publicados del mismo estudio, no replicación biológica nueva. El mapa observación→cultivo, identidad/exclusiones y NO-GO inferencial siguen pendientes aunque ambas medias concuerden. La sesión termina con un informe reproducible y PR revisable.
