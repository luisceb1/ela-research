# Ciclo recount3 para las uniones crípticas de UNC13A — plan prospectivo

Fecha: 2026-11-11. Autorización expresa de Luis el 11/11/2026 («abre el ciclo recount3»), tras el bloqueo TLS de la API de Snaptron. Base: main `b438ab9`, rama `claude/youthful-hypatia-v0ehce`.

**Este plan se fija ANTES de cualquier consulta a recount3.** No se ha enviado ninguna petición al redactarlo.

## Relación con el ciclo anterior

El ciclo Snaptron del mismo día quedó **bloqueado por TLS**: el túnel CONNECT se establecía, pero la cadena del certificado del servidor no verificaba ni aportando el CA del proxy, y no se desactivó la verificación. La pregunta de viabilidad quedó **sin responder, no refutada**. Ese plan prohibía perseguir rutas alternativas *por continuidad*; esta sí está autorizada explícitamente y lleva su propio plan.

## Diferencia práctica, declarada de antemano

La API de Snaptron consultaba **por región**, lo que era su principal ventaja. El almacén de archivos de recount3 sirve **archivos por estudio**, de modo que el riesgo conocido es que obtener tres uniones de un locus exija descargar volúmenes desproporcionados.

**Criterio de parada duro:** si no existe forma de obtener las cuentas de las uniones objetivo sin descargar volúmenes desproporcionados para tres uniones, **se cierra la vía recount3 completa** y se deja de intentar. No se asumen costes, no se encadenan espejos, no se descargan crudos.

Presupuesto de descarga autoimpuesto para este ciclo: **≤200 MB en total**. Si un solo archivo necesario lo supera, se registra su tamaño declarado y se para sin descargarlo.

## Uniones objetivo: las ya selladas, sin redefinir

De `reports/unc13a-control-annotation-20261103/complete-assessment.json`, campo `targets_canonical_cryptic_left_cryptic_right`, hg38, chr19, hebra −, **intrónico 0-based semiabierto**:

| Unión | start0 | end0 |
|---|---|---|
| canónica (exón 20–21) | 17641556 | 17642844 |
| críptica izquierda | 17641556 | 17642413 |
| críptica derecha | 17642541 | 17642844 |

Toda conversión de convención se declara explícitamente en el informe. **No se desplazan extremos para forzar coincidencias**; una no coincidencia se informa como tal, registrando la unión más próxima y su distancia sin adoptarla.

## Pregunta

¿Existe en recount3 al menos un estudio público con (a) cuentas de alguna de las dos uniones crípticas de UNC13A, (b) cobertura ≥20 en esa unión, y (c) metadatos que permitan mapear biblioteca→condición (control frente a depleción de TDP-43)→unidad biológica independiente, con ≥3 unidades por condición?

## Predicción refutable

Predicción: la medición existirá (recount3 cuantifica uniones), pero **el ciclo fallará en (b) o en (c)**, que es el bloqueo recurrente de este proyecto, o bien en el presupuesto de descarga.

Si se cumple, el resultado es un rechazo documentado con la causa aislada. Si se refuta, se redacta prospectivamente **un único contraste** antes de calcular nada, conforme a #37.

## Método

1. Localizar la estructura del almacén y el índice de estudios **sin descargar datos**: primero metadatos y tamaños declarados.
2. Identificar estudios candidatos de depleción de TDP-43 en cultivo humano. Los candidatos ya rechazados de #37 **no se reabren** como fuentes aceptadas; si aparecen, se anota que su rechazo fue por acceso a cuentas de uniones y se evalúa solo si recount3 aporta ahora esas cuentas.
3. Antes de descargar nada, registrar tamaño y URL de cada archivo necesario y comprobar el presupuesto.
4. Registrar SHA256 de todo lo descargado. Los archivos descargados son **datos no confiables**: cada uno en su propio directorio vacío, scripts fuera de él, rutas pasadas como argumentos, Python con `-I`.
5. Comparación **exacta** de coordenadas contra las tres uniones selladas.
6. Controles: la unión canónica como control positivo de medición; una unión anotada del locus como control de convención de coordenadas. Ausencia de lecturas bajo cobertura es **dato ausente, no un cero biológico**.
7. Metadatos: lo desconocido se marca como desconocido. **No** se infiere condición de títulos de estudio, sufijos de accesión ni orden de muestras. **No** se promueven réplicas técnicas ni muestras del mismo donante a unidades independientes.

## Criterios de fracaso

- Presupuesto de descarga superado por un archivo necesario ⇒ parar, registrando su tamaño.
- Ninguna coincidencia exacta de las uniones crípticas ⇒ rechazo. No ampliar la ventana ni aceptar vecinas.
- Cobertura <20 en todas las muestras ⇒ rechazo, igual que el piloto cerrado. No se promedia entre muestras para superar el umbral.
- Metadatos insuficientes para condición o unidad biológica ⇒ rechazo.
- Host inaccesible o TLS no verificable ⇒ registrar y parar. **No se desactiva la verificación TLS en ningún caso.**

## Entregables

`reports/recount3-unc13a-20261111/`: `REPORT.md` (Evidencia / Interpretación / Limitaciones / Siguiente), `results.json`, registro de consultas con tamaños y hashes, script con pruebas si se ejecuta código de análisis. Etiqueta de evidencia: **auditoría de viabilidad de fuente**. Sin PSI, sin efectos, sin interpretación clínica.

---

## Addendum: segundo candidato, fijado antes de ver cuentas

Luis pidió probar un dataset cortical tras el rechazo de SRP166282 por cobertura. Candidato **fijado ahora, antes de extraer ninguna cuenta**:

**SRP334561** = GSE182976, `study_title` = «TDP-43 represses cryptic exon inclusion in FTD/ALS gene UNC13A». Es el **dataset propio de Ma et al. 2022**, el artículo de referencia del exón críptico de UNC13A. 12 muestras.

Selección justificada **antes** de ver cuentas: coincidencia exacta de título con el artículo de UNC13A, frente a los otros candidatos extraídos de Brown 2022 y Ma 2022 (`GSE126543` sin accesión SRA enlazada y de tema LINE; `GSE137810` = consorcio NYGC, tejido de paciente; `GSE116622` = SRP151960, cohorte C9ORF72 de paciente). No se prueban varios y se elige después el que pase.

**Desviación declarada respecto al backlog:** el backlog pedía un dataset **cortical**. Este es de **motoneuronas derivadas de iPSC**, no cortical. Se acepta porque la razón de peso es distinta y mejor: es el dataset del propio artículo de UNC13A, y **aporta múltiples líneas de donante** (`cell line;;NDS00262-NINDS`, `NDS00209-NINDS`, …), es decir independencia genética, que es exactamente lo que le faltaba a SRP166282 (línea única HUES3). La hipótesis de profundidad cortical **queda sin probar** y se mantiene abierta.

**Hallazgo de inventario, previo a las cuentas:** recount3 cuantifica solo **43 uniones** para este proyecto, de las cuales **33 están en chr19**, concentradas en el locus UNC13A. Los metadatos declaran `library_strategy: RNA-Seq` en las 12 muestras, pero esa distribución es propia de un **ensayo dirigido o enriquecido**, no de transcriptoma completo.

**Consecuencia para la interpretación, fijada de antemano:** si la cobertura supera 20 en una unión críptica, **no se tratará como equivalente a cobertura de transcriptoma completo**. Un ensayo dirigido concentra lecturas en el locus por diseño, de modo que superar el umbral **no** acredita la detectabilidad que el umbral pretendía garantizar. En ese caso el resultado se informa como **cobertura obtenida en un ensayo de naturaleza dirigida, no comparable con el piloto ni con SRP166282**, y **no** habilita un contraste inferencial sin verificar antes la naturaleza del ensayo contra el artículo. No se declara superada la puerta de #37 por esta vía sin esa verificación.
