# ELA — investigación autónoma (MVP)

**Estado:** primera capa automática de vigilancia pública y control de fuentes. No es todavía un investigador científico autónomo, ni genera resultados clínicos.

## Objetivo
Analizar de forma reproducible datos publicados sobre pérdida de función nuclear de TDP-43, alteraciones de splicing de STMN2, UNC13A y otros transcritos crípticos. Separar observaciones, hipótesis y validación funcional.

## Qué funciona ahora
- GitHub Actions realiza una comprobación diaria de literatura PubMed y un inventario inicial de dos archivos públicos de GEO.
- Las búsquedas registran los PMID vistos y generan informes versionados.
- Los análisis quedan sujetos a las reglas de `AGENTS.md`, `research/PROTOCOL.md`, `research/STATE.md` y `research/BACKLOG.md`.
- Las pruebas unitarias se ejecutan antes de consultar fuentes externas.

## Cómo arrancar
1. Abre **Actions > ELA source watch > Run workflow** y selecciona `main`.
2. Revisa los logs y los ficheros creados en `reports/` y `state/`. Si alguna consulta falla, el workflow lo señalará.
3. El cron funciona diariamente a las **07:17 UTC** (puede retrasarse por GitHub).
4. Si en GitHub Actions se deniega el commit automático, revisa **Settings > Actions > General > Workflow permissions**. Se precisa permiso de escritura para `contents`.
5. Si no aparece el workflow, comprueba que Actions esté habilitado para el repositorio.

## Segunda capa: agente con razonamiento
Este kit **no** invoca por sí mismo un modelo de IA ni decide experimentos nuevos. Para ello, conecta este repositorio a Codex/ChatGPT Work y programa una tarea con este mandato:

> Lee AGENTS.md, research/STATE.md, research/BACKLOG.md y research/PROTOCOL.md. Selecciona la primera tarea segura pendiente, desarrolla y ejecuta código reproducible, incorpora pruebas y registra los resultados en un PR para revisión. Continúa sin preguntar cuando sea posible. No inventes resultados ni publiques conclusiones científicas sin auditoría.

Se recomiendan PR revisables y no conceder a un agente permisos irrestrictos sobre `main`.

## Organización
- `scripts/pubmed_watch.py`: vigilancia bibliográfica (NCBI E-utilities).
- `scripts/geo_inventory.py`: inventario estructural de tablas Iso-Seq `uniqueCounts`.
- `tests/test_watchers.py`: pruebas sin conexión.
- `.github/workflows/daily.yml`: ejecución programada.
- `research/`: protocolo, estado y cola de investigación.
- `reports/` y `state/`: salidas generadas en cada ejecución.

## Límites
No subir datos sanitarios personales. No enviar correos, gastar dinero, publicar hallazgos ni cambiar recomendaciones clínicas automáticamente. La cantidad de réplicas y los metadatos de cada muestra deben comprobarse antes de inferir diferencias biológicas.

**La instalación del workflow no constituye una validación de GSE310723 o GSE315972.**

## Ciclo computacional de 29/10/2026 (PR pendientes)

Resultados revisables: [#3 auditoría](https://github.com/luisceb1/ela-research/pull/3) → [#4 mapeo](https://github.com/luisceb1/ela-research/pull/4) → [#5 sensibilidad](https://github.com/luisceb1/ela-research/pull/5). Los PR están encadenados: revisar/integrar en ese orden y actualizar la base del siguiente a main tras integrar su dependencia. No están fusionados automáticamente.

Desde la rama que contiene los tres análisis:

```bash
python -m unittest discover -s tests -v
python scripts/geo_audit.py
python scripts/map_isoforms.py
python scripts/describe_targets.py
```

Python 3.12, biblioteca estándar. La primera ejecución descarga fuentes públicas; manifiestos fijados por SHA256, caché verificada en `data/cache/` (fuera de git). `--refresh` en la auditoría consulta de nuevo y rechaza cambios de fuente respecto al hash fijado. Consultar `reports/geo-audit/REPORT.md`, `reports/isoforms/REPORT.md` y `reports/descriptive/REPORT.md`, con planes previos, errores y pruebas.

Las 30 pruebas offline y las CI de los tres PR pasan. La auditoría confirma integridad/enlace técnico; el mapeo y los contrastes son exploratorios. La atribución críptica del candidato STMN2, la escala de uniqueCounts y la validación funcional siguen pendientes. No inferir significación de los contrastes de cultivo ni de los rangos de retirada cerebral.

Work tiene una tarea diaria configurada para la mañana (aproximadamente 08:00–09:00 Europe/Madrid), que incluye informe semanal los viernes. Cada ejecución debe volver a comprobar acceso y herramientas, leer también los PR pendientes y registrar avances en GitHub. No hay cómputo continuo entre ejecuciones ni garantía de éxito de una ejecución futura. Estado, próxima tarea y restricciones en `research/STATE.md`/`BACKLOG.md`/`AGENTS.md`.
