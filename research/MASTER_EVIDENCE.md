# Registro maestro de evidencia ELA — v0.1 (2026-10-29)

Este inventario distingue **resultados comunicados en análisis previos** de resultados **reproducidos desde este repositorio**. No atribuir validación independiente a un resultado hasta ejecutar aquí su código sobre sus datos y auditar los outputs.

| ID | Línea | Fuente | Observación previa / objetivo | Estado de reproducción en repositorio |
|---|---|---|---|---|
| ELA-01 | GSE126542 expresión | Núcleos corticales, 7 pares TDP-43 nuclear +/- | STMN2 -51,5% con median-of-ratios, descenso en 7/7; UNC13A ARN nuclear total +41,8%; TARDBP no consistente | **PENDIENTE** importar código, recuentos y reejecutar |
| ELA-02 | GSE126542 uniones | Datos secundarios publicados por Fratta | Cuantificación de uniones crípticas STMN2/UNC13A; inspeccionar deduplicación y denominadores | **PENDIENTE** auditar original, script, uniones y PSI |
| ELA-03 | GSE121569 expresión | Motoneuronas cultivadas siTDP43 / siScr | STMN2 -55,1%; UNC13A -9,2%; TARDBP -59,8%; dos diferenciaciones, no seis réplicas biológicas | **PENDIENTE** reejecutar y auditar pseudorreplicación |
| ELA-04 | GSE126542 genética | Paquete de análisis previo | Hipótesis exploratoria; no se afirma un hallazgo hasta inspección | **PENDIENTE** recuperar artefactos |
| ELA-05 | CAMK2B | Paquete de validación independiente previo | Resultado y controles no verificados en GitHub | **PENDIENTE** recuperar artefactos |
| ELA-06 | Péptidos crípticos | Paquete de cribado previo | Solo candidatos exploratorios, sin prueba proteómica | **PENDIENTE** recuperar artefactos |
| ELA-07 | UNC13A MEA | Simulador y sensibilidad previos | Diferenciar recuperación, protección y ausencia de efecto; efectos supuestos, no medidos | **PENDIENTE** importar simulador y pruebas |
| ELA-08 | GSE310723 Iso-Seq | GEO, i3N 4 condiciones | 392871 filas de transcritos en uniqueCounts; inventario estructural | **ESTRUCTURA VERIFICADA**; bio-QC y mapping pendientes |
| ELA-09 | GSE315972 Iso-Seq | GEO, tejido humano 8 columnas | 401720 filas de transcritos; grupos clínicos no confirmados | **ESTRUCTURA VERIFICADA**; bio-QC y mapping pendientes |
| ELA-10 | Rescate STMN2/UNC13A | Propuestas para colaboración | Intervención posterior a déficit; dianas moleculares y medidas funcionales | **PROPUESTA**, no prueba experimental |

## Interpretación obligatoria
- Reproducción descriptiva de hechos ya publicados NO equivale a descubrimiento nuevo.
- ARN total ≠ isoforma funcional ≠ proteína ≠ recuperación de actividad neuronal ≠ beneficio clínico.
- Los porcentajes ELA-01/03 son observaciones de análisis anteriores, **no verificadas aquí**.
- Las simulaciones UNC13A MEA no aportan eficacia biológica.
- El repositorio no almacena información personal de pacientes ni sugiere tratamientos.
- Para promover estado: script + fuente verificable (GSE/GSM) + hash + tests + tablas + sensibilidad + revisión.

## Próximo ciclo
1. Ejecutar auditoría de GTF y correspondencia TXNAME/GENEID (Issue #2) tras metadatos y QC (Issue #1).
2. Importar paquetes originales de análisis previo, preservar artefactos y registrar hashes antes de reproducirlos.
3. Auditar originalidad con fuentes primarias; jerarquizar candidatos por evidencia, no por novedad aparente.
4. Presentar a laboratorio una sola hipótesis falsable con controles y endpoints predefinidos.
