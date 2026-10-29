# Reconciliar21frente a1910uniones, issue20

Fuente original recuperada: ZIP15185bytes, SHA25673edc0006287f355001f968ce12f54d38a148535c05f7195f2db83e636215393. Siete miembros verificados por CRC y hash; código leído, aún no ejecutado al fijar este plan.

Pregunta: ¿las21uniones del paquete original son el subconjunto con soporte uniqueCounts positivo de las1910del catálogo, o existe pérdida de estructura por el parser que asume exones consecutivos por transcrito?

Hipótesis refutables: (H1) excluir modelos de suma0explica la diferencia; (H2) la agrupación consecutiva del parser original fragmenta/reescribe modelos o referencias ENST y altera la intersección. También comprobar deduplicación de exones, convención intrónica1-based y gen/cromosoma/hebra.

Controles: cuatro SHA256 idénticos a auditorías; mismo orden explícito de condiciones, grupos publicados3/3/2sin reconstruir datos clínicos; comparar conjuntos de claves exactas del CSVoriginal, con separación de totales de catálogo, positivos y exclusiónENST. Fixture de exones intercalados y modelos con cuenta0antes de analizar datos reales.

Método: ejecutar solo funciones revisadas del código original en caché y métodos de cruce actuales; no CLI que exporta columnas individuales. Salidas nuevas solo claves estructurales y resúmenes agregados. No pvalores, causalidad, proteína o novedad. Una tabla de21eventos no constituye otra cohorte.

Fracaso: diferencia no explicada o cambio de claves se conserva como tal. No forzar21ni1910; registrar errores y criterio exacto. Si un parser falla, corregir/verificar antes de interpretar filtros. Entregar código, pruebas, manifest y conclusión limitada por PR, sin cerrarissue ni fusionar.
