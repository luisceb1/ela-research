# Auditoría de las coordenadas selladas de UNC13A con ancla doble — plan prospectivo

Fecha: 2026-11-11. Autorización de Luis («revisa las coordenadas de UNC13A»). Base: main `9dc97c6`.

**Criterio de aceptación fijado ANTES de consultar UCSC.**

## Por qué

El ciclo STMN2 demostró que mi criterio estructural de `annotated=0` podía excluir el evento publicado, y que solo el cruce con ancla doble lo resolvía. Las coordenadas selladas de UNC13A proceden de una derivación **anterior** del proyecto y nunca pasaron ese cruce. Si están mal, toda la medición de esta semana apunta a uniones equivocadas.

## Lo que se audita

`research/references/unc13a_targets_sealed.json`, hg38, chr19, hebra **−**, intrónico 0-based semiabierto:

| Unión | start0 | end0 | Intrón 1-based |
|---|---|---|---|
| canónica | 17641556 | 17642844 | 17.641.557–17.642.844 |
| críptica izquierda | 17641556 | 17642413 | 17.641.557–17.642.413 |
| críptica derecha | 17642541 | 17642844 | 17.642.542–17.642.844 |

**Exón críptico implicado** por esas dos uniones: `chr19:17.642.414–17.642.541`, ancho **128**.

Intervalo publicado, en **hg19**: `chr19:17.753.223–17.753.350`, ancho **128**, DOI `10.1007/s00401-023-02655-0`. Los anchos ya coinciden; eso es consistencia interna, no verificación de posición.

## Criterio de aceptación, fijado ahora

1. Obtener de UCSC `ncbiRefSeq` el mismo transcrito de UNC13A en **hg19 y hg38**, y calcular el desplazamiento desde **dos rasgos independientes** (dos límites exónicos distintos).
2. Los dos desplazamientos deben **coincidir exactamente**. Si no, la auditoría se declara no concluyente y se para.
3. Aplicar el desplazamiento al intervalo publicado en hg19. El resultado debe reproducir **exactamente** `17.642.414–17.642.541`.

**Desplazamiento implicado por las coordenadas selladas: 110.809** (`17.753.223 − 17.642.414`). Se anota de antemano para que la comprobación sea una predicción, no un ajuste.

## Qué se hace con cada resultado

- **Coincidencia exacta** ⇒ coordenadas confirmadas; se registra la verificación en el archivo sellado y **no se cambia nada**.
- **Discrepancia** ⇒ se informa la magnitud y el sentido, se marcan como **no verificadas** y se detiene su uso hasta rederivarlas. **No se ajustan las coordenadas para que cuadren**, y se declara explícitamente qué informes de esta semana quedarían afectados.
- Si UCSC no devuelve un transcrito común a ambos ensamblajes ⇒ no concluyente; parar.

Además se comprobará si las dos uniones crípticas selladas aparecen marcadas `annotated=0` o `annotated=1` en recount3, para dejar registrado si el criterio que falló en STMN2 también se aplicó aquí.

Sin descargas nuevas de datos (los RR ya están en disco). Sin contactos, gastos ni interpretación clínica.
