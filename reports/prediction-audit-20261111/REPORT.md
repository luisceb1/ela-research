# Auditoría de 16 predicciones: coherencia declarativa, no validación inferencial

**Revisión de integración:** [REVIEW](../integration-20261111/REVIEW.md). Se conserva la clasificación original de Claude como resultado de su auditoría estrecha; no es un recuento de todos los errores científicos. La revisión retira la exclusión de confusión por p>0,05 y la confirmación inferencial por intervalos de Wilson.

**Fecha:** 2026-11-11. **Plan prefijado:** [`research/plans/2026-11-11-prediction-audit.md`](../../research/plans/2026-11-11-prediction-audit.md), commit `06d08de`.
**Etiqueta de evidencia:** auditoría de coherencia entre umbral prefijado y veredicto declarado. **No** audita si los análisis eran correctos.

**Sesgo declarado:** audito mi propio trabajo. Por eso las 11 predicciones con umbral numérico se verificaron **recalculando desde los JSON depositados**, no releyendo mi prosa.

## Por qué se hizo

En el ciclo STMN2 declaré CONFIRMADA una predicción cuyo umbral era ≥10× y cuyo resultado fue 6,6×. **Lo detectó un segundo lector, no yo.** Quedaba por saber si era un caso aislado o un patrón.

## Resultado

**Clasificación original de Claude: 16 predicciones, agrupadas por Claude en ocho planes/ciclos (la tabla tiene nueve etiquetas, al separar el addendum de covariables), 14 coherentes según su regla de umbral/veredicto, 1 incoherencia de P1 y 1 sustitución declarada.** Esto no significa que las otras 14 estén validadas científicamente; algunas solo registran una dirección descriptiva.

Tabla completa y verificable: [`audit.tsv`](audit.tsv).

### El fallo, ya corregido

| Ciclo | Umbral | Valor | Declarado | Correcto |
|---|---|---|---|---|
| stmn2-derivation **P1** | ≥10× | **6,6× bruto; 8,085× normalizado** | CONFIRMADA | **REFUTADA** |

Corregido en el informe de STMN2 el mismo día, con la corrección visible al inicio del documento y en `STATE.md`. Es la incoherencia umbral/veredicto identificada por esa revisión acotada; no certifica ausencia de otros errores.

### La sustitución de prueba, declarada pero digna de registro

El addendum de Ikegami predijo que **RIN, PMI y pérdida neuronal no mostrarían correlación significativa con las dos medidas** (p ≥ 0,05). Esa prueba **nunca se ejecutó**: el enlace por caso quedó rechazado porque la duración no era clave única en dos subtipos, y el propio plan ordenaba entonces no informar correlaciones de covariables.

Lo que sí se hizo fue una prueba **distinta**: si esas covariables difieren **entre subtipos**. El informe declaró la sustitución. **La justificación de que una diferencia no significativa entre subtipos descarta confusión es incorrecta:** p>0,05 no prueba equivalencia ni ausencia de relación con el marcador. La prueba alternativa no responde a la correlación prefijada.

**Veredicto integrado: NO COMPROBADA TAL COMO SE ESCRIBIÓ.** Declarar una sustitución evita ocultarla, pero no valida su inferencia ni permite etiquetar la predicción original como confirmada. La auditoría no rehabilita la conclusión sobre confusores.

### Las 14 coherentes

Claude registra recalcular las once predicciones numéricas. Esta integración no reproduce todas esas operaciones: conserva su procedencia y distingue aritmética de inferencia. Entre las filas que requieren contexto:

- **target-als-cortex P1**: declarada REFUTADA; máximo real 4 lecturas frente a umbral 20. Correcto.
- **target-als-cervical P2**: intervalos de Wilson 0,117 frente a 0,121 — **no solapan por 0,004**. El informe ya advertía «por muy poco». La desigualdad entre extremos es una observación aritmética; el solapamiento o no de intervalos no sustituye un contraste válido ni controla diseño/profundidad.
- **stmn2-derivation P2**: 4 muestras con ≥20, máximo 52. Confirmada de verdad, y es la predicción central del ciclo.
- La tabla contiene **cinco filas cualitativas**, no cuatro no comprobables. Dos figuran como no comprobables: Snaptron por TLS y la comparación de eficacia no declarada. Las otras registran lecturas o resultados descriptivos.
- Las direcciones observadas en P3 de corteza/STMN2 se conservan como descriptivas; no se confirma inferencia de enfermedad.

## Interpretación

Una incoherencia identificada con esta regla en 16 filas no estima la tasa global de errores ni certifica ausencia de un patrón. El autor señaló además tres límites:

1. **No lo encontré yo.** Las dos revisiones externas de hoy encontraron errores míos; mi propia lectura no.
2. **El fallo estaba en el ciclo donde más me felicitaba** por haber parado ante un criterio erróneo. La autocomplacencia y el error aparecieron en el mismo documento.
3. **Esta auditoría tiene el mismo sesgo.** La hice yo, y su valor está en haber sido mecánica, no en mi juicio.

Lo que sí sostiene esta auditoría: la existencia de planes y criterios escritos permitió contrastar los veredictos en el alcance revisado, con umbrales explícitos, y eso es lo que hizo posible detectar el fallo. Sin umbrales prefijados no habría nada que auditar.

## Limitaciones

- **Solo cubre los ciclos del 10–11/11.** Los informes anteriores al 10/11 **no se han auditado**.
- **Solo comprueba coherencia umbral/veredicto.** Un veredicto coherente puede apoyarse en un análisis equivocado, y eso queda fuera.
- No audita la rama de la PR #57 ni otro trabajo ajeno, por acuerdo explícito.
- La verificación de las predicciones cualitativas es por lectura, no mecánica, y hereda mi sesgo.

## Siguiente paso

**Lo que esta auditoría deja claro no es técnico:** mis informes necesitan un segundo lector **de forma sistemática**, no cuando a alguien se le ocurre. Hoy dos revisiones externas encontraron cuatro sobreafirmaciones y una predicción mal etiquetada. Ninguna la encontré yo.

Queda sin hacer: auditar los ciclos anteriores al 10/11 con este mismo procedimiento. No se abre aquí.

Sin contactos, gastos, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
