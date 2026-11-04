# Final-article-linked ELK1 source reconciliation — 2026-11-04

## Outcome

The archive cited by the final paper was successfully inspected without downloading it in full. Six selected FISH files were extracted with exact HTTP Range checks, ZIP CRC verification and individual SHA256 hashes. The three input data files and plotting script are byte-identical to the pinned GitHub files. Therefore the archive **does not resolve the two replicate-1 deposited count-ratio discrepancies**.

The archived long table matches all 240 reconstructed rows (480 nucleus/focus count values), and all 84 numeric fields in its 12-row aggregate table match the R-specified arithmetic within 1e-12. This confirms the provenance of the intermediate calculation, including the doubled nucleus denominator. It does not establish why two separately deposited summary ratios differ.

## A. Published endpoint and source attribution

Final article: Bryce-Smith et al., Nature Neuroscience 28:2190–2200 (2025), published 21 October 2025, DOI [10.1038/s41593-025-02050-w](https://doi.org/10.1038/s41593-025-02050-w). [Primary text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12586162/), Fig.3g and data availability.

Fig.3g shows extranuclear FISH focus counts for shared/total and extension-specific ELK1 probes. Its caption reports ten images and within-replicate normalization with three replicates for testing. The page's statistical Source Data Fig.3 XLSX is explicitly for **Fig.3h**, a different fractionation assay. It cannot validate FISH counts. The Fig.3 PDF contains western blots, also a different endpoint. The article links a processed-data archive via DOI [10.5281/zenodo.15538002](https://doi.org/10.5281/zenodo.15538002), resolving on retrieval to record15538003.

## B. Numerical reconstruction

Using the archive's image counts, the means and within-replicate ratios of extranuclear counts are:

| Replicate | Probe | CTRL mean foci/image | KD mean foci/image | KD/CTRL |
|---|---|---:|---:|---:|
| 1 | Shared/total | 5.6 | 19.5 | 3.482143 |
| 2 | Shared/total | 6.3 | 33.5 | 5.317460 |
| 3 | Shared/total | 4.9 | 17.8 | 3.632653 |
| 1 | Extension-specific | 2.1 | 31.4 | 14.952381 |
| 2 | Extension-specific | 2.0 | 30.6 | 15.300000 |
| 3 | Extension-specific | 0.8 | 32.5 | 40.625000 |

`final-article/fig3g-image-counts.csv` contains 120 image/probe observations from 60 image rows; this is not 120 independent samples. `fig3g-endpoint.csv` preserves full-precision summaries. These counts per image are not foci per nucleus or nuclear:extranuclear localization ratios. In particular, a larger fold for the extension-specific probe does not prove a larger absolute molecular response: baseline counts differ.

This is reconstruction of the **published endpoint from final-paper-linked input**, not certification that every editorial plotted point came from these exact bytes. The archive includes generated plots, but no numeric panel-specific file-to-editorial mapping was established. No point digitization, P-value recomputation, R execution or independence validation was performed. The previously reported 7/9 agreement concerns different deposited per-nucleus/localization ratios and is not a 7/9 score for Fig.3g.

## Source retrieval and reproducibility

Archive: `2025-05-28__tdp43-apa__data.zip`, advertised size 831,190,727 bytes. Only **517,501 response-body bytes** were read across 14 strict HTTP206 requests, including a 65,557-byte end record window, 445,005-byte central directory and selected member headers/payloads. The configured ceiling was 5MiB. The full archive was not fetched and its advertised whole-file MD5 was not verified. Per-member CRC and SHA256 are recorded in `final-article/extracted-members.json`; byte ranges/response hashes in `range-receipt.json`. Metadata retrieval resolved the concept record to15538003; no unrelated dataset members were extracted.

The two retrieval helpers in `final-article/retrieval/` preserve the actual bounded procedure. From project root, with network access:

```bash
mkdir -p elk1-final-cache
python reports/elk1-fish-replay-20261104/final-article/retrieval/inspect_remote_zip.py
python reports/elk1-fish-replay-20261104/final-article/retrieval/extract_selected.py
python scripts/reconcile_elk1_archive.py --wet-dir elk1-final-cache/members/wet --output /path/comparison
```

The analysis verifies all six member hashes before parsing. It rejects mismatched aggregate keys and a changed long table; records aggregate-field agreement and exports the reconstructed endpoint. Original archive members are not republished. The original replay and its receipts remain available; later validation hashes identify amended reports separately. Inspection scripts are acquisition receipts for this archive, not a general ZIP library.

Access notes: the PMC XLSX link returned an HTML challenge; its advertised panel was already known to be3h, so no alternative workbook download was pursued. Web access to Zenodo metadata failed; direct bounded API access succeeded. No paid service, full ZIP, external contact, access request or merge was used.

## C. Conclusion and stopping rule

**Concordance:** raw-input identity, all long-table values, all aggregate numeric fields and reconstructable Fig.3g-style extranuclear summaries.

**Explained difference:** code pools image counts with a repeated nucleus denominator, while written methods describe image-level averages. The denominator issue cancels in fold changes and is irrelevant to raw extranuclear counts per image.

**Unresolved:** two older replicate-1 per-nucleus summary ratios, explicit donor/culture hierarchy and exact final editorial point identity. Their origin must not be inferred from convenient exclusions, candidate transcription errors or reverse-fitting.

Close this bounded computational task. A processing history or panel-keyed original export would be needed to settle the remaining discrepancies. This adds technical traceability, not new ELK1 biology, neuronal recovery, or evidence that an ELK1 intervention benefits ALS. #37/#44 and PR#48 remain unchanged; no new ELK1 study is scheduled.
