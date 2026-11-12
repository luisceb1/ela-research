# Viabilidad Snaptron/recount3 para las uniones crípticas de UNC13A — plan prospectivo

Fecha: 2026-11-11. Autorización de Luis el 11/11/2026 («adelante con todo») tras el plan estratégico. Base: main `b438ab9`, rama `claude/youthful-hypatia-v0ehce`.

**Este plan se fija ANTES de cualquier consulta.** No se ha enviado ninguna petición a Snaptron al redactarlo.

## Por qué esta vía y no otra

Las cuatro familias candidatas de #37 (Seddighi, Irwin, Baughn, Humphrey) se rechazaron por **falta de cuentas de uniones accesibles**, no por falta de datos. El piloto propio sobre crudos se cerró con cobertura `[1,0,0]` frente al mínimo de 20, y procesar más crudos exige presupuesto que no existe.

recount3 publica uniones exón-exón **ya cuantificadas** para miles de estudios públicos, consultables por API vía Snaptron sin descargar FASTQ ni alinear. Mallika 2026 usa esa misma infraestructura para su figura de GTEx, lo que confirma que es utilizable. Esto ataca el bloqueo por un flanco distinto a pedir acceso a terceros.

**Esto no reabre las candidatas rechazadas ni relaja ningún criterio.** Se mantienen cobertura ≥20 en la unión objetivo y ≥3 unidades biológicas independientes por condición.

## Uniones objetivo: las ya selladas, sin redefinir

De `reports/unc13a-control-annotation-20261103/complete-assessment.json`, campo `targets_canonical_cryptic_left_cryptic_right`, hg38, chr19, hebra −, **intrónico 0-based semiabierto**:

| Unión | start0 | end0 |
|---|---|---|
| canónica (exón 20–21) | 17641556 | 17642844 |
| críptica izquierda | 17641556 | 17642413 |
| críptica derecha | 17642541 | 17642844 |

Conversión declarada a 1-based inclusivo del intrón, `[start0+1, end0]`, que es la convención de Snaptron:

| Unión | 1-based inclusivo |
|---|---|
| canónica | 17641557–17642844 |
| críptica izquierda | 17641557–17642413 |
| críptica derecha | 17642542–17642844 |

**No se desplazan extremos para forzar coincidencias.** Si ninguna unión de Snaptron coincide exactamente, se informa como no coincidencia y se registra la unión más próxima con su distancia, sin adoptarla como objetivo.

## Pregunta

¿Existe en recount3/Snaptron al menos un estudio público de RNA-seq con (a) cuentas de alguna de las dos uniones crípticas de UNC13A, (b) cobertura ≥20 en esa unión, y (c) metadatos que permitan mapear biblioteca→condición (control frente a depleción de TDP-43)→unidad biológica independiente, con ≥3 unidades por condición?

## Predicción refutable

Predicción: **se encontrarán cuentas de uniones** para la región (la infraestructura resuelve el problema de medición), pero **el mapeo condición→unidad independiente fallará o la cobertura quedará por debajo de 20**, que es el bloqueo recurrente de este proyecto.

Si la predicción se cumple, el resultado es un rechazo documentado con la causa aislada, no un fracaso del ciclo. Si se refuta —hay cuentas suficientes y diseño reconstruible— se redacta prospectivamente **un único contraste** antes de calcular nada, conforme a #37.

## Método

1. Consultar la región del locus UNC13A en la compilación humana de SRA (`srav3h`) y, si procede, GTEx (`gtexv2`) como contexto de tejido, **no** como sustituto del contraste en cultivo.
2. Registrar la respuesta íntegra con SHA256 antes de filtrar. Inventariar cuántas uniones distintas devuelve la región y cuáles coinciden **exactamente** con las tres objetivo.
3. Solo para las que coincidan exactamente: extraer cuentas por muestra y la distribución de cobertura. Declarar cuántas muestras alcanzan ≥20.
4. Para esas muestras, recuperar metadatos y evaluar si permiten mapear condición y unidad biológica. **Lo desconocido se marca como desconocido**; no se infiere condición de títulos de estudio, de sufijos de accesión ni del orden de las muestras.
5. Controles: la unión **canónica** sirve de control positivo de la medición (debe tener cobertura sustancial si la región se expresa); una unión anotada del mismo locus sirve de control de la convención de coordenadas. Ausencia de lecturas por debajo de cobertura es **dato ausente, no un cero biológico**.

## Criterios de fracaso y parada

- Host no accesible o API sin respuesta verificable ⇒ registrar el fallo y parar. No buscar espejos ni rutas alternativas por continuidad.
- Ninguna coincidencia exacta de las uniones crípticas ⇒ rechazo documentado. **No** ampliar la ventana ni aceptar uniones vecinas.
- Cobertura <20 en todas las muestras ⇒ rechazo, igual que el piloto cerrado. No se promedia entre muestras para superar el umbral.
- Metadatos insuficientes para condición o unidad biológica ⇒ rechazo. **No** convertir réplicas técnicas ni muestras del mismo donante en unidades independientes.
- Un solo ciclo. No se descargan crudos, no se alinea nada, no se contacta a nadie, no se asumen costes.

## Entregables

`reports/snaptron-unc13a-feasibility-20261111/`: `REPORT.md` (Evidencia / Interpretación / Limitaciones / Siguiente), `results.json`, consultas y hashes de respuesta, script con pruebas. Etiqueta de evidencia: **auditoría de viabilidad de fuente**, no medición biológica ni contraste. Sin PSI, sin efectos, sin interpretación clínica.
