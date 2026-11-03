# Ejecutar sólo el control local

Usar el commit verificado comunicado tras CI y conservar todos los originales.

Preparar con `scripts/offline_control_pilot.py --prepare /home/luisceb/ela-control-local-plan.json --recovery RAIZ_R2_SELLADO`. La preparación sólo consulta metadatos, tamaños y recursos; no copia, descomprime ni alinea.

Comprobar estos campos antes de ejecutar:

| Campo | Valor |
|---|---|
| new_transfer_bytes | 0 |
| prior_charged_body_bytes | 7322807977 |
| total_seconds | 3000 |
| prefix_pairs | 1000000 |
| minimum_fragment_union | 20 |
| clock | CLOCK_BOOTTIME |
| sha256 | 64 caracteres hexadecimales |

Ejecutar con `--execute PLAN --accept-plan-sha256 SHA --accept-offline-control-window`. El bloque PowerShell comunicado comprueba automáticamente estos campos antes de aceptar la ventana local de 50 minutos.

Límites: 2 CPU, RSS de grupo de 6 GiB muestreada, espacio virtual por proceso de 8 GiB; disco de 27 GiB y reserva de 8 GiB. Preflight requiere 35 GiB libres y 6 GiB de RAM disponible bajo un techo de al menos 7 GiB. No aumenta automáticamente la memoria WSL.

Mantener la terminal abierta y el equipo sin suspensión. La raíz nueva termina en `-clock-01-control-01` y no admite repetir intentos. Resultado: `sealed_offline_control_pilot`, con `coverage_adequate` o `coverage_insufficient`. Ambos pueden indicar ejecución técnica completa. La insuficiencia no prueba ausencia biológica. Devolver el JSON final o el error; si falla, conservar todo y no repetir el bloque.
