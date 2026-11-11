# Mensaje a Philip C. Wong (Johns Hopkins) — BORRADOR, NO ENVIADO

Fecha: 2026-11-11. Reescritura del borrador anterior con las tres correcciones acordadas, dirigido a **Wong** en vez de a Fratta.

**No lo envío yo.** Notifica a un investigador real, lo firmas tú y es tu reputación la que queda comprometida. `AGENTS.md` exige autorización expresa para comunicaciones externas.

## Por qué Wong y no Fratta

Wong es el autor corresponsal de Mallika 2026 y Cao 2026. Es **quien hizo el experimento multidiana posdéficit**, es decir el contraste que hace interesante la observación. El mensaje **cita su trabajo como el caso que abre la pregunta**, no lo cuestiona.

Fratta, en cambio, es autor de Keuss 2024, el trabajo cuya cronología se señala. Habría sido decirle que su propio experimento es preventivo. Legítimo, pero innecesariamente incómodo cuando existe un destinatario mejor.

Es un correo **frío**: hay que presentarse desde cero y ser breve.

## Las tres correcciones aplicadas

1. **Eliminada** la advertencia sobre el repositorio privado: ya es público, así que el enlace funciona.
2. **Añadida** la salvedad sobre la fila M-a, que es la pieza más débil del argumento y sostiene precisamente el contraste con Mallika.
3. **Añadido** el hallazgo tisular, de utilidad inmediata para cualquiera que diseñe un estudio de UNC13A.

## Dirección

Correspondencia de Mallika 2026 y Cao 2026: Philip C. Wong, Johns Hopkins University School of Medicine. **La dirección exacta hay que tomarla del artículo**, no de aquí.

## Asunto propuesto

`Intervention timing in UNC13A cryptic-exon studies, and a tissue-coverage observation`

---

> Dear Professor Wong,
>
> I am writing in a personal capacity. I am a lawyer in Spain, and I run a small independent documentation project on the transcriptomic consequences of TDP-43 nuclear loss of function, using public sources only. The analysis is carried out by an automated agent (Claude) under my direction; the full material, including its provenance, its limitations and the corrections made to my own earlier claims, is public at https://github.com/luisceb1/ela-research
>
> Two observations from it may be of interest to your group. I am not claiming either is novel to someone working in the field directly.
>
> **1. Intervention timing.** Tabulating the accessible experiments that correct or prevent UNC13A cryptic-exon inclusion, I find that of the six UNC13A-specific experiments I could examine, none administers the intervention after a baseline functional deficit has been documented in the same system and endpoint. They are preventive by construction, either through germline deletion of the cryptic exon or because dosing precedes or coincides with TDP-43 loss. In Keuss 2024, for example, the methods state that "ASO treatments were started at the same time as PROTAC treatment".
>
> What drew my attention was the contrast with your multi-target work. Mallika et al. 2026 delivers AAV-PHP.eB-CTR at six weeks, "when fine tremors are already apparent", and reports maintained grip strength and survival extended from roughly 47 to at least 110 weeks. The post-deficit window therefore does not look intrinsically intractable in that model, which makes it more pointed to ask what an isolated UNC13A correction would do when given after a measured deficit.
>
> **An important caveat on my own classification.** My prespecified rule required the deficit of the same endpoint to be measured in the same animals before dosing, and explicitly excluded a parallel untreated arm as baseline evidence. Under that strict reading your CTR arm does not qualify either, since what is documented at dosing age are fine tremors rather than the measured endpoint, and the grip-strength deficit comes from the GFP arm. I record both readings rather than choosing one, and this particular row has had no independent review. It is the weakest part of the argument and I would rather flag it than let it pass.
>
> **2. A tissue-coverage observation that may be practically useful.** Using recount3 junction counts from the TARGET_ALS cohort, with sequencing depth matched between tissues (median 44.4M exon-assigned reads in both), UNC13A canonical junction coverage is about 21 times lower in cervical spinal cord than in motor cortex: 0.11 against 2.30 reads per million in ALS-spectrum samples. In that cohort no sample reaches 20 reads on a cryptic UNC13A junction, the maximum on any single junction being four.
>
> The practical implication, if it holds, is that standard whole-transcriptome RNA-seq of spinal cord is unlikely to detect UNC13A cryptic junctions at useful precision, which may be part of why the defining studies used targeted assays. STMN2 behaves in the opposite direction in the same data, with cryptic junctions readily detectable in cord, so the limitation appears to be gene-specific rather than general.
>
> I should be clear about what this is not: bulk post-mortem tissue with unmeasured cell composition, no donor pairing available in the metadata, and no inference attempted. It is a coverage observation, not a biological result.
>
> If the timing table would be useful, I am glad to send it with its sources and locators. And if I have misread the chronology of any study, including yours, I would value the correction more than anything else.
>
> I am aware your group's time is scarce and expect no reply if none is warranted.
>
> With kind regards,
> Luis Cebrián Fraile

---

## Antes de enviarlo, comprueba

- **Las dos citas son literales**, verificadas 14/14 por `scripts/verify_matrix_quotes.py`: la de Keuss y la de Mallika.
- **Las cifras del punto 2** salen de `reports/target-als-cervical-20261111/tissue_comparison.tsv`.
- **El enlace del repositorio funciona** (es público desde hoy). Verás también en él los informes donde se corrigen errores propios, incluidas tres correcciones de hoy a mis propias sobreafirmaciones. Eso es deliberado: un proyecto que registra sus fallos es más creíble que uno que solo muestra aciertos.
- **La dirección exacta** tómala del artículo, no de este archivo.
- **Tu nombre completo** figura en la firma. Si prefieres no exponerlo, cámbialo antes de enviar.

## Lo que el mensaje deliberadamente NO hace

No pide datos. No propone colaboración formal. No reclama novedad. No sugiere que nadie haya cometido un error. No menciona #37 ni #44 ni pide acceso a nada. Es una observación ofrecida, con su parte más débil señalada por mí mismo, y una invitación a corregirme.
