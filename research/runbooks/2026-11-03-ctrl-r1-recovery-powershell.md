# Recuperación de CTRL_R1: PowerShell

Fijar COMMIT_VERIFICADO comunicado trasCI, conservando carpetas y plan anterior.

```powershell
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto fetch origin research/2026-11-01-gse296714-design
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto checkout --detach COMMIT_VERIFICADO
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-research-piloto/scripts/recover_ctrl_read.py --prepare /home/luisceb/ela-control-r1-recuperacion-plan.json --original /home/luisceb/ela-piloto-real-01-index-recovery-01-extracted-01-reads-01
```

Sólo audita y prepara, sinHTTP. Puede tardar calculandoSHA; tamaño debe coincidir con recibo354631727B. Devolver JSON/SHA oerror. No relanzar piloto ni editarledger. Raíz nueva termina en -reads-01-CTRL_R1-recovery-01 y admite un intento.

Después de revisar descriptor concreto, ejecutar requiere --execute, --accept-plan-sha256 exacto y --accept-additional-time-window. Propone40min totales/30min HTTP adicionales sin modificar ventana anterior. Recupera sóloCTRL_R1, MD5 completo obligatorio; no otros mates/alineamientos. Preparar no acepta tiempo ni inicia red.
