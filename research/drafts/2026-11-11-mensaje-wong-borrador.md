# Mensaje a Philip C. Wong (Johns Hopkins) — BORRADOR LISTO, NO ENVIADO

Fecha: 2026-11-11, **versión 2**. La versión 1 (mía) queda descartada tras una revisión externa que señaló cuatro problemas. **Los cuatro eran correctos.** Esta versión adopta la redacción propuesta en esa revisión, que es mejor que la mía.

**No lo envío yo.** `AGENTS.md` exige autorización expresa para comunicaciones externas, lo firmas tú y es tu reputación la que queda comprometida.

## Qué estaba mal en mi versión 1

| Mi texto | Problema |
|---|---|
| «no donor pairing available in the metadata» | **Desactualizado.** La rama de la PR #57 recuperó un mapa de donante y estableció **45 pares**, con análisis exploratorios ya hechos. Enviar eso habría sido afirmar algo falso sobre nuestro propio trabajo |
| «with sequencing depth matched between tissues» | **No es un control.** Coincidir en la mediana no controla la profundidad. Y mi cifra de 21× era una **razón de medianas**, no una normalización por biblioteca. Recalculado: **22,3×**. Corregido en el informe |
| «the limitation appears to be gene-specific rather than general» | **Sobreafirmación.** Dos genes que se comportan distinto muestran que difieren, no que la limitación sea «específica del gen» como propiedad general |
| «they are preventive by construction» | **No se sigue.** No documentar un déficit antes de tratar no demuestra que la intervención fuese preventiva. Para las deleciones germinales sí; para la fila K-c, donde el knockdown llevaba 5 días establecido, **no**. Lo correcto es «no pude establecer que el tratamiento empezara tras un déficit documentado» |

Y la decisión de fondo que también comparto: **fuera el apartado tisular**. Un primer contacto frío con dos hallazgos y una salvedad metodológica pide demasiado. Una pregunta concreta tiene más probabilidad de respuesta y menos superficie de error.

## Destinatario

**Philip C. Wong**, Johns Hopkins University School of Medicine. Autor corresponsal de Mallika 2026 y Cao 2026. **La dirección exacta hay que tomarla del artículo**, no de este archivo.

Correo **frío**: presentación desde cero y breve.

## Asunto propuesto

`Question on treatment timing in the AAV-PHP.eB-CTR experiment (Mallika et al.)`

---

> Dear Professor Wong,
>
> I am a lawyer in Spain conducting a small, AI-assisted review of public studies on TDP-43 loss of function, with a particular interest in UNC13A. Our source matrix, methods and corrections are available here:
> https://github.com/luisceb1/ela-research
>
> I am writing with a question about the timing of treatment in Mallika et al.'s AAV-PHP.eB-CTR experiment.
>
> In the six UNC13A-specific experiments included in our bounded review, I could not establish that treatment began after a functional deficit had been documented under our operational criterion. Your multi-target CTR experiment raised an interesting comparison because dosing began at six weeks, when fine tremors were already apparent.
>
> Was grip strength assessed before dosing in the animals subsequently receiving CTR, or was their symptomatic status established through tremor onset and the model's age-dependent characterisation?
>
> Our original classification required a deficit in the same functional endpoint to be documented in the same animals before treatment. I recognise that this criterion may be too restrictive for this model. We therefore record both readings and do not treat the classification as settled.
>
> This is a request to clarify our interpretation of the chronology. I would welcome any correction, including an UNC13A-specific experiment that our review may have missed.
>
> Thank you for your time.
>
> Kind regards,
> Luis Cebrián Fraile

---

## Antes de enviarlo, comprueba

- **La dirección exacta** tómala del artículo de Mallika o Cao, no de aquí.
- **Tu nombre completo** figura en la firma. Si prefieres no exponerlo, cámbialo.
- **El enlace funciona**: el repositorio es público. Verá también los informes donde se corrigen errores propios, incluidas cuatro correcciones de hoy. Es deliberado.
- La cita «when fine tremors are already apparent» es **literal**, verificada por `scripts/verify_matrix_quotes.py`.

## Lo que el mensaje hace y no hace

**Hace:** una pregunta factual concreta y respondible, reconoce que nuestro criterio puede ser demasiado restrictivo para ese modelo, declara el uso de IA, e invita a corregirnos — incluido señalarnos un experimento que se nos haya pasado.

**No hace:** no pide datos ni colaboración, no reclama novedad, no afirma que nadie se haya equivocado, no incluye el apartado tisular, no menciona #37 ni #44, y **no afirma que los seis experimentos sean preventivos** — solo que no pudimos establecer lo contrario bajo nuestro criterio.
