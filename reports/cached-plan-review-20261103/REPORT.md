# Revisión offline parcial del descriptor — 03/11/2026

## Evidencia y pregunta

Se verificaron acceso al repositorio y Python3.12.14 real. Main consultado:a16b6d9c6e79783e0559bfa56b1676cf506be2d4. Única PR abierta:#36, cabeza49f37a0cbda83b8046cf40492f566bc27906171f. Se leyeron AGENTS, STATE, BACKLOG, PROTOCOL y las issues#1/#2: auditoría GEO y mapeo ya ejecutados; no repetir. La rama pendiente contiene trabajo posterior al resumen de main, incluido el sello del índice aportado por Luis. No se trataron sus informes como fusionados.

El siguiente paso real sigue siendo emitir y revisar un descriptor deshabilitado en WSL y decidir expresamente sobre7200s totales/1800s HTTP nuevos. No se ha recibido ese descriptor en esta ejecución ni se accedió al host de Luis. Para avanzar por una vía segura se preparó una ayuda opcional de revisión de metadatos. **No añade un gate obligatorio ni cambia el trabajador del piloto.**

Plan previo: research/plans/2026-11-03-cached-plan-offline-review.md. Pregunta: ¿podemos detectar deriva de cargos, ventanas, muestras, prefijos y cobertura antes de decidir ejecutar? Predicción: propuesta archivada aritméticamente coherente y descriptor artificial estable; mutaciones negativas deben rechazarse. Fracaso si una mutación pasa o si el revisor ejecuta procesos/red, sigue rutas del descriptor o confunde un fixture con el equipo real.

## Código y resultados ejecutados

Nuevo audit_cached_pilot_descriptor.py, solo biblioteca estándar. LeeJSON≤2MiB, rechaza claves duplicadas, NaN/Infinity/desbordamiento, booleanos como enteros de límites, rutas no canónicas y controles explícitos de presupuesto/política. Perfil estático fijado por SHA256 a la propuesta y al código revisado49f37a0c. Los dosJSON de referencia conservan exactamente los SHA256 que exige el trabajador existente; pinned-source-check.json recoge la comparación.

La propuesta real archivada pasa: cargo previo4.355.802.733B + cuatro mates6.349.703.881B =10.705.506.614B; margen1.294.493.386B dentro de12GB. La suma de lecturas se coteja además contra los cuatro tamaños del manifiesto fuente, no solo contra un total copiado. Los3748,5157940387726s históricos y el deadline antiguo permanecen como datos, sin renovarlos.

16 pruebas locales correctas y compileall correcto. Dos revisiones de un descriptor **artificial**, con rutas/suplentes explícitamente sintéticos, producen bytes idénticos. Las22mutaciones declaradas se rechazan: activar ejecución, aumentar bytes o ventanas, devolver cargos o tiempo, cambiar URL/MD5, invertir etapas, añadir muestras/descarga del índice, duplicar prefijo, relajar cobertura/temporales, cambiar coordenadas o miembros y alterar raíces. Otras pruebas cubren esquema, no mutación de entradas y JSON inválido. Un test intercepta acceso a archivos, sockets y Popen para demostrar que review() no los usa. Son controles de software, no experimentos biológicos.

Los comandos CLI se ejecutaron sobre la propuesta archivada y sobre el fixture. El resultado de este último declara fuente no autenticada. executed-final/summary.json conserva real_WSL_descriptor_provided=false; no hay un descriptor real aprobado. executed corresponde a la primera demostración antes de añadir la comprobación cruzada del total contra los cuatro mates; se conserva como historia local de software, sin convertirla en otra muestra.

## Interpretación y límites

La ayuda verifica únicamente los campos estáticos enumerados: caps/etapas, orígenes, selección de mates, prefijo, cobertura, objetivos, parte de los límites compactos y continuidad declarada del índice/cargos. **No sustituye validate_job, el trabajador ni la aceptación expresa.** No autentica productor, Python/decodificador/binario, sellos, archivos, host, política completa del reductor o recursos observados. El sello comunicado por Luis sigue siendo evidencia aportada por él; no una inspección remota del equipo.

Toda salida mantiene execution_enabled=false, raw_execution_ready=false, host_files_verified=false y window_authorized=false. Un resultado declared_offline_policy_checks_passed solo significa que esos campos concretos coinciden con el perfil; no que el plan pueda ejecutarse, que todo el manifiesto esté validado o que se haya aceptado una ventana. Ningún URL o ruta del descriptor se consulta. No hay lecturas biológicas, descargas, índice humano, alineamientos, efectos, PSI, inferencia, función o clínica nuevos. Tampoco se reabrieron búsquedas bibliográficas cerradas: esta fase no formula una afirmación científica nueva que requiera otro rastreo.

## Uso y siguiente prueba discriminante

Desde la raíz del repositorio:

```bash
python -m unittest discover -s tests -p 'test_cached_pilot_descriptor_review.py' -v
python scripts/audit_cached_pilot_descriptor.py --proposal reports/cached-index-pilot-20261102/execution-proposal.json
python scripts/audit_cached_pilot_descriptor.py --plan /ruta/al/descriptor-deshabilitado.json
python scripts/run_cached_plan_review_fixture.py /tmp/review-fixture-new-directory
```

El último comando genera únicamente metadatos artificiales. Para una revisión real hace falta elJSON completo deshabilitado de WSL y su SHA, no solo la captura del sello del índice. Sigue vigente el runbook research/runbooks/2026-11-02-cached-index-pilot-powershell.md. Después se revisarán sus valores concretos y, si procede, Luis decidirá expresamente sobre la nueva ventana. No se emite aceptación automática ni se relanza el job viejo. Esta ayuda no modifica esa secuencia ni exige repetir preparación si el código del trabajador no ha cambiado.

Cierre de esta tarea: comprobación offline opcional ejecutada y persistida en PR36; piloto real pendiente de descriptor/decisión. La CI de la nueva cabeza se verifica por separado y se enlaza en la PR. Sin merge/cierre automático, contactos, gastos o publicación externa.
