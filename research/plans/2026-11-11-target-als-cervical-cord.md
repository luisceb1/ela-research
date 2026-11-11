# Médula cervical de TARGET_ALS frente a corteza motora — plan prospectivo

Fecha: 2026-11-11. Autorización de Luis. Diseño corregido tras una **revisión externa** (ChatGPT) cuyas cinco instrucciones se incorporan y se citan donde aplican. Base: main `9dc97c6`, rama `claude/youthful-hypatia-v0ehce`.

**Este plan se fija ANTES de descargar las uniones de médula o calcular nada sobre ellas.**

## Un único tejido, elegido de antemano

**`TALS_Spinal_Cord_Cervical`** es la comparación primaria y la única de este ciclo. **Lumbar y torácica quedan fuera**, y solo se abrirían si aportasen una comprobación necesaria que este ciclo identifique. No se descargan los tres segmentos para elegir después el que dé el resultado más vistoso.

Inventario ya hecho (metadatos, 2,4 KB): 164 muestras, con 95 `ALS Spectrum MND`, 26 mixtas, 24 sin etiqueta, 13 `Non-Neurological Control`, 3 otros, 2 pre-fALS, 1 `Other MND`.

## Emparejamiento por donante: comprobado y NO disponible

Pertenecer al mismo consorcio no implica proceder de las mismas personas. Comprobado: `ExternalSampleId` (`CGND-HRA-…`) es un identificador de **muestra**, no hay columna de sujeto, y la intersección por prefijo entre corteza y cervical es **cero**, lo que indica que el identificador no codifica donante.

**Consecuencia declarada de antemano: será una comparación entre conjuntos de muestras distintos, no emparejada por donante.** No se afirmará que comparte donantes, ni se tratará como pareada, ni se usará el solapamiento de prefijos como prueba de nada. El número de sujetos distintos por tejido es **desconocido** y se informará como tal.

## Pregunta, formulada sobre tejidos

**¿Difieren la cobertura y el uso relativo de estas uniones entre corteza motora y médula cervical?**

Formulación deliberada: el tejido contiene varios tipos celulares, de modo que este contraste **no identifica por sí solo una dependencia del tipo neuronal**. No se presentará como prueba de H1.

## Denominadores, fijados antes del análisis

Se informarán **tres** cosas por grupo y tejido, y la comparación primaria es la tercera:

1. **Cada unión por separado** (`cryptic_left`, `cryptic_right`, `canonical`): mediana, máximo, nº de muestras con alguna lectura y con ≥20.
2. **Razón sumada** `(cL+cR)/(cL+cR+canónica)`, solo por continuidad con los ciclos anteriores.
3. **PSI por unión** `media(cL,cR)/(media(cL,cR)+canónica)` — **comparación primaria**. Razón: una molécula con el exón críptico ofrece dos uniones donde leer y una sin él ofrece una, de modo que sumarlas infla la razón ≈2× a valores bajos. Ninguna de las dos es un porcentaje de moléculas medido; son razones de cuentas, y así se nombran.

**Normalización obligatoria de cobertura:** la cobertura canónica **no** se comparará en lecturas brutas entre tejidos. Se normalizará por lecturas asignadas a exones de `recount_qc` y se informarán ambas cifras. Una cobertura mayor sin normalizar **no** demuestra mayor expresión.

## Predicciones refutables

- **P1 (cobertura):** la cobertura canónica normalizada de UNC13A será **menor en médula cervical que en corteza motora**. Es la versión comprobable de la observación de Ikegami 2026 y del panel GTEx de Mallika 2026, ahora dentro de una sola cohorte y tubería.
- **P2 (detección):** la proporción de muestras del espectro ELA con alguna lectura críptica será **menor en médula que en corteza** (en corteza fue 23/109, 21 %).
- **P3 (umbral):** **ninguna** muestra de médula alcanzará 20 lecturas en una sola unión críptica.

Si P1 se refuta —médula con cobertura normalizada igual o mayor— caería la explicación por expresión tisular y habría que buscar otra; se informaría así sin rescatar la predicción.

## Método

1. Descargar uniones y `recount_qc` de `TALS_Spinal_Cord_Cervical`. Registrar SHA256 y tamaños. **Presupuesto: ≤400 MB**, un solo tejido.
2. Aplicar el mismo script y las **mismas coordenadas selladas**, sin redefinir. El guardián de convención debe pasar; `assay_shape()` debe confirmar que no parece dirigido.
3. Entregar **una tabla por tejido** con: n de muestras, nº de sujetos (desconocido, declarado), cobertura canónica bruta y normalizada, detección por unión, y las dos razones. Esa tabla es el entregable.
4. Incertidumbre: para las proporciones de detección se dará intervalo de Wilson al 95 %. **No** se calcularán p-valores entre tejidos: son conjuntos de muestras distintos, sin emparejamiento y con confusores no medidos.

## Conclusión admisible, acotada de antemano

Si ninguna muestra alcanza el umbral, la conclusión será: **esta búsqueda se cierra por falta de precisión con los datos examinados.** No se concluirá que el umbral sea inalcanzable en todo el RNA-seq público, ni se extrapolará más allá de los cinco datasets examinados.

## Límites

- Tejido bulk; composición celular no medida y confusora.
- 13 controles no neurológicos por tejido: descriptivo, no estimación estable.
- Sin identidad de donante: comparación no emparejada, nº de sujetos desconocido.
- STMN2 fuera: sin coordenadas selladas en hg38.
- Datos personales: **solo** la columna de grupo. Sin filas clínicas individuales; el archivo de metadatos no se versiona.
- No se reclama novedad frente a las publicaciones del propio consorcio.
- Sin PSI inferencial, sin efectos, sin interpretación clínica.

## Entregables

`reports/target-als-cervical-20261111/`: `REPORT.md`, `results.json` y la tabla comparativa por tejido. Etiqueta de evidencia: **descriptivo exploratorio en tejido post mortem, comparación no emparejada entre tejidos**.
