# Reproducción descriptiva de los datos fuente de Ikegami/Koike 2026 — plan prospectivo

Fecha: 2026-11-10. Autorización de Luis el 10/11/2026 para esta extensión acotada. Base: main `3916b77ec0546e9d327e6d54e4dacd90d1a51ce4`, rama `claude/youthful-hypatia-v0ehce`.

**Este plan se fija y se confirma ANTES de abrir el XLSX.** No se ha inspeccionado ninguna celda al redactarlo.

## Fuente

Ikegami I, Hongo S, Koyama A, Hayakawa-Yano Y, Yano M, Sugai A, Ishihara T, Tada M, Kakita A, Onodera O, Koike YM. «TDP-43-related cryptic splicing reflects pathological heterogeneity in amyotrophic lateral sclerosis». *Acta Neuropathologica Communications* 14:229, 2026-08-08. DOI 10.1186/s40478-026-02400-0. PMID 42983891, PMC13737708. Revisado por pares, acceso abierto CC-BY-NC-ND 4.0.

Archivo: Additional file 3 (`40478_2026_2400_MOESM3_ESM.xlsx`, ~29 KB), descrito en el artículo como «Source data underlying all quantitative figures presented in the main text and supplementary materials». Vía: endpoint `supplementaryFiles` de Europe PMC. Se registrará SHA256 del ZIP y del XLSX. **El archivo no se versiona en el repositorio** (licencia ND y política del proyecto); solo hashes, tablas derivadas propias y citas cortas.

## Qué es y qué no es

Verificación descriptiva de reproducibilidad interna: ¿los números depositados reproducen los estadísticos publicados? **No** es validación biológica, **no** es replicación independiente (son los mismos sujetos y las mismas medidas) y **no** aporta cuentas de uniones.

**No avanza #37**, que exige cuentas de uniones por biblioteca o BAM/índices con mapa condición→unidad→lote. Esta fuente es qRT-PCR/ddPCR sobre tejido post mortem y ya fue **rechazada** para esa puerta el 10/11. Este trabajo no la reabre ni la convierte en candidata. Tampoco se equipara tejido post mortem con cultivos i3N.

## Pregunta precisa

¿Los datos fuente depositados reproducen, dentro de tolerancias de redondeo prospectivas, los tres estadísticos publicados en el abstract y las figuras principales?

Objetivos de reproducción, fijados ahora:

- **R1.** Correlación de Spearman entre RNA críptico de UNC13A y RNA de STMN2 truncado: publicado **ρ = 0,58**.
- **R2.** Diferencia por subtipo: el Tipo 2b muestra niveles **significativamente más altos** que Tipos 1 y 2a, en ambas medidas, por Kruskal–Wallis con corrección de Dunn (el artículo declara GraphPad Prism 10.5.0, Mann–Whitney o Kruskal–Wallis con Dunn, significación p < 0,05).
- **R3.** Tamaños de grupo declarados: Tipo 1 n=12, Tipo 2a n=12, Tipo 2b n=11 (total 35).
- **R4.** Concordancia qRT-PCR ↔ ddPCR: el artículo afirma «strong correlations»; se reproducirá el coeficiente si el archivo identifica ambas medidas por caso.

## Predicción refutable

Predicción: R3 se reproduce exactamente, y R1 reproduce ρ = 0,58 con |Δ| ≤ 0,01 tras aplicar el mismo tratamiento de empates que `scipy.stats.spearmanr` (rangos promediados).

Refutación / hallazgo: cualquier discrepancia que no se explique por redondeo, por exclusiones documentadas o por una convención de empates distinta, se **informa como discrepancia**, no se repara ajustando el método hasta cuadrar.

## Método y controles

1. Hash del ZIP y del XLSX antes de leer. Inventario de hojas, dimensiones y cabeceras **antes** de calcular nada.
2. Reconstruir identidad caso→subtipo→medidas sin inventar claves. Si el archivo no permite enlazar una medida a su caso, se declara no enlazable; **no** se emparejan por orden de filas.
3. Calcular R1–R4 con `scipy`/`numpy` (versiones registradas). Spearman con rangos promediados; declarar el tratamiento de empates y de ausentes.
4. **Controles negativos**: permutar etiquetas de subtipo (semilla fija) debe destruir la diferencia de R2; correlacionar UNC13A críptico contra una variable sin relación esperada del propio archivo (p. ej. PMI o RIN, si están) no debe reproducir ρ = 0,58.
5. **Sensibilidad**: recalcular R1 y R2 excluyendo un caso a la vez (leave-one-out) para comprobar que ningún valor único domina el resultado.
6. Explicaciones alternativas a considerar explícitamente: estrategia de normalización, calidad de RNA (RIN), intervalo post mortem, duración de enfermedad y pérdida neuronal semicuantitativa — el propio artículo afirma que las diferencias por subtipo **no** se explican por ellas, lo cual es comprobable si esas columnas están depositadas.

## Criterios de fracaso y parada

- Si el XLSX no contiene valores por caso (solo medias o gráficos), se declara **no reproducible desde el depósito** y se para. No se extraen números de imágenes.
- Si falta la asignación de subtipo por caso, R2 queda **no evaluable**; se informa y no se imputa.
- Si la descarga no se completa íntegra y verificable, se registra el fallo y se para. No se usan números del abstract como sustituto de los datos.
- Un solo ciclo. No se amplía a otros artículos del mismo grupo, ni se contacta a los autores, ni se descargan los otros dos Additional files salvo que R1–R4 lo exijan y se justifique.

## Entregables

`reports/ikegami-source-replay-20261110/`: `REPORT.md` (Evidencia / Interpretación / Limitaciones / Siguiente), `results.json`, tablas derivadas propias, script con pruebas, y procedencia con hashes y versiones. Etiqueta de evidencia: **reproducción descriptiva interna**, no replicación externa ni validación funcional. Sin indicaciones clínicas.
