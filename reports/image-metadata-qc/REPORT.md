# Figure7: independencia experimental y calibración

## Evidencia ejecutada
Se consultaron las27cabeceras TIFF mediante rangos HTTP206 verificados:65.536bytes por archivo,1.769.472bytes en total. Todas describen imágenes27740×7940píxeles,16bits, sin compresión y con un solo IFD en la cadena estándar. No se analizaron píxeles ni se validó el MD5 de los ficheros completos. Cada rango conserva SHA256; el checksum de origen se registra como no verificado sobre el fichero completo.

Cuatro archivos contienen unidad ImageJ micron y resoluciones TIFF X/Y3076923/1000000: aproximadamente0,325µm/píxel. Son KO_mScarlet_0h_01, KO_mScarlet_24h_01, KO_WTmScarlet_24h_01 y KO_WTmScarlet_48h_01. Los otros23no incluyen resolución física en los tags revisados. Ninguna cabecera tiene fecha/hora TIFF. El tiempo0/24/48procede del nombre, no de adquisición verificada. Descripciones ImageJ incluyen límites de visualización min/max: no son pruebas del mínimo/máximo real del sensor ni calibración espacial.

Los archivos calibrados no forman ningún triplete completo0/24/48, y no cubren WT ni TBN. Igualdad de tamaño de lienzo no prueba escala, registro de la misma cámara/campo ni identidad longitudinal. Transferir0,325a los23restantes sería una hipótesis, no un hecho verificado.

## Hoja publicada y unidad experimental
Se descargó Beccari_et_al_RawData.xlsx (171.253bytes); MD5 coincide con Zenodo y SHA256 figura en summary.json. Lectura directa del XML del libro, sin editarlo ni ejecutar fórmulas/macros. Figure7 contiene medidas de longitudes a24/48h y porcentajes de regeneración/estancamiento/fragmentación. Se conserva proyección de celdas y localizadores, no se altera el libro.

| Condición de columnas | Medidas24h | Medidas48h |
|---|---:|---:|
| WT+mScarlet |133|141|
| KO+mScarlet |33|64|
| KO+WT:mScarlet |127|157|
| KO+TubBindNull:mScarlet |167|217|

Son entradas numéricas, no recuento de réplicas biológicas. No hay identificadores de axón, imagen, cámara ni diferenciación que permitan enlazar esas filas con las nueve series nominales de TIFF. El artículo declara dos diferenciaciones independientes en Fig7; no se convierten nueve etiquetas ni cientos de medidas en réplicas. Tampoco se emparejan automáticamente filas24/48: tamaños distintos y ausencia de ID impiden establecer seguimiento. No se imputan ceros a axones no medidos.

La descripción del depósito resume el artículo y no aporta tabla de correspondencia. Los otros archivos auxiliares son tres vídeos de Figure4 y un macro de Figure4; no se ejecutó ese macro ni se usa para calibrar Figure7. En el cuerpo del artículo los detalles de imagen se remiten al suplemento; su descarga devolvió HTML de comprobación en lugar de PDF. La calibración alternativa y la asignación experimental permanecen abiertas.

## Decisión científica
Posible: inspección exploratoria de imágenes calibradas y mediciones en píxeles con denominador explícito, tras comprobar visualmente orientación, frontera de lesión y alineamiento. No realizado en este ciclo.

Bloqueado: comparación inferencial entre condiciones como si se conocieran réplicas independientes; velocidades en unidades físicas para todo el conjunto; cambios pareados por axón sin identificadores. No se comunica un efecto de rescate nuevo ni se interpreta el conjunto como intervención tardía: la expresión precede la lesión según cronología ya auditada.

Siguiente tarea segura: obtener suplemento por fuente pública alternativa y examinar visualmente un par calibrado de la misma etiqueta, verificando correspondencia por contenido antes de segmentar. Si no se resuelve diferenciación, mantener resultado descriptivo por imagen y registrar ese límite. Consultar autores requeriría autorización; no se ha enviado comunicación.

## Reproducción y calidad
scripts/image_metadata_qc.py lee cabeceras/caché y proyección XML; no fabrica mediciones biológicas. Verificación del transporte rechaza respuestas200, Content-Range discordante y cuerpos truncados. El lector distingue endian, tipos SHORT/LONG/RATIONAL y TIFF clásico; BigTIFF fuera de alcance se rechaza. La conversión física exige unidad micrón y racional válido, nunca escala1por defecto.

python scripts/image_metadata_qc.py; python -m unittest discover -s tests -v.59pruebas locales pasan. Fuente metadata: https://zenodo.org/api/records/15346391 ; artículo: https://doi.org/10.1073/pnas.2502294122 . Binarios originales permanecen fuera de git. La entrega contiene tablas/proveniencia y código; no nuevas imágenes completas ni datos clínicos personales.
