# GOE-Seek260: lectura anónima denegada por la aplicación

Continuación manual solicitada por Luis el04/11/2026 para intentar la siguiente entrada, acceso efectivo al manifiesto/mapa de cultivos. No se autoriza ni realiza envío externo, creación de cuenta, login, solicitud de acceso, consulta clínica o cambio del objetivo científico.

## Comprobación y resultado

Se revisó la representación HTML del registro publicado por MBExC y la documentación oficial de SEEK. La [documentación de la API](https://docs.seek4science.org/help/user-guide/api) indica que el acceso anónimo solo devuelve contenido públicamente visible. La representación JSON documentada permite comprobar una vía pública alternativa sin utilizar credenciales o sesiones.

GET anónimo a https://goeseek.gwdguser.de/studies/260.json con Accept:application/json devuelve HTTP403, Content-Type:application/vnd.api+json y un cuerpo JSON de73bytes:

```json
{"errors":[{"title":"Forbidden","details":"You may not view study:260"}]}
```

SHA256 de la respuesta: `da151a44635eee7099a605f935722038b1c9e9eb5739965ed62a4ada31930406`. Recibo completo reducido en public-access-api.json, con Python3.12.14, fecha, parámetros y fuente. No se guarda ningún cookie, token, cabecera de sesión ni cuerpo HTML.

La consulta HTML también devolvió403. Un enlace de navegación «Log in» no prueba que crear una cuenta baste para ver el registro. La respuesta JSON acredita denegación de lectura anónima de study260; no explica si el registro es privado, existe un error de permisos, el enlace institucional quedó antiguo o se requiere una autorización específica.

No se obtuvo manifiesto, lista de archivos ni mapa de cultivos. No se enumeran IDs alternativos, buscan rutas ocultas o reutilizan sesiones para eludir la denegación. Se detiene esta vía pública hasta un enlace público nuevo, cambio confirmado del acceso o respuesta institucional.

## Canal técnico verificado y propuesta revisable

La [plataforma oficial GoeSeek Uploader](https://upload.goeseek.gwdguser.de/) identifica al servicio como parte del marco de datos de investigación de University Medical Center Göttingen y publica `menoci@medizin.uni-goettingen.de` como soporte técnico. Se elige ese canal específico del servicio para una consulta de enlace/permisos, sin atribuir a soporte la autoría del experimento. No se adivina una persona ni se añade CC. El registro MBExC también publica un alias de soporte de su plataforma; no se mezclan destinatarios por defecto.

[SUPPORT_REQUEST_DRAFT.md](SUPPORT_REQUEST_DRAFT.md) conserva el borrador histórico, que no se envió. Tras presentarse una versión final más breve en el chat, Luis autorizó expresamente su envío el04/11/2026. Ese texto final y su recibo verificado constan en [COMMUNICATION_LOG.md](COMMUNICATION_LOG.md) y [SUPPORT_REQUEST_SENT.md](SUPPORT_REQUEST_SENT.md). No se incluyen el repositorio privado, resultados propios, datos personales, adjuntos o información clínica. La autorización de este mensaje no habilita seguimientos u otros contactos.

## Reproducción del chequeo

```python
import urllib.error
import urllib.request

request = urllib.request.Request(
    "https://goeseek.gwdguser.de/studies/260.json",
    headers={"Accept": "application/json"},
)
try:
    with urllib.request.urlopen(request, timeout=20) as response:
        status, body = response.status, response.read(2_097_153)
except urllib.error.HTTPError as error:
    status, body = error.code, error.read(16_384)
```

La respuesta futura puede variar. Es una comprobación administrativa de acceso, sin nuevas pruebas unitarias o experimentos biológicos; no se vuelve a ejecutar el análisis de las73 medidas ni se hereda la CI de una cabeza anterior. La concordancia38/35 y el NO-GO inferencial del informe anterior permanecen.
