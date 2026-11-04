# Mapa de cultivos: Supplementary Data3 y depósito enlazado

Continuación dirigida autorizada por Luis el04/11/2026 después de la auditoría numérica parcial. Permanece en PR#47, sin cambiar las prioridades #37/#44 ni reactivar la automatización.

## Resultado

**No se ha recuperado el mapa observación→cultivo.** El suplemento técnico confirma los recuentos de Fig.3s, pero ofrece resúmenes por grupo. El depósito enlazado no pudo inspeccionarse por HTTP403. La predicción prospectiva de recuperar una asignación inequívoca no se confirma en estas dos vías; no se demuestra que el mapa no exista en otras fuentes o en manos de los autores.

Se mantiene disponibilidad parcial y NO-GO para inferencia que respete la dependencia por cultivo. Los73 valores anteriores no se vuelven a contar como un experimento ni se calcula su efecto. No se imputa un mapa a partir de n, orden de filas, coincidencia de cifras o estilos.

## Fuente técnica nueva verificada

[Supplementary Data3](https://static-content.springer.com/esm/art%3A10.1038%2Fs41588-025-02361-5/MediaObjects/41588_2025_2361_MOESM8_ESM.xlsx), descrito por [Nature Genetics](https://www.nature.com/articles/s41588-025-02361-5) como caracterización electrofisiológica en cultivos neuronales. El enlace de archivo está confirmado en el [registro MBExC](https://mbexc.uni-goettingen.de/literature/publications/1299), recurso255 en la página consultada. No se descargan Data1 ni materiales clínicos.

HTTP200;18581bytes; SHA256 `7ba494959360e824eb333eeadb2e0fd1bb431a32859da92cabdd5a958cf1c2e7`. Una hoja, `Table 3`, dimensión A1:I191. Se fija por hash y se resuelve su miembro XML mediante la relación rId1 del libro, no por orden del archivo de relaciones.

| Campo permitido | Celda fuente | Valor |
|---|---|---|
| Grupo normal | C18 | UNC13AWT |
| Variante | E18 | UNC13AR202H |
| Medida | B35 | Charge (pC) |
| Panel | I35 | 3s |
| n declarado WT | C36 |38|
| n declarado R202H | E36 |35|

Los n38/35 concuerdan exactamente con los recuentos de la proyección anterior, I4:I41/J4:J38 de MOESM10. Es concordancia de recuentos, no una reproducción estadística ni una prueba de independencia. La misma tabla contiene otras medidas y condiciones que no se adoptan como nuevos objetivos ni se exportan.

No aparecen campos de cultivo, lote, identificador de neurona, réplica independiente o exclusión en las etiquetas revisadas. No hay comentarios o nombres definidos que ofrezcan el mapa. El título dice *cultured hippocampal neurons*: describe el modelo, no identifica cultivos. La tabla no contiene filas de observaciones individuales con una clave compartida enlazable a los73 valores. Los resúmenes por grupo no permiten reconstruir esa asignación.

Control de identidad adicional: B33 corresponde a amplitud en nA; aunque comparte los mismos n, no es Fig.3s. El lector exige B35=Charge(pC), I35=3s y ambos grupos antes de aceptar los recuentos. No basta con encontrar38/35 en cualquier fila. No se recalculan o exportan p-valores/medias publicadas.

## Depósito enlazado

El [registro MBExC](https://mbexc.uni-goettingen.de/literature/publications/1299) enlaza [GOE-Seek study260](https://goeseek.gwdguser.de/studies/260). Se intentó una consulta pública GET con `Accept: application/vnd.api+json`, máximo2MiB y25s. Respuesta HTTP403. La herramienta de búsqueda/apertura tampoco pudo acceder a esa URL.

**Contenido del depósito no inspeccionado.** No se declara vacío, sin datos, privado o carente de mapa a partir de ese error. No se inicia sesión, solicita acceso o contacta al soporte. Se conserva el recibo del fallo en culture-map-retrieval.json, sin cuerpo HTML de error o enlaces de autenticación.

## Ejecución, controles y errores

Python3.12.14 real, biblioteca estándar. CULTURE_MAP_PLAN.md se guardó y fijó por hash antes de recuperar el suplemento. Reutilización de los lectores XML/hash locales existentes. No se ejecutan macros, fórmulas ni código externo. culture-map-audit.json conserva las celdas técnicas seleccionadas, hashes de miembros, parámetros y hash del script. El binario completo del suplemento no se redistribuye en GitHub.

Cinco controles de software nuevos pasaron: un n agregado nunca crea asignaciones a cultivos; panel/unidad incorrectos no se aceptan por compartir n; recuento implícito se rechaza; una etiqueta «3 cultures» requiere revisión y no habilita inferencia; una fuente con hash distinto se rechaza. La fixture coloca styles.xml antes de la relación de hoja para proteger la selección por ID. Junto a los14 controles de la primera fase, son19 pruebas informáticas, no nuevos experimentos biológicos.

Se documentan dos errores de exploración local, corregidos antes del lector final: seleccionar inicialmente la primera relación XML conducía al archivo de estilos y no a una hoja; después una celda de formato sin valor produjo un error al acceder a su texto. El programa final resuelve por ID y trata las celdas vacías. No se obtuvo resultado científico de esas ejecuciones fallidas. HTTP403 del depósito permanece sin resolver.

Reproducción del suplemento técnico:

```bash
python scripts/audit_asadollahi_culture_map.py --download --source /tmp/asadollahi-MOESM8-supplement3.xlsx --output /tmp/asadollahi-culture-map-audit.json
python -m unittest discover -s tests -p 'test_audit_asadollahi*.py' -v
```

Sin `--download`, se utiliza una copia local con el hash fijado. El intento al depósito se reproduce con la URL/cabecera y límites del recibo; su respuesta futura puede cambiar y no se presume nuevamente fallida.

## Decisión y siguiente condición

Se completa y detiene esta búsqueda dirigida. No se amplía a otro candidato, suplemento clínico, descarga masiva o modelo. No se vuelve a abrir la misma fuente sin cambio verificable.

El dato que cambiaría la decisión es una asignación técnica explícita de las observaciones a cultivos con su significado, más aclaración de identidad/exclusiones. El acceso efectivo al manifiesto de GOE-Seek sería una vía posible para comprobarlo, **sin garantía de que contenga el mapa**. Cualquier contacto o solicitud de acceso requerirá autorización específica. #37 y #44 conservan sus bloqueos distintos.
