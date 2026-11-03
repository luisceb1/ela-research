# Piloto con índice local: PowerShell

Actualizar la rama y fijar el commit aprobado tras comprobar CI. Todos los comandos se ejecutan desde PowerShell; sustituir COMMIT_VERIFICADO por el SHA comunicado.

```powershell
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto fetch origin research/2026-11-01-gse296714-design
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto checkout --detach COMMIT_VERIFICADO
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-research-piloto/scripts/cached_index_pilot.py --prepare /home/luisceb/ela-piloto-lecturas-plan.json --index /home/luisceb/ela-piloto-real-01-index-recovery-01-extracted-01
```

Devuelve descriptor deshabilitado y SHA. No inicia HTTP, extracción ni alineamiento. Root nuevo derivado termina en -extracted-01-reads-01; no reutilizar raíces interrumpidas. No editar el ledger ni relanzar real_pilot_workflow.py con el plan viejo.

Después de revisar el plan concreto, la ejecución requiere --execute, --accept-plan-sha256 con su SHA y --accept-new-run-window. La ventana propuesta es nueva: 7.200 s totales y 1.800 s adicionales de transferencia; preserva el cargo anterior y el tiempo histórico. No hay aceptación de esta ventana por el mero acto de preparar el plan. Véase reports/cached-index-pilot-20261102/execution-proposal.json.
