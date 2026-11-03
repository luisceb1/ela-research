# Preparar recuperación IPv4 de CTRL_R2

Usar el COMMIT_VERIFICADO comunicado tras CI. No editar ni borrar planes/archivos anteriores.

```powershell
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto fetch origin research/2026-11-01-gse296714-design
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto checkout --detach COMMIT_VERIFICADO
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-research-piloto/scripts/recover_ctrl_r2_ipv4.py --prepare /home/luisceb/ela-control-r2-ipv4-plan.json --original /home/luisceb/ela-piloto-real-01-index-recovery-01-extracted-01-reads-01-CTRL_R1-recovery-01-pilot-01-CTRL_R2-recovery-01
```

Sólo audita intentos anteriores y hashes locales y emite plan deshabilitado. Sin red, copia o alineamiento. Devolver JSON/SHA oerror; no repetir si existe plan.

Propuesta6000s/5400sHTTP (100/90min), mismos27GiB contandoochoárboles/reserva8GiB. Conserva5.603.756.481Bcargados y tiempoTLSfallido. Una peticiónIPv4/TLSverificado para712.749.730B restantes; MD5entero antesdesello. No desactiva certificados ni cambia DNS global, redWSL o identidades históricas.

Después de revisarSHA concreto, ejecutar con --execute, --accept-plan-sha256 y --accept-additional-time-window. Preparar no acepta ventana nueva. Si falla, conservarcarpeta y no repetir. No otrosmates ni reinicio delpiloto.
