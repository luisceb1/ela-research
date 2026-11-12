# Vía Snaptron para las uniones crípticas de UNC13A: bloqueada por TLS, pregunta sin responder

**Fecha:** 2026-11-11. **Plan prefijado:** [`research/plans/2026-11-11-snaptron-unc13a-feasibility.md`](../../research/plans/2026-11-11-snaptron-unc13a-feasibility.md), commit `928534e`, **anterior a cualquier consulta**.
**Etiqueta de evidencia:** fallo de acceso registrado. **La pregunta de viabilidad NO queda respondida**, ni a favor ni en contra.

## Qué se intentó y por qué

Las cuatro familias candidatas de #37 se rechazaron por falta de **cuentas de uniones accesibles**, y el piloto propio sobre crudos se cerró con cobertura `[1,0,0]` frente al mínimo de 20. recount3 publica uniones exón-exón ya cuantificadas para miles de estudios públicos, consultables por API vía Snaptron sin descargar crudos ni alinear. Mallika 2026 usa esa misma infraestructura para su figura de GTEx, lo que confirma que es utilizable por terceros.

Uniones objetivo: las **ya selladas** del proyecto, sin redefinir (hg38, chr19, hebra −, intrónico 0-based semiabierto), convertidas a 1-based inclusivo para la convención de Snaptron:

| Unión | 0-based semiabierto | 1-based inclusivo |
|---|---|---|
| canónica (exón 20–21) | 17641556–17642844 | 17641557–17642844 |
| críptica izquierda | 17641556–17642413 | 17641557–17642413 |
| críptica derecha | 17642541–17642844 | 17642542–17642844 |

## Resultado: fallo de acceso, no de datos

Consulta intentada: `https://snaptron.cs.jhu.edu/srav3h/snaptron?regions=chr19:17641557-17642844`

Secuencia observada el 11/11/2026:

1. Primer intento: el proxy de egreso rechazó el CONNECT con **403** (host no permitido por la política de red). Registrado en el estado del proxy como `connect_rejected` a las 08:54 UTC.
2. Tras permitir `snaptron.cs.jhu.edu`, el túnel **CONNECT se establece correctamente** (`HTTP/1.1 200 Connection Established`), luego la política de red ya **no** es el obstáculo.
3. El handshake TLS falla al validar la cadena del servidor: **`SSL certificate problem: self-signed certificate in certificate chain`**, también aportando explícitamente el CA del proxy con `--cacert /root/.ccr/ca-bundle.crt`. El estado del proxy declara `bundleCoversEveryHost: true`, de modo que el problema apunta al certificado del origen, no al bundle.

**No se desactivó la verificación TLS** y no se intentó ninguna ruta que la eludiera. Cero bytes de datos recuperados.

## Interpretación

La vía **no queda refutada**: queda **sin probar**. La distinción importa, porque el motivo del fallo es un problema de confianza en el certificado del servidor, no la ausencia de datos ni un rechazo de política. Las cuentas de uniones de recount3 pueden perfectamente estar ahí.

Tampoco se ha comprobado nada sobre los dos criterios que de verdad decidirían: cobertura ≥20 en una unión críptica, y mapeo biblioteca→condición→unidad biológica independiente con ≥3 unidades por condición. **La predicción prefijada —que el mapeo o la cobertura fallarían— no ha podido ponerse a prueba.**

## Limitaciones

- Ninguna consulta completada; ninguna unión comparada; ninguna cuenta obtenida.
- El diagnóstico del certificado se basa en el mensaje de curl y en el estado del proxy. **No se inspeccionó la cadena** del certificado, porque hacerlo exigía no verificarla.
- Que el certificado falle hoy no implica que el servicio esté caído ni que vaya a fallar siempre.
- Este informe **no** reabre las candidatas rechazadas de #37 ni relaja ningún criterio. Cobertura ≥20 y ≥3 unidades independientes siguen vigentes.

## Siguiente paso, con decisión de alcance pendiente

El plan prefijado dice, literalmente: «No buscar espejos ni rutas alternativas por continuidad». Lo respeto y **paro aquí** en lugar de encadenar intentos.

La alternativa existe y es única y obvia, pero requiere tu decisión de alcance antes de abrirla: recount3 distribuye sus archivos de uniones por su propio almacén de datos, distinto de la API de Snaptron. Sería otro ciclo acotado, con su propio plan prefijado, y con el riesgo conocido de que los archivos por estudio sean grandes frente a una consulta puntual por región.

**Criterio de parada si se abre ese ciclo:** si los archivos de uniones por estudio no pueden consultarse por región sin descargar volúmenes desproporcionados, se cierra la vía recount3 completa y se deja de intentar. No se asumen costes ni descargas masivas.

Sin contactos, gastos, datos personales, laboratorio ni publicación externa. Marco: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
