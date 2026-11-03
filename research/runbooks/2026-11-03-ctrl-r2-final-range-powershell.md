# Preparar el tramo restante de CTRL_R2

Usar el COMMIT_VERIFICADO comunicado tras CI; conservar todas las carpetas y planes anteriores.

```powershell
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto fetch origin research/2026-11-01-gse296714-design
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto checkout --detach COMMIT_VERIFICADO
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-research-piloto/scripts/recover_ctrl_r2_final.py --prepare /home/luisceb/ela-control-r2-tramo-final-plan.json --original /home/luisceb/ela-piloto-real-01-index-recovery-01-extracted-01-reads-01-CTRL_R1-recovery-01-pilot-01-CTRL_R2-recovery-01-ipv4-01
```

Sólo lectura de metadatos y hashes locales y plan deshabilitado; sin HTTP, copia, descompresión o alineamiento. Devolver JSON/SHA o error. Puede tardar mientras calcula los hashes; no repetir si el plan existe.

Propuesta nueva de40min totales/30min HTTP, copia y verificación5min cada una. Mismo límite27GiB/reserva8GiB,35GiB libres al iniciar. Cargo inicial6.199.347.649B conservado, tramo121.270.068B. IPv4/TLS verificado, una petición y MD5 entero antes de sello. Preparar no acepta la ventana.

Después de revisar el SHA concreto, ejecutar requiere --execute, --accept-plan-sha256 y --accept-additional-time-window. Si falla, conservar todo y no repetir. No volver a lanzar los planes fallidos ni editar sus ledgers. El éxito conserva el tipo de sello `sealed_verified_ctrl_r2_ipv4`; la raíz y el plan identifican este tramo. No inicia automáticamente el piloto.
