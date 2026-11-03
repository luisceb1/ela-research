# Preparación tras corregir la clasificación de temporales

El intento v2 falló al preparar, sin crear plan aceptado ni raíz de ejecución. Se corrige la clasificación de temporales antiguos, no las cuotas. Evidencia y límites en `reports/unc13a-audit-disk-accounting-20261103/REPORT.md`.

Usar el commit verificado comunicado, `scripts/unc13a_locus_audit_v2.py` y un plan nuevo `/home/luisceb/ela-unc13a-locus-guard-disk-plan.json`. `--control` sigue apuntando al control sellado. Preparar imprime `disk_policy=cumulative-audit-partitions-v1` y `disk_used_bytes`, además de ventana 2100 s, reducción 720 s, prefijo 1.000.000, cargo 7.322.807.977 y cero bytes nuevos. Exigir SHA exacto, guard_policy `in-memory-worker-independent-parent-v2`, clock CLOCK_BOOTTIME, ejecución deshabilitada y gate_promoted false.

Pegar todo el bloque PowerShell comunicado, contenido en `& { ... }`; las comprobaciones de fallo y ejecución deben estar dentro de las mismas llaves. Esto impide que un error de preparación continúe hasta un comando con SHA vacío. Mantener terminal abierta y equipo sin suspensión. No repetir raíces ni borrar archivos. Si falla, devolver el error completo.
