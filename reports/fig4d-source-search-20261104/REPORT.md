# Búsqueda pública ampliada — K26 Fig.4d, 04/11/2026

## Resultado

**No se ha localizado ni descargado una tabla original atribuible a K26 Fig.4d.** Resultado negativo acotado de acceso, no demostración de inexistencia. El contrato FR-K26-4d v1 sigue deshabilitado: no se ha estimado efecto ni reproducido función.

Luis pidió expresamente esta ampliación manual después de revisar un suplemento y una imagen de la versión anterior. No es una reanudación de la continuidad automática. No se cambia endpoint, no se contacta a nadie y no se abren candidatos científicos nuevos.

## Evidencia y controles

| Ruta | Inspección efectiva | Resultado y límite |
|---|---|---|
| [KCL, manuscrito aceptado](https://kclpure.kcl.ac.uk/portal/en/publications/unc13a-splice-correction-rescues-synaptic-dysfunction-induced-by-/) | Ficha completa por buscador/apertura; un enlace de manuscrito, estado Accepted/In press, 06/10/2026 | No tabla independiente enlazada. Descarga directa por Python: HTTP403. No asumir identidad binaria de PDFs ni ausencia de archivos ocultos/no indexados. |
| Crossref | Dos consultas por títulos, diez registros por consulta | Localiza DOI del preprint 2024; no identifica DOI final K26 entre esos resultados. No búsqueda exhaustiva de todos los registros Crossref. |
| DataCite | Consulta general UNC13A: cuatro páginas, 25+25+25+2=77 registros DOI; adicional UNC13A Keuss: uno | Ningún título identifica K26. Los 77 incluyen versiones/conceptos repetidos, no 77 datasets independientes. La consulta por autor recupera Dryad 10.5061/dryad.cjsxksnfr, asociado a otro trabajo, no a Fig.4d K26. Inspección de metadatos y relaciones, no de todos los archivos. |
| Zenodo | Consulta UNC13A, dos páginas completas, diez y cinco entradas | Ningún título identifica el ensayo K26. Hay datos de otros trabajos y análisis secundarios; no se descargan datos clínicos ni se adoptan como nueva línea. Primer intento size50: HTTP400; size10 y página2: HTTP200. |
| Figshare | POST de búsqueda, UNC13A, límite100: 42 metadatos | Ningún registro se identifica como K26 Fig.4d. Incluye trabajos de 2022 y otras investigaciones. No se confunde un Excel de otro artículo con los datos requeridos. |
| [BioStudies/OmicsDI S-EPMC11230273](https://www.omicsdi.org/dataset/biostudies-literature/S-EPMC11230273) | API BioStudies: un archivo listado, media-1.pdf, 840350 bytes declarados; ficha OmicsDI de junio2024 | Es la entrada bibliográfica del preprint K24. Descarga del PDF por endpoint público: HTTP503; **no se inspeccionan sus bytes ni se le atribuye contenido**. No afirmar identidad con el PDF aportado por Luis de distinto tamaño. |
| Europe PMC | XML completo PMC11230273, parseado; búsqueda simple Keuss AND UNC13A:16 registros | Fig.4d del XML: intensidad UNC13A, n88/96, no eEPSC espinal. Lista media-1.pdf como suplemento. No hay M21-6 ni eEPSC en ese XML. Las búsquedas de título y EXT_ID de control dan0 pese a que el XML existe: recuperación imperfecta; esos ceros **no** son evidencia fuerte de ausencia. |
| bioRxiv API | DOI10.1101/2024.06.20.599684 | Una versión devuelta, 24/06/2024; campo published=NA. No identifica la versión editorial final. NA no prueba que no se haya publicado por otra vía. Apertura de suplementos web fallida. |
| GitHub público | Búsqueda de repositorios UNC13A:7; inventario org:frattalab:25; iGluSNFR3:2 | No repositorio nuevo identificable con la tabla. Los inventarios por nombre/descripcion no equivalen a leer todos los blobs. |
| [f-hamidlab/iGluSNFR3](https://github.com/f-hamidlab/iGluSNFR3) | Árbol no truncado 0155d8dbe116a09e5e67cae4749675965515a508 y README | Procesa imágenes fluorescentes, no la tabla eEPSC espinal; esta distinción ya constaba en #35. Se confirma el destino de una pista, no se repite la auditoría del algoritmo. |
| GitHub código M21-6 + UNC13A | Búsqueda devuelve3 coincidencias, todas del propio ela-research | No evidencia externa. Buscar M21-6 sin UNC13A produce2280 coincidencias de cadenas ambiguas: no se usan como candidatos y no se afirma haber revisado las2280. |
| [Burrone/CDN, publicaciones](https://devneuro.org/cdn/group-publications.php?groupID=63&height=768&key_only=0&page=1&type=3&width=320) | Página de publicaciones y dos fichas del trabajo | Remiten al preprint2024, sin tabla aparte visible. Otros grupos/UCL/Crick buscados por índices web: sin enlace nuevo verificable; no se certifica inventario exhaustivo de sus sitios. |

Consultas web adicionales: título aceptado y anterior; LossOfTDP_Keuss_GreenAAM; autor + M21-6, source data, spinal, dataset o supplementary; restricciones a Nature, UCL Discovery/RDR, KCL Research Data, Zenodo, Figshare, Dryad, OSF, GIN, Fratta y FMP. Se usaron dos buscadores. Son búsquedas dirigidas con indexación limitada, no revisión sistemática ni certificación de inexistencia.

## Interpretación

La explicación de que la tabla aún no se haya expuesto con la versión editorial es **plausible, no verificada**. El registro KCL sigue en prensa. La declaración de datos fuente de p36 del manuscrito aceptado procede de la auditoría ya guardada en reports/functional-rescue-20261103/DATA_AVAILABILITY.md; no se presenta como nueva lectura del PDF aceptado en esta sesión.

Se mantiene la distinción de versiones: K24 Fig.4d cuantifica UNC13A en sinapsis; K26 Fig.4d, objetivo aprobado, cuantifica eEPSC espinal con 34/30/25 células. Un fichero de otro trabajo sobre UNC13A o una imagen no sustituye mediciones y mapa de independencia.

## Ejecución, errores y QC

Python3.12.14 real, biblioteca estándar, sin instalar paquetes. Primer intento con requests falló por ModuleNotFoundError; se continuó con urllib. El script guardado ejecuta las once consultas iniciales. Las consultas adaptativas posteriores y sus URL exactas quedan en api-followup.json, api-final-followup.json y datacite-pages.json; no se atribuyen al script inicial. Las versiones remotas y sus respuestas pueden cambiar.

Se conservan estados HTTP, errores, tamaño y SHA256 de respuestas leídas. Los hashes son de las respuestas de API/XML, **no de datos funcionales ni del PDF cuya descarga falló**. Se reduce la salida a metadatos bibliográficos y de archivos; sin variables clínicas, mediciones por caso ni cuerpos de correo. Las cuentas son cobertura de búsqueda, no experimentos.

Otros errores: DataCite inicial HTTP500 (recuperado con páginas25); BioStudies web inaccesible por buscador pero API legible; PMC web presenta comprobación de navegador pero XML Europe PMC legible. No se intenta sortear login o controles de acceso.

QC local: JSON parseables, SHA256 de formato válido, completitud de páginas 77/77 DataCite y15/15 Zenodo para esas consultas, 42 entradas Figshare por debajo del límite100, DOI K24 como control positivo Crossref y Fig.4d K24 como control de identidad XML. Compilación del script correcta. No nuevos tests biológicos ni suite de inferencia.

## Siguiente prueba discriminante y parada

Continuar solo con una URL o archivo original nuevo que contenga los valores eEPSC atribuibles al panel y sus claves de cultivo/diferenciación. Primero inspeccionar esquema, unidades, grupos y exclusiones; si falta el mapa, registrar disponibilidad parcial y mantener bloqueado el ajuste. Una eventual publicación editorial con Source Data también es un disparador válido. No repetir esta búsqueda amplia periódicamente sin cambio de fuente; no digitalizar puntos para fabricar datos originales. La automatización sigue pausada y las issues no se cierran.
