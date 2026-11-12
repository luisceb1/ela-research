import csv,json,pathlib,hashlib,collections,shutil,re
repo=pathlib.Path('/workspace/scratch/9fdc55a9cfb9/ela-recount3-stageA');out=repo/'reports/recount3-metadata-stageA-20261112';cache=pathlib.Path('/workspace/scratch/9fdc55a9cfb9/stageA-cache')
summ=json.loads((cache/'series_summaries.json').read_text())['result'];dis=json.loads((cache/'discovery.json').read_text());log=json.loads((cache/'retrievals.json').read_text());maps=json.loads((cache/'selected_library_maps.json').read_text())
prior={
'GSE304550':'Alessandrini previously inspected;exact accession in prior inventory',
'GSE304548':'Alessandrini same PMID41389796;named in prior source audit;no independent new family',
'GSE304547':'Alessandrini same PMID41389796;named in prior source audit;RIP modality',
'GSE296716':'same Humphrey APA family PMID41120751;modality not new family',
'GSE296714':'closed Humphrey/pilot family;exact prior accession',
'GSE296711':'same Humphrey APA family PMID41120751;neuroblastoma dose-curve modality',
'GSE296710':'same Humphrey APA family PMID41120751;not new independent data by accession',
'GSE97262':'Brown reused neuroblastoma source already documented in recount3 report',
'GSE296063':'UPF1-only condition;same PMID40737092 as GSE299341;not additional TDP43 contrast',
'GSE290437':'same named Rapid and Inducible Mislocalization study as prior relocalization family;miRNA modality',
'GSE182976':'Ma targeted amplicon;already measured as SRP334561;explicit locked exclusion',
'GSE121569':'Klim already measured as SRP166282;explicit locked exclusion',
}
scopes={
'GSE298756':'DDX6-directed ARTR-seq;primary methods confirm antibody-guided assay;RNAseq sibling GSE298758 is same experiment family',
'GSE308462':'postmortem cortex cohort,not a matched experimental TDP43 depletion/control design',
'GSE272626':'postmortem spinal-cord cohort,not a matched experimental depletion design',
'GSE272624':'postmortem cortex cohort,not a matched experimental depletion design',
'GSE271156':'postmortem snRNA-seq;not conventional whole-transcriptome bulk depletion/control',
'GSE252200':'C9orf72 allele editing/ASO study,not the specified direct TDP43 depletion/control contrast',
'GSE124439':'postmortem cortex subtype cohort,not experimental TDP43 depletion',
'GSE67027':'GDS assay type is expression profiling by array;not RNA-seq junction source',
'GSE18632':'GDS assay type is expression profiling by array;listed assay samples HEK293E;not eligible neuronal RNAseq',
'GSE344875':'patient cortex and C9/control iPSC synaptosomes;three control lines do not create matched TDP43 depletion per background',
'GSE299976':'BORCS6 perturbation versus nontargeting sgRNA;not a direct TDP43-depletion contrast',
'GSE260532':'single-cell mechanical-injury organoids;not the specified bulk matched TDP43-depletion assay',
'GSE259432':'mechanical injury versus sham;not direct matched TDP43-depletion contrast',
'GSE248847':'series overall design explicitly SH-SY5Y neuroblastoma cell line;not three independent neuronal backgrounds',
}
design={
'GSE252892':'all six relevant whole-transcriptome RNAseq libraries map to WA01;one background,not three',
'GSE307054':'two simple TDP43KD and two guide controls,all WTC-11;NMD co-depletions cannot supply new genetic backgrounds',
'GSE299341':'all ten relevant TDP43-experiment soma libraries map to WTC11;neurite fractions are not new backgrounds',
}
cols=['discovery_order','geo_series','series_title','declared_assay','declared_total_samples_not_independent_units','pubmed_ids','lineage_group','decision','reason','primary_locator','recount3_availability','eligible_for_stageB']
records=[]
for i,k in enumerate(summ['uids'],1):
 s=summ[k];acc=s['accession']
 if acc in prior:decision='prior_or_sibling_excluded';reason=prior[acc]
 elif acc in scopes:decision='scope_rejected';reason=scopes[acc]
 elif acc in design:decision='design_rejected';reason=design[acc]
 elif acc=='GSE298758':decision='metadata_pending_closed';reason='three biological replicates and paired KD/control stated;three donor/genetic backgrounds and differentiation linkage not established in inspected GEO and primary methods;no active waiting task'
 else:raise ValueError('unclassified record '+acc)
 group=('PMID'+','.join(s.get('pubmedids',[]))) if s.get('pubmedids') else acc
 records.append([i,acc,s['title'],s.get('gdstype','unknown'),len(s.get('samples',[])),','.join(s.get('pubmedids',[])),group,decision,reason,'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc='+acc,'not assessed after earlier eligibility failure;no count URL probed','no'])
with (out/'records.tsv').open('w') as f:w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(cols);w.writerows(records)
# Technical culture keys only: no postmortem subject metadata or clinical rows exported.
libcols=['geo_series','geo_sample','declared_title','cell_line','cell_type','declared_genotype_or_treatment','batch','source_sha256','source_url']
libs=[]
for series,gsms in maps.items():
 for gsm in gsms:
  b=(cache/(gsm+'_sample.attempt1.body')).read_bytes();t=b.decode()
  def vals(prefix):return '; '.join(line.split(' = ',1)[1] for line in t.splitlines() if line.startswith(prefix+' = ')) or 'not documented'
  chars=[line.split(' = ',1)[1] for line in t.splitlines() if line.startswith('!Sample_characteristics_ch1 = ')]
  def ch(key):return '; '.join(x[len(key)+2:] for x in chars if x.startswith(key+': ')) or 'not documented'
  libs.append([series,gsm,vals('!Sample_title'),ch('cell line'),ch('cell type'),'; '.join(x for x in chars if x.startswith(('genotype:','treatment:'))),ch('batch'),hashlib.sha256(b).hexdigest(),'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc='+gsm])
with (out/'library_metadata.tsv').open('w') as f:w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(libcols);w.writerows(libs)
focal=[
['GSE298758','3CTRshCTR and3TDP43shCTR standardRNAseq;day14;KD transduction8days','polyA whole-transcriptome;paired150bp;40million raw reads/sample reported in primary RNAseq methods;not independently recounted','generic i3Neurons field in all6relevant libraries;three genetic backgrounds not mapped','numeric efficiency linked to selectedRNAseq libraries/time not established in this inspection','batch4/7/2023 for6relevant libraries;differentiation-to-background map unresolved','no demonstrated prior-data reuse;distinct accession not proof of independence','metadata_pending_closed','GEO series,six GSM records;PMC13058276 RNA-seq and human iPSC methods;not borrowing other motor-neuron assays'],
['GSE252892','3scrambled and3TDP43shRNA wholeRNAseq;7days;3endseq kept separate','SMARTer stranded totalRNAseq;depth/read length not pursued after design failure','WA01 in all6relevant RNAseq libraries;one background','numeric linked efficiency not inspected after design rejection','differentiation batch key unverified;no inferential grouping fabricated','new record in this inventory;no independent-validation certification','design_rejected','GEO series;GSM8009878-8009883;cell line/treatment/library protocol'],
['GSE307054','2guide controls and2simple TDP43KD;day14;NMD combined arms excluded','stranded mRNA RNAseq;depth/read length not pursued after design failure','WTC-11 in4relevant libraries;one background;only2KD libraries','stableCRISPRi module stated;linked numeric efficacy not inspected','biological differentiation identifiers not documented in retrieved field map','no reuse certified;NMD perturbation arms not pooled','design_rejected','GEO series;GSM9214880-9214883;cell line/treatment protocol'],
['GSE299341','5nontargeting and5TDP43KD soma libraries;day17;neurite fractions kept separate','totalRNAseq paired-end/UMI protocol stated;numeric depth/read length not pursued after design failure','WTC11 in10relevant soma libraries;one background','CRISPRi treatment stated;linked numeric efficacy not inspected','sample numbers retained as technical labels,not inferred donor or batch IDs','same PMID asGSE296063 UPF1 arm;not a second independent family','design_rejected','GEO series;GSM9037603-9037607 andGSM9037613-9037617;cell line/processing'],
['GSE248847','RGNEF/TDP43 neuronal-like-cell study','RNAseq series;not processed after scope rejection','SH-SY5Y in series overall design;three independent neuronal backgrounds not established','not inspected after scope rejection','not inspected','new title not a new admissible neuronal model','scope_rejected','GEO series overall design explicitly SH-SY5Y'],
]
with (out/'focal_triage.tsv').open('w') as f:w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['series','contrast_timing','assay_depth_readlength','background_evidence','efficacy','batch_and_differentiation','independence','decision','locator']);w.writerows(focal)
(out/'discovery.json').write_text(json.dumps(dis,indent=2)+'\n');(out/'retrievals.json').write_text(json.dumps(log,indent=2)+'\n')
(out/'stageB_manifest.json').write_text(json.dumps({'stageA_status':'closed_no_eligible_source','eligible_projects':[],'stageB_authorized':False,'count_downloads':0,'coverage_assessed':False,'source_gate_reopened':False},indent=2)+'\n')
stats={'query_lock_commit':'3bbc9326a926a77e6224600a8250e189d5c679b3','original_plan_commit':'55ab5a8777887d855c19e8b3d725517deeb67473','queries_executed':len(dis['queries']),'queries_not_executed':['G3-Q2'],'stop_reason':'30-distinct-series cap reached after G3-Q1','series_inspected':len(records),'request_attempts':len(log),'received_body_bytes':sum(x['bytes'] for x in log),'metadata_byte_cap':10_000_000,'status_counts':dict(collections.Counter(x[7] for x in records)),'technical_library_records_inspected':len(libs),'eligible_projects':0,'nominated_projects':0,'coverage_results':'not measured;StageB not authorized','retry_or_access_errors':[x for x in log if x.get('error')],'source_headers_tls_overhead_bytes':'not measured;payload bodies only'}
(out/'execution_summary.json').write_text(json.dumps(stats,indent=2)+'\n')
# Preserve executed acquisition code as a historical audit snapshot, not a runnable repository executor.
exe=out/'execution_snapshot';exe.mkdir(exist_ok=True)
for name in ['transport.py','discover.py','inspect_series.py','inspect_samples.py','finish_unitmap.py','inspect_dcps_methods.py','build_outputs.py']:
 shutil.copyfile(cache/name,exe/name)
(exe/'README.md').write_text('''# Historical execution snapshot\n\nThese are the actual Stage A scripts used on 12 November 2026. They contain the original scratch-cache paths and are not a supported repository CLI. `transport.py` enforces received-body caps and logs HTTP errors; discovery consumes the committed query lock. Execution order: discover, inspect_series, inspect_samples, finish_unitmap, inspect_dcps_methods, build_outputs. No junction-count file is fetched.\n\nRaw responses are not versioned. To reproduce acquisition, use the exact locked terms/parameters and URL manifest with a fresh isolated cache, retaining caps and failures; changed live records may differ. Do not run these snapshots blindly or mistake their cache paths for delivered data. Source hashes authenticate received bytes, not biological validity. Selected source fields and complete decisions are in the parent report directory; no clinical sample table is delivered.\n''')
print(json.dumps(stats,indent=2))
