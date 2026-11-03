# B4 local: política y cómputo ligados al ledger — 02/11/2026

Base PR36:b6522a94689eee057b7abddb72bde7b5497b37dc.
Pregunta: ¿puede una fase compacta verificarse/reutilizarse solo con fuente,
dependencias, recursos, clocks y resultado concordantes, sin reiniciar presupuestos?

Antes de ejecutar: fixtures SAM existentes, reloj inyectado para controles de
deadline y worker local supervisado. Sin URL externa, datos biológicos, índice
humano, alineamientos o habilitación de producción. Compatibilidad de runners
históricos sin política nueva; ninguna conversión automática de un ledger viejo.

Política opt-in fijada por fingerprint: plazo total, transporte acumulado (incluye
fallos/reintentos dentro de una fase), caps de fase, subfases productor/reducción,
RSS y RLIMIT_AS distintos, y particiones de disco cuya suma cabe en el total.
Guardas cooperativas y supervisor externo; no garantía kernel de RSS/disco ni
tiempo real. Un salto atrás de reloj se rechaza; reabrir no reinicia deadline.

Cómputo local: source_scope=existing-synthetic-sam-only, transferencia verificada,
biblioteca/objetivos/cotas/política de cobertura, versión/hash de PySAM/HTSlib
bindings y scripts. Recibo final con SHA de resultado; rehash al reabrir/reusar.
Fase failed/started impide continuación, aunque el pipeline haya dejado verified.

Cobertura prospectiva: exigir al menos20grupos aceptados(RG,QNAME) con una o más
uniones objetivo, ancla15. Contar cada grupo una vez en la unión de objetivos;
registrar también suma de soportes por evento. Nunca llamar moléculas únicas a
estos grupos: duplicados marcados se retienen y no hay UMI. Esta precisión cambia
el borrador anterior de suma solapada antes de datos reales; conservar su historia.

Predicción refutable: éxito/reuso conserva clocks/consumo/resultados; alteraciones
de hash/identidad/dependencias/caps fallan; fase/subfase/transporte acumulado se
detienen con fakeclock y timeout real local; soporte de dos objetivos por grupo
da suma2/unión1. Negativos incluyen recibo/resultado/fuente cambiados, fase parcial,
presupuestos incoherentes y relleno de disco. No ampliar cobertura insuficiente.

Entrega adicional: política humana solo de planificación, total9000s, transporte
3600s,15/8anclas,2CPU,6GiBRSS y8GiBAS por proceso como cotas explícitas a revisar
en entorno real.25GiB se particionan y se reserva8GiB libre; no benchmark o
presupuesto activado. Si pasa, cerrar B4como diseño/componente local; B1/B5siguen.
