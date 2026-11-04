# Revisión de integración de PR #46 y #47 — 04/11/2026

Base remota comprobada: main `95bf05ecc1f991ec9843d48519d0764b29dc5dfb`. Ambas ramas proceden directamente de main y están abiertas. Este documento prepara su revisión; no ejecuta merge.

| PR | Cabeza revisada antes de esta continuación | Contenido |
|---|---|---|
| [#46](https://github.com/luisceb1/ela-research/pull/46) | `9a69cb8caec3281a35dd29cd8add7a36d07ec968` | Continuidad administrativa y búsqueda pública ampliada K26 Fig.4d |
| [#47](https://github.com/luisceb1/ela-research/pull/47) | `90eef8b31f223107bf6e4aaa5a232a6e44760035` | Auditoría A25 Fig.3s, mapa pendiente, denegación de acceso y comunicación autorizada; esta continuación añade reproducción descriptiva |

La CI de #46 en esa cabeza tiene cinco checks correctos, incluida la matriz Python 3.11/3.12. No es validación biológica ni sustituye comprobar la CI de la nueva cabeza de #47. Los 24 controles locales A25 se documentan por separado.

Orden recomendado cuando se autorice la integración: #46 primero; después reconciliar #47 contra el main resultante, resolver STATE/BACKLOG y comprobar su nueva cabeza/CI antes del segundo merge. No crear una cadena de PR dependientes para hacerlo.

Puntos concretos que deben conservarse al resolver conflictos:

1. #46 documenta avisos administrativos mixtos: aprobación del dataset seguida de revisión, workspace pendiente. No volver al texto antiguo que decía solo recepción/revisión. Ninguno acredita acceso efectivo o manifiesto.
2. Conservar el resultado de la búsqueda ampliada Fig.4d, sus errores y regla de no repetición, enlazando sus informes una vez incorporados realmente.
3. Conservar todos los informes, fuentes fijadas y 73 observaciones A25 de #47; la concordancia de 2/2 medias es aritmética, sin mapa de cultivos ni inferencia habilitada.
4. Mantener separadas ambas comunicaciones previamente autorizadas y sus recibos. No interpretar integración como autorización de nuevos mensajes.
5. #37/#44 y sus requisitos concretos continúan; bloqueos históricos #1/#2/#14/#20 no se reactivan. Automatización pausada. No cerrar issues como consecuencia del merge.

En esta rama, los informes de #46 se citan por URL inmutable: no se copian ni se declaran incorporados. STATE/BACKLOG corrigen su nota administrativa antigua con esa procedencia y registran el resultado descriptivo propio. La resolución final debe preservar ambas aportaciones y eliminar referencias a PR pendientes únicamente después del merge real.

