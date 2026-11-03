# Rescate funcional UNC13A: auditoría y decisión — 03/11/2026

## Decisión

Seleccionamos **Keuss aceptado, Fig. 4d: amplitud eEPSC en motoneuronas espinales**, como único objetivo de reproducción condicional. No hay archivo numérico original con identificadores de diferenciación verificado: **NO-GO para estimar el efecto**. El resultado de esta entrega es una auditoría documental y un plan ejecutable de entrada de datos, no una reproducción funcional ni evidencia de reversión posdéficit.

Esta línea está autorizada por el encargo de Luis del 03/11. Parte de main `9076802fa78bfd1e4cdc97a3b92dd24a06d054c4`, con PR #36 fusionada y #38 abierta. No depende de #37/AD Workbench. No altera sus archivos, umbrales, muestras o decisiones. Las issues #16 y #18 siguen como antecedentes; no se abre una segunda supuesta invención del protocolo posdéficit.

## Qué añade respecto al trabajo anterior

Se leyeron AGENTS.md, STATE.md, BACKLOG.md y PROTOCOL.md; inventario completo de issues/PRs y árbol de main. Se revisaron las auditorías de las PR #7/#8/#30/#35, `reports/accepted-keuss`, `reports/functional-source-access-20261101`, `reports/originality-audit`, y el protocolo UNC13A v0.4. **La temporalidad preventiva y el antecedente multidiana ya estaban documentados**: confirmarlos no es un descubrimiento nuevo. Tampoco el preprint negativo de septiembre es nuevo para el proyecto: ya consta como `motor2026` en la auditoría de originalidad.

El incremento concreto es: matriz por experimento con unidades y versiones; selección de un único ensayo de tres brazos en motoneuronas; contrato informático de aceptación que impide agrupar células sin diferenciación; inventario actualizado de bloqueos y protocolo de reproducción separado de una futura prueba posdéficit. Se explicita que la combinación del **preprint Guo** incluye UNC13A, KALRN, RAP1GAP y SYT7; no STMN2. No se atribuye esa lista a métodos finales todavía inaccesibles.

## A. Evidencia publicada

Keuss aceptado (K26; páginas de la copia aportada por Luis) ofrece validación genética y farmacológica en neuronas humanas. La deleción constitutiva del exón críptico produce una recuperación de frecuencia mEPSC que los autores describen como 80%; queda una reducción aproximada del 10% de amplitud. No hemos reconstruido el denominador de ese 80%. Las ASO mejoran liberación espontánea; las corrientes evocadas se recuperan parcialmente en neuronas corticales y espinales. La densidad de sinapsis y el número de sinapsis activas no se recuperan, aunque mejora la probabilidad de liberación de las restantes (pp.7–11). Por tanto, suficiencia para algunos componentes presinápticos no equivale a reparación completa de la neurona.

Cronología K26 comprobada directamente: mEPSC y autapsis corticales, primera dosis DIV14; motoneuronas, corrector y gapmer TDP-43 en paralelo desde DIV45; MEA, ASO DIV14 y KD DIV14 o DIV33. En este último brazo la intervención precede al KD en 19 días. Un cultivo maduro antes de dañarlo no es un cultivo tratado después de demostrar daño. Ratón reportero humanizado: intervención concurrente y desenlace de splicing, sin ensayo motor que demuestre eficacia.

Guo: el artículo final G26 confirma rescate individual parcial y combinado casi completo (resumen). Los detalles accesibles pertenecen al preprint G25: combinación UNC13A/KALRN/RAP1GAP/SYT7; primera ASO d20 antes del shRNA d21; lectura MEA d28. Leyendas n=3–8 individual y n=8 combinado; métodos declaran réplicas biológicas, pero falta el mapa pozo/diferenciación. No acusamos pseudorreplicación sin ese mapa. Las lecturas moleculares se hacen en otro calendario, no son parejas verificadas de las mediciones MEA. No combinamos estos resultados con K26 en un metaanálisis.

## B. Qué ha producido nuestro proyecto

No hemos corregido UNC13A en neuronas ni medido recuperación funcional propia. RiMOD/NYGC son observaciones de splicing; STMN2 TPM→PPAU es una reproducción molecular descriptiva; el piloto local UNC13A terminó por cobertura insuficiente. Esta auditoría no cambia esos niveles de evidencia. El código nuevo valida una entrada y produce una decisión reproducible; sus pruebas artificiales solo comprueban controles informáticos.

## C. Qué queda por investigar

La pregunta estrecha sigue siendo si **iniciar** el corrector de UNC13A después de comprobar un déficit funcional permite recuperación absoluta frente al estado deficitario y diferencial frente al control. La presente reproducción propuesta no responde a esa pregunta: Fig.4d inicia corrector y perturbación conjuntamente. Puede comprobar la magnitud y robustez de una intervención concurrente en un modelo relevante, antes de invertir en una extensión temporal. El diseño conceptual posdéficit existente se conserva en `research/UNC13A_POST_DEFICIT_PROTOCOL_v0.4.md`; no se presenta otra versión como avance biológico.

## Límites y traslación

- TDP-43 degradado mediante HaloPROTAC, reducido por shRNA o por gapmer no reproduce necesariamente su pérdida nuclear progresiva, agregación y toxicidad citoplasmática en ELA. Intensidad, duración y maduración cambian el fenotipo.
- Autapsis aíslan componentes de transmisión; MEA integra actividad de red; frecuencia mEPSC también depende del número de sinapsis. Ninguno sustituye supervivencia, reinervación muscular o función motora.
- Tres diferenciaciones y un contexto genético limitado permiten un contraste condicionado al modelo; muchas células no aumentan la diversidad de donantes. Cultivos, coverslips y lotes deben identificarse antes de fijar la jerarquía definitiva.
- Analizar solo sinapsis activas o células registrables selecciona supervivientes funcionales. Deben recuperarse exclusiones y pérdidas, además de valores exitosos. Un intercepto de lote no resuelve toda dependencia entre células del mismo cultivo.
- Restauración molecular, reparto del ASO en SNC, seguridad de dosis repetidas, efectos fuera de diana, reserva neuronal y heterogeneidad de enfermedad son barreras distintas. No se ha demostrado aquí eficacia clínica ni que añadir STMN2 restaure las sinapsis perdidas.

## Recomendación única

Mantener **un solo objetivo computacional: reproducción jerárquica de Fig.4d K26**, condicionado al archivo original de células/cultivos y sus metadatos. No reabrir búsquedas equivalentes cerradas, digitalizar la figura para fabricar réplicas, cambiar automáticamente a otro ensayo o iniciar laboratorio. El disparador de continuación será un enlace concreto nuevo a datos fuente o material proporcionado con autorización. Sin ello, esta línea queda preparada y bloqueada por datos; AD Workbench puede avanzar por separado.

Véanse `evidence_matrix.tsv`, `DATA_AVAILABILITY.md`, `ORIGINALITY.md`, `REPRODUCTION_PLAN.md` y `sources.json`. La recomendación es una reproducción incremental, **no una contribución original ya acreditada**.

## Referencias

- Keuss, M. J., et al. (2026, aceptado 6 octubre). *UNC13A splice correction rescues synaptic dysfunction induced by TDP-43 loss*. Nature. [Registro KCL](https://kclpure.kcl.ac.uk/portal/en/publications/unc13a-splice-correction-rescues-synaptic-dysfunction-induced-by-/). DOI final no verificado. Manuscrito aportado: 63 pp.; identidad y localizadores en sources.json.
- Keuss, M. J., et al. (2024, 24 junio). *Loss of TDP-43 induces synaptic dysfunction that is rescued by UNC13A splice-switching ASOs*. bioRxiv. https://doi.org/10.1101/2024.06.20.599684. Versión anterior, no replicación independiente.
- Guo, C., et al. (2025, 2 septiembre). *Cryptic splicing in synaptic and membrane excitability genes links TDP-43 loss to neuronal dysfunction*. bioRxiv, v1. https://doi.org/10.1101/2025.08.28.672801.
- Guo, C., et al. (2026, 3 junio). Mismo título. *Science Translational Medicine, 18*(852), eaeb8517. https://doi.org/10.1126/scitranslmed.aeb8517.
- Peethambaran Mallika, A., et al. (2026, 18 septiembre). *Restoring multiple TDP-43 cryptic targets, but not solely Unc13a, rescues motor neuron disease*. bioRxiv, v1. https://doi.org/10.64898/2026.09.11.751082. Preprint; lectura parcial primaria indexada.
- Joseph, B. J., et al. (2025). *TDP-43-dependent mis-splicing of KCNQ2 triggers intrinsic neuronal hyperexcitability in ALS/FTD*. Nature Neuroscience, 28, 2476–2492. https://doi.org/10.1038/s41593-025-02096-w. Consulta de resumen/leyendas PubMed, no reproducción.

Scite se usó para metadatos y rastreo; `contentDenied` no cuenta como lectura. Ejemplo de contexto de citación recuperado de Watanabe et al. (2025, DOI 10.1038/s44318-025-00506-0): “UNC13A is essential for the formation and maintenance of synaptic vesicles and neurotransmitter release at synapses”. Es contexto mecanístico de introducción, no confirmación independiente del rescate de Keuss. Las búsquedas de avisos editoriales no resolvieron `editorialNotices`; no certificamos ausencia de correcciones/retractaciones.
