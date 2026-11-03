# Extracción y comprobación local del índice recuperado

Recuperación realaportada porLuis: archivo4.355.786.349B/SHA18487844…verificado,
externoexit0/grupovacío. Tramo2.723.339.065Ben148,515s; total167,457s,
RSS26,81MiBsolo deldescargador. No extrapolar alalineamiento. Ambosrecibos de
terminalnormalizadoscoinciden conSHAregistrado enelsello aportado.

Este paso no descarga, extraeFASTQ oalinea. Usaelarchivorecuperado, no repiteS3.
CompruebaSHAcompleto, nuevearchivos exactos/ochoht2+receta sin ejecutarla,
tamaños/hashes/CRC; HISAT2inspector comprueba resumenchr19/longitud58617616.
No afirmaigualdad de secuenciaentera o validaciónbiológica.

## Comando desde PowerShell

Despuésdeactualizar alSHAcomunicadoenelchat:

```powershell
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-research-piloto/scripts/prepare_verified_index.py --recovery /home/luisceb/ela-piloto-real-01-index-recovery-01 --aligner /home/luisceb/ela-tools/hisat2-2.2.3/hisat2-align-s
```

Paso localnuevo≤900s(15min), conpreflight120s/extracción600s/inspector120s,
60smargen;2CPU,RSSglobal6GiB/AS8GiB; fases512MiB/1GiB/6GiBRSS y1/2/8GiBAS.
Conteodisco≤25GiBparaoriginal+recuperación+salidas,reserva8GiB. Verificaespacio
antesdeempezar. Descargaadicional0B, cargoprevio4.355.802.733Binalterado;
plazosprevios no se renuevan. Puede trabajar sinmensajes hasta elJSONfinal.

Directoriodesalidaexclusivo:
/home/luisceb/ela-piloto-real-01-index-recovery-01-extracted-01
No sobrescribe, reabre o adopta intentosfallidos. Conservar originales,archivo
recuperado,parciales yrecibos. Si falla,no repetir ni extraermanualmente.

Éxitoesperado: statussealed_verified_extracted_index,member_count9,
new_transfer_bytes0,remaining_body_budget_bytes7644197267,
raw_execution_readyfalse. Pasa elJSONfinalalchat. Si falla,pasaeltraceback;
losdetallesestánen supervision/run.log deldirectoriodesalida.

Esto prepara referencia. Todavía falta ligar elíndice/recibos/cargos alpiloto
sinrehacerHTTPy decidir ejecución de lecturas. No relanzar eljobviejo o copiar
uníndicecomo cache sinprocedencia revisada. No PSI,p-valores o hallazgosELA.

Guardasdisco/RSSmuestreadas,nocuotasduras o tiemporeal. Pérdida delsistema,
I/Oininterrumpible/procesosdesacoplados/hosthostil conservan límitesprevios.
