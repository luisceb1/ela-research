# Recuperar CTRL_R2 con plazos de reloj transcurrido

Conservar todos los intentos; navegador detenido según aceptación anterior. Fijar COMMIT_VERIFICADO trasCI.

```powershell
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto fetch origin research/2026-11-01-gse296714-design
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto checkout --detach COMMIT_VERIFICADO
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-research-piloto/scripts/recover_ctrl_r2_clock.py --prepare /home/luisceb/ela-control-r2-reloj-plan.json --original /home/luisceb/ela-piloto-real-01-index-recovery-01-extracted-01-reads-01-CTRL_R1-recovery-01-pilot-01-CTRL_R2-recovery-01-ipv4-01-final-01-resume-01
```

Preparar sólo lee metadatos y hashes locales y emite descriptor deshabilitado. Puede tardar comprobando la cadena; sinHTTP/copia/alineamiento. Esperado96550743B restantes/cargo7226257234B/final7322807977B/40min total30HTTP/CLOCK_BOOTTIME. Misma reserva de navegador, sin duplicarla. Código yboot_id fijados; si reiniciaWSL/elhost entreplan y ejecución, preparar un descriptor nuevo y no ejecutar el viejo.

Ejecutar sólo conSHA exacto y --accept-elapsed-clock-window. Puede automatizarse la comprobación de esos campos y el SHA de preparación enPowerShell antes de ejecutar, con aceptación expresa del bloque entero. No aumentar límites. No repetir si falla; devolver error/recibos. Si tiene éxito, el sello será sealed_verified_ctrl_r2_elapsed; no inicia alineamiento.
