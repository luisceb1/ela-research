# Continuar desde el parcial más avanzado

Cancelar primero la descarga del navegador; conservar carpetas y planes. Fijar COMMIT_VERIFICADO comunicado tras CI.

```powershell
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto fetch origin research/2026-11-01-gse296714-design
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto checkout --detach COMMIT_VERIFICADO
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-research-piloto/scripts/recover_ctrl_r2_resume.py --prepare /home/luisceb/ela-control-r2-continuacion-plan.json --original /home/luisceb/ela-piloto-real-01-index-recovery-01-extracted-01-reads-01-CTRL_R1-recovery-01-pilot-01-CTRL_R2-recovery-01-ipv4-01-final-01
```

Sólo metadatos/hashes locales y plan deshabilitado; sin descarga o alineamiento. Devolver JSON/SHA. Propuesta40min total/30HTTP; quedan97174406B; mismos27GiB/reserva8GiB y35GiB libres previos.

Distingue cargoWSL6224513473B de reserva para navegador997549457B. Luis indicó74MB aproximados; la reserva de un archivo completo no es tráfico medido y no certifica retries externos. Se arrastra la ventana interrumpida completa, sin inventar instante final.

Tras revisar plan, ejecutar requiere --execute, --accept-plan-sha256, --accept-additional-time-window y --accept-browser-stopped-and-manual-reserve. Preparar no acepta esas condiciones. No repetir ejecuciones o editar ledgers. Sólo se recuperaR2 y verificaMD5entero; no reinicia piloto.
