# Índice HISAT2: descarga e inspección real — 31/10/2026

## Pregunta y resultado

Plan fijado antes de descargar: research/plans/2026-10-31-hisat2-index-inspection.md. ¿El índice público hg38 fijado porversionId se recupera íntegro bajo presupuesto y reconstruye chr8/ventanas STMN2 concordantes? **La puerta técnica acotada pasa.** No es evidencia biológica, comparación de grupos o piloto RNA-seq ejecutado.

| Comprobación ejecutada | Resultado |
|---|---|
| ObjetoS3 fijado | versión8z.MUbL_W4wij.Nmcia5c4mT7tlz0cU.; tamaño4.355.786.349bytes; ETag y versión coincidentes en GET |
| SHA256 del archivo completo | 1848784403a0fb3ee7735b2f891d8be96fd2782e08aed3d8212d922666f077a5 |
| Integridad y extracción | Gzip drenado hastaEOF conCRC/ISIZE verificados; tar sin rutas inseguras/enlaces/dispositivos; hashes de cada fichero |
| Contenido | Ocho ficherosht2 + make_hg38.sh de1292bytes, leído y conservado como texto, sin ejecutarlo |
| Tamaño extraído | 4.664.043.238bytes; archivo+extraído9.019.829.587bytes (~8,40GiB) |
| Software ejecutado | hisat2-inspect-s2.2.3, compilado decommit0d244324f98de541bce04d45c75e83bc3522f7f4, g++13.3.0 |
| Reconstrucción en flujo | 455secuencias,3.209.286.105bases; sin FASTA completo escrito en disco |
| chr8 | longitud145.138.636; tres ventanas STMN2 idénticas a las ya cotejadas con UCSC/Ensembl |
| Memoria/tiempo de inspección | máximo hijo4.758.644KiB (~4,54GiB);44,83segundos; límite de espacio virtual6GiB |

Descarga111,69s; extracción31,27s; compilación del inspector24,83s, máximo hijo382.160KiB. Tiempos observados de esta ejecución, no estimación de tiempo para alinear bibliotecas. Se trabajó con máximo2hilos y sin costes de servicios externos.

## Integridad y alcance de referencia

La descarga se hizo desde URLconversionId, no desde objeto mutable. Coinciden el tamañoHTTP y los bytes recuperados. El SHA256 es propio y sirve para cotejar futuras recuperaciones; **no había un SHA256 esperado independiente publicado**. El ETag multipart no se trata como MD5. Antes de extraer se recalculó el SHA256 contra el registro de la descarga. Cada archivo extraído tiene tamaño/hash; el lector gzip se drenó después del final del tar para verificar su pie. Los controles rechazan tamaño, rutas, enlaces, CRC alterado y presupuesto excedido.

El paquete fuenteHISAT2 de7.061.238bytes tiene SHA2566945738e803a0fd742718b3b46cadc207c6eda61762e7248e05af4afa96b8fdc. El binarioInspector tiene SHA25677828165beac1086689b47bbc8413a9d66c1eb46e5d9fb85b5d1333295a3368b y comunica versión2.2.3. No se instaló globalmente ni se compiló/ejecutó todavía el alineador. La receta interna del índice apunta a UCSC hg38.chromFa.tar.gz y construcción sinGTF, pero no acredita el comando/version exactos del constructor original. La receta no se ejecutó.

El inspector reconstruyó secuencias y se registran nombres, longitudes y SHA256 normalizados porcontig. Para chr8, SHA256334965118a901898c62cd9e12942357b60b98ca490be82974efc4bb45a3febce. Este hash dechr8 es observado, no cotejado contra un hash externo del cromosoma completo. La comparación externa verifica longitud145138636 y solo estas ventanas:

- Donante: AGCAATGGGTAAGGCA.
- Aceptor críptico candidato: TATTGCAGGACTCGGC.
- Aceptor canónico: CATTTCAGCCTACAAG.

No se declara igualdad externa completa de3,2Gb, GTF completo revalidado, sitio polyA, transcrito completo o uso real de las uniones. La aceptación es **para continuar controles técnicos**, no para declarar una fuente biológica aceptada o piloto listo. No se alineó un genoma recortado ni se usó-k1 para fabricar unicidad.

## Recursos, reproducibilidad y fallos

Presupuesto previo:6GiB RAM,2hilos,15GiB adicionales y8GiB libres de reserva. Archivo+índice9,02GB. El incremento global de disco observado, que incluye fuente/compilación y posibles cambios compartidos del entorno, queda por debajo15GiB; quedaron más51GB libres. El máximo de memoria corresponde al proceso hijo inspector, medido conPythonresource; no es pico agregado del sistema ni consumo del futuro alineador. La reconstrucción se procesó por líneas64KiB y solo conserva hashes/longitudes/ventanas.

Python3.12.14, sin aleatoriedad o dependencias Python nuevas. **295pruebas locales correctas** (284anteriores+11nuevas) ycompileall. Incluyen corrupción deCRC incluso con SHA recalculado, escape de rutas, symlink, límite de tamaño, archivo alterado/incompleto y ventana que cruza bloques. No son295experimentos. La CI nueva se verifica por SHA; no vuelve a descargar el índice de4,36GB ni ejecuta esta inspección completa.

Fallos conservados: el protocolo faltaba en la copia local parcial y se leyó de la rama remota antes del análisis; /usr/bin/time no está disponible y el primer comando terminó127 antes de compilar. El reintento conmonotonic/resource compiló correctamente. Advertencias del compilador en build-inspect-retry.txt, sin ocultarlas como si fueran éxitos biológicos. errors.json y logs conservan la distinción.

Comandos reales de referencia:

```bash
python scripts/inspect_hisat2_index.py download --manifest reports/stmn2-reference-gate-20261031/index_candidate.json --archive data/cache/hisat2-index-20261031/hg38_genome.tar.gz --report reports/hisat2-index-inspection-20261031/download.json
python scripts/inspect_hisat2_index.py extract --manifest reports/stmn2-reference-gate-20261031/index_candidate.json --archive data/cache/hisat2-index-20261031/hg38_genome.tar.gz --download-record reports/hisat2-index-inspection-20261031/download.json --destination data/cache/hisat2-index-20261031/extracted --report reports/hisat2-index-inspection-20261031/extraction.json
```

El comando exacto de inspección, límites, fuente/binario/versiones y parámetros está en reference_comparison.json, build.json y environment.json. Los programas rechazan sobreescribir una descarga/extracción existente; no volver a ejecutar estos comandos sin revisar el manifiesto y el estado de archivos. Para recuperar más adelante, cotejar los bytes completos con el SHA registrado, no aceptar silenciosamente una copia parcial. verified_index.json es el registro vigente; el candidato del informe anterior se conserva como entrada histórica inmutable.

## Continuación y operación

Se amplía **el mismoPR33**, sin nueva cadena de ramas ni fusión automática. Main9c82795d yPR30 cabeza053ef70ce437cc637ec18278a2c07e3abd6bf58b permanecen intactos. No datos clínicos personales, contactos, publicación externa, gastos, FASTQ, cuentas RNA-seq o resultados funcionales.

La siguiente prueba discriminante es compilar/ejecutar el alineador fijado y probar con datos sintéticos la semánticaNH/XS/MAPQ, multimapeo, anclas y extracción comparada con implementación independiente. Un índice válido no demuestra sensibilidad del alineamiento. Si no reproduce ambos eventos o acepta controles negativos, corregir antes de crudos; no modificar umbrales según un efecto observado. Solo después puede iniciarse el piloto técnico predefinido, sin contraste biológico del subconjunto inicial.

Fuentes primarias: página de índices https://daehwankimlab.github.io/hisat2/download/; objeto/versionId exactos en download.json; fuente de software https://github.com/DaehwanKimLab/hisat2/tree/0d244324f98de541bce04d45c75e83bc3522f7f4. Ventanas de referencia y respuestas públicas en reports/stmn2-reference-gate-20261031/reference_inputs.json. No nueva afirmación bibliográfica o clínica.
