# Uniones crípticas de UNC13A en corteza motora de TARGET_ALS — plan prospectivo

Fecha: 2026-11-11. Autorización expresa de Luis el 11/11/2026 («abre el ciclo de corteza motora»). Base: main `9dc97c6`, rama `claude/youthful-hypatia-v0ehce`.

**Este plan se fija ANTES de descargar las uniones o calcular nada.** Solo se han inspeccionado metadatos de muestra (2,4 KB) y listados de tamaños.

## Qué cambia respecto a los tres ciclos anteriores

Los tres candidatos previos fueron experimentos de depleción en cultivo, con 6–18 muestras, y fracasaron por cobertura o por ensayo dirigido. Este es distinto en tres aspectos que importan:

| | Ciclos anteriores | Este |
|---|---|---|
| Sistema | cultivo, depleción artificial de TDP-43 | **tejido de paciente**, patología real |
| Tejido | motoneuronas espinales / líneas | **corteza motora** |
| Tamaño | 6–18 muestras | **149 muestras** en un solo tejido |

Y aborda la **hipótesis cortical** que quedó sin probar tres veces: UNC13A se expresa menos en médula que en córtex (Ikegami 2026; panel GTEx de Mallika 2026), de modo que la detección debería ser mejor aquí.

**Esto NO responde la pregunta original de #37**, que pedía un contraste control frente a depleción experimental. Es una **pregunta distinta**, sobre tejido de paciente, y se informa como tal. No se presenta como el desbloqueo de #37 ni se mezcla con sus criterios.

## Diseño declarado por el depósito

`Subject Group` de `TALS_Cortex_Motor_Lateral`, 149 muestras:

| n | Grupo |
|---:|---|
| 84 | ALS Spectrum MND |
| 25 | ALS Spectrum MND, Other Neurological Disorders |
| 23 | **(sin etiqueta)** |
| 13 | Non-Neurological Control |
| 3 | Other Neurological Disorders |
| 1 | Pre-fALS, Other Neurological Disorders |

Reglas fijadas: las 23 sin etiqueta se marcan **desconocido y se excluyen**, no se imputan. El grupo mixto «ALS Spectrum MND, Other Neurological Disorders» se analiza **aparte**, no se fusiona con ELA pura. El contraste primario es **84 ALS Spectrum MND frente a 13 Non-Neurological Control**.

## Datos personales: límite estricto

Los metadatos incluyen sexo, etnia, edad de inicio, edad a la muerte y sitio de inicio motor, de donantes post mortem seudonimizados (identificadores CGND). Igual que con la Table S1 de Ikegami: **solo se informan agregados por grupo; nunca filas individuales con datos clínicos**, y no se versiona el archivo de metadatos. No se busca ni se cruza ninguna identidad.

## Pregunta

En corteza motora, ¿se detectan las uniones crípticas de UNC13A en ELA y no en controles, y a qué fracción respecto a la unión canónica?

## Predicciones refutables, fijadas ahora

- **P1 (cobertura):** al menos una muestra de ELA alcanzará **≥20 lecturas** en una unión críptica. Es la primera vez que el proyecto podría superar ese umbral en RNA-seq de transcriptoma completo.
- **P2 (magnitud):** la **mediana** de fracción críptica en ELA quedará **por debajo de 0,10**, es decir mucho más cerca del RNA-seq de Klim (0,000–0,145) que del amplicón de Ma (0,390–0,690). Razón: el tejido bulk contiene muchas células sin pérdida nuclear de TDP-43, de modo que la señal se diluye.
- **P3 (dirección):** la fracción críptica será mayor en ELA que en controles no neurológicos.

Si P2 se refuta y la fracción en tejido se parece a la del amplicón, eso **reorientaría** el arbitraje de la discrepancia hacia un sesgo del RNA-seq y no del amplicón. Se informaría así, sin rescatar la predicción.

## Método

1. Descargar uniones de `TALS_Cortex_Motor_Lateral` (`RR` ≈36 MB, `MM` ≈158 MB) y sus metadatos. Registrar SHA256 y tamaños. **Presupuesto de descarga: ≤400 MB**; un solo tejido en este ciclo.
2. Aplicar la sonda ya probada `scripts/recount3_junction_probe.py` con las **mismas coordenadas selladas**, sin redefinir. El guardián de convención debe pasar; si no, abortar.
3. Fracción críptica por muestra = `(cr_izq + cr_der) / (cr_izq + cr_der + canónica)`. Es una razón **dentro del mismo gen**, lo que controla parcialmente expresión y composición celular, pero **no** las elimina.
4. Agregados por grupo: n, mediana, rango, número de muestras con alguna lectura y con ≥20.
5. Controles: la unión canónica como control positivo de medición; `assay_shape()` debe confirmar que **no** parece dirigido.
6. Confusores comprobables con `recount_qc`: intervalo post mortem y calidad de RNA si están. Se informan; no se ajusta ningún modelo.

## Límites que no se pueden eludir, declarados de antemano

- **Tejido bulk.** La composición celular confunde cualquier magnitud. La razón dentro del gen mitiga, no resuelve.
- **Solo 13 controles.** Suficiente para una comparación descriptiva, no para una estimación estable.
- **No todo caso de ELA tiene patología de TDP-43 en corteza motora** (SOD1, FUS). Por tanto la **ausencia de lecturas crípticas en una muestra de ELA no es evidencia contra el mecanismo**, y la heterogeneidad es esperable.
- El consorcio ha publicado sobre estos datos y Ma 2022 incluye una tabla suplementaria de variantes de UNC13A y STMN2 en la cohorte NYGC. **No se reclama novedad** sin comprobar antecedentes.
- STMN2 **no** se analiza: el proyecto no tiene sus coordenadas de unión selladas en hg38. No se improvisan.

## Criterios de fracaso y parada

- Uniones objetivo ausentes del `RR` ⇒ rechazo documentado; no ampliar ventana ni aceptar vecinas.
- Presupuesto superado ⇒ parar registrando tamaños.
- Grupos no separables ⇒ parar; no imputar.
- Un solo tejido y un solo ciclo. La comparación **córtex frente a médula** de la misma cohorte es el ciclo siguiente, con su propio plan.
- Sin PSI inferencial, sin p-valores, sin efectos, sin supervivencia ni ninguna variable clínica individual. Sin interpretación clínica.

## Entregables

`reports/target-als-cortex-20261111/`: `REPORT.md` (Evidencia / Interpretación / Limitaciones / Siguiente), `results.json` con agregados por grupo, y procedencia con hashes. Etiqueta de evidencia: **descriptivo exploratorio en tejido post mortem**. Ni rescate, ni causalidad, ni beneficio clínico.
