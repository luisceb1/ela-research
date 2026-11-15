# Linked Zenodo catalogue check — 15 November 2026

## Outcome

**No eligible library-linked junction-count entry identified in this finite catalogue inspection.** Close the public processed-count availability task; no ZIP/count/raw-data download or new candidate is scheduled. This is not proof that every archive member lacks useful data or that all public sources are exhausted.

Prospective protocol [here](../../research/plans/2026-11-15-gse299341-zenodo-catalogue.md) was committed before requests. Sole deposit [Zenodo15298524](https://zenodo.org/records/15298524), explicitly linked in the previously reviewed primary article. Three requested metadata resources: landing page, ZIP preview and API; API route failed via the web tool. No direct HTTP body acquisition; origin network-byte accounting is unavailable from the web service, so no zero-origin-byte claim. No fourth request required after the catalogue decision.

## Traceable catalogue evidence

| Resource | Observed metadata | Implication |
|---|---|---|
| Record15298524 | Version1, published28April2025; description identifies a supplementary-code snapshot and links NIH-CARD/Neurite-WT-RBP-KD. | Linked archive, not an independently new experiment or a claim of donor replication. |
| Listed payload | Neurite-WT-RBP-KD-main.zip,390.4MB advertised; listed MD5 b1eddb914ed2e84af4e18cd58ee50d89. | Advertised checksum not verified because ZIP was not downloaded. |
| Public preview | Exposes RNA metadata/scripts/QC, expression files and figure3/data/tdp_kd_whole_cell_junctions.tsv,85.9MB rounded. | Named junction-table entry corresponds by path/rounded size to the already inspected GitHub candidate; byte identity between repositories is unverified. |
| Other displayed entries | RNA_DE/raw_counts.tsv and WT Salmon outputs are also listed. | Names/known script roles do not establish exact per-library junction support. No gene counts were substituted for junction counts. |
| API attempt | Web tool could not access api/records/15298524. | Route failure retained; not absence of the record/data. |

[Returned preview/API evidence](retrieval.json) preserves the tool-provided text and errors, not original server bytes. [Public ZIP preview](https://zenodo.org/records/15298524/preview/Neurite-WT-RBP-KD-main.zip?include_deleted=0). The printed preview was compared to the previously [pinned GitHub tree](../gse299341-artifact-inspection-20261115/repository-tree.json) for relevant named entries; no byte-level archive equivalence or exhaustive content validation was performed. The known table's [count-schema rejection](../gse299341-junction-schema-20261115/REPORT.md) is not automatically transferred to an unverified different archive member; no new eligible member was identified.

## Recommendation and stop

PR80 now contains the bounded design review, code/sample-QC inspection, exact aggregate-table schema rejection and linked-archive catalogue check. Stop further small search extensions on this source. Raw execution remains unselected, with molecular dedup/run linkage and RNA culture/batch provenance unresolved.

Next discriminating input is concrete library-linked junction support with coordinate/filter definitions, or substantive existing-author clarification/verified ADWB inventory. The recorded request acknowledgment is not active workspace access. No reminder/contact, cloud spend, raw pipeline, marker expansion or merge follows this inspection. Preserve all prior positive/negative results; no target measurement was run and no absence/causal/functional/clinical conclusion is inferred.

