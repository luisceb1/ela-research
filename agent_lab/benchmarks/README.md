# Benchmark UNC13A v0.1 — 10 de noviembre de 2026

**Alcance exacto:** 20 afirmaciones etiquetadas sobre 8 registros concretos de PubMed. **No representa una revisión exhaustiva de 20 artículos**, ni una validación independiente de las etiquetas. Se conserva la procedencia y no se reproducen resúmenes íntegros ni textos de terceros.

## Registro maestro

`unc13a_v01.json` contiene **13** afirmaciones respaldadas por el resumen, **6** no justificables desde el resumen y **1** directamente contradictoria respecto al resumen publicado.

Semántica:
- `supported`: el **abstract** declara ese resultado en el modelo descrito; no equivale a prueba clínica o replicación independiente.
- `contradicted`: el **abstract** afirma algo incompatible con la proposición.
- `insufficient`: el **abstract** no permite decidirlo; no equivale a falsedad biológica universal.

Los registros de 2024–2025 indicados como preprint no deben contarse como artículos revisados por pares. Las versiones de Keuss (preprint 2024 y artículo aceptado 2026) forman parte de una misma línea de trabajo; solo un contraste de datos y métodos autoriza reconocer evidencia experimental adicional.

## Ejecuciones

Sin acceso a la red ni modelos:

~~~bash
python -m agent_lab.benchmark --validate
python -m unittest discover -s tests -p 'test_agent_benchmark.py' -v
~~~

Consulta real, gratuita, a ocho referencias PubMed: requiere salida HTTPS a NCBI.

~~~bash
python -m agent_lab.benchmark --source-check --output test-results/agent-lab-source-check.json
~~~

El workflow `.github/workflows/agent-lab-pubmed-check.yml` prueba esa consulta en PR. **No envía datos personales ni hace llamadas LLM.** Una consulta operativa exitosa no demuestra que una etiqueta bibliográfica sea correcta. Un fallo de red no es evidencia científica negativa.

Para evaluar decisiones elaboradas por investigadores o modelos, preparar un archivo local con este esquema de 20 entradas:

~~~json
{
  "predictions": [
    {
      "id": "UNC13A-001",
      "decision": "supported",
      "reason": "Explicación del soporte y sus límites"
    }
  ]
}
~~~

El ejemplo muestra solo la primera entrada; para puntuar se exigen las 20, una por caso. Después ejecutar:

~~~bash
python -m agent_lab.benchmark --score ruta/al/archivo-de-predicciones.json
~~~

El informe indica concordancia de etiquetas y, especialmente, **sobrerreivindicaciones**: casos no respaldados que el agente clasificó como demostrados. Es un contrato de evaluación, **no** un agente adjudicador independiente.

## Fuentes primarias consultadas en la curación inicial

- Ma 2022: https://pubmed.ncbi.nlm.nih.gov/35197626/
- Brown 2022: https://pubmed.ncbi.nlm.nih.gov/35197628/
- Keuss 2024 (preprint): https://pubmed.ncbi.nlm.nih.gov/38979232/
- Guo 2025 (preprint): https://pubmed.ncbi.nlm.nih.gov/40949955/
- Gomberg 2025 (preprint): https://pubmed.ncbi.nlm.nih.gov/41573891/
- Baughn 2023: https://pubmed.ncbi.nlm.nih.gov/36927019/
- Klim 2019: https://pubmed.ncbi.nlm.nih.gov/30643292/
- Melamed 2019: https://pubmed.ncbi.nlm.nih.gov/30643298/

Material complementario **no incorporado como una novena réplica**:
- Keuss et al., trabajo aceptado en Nature, octubre 2026:
  https://kclpure.kcl.ac.uk/portal/en/publications/unc13a-splice-correction-rescues-synaptic-dysfunction-induced-by-/

## Dos controles metodológicos especialmente importantes

1. **Intervención preventiva frente a rescate posdéficit.** En la versión pública del trabajo de Guo, los ASO se administran los días 3 y 10; la reducción de TDP-43 empieza el día 5. Un agente no debe presentarlo como rescate tras demostrar previamente una alteración funcional en las mismas unidades.
2. **Pseudorreplicación y doble conteo.** Las células, cultivos y diferenciaciones no son automáticamente unidades independientes; las versiones de un mismo trabajo tampoco son cohortes adicionales.

Fuente: https://pmc.ncbi.nlm.nih.gov/articles/PMC12424808/ .

## Puertas científicas que NO se desbloquean

- Issue #37: exige un archivo/manifiesto Seddighi con recuentos directos y unidades independientes verificables.
- Issue #44: exige valores numéricos originales eEPSC y clave célula→cultivo→diferenciación.
- Sin datos nuevos y controles aprobados, ningún resultado del benchmark autoriza un nuevo contraste, ensayos in vivo o comunicaciones externas.
