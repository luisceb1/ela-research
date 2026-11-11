# STMN2: derivar y sellar sus uniones en hg38, y probar si supera el umbral — plan prospectivo

Fecha: 2026-11-11. Autorización de Luis («abre el ciclo STMN2»). Base: main `9dc97c6`, rama `claude/youthful-hypatia-v0ehce`.

**Este plan se fija ANTES de derivar coordenadas o calcular nada.**

## Por qué STMN2 y por qué ahora

El ciclo anterior cerró la búsqueda de cobertura **para UNC13A** y anotó que no se propongan más datasets de transcriptoma completo para esa pregunta. Este ciclo **no** la reabre: cambia de gen, por una razón cuantitativa medida en este propio proyecto.

En las motoneuronas de Klim, con cuentas génicas de recount3 ya verificadas: **STMN2 CPM 2.145,6 frente a UNC13A 178,5 en control, es decir 12 veces más expresado.** Y el ciclo cervical estableció que lo que condena a UNC13A es la cobertura del locus (0,11 lecturas canónicas por millón en médula cervical).

Hipótesis de este ciclo: **si el fracaso de UNC13A era de cobertura y no de método, STMN2 debería superar el umbral de 20 donde UNC13A no llega.** Es la predicción directa del hallazgo de ayer y es refutable.

Además STMN2 es la diana que importa en motoneuronas espinales, el tejido donde UNC13A está peor cubierto.

Datos: **ya descargados** (TARGET_ALS corteza 194 MB y médula cervical 213 MB contienen **todas** las uniones). Presupuesto de descarga adicional de este ciclo: **≤50 MB**, solo metadatos si hiciera falta.

## Parte 1: derivación de coordenadas, con sellado y verificación

El proyecto **no** tiene coordenadas de uniones de STMN2 en hg38. Tiene:

- Gen en hg38 (GENCODE v47, auditado): `chr8:79.611.117–79.666.158`, hebra **+**, `ENSG00000104435`.
- Región de conteo del exón críptico **en hg19**: `chr8:80.529.057–80.529.284`, ancho 228, de `10.1007/s00401-023-02655-0`.

**No se improvisa una conversión de ensamblaje.** La derivación se hace por **estructura**, con la anotación y los datos ya en disco:

1. Listar todas las uniones del `RR` dentro de los límites hg38 del gen.
2. **Canónica:** la unión **anotada** (`annotated=1`) más 5′ en hebra +, que corresponde a exón 1 → exón 2.
3. **Críptica candidata:** unión **no anotada** (`annotated=0`) que **comparte el donante** con la canónica (mismo `start`) y cuyo aceptor cae **dentro del intrón 1**, es decir entre el donante canónico y el aceptor canónico.

Fundamento biológico declarado: el splicing críptico de STMN2 usa el **donante canónico del exón 1** con un **aceptor críptico en el intrón 1**; el exón críptico contiene una señal de poliadenilación prematura, de modo que el transcrito termina ahí. **Por tanto se espera UNA sola unión críptica, no dos** — a diferencia de UNC13A, que tiene dos por flanquear un exón interno.

**Consecuencia sobre el denominador, fijada ahora:** con una única unión críptica, inclusión y exclusión aportan una unión cada una, de modo que `críptica/(críptica+canónica)` **sí** está en pie de igualdad por unión. No aplica la corrección ×2 de UNC13A. Se informará esa razón y también cada unión por separado.

### Verificaciones obligatorias de la derivación

La candidata se acepta **solo si pasa todas**:

- [ ] Motivos de splicing **GT/AG** (hebra +).
- [ ] `left_annotated` no nulo (donante conocido) y `right_annotated` nulo (aceptor novedoso).
- [ ] Aceptor estrictamente dentro del intrón 1.
- [ ] Reproducible de forma **independiente en los dos tejidos** ya descargados (corteza y médula cervical), con la misma fila de coordenadas.

**Cruce con la literatura:** el intervalo publicado está en hg19 y el proyecto no tiene un ancla fiable para convertirlo. Si no se puede establecer el desplazamiento de ensamblaje sin suponer, se registrará el cruce con hg19 como **NO REALIZADO**, en vez de forzarlo. La derivación se sostendrá entonces solo sobre estructura y anotación, y así se declarará.

**Si hay más de una candidata** que pase las verificaciones, se informan **todas** y no se elige una; el ciclo se detiene antes de medir hasta que haya criterio para distinguirlas.

El resultado se sella en `research/references/stmn2_targets_sealed.json`, con su procedencia y el método de derivación, para que ciclos futuros no lo rederiven.

## Parte 2: medición, solo si la Parte 1 pasa

Aplicar la sonda ya probada a los dos tejidos con las coordenadas selladas.

### Predicciones refutables

- **P1 (cobertura):** la cobertura canónica normalizada de STMN2 en médula cervical será **al menos 10 veces** la de UNC13A en el mismo tejido (UNC13A: 0,11 por millón).
- **P2 (umbral):** **al menos una** muestra alcanzará **≥20 lecturas** en la unión críptica de STMN2. Es la predicción central del ciclo.
- **P3 (dirección):** la detección de la unión críptica será mayor en el espectro ELA que en controles no neurológicos.

Si P2 se refuta, la conclusión será que el umbral de 20 **no es alcanzable en tejido post mortem bulk ni para una diana 12 veces más expresada**, lo que reforzaría la explicación por dilución celular y cerraría la vía de transcriptoma completo para **ambas** dianas, no solo para UNC13A. Eso sería un resultado, no un fracaso.

## Límites

- Tejido bulk; composición celular no medida y confusora.
- Comparación entre tejidos **no emparejada**: sin identidad de donante.
- Las razones no se interpretan por debajo de un denominador mínimo; se declarará el umbral usado.
- Sin p-valores entre tejidos; intervalos de Wilson para proporciones de detección.
- **No se reclama novedad**: el splicing críptico de STMN2 está ampliamente publicado y el consorcio ha trabajado estos datos.
- Datos personales: **solo** la columna de grupo, como en los ciclos anteriores.
- Sin efectos, sin interpretación clínica.

## Criterios de fracaso y parada

- Ninguna candidata pasa las verificaciones ⇒ parar y registrar; **no** relajar criterios ni aceptar una unión por parecido.
- Más de una candidata indistinguible ⇒ parar antes de medir.
- Un solo ciclo, dos tejidos, dos genes. No se amplía a lumbar ni torácica.

## Entregables

`research/references/stmn2_targets_sealed.json` y `reports/stmn2-derivation-20261111/`: `REPORT.md`, `derivation.json` con las verificaciones y `results.json` por tejido. Script con pruebas. Etiqueta de evidencia: **derivación de coordenadas verificada estructuralmente + medición descriptiva**.
