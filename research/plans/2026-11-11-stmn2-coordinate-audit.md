# Auditoría de las coordenadas selladas de STMN2 — plan prospectivo

Fecha: 2026-11-11. Autorización de Luis («audita las coordenadas de STMN2»). Base: main `ad96ec5`.

**Criterios fijados ANTES de mirar cuentas o consultar literatura.**

## Por qué, y qué pregunta queda abierta

Las coordenadas de STMN2 se derivaron hoy mismo y **pasaron** el cruce con ancla doble: dos rasgos de `NM_007029.4` dan el mismo desplazamiento (912.235) y el intervalo publicado cae exactamente donde una unión observada pone su aceptor.

Lo que **no** se comprobó es si el evento medido es el **único** evento críptico documentado de STMN2, o si hay otros que no estamos midiendo. La auditoría de UNC13A confirmó sus coordenadas pero no se hizo esa pregunta; aquí sí.

## Las cinco comprobaciones, con criterio de fallo

| # | Comprobación | Criterio de aceptación |
|---|---|---|
| **A1** | La unión críptica sellada aparece con **las mismas coordenadas** en los dos tejidos ya descargados | Coordenadas idénticas; si difieren, parar |
| **A2** | El exón críptico es **terminal** (poliadenilación prematura), luego **no** debe haber una unión con donante en su extremo 3′ (≈79.617.049) con soporte sustancial | Soporte ≤2 lecturas totales. Si hay más, el supuesto de «una sola unión críptica» es falso y el denominador del PSI está mal |
| **A3** | Las **cinco candidatas `annotated=0` rechazadas** (aceptores 79.613.669 / 79.613.822 / 79.615.701 / 79.630.995 / 79.631.040) deben tener soporte **despreciable** | Si alguna tiene soporte comparable al de la unión sellada, exige explicación y la auditoría no pasa sin ella |
| **A4** | Búsqueda acotada de **otros eventos crípticos documentados** de STMN2 en la literatura | Si aparece un segundo evento con coordenadas publicadas, se registra como no medido |
| **A5** | Identificar qué fuente de anotación marca la unión sellada como `annotated=1` (código `cH38`) | Informativo; no bloquea |

## Qué se hace con cada resultado

- **Todas pasan** ⇒ coordenadas confirmadas; se registra la verificación y **no se cambia nada**.
- **A2 falla** ⇒ el supuesto de unión única es erróneo; se marca el PSI de STMN2 como **mal denominado** y se declara qué informe queda afectado. **No se ajusta nada para que cuadre.**
- **A3 falla** ⇒ se informa la candidata con soporte y se detiene su interpretación hasta resolverla.
- **A4 encuentra otro evento** ⇒ se registra como laguna de medición, sin medirlo en este ciclo.

Sin descargas nuevas de datos (los RR y MM ya están en disco). Presupuesto adicional: solo metadatos bibliográficos. Sin contactos, gastos ni interpretación clínica.
