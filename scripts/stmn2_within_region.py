"""Fixed exploratory rank associations within tissues; no tissue correction or p-values."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
from stmn2_composition_gate import baseline, read_st7, validate_vectors
from stmn2_rin_sensitivity import read_qc, compatibility, qc_pass


def ranks(values):
    arr=np.asarray(values,dtype=float)
    if not np.isfinite(arr).all():raise ValueError('nonfinite rank input')
    order=np.argsort(arr,kind='stable');out=np.empty(len(arr),dtype=float);i=0
    while i<len(arr):
        j=i+1
        while j<len(arr) and arr[order[j]]==arr[order[i]]:j+=1
        out[order[i:j]]=(i+j-1)/2+1;i=j
    return out


def pearson(x,y):
    x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=float)
    x=x-x.mean();y=y-y.mean();den=float(np.linalg.norm(x)*np.linalg.norm(y))
    return float(np.clip(np.dot(x,y)/den,-1,1)) if den>1e-10 else None


def spearman(x,y,minimum=10):
    return pearson(ranks(x),ranks(y)) if len(x)>=minimum else None


def residual_correlation(x,y,design):
    design=np.asarray(design,dtype=float)
    if not np.isfinite(design).all():return None,'nonfinite_design'
    if np.linalg.matrix_rank(design)!=design.shape[1]:return None,'singular_design'
    if np.linalg.cond(design)>1e8:return None,'ill_conditioned_design'
    rx=x-design@np.linalg.lstsq(design,x,rcond=None)[0]
    ry=y-design@np.linalg.lstsq(design,y,rcond=None)[0]
    corr=pearson(rx,ry)
    return corr,'ok' if corr is not None else 'zero_residual_variance'


def partial(rows):
    x=[r['neuronal'] for r in rows];y=[r['ratio'] for r in rows]
    if len(rows)<20:return None,'insufficient_n'
    if min(len(set(x)),len(set(y)))<5:return None,'insufficient_distinct_values'
    design=np.column_stack([np.ones(len(rows)),ranks([r['rin'] for r in rows]),
                            ranks([np.log1p(r['total']) for r in rows]),
                            [r['prep']=='Automated KAPA Total' for r in rows]])
    return residual_correlation(ranks(x),ranks(y),design)


def require_vector(vectors, sample, reference):
    if (sample, reference) not in vectors:
        raise ValueError("missing valid composition vector")
    return vectors[(sample, reference)]


def attach(root):
    root=Path(root);pairs=baseline(root);vectors,bad,_=validate_vectors(read_st7(root/'source-gate/nygc-expression-tables.xlsx'))
    qc=defaultdict(list)
    for row in read_qc(root/'source-gate/nygc-metadata.xlsx'):qc[row['rna_id']].append(row)
    for pair in pairs:
        for i,(region,reference) in enumerate([('Cortex_Motor_Lateral','Cortex'),('Spinal_Cord_Cervical','Spinal Cord')]):
            r=pair[i];rin,reason=compatibility(r,qc[r['sample']],region)
            if reason:raise ValueError('QC linkage failed: '+reason)
            v=require_vector(vectors,r['sample'],reference)
            r['neuronal']=v['Excitatory']+v['Inhibitory'] if i==0 else v['Neurons']
            r['rin']=rin;r['total']=r['c']+r['k'];r['ratio']=r['k']/r['total']
    return pairs


def summary(rows,adjusted=True):
    x=[r['neuronal'] for r in rows];y=[r['ratio'] for r in rows]
    out={'n_donors':len(rows),'distinct_neuronal_values':len(set(x)),'distinct_ratio_values':len(set(y)),
         'zero_neuronal_estimates':sum(v==0 for v in x),'zero_cryptic_ratios':sum(v==0 for v in y),
         'spearman':spearman(x,y)}
    if adjusted:
        estimate,status=partial(rows);out['partial_rank_correlation']=estimate;out['partial_status']=status
        if estimate is not None:
            estimates=[];failures=0
            for i in range(len(rows)):
                value,_=partial(rows[:i]+rows[i+1:])
                if value is None:failures+=1
                else:estimates.append(value)
            out['leave_one_out']={'valid_estimates':len(estimates),'failed_estimates':failures,
                                 'min':min(estimates) if estimates else None,'max':max(estimates) if estimates else None,
                                 'same_sign_as_full':sum(v*estimate>0 for v in estimates)}
    return out


def run(root):
    root=Path(root);pairs=attach(root);quality=[p for p in pairs if qc_pass(p,6)]
    out={'evidence':'exploratory within-region associations, same 45 donors; no p-values or tissue-effect correction',
         'python':platform.python_version(),'numpy':np.__version__,'baseline_pairs':len(pairs),'rin_subset_pairs':len(quality),
         'regions':{}}
    for name,i in [('cortex',0),('cervical',1)]:
        out['regions'][name]={'neuronal_proxy':'Excitatory+Inhibitory (GSE140231)' if i==0 else 'Neurons (GSE190442)',
                              'main':summary([p[i] for p in pairs]),'rin_sensitivity_unadjusted':summary([p[i] for p in quality],False)}
    paths=[root/'source-gate/nygc-expression-tables.xlsx',root/'source-gate/nygc-metadata.xlsx',root/'project_global.source',root/'author_map.source',root/'jung_table.source',root/'repo/reports/stmn2-derivation-20261111/results_corteza.json',root/'repo/reports/stmn2-derivation-20261111/results_cervical.json']
    out['input_sha256']={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-root',required=True);p.add_argument('--output',required=True)
    args=p.parse_args();out=run(args.source_root);dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps(out['regions'],indent=2))
