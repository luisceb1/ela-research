# Plan previo: identidad de unión STMN2 y escala de uniqueCounts

Pregunta 1: ¿la unión del candidato GSE310723:BambuTx9249 coincide exactamente, en GRCh38 y hebra correcta, con una unión críptica STMN2 informada en una fuente primaria independiente?

Predicción: coincidencia de cromosoma y de límites exónicos 79.611.214→79.616.822, con STMN2 en hebra + según referencia. Distinguir coincidencia de unión de identidad de transcrito completo, final 3′/poliadenilación y nueva validación funcional. Un eventual signo de hebra discordante en una tabla debe registrarse, no corregirse silenciosamente. Criterio de fracaso: coordenadas/ensamblaje/convención no verificables o discordantes. Controles: unión anotada, ±1 base, hebra opuesta y transcritos UNC13A del catálogo.

Pregunta 2: ¿el código de bambu 3.2.6 o la exportación del estudio justifican que todos los uniqueCounts sean múltiplos de dos?

Predicción abierta: la fuente definirá la semántica de uniqueCounts; la paridad podrá quedar sin explicación. No adjudicar multiplicación a software, biología o duplicación de lecturas sin rastrear una operación concreta. Comparar también fullLengthCounts y CPM publicados, sujetos a hashes y controles numéricos, para localizar la anomalía. No transformar las cuentas originales por suposición.

Método: Python determinista, fuentes primarias oficiales (artículos, suplementos, repositorio del autor/Bioconductor), extracción mínima de coordenadas/documentación y registro de URL, fecha y SHA256. No descargar tablas individuales clínicas; trabajar con anotaciones moleculares, código y matrices públicas de expresión ya autorizadas. Pruebas offline y resultados exportables. Sin p-valores ni nuevas muestras clínicas. Evidencia: identificación estructural contrastada, manteniendo abundancia exploratoria; documentación técnica no prueba de causa en los datos depositados.

Siguiente prueba si se resuelve: comprobar soporte full-length del candidato y distinguir coincidencia de unión de terminación 3′. Si no se resuelve escala/identidad, documentar bloqueo y avanzar a evidencia funcional publicada, sin comunicaciones externas ni gastos.
