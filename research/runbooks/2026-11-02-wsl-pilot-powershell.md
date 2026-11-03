# Piloto UNC13A en Windows desde PowerShell

> Actualización: la ejecución `ela-piloto-real-01` alcanzó el límite de transporte
> durante el índice. No repetir pasos4–5para esa ejecución ni emitir otro plan
> para reiniciar presupuestos. Conservarla intacta y usar primero
> `scripts/inspect_interrupted_pilot.py --root /home/luisceb/ela-piloto-real-01`.
> La versión nueva optimiza sincronizaciones, pero NOreanuda trabajos antiguos.
> Tras auditoría, consultar `2026-11-02-index-recovery-powershell.md`: recuperación
> separada solo delíndice y nueva ventana de tiempo pendiente de aceptación.


02/11/2026. Preparación revisable; no ejecución biológica realizada por esta entrega.
No requiere Cursor, GPU, dominio, puertos abiertos o servicio web.

## Equipo observado por Luis

Windows ~15,8 GiB RAM física, C: ~613,2 GiB libres. Ubuntu24.04 en WSL2:
7,6 GiB RAM total /7,1 GiB disponible, x86_64, Python3.12.3, PySAM0.23.3.
Las201pruebas del commit6a3ec780 pasaron sin omisiones en su equipo.
Son salidas aportadas por Luis, no acceso remoto nuestro a su ordenador.

## 1. Actualizar la copia de Ubuntu

Ejecutar desde PowerShell, con prompt `PS ...>`. No hace falta entrar en Ubuntu.
No modifica la copia de C:\Users\Luis\ela-research ni fusiona la PR.
Para reproducción exacta, utilizar el SHA comunicado en el chat en lugar de
FETCH_HEAD. Si hay cambios locales, detenerse; nunca reset --hard/--force.

```powershell
wsl -d Ubuntu-24.04 -- bash -lc 'cd ~/proyectos/ela-research-piloto && git fetch origin research/2026-11-01-gse296714-design && git checkout --detach FETCH_HEAD'
```

## 2. Instalar HISAT2 desde la fuente fijada

La instalación de herramientas es previa al presupuesto de9000s/12GBdel piloto.
No descarga genoma humano, FASTQbiológico o secuencias de pacientes. Se observa
el checkout y se fijan hashes de los binarios locales; esto no es una compilación
reproducible bit a bit ni una atestación de que el compilador sea fiable.

```powershell
wsl -d Ubuntu-24.04 -- sudo apt-get install -y build-essential git
```

```powershell
wsl -d Ubuntu-24.04 -- bash -lc 'mkdir -p ~/ela-tools && git clone --depth 1 --branch v2.2.3 https://github.com/DaehwanKimLab/hisat2.git ~/ela-tools/hisat2-2.2.3'
```

Comprobar que imprime exactamente el commit siguiente:

```powershell
wsl -d Ubuntu-24.04 -- bash -lc 'cd ~/ela-tools/hisat2-2.2.3 && git rev-parse HEAD'
```

`0d244324f98de541bce04d45c75e83bc3522f7f4`

Compilar ambos binarios con2trabajos. Puede tardar varios minutos:

```powershell
wsl -d Ubuntu-24.04 -- make -C /home/luisceb/ela-tools/hisat2-2.2.3 -j2 hisat2-align-s hisat2-inspect-s
```

```powershell
wsl -d Ubuntu-24.04 -- bash -lc '~/ela-tools/hisat2-2.2.3/hisat2-align-s --version && sha256sum ~/ela-tools/hisat2-2.2.3/hisat2-align-s ~/ela-tools/hisat2-2.2.3/hisat2-inspect-s'
```

Si la carpeta ya existe de un intento anterior, no clonarla encima: conservarla y
comprobar su commit/estado antes de seguir. No cambiar a una versión apt distinta.

## 3. Pruebas nuevas y diagnóstico local

No es necesario repetir ahora las201históricas para instalar herramientas. Estas
20pruebas nuevas usan productores sustitutos y datos sintéticos, no HISAT2real:

```powershell
wsl -d Ubuntu-24.04 -- bash -lc 'cd ~/proyectos/ela-research-piloto && .venv/bin/python -m unittest discover -s tests -p test_real_pilot_workflow.py -v'
```

```powershell
wsl -d Ubuntu-24.04 -- bash -lc 'cd ~/proyectos/ela-research-piloto && .venv/bin/python scripts/real_pilot_workflow.py --host'
```

## 4. Emitir la configuración sin ejecutar

Crea un archivo nuevo de configuración y muestra su SHA256. Si ya existe, falla;
no lo sobrescribe. El directorio de ejecución también deberá ser nuevo.

```powershell
wsl -d Ubuntu-24.04 -- bash -lc 'cd ~/proyectos/ela-research-piloto && .venv/bin/python scripts/real_pilot_workflow.py --prepare ~/ela-piloto-plan.json --root ~/ela-piloto-real-01 --aligner ~/ela-tools/hisat2-2.2.3/hisat2-align-s'
```

El resultado debe indicar execution_enabled=false y raw_execution_ready=false.
Pasa al chat la versión deHISAT2, el diagnóstico y el resumen con elSHA256.
La preparación verifica checkout fuente limpio, hashes locales y recursos; la
versión ejecutable se vuelve a comprobar dentro de la fase supervisada anterior
a toda descarga. El archivo contiene rutas/configuración técnica, no credenciales.

## 5. Activación posterior, solo tras revisar el archivo

Este comando está documentado para revisión; no forma parte de los pasos1–4.
Consume el índice y las lecturas públicas. Requiere una decisión expresa del
operador y el SHA256exacto obtenido en el paso4, no una bandera en el código.
No ejecutar aún copiando un SHA de ejemplo.

```text
wsl -d Ubuntu-24.04 -- bash -lc 'cd ~/proyectos/ela-research-piloto && .venv/bin/python scripts/real_pilot_workflow.py --execute ~/ela-piloto-plan.json --accept-plan-sha256 SHA256_REAL_REVISADO'
```

Secuencia: preflight→índice4,36GB→extracción exacta→inspectorresumenchr19→
CTRLdosmates1,96GB→EOF/CRC/prefijo1M→descompresiónacotada→alineamiento/conteo→
solo si hay cobertura suficiente, TDPdosmates4,39GB→prefijo1M→alineamiento/conteo.
Un mínimo de20grupos aceptados con soporte aobjetivo a15bases es condición técnica;
seis grupos del fixture no lo cumplen. No ampliar ante insuficiencia.

Caps propuestos:2CPU;9000stotales;3600stransferencias acumuladas;12.000.000.000bytes
de cuerpoHTTP;25GiBadicionales+8GiBreserva;6GiBRSSgrupo muestreado/8GiBASproceso.
Índiceprobe añade120sa la envolvente previa:8640s,360ssin asignar, mismo capglobal.
Temporales6GiB:2GiBdescompresión+4GiBcolación. No SAMcompleto ni ejecución clínica.
Los tiempos son límites de parada, no estimaciones de duración ni benchmarks.

## Parada y conservación

Ctrl+Cinterrumpe el padre; el supervisor intenta terminar el grupo y registra el
fallo. No cerrar WSL a la fuerza para simular una finalización correcta. Si muere
el supervisor o Windows, no hay garantía de limpieza: conservar todo y revisar.
Un trabajo fallido/interrumpido no se reanuda automáticamente ni se adopta por
haber archivos aparentemente completos. No borrar ledger, recibos o parciales.
No volver a iniciar en otra carpeta para eludir un presupuesto fallido.

La revalidación del resultado usa el plazo original y no descarga. Fuera de plazo
se necesita un nuevo plan de auditoría; no se extiende el reloj automáticamente.

```text
wsl -d Ubuntu-24.04 -- bash -lc 'cd ~/proyectos/ela-research-piloto && .venv/bin/python scripts/real_pilot_workflow.py --verify ~/ela-piloto-real-01'
```

## Límites de interpretación

Dos bibliotecas técnicas, no réplicas/grupos comparables acreditados. No PSI,
p-valores, efecto de TDP43, rescate funcional o beneficio clínico. Concordancia
texto/HTSlib acredita decodificaciónCIGAR, con selección/reducción compartidas.
La inspección del índice comprueba resumen/nombre/longitudchr19, no igualdad de
toda la secuencia. Su SHA256lo liga al archivo histórico ya inspeccionado.
EOF/CRCcompleto y hashes cuestan tiempo sobre las fuentes enteras, aunque solo
se alinee el primer millón. RSS/disco muestreados no son cuotas duras delkernel.
HTTPcuenta cuerpo leído, noTLS/TCP/cabeceras/buffering. No retriesautomáticos.
