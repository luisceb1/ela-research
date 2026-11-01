# GSE122069: piloto real del primer control — 31/10/2026

## Evidencia y decisión

Plan previo: research/plans/2026-10-31-gse122069-pilot.md. **La ejecución técnica del primer millón terminó correctamente y los dos parsers coinciden; el evento prefijado sigue sin ser evaluable por falta de cobertura.** No se amplió el subconjunto ni se calcularon razones, PSI, efectos, p-valores o inferencia biológica.

Única biblioteca: SRR8144907/SRX4965534/GSM3454242, grupo publicado siControl1, cultivoSH-SY5Y. El archivo comprimido completo,1.391.030.664bytes, coincide conMD5ENA90ad6a34a34e8262bf300d7bb35406e1. SHA256propio d3f57e023735d35261f9b0c2acb4d8034a859295ab12178375be352c7b7d6593. Selección: primer1.000.000registros en orden depositado; no muestra aleatoria, no biblioteca completa ni unidad biológica adicional por cada lectura.

| QC real | Resultado |
|---|---:|
| RegistrosFASTQ/primariosSAM | 1.000.000/1.000.000 |
| Lecturas alineadas | 965.822 (96,58%) |
| Alineadas a una ubicación reportada | 842.130 |
| Alineadas a más de una ubicación reportada | 123.692 |
| No alineadas | 34.178 |
| RegistrosSAM incluidos secundarios | 1.256.935 |
| Observaciones de intrón aceptadas, ancla15 | 54.054 |
| Observaciones de intrón aceptadas, ancla8 | 87.261 |
| CanónicaSTMN2 prefijada,15/8 | 0/0 |
| CrípticaSTMN2 prefijada,15/8 | 0/0 |

Los dos extractores coinciden tanto en soporte de los objetivos como en total de intrones yregistrosSAM. Un alto porcentaje global de alineamiento **no** acredita cobertura de una unión concreta. El mínimo prospectivo de20cuentas canónica+críptica no se alcanza en el subconjunto. Estos ceros son recuentos observados bajo los filtros, no imputación de muestras faltantes ni prueba de ausencia molecular.

## Métodos y controles

HISAT2v2.2.3 e índice fijados/verificados por hashes del trabajo previo. Antes de cuentas reales se parametrizaron ambos parsers: primaria≥15bases de anclaje y sensibilidad≥8, MAPQ≥20/excluye255, NH1, XS requerida para uniones, alineamientos primarios sinQCfail. Sin deduplicación arbitraria. Preflight sintético porflujo a15/8: concordancia total antes de analizarFASTQreal. Se conservan expectativas y resultados anteriores con8, incluida la asimetría de anclaje; no se reetiquetaron retrospectivamente.

Parámetros de alineamiento conservados:2hilos,-k5,--seed0,--no-temp-splicesite,--reorder, sinstrandness impuesta, dta o sitios de unión inyectados. CoordenadasGRCh38chr8+ invariables: canónica79611214→79636802 ycríptica79611214→79616822, límitesexónicos1-based. No-k1 para fabricar unicidad. NH describe ubicaciones reportadas, no búsqueda exhaustiva de toda alternativa posible.

Python alimenta el primer millón porgzip/pipes al mismo binario alineador, y elSAMse envía porpipes a parser textual propio yHTSlib/pysam0.23.3/HTSlib1.21. NoFASTQdescomprimido, SAM/BAMcompleto, IDs o secuencias reales exportados. Los histogramas ycuentas se limitan a accesiones/grupo publicado yvariables técnicas. Los datos originales permanecen en caché ignorada y se recuperan porURL/hash; no se incorporan aGit.

QCFASTQ:50.557.803bases,15.930N; longitudes35–51, con679.464lecturas de51nt y234.053de50nt. Se conserva el histograma completo, sin recortar automáticamente a los50bp nominales deGEO. ASCII de calidad35–74; media35,71 **si se interpretaPhred33**, como usa esta ejecución. No se presenta como validación independiente de codificación. ElQClee solo primer1M, no certificaCRCde todo elgzip; la integridad del archivo completo se coteja medianteMD5publicado ySHA256propio.

## Resultado negativo y diagnóstico acotado

El plan posterior research/plans/2026-10-31-gse122069-pilot-locus-qc.md fijó una nueva pregunta antes de reanalizar: ¿hay cobertura del locus/exonesaunque falten ambas uniones? Se ejecutó sobre **el mismo primer millón**, no otro subconjunto; dos pasadas no son2Mlecturas únicas ni dos réplicas.

Diagnóstico en reports/gse122069-pilot-locus-qc-20261031:628lecturas primarias únicasMAPQ≥20 solapan bloques del locusSTMN2,31solapanexon2 y0exon1. Hay48lecturas con las tres uniones posteriores conocidas, con18/18/12cuentas. El solapamiento no prueba por sí solo asignación inequívoca de expresión. Cuentas prefijadas ySAMQCson idénticos a los del piloto inicial. No se sustituyen los objetivos por esas uniones para obtener un positivo.

La limitación se localiza en la cobertura aceptada del primerexón/donante del evento dentro de este subconjunto. No se sabe todavía si se debe a mapeabilidad, isoforma, distribución de cobertura u otra propiedad técnica. No prueba pérdida biológica deSTMN2, fallo del mecanismo publicado o ausencia de launión en toda la biblioteca.

Comprobación dirigida de protocolo: ENASRX4965534 yGEOdeclaranIlluminaTruSeqRNAkit, nominal50bpSINGLE eHG38, conSTAR/RSEM como flujo original. El método publicado coincide en el kit. **No se acreditó un ensayo exclusivo3prime** con esas fuentes; tampoco se descarta un sesgo de cobertura por el nombre del kit. No se presenta la hipótesis3prime-only como explicación demostrada. Este pilotoHISAT2de1Mno reproduce íntegramente el flujoSTAR/RSEM deautores ni un contraste publicado.

## Recursos, errores y límites

La primera solicitudHTTPdel archivo completo se agotó con0bytes. La recuperación por83rangosHTTP206 exactos de16MiB,2conexiones yETagconstante completó el archivo en824,67s; el ensamblaje solo se aceptó trasMD5completo. Los parámetros demuestra/hipótesis no cambiaron por este fallback de transporte.

Un primer intento de pipeline terminóBrokenPipe sin resultadosSAMaceptados. El diagnóstico mostró que se excedía el límite conservador de disco global y que/proc/.../children no estaba disponible; la primera excepción no conservó la razón interna delwatchdog, por lo que no se afirma una traza causal exacta. Los logs/resultados fallidos se preservan enattempt1 y no se usan como cuentas. El0registrado allí paraRSSno es una medición válida de memoria.

Se eliminó solo la caché comprimida del índice creada en esta tarea (4,36GB), cuyo origen/hashpersisten; el índice extraído se verificó de nuevo porficheros. Con más50GB libres se reintentó usando el mismo ejecutable directo y los mismos parámetros, congzipPython y límitesvirtuales porproceso: alineador5GiB, padre512MiB yHTSlib256MiB, suma5,75GiB. La paridad con elwrapper se comprobó sobrecontroles sintéticos15/8 antes del reintento. No se finge mediciónRSScombinada; se conservan máximosrusageindividuales y límites explícitos, además de afinidad2CPUs,30min yguardiadisco/reserva8GiB.

Ejecución correcta:62,64s en total,24,14s de verificación/QCprevios; máximo hijo4.646.832KiB (~4,43GiB), padre31.360KiB yHTSlib31.360KiB. Son métricasporproceso yno un picoRSSagregado. El diagnóstico adicional tardó68,05s. No extrapolar linealmente este subconjunto a37,5Mlecturas o seisbibliotecas. La medición global de disco incluye posibles cambios compartidos del entorno, no se atribuye toda la variación a estos archivos.

Python3.12.14; **309pruebasoffline correctas** (301+8), compileall. CI debe verificarse por la nueva cabeza; no descargaENA ni ejecuta1Mlecturas. Los tests pruebanFASTQtruncado/calidad/bases inválidas, integridad, rangosHTTPincorrectos yseparación de políticas. Código final reproduce modo primario e incluyeinstrumentación opcional de locus; checkpoint anterior conserva el supervisor inicialmente fallido. Parámetros, hashes de código/entradas/salidas, excepciones ytablasTSVse preservan.

## Continuación

**No iniciar las otras cinco bibliotecas ni ampliar adaptativamente el piloto.** Única prueba siguiente: auditar mapeabilidad/definición del primerexón con referencia fijada ylecturas sintéticas50/51nt, sin cambiar las dos uniones prefijadas. Después decidir una fasecompleta de tamaño y recursos fijados antes de observarla; no detenerla o ampliarla según aparezcan cuentas. El contraste sigue bloqueado por cobertura/adecuación del evento.

Se amplía el mismoPR33 sin merge/cierre automático; PR30cabeza053ef70ce437cc637ec18278a2c07e3abd6bf58b ymain9c82795d intactos. Sin gastos, contactos, publicación externa, clínica personal o laboratorio. No validación funcional o beneficio clínico.

## Referencias

- GEO/ENA: GSM3454242,SRX4965534,SRR8144907,GSE122069. URL/fecha/hash y proyección técnica en el diagnóstico. https://www.ebi.ac.uk/ena/browser/api/xml/SRX4965534 y https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM3454242&targ=self&form=text&view=quick.
- Melamed,Z., López-Erauskin,J., Baughn,M.W., etal.(2019). Premature polyadenylation-mediated loss of stathmin-2 is a hallmark of TDP-43-dependent neurodegeneration. *NatureNeuroscience,22*,180–190. https://doi.org/10.1038/s41593-018-0293-z. MétodosRNAsequencing, https://pmc.ncbi.nlm.nih.gov/articles/PMC6348009/. Scite verificómetadatos, pero la consultaQuantSeqno devolvió pasaje relevante ni avisos editoriales completos; el protocolo se cotejó en fuentesprimarias. Sin nueva conclusión sobreel mecanismo.
