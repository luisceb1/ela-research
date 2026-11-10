# Auditoría bibliográfica inicial: dependencia neuronal del papel de UNC13A

**Fecha:** 2026-11-10  
**Estado:** revisión exploratoria de publicaciones primarias; no es un resultado experimental propio  
**Autoría:** síntesis asistida, basada en publicaciones verificadas; **los cuatro agentes del MVP NO se han ejecutado con una API de modelo**  
**Documento de trabajo:** requiere comprobación independiente de datos completos, figuras, tamaños de muestra, versiones y controles antes de concluir causalidad

## Pregunta

¿La corrección aislada del splicing de UNC13A es suficiente para restaurar funciones neuronales relevantes para la ELA, o su contribución depende del circuito neuronal y del resultado funcional considerado?

## Evidencia diferenciada por objetivo

| Fuente | Modelo | Fenómeno descrito | Evidencia que NO aporta |
| --- | --- | --- | --- |
| Ma 2022, PMID 35197626 | Neuronas humanas y tejido de pacientes | La pérdida nuclear de TDP-43 aumenta la inclusión del exón críptico UNC13A y reduce su proteína | Recuperación funcional posdéficit |
| Brown 2022, PMID 35197628 | Neuronas humanas y muestras ALS/FTD | Splicing y pérdida de UNC13A, modulados por alelos de riesgo | Eficacia clínica |
| Keuss 2024, PMID 38979232, preprint; Nature aceptado en 2026 | Neuronas humanas, intervención sobre UNC13A | Corrección de splicing y rescate de transmisión sináptica en modelos experimentales | Demostración de tratamiento después de un déficit basal medido en todas las unidades |
| Guo 2025, PMID 40949955, preprint | Neuronas humanas | Varias dianas de TDP-43; inhibición combinada próxima a normalizar déficit sináptico | Prueba de eficacia en ELA humana; diseño posdéficit establecido |
| Mallika 2026, PMID 42779622, preprint | Ratón con Tdp43 eliminado específicamente en motoneuronas espinales | Impedir solo el exón críptico de Unc13a no mitigó la enfermedad motora; restaurar múltiples dianas mejoró fenotipos motores | Demostrar que UNC13A es irrelevante en motoneuronas humanas o que un único fármaco falla en pacientes |
| Cao 2026, PMID 42779638, preprint | Ratón con Tdp43 eliminado en neuronas del prosencéfalo | Impedir solo el exón críptico de Unc13a preservó memoria; la corrección de varias dianas protegió adicionalmente contra pérdida neuronal | Demostrar eficacia en pacientes con ELA o rescate motor |
| Mehta 2025, PMID 41394711, preprint | Neuronas humanas iPSC y modelo in vivo | Tecnología U7 para modular splicing de STMN2 y UNC13A | Beneficio clínico demostrado |
| Gomberg 2025, PMID 41573891, preprint | Motoneuronas humanas iPSC y ratón modelo STMN2 | Corrección conjunta de transcritos; el componente de función axonal reportado se centra en STMN2 | Equivalencia con recuperación sináptica de UNC13A |

## Hallazgo de la revisión

Los resultados **no constituyen una contradicción simple**. Ensayan resultados y poblaciones distintas: transmisión sináptica, memoria y supervivencia o fenotipo de motoneuronas. Una intervención puede mejorar un endpoint y resultar insuficiente para otro.

Especial atención a la extrapolación murina: según Mallika, el exón críptico de **Unc13a de ratón** evaluado se localiza en un segmento diferente del exón críptico humano de **UNC13A** (intron 1 frente a intron 20). No equiparar mecánicamente las dos intervenciones. En su estudio, un represor dirigido a múltiples dianas se administró mediante AAV-PHP.eB; los efectos no permiten adjudicar por separado la mejora a cada diana. El vector utilizado atraviesa la barrera hematoencefálica de ratón pero no demuestra aplicabilidad humana.

El preprint de Guo sitúa el primer ASO antes del comienzo de reducción de TDP-43: su protocolo comunicado emplea ASO en días 3/10 y shRNA de TDP-43 en día 5. Por tanto, no satisface un criterio fuerte de **intervención posterior a una pérdida funcional basal previamente acreditada**.

## Hipótesis prospectivas, NO resultados

**H1. Dependencia del tipo neuronal.** La contribución del splicing de UNC13A a déficits medibles bajo pérdida de TDP-43 es mayor en ciertos modelos corticales que en motoneuronas espinales.  
- Predicción falsable: al normalizar diseño, nivel de alteración críptica, genotipo y unidad biológica, la magnitud de mejora funcional por corrección de UNC13A cambia con el tipo neuronal.  
- Alternativa: diferencias de desarrollo, intensidad/tiempo de eliminación de TDP-43, tipo de ASO, dosificación o sensibilidad del ensayo.  
- No afirmar originalidad: los trabajos Mallika/Cao ya plantean esta explicación.

**H2. Multidiana y endpoint.** La restauración de UNC13A puede corregir un fenotipo presináptico, pero no ser suficiente para evitar degeneración de motoneuronas cuando otras dianas TDP-43 (por ejemplo STMN2) siguen afectadas.  
- Predicción falsable: un diseño factorial con control, intervención UNC13A, STMN2 y combinación separa efectos principales e interacción en medidas presinápticas, regeneración axonal y supervivencia neuronal.  
- Alternativa: restauración incompleta de cada proteína, efectos de dosis, maduración o tratamiento antes del déficit.  
- La recuperación combinada no demuestra sinergia sin control factorial.

**H3. Sesgo de detección molecular.** Diferencias entre regiones/neuronalidades de abundancia UNC13A y degradación NMD podrían modificar la cuantificación del exón críptico sin reflejar proporcionalmente un efecto funcional.  
- Predicción falsable: uniones objetivo directamente cuantificadas, medidas de proteína y endpoints funcionales guardan relaciones distintas por modelo, una vez se consideran cobertura, degradación y composición celular.  
- Alternativa: limitaciones de alineamiento, lote o diferencias técnicas.

## Experimento computacional admisible a continuación

1. Crear una matriz **a nivel de experimento** (no únicamente PMID) de tipo celular, condición TDP-43, intervención, orden temporal, fuente de unidades independientes, endpoint molecular/funcional y versión de publicación.
2. Solicitar *una revisión humana* de las fuentes y clasificar **prevention / post-deficit recovery / indeterminate**. El lector debe exigir una medición basal del defecto antes de la intervención; llamar «rescue» a un resultado final no basta.
3. Fijar una pregunta de reanálisis solo si aparece **un fichero numérico nuevo y trazable** que cumpla criterios de cobertura, grupos, cronología y unidad experimental; no repetir análisis bloqueados por inercia.
4. Si no existen tales datos, el entregable es una laguna documental con un diseño prospectivo y criterios de falsación, no una estimación del efecto.

## Riesgos de sobreinterpretación

- **Preprints** Mallika/Cao/Guo/Mehta/Gomberg: resultados sujetos a revisión/corrección.
- Los estudios del mismo laboratorio pueden compartir recursos o animales y **no** son necesariamente replicaciones independientes.
- El estudio de Mallika no refuta el rescate sináptico *in vitro* de Keuss: los endpoints difieren.
- La diferencia de expresión de UNC13A entre tejido cortical y médula en GTEx no implica automáticamente diferencia funcional por neurona; existe heterogeneidad celular.
- Ningún trabajo citado demuestra que un paciente con ELA mejore por intervención sobre UNC13A. No recomendar tratamientos con base en esta revisión.

## Fuentes primarias

- Ma: https://pubmed.ncbi.nlm.nih.gov/35197626/
- Brown: https://pubmed.ncbi.nlm.nih.gov/35197628/
- Keuss 2024: https://pubmed.ncbi.nlm.nih.gov/38979232/
- Keuss Nature 2026, aceptación: https://kclpure.kcl.ac.uk/portal/en/publications/unc13a-splice-correction-rescues-synaptic-dysfunction-induced-by-/
- Guo: https://pmc.ncbi.nlm.nih.gov/articles/PMC12424808/
- Mallika: https://pmc.ncbi.nlm.nih.gov/articles/PMC13596259/
- Cao: https://pubmed.ncbi.nlm.nih.gov/42779638/
- Mehta: https://pubmed.ncbi.nlm.nih.gov/41394711/
- Gomberg: https://pubmed.ncbi.nlm.nih.gov/41573891/

## Estado del repositorio

Respetar `research/STATE.md`, `research/BACKLOG.md`, y `research/PROTOCOL.md`. Las issues #37 y #44 continúan bloqueadas sin fuentes nuevas aceptadas; esta revisión no las reabre y no autoriza gastos, comunicaciones, laboratorio ni publicación.
