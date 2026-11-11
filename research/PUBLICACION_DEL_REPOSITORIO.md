# Hacer público el repositorio: lo que hay que saber antes

Fecha: 2026-11-11. Luis pidió hacerlo público. Esta nota recoge la comprobación previa y un límite que **no se puede evitar**.

## Lo que se ha redactado en el estado actual

Tres direcciones de correo aparecían en siete archivos de informes y han sido sustituidas por descripciones, sin perder el sentido documental:

| Dato | Dónde | Tratamiento |
|---|---|---|
| Dirección personal del remitente | logs y borradores de comunicación | Sustituida por una descripción |
| Dirección de correspondencia de un investigador | petición de datos de Fig.4d | Sustituida; figura publicada en el manuscrito, pero no se republica aquí |
| Dirección de soporte institucional de un repositorio de datos | auditoría A25 | Sustituida |

Ninguna contiene datos de pacientes. Los logs recogen **solo mensajes enviados por Luis**, no respuestas de terceros, de modo que no se publica correspondencia privada ajena.

## El límite que no se puede evitar

**Redactar ahora no borra esas direcciones del historial de git.** En un repositorio público, cualquiera puede leer los commits antiguos. La redacción reduce el rastreo automático de direcciones, que es el riesgo práctico, pero no impide el acceso de quien busque a propósito.

Purgar el historial sí las eliminaría, pero **rompería este proyecto**: `STATE.md`, los informes y los contratos citan commits exactos como evidencia, y reescribir el historial invalidaría todos esos SHA. El protocolo exige conservar hashes, ejecutores históricos e informes. El coste es desproporcionado.

## Lo que queda expuesto de forma deliberada, y es decisión de Luis

- **Su nombre completo** y la descripción de sí mismo como jurista en España, en el texto de la carta que envió. Es su propia divulgación; puede querer conservarla como atribución.
- **El historial completo de errores del agente**: citas mal unidas con elipsis, un bug en el propio verificador, un recuento hecho a mano que resultó falso, y la corrección de una afirmación demasiado fuerte sobre una predicción «refutada».

Sobre lo segundo: un proyecto que documenta sus fallos es más creíble que uno que solo muestra aciertos. Pero conviene elegirlo a conciencia, no descubrirlo después.

## Cómo se hace, y quién

El agente **no** tiene herramienta para cambiar la visibilidad. Lo hace Luis en GitHub: **Settings → General → Danger Zone → Change repository visibility**.

Recomendación de orden: fusionar primero la redacción, y cambiar la visibilidad después.
