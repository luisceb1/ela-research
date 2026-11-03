# Auditoría local tras agotarse la reducción original

Pregunta, ventana exploratoria, objetivos/filtros y criterio de replay no cambian. El intento anterior agotó sus 300 s de reducción tras terminar HISAT2. Informe y evidencia: `reports/unc13a-audit-reduction-timeout-20261103/REPORT.md`.

Nuevo ejecutor `unc13a_locus_audit_v2.py`: guarda local en memoria, supervisor independiente y reducción 720 s dentro del mismo máximo de 2100 s. Conserva catorce árboles y todos los cargos/metadatos anteriores. No adopta el cómputo incompleto ni elimina archivos. Sin HTTP ni TDP.

Preparar `--prepare /home/luisceb/ela-unc13a-locus-guard-plan.json --control RAIZ_CONTROL_SELLADO`. Comprobar `execution_enabled=false`, `total_seconds=2100`, `reduction_seconds=720`, `guard_policy=in-memory-worker-independent-parent-v2`, `prefix_pairs=1000000`, `new_transfer_bytes=0`, `cumulative_body_bytes=7322807977`, `clock=CLOCK_BOOTTIME`, `gate_promoted=false` y SHA hexadecimal de 64 caracteres. Ejecutar el plan exacto con `--execute PLAN --accept-plan-sha256 SHA --accept-local-audit-window`. La nueva raíz termina en `-locus-audit-01-guard-02`. No repetir un intento.
