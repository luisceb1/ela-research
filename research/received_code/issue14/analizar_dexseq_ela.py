from pathlib import Path
import hashlib, json, shutil, zipfile, sys
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SRC=Path('GSE121569_dexseq-all.csv.gz')
ROOT=Path('salida')
ROOT.mkdir(exist_ok=True)
T={'STMN2':'ENSG00000104435','UNC13A':'ENSG00000130477','TARDBP':'ENSG00000120948'}
CE={'STMN2':('chr8',80529057,80529284,'STMN2 CE 2a'), 'UNC13A':('chr19',17753223,17753350,'UNC13A CE 128 bp')}
OUT=ROOT/'resultados'; OUT.mkdir(exist_ok=True)

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()

def main(infile=SRC,root=ROOT):
 root.mkdir(parents=True,exist_ok=True); out=root/'resultados';out.mkdir(exist_ok=True)
 rows=0; chunks=[]; ncols=0; na_symbols=0
 for x in pd.read_csv(infile,compression='infer',chunksize=60000,low_memory=False):
  rows+=len(x); ncols=len(x.columns);na_symbols+=int(x['symbol'].isna().sum())
  hit=x[x['groupID'].isin(T.values())|x['symbol'].isin(T.keys())]
  if len(hit):chunks.append(hit)
 d=pd.concat(chunks,ignore_index=True)
 d['gen']=d['groupID'].map({v:k for k,v in T.items()})
 assert not d['gen'].isna().any()
 assert len(d)==d.fragment.nunique(), 'filas duplicadas'
 keepcols=['gen','fragment','groupID','featureID','genomicData.seqnames','genomicData.start','genomicData.end','genomicData.width','exonBaseMean','scrambled','als','log2fold_als_scrambled','pvalue','padj']
 keepcols += [x for x in d.columns if x.startswith('countData.')]
 d[keepcols].to_csv(out/'fragmentos_diana_detalle.csv',index=False)
 sig=d[d.padj<0.05].copy().sort_values(['gen','padj'])
 sig[keepcols].to_csv(out/'fragmentos_significativos.csv',index=False)
 summary=[];cov=[]
 for gene,ens in T.items():
  z=d[d.gen==gene]
  summary.append({'gen':gene,'fragments':len(z),'padj_evaluable':int(z.padj.notna().sum()),'padj_NA':int(z.padj.isna().sum()),'fdr_0_05':int((z.padj<0.05).sum()),'fdr_0_10':int((z.padj<0.1).sum()),'min_padj':float(z.padj.min()) if z.padj.notna().any() else None})
  if gene in CE:
   chrom,start,end,label=CE[gene]
   ov=z[(z['genomicData.seqnames']==chrom)&(z['genomicData.start']<=end)&(z['genomicData.end']>=start)]
   zz=z.assign(distance=np.maximum.reduce([start-z['genomicData.end'].to_numpy(),z['genomicData.start'].to_numpy()-end,np.zeros(len(z),dtype=int)]))
   closest=zz.sort_values('distance').iloc[0]
   cov.append({'gen':gene,'CE':label,'assembly':'GRCh37/hg19','chr':chrom,'CE_start_inclusive':start,'CE_end_inclusive':end,'n_fragments_overlapping_CE':len(ov),'closest_fragment':closest.fragment,'distance_nearest_bp':int(closest.distance),'nearest_region_start':int(closest['genomicData.start']),'nearest_region_end':int(closest['genomicData.end']),'interpretation':'La tabla no incluye fragmento que cubra el CE; no estimar PSI ni inferir ausencia de CE.'})
 pd.DataFrame(summary).to_csv(out/'resumen_genes.csv',index=False)
 pd.DataFrame(cov).to_csv(out/'cobertura_exones_cripticos.csv',index=False)
 # PNG per gene: coefficient of DEXSeq vs genomic position, significant annotated
 for gene in ['STMN2','UNC13A']:
  z=d[(d.gen==gene)&d.padj.notna()].sort_values('genomicData.start')
  x=z['genomicData.start'].to_numpy()/1e6
  fig,ax=plt.subplots(figsize=(10,4.2))
  ax.axhline(0,linestyle='--',linewidth=.8)
  ax.scatter(x,z.log2fold_als_scrambled,alpha=.6,label='Fragmentos con padj evaluable')
  ss=z[z.padj<.05]
  ax.scatter(ss['genomicData.start']/1e6,ss.log2fold_als_scrambled,marker='D',s=55,label='padj < 0.05')
  for _,r in ss.iterrows():
   ax.annotate(str(r.featureID), (r['genomicData.start']/1e6,r.log2fold_als_scrambled),xytext=(5,8),textcoords='offset points',fontsize=8)
  chrom,start,end,_=CE[gene]
  ax.axvspan(start/1e6,end/1e6,alpha=.16,label='Exón críptico (no cubierto)')
  ax.set_xlabel('Posición genómica, GRCh37 (Mb)')
  ax.set_ylabel('DEXSeq: cambio log2 en uso exónico relativo')
  ax.set_title(f'{gene} — Fragmentos anotados y localización del exón críptico')
  ax.legend(loc='best',fontsize=8)
  fig.tight_layout();fig.savefig(out/f'{gene}_fragmentos_ubicacion.png',dpi=175);plt.close(fig)
 record={'file':str(infile),'sha256':sha(infile),'n_rows':rows,'n_columns':ncols,'n_missing_symbols':na_symbols,'n_target_fragments':len(d),'genes':summary,'ce_coverage':cov,'notes':['DEXSeq exon-part usage is not junction-count PSI','Original authors provided adjusted p-values','2 independent differentiations per original paper']}
 (out/'auditoria.json').write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
 return d,sig,summary,cov,record

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--dexseq',type=Path,default=SRC);p.add_argument('--out',type=Path,default=ROOT)
 a=p.parse_args(); d,sig,summary,cov,record=main(a.dexseq,a.out)
 print(json.dumps({'sha256':record['sha256'],'rows':record['n_rows'],'genes':summary,'ce_coverage':cov,'sig':sig[['gen','featureID','padj']].to_dict('records')},indent=2,ensure_ascii=False))
