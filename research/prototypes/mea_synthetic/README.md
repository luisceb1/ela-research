# Prototipos MEA recibidos: archivo para auditoría de software

Fuentes propias del proyecto procedentes de dos ZIP generados en otros chats. Cinco archivos Python se conservan byte por byte y se identifican en `source_manifest.json`. Los ZIP completos, CSV sintéticos, gráficos e informes generados no se importan aquí. No contienen datos experimentales.

No ejecutar los CLI de generación, funciones de gráficos/informes ni consolidadores. Esta tarea reproduce solo las pruebas y el núcleo computacional revisado. Los módulos originales son un archivo de comparación y **no** el punto de entrada recomendado para nuevos datos. Sus validadores tienen los defectos documentados en `reports/mea-software-audit`.

Desde la raíz del repositorio:

```
python scripts/audit_mea_software.py
python -m unittest discover -s tests -v
```

El primer comando requiere las versiones registradas en requirements-audited.txt; no instala paquetes automáticamente. El segundo es la suite técnica estándar sin dependencias científicas, e incluye las pruebas del nuevo control previo `scripts/mea_input_qc.py`. Los tests originales se ejecutan por separado: seis de base y cinco de sensibilidad; no se cuentan como los tests estándar de GitHub.

El nuevo control solo acepta fixtures declarados sintéticos y no calcula efectos, potencia ni clasificación. No integra automáticamente el guard con el CLI histórico ni habilita importación real. Un protocolo experimental necesitaría validar métrica, unidades/tiempos, elegibilidad, exclusiones, estimando, pérdidas, cegamiento y modelo con dependencia. La muerte como0 pertenece al desenlace compuesto elegido; no representa que la sincronía haya sido observada como0 ni equivale a pérdida técnica.
