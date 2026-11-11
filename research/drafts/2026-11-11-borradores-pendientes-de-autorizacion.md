# Borradores preparados y NO ejecutados — 11/11/2026

Luis dijo «adelante con todo» el 11/11/2026. He ejecutado la parte técnica. Estas dos piezas **no** las ejecuto por iniciativa propia, y explico por qué en cada una. Quedan aquí redactadas para que decida y, si procede, las envíe o publique **él**.

`AGENTS.md` prohíbe sin autorización expresa: enviar mensajes a investigadores o terceros, y publicar o distribuir hallazgos. Una instrucción general como «adelante con todo» no la trato como esa autorización específica, porque ambas acciones son externas, irreversibles y afectan a personas reales que no están en esta conversación.

---

## 1. Mensaje de colaboración a un laboratorio (BORRADOR, NO ENVIADO)

**Por qué es el mayor multiplicador.** Este proyecto no tiene laboratorio. La matriz de cronología identifica una laguna que solo puede cerrarse con un experimento. Un grupo que ya trabaja en UNC13A podría cerrarla; nosotros no.

**Por qué no lo envío yo.** Notifica a investigadores reales, lo firma una persona, y su reputación —la tuya— es la que queda comprometida. Además debe declarar sin ambigüedad que el análisis lo hizo un agente automatizado bajo tu dirección; omitirlo sería engañoso.

**Destinatario sugerido.** El grupo de Pietro Fratta ya está en contacto contigo por los datos de K26, así que existe un hilo abierto y no sería un correo frío. Alternativa: el grupo de Philip C. Wong (Johns Hopkins), autor de Mallika y Cao, que es quien ha hecho el experimento multidiana posdéficit.

**Asunto propuesto:** Observación sobre cronología de intervención en los trabajos de corrección de UNC13A

> Estimado/a [nombre]:
>
> Le escribo a título personal. Llevo un proyecto de documentación sobre las consecuencias transcriptómicas de la pérdida de función nuclear de TDP-43, trabajando solo con fuentes públicas. El análisis lo realiza un agente automatizado (Claude) bajo mi dirección; todo el material, con su procedencia y sus limitaciones, es público en [URL del repositorio].
>
> Al tabular la cronología de intervención de los trabajos accesibles que corrigen o impiden el exón críptico de UNC13A, aparece un patrón que quizá le resulte de interés. De los seis experimentos específicos de UNC13A que he podido examinar, **ninguno administra la intervención después de documentar un déficit funcional basal**: todos son preventivos por construcción, ya sea por deleción germinal del exón críptico o porque la dosis precede o coincide con la pérdida de TDP-43. En Keuss 2024, por ejemplo, los métodos indican que «ASO treatments were started at the same time as PROTAC treatment».
>
> El contraste con la restauración multidiana es lo que me llamó la atención: Mallika 2026 administra el represor CTR a las seis semanas, «when fine tremors are already apparent», y reporta rescate de fuerza de agarre y supervivencia. Es decir, la ventana posdéficit no parece intrínsecamente intratable en ese modelo, lo que vuelve más pertinente la pregunta de qué haría una corrección aislada de UNC13A administrada después de un déficit medido.
>
> No pretendo que esto sea un hallazgo novedoso para quien conoce el campo de primera mano, y es muy posible que haya datos no publicados que lo respondan. Si la tabulación le resulta útil, se la envío con sus fuentes y localizadores. Y si hay un error en mi lectura de la cronología de algún trabajo, agradecería la corrección más que nada.
>
> Soy consciente de que el tiempo de su grupo es escaso, así que no espero respuesta si no procede.
>
> Un saludo cordial,
> [Luis]

**Antes de enviarlo, revisa:** que la cita de Keuss y la de Mallika son literales (lo son, verificadas 14/14 por `scripts/verify_matrix_quotes.py`); que el repositorio es **privado** ahora mismo, así que la URL no funcionaría para un tercero sin cambiar eso; y que la fila M-a de la matriz sigue sin revisión independiente.

---

## 2. Comentario o preprint (BORRADOR DE ESTRUCTURA, NO PUBLICADO)

**Por qué no lo publico, aunque dijeras «adelante con todo».** Yo mismo recomendé esperar, y mi razón no ha cambiado: la fila M-a está clasificada por un juicio de criterio que no puede evaluar con independencia quien escribió la regla, y las versiones revisadas por pares de Mallika y Cao están en camino. Publicar antes de eso sería prematuro y el vigilante ya avisará sin coste. Publicar es además irreversible: lo que se indexa no se retira.

**Cuándo sí.** Cuando (a) salga la revisión por pares de Mallika o Cao y confirme o corrija la cronología, o (b) alguien ajeno al proyecto revise M-a.

**Estructura propuesta, una vez cumplido lo anterior:**

1. **Observación.** De las intervenciones específicas de UNC13A publicadas y accesibles, ninguna se ha probado tras un déficit funcional medido.
2. **Evidencia.** La matriz de 14 experimentos, con cita literal y localizador de sección por fila, y las dos lecturas del criterio en columnas contables. Material suplementario: `matrix.tsv`, `sources.json`, `CURATION.md` y el verificador de citas.
3. **Contraste informativo.** La restauración multidiana posdéficit sí rescata función y supervivencia en ratón (Mallika), de modo que la laguna no se explica por intratabilidad de la ventana.
4. **Por qué importa.** El desarrollo de ASO contra UNC13A apunta a pacientes diagnosticados, que por definición parten de un déficit establecido. Un diseño preventivo no informa sobre ese escenario.
5. **Lo que la observación NO es.** No es una crítica a esos trabajos, que no declaran probar rescate posdéficit. No es un resultado biológico propio. No es base para ninguna recomendación clínica.
6. **Limitaciones**, sin suavizar: un solo lector automatizado; M-a depende de un juicio de criterio; Mallika y Cao comparten laboratorio y seis autores; el exón críptico murino está en el intrón 1 y el humano en el intrón 20.
7. **Declaración de autoría y método**, explícita sobre el uso de un agente automatizado.

**Vía sugerida:** bioRxiv o Zenodo, ambas sin coste. Un *Correspondence* en revista suele no cobrar, pero no lo he verificado y no asumiría ningún gasto sin avisarte del precio.

---

## Estado de las tres vías del plan estratégico

| Vía | Estado |
|---|---|
| Publicación del hallazgo de cronología | **Borrador de estructura listo. No publicado**, esperando revisión independiente |
| Snaptron/recount3 para desbloquear #37 | **Intentada y bloqueada por TLS.** Pregunta sin responder, no refutada. Ver [informe](../../reports/snaptron-unc13a-feasibility-20261111/REPORT.md) |
| Auditoría de reproducibilidad sostenida | Dos ciclos completados sobre Ikegami. Herramientas reutilizables en `scripts/` |
| Contacto con laboratorio | **Borrador listo. No enviado** |
