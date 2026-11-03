# Continuación con CTRL_R1 recuperado: PowerShell

Fijar COMMIT_VERIFICADO comunicado trasCI. No mover/borrar archivos oparciales anteriores.

```powershell
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto fetch origin research/2026-11-01-gse296714-design
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto checkout --detach COMMIT_VERIFICADO
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-research-piloto/scripts/recovered_read_pilot.py --prepare /home/luisceb/ela-piloto-continuacion-plan.json --recovery /home/luisceb/ela-piloto-real-01-index-recovery-01-extracted-01-reads-01-CTRL_R1-recovery-01
```

Sólo metadatos yplan deshabilitado, sinHTTP/copia/alineamiento. DevolverJSON/SHA oerror. Nueva raíz derivada termina en -CTRL_R1-recovery-01-pilot-01; no admite reejecución.

Después de revisar plan concreto, requiere --execute, --accept-plan-sha256 exacto y --accept-new-window-and-disk. Propone7200s nuevos/1800s acumulados de transferencias(incluye copia local), disco27GiB frente25anteriores yartefactos18GiB frente16, para conservar todos los parciales y copia verificada. Techo12GB deHTTP acumulado intacto y cargos viejos incluidos. Ninguna aceptación por preparar.

CTRL_R1 eíndice no se vuelven a descargar; sóloCTRL_R2 y luegoTDP condicionado a cobertura delcontrol. Mantener equipo encendido yterminal abierta durante ejecución aceptada. DevolverJSON/errorfinal sinrepetir comandos deejecución.
