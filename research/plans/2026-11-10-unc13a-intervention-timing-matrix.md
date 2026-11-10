# Matriz de cronología de intervenciones UNC13A — plan prospectivo, 2026-11-10

Extensión documental autorizada por Luis el 10/11/2026 ("continúa con lo demás") tras confirmar que siguen sin llegar los datos K26 (#44) ni el acceso AD Workbench (#37). No reabre #37/#44 ni las reproducciones cerradas. Sin contactos, gastos, datos personales, laboratorio ni publicación externa.

Base: main `3916b77ec0546e9d327e6d54e4dacd90d1a51ce4`. Este plan se fija y se confirma **antes** de recuperar los textos completos.

## Pregunta

En los experimentos primarios accesibles que corrigen (o impiden) el exón críptico de UNC13A/Unc13a bajo pérdida de TDP-43, ¿alguno inicia la intervención **después** de documentar, en el mismo sistema y endpoint, un déficit funcional basal?

## Fuentes fijadas antes de leer (sin ampliar tras ver resultados)

Las fuentes de intervención listadas en el informe de la PR #51 (`reports/agent-lab/2026-11-10-unc13a-context/REPORT.md`), únicas evaluadas:

| ID | Referencia | Motivo |
|---|---|---|
| S1 | Keuss 2024, PMID 38979232 (preprint; versión Nature 2026 aceptada) | Corrección de splicing UNC13A y transmisión sináptica |
| S2 | Guo 2025, PMID 40949955 / PMC12424808 (preprint) | ASO multidiana, déficit sináptico |
| S3 | Mallika 2026, PMID 42779622 / PMC13596259 (preprint) | Ratón, motoneuronas, Unc13a frente a multidiana |
| S4 | Cao 2026, PMID 42779638 (preprint) | Ratón, prosencéfalo, Unc13a y memoria |
| S5 | Mehta 2025, PMID 41394711 (preprint) | U7 STMN2/UNC13A |
| S6 | Gomberg 2025, PMID 41573891 (preprint) | Corrección conjunta STMN2/UNC13A |

Ma 2022 y Brown 2022 son observacionales (sin intervención): se registran como contexto, no se clasifican.

## Unidad y variables

Unidad de la matriz = **experimento** (sistema × intervención × endpoint), no PMID. Variables: sistema/tipo celular, modo de pérdida de TDP-43, intervención, día de inicio de la pérdida de TDP-43, día de primera dosis, ¿déficit funcional medido antes de la primera dosis? (sí/no/no informado), endpoint, unidad biológica declarada (diferenciaciones/animales/células), versión y localizador textual de cada dato.

## Reglas de clasificación (fijadas)

- **prevention**: primera dosis antes o a la vez que la pérdida de TDP-43, o antes de que el déficit del endpoint se haya medido.
- **post-deficit recovery**: el déficit del mismo endpoint se mide en el mismo sistema/cohorte antes de la primera dosis, y la intervención empieza después. Un control no tratado en paralelo que muestre déficit al final **no basta**.
- **indeterminate**: cronología o medición basal no recuperable del texto accesible. Nunca se completa por suposición.
- Endpoint molecular (splicing/proteína) y funcional se clasifican por separado. Corrección de splicing ≠ rescate funcional.

## Predicción refutable y criterios de fracaso

Predicción: **ningún** experimento accesible de intervención sobre UNC13A cumple *post-deficit recovery* para un endpoint funcional. Se refuta si al menos un experimento lo cumple con localizador textual verificable.

Fracaso/insuficiencia: si menos de 4 de las 6 fuentes tienen métodos accesibles con cronología, la matriz se declara **insuficiente**, sin conclusión general. Solo abstract ⇒ toda fila de esa fuente queda *indeterminate*.

## Método

Recuperar metadatos y texto completo vía Europe PMC REST (host permitido el 10/11/2026), guardar originales fuera del repositorio con SHA256 registrado y localizar frases de métodos por búsqueda de términos; transcribir con cita literal corta. Sin ejecutar modelos ni estimar efectos. Clasificación por un único lector (agente): requiere **segunda revisión humana** antes de considerarla curada.

## Entregables

`reports/unc13a-intervention-timing-20261110/`: `matrix.tsv`, `sources.json` (hashes, versiones, URL, fecha), script de extracción con prueba y `REPORT.md` (Evidencia / Interpretación / Limitaciones / Siguiente experimento). Parar tras esta matriz.
