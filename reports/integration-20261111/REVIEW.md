# Integración revisada de Claude y PR #57

Fecha: 11/11/2026. Alcance autorizado: integrar los seis commits de Claude con el ciclo STMN2 cerrado, verificar la combinación y fusionar el PR. Sin nuevos análisis biológicos, contactos ni descargas de datos.

## Referencias revisadas

- Base común: ad96ec5e3e5ebb40a12324c0802a4979916f5c4d.
- Rama Claude: 5ef8825911c0a054e9ffa773a01f10cb1a8322dc, seis commits exclusivos: 06d08de (plan de predicciones), fdb48c2 (auditoría), 8fcb33c (plan de coordenadas recuperado), ac670be (auditoría de coordenadas), a85f950 (corrección de P1), 5ef8825 (restauración tras push forzado e incidente).
- Rama #57 revisada: 7d1e39fda224781c2bdf6c5f195bdc0931624ead, ciclo cerrado, CI 1151 pruebas correcta.
- main al preparar integración: 6454421114c33bfa23965ab36efffef5af87a184. Su único cambio posterior a la base común es reports/2026-11-11-pubmed.md, que se conserva intacto.

La integración usa los tres padres explícitos, sin reset ni push forzado: conserva tanto la ascendencia de los seis commits de Claude como la de #57 y main. No se toma una rama completa por encima de la otra.

## Resolución por archivo

| Entrada de Claude | Resolución |
|---|---|
| Dos planes originales | Conservados byte a byte; no se reescriben criterios históricos para adaptarlos a resultados |
| Auditoría de 16 predicciones y TSV | Incorporadas con revisión visible y columna integration_review; clasificación estrecha original preservada, sin convertirla en validación científica |
| Auditoría regional de coordenadas | Conteos conservados con procedencia; se retiran terminalidad/exhaustividad demostradas por no detección y la comparación incorrecta con todos los eventos no canónicos |
| Informe de derivación STMN2 | Se conserva versión corregida de #57 y se reconoce explícitamente la corrección de Claude; P1 6,6× bruto / 8,085× normalizado, ambos <10; P3 descriptiva |
| Archivo sellado STMN2 | Coordenadas y campos originales inalterados; anotaciones de auditoría acotadas, sin afirmar fracción molecular validada |
| STATE/BACKLOG | Combinación de tres vías sin conflictos de texto; se revisan las adiciones que reintroducían sobreafirmaciones y se añade un estado actual único |
| Incidente de git | Conservado como historial y corrección, sin repetir el push forzado |

## Correcciones materiales durante la revisión

1. **P1 no cumplida:** 6,6× es razón de medianas brutas, no la cuantificación normalizada. El cálculo normalizado de #57 da 8,085×; tampoco cumple ≥10.
2. **P3/Wilson:** la dirección de frecuencias puede describirse; el solapamiento o no de intervalos no confirma por sí solo una hipótesis de enfermedad.
3. **P2/UNC13A:** cuatro bibliotecas con ≥20 lecturas demuestran cobertura local STMN2 en esos casos; no prueban una causa exclusiva del locus para el límite UNC13A.
4. **Confusores Ikegami:** una prueba no significativa entre subtipos no establece equivalencia ni excluye confusión. La correlación prefijada no se ejecutó tal como estaba escrita. Se corrige también el informe fuente que sostenía esa inferencia, preservando sus cifras. El cuadrado de Spearman tampoco se interpreta como fracción de varianza biológica explicada.
5. **No detección:** ausencia de una unión de salida observada no demuestra inexistencia, terminalidad universal ni exhaustividad. La literatura y la alineación respaldan el evento sellado; siguen sin resolverse otros extremos de poliadenilación y sensibilidad.
6. **Anotación/dominancia:** 484/9≈54 compara solo con el subconjunto no anotado. No representa todos los eventos no canónicos; dos alternativas anotadas del inventario tienen 108 y 89 lecturas.
7. **Donantes:** tres sitios donantes de empalme son tres coordenadas, no tres personas.
8. **Alcance de auditoría:** la tabla tiene 16 filas, once numéricas y cinco cualitativas. Hay nueve etiquetas de ciclo porque el addendum de covariables se separa; el autor las agrupó en ocho planes/ciclos. La clasificación 14/1/1 no es un censo de todos los errores ni certifica las inferencias de las otras filas.

## Comprobaciones y límites de revisión

Se recalcularon contra los JSON ya depositados los totales crípticos STMN2: **215 en corteza y 484 en cervical**, y el total canónico cervical **15.004**; la detección críptica cervical es **72 bibliotecas** entre todos los grupos. Coinciden con los números de la auditoría regional. Las cuentas originales no cambian.

No se reabrieron matrices regionales completas para recalcular las 50 uniones/candidatas raras reportadas por Claude, ni se reprodujeron las once operaciones históricas de toda su auditoría. Esos inventarios conservan procedencia y alcance explícitos; no se usan para sostener completitud. La revisión corrige su interpretación, no los presenta como verificación independiente de todos los datos.

Se comprueba identidad de los planes originales, igualdad semántica de la diana sellada salvo metadatos de auditoría, integridad de las 16 filas originales del TSV y ausencia de cambios a cuentas. La suite completa se ejecuta sobre el commit combinado antes de fusionar, no se suman las cuentas de pruebas de dos ramas. Los enlaces de CI y SHA exacto quedan en el PR.

## Balance científico único y cierre

El [informe final STMN2](../stmn2-within-region-20261111/REPORT.md) sigue siendo el balance vigente: patrón tisular exploratorio en 45 pares, restricción RIN principal positiva en 19, filtro estricto de nueve con mediana cero y composición sin resolver. Las correlaciones dentro de región no corrigen el efecto tisular ni prueban mecanismo. No hay rescate, causalidad ni replicación independiente.

El ciclo sobre los mismos donantes queda cerrado. La auditoría anterior al 10/11 sigue pendiente y se prioriza solo si una afirmación antigua continúa sustentando una conclusión actual; esta revisión no certifica todo el histórico. Las condiciones de #37 UNC13A y #44 K26 no cambian. El siguiente avance científico exige una entrada discriminante o datos independientes, no otro ajuste sobre estos 45 donantes.
