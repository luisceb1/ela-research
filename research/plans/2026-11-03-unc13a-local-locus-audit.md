# Auditoría local exploratoria del locus UNC13A

Especificación prospectiva, controles, criterio de fracaso, recursos e interpretación: `reports/ctrl-local-locus-audit-20261103/REPORT.md`.

Se parte del control sellado con cobertura insuficiente (1/20). Usar el mismo prefijo certificado de un millón de pares y los objetivos originales; inventariar ambas hebras en chr19:[17600000,17690000), anclajes 15 y 8, y desplazamientos de hasta dos bases. Comparar conteos/QC completos con el original como control de replay. Conservar la puerta cerrada, sin TDP, PSI ni conclusión biológica.

Preparar con `scripts/unc13a_locus_audit.py --prepare /home/luisceb/ela-unc13a-locus-plan.json --control RAIZ_CONTROL_SELLADO`.

Comprobar SHA hexadecimal de 64 caracteres, `execution_enabled=false`, `total_seconds=2100`, `prefix_pairs=1000000`, `new_transfer_bytes=0`, `cumulative_body_bytes=7322807977`, `clock=CLOCK_BOOTTIME` y `gate_promoted=false`. Ejecutar el plan exacto con `--execute PLAN --accept-plan-sha256 SHA --accept-local-audit-window`. Root exclusivo con sufijo `-locus-audit-01`; no volver a intentar un root usado. Ante error, conservar todos los recibos.
