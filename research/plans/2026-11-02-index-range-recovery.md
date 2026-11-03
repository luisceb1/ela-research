# Recuperación explícita del índice, sin FASTQ/alineamiento

Auditoría aportada porLuis: parcial1632447284B/SHAaf7750fc6ef148017aab8c339de670faebff34be5de69bddc0275dbeed21216d;
cargo1632463668B, diferencia16384Bque NOse reembolsa. Supervisor−9/grupovacío;
fingerprint/metadatos/aceptación consistentes. Resto delíndice2723339065B;
trasrecuperarlo,cargo4355802733B y saldo7644197267Bdelcaporiginal12GB.
No afirmar que elparcial seaverificado frente alorigen hastaSHAcompleto.

Pregunta: ¿permite una peticiónRange206fijada conservar elparcial yverificar el
archivo entero concontabilidad acumulada y reciboexterno sin tocar ejecución01?
Predicción: copiar/hashdelprefijo→Range[start,total−1]→SHAcompleto; solo entonces
promoción/sello. Datos sintéticos localessustituyen tamaño/SHAparapruebasinternas,
jamás enconfiguraciónCLIreal. Error200/rango/tamaño/version/CRC/hash/timeout o
salidaexternafallida deben impedir aceptación. Conservar todoslosfallos.

Propuesta revisable: solo archivo deíndice, una petición, sinretry/extracción/
FASTQ/alineamiento. Nuevo procesorecuperación hasta2400s:copy/auditoría300,
transporte1800yverificación300; RSS512MiB/AS1GiB,2CPU. Originaldeadliney3600s
gastados permanecen intactos. Nueva ventana es ampliación expresa detiempo,
no reanudación bajo plazoviejo; transporteacumulado previo+1800≈5400s. Capbytes
original12GBincluye16384Bsinarchivo; disco25GiBcuentaoriginal+nuevo+reserva8GiB.

Directoriorecuperaciónúnico derivado deloriginal yexclusivo; si existe, no se
reintenta ni cambia automáticamente. --prepare soloaudita y emiteplan deshabilitado;
--execute exige aceptarSHAexactodelplan yacknowledgement explícito delnuevo tiempo.
No descargar aquí; ensayos soloHTTPloopback. DespuésLuisprepara/revisa configuración;
aprobación sobreestealcance/tiempos concretos precede cualquier peticiónS3futura.
