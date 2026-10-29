# Auditoría dirigida AGRN / CAMK2B — estado de evidencia 2026-10-29

## Propósito
No seleccionar una diana por cambios de ARN total ni presentar eventos publicados como nuevos. Este registro contrasta antecedentes y delimita preguntas falsables para una posible siguiente fase.

## AGRN
**Publicado:** Seddighi et al., *Science Translational Medicine*, 2024: modelos de exón críptico **in-frame** y péptidos crípticos detectados en modelos de pérdida de TDP-43. PMID 38277467, https://pmc.ncbi.nlm.nih.gov/articles/PMC11325748/ . Revisión de 2026 sobre splicing críptico y ELA, https://pmc.ncbi.nlm.nih.gov/articles/PMC7619245/ : relevancia de la agrina para mantenimiento de la unión neuromuscular; queda por determinar si la variante con exón críptico afecta secreción, localización y función. AGRN también aparece como evento críptico en PBMC tratados con ciclopirox, https://www.nature.com/articles/s41467-025-62004-5 . **No extrapolar** esos modelos a ELA clínica.

**Hipótesis de investigación, no resultado:** inclusión de la secuencia críptica AGRN altera señalización agrina–LRP4/MuSK y agrupamiento de receptores de acetilcolina aunque se mantenga ARN/proteína totales.

**Experimento discriminante:** comparar isoforma canónica y variante críptica a dosis proteicas igualadas, cuantificar secreción extracelular, agrupamiento de AChR y viabilidad/cobertura de NMJ. Rescatar isoforma normal sin reducir indiscriminadamente agrina. Controles de sobreexpresión e identidad de isoforma; replicaciones independientes. Una diferencia de RNA total no confirmaría la hipótesis.

## CAMK2B
**Publicado:** Seddighi et al., https://pmc.ncbi.nlm.nih.gov/articles/PMC11325748/ : isoformas CAMK2B con exones crípticos tanto in-frame como out-of-frame identificadas por long reads; péptidos crípticos in-frame confirmados por proteómica dirigida en neuronas con pérdida TDP-43. Otro trabajo sobre NMD enumera CAMK2B como exón críptico de alta expresión, https://pmc.ncbi.nlm.nih.gov/articles/PMC12262666/ .
**Datos previos internos:** ARN total +23,1 % en GSE126542 y -18,9 % en GSE121569; por sí mismos no prueban inducción de un exón críptico, traducción ni toxicidad, y proceden de sistemas heterogéneos.

**Pregunta útil:** ¿qué variante específica y qué proporción de proteína anómala cambian actividad de quinasa/localización/fenotipos sinápticos? Requiere primero coordenadas/junction reads, identidad de isoforma, NMD y cuantificación proteica; separar isoformas crípticas in-frame de out-of-frame.

## Riesgos de originalidad
- Seddighi ya demostró transcritos y péptidos AGRN/CAMK2B; no 'descubrimiento' de proteínas nuevas.
- La revisión de AGRN formula expresamente una pregunta pendiente, pero **verificar exhaustivamente literatura posterior y trabajos no publicados antes de presentar originalidad**.
- Las cohortes Iso-Seq GEO 310723 y 315972 proceden del mismo proyecto Bolger, no aportan validación externa independiente.

## Decisión provisional
1. AGRN: prioridad **hipótesis funcional de NMJ**, solo después de confirmar material experimental y financiación; no iniciar intervención.
2. CAMK2B: prioridad **auditoría molecular isoforma-específica**; no proponer ensayo funcional antes de clarificar la variante.
3. UNC13A: sigue en paralelo como propuesta más desarrollada de recuperación de red después de déficit verificado.
4. Cerrar reproducción 21 uniones originales antes de ampliar el cribado genómico.

## Bloqueo de integridad
El ZIP original `ELA_06_cruce_sistematico_longread_2026-10-29.zip` es visible en la biblioteca, pero no fue accesible como bytes desde este contexto; no puede afirmarse reproducción exacta de sus scripts ni del filtro que reduce 1910 a 21.
