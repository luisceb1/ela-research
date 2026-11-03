# Fig.4d — solicitud enviada

Estado actualizado 03/11/2026: Luis autorizó expresamente el envío. Enviado desde `luis.ceb.fr@gmail.com` a `p.fratta@ucl.ac.uk`, sin CC ni adjuntos; Gmail devolvió etiqueta SENT, mensaje/hilo `1a1a307be60459fe`. Esto confirma envío, no entrega, lectura o respuesta. Texto exacto en `COMMUNICATION_LOG.md`. Pendiente de datos; no se estima ningún efecto.

La preparación anterior se conserva a continuación como historial; sus indicaciones «sin enviar» describen el estado previo, no el actual.

---

# Fig.4d — solicitud concreta preparada, sin enviar

Estado 03/11/2026: **no enviada; requiere autorización expresa de Luis**. No se ha creado un borrador en el buzón ni solicitado acceso. No se adjunta el manuscrito ni se propone un experimento nuevo.

## Destinatario propuesto y comprobación

Pietro Fratta, `p.fratta@ucl.ac.uk`, autor de correspondencia de K26. La dirección aparece en p.2 del manuscrito aceptado aportado por Luis, junto con las de Juan Burrone, Matthew Keuss y Peter Harley. Se elige un solo destinatario, sin CC, para que pueda remitir la petición al equipo responsable del panel espinal. No se presupone que Fratta adquiriese personalmente esos registros.

Consulta acotada de Gmail conectado: mensajes desde/hacia Fratta o Keuss posteriores al 20/10/2026, sin coincidencias. Esto **no demuestra que Luis no haya contactado antes**, por otras direcciones, cuentas, alias o fechas. Antes de enviar, confirmar que no existe una petición pendiente en otra cuenta o hilo; si existe, adaptar como seguimiento, sin duplicarla. No se ha inspeccionado otro buzón ni se amplió la búsqueda.

## Mensaje preparado en inglés

**To:** Pietro Fratta <p.fratta@ucl.ac.uk>  
**Subject:** Source data for Fig. 4d — UNC13A splice correction in spinal motor neurons

Dear Professor Fratta,

I am an independent researcher with a legal background, learning biology and working on a reproducible computational review of TDP-43-dependent splicing and neuronal function.

I would like to reproduce the analysis of evoked EPSC amplitude in spinal motor neurons in Fig. 4d of the accepted manuscript, “UNC13A splice correction rescues synaptic dysfunction induced by TDP-43 loss”. Could you point me to the original source-data file for that panel, or forward this request to the appropriate co-author?

For this analysis, I would need the individual cell values and units, their condition and independent culture/differentiation identifiers, and any recorded exclusions or quality-control criteria. The panel reports 34 control, 30 TDP-43 knockdown and 25 knockdown plus M21-6 cells from three experiments. I would like to preserve that experimental structure rather than treat all cells as independent biological replicates.

If available, the statistical script, package versions, treatment and recording dates, and clarification of the amplitude sign convention would also help. The existing file format is fine; no new experiments or matched RNA measurements are needed. Please let me know any conditions for reuse and attribution.

Thank you for your time.

Best regards,
Luis Cebrián Fraile

## Respuesta mínima útil

Un enlace al fichero ya existente puede bastar. CSV, Excel, Prism o exportación Igor/R son aceptables para inspección: no exigir al autor nuestro esquema CSV. Transformar posteriormente mediante un adaptador trazable, conservando bytes originales y mapeo de columnas; nunca generar IDs de diferenciación por orden de filas o colores.

La tabla debe permitir distinguir grupos y agrupación biológica; el código y los metadatos adicionales mejoran la reproducción, pero no se finge su disponibilidad. No pedir datos personales de pacientes ni nuevos experimentos. Si solo llegan puntos sin identificadores, se mantiene el bloqueo para análisis jerárquico.
