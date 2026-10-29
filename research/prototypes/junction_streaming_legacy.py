"""Reviewed legacy function excerpts: intentionally retained to reproduce parser defect.
No patient/sample metadata, reporting CLI or analysis-by-person code included.
Source ZIP/function hashes and original line ranges are in source_inventory.json.
"""
import gzip
from collections import defaultdict

def attr_value(attr,k):
 q=k+' "'; i=attr.find(q)
 if i<0:return None
 i+=len(q); j=attr.find('"',i)
 return attr[i:j]

def parse_bambu(path, count_map):
 # Los exon records de cada transcrito son consecutivos en estos GTF.
 models={}; missing=set(count_map); nonensg=0; nlines=0
 curr=None; exons=[]; chromosome=None; strand=None; gene_id=None
 def flush():
  nonlocal nonensg
  if curr is None or not exons or curr not in count_map:return
  g=gene_id.split('.')[0]
  if not g.startswith('ENSG'):
   nonensg+=1; missing.discard(curr); return
  count_gene=count_map[curr][0].split('.')[0]
  if g!=count_gene: raise ValueError(f'GTF/Count gene conflict {curr}: {g} {count_gene}')
  es=sorted(set(exons))
  jun=tuple((chromosome,es[i][1]+1,es[i+1][0]-1,strand) for i in range(len(es)-1) if es[i][1]+1<es[i+1][0])
  models[curr]=(g,jun, count_map[curr][1],len(es))
  missing.discard(curr)
 with gzip.open(path,'rt') as f:
  for line in f:
   nlines+=1
   if line.startswith('#'):continue
   a=line.rstrip('\n').split('\t')
   if len(a)!=9:continue
   if a[2]!='exon' and a[2]!='transcript':continue
   tx=attr_value(a[8],'transcript_id')
   if tx!=curr:
    flush();curr=tx;exons=[]; chromosome=a[0];strand=a[6];gene_id=attr_value(a[8],'gene_id') or ''
   if a[2]=='exon' and curr in count_map:exons.append((int(a[3]),int(a[4])))
  flush()
 if missing: raise ValueError(f'No se encontraron {len(missing)} BambuTx con recuentos en el GTF; ejemplos {list(missing)[:3]}')
 return models,dict(lines=nlines,bambu_annotated=len(models),bambu_without_ensg=nonensg)

def tx_junctions(models):
 d=defaultdict(lambda:defaultdict(list))
 for tx,(g,js,counts,nexon) in models.items():
  if sum(counts)==0:continue
  for j in js:
   d[g][j].append((tx,counts,nexon))
 return d

def internal_ref(path,targets):
 # Uniones ENST coincidentes con uniones BambuTx: no se almacena la referencia completa.
 found=set();seen=0;tx_last=None; exons=[];chr_=None;strand=None;gene_id=None
 def flush():
  if not exons or gene_id not in targets:return
  ex=sorted(set(exons))
  for i in range(len(ex)-1):
   j=(chr_,ex[i][1]+1,ex[i+1][0]-1,strand)
   if j in targets[gene_id]:found.add((gene_id,j))
 with gzip.open(path,'rt') as f:
  for line in f:
   if line.startswith('#'):continue
   a=line.rstrip('\n').split('\t')
   if len(a)!=9 or a[2] not in ('exon','transcript'):continue
   tx=attr_value(a[8],'transcript_id')
   if tx!=tx_last:
    flush();tx_last=tx;exons=[];chr_=a[0];strand=a[6];gene_id=(attr_value(a[8],'gene_id') or '').split('.')[0]
   if tx.startswith('ENST') and a[2]=='exon' and gene_id in targets:
    exons.append((int(a[3]),int(a[4])))
  flush()
 return found
