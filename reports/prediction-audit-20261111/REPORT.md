# Auditoría de predicciones: 16 revisadas, un fallo real, una sustitución de prueba

**Fecha:** 2026-11-11. **Plan prefijado:** [`research/plans/2026-11-11-prediction-audit.md`](../../research/plans/2026-11-11-prediction-audit.md), commit `06d08de`.
**Etiqueta de evidencia:** auditoría de coherencia entre umbral prefijado y veredicto declarado. **No** audita si los análisis eran correctos.

**Sesgo declarado:** audito mi propio trabajo. Por eso las 11 predicciones con umbral numérico se verificaron **recalculando desde los JSON depositados**, no releyendo mi prosa.

## Por qué se hizo

En el ciclo STMN2 declaré CONFIRMADA una predicción cuyo umbral era ≥10× y cuyo resultado fue 6,6×. **Lo detectó un segundo lector, no yo.** Quedaba por saber si era un caso aislado o un patrón.

## Resultado

**16 predicciones auditadas de 8 ciclos: 14 coherentes, 1 fallo real, 1 sustitución de prueba declarada.**

Tabla completa y verificable: [`audit.tsv`](audit.tsv).

### El fallo, ya corregido

| Ciclo | Umbral | Valor | Declarado | Correcto |
|---|---|---|---|---|
| stmn2-derivation **P1** | ≥10× | **6,6×** | CONFIRMADA | **REFUTADA** |

Corregido en el informe de STMN2 el mismo día, con la corrección visible al inicio del documento y en `STATE.md`. **Es el único fallo de este tipo en los 8 ciclos.**

### La sustitución de prueba, declarada pero digna de registro

El addendum de Ikegami predijo que **RIN, PMI y pérdida neuronal no mostrarían correlación significativa con las dos medidas** (p ≥ 0,05). Esa prueba **nunca se ejecutó**: el enlace por caso quedó rechazado porque la duración no era clave única en dos subtipos, y el propio plan ordenaba entonces no informar correlaciones de covariables.

Lo que sí se hizo fue una prueba **distinta**: si esas covariables difieren **entre subtipos**. El informe declara la sustitución, su lógica («una covariable que no difiere entre subtipos no puede explicar una diferencia entre esos subtipos») y su límite («descarta un confusor si no difiere, pero no cuantifica su efecto sobre el marcador»).

**Veredicto de la auditoría: aceptable, no oculto.** La sustitución está razonada y limitada en el propio informe, y el criterio de fracaso del plan se respetó. Pero la predicción **tal como se escribió** no se puso a prueba, y el informe dice «las tres confirmadas» sin marcar que lo confirmado es otra cosa. Queda registrado aquí.

### Las 14 coherentes

Verificadas recalculando desde los datos depositados. Entre ellas, las que más importan:

- **target-als-cortex P1**: declarada REFUTADA; máximo real 4 lecturas frente a umbral 20. Correcto.
- **target-als-cervical P2**: intervalos de Wilson 0,117 frente a 0,121 — **no solapan por 0,004**. El informe ya advertía «por muy poco». Coherente, y el margen es tan estrecho que conviene no construir nada sobre él.
- **stmn2-derivation P2**: 4 muestras con ≥20, máximo 52. Confirmada de verdad, y es la predicción central del ciclo.
- Las cuatro predicciones cualitativas declaradas «no comprobables» (Snaptron por TLS, discrepancia de fracción por eficacia no declarada) son coherentes: en ninguna se sustituyó la predicción por otra a posteriori.

## Interpretación

Un fallo en 16 no es un patrón, pero tampoco es tranquilizador por tres razones:

1. **No lo encontré yo.** Las dos revisiones externas de hoy encontraron errores míos; mi propia lectura no.
2. **El fallo estaba en el ciclo donde más me felicitaba** por haber parado ante un criterio erróneo. La autocomplacencia y el error aparecieron en el mismo documento.
3. **Esta auditoría tiene el mismo sesgo.** La hice yo, y su valor está en haber sido mecánica, no en mi juicio.

Lo que sí sostiene esta auditoría: las predicciones **se escribieron antes** en los 8 ciclos, con umbrales explícitos, y eso es lo que hizo posible detectar el fallo. Sin umbrales prefijados no habría nada que auditar.

## Limitaciones

- **Solo cubre los ciclos del 10–11/11.** Los informes anteriores al 10/11 **no se han auditado**.
- **Solo comprueba coherencia umbral/veredicto.** Un veredicto coherente puede apoyarse en un análisis equivocado, y eso queda fuera.
- No audita la rama de la PR #57 ni otro trabajo ajeno, por acuerdo explícito.
- La verificación de las predicciones cualitativas es por lectura, no mecánica, y hereda mi sesgo.

## Siguiente paso

**Lo que esta auditoría deja claro no es técnico:** mis informes necesitan un segundo lector **de forma sistemática**, no cuando a alguien se le ocurre. Hoy dos revisiones externas encontraron cuatro sobreafirmaciones y una predicción mal etiquetada. Ninguna la encontré yo.

Queda sin hacer: auditar los ciclos anteriores al 10/11 con este mismo procedimiento. No se abre aquí.

Sin contactos, gastos, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
