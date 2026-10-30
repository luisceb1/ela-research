# Cierre acotado de la búsqueda de definiciones — 30/10/2026

## Resultado verificable

**El historial permite identificar el fichero de entrada esperado por el pipeline, pero no recuperar su definición en los materiales revisados.** Dos versiones históricas de `parse_star_junctions.smk` apuntan a `stmn2_and_unc13a.bed` bajo una ruta local del laboratorio. Una configura además la salida `kds_stmn2_and_unc13a`. Esa referencia es evidencia de procedencia del flujo, no el contenido del fichero ni una garantía de que esa ejecución produjera nuestro CSV.

La versión histórica de `paper_figures.Rmd` inspeccionada lee el CSV ya calculado. No se localizó allí el paso que enlaza sus cuatro nombres de unión críptica UNC13A con las coordenadas de S6. Tampoco se resolvió la discrepancia de hebra STMN2. **No se reparan datos ni se asignan nombres por interpretación de los sufijos.**

## Alcance exacto de la revisión

- Se recuperaron metadatos de los 104 commits accesibles de la línea predeterminada del repositorio del artículo y 160 del pipeline, con dos páginas por repositorio y última página incompleta. Son **264 metadatos de commits**, no 264 revisiones integrales de código.
- Se inspeccionaron ocho árboles históricos seleccionados: iniciales, incorporación de datos, eliminación de rutas, modelos históricos y cambios de configuraciones de cultivo. Sus listados no estaban truncados. No se halló el fichero de definición en esos ocho árboles.
- Se leyeron cinco versiones de scripts y se conservaron únicamente localizadores y declaraciones relevantes. Se hicieron cuatro búsquedas dirigidas en las ramas predeterminadas del pipeline y `frattalab/splicing`: una encontró la referencia local y tres no devolvieron resultados.
- No se revisaron todos los árboles, ramas o forks del mundo ni se afirma ausencia universal del fichero. No se abrieron archivos de IDE, modelos clínicos, genotipos o el BED mixto previamente excluido.

Las dos referencias históricas son:

| Commit del pipeline | Blob de reglas | Localizador |
|---|---|---|
|825d75e45c34cecd5e2d7378c48d2642a359825e|d6b5188b3cd5398bca71414ab9e5022a9d74f89a|línea8: fichero stmn2_and_unc13a.bed; línea9: salida kds_stmn2_and_unc13a|
|4c2fbc27d9f90639a9bd356d0aabf065cfcc0cb1|a0712aec0d93d4c68de2cf23ef3a5e6be1e6c207|línea8: mismo fichero de definición|

## Decisión y límite científico

La predicción de una definición pública explícita con siete enlaces unívocos **no se cumple en esta revisión**. Se conserva el estado anterior, sin volver a calcularlo: seis bibliotecas SH-SY5Y enlazadas a ENA; una etiqueta con geometría/hebra concordantes, dos nombres con conflicto de hebra y cuatro alias sin correspondencia explícita.

**El reanálisis externo conjunto de esas siete uniones queda bloqueado por identidad molecular incompleta.** No se concluye que las uniones no existan ni que el resultado publicado sea erróneo. La independencia biológica de las seis bibliotecas tampoco se deduce de sus accesiones.

Este bloque termina aquí. No volver a buscar los mismos nombres en las mismas fuentes sin un nuevo indicio. Tampoco continuar la cadena de auditorías de bins DEXSeq para interpretar eventos que no cubren. La condición para reabrir esta vía es concreta: un fichero de definición original, un paso de generación que documente las equivalencias, o evidencia primaria que resuelva los extremos y la hebra sin suposición. Contactar a los autores requeriría autorización y no se ha hecho.

Para continuar por otra vía segura, el proyecto conserva las observaciones y reproducciones ya ejecutadas como tales; esta fuente no se añade como replicación externa ni se usa para priorizar una diana. La siguiente decisión de investigación debe escoger una pregunta con entradas públicas completas, en lugar de mantener este bloqueo abierto mediante búsquedas equivalentes. Issue14 sigue parcial y no se cierra automáticamente.

## Reproducción y controles

Plan previo: `research/plans/2026-10-30-junction-definition-search.md`. Manifiesto auditable con commits, ocho listados, blobs, localizadores y alcance en `research/references/junction_definition_search_20261030.json`. El script propio `scripts/audit_junction_definition_search.py` verifica paginación, ausencia de duplicados, árboles no truncados y referencias exactas. Sus hashes y versiones quedan en run.json. No se ejecutó código de terceros ni se adquirieron datos biológicos nuevos.

Tres controles negativos ejecutados rechazan: un árbol truncado, la aparición de una nueva definición pendiente de lectura y un fichero de definición presente en un árbol. Esos controles impiden conservar por error el estado bloqueado si aparece evidencia nueva; no validan ciencia ni prueban ausencia global. Se conservan sus resultados.

**183 tests existentes correctos y compileall correcto.** No se añaden tests ni se cuentan las búsquedas como experimentos. Se ejecutaron Python3.12.14 y stdlib:

```bash
python -m scripts.audit_junction_definition_search \
 --manifest research/references/junction_definition_search_20261030.json \
 --out reports/junction-definition-search
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

Mismo PR29, PR28 separado, sin merge, cierre de issue, contacto, gasto, laboratorio o publicación externa.

## Fuentes primarias

- Reglas históricas de autores: https://github.com/frattalab/bedops_parse_star_junctions/blob/825d75e45c34cecd5e2d7378c48d2642a359825e/parse_star_junctions.smk y https://github.com/frattalab/bedops_parse_star_junctions/blob/4c2fbc27d9f90639a9bd356d0aabf065cfcc0cb1/parse_star_junctions.smk .
- Script histórico de figuras: https://github.com/frattalab/unc13a_cryptic_splicing/blob/50395ecf29c3ad37ec9463c20e1fd59c4decc515/paper_figures.Rmd , línea93. Las referencias locales se registran como rutas históricas del autor, no como ficheros accesibles en esta ejecución.
- Auditoría anterior de S6 y enlaces ENA: `reports/shsy5y-junction-map`; sus límites y corrección editorial se conservan, sin una nueva comprobación biológica en este bloque.
