# Recuperar únicamente CTRL_R2

Fijar el COMMIT_VERIFICADO comunicado después de CI. Conservar todos los originales.

```powershell
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto fetch origin research/2026-11-01-gse296714-design
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto checkout --detach COMMIT_VERIFICADO
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-research-piloto/scripts/recover_ctrl_r2.py --prepare /home/luisceb/ela-control-r2-recuperacion-plan.json --original /home/luisceb/ela-piloto-real-01-index-recovery-01-extracted-01-reads-01-CTRL_R1-recovery-01-pilot-01
```

Sólo audita metadatos/hash del parcial y prepara un descriptor deshabilitado; sin HTTP, copia, extracción o alineamiento. Devolver JSON/SHA o error. No repetir prepare si el archivo de plan ya existe.

Propuesta: 100 minutos totales, 90 de HTTP adicional, mismo disco27GiB y reserva8GiB; requiere35GiB libres al iniciar. Sólo712.749.730 B restantes, cargo anterior5.603.756.481 B sin reembolso. Arrastra conservadoramente la ventana anterior completa; tiempos y archivos históricos no se editan.

Después de revisar el SHA concreto, ejecutar requiere --execute, --accept-plan-sha256 y --accept-additional-time-window. No se autoriza por preparar. Una sola petición Range y MD5 entero antes del sello. Si falla, conservar todo y no repetir execute. No hay alineamiento ni reinicio automático del piloto.
