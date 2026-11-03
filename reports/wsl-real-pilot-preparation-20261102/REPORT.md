# Preparación del piloto real en WSL — 02/11/2026

Base: PR36,6a3ec780adcc6a55548bf8d1999a5718f10d7bfd.
Plan previo: research/plans/2026-11-02-wsl-real-pilot-preparation.md.
Resultado: candidato ejecutable bajo aceptación expresa del archivo preparado;
ninguna descarga biológica o alineamiento humano ejecutados en esta entrega.

## Evidencia

222tests seleccionados pasan sin fallos/errores/omisiones:201anteriores,
20nuevos de preparación/adaptador y1regresión de identidad del supervisor.
CPython3.12.14/PySAM0.23.3, compileallcorrecto. validation.json/tests.txt.
Las20pruebas nuevas no alinean: usan binariosPythonrenombrados para negativos de
versión y productor sustituido que emite SAMhistórico para probar el adaptador.
Positivo de9pares produce6grupos objetivo, insuficiente al umbral20, y retira
los prefijos planos. No afirmación de mapeo real o tasa biológica.

Control adicional de CLIreal/worker/supervisor, no incluido como testúnico:
acepta archivo preparado exacto, conserva sus bytes aun con JSONno canónico y
lanza workerfijo. BinarioPythonELFrenombrado deliberadamente falla la prueba de
versión. Solo preflightfailed,0bytes transferidos, exitexterno1,grupo sin vivos,
sinsello. blocked-worker-smoke.json/.log. No se inyecta un exitcomo si fuera real.

El usuario aportó desde su equipo:201tests pasaban en6a3ec780, WSLUbuntu24.04,
Python3.12.3/PySAM0.23.3, RAMfísica15,8GiB, WSL7,6GiB/7,1disponible y discoC:
613,2GiBlibres. user-reported-environment.json conserva procedencia. environment.json
es OTROhost, el de trabajo del agente; no confundirlos ni atribuir instalaciones.

## Cambio de ejecución

- Nuevo real_pilot_workflow.py independiente del CLI sintético: --host y --prepare
  no acceden aENA/S3 o ejecutan alineamientos. --prepareobserva checkoutgitlimpio,
  fija2binariosELF/hashes/commit y código/Python/decoder, exige recursos y emite
  archivo nuevo deshabilitado. No sobrescribe plan o directorio de ejecución.
- Manifiesto reconstruido exactamente desde2fuentes pinadas porSHA256. Solo
  SRR33425816/819, cincoURLs fijadas con tamaño/checksum, orígenesHTTPSexactos,
  sinredirect/proxy/reintentoautomático. Cambios de muestras/caps/argv/orígenes
  fallan. Política real solo con opt-in explícito de runner; el sintético larechaza.
- --executerequiereSHA256delarchivo preparado aceptado poroperador antes de
  crearroot/descargar; no es firma de seguridad ni aprobación científica.
  Workerexige recibo.started delgrupoactual y archivo de aceptacióncoherente.
  Supervisor publica identidadprocfsantes de empezar la fase.
- Secuencia fija: versión2.2.3→índice→extracciónhash/EOF/CRC/inventario→
  inspect-s -sconchr19/58617616→CTRLmates/prefijo/cómputo→solo si cobertura
  adecuada,TDPmates/prefijo/cómputo. Rechazo delíndiceantes de FASTQreales.
- Se corrige el diseño de gzipdirecto albinario: documentación HISAT2yfuente
  v2.2.3asignan compresión alwrapper. Se evita introducir elshellinternodelwrapper:
  se descomprimen prefijos verificadosaFASTQregular bajo cap2GiB; binariofijo
  recibe archivos planos. Rehashantes/después, CRCycap, sin SAMcompleto en disco.
  Plaintextretirado traséxito; fallos conservan evidencia y no se reanudan.
-2GiBplaintext+4GiBcolación sustituyen6GiBcolación dentro de la misma partición.
  Probeíndice120susa120de480sde margen:envolvente8640/global9000, quedan360.
  Resto intacto:2CPU,3600stransporte,12GBcuerpoHTTP,25GiBdisco+8GiBreserva,
 6GiBRSSmuestreado/8GiBASporproceso. Stopcaps, no benchmarks.
- Sellado externo y revalidación usan recibos/ledger/entradas sin extenderplazo.
  Una fase incompleta o cobertura<20bloquea cualquier siguiente fase. Sello no
  certifica un efecto: puede registrar coverage_insufficient.

## Interpretación

Se ha preparado la ruta y probado contratos/fallos. No se ha acreditado aún su
rendimiento con el índicehumano en el ordenador deLuis. El CLIrequiere una
acción expresa deejecución futura; pasar tests o preparar JSONno la realiza.
La bandera del módulo sintético continúa False. El esquema real declara caps
para un plan potencial, no habilita el antiguo CLI o descarga al importarlo.

No PSI,p-valores,efectosdegrupo,réplicas nuevas,rescate funcional obeneficio
clínico. Las dos bibliotecas seleccionadas prueban viabilidad técnica; no
representan un contraste biológico acreditado. Fuente/selección previas intactas.

## Limitaciones y siguiente paso

Instalar/compilaraligner+inspector en el equipo deLuis, ejecutar20tests nuevos,
emitir configuración y revisar rutas/hashes/diagnóstico/SHA. Solo entonces
aceptación expresa para elpiloto acotado. RunbookPowerShellentregado enresearch/runbooks.
No descargamos ni restauramos índice/FASTQhumanos, no alineamos ni fusionamos.

La extracción falla conservadoramente si eltarreal usa un dialecto noadmitido;
no se relaja elparser sobre lamarcha. Elinspectorresumencomprueba nombre/longitud,
no igualdad íntegradelsecuenciado; hashes enlazan índicehistórico. Alinear y
rehashear entradas enteras puede agotar eltiempo; el ensayo aún no lo mide.
RSS/disco muestreados no son cuotas duras o garantías de tiempo real. Heredados
límites de grupos que se desacoplan, I/Oininterrumpible, muerte delsupervisor y
hosthostil. Ctrl+Cproduce intento de limpieza, no recuperación garantizada tras
apagarWindows/WSL. Instalación deherramientas previa tiene recursos separados.
Elcheckoutfuente observado y hasheslocales no prueban un build bit a bit ni
protegen de un compilador/binario malicioso concontrol delhost.

## Fuentes verificadas

- Tagv2.2.3oficial→0d244324f98de541bce04d45c75e83bc3522f7f4:
  https://api.github.com/repos/DaehwanKimLab/hisat2/git/ref/tags/v2.2.3
- Manualoficial, compresiónenwrapper:
  https://daehwankimlab.github.io/hisat2/manual/
- Fuente local pinada: hisat2, cat_file/wrapInput; hisat2_inspect.cpp,
  print_index_summary. Sin descargar fuentes/índice adicionales en estaentrega.
- Manifiestos fuente: reports/pilot-readiness-audit-20261102/execution-proposal.json
  y reports/unc13a-reference-strand-20261102/contract.json, SHA256enSOURCESdelCLI.
