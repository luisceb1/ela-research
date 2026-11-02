# Recuperar únicamente el archivo de índice desde PowerShell

Propuesta02/11/2026. Elparcial37,48%está identificado porSHA256, aún noverificado
como partecorrecta delíndice hasta comprobar elarchivoentero. Elintento anterior
queda intacto y conserva16384Bcargados que no llegaron alarchivo. No reembolsarlos.

## Alcance y revisión de tiempo

Una petición de2.723.339.065bytes restantes, mismaURLversionada delíndice.
HTTP206/Content-Range/Content-Length/versionIDexactos; cualquier200/redirect/
truncamiento/checksumincorrecto se rechaza. Sinretry. Elparcial seCOPIAauna
carpeta nueva yúnica, no seconcatena sobre laejecución original. Solo elSHA256
delarchivoentero permite promoción; aceptaciónexternadelgrupo permite elsello.

Se propone NUEVAventana de40min:5minaudit/copia,30mintransporte,5minverificación.
Son stopcaps, no duraciónestimada. La hora de transporte anterior está agotada;
esta ampliación necesita aceptación expresa y no cambia eldeadline viejo. Cap
bytes original12GBsin aumento, contando cargo anterior; traséxito4.355.802.733B
cargados y7.644.197.267Bde saldo. Discooriginal+nuevo≤25GiB, reserva8GiB;
2CPU,512MiBRSSmuestreado/1GiBASporproceso. Noextraeíndice, noFASTQ/alineamiento.

## Preparar sin descargar

Actualizar al commit comunicado enelchat; laejecución01yplananterior no se editan.
Después ejecutardesdePowerShell:

```powershell
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-research-piloto/scripts/recover_index_range.py --prepare /home/luisceb/ela-indice-recuperacion-plan.json --original /home/luisceb/ela-piloto-real-01
```

Muestra SHA256delplan,execution_enabled=false,2.723.339.065bytes restantes y caps.
No descarga, altera datos o acepta elnuevo presupuesto de tiempo. Devolver resumen
alchatpara revisión. No sobrescribir archivo existente; no crearintentos sucesivos.

## Ejecutar después de revisión y aceptación explícita del nuevo tiempo

Plantilla documental, no ejecutar con el textoSHA256_REAL_REVISADO:

```text
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-research-piloto/scripts/recover_index_range.py --execute /home/luisceb/ela-indice-recuperacion-plan.json --accept-plan-sha256 SHA256_REAL_REVISADO --accept-additional-time-window
```

La segunda bandera acepta expresamente esos40minadicionales/30mintransporte;
no es una renovación automática. Elrootfijoes
/home/luisceb/ela-piloto-real-01-index-recovery-01. Si existe, falla: no sobrescribe,
reanuda, adopta o cambia aotracarpeta. Antefallo conservar ambosárboles/recibos y
no reejecutar. Antesdeléxitoelsambladoesrecovered-index.partial; soloSHAcorrecto
permitehg38_genome.tar.gz. Soloexternofinished/exit0/sinviolación/grupovacío
permiterecovery-seal.json. Unarchivosinsello no se adopta por estarcompleto.

No reenviar laejecuciónvieja con--execute ni copiar esteíndice alrunneranterior
sin unprocedimientodeadopciónrevisado. Laextracción/piloto posterior necesitará
configuración que reconozca estosrecibos/cargos; no estáhabilitado porelrestore.

## Límites

PruebasHTTPloopbacksintéticas no acreditan queS3respondarácomo seexige o eltiempo
real. GuardasRSS/disco sonmuestreadas, no cuotasduras ni garantíadetiemporeal.
PresupuestoHTTPcuentacuerpoleído, noTLS/TCP/cabeceras/buffering. MuerteWSL/Windows,
I/Oininterrumpible, procesosdesacopladosohosthostil siguenfuera delas garantías.
Elhashpinado verificaarchivo, no biología. Ningúnresultado de este paso es PSI,
efectodegrupo,rescate o hallazgo clínico.
