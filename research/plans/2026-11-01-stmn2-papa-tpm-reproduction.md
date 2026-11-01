# Reproducción prospectiva de PPAU desde TPM — aún no ejecutada

Antecedente: el contraste preregistrado counts/suma(counts) frente a PPAU falló en las doce bibliotecas; se conserva sin modificar fórmula ni tolerancia en reports/stmn2-papa-reproduction-20261101. El código de PAPA define PPAU mediante TPM/suma(TPM), mientras que las cuentas exportadas usan lengthScaledTPM. Este plan nuevo no convierte el ensayo anterior en un éxito.

Pregunta: ¿la tabla TPM del mismo directorio y versión reproduce la PPAU publicada por biblioteca para STMN2?

Antes de recuperar la tabla se fija:

- Versión Zenodo15538003, mismo directorio Humphrey; miembro summarised_pas_quantification.tpm.tsv. Usar el índice ya recuperado para fijar offset/tamaños/CRC, sin redescargar el ZIP.
- Gene_id exacto ENSG00000104435.14; numerador ENSG00000104435.14_1; denominador suma de **todos** los grupos del gen en la tabla completa TPM. Conservar los grupos; no limitar a dos por conveniencia ni usar la matriz génica GEO como denominador.
- Enlace explícito de doce etiquetas autores↔biblioteca↔GSM ya verificado. No seleccionar por condición, efecto o profundidad; sin parejas deducidas de sufijos.
- Unidades: proporciones, según código PAPA fijado en measurement_definition.json del contraste anterior. No elegir una escala según la concordancia observada.
- Tolerancia absoluta por biblioteca1e-6; todas deben pasar. Si denominador cero: indeterminado, no imputar cero. Si falta grupo/columna/identidad, detener.
- No medias de grupos, p-valores, significación, función, inferencia clínica o nueva replicación independiente. La concordancia solo reproduce aritmética sobre insumos de autores.

Salida: tabla TPM numerador/denominador, proporción calculada, PPAU original, diferencia y estado por biblioteca; hashes, código y controles. Si hay fallo, preservarlo y cerrar sin sustituir tablas o alterar tolerancia. Aprobación de una descarga grande o envío a autores no forma parte de esta fase.
