# Control global de geometría GENCODE v47

Pregunta: ¿cuántas de1901 claves coinciden con una unión anotada en cualquier gen, conservando cromosoma, hebra y extremos intrónicos? El contraste anterior solo buscaba bajo el mismo gen;73 conflictos ya demostraron que ese límite puede ocultar geometrías conocidas.

Método predefinido: tabla1901 yGTFreferencia fijados por hash; buscar todos los genes del snapshot, sin alias, proximidad, spans o tolerancia de extremos. Conservar ENSG/ENST testigos y distinguir clave con gen de geometría sin gen: dos candidatos pueden compartir geometría, no sumar como moléculas.

Para limitar memoria sin perder exones: primera pasada identifica transcritos que contienen algún anclaje exacto de los candidatos (fin de exón=startintrónico−1 o inicio=endintrónico+1). Segunda pasada recupera TODOSlos exones de cada transcripto seleccionado, incluyendo los intermedios. Agrupar antes de formar uniones; excluir un falso salto si existe un exón entre los anclajes. No asumir contigüidad del GTF. Coincidencia exacta exige ambos extremos, cromosoma y hebra.

Controles positivos: reproducir las17 coincidencias del mismo gen y las73 geometrías canónicas del gen autor. Controles adversariales: exones intercalados, exón intermedio que impide unión, hebra, mismo nombre de transcripto entre genes, varias anotaciones para una geometría y_PAR_Y. Rechazar discrepancias con testigos previos antes de interpretar resultados.

Exportar partición por candidato (mismo gen / solo otros / no encontrada), geometrías únicas, lista completa de testigos y cruce descriptivo con estados del catálogo autor. No encontrado en v47 no certifica novedad, crypticidad, función o causa. No modificar354 coincidencias estrictas ni sensibilidad355; son ejes distintos. Sin datos clínicos ni significación. Tras este control, seleccionar cobertura excluida/catálogo o reproducción #14 según evidencia y bloqueos.
