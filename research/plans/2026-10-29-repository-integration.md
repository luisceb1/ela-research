# Plan de consolidación del repositorio

Autorización: Luis acepta revisar e integrar las dos cadenas en main, 29/10/2026. No autoriza de forma general publicaciones, gastos, datos personales, contactos, experimentos ni merges futuros.

Pregunta técnica: ¿pueden coexistir los análisis de PR3–13/#22 y PR23–25 con las correcciones concurrentes de main sin perder archivos, cambiar resultados o reintroducir estados obsoletos?

Entradas fijadas: main 13ccbc5c9f1c9744c57ed9abb822d169772e32a5; cadena antigua e3ca351d5bf79430abf283b12f65862e363bc707; reciente 963b176436907be0ba265bd2ff9c4a2f2e05d45a. Inventario remoto de archivos/PR antes de editar. No ejecutar material recibido ni importar nuevos datos.

Método: unión de blobs verificados; preferir reciente en seis diferencias comunes, salvo README/STATE/BACKLOG que se reescriben. Conservar snapshots de vigilancia recientes. Reunir CI offline en una matriz 3.11/3.12. Anotar límites históricos sin recalcular efectos. Crear commit con main y ambas cabezas como padres, PR de consolidación y merge preservando historia después de checks.

Predicción refutable: todos los scripts/tests y tablas de datos existentes conservan sus blobs; la suite conjunta pasa 105 tests. Las diferencias documentales/workflow se enumeran explícitamente. Ningún archivo único de entrada desaparece salvo el workflow offline duplicado.

Criterio de fracaso: diferencias sin justificación, pérdida de archivo/commit, cambio de resultados, tests fallidos o cambios concurrentes de main sin revisar. Detener integración, registrar causa y corregir; no forzar main ni reescribir ramas originales.

Verificación: hashes Git de archivos, tablas y fuentes; unittest completo, compilación y checks CI del PR. Revisar main/PR al terminar y actualizar continuidad Work. No cerrar issues científicas por integrar entregables; conservar ramas si la herramienta no permite borrado seguro.
